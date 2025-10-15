#!/bin/bash
set -e

VERSION=0.17.1
SRC_DIR="source/libass-${VERSION}"

if [ ! -d "$SRC_DIR" ]; then
    echo "📥 Cloning libass ${VERSION}..."
    mkdir -p source
    git clone --branch ${VERSION} https://github.com/libass/libass.git "$SRC_DIR"
else
    echo "✅ libass source already exists: $SRC_DIR"
fi

