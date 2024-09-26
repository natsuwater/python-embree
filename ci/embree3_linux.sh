#!/bin/bash

build="./build"
if [ -d "$build" ]; 
    then rm -rf "$build"
fi

dist="./dist"
if [ -d "$dist" ]; then
    rm -rf "$dist"
fi

embree3="./embree3"
if [ ! -d "$embree3" ]; then
    curl -L -o embree3.tar.gz https://github.com/RenderKit/embree/releases/ download/v3.13.5/embree-3.13.5.x86_64.linux.tar.gz
    tar xzvf embree3.tar.gz
    mv embree-3.13.5.x86_64.linux / embree3
    rm embree3.tar.gz
fi

