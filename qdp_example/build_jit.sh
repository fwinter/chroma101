#!/bin/bash

CXX=mpicxx
CC=mpicc

PACKAGE_PATH=$HOME/git/package/cuda/install



FILENAME="simple.cc"
NEWDIR="build"

# Check if the file exists in the current directory
if [ -f "./$FILENAME" ]; then
    echo "File '$FILENAME' found. Creating directory '$NEWDIR'..."
    mkdir -p "$NEWDIR"
    cd "$NEWDIR" || exit
    echo "Now inside directory: $(pwd)"
fi



cmake \
    -DQMP_DIR=${PACKAGE_PATH}/qmp/lib/cmake/QMP \
    -DQDPXX_DIR=${PACKAGE_PATH}/qdpxx/lib/cmake/QDPXX \
    -DCMAKE_CXX_COMPILER=$CXX \
    -DCMAKE_C_COMPILER=$CC \
    -DLLVM_DIR=${PACKAGE_PATH}/llvm-17/lib/cmake/llvm \
    ..
