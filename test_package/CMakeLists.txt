project(test_package)
cmake_minimum_required(VERSION 3.11)

find_package(Vulkan REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Vulkan::Vulkan)
