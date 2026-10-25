#!/usr/bin/env node
"use strict";

/**
 * Scans generated or staged content for secrets and high-risk PII before it is
 * written or committed. Pass file paths as arguments, or pipe content on stdin.
 */

const fs = require("fs");
const path = require("path");

const SECRET_PATTERNS = [
  {
    name: "AWS access key identifier",
    pattern: /\b(A3T[A-Z0-9]|AKIA|ASIA|AGPA|AIDA|AROA)[A-Z0-9]{16}\b/g,
  },
  {
    name: "GCP service account private key marker",
    pattern: /-----BEGIN PRIVATE KEY-----|private_key_id\s*[:=]\s*["'][a-f0-9]{16,}["']/gi,
  },
  {
    name: "Database connection string",
    pattern: /\b(?:postgres(?:ql)?|mysql|mariadb|sqlserver|mongodb(?:\+srv)?|redis):\/\/[^@\s:]+:[^@\s]+@[^/\s]+/gi,
  },
  {
    name: "Generic API token assignment",
    pattern: /\b(?:api[_-]?key|access[_-]?token|secret[_-]?key|client[_-]?secret)\b\s*[:=]\s*["'][^"'\s]{16,}["']/gi,
  },
];

const PII_PATTERNS = [
  {
    name: "Email address",
    pattern: /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi,
  },
  {
    name: "US Social Security number",
    pattern: /\b\d{3}-\d{2}-\d{4}\b/g,
  },
  {
    name: "Credit card-like number",
    pattern: /\b(?:\d[ -]*?){13,19}\b/g,
  },
];

function readStdin() {
  if (process.stdin.isTTY) {
    return "";
  }

  return fs.readFileSync(0, "utf8");
}

function readFileContent(filePath) {
  const resolvedPath = path.resolve(filePath);
  const stats = fs.statSync(resolvedPath);

  if (!stats.isFile()) {
    return null;
  }

  return {
    label: resolvedPath,
    content: fs.readFileSync(resolvedPath, "utf8"),
  };
}

function lineNumberForIndex(content, index) {
  return content.slice(0, index).split(/\r?\n/).length;
}

function scanContent(label, content) {
  const findings = [];

  for (const rule of [...SECRET_PATTERNS, ...PII_PATTERNS]) {
    for (const match of content.matchAll(rule.pattern)) {
      findings.push({
        source: label,
        line: lineNumberForIndex(content, match.index || 0),
        type: rule.name,
      });
    }
  }

  return findings;
}

function main() {
  const filePaths = process.argv.slice(2);
  const scanTargets = [];

  if (filePaths.length > 0) {
    for (const filePath of filePaths) {
      try {
        const target = readFileContent(filePath);
        if (target) {
          scanTargets.push(target);
        }
      } catch (error) {
        console.error(JSON.stringify({
          level: "error",
          event: "pre_commit_guard_read_failed",
          file: filePath,
          message: error.message,
        }));
        process.exitCode = 2;
        return;
      }
    }
  } else {
    scanTargets.push({
      label: "stdin",
      content: readStdin(),
    });
  }

  const findings = scanTargets.flatMap((target) => scanContent(target.label, target.content));

  if (findings.length > 0) {
    console.error(JSON.stringify({
      level: "error",
      event: "pre_commit_guard_blocked",
      finding_count: findings.length,
      findings,
    }, null, 2));
    process.exitCode = 1;
    return;
  }

  console.error(JSON.stringify({
    level: "info",
    event: "pre_commit_guard_passed",
    scanned_targets: scanTargets.length,
  }));
}

main();
