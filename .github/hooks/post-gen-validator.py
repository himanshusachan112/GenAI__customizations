"""Validate generated Airflow DAG files before presenting or committing them."""

from __future__ import annotations

import argparse
import ast
import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable


LOGGER = logging.getLogger("post_gen_validator")


def configure_logging() -> None:
    """Configure structured logging for hook execution."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def log_event(level: int, event: str, **context: object) -> None:
    """Emit a JSON-formatted hook event.

    Args:
        level: Logging level used for the event.
        event: Stable event name.
        **context: Additional JSON-serializable event context.
    """
    LOGGER.log(level, json.dumps({"event": event, **context}, sort_keys=True))


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Command line arguments excluding the executable name.

    Returns:
        Parsed arguments for generated DAG validation.
    """
    parser = argparse.ArgumentParser(
        description="Validate generated Airflow DAG Python files with AST syntax checks and airflow dags test.",
    )
    parser.add_argument("dag_files", nargs="+", help="Generated DAG Python files to validate.")
    parser.add_argument(
        "--dag-id",
        action="append",
        dest="dag_ids",
        help="DAG ID to test. Repeat for multiple DAGs. If omitted, DAG IDs are inferred from DAG(...) calls.",
    )
    parser.add_argument(
        "--execution-date",
        default="2024-01-01",
        help="Execution date passed to `airflow dags test`.",
    )
    parser.add_argument(
        "--skip-airflow-if-missing",
        action="store_true",
        help="Run syntax validation only when the Airflow CLI is unavailable.",
    )
    return parser.parse_args(list(argv))


def validate_python_syntax(dag_file: Path) -> None:
    """Validate Python syntax for a generated DAG file.

    Args:
        dag_file: Python DAG file to parse and compile in memory.

    Raises:
        SyntaxError: If the file contains invalid Python syntax.
    """
    source = dag_file.read_text(encoding="utf-8-sig")
    compile(ast.parse(source, filename=str(dag_file)), filename=str(dag_file), mode="exec")
    log_event(logging.INFO, "python_syntax_passed", file=str(dag_file))


def infer_dag_ids(dag_file: Path) -> list[str]:
    """Infer DAG IDs from common Airflow DAG constructor patterns.

    Args:
        dag_file: Python DAG file to inspect.

    Returns:
        Sorted unique DAG IDs found in `DAG(...)` constructor calls.
    """
    tree = ast.parse(dag_file.read_text(encoding="utf-8-sig"), filename=str(dag_file))
    dag_ids: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function_name = ""
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr

        if function_name != "DAG":
            continue

        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            dag_ids.append(node.args[0].value)
            continue

        for keyword in node.keywords:
            if keyword.arg == "dag_id" and isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                dag_ids.append(keyword.value.value)

    return sorted(set(dag_ids))


def run_airflow_dag_test(dag_id: str, dag_folder: Path, execution_date: str) -> None:
    """Run `airflow dags test` for one DAG ID.

    Args:
        dag_id: Airflow DAG identifier to test.
        dag_folder: Folder containing the generated DAG file.
        execution_date: Execution date passed to the Airflow CLI.

    Raises:
        RuntimeError: If the Airflow CLI is missing or DAG validation fails.
    """
    airflow_executable = shutil.which("airflow")
    if airflow_executable is None:
        raise RuntimeError("Airflow CLI is not installed or not available on PATH.")

    env = os.environ.copy()
    env["AIRFLOW__CORE__DAGS_FOLDER"] = str(dag_folder)

    command = [airflow_executable, "dags", "test", dag_id, execution_date]
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        log_event(
            logging.ERROR,
            "airflow_dag_test_failed",
            dag_id=dag_id,
            return_code=result.returncode,
            stderr=result.stderr[-4000:],
        )
        raise RuntimeError(f"airflow dags test failed for DAG '{dag_id}'.")

    log_event(logging.INFO, "airflow_dag_test_passed", dag_id=dag_id)


def main(argv: Iterable[str]) -> int:
    """Run generated DAG validation.

    Args:
        argv: Command line arguments excluding the executable name.

    Returns:
        Process exit code.
    """
    configure_logging()
    args = parse_args(argv)
    dag_files = [Path(dag_file).resolve() for dag_file in args.dag_files]

    for dag_file in dag_files:
        if not dag_file.is_file():
            log_event(logging.ERROR, "dag_file_missing", file=str(dag_file))
            return 2
        validate_python_syntax(dag_file)

    dag_ids = sorted(set(args.dag_ids or []))
    if not dag_ids:
        for dag_file in dag_files:
            dag_ids.extend(infer_dag_ids(dag_file))
        dag_ids = sorted(set(dag_ids))

    if not dag_ids:
        log_event(logging.ERROR, "dag_id_not_found", files=[str(dag_file) for dag_file in dag_files])
        return 2

    if shutil.which("airflow") is None and args.skip_airflow_if_missing:
        log_event(logging.WARNING, "airflow_validation_skipped", reason="airflow_cli_missing", dag_ids=dag_ids)
        return 0

    dag_folder = dag_files[0].parent
    for dag_id in dag_ids:
        run_airflow_dag_test(dag_id, dag_folder, args.execution_date)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as exc:
        log_event(logging.ERROR, "post_gen_validator_failed", message=str(exc))
        raise SystemExit(1) from exc
