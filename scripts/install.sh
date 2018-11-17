#!/bin/sh

set -e

TARGET=/usr/local
TARGET_LIB=$TARGET/lib/sec-tools
TARGET_BIN=$TARGET/bin
TARGET_MAN=$TARGET/man/man1

echo "Installing into $TARGET..."

echo "Creating $TARGET_LIB"
mkdir -p $TARGET_LIB

# Install libs and data
echo "Installing libs and data into $TARGET_LIB"
install src/tools.py -m 644 $TARGET_LIB
cp -r src/reports $TARGET_LIB
cp -r src/sec-gather-misconfigs.d $TARGET_LIB

# Install binaries
echo "Installing binaries into $TARGET_LIB"
for BIN in $(find src -maxdepth 1 -executable -type f ); do
    BIN=$(basename "$BIN")
    install "src/$BIN" $TARGET_LIB
done

# Symlink binaries
echo "Symlinking binaries to $TARGET_BIN"
for BIN in $(find src -maxdepth 1 -executable -type f ); do
    BIN=$(basename "$BIN")
    TARGET_LINK="$TARGET_BIN/$BIN"

    if [ \! -f "$TARGET_LINK" ]; then
        ln -s "$TARGET_LIB/$BIN" $TARGET_BIN/
    fi
done

# Install man pages
echo "Installing man pages to $TARGET_MAN"
cp docs/man/*.1 "$TARGET_MAN"

echo "Installation complete. Run 'make uninstall' to remove"
