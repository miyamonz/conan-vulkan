# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools, RunEnvironment


class VulkanTestConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake_find_package'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if self.settings.os == 'Windows':
            self.run('.\\Release\\test_package.exe')
        else:
            self.run(f'./test_package')
