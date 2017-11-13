#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ExpatConan(ConanFile):
    """ This recipe requires conan 0.25.1 at least"""

    name = "Expat"
    version = "2.2.5"
    description = "Recipe for Expat library"
    license = "MIT/X Consortium license. Check file COPYING of the library"
    url = "https://github.com/ZaMaZaN4iK/conan-expat"
    source_url = "https://github.com/libexpat/libexpat"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = ['FindExpat.cmake']
    exports_sources = ['CMakeLists.txt']

    def source(self):
        base_url = "https://github.com/libexpat/libexpat/archive"
        zip_name = "R_2_2_5.zip"
        tools.download("%s/%s" % (base_url, zip_name), "libexpat")
        tools.unzip("libexpat")
        os.unlink("libexpat")

    def build(self):
        cmake = CMake(self, parallel=True)

        cmake.definitions['BUILD_doc'] = False
        cmake.definitions['BUILD_examples'] = False
        cmake.definitions['BUILD_tests'] = False
        cmake.definitions['BUILD_tools'] = False
        cmake.definitions['CMAKE_DEBUG_POSTFIX'] = 'd'
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        cmake.definitions['BUILD_shared'] = self.options.shared

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindExpat.cmake", ".", ".")

    def package_info(self):
        self.cpp_info.libs = ["expatd" if self.settings.build_type == "Debug" else "expat"]
        if not self.options.shared:
            self.cpp_info.defines = ["XML_STATIC"]

    def configure(self):
        del self.settings.compiler.libcxx
