# -*- coding: utf-8 -*-
name = "libass"
version = "0.17.1"
authors = ["M83"]
description = "libass subtitle rendering library"
build_requires = [
    "freetype",
    "harfbuzz",
]

build_command = 'python {root}/rezbuild.py install'

def commands():
    env.LD_LIBRARY_PATH.prepend("{root}/lib")
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")
    env.CPATH.prepend("{root}/include")
    env.CMAKE_PREFIX_PATH.append("{root}")
