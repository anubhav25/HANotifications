#!/usr/bin/env sh

DIR="$(cd "$(dirname "$0")"; pwd)"

java -version >/dev/null 2>&1 || {
    echo "Java not found"
    exit 1
}

exec gradle "$@"