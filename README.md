[![DOI](https://zenodo.org/badge/194721283.svg)](https://zenodo.org/badge/latestdoi/194721283)
[![Build Status](https://app.travis-ci.com/sampotter/python-embree.svg?branch=master)](https://app.travis-ci.com/sampotter/python-embree)

# python-embree #

This library is a thin wrapper around Embree 3.

As much as possible, it tries to emulate the C API usage. The main
point of this is to avoid creating a new API which would obfuscate the
usage of the C API. Ideally, it should be easy to read the Embree
documentation or examples, and translate things straightforwardly to
equivalent Python code.

A secondary goal is to provide easy interoperability with numpy.

**NOTE**: *very little of the library is wrapped so far, but this
library is being developed in a way that should make it as easy as
possible to wrap more functionality as necessary. If you find that a
function that you'd like to use isn't wrapped, please create an issue
or feel free to wrap it on your own and submit a pull request.*

## Installation

### Windows

1. Clone the repositry to your local windows machine. `git clone`

2. pip install on your local machine. (Requires Cython and `CL` command of Visual studio installed.)

```
cd python-embree
pip install .
```

The binary package of embree 3.13.5 will be downloaded into your working directory `.\embree3`.
Then a wheel package with 'embree_y/embree.cp312-win_amd64.pyd', 'embree_y/embree3.dll', 'embree_y/tbb12.dll'
is generated under `dist` directory and installed.

Alternatively, you can build a wheel package with
`python -m build --wheel`
after you pip install `build` to your python (or python venv).

### Linux

1. Clone the repositry to your local windows machine. `git clone`

2.
2. pip install on your local machine.

```
cd python-embree
pip install .
```

The binary package of embree 3.13.5 will be downloaded into your working directory `.\embree3`.
Then a wheel package with 'embree_y/embree.cpython-312-x86_64-linux-gnu.so', 'embree_y/libembree3.so.3', and 'embree_y/libtbb.so.12' is generated.
Note that linker option "-Wl,-rpath,$ORIGIN" is given in `setup.py`. You don't need to set LD_LIBRARY_PATH to `libembree3.so` and `libtbb.so.12`

## Tips and tricks

### Retain and release

The underlying Embree library uses reference counting to properly
clean up resources used by the different types it provides
(`RTCDevice`, `RTCScene`, etc.). This means that each type exposes a
pair of "retain" and "release" functions: e.g., `rtcRetainDevice`, and
`rtcReleaseDevice`. How to use these correctly is spelled out in the
[Embree API docs](https://www.embree.org/api.html) and the [many
Embree tutorials](https://www.embree.org/tutorials.html). Please
consult these when using
[python-embree](https://github.com/sampotter/python-embree). The
classes providing a lightweight object-oriented wrapper around
Embree's types *do not call any retain or release functions behind the
scenes: this is the user's responsibility*.

### Parallelism

Using
[multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
for concurrency in Python requires objects that are put into queues to
be serialized using
[pickle](https://docs.python.org/3/library/pickle.html). Unfortunately,
it is not currently possible to serialize the Embree data structures
(see the Embree repository's issues
[#137](https://github.com/embree/embree/issues/137) and
[#238](https://github.com/embree/embree/issues/238)), and there do not
appear to be plans to support this feature. The rationale for not
supporting this feature is that building the Embree BVH from scratch
is usually faster than reading the equivalent amount of data from
disk.

This means that you will not be able to use any of the extensions
classes exported by
[embree.pyx](https://github.com/sampotter/python-embree/blob/master/embree.pyx)
(such as `embree.Device`, `embree.Scene`, etc.) with multiprocessing
*directly*. To get around this problem, a simple fix is to wrap a bit
of Embree functionality in a Python class with its own `__reduce__`
method. For an example, see the implementation of `TrimeshShapeModel`
[here](https://github.com/sampotter/python-flux/blob/master/flux/shape.py).
