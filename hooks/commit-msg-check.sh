#!/usr/bin/env bash

COMMIT_MSG_FILE=$1
COMMIT_MSG="$(head -n 1 "$COMMIT_MSG_FILE")"

# Simple regex: requires the commit message to start with something like :bug:, :sparkles:, :tada:, etc.
if ! echo "$COMMIT_MSG" | grep -qE '^:\w+:'; then
  echo "ERROR: Commit message must start with :emoji: (e.g. ':sparkles: Add new feature')"
  echo "Please amend your commit message and try again."
  exit 1
fi

exit 0
