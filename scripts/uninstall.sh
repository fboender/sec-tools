#!/bin/sh

set -e

TARGET=/usr/local
TARGET_LIB=$TARGET/lib/sec-tools
TARGET_BIN=$TARGET/bin
TARGET_MAN=$TARGET/man/man1

echo "Uninstalling from $TARGET..."

# Remove symlinked binaries
echo "Removing symlinked binaries from $TARGET_BIN"
for BIN in $(find src -maxdepth 1 -executable -type f ); do
    BIN=$(basename "$BIN")
    TARGET_LINK="$TARGET_BIN/$BIN"

    if [ -f "$TARGET_LINK" ]; then
        rm "$TARGET_LINK"
    fi
done

# Uninstall libs, data and binaries
echo "Uinstalling libs, data and binarines from $TARGET_LIB"
rm -rf "$TARGET_LIB"

# Uninstall man pages
echo "Uinstalling man pages from $TARGET_MAN"
for MAN in docs/man/*.1; do
    F="$TARGET_MAN/$(basename "$MAN")"
    if [ -f $F ]; then
        rm "$F"
    fi
done

echo "Uninstallation complete."
