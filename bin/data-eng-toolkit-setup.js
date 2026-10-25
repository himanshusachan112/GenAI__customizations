#!/usr/bin/env node
"use strict";

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function candidateShells() {
  const candidates = [];

  if (process.env.SHELL) {
    candidates.push(process.env.SHELL);
  }

  candidates.push("sh", "bash");

  if (process.platform === "win32") {
    const programFiles = process.env.ProgramFiles || "C:\\Program Files";
    candidates.push(
      path.join(programFiles, "Git", "bin", "sh.exe"),
      path.join(programFiles, "Git", "usr", "bin", "sh.exe")
    );
  }

  return candidates;
}

function shellExists(shellPath) {
  if (path.isAbsolute(shellPath)) {
    return fs.existsSync(shellPath);
  }

  const probe = spawnSync(shellPath, ["-c", "exit 0"], { stdio: "ignore" });
  return !probe.error && probe.status === 0;
}

function resolveShell() {
  for (const shellPath of candidateShells()) {
    if (shellExists(shellPath)) {
      return shellPath;
    }
  }

  return null;
}

function main() {
  const shellPath = resolveShell();
  if (!shellPath) {
    console.error("Unable to find a POSIX shell. Install Git for Windows or run setup-toolkit.sh from a shell environment.");
    process.exit(2);
  }

  const scriptPath = path.resolve(__dirname, "..", "setup-toolkit.sh");
  const result = spawnSync(shellPath, [scriptPath, ...process.argv.slice(2)], {
    stdio: "inherit",
  });

  if (result.error) {
    console.error(result.error.message);
    process.exit(2);
  }

  process.exit(result.status === null ? 1 : result.status);
}

main();
