cmake_minimum_required(VERSION 3.15...3.27)

project(bloaty-wheel LANGUAGES CXX)

# 从 pyproject.toml 获取版本号
if(NOT DEFINED SKBUILD_PROJECT_VERSION)
  message(FATAL_ERROR "SKBUILD_PROJECT_VERSION is not defined")
endif()

# 提取 bloaty 版本号（用于显示）
string(REGEX MATCH "^([0-9]+)\.([0-9]+)" BLOATY_VERSION
             "${SKBUILD_PROJECT_VERSION}")

# 使用 Git 克隆 bloaty 仓库（固定到已验证的主分支提交）
# v1.1 标签的依赖项太老，与新版 CMake 不兼容
set(BLOATY_GIT_URL "https://github.com/google/bloaty.git")
set(BLOATY_GIT_TAG "4a601b636e2347322d0371c8bf8ca5eaeaca4bac")

message(STATUS "Building bloaty from commit ${BLOATY_GIT_TAG}")
message(STATUS "Git repository: ${BLOATY_GIT_URL}")

option(BLOATY_WHEEL_PREFER_SYSTEM_DEPS
       "Prefer system bloaty dependencies instead of bundled dependencies" OFF)

if(DEFINED ENV{BLOATY_WHEEL_PREFER_SYSTEM_DEPS})
  set(BLOATY_WHEEL_PREFER_SYSTEM_DEPS "$ENV{BLOATY_WHEEL_PREFER_SYSTEM_DEPS}"
      CACHE BOOL "Prefer system bloaty dependencies instead of bundled dependencies"
      FORCE)
endif()

if(BLOATY_WHEEL_PREFER_SYSTEM_DEPS)
  set(BLOATY_PREFER_SYSTEM_DEPS YES)
else()
  set(BLOATY_PREFER_SYSTEM_DEPS NO)
endif()

# 设置构建目录
set(BLOATY_BUILD_DIR "${CMAKE_BINARY_DIR}/bloaty-build")
set(BLOATY_INSTALL_DIR "${CMAKE_BINARY_DIR}/bloaty-install")

# 检测平台
if(WIN32)
  set(BLOATY_EXECUTABLE "${BLOATY_INSTALL_DIR}/bin/bloaty.exe")
else()
  set(BLOATY_EXECUTABLE "${BLOATY_INSTALL_DIR}/bin/bloaty")
endif()

include(ExternalProject)

# 配置 bloaty 编译选项
set(BLOATY_CMAKE_ARGS
    -DCMAKE_BUILD_TYPE=Release
    -DCMAKE_INSTALL_PREFIX=${BLOATY_INSTALL_DIR}
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON
    # 允许旧版 CMake 项目构建（capstone 子模块需要）
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5
    -DBUILD_TESTING=OFF
    # 默认禁用系统库，使用捆绑的依赖项确保静态链接。
    # CI 可通过 BLOATY_WHEEL_PREFER_SYSTEM_DEPS=ON 使用系统库来规避平台
    # runner 上的第三方源码编译问题。
    -DBLOATY_PREFER_SYSTEM_CAPSTONE=NO
    -DBLOATY_PREFER_SYSTEM_PROTOBUF=${BLOATY_PREFER_SYSTEM_DEPS}
    -DBLOATY_PREFER_SYSTEM_RE2=${BLOATY_PREFER_SYSTEM_DEPS}
    -DBLOATY_PREFER_SYSTEM_ABSL=NO
    -DBLOATY_PREFER_SYSTEM_ZLIB=${BLOATY_PREFER_SYSTEM_DEPS}
    -DBLOATY_PREFER_SYSTEM_ZSTD=${BLOATY_PREFER_SYSTEM_DEPS}
    # 禁用调试功能
    -DBLOATY_ENABLE_ASAN=OFF
    -DBLOATY_ENABLE_UBSAN=OFF)

# Windows 特定配置：静态运行时
if(MSVC)
  list(APPEND BLOATY_CMAKE_ARGS
       -DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded$<$<CONFIG:Debug>:Debug>)
endif()

if(APPLE)
  foreach(_bloaty_osx_var CMAKE_OSX_ARCHITECTURES CMAKE_OSX_DEPLOYMENT_TARGET
                          CMAKE_OSX_SYSROOT)
    if(DEFINED ${_bloaty_osx_var} AND NOT "${${_bloaty_osx_var}}" STREQUAL "")
      list(APPEND BLOATY_CMAKE_ARGS
           -D${_bloaty_osx_var}=${${_bloaty_osx_var}})
    endif()
  endforeach()
endif()

# 使用 ExternalProject 从 Git 克隆和构建 bloaty
ExternalProject_Add(
  build-bloaty
  GIT_REPOSITORY ${BLOATY_GIT_URL}
  GIT_TAG ${BLOATY_GIT_TAG}
  GIT_SUBMODULES ""
  GIT_SUBMODULES_RECURSE OFF
  GIT_SHALLOW OFF
  PREFIX ${CMAKE_BINARY_DIR}/bloaty-prefix
  BINARY_DIR ${BLOATY_BUILD_DIR}
  CMAKE_ARGS ${BLOATY_CMAKE_ARGS}
  CMAKE_GENERATOR Ninja
  BUILD_COMMAND ${CMAKE_COMMAND} --build . --config Release
  INSTALL_COMMAND ${CMAKE_COMMAND} --build . --config Release --target install
  LOG_DOWNLOAD OFF
  LOG_UPDATE OFF
  LOG_CONFIGURE OFF
  LOG_BUILD OFF
  LOG_INSTALL OFF)

# 减小二进制体积
find_program(STRIP_EXECUTABLE strip)
if(STRIP_EXECUTABLE AND NOT WIN32)
  add_custom_target(
    strip-bloaty ALL
    COMMAND ${STRIP_EXECUTABLE} ${BLOATY_EXECUTABLE}
    DEPENDS build-bloaty
    COMMENT "Stripping bloaty executable to reduce size")
endif()

# 安装到 Python 包目录
install(
  PROGRAMS ${BLOATY_EXECUTABLE}
  DESTINATION bloaty/data/bin
  PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE
              WORLD_READ WORLD_EXECUTE)
