import os
import shutil
import subprocess

from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import find_packages, setup
from setuptools.extension import Extension

extension_param = dict()
extension_param.update(
    name="embreepy.embree",
    sources=["./src/embreepy/embree.pyx"],
    libraries=["embree3"],
    include_dirs=["./embree3/include"],
    library_dirs=["./embree3/lib"],
    language="c++",
)

if os.name == "posix":
    extension_param.update(extra_link_args=["-WL,-rpath,$ORIGIN"])

extensions = [Extension(**extension_param)]


class CustomBuildExt(build_ext):
    def run(self):
        if os.name == "nt":
            subprocess.run([r".\ci\embree3_windows.bat"], check=True)
            build_ext.run(self)
            # DLLファイルをコピーして、whl を介してインストールフォルダに導入する。
            for dll in ["./embree3/bin/embree3.dll", "./embree3/bin/tbb12.dll"]:
                shutil.copy(dll, os.path.join(self.build_lib, "embreepy"))
        elif os.name == "posix":
            subprocess.run(["./ci/embree3_linux.sh"], check=True)
            build_ext.run(self)
            for lib in ["./embree3/lib/libembree3.so.3", "./embree3/lib/libtbb.so.12"]:
                shutil.copy2(
                    lib, os.path.join(self.build_lib, "embreepy"), follow_symlinks=True
                )


setup(
    name="embreepy",
    ext_modules=cythonize(extensions),
    cmdclass={"build_ext": CustomBuildExt},
    package_data={"embreepy": ["*.pyd", "*.dll", "libs"]},
    package_dir={"": "src"},
    packages=find_packages(),
    zip_safe=False,
)
