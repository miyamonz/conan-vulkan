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
        if not tools.cross_building(self.settings):
            self.run(f'.{os.sep}test_package')
