#!/bin/bash
# Author: Cody Lane
# Date: 9-3-2014

HOMEBREW_DIR="/usr/local/Cellar"

LIBXML2_DIR="$HOMEBREW_DIR/libxml2"
LIBXSLT_DIR="$HOMEBREW_DIR/libxslt"

PYTHON_BINDINGS_VER="2.6.21"
PYTHON_BINDINGS_URI="ftp://xmlsoft.org/libxml2/python/libxml2-python-${PYTHON_BINDINGS_VER}.tar.gz"

function err() {
  echo "ERR: $* exiting"
  exit 1
}

OS_TYPE=$(uname -s)

case "$OS_TYPE" in
  Darwin)
    # just continue
    ;;
  *)
    err "This version '$OS_TYPE' is not a reconginzed OSX version"
    ;;
esac

[ ! -d "$HOMEBREW_DIR" ] && err "You don't appear to have homebrew installed"

if [ ! -d "$LIBXML2_DIR" ]; then
  brew install libxml2 --with-python || err "Unable to install libxml2 binaries"
fi

if [ ! -d "$LIBXSLT_DIR" ]; then
  brew install libxslt --with-python || err "Unable to install libxslt binaries"
fi

LIBXML2_VER=$(ls $LIBXML2_DIR | tail -1)

[ -z "$LIBXML2_VER" ] && err "Unable to auto-detect libxml2 version from directory '$LIBXML2_DIR'"

LIBXSLT_VER=$(ls $LIBXSLT_DIR | tail -1)

[ -z "$LIBXSLT_VER" ] && err "Unable to auto-detect libxslt version from directory '$LIBXSLT_DIR'"

echo "[auto-detected the following required dependencies]"
echo "libxml2 version: $LIBXML2_VER"
echo "libxslt version: $LIBXSLT_VER"

LIBXML2_DIR="$LIBXML2_DIR/$LIBXML2_VER"
LIBXSLT_DIR="$LIBXSLT_DIR/$LIBXSLT_VER"

export LDFLAGS="-I${LIBXML2_DIR}/lib:-I${LIBXSLT_DIR}/lib"
export CPPFLAGS="-I${LIBXML2_VER}/include:-I${LIBXSLT_DIR}/include"

PYTHON_BINDINGS_TARGZ=$(echo "${PYTHON_BINDINGS_URI##*/}")

[ -f "$PYTHON_BINDINGS_TARGZ" ] || wget -O "$PYTHON_BINDINGS_TARGZ" "$PYTHON_BINDINGS_URI"

easy_install "$PYTHON_BINDINGS_TARGZ" || err "Unable to compile python bindings from file '$PYTHON_BINDINGS_TARGZ'"

# validate module actually can be imported
python -c 'import libxml2' || err "After installing python binding from file '$PYTHON_BINDINGS_TARGZ', python still doesn't recongize the 'libxml2' module, sorry but I don't know how to fix that"

