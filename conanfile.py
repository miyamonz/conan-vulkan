# -*- coding: utf-8 -*-

import os

from conans import ConanFile, tools
from conans.errors import ConanException


class VulkanConan(ConanFile):
    name = 'Vulkan'
    version = '1.1.92.1'
    description = 'The LunarG Vulkan SDK provides the development and runtime components required to build, run, and debug Vulkan applications.'
    url = 'https://github.com/birsoyo/conan-vulkan'
    homepage = 'https://vulkan.lunarg.com/sdk/home'
    author = 'Orhun Birsoy <orhunbirsoy@gmail.com>'

    license = 'Various'

    # Packages the license for the conanfile.py
    exports = ['LICENSE.md']

    settings = 'os', 'arch'

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = 'source_subfolder'
    build_subfolder = 'build_subfolder'

    def source(self):
        prefix_url = f'https://sdk.lunarg.com/sdk/download/{self.version}'
        win_url = f'{prefix_url}/windows/VulkanSDK-{self.version}-Installer.exe'
        mac_url = f'{prefix_url}/mac/vulkansdk-macos-{self.version}.tar.gz'
        lin_url = f'{prefix_url}/linux/vulkansdk-linux-x86_64-{self.version}.tar.gz'

        if self.settings.os == 'Windows':
            tools.download(win_url, 'vulkan-installer.exe')
            self.run('vulkan-installer.exe /S')
        else:
            if self.settings.os == 'Linux':
                url = lin_url
            elif self.settings.os == 'Macos':
                url = mac_url
            else:
                raise ConanException(f"Unsupported platform: {self.settings.os}")
            tools.get(url, keep_permissions=True)

            # https://vulkan.lunarg.com/issue/view/5bfee3d366315165b412a8ee
            # libshaderc_shared.1.dylib missed on 1.1.92.1
            if self.settings.os == 'Macos':
                libshaderc_url = "https://vulkan.lunarg.com/issue/file/5bfee3d366315165b412a8ee/upload/1543446619_libshaderc_shared.1.dylib"
                dst_folder = f'vulkansdk-macos-{self.version}/macOS/lib/'
                tools.download(libshaderc_url, dst_folder + "libshaderc_shared.1.dylib")

    def package(self):
        self.copy(pattern='LICENSE', dst='licenses', src=self.source_subfolder)

        if self.settings.os == 'Windows':
            location = f'C:\\VulkanSDK\\{self.version}'
            inc_folder = os.path.join(location, 'Include')
            if self.settings.arch == 'x86':
                lib_folder = os.path.join(location, 'Lib32')
                bin_folder = os.path.join(location, 'Bin32')
            elif self.settings.arch == 'x86_64':
                lib_folder = os.path.join(location, 'Lib')
                bin_folder = os.path.join(location, 'Bin')
            else:
                raise ConanException(f'Unsupported architecture: {self.settings.arch}')
        elif self.settings.os == 'Macos':
            inc_folder = f'vulkansdk-macos-{self.version}/macOS/include'
            lib_folder = f'vulkansdk-macos-{self.version}/macOS/lib'
            bin_folder = f'vulkansdk-macos-{self.version}/macOS/bin'
            self.copy("*", dst='sdk', src=f'vulkansdk-macos-{self.version}');
        elif self.settings.os == 'Linux':
            inc_folder = f'{self.version}/x86_64/include'
            lib_folder = f'{self.version}/x86_64/lib'
            bin_folder = f'{self.version}/x86_64/bin'
        else:
            raise ConanException(f"Unsupported platform: {self.settings.os}")

        self.copy(pattern='*', dst='include', src=inc_folder)
        self.copy(pattern='*', dst='lib', src=lib_folder)
        self.copy(pattern='*', dst='bin', src=bin_folder)

    def package_info(self):
        if self.settings.os == 'Windows':
            self.cpp_info.libs = ['vulkan-1']
        else:
            self.cpp_info.libs = ['vulkan']
