#!/usr/bin/env sh
set -eu

show_help() {
  cat <<'EOF'
Usage: setup-toolkit.sh [options]

Install the enterprise data engineering AI toolkit into a target repository.

Options:
  --target PATH       Target repository root. Defaults to the current directory.
  --bundle PATH       Toolkit bundle root. Defaults to this script's directory.
  --mode MODE         copy or symlink. Defaults to copy.
  --force             Replace existing toolkit-managed files.
  --help              Show this help text.

Examples:
  ./setup-toolkit.sh --target /work/customer-pipeline --mode copy
  ./setup-toolkit.sh --target /work/customer-pipeline --mode symlink
EOF
}

TARGET_ROOT="$(pwd)"
SCRIPT_DIR="$(CDPATH='' cd "$(dirname "$0")" && pwd)"
BUNDLE_ROOT="$SCRIPT_DIR"
INSTALL_MODE="copy"
FORCE="false"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      TARGET_ROOT="$2"
      shift 2
      ;;
    --bundle)
      BUNDLE_ROOT="$2"
      shift 2
      ;;
    --mode)
      INSTALL_MODE="$2"
      shift 2
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    --help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      show_help >&2
      exit 2
      ;;
  esac
done

TARGET_ROOT="$(CDPATH='' cd "$TARGET_ROOT" && pwd)"
BUNDLE_ROOT="$(CDPATH='' cd "$BUNDLE_ROOT" && pwd)"

if [ "$INSTALL_MODE" != "copy" ] && [ "$INSTALL_MODE" != "symlink" ]; then
  echo "Invalid --mode value: $INSTALL_MODE. Expected copy or symlink." >&2
  exit 2
fi

if [ ! -d "$TARGET_ROOT/.git" ]; then
  echo "Target path is not a Git repository: $TARGET_ROOT" >&2
  exit 2
fi

copy_or_link() {
  source_path="$1"
  target_path="$2"

  if [ "$source_path" = "$target_path" ]; then
    echo "Skipping source path already in place: $target_path"
    return 0
  fi

  if [ -e "$target_path" ] || [ -L "$target_path" ]; then
    if [ "$FORCE" = "true" ]; then
      rm -rf "$target_path"
    else
      echo "Skipping existing path: $target_path"
      return 0
    fi
  fi

  mkdir -p "$(dirname "$target_path")"

  if [ "$INSTALL_MODE" = "symlink" ]; then
    ln -s "$source_path" "$target_path"
  else
    if [ -d "$source_path" ]; then
      cp -R "$source_path" "$target_path"
    else
      cp "$source_path" "$target_path"
    fi
  fi

  echo "Installed: $target_path"
}

install_toolkit_assets() {
  mkdir -p "$TARGET_ROOT/.github"

  copy_or_link "$BUNDLE_ROOT/.github/copilot-instructions.md" "$TARGET_ROOT/.github/copilot-instructions.md"
  copy_or_link "$BUNDLE_ROOT/.github/instructions" "$TARGET_ROOT/.github/instructions"
  copy_or_link "$BUNDLE_ROOT/.github/agents" "$TARGET_ROOT/.github/agents"
  copy_or_link "$BUNDLE_ROOT/.github/skills" "$TARGET_ROOT/.github/skills"
  copy_or_link "$BUNDLE_ROOT/.github/commands" "$TARGET_ROOT/.github/commands"
  copy_or_link "$BUNDLE_ROOT/.github/hooks" "$TARGET_ROOT/.github/hooks"
  copy_or_link "$BUNDLE_ROOT/.github/mcp-servers" "$TARGET_ROOT/.github/mcp-servers"
  copy_or_link "$BUNDLE_ROOT/.github/plugin-manifest.yml" "$TARGET_ROOT/.github/plugin-manifest.yml"
  copy_or_link "$BUNDLE_ROOT/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
}

install_mcp_config() {
  vscode_dir="$TARGET_ROOT/.vscode"
  mcp_config="$vscode_dir/mcp.json"

  mkdir -p "$vscode_dir"

  if [ -e "$mcp_config" ] && [ "$FORCE" != "true" ]; then
    echo "Skipping existing MCP config: $mcp_config"
    return 0
  fi

  cat > "$mcp_config" <<'EOF'
{
  "servers": {
    "enterprise-bigquery": {
      "type": "stdio",
      "command": "${env:ENTERPRISE_BIGQUERY_MCP_COMMAND}",
      "args": [
        "--project",
        "${env:BIGQUERY_PROJECT_ID}",
        "--location",
        "${env:BIGQUERY_LOCATION}"
      ]
    },
    "internal-catalog": {
      "type": "stdio",
      "command": "${env:INTERNAL_CATALOG_MCP_COMMAND}",
      "args": [
        "--catalog-url",
        "${env:INTERNAL_CATALOG_URL}",
        "--auth-mode",
        "environment"
      ]
    }
  }
}
EOF

  echo "Installed MCP config: $mcp_config"
}

install_git_hooks() {
  hooks_dir="$TARGET_ROOT/.git/hooks"
  pre_commit_hook="$hooks_dir/pre-commit"

  mkdir -p "$hooks_dir"

  if [ -e "$pre_commit_hook" ] && [ "$FORCE" != "true" ]; then
    echo "Skipping existing Git hook: $pre_commit_hook"
    return 0
  fi

  cat > "$pre_commit_hook" <<'EOF'
#!/usr/bin/env sh
set -eu

files="$(git diff --cached --name-only --diff-filter=ACMR)"
if [ -n "$files" ]; then
  # shellcheck disable=SC2086
  node .github/hooks/pre-commit-guard.js $files
fi

dag_files="$(printf '%s\n' "$files" | grep -E '(^|/)dags?/.*\.py$' || true)"
if [ -n "$dag_files" ]; then
  # shellcheck disable=SC2086
  python .github/hooks/post-gen-validator.py --skip-airflow-if-missing $dag_files
fi
EOF

  chmod +x "$pre_commit_hook"
  echo "Installed Git hook: $pre_commit_hook"
}

install_toolkit_assets
install_mcp_config
install_git_hooks

cat <<EOF
Toolkit setup completed.
Target: $TARGET_ROOT
Bundle: $BUNDLE_ROOT
Mode: $INSTALL_MODE
EOF
