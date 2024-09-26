#!/bin/bash
set -xe

VERSION="3.13.5"

rm -rf /tmp/embree.tar.gz
rm -rf ~/embree

wget -nv https://github.com/RenderKit/embree/releases/download/v${VERSION}/embree-${VERSION}.x86_64.linux.tar.gz -O /tmp/embree.tar.gz
cd /tmp
tar -zxvf embree.tar.gz
rm -f embree.tar.gz

mv embree-${VERSION}.x86_64.linux ~/embree


