#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ExpatConan(ConanFile):
    name = "expat"
    version = "2.2.5"
    description = "Fast XML parser in C"
    url = "https://github.com/bincrafters/conan-expat"
    license = "https://github.com/libexpat/libexpat/blob/master/expat/COPYING"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = ['FindExpat.cmake', 'LICENSE']
    exports_sources = ['CMakeLists.txt']

    def source(self):
        base_url = "https://github.com/libexpat/libexpat/archive"
        zip_name = "R_%s.zip" % self.version.replace(".", "_") 
        tools.get("%s/%s" % (base_url, zip_name))

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
