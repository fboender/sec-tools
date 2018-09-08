#!/bin/sh
#
# Convert Markdown man pages in docs/man/ to Groff formatted (real) man pages.
#

BASE_DIR=$(dirname $(realpath $0))
MAN_DIR=$BASE_DIR/../docs/man

for MD_MAN_FILE in $MAN_DIR/*.md; do
    echo "Converting $(basename $MD_MAN_FILE)"
    MAN_FILE=$(basename $MD_MAN_FILE .md)
    pandoc $MD_MAN_FILE -s -t man > $MAN_DIR/$MAN_FILE
    sed "/Automatically generated/,+1d" -i "$MAN_DIR/$MAN_FILE" 
done
