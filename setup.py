import os
import shutil
import subprocess

from setuptools import find_packages, setup
from setuptools.extension import Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext


extension_param = dict()
extension_param.update(
    name="embree.embree",
    sources=["./src/embree/embree.pyx"],
    libraries=["embree3"],
    include_dirs=["./embree3/include"],
    library_dirs=["./embree3/lib"],
    language="c++",
)

if os.name == "posix":
    extension_param.update(extra_link_args=["-Wl,-rpath,$ORIGIN"])

extensions = [Extension(**extension_param)]


class CustomBuildExt(build_ext):
    def run(self):
        if os.name == "nt":
            subprocess.run([r".\ci\embree3_windows.bat"], check=True)
            build_ext.run(self)
            # copy DLLs into build_lib, those files goes into wheel packge
            for dll in ["./embree3/bin/embree3.dll", "./embree3/bin/tbb12.dll"]:
                shutil.copy(dll, os.path.join(self.build_lib, "embree"))
        elif os.name == "posix":
            subprocess.run(["./ci/embree3_linux.sh"], check=True)
            build_ext.run(self)
            for lib in ["./embree3/lib/libembree3.so.3", "./embree3/lib/libtbb.so.12"]:
                shutil.copy2(
                    lib, os.path.join(self.build_lib, "embree"), follow_symlinks=True
                )

setup(
    name="embree",
    ext_modules=cythonize(extensions),
    cmdclass={"build_ext": CustomBuildExt},
    package_data={"embree": ["*.pyd", "*.dll", "libs"]},
    package_dir={"": "src"},
    packages=find_packages(),
    zip_safe=False,
)
