cmake_minimum_required(VERSION 3.15...3.27)

project(bloaty-wheel LANGUAGES CXX)

# 从 pyproject.toml 获取版本号
if(NOT DEFINED SKBUILD_PROJECT_VERSION)
  message(FATAL_ERROR "SKBUILD_PROJECT_VERSION is not defined")
endif()

# 提取 bloaty 版本号（去掉最后的 .0 后缀）
string(REGEX MATCH "^([0-9]+)\.([0-9]+)\.([0-9]+)" BLOATY_VERSION
             "${SKBUILD_PROJECT_VERSION}")

# 构建下载 URL - 使用官方 GitHub 发布的源码包
set(BLOATY_VERSION_TAG "v${BLOATY_VERSION}")
set(BLOATY_DOWNLOAD_URL
    "https://github.com/google/bloaty/releases/download/${BLOATY_VERSION_TAG}/bloaty-${BLOATY_VERSION}.tar.bz2")

# 如果官方发布不可用，从主分支克隆（备用方案）
set(BLOATY_GIT_URL "https://github.com/google/bloaty.git")
set(BLOATY_GIT_TAG "${BLOATY_VERSION_TAG}")

message(STATUS "Building bloaty version: ${BLOATY_VERSION}")
message(STATUS "Download URL: ${BLOATY_DOWNLOAD_URL}")

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
    # 禁用系统库，使用捆绑的依赖项确保静态链接
    -DBLOATY_PREFER_SYSTEM_CAPSTONE=NO
    -DBLOATY_PREFER_SYSTEM_PROTOBUF=NO
    -DBLOATY_PREFER_SYSTEM_RE2=NO
    -DBLOATY_PREFER_SYSTEM_ABSL=NO
    -DBLOATY_PREFER_SYSTEM_ZLIB=NO
    -DBLOATY_PREFER_SYSTEM_ZSTD=NO
    # 禁用调试功能
    -DBLOATY_ENABLE_ASAN=OFF
    -DBLOATY_ENABLE_UBSAN=OFF)

# Windows 特定配置：静态运行时
if(MSVC)
  list(APPEND BLOATY_CMAKE_ARGS
       -DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded$<$<CONFIG:Debug>:Debug>)
endif()

# 使用 ExternalProject 下载和构建 bloaty
ExternalProject_Add(
  build-bloaty
  URL ${BLOATY_DOWNLOAD_URL}
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  PREFIX ${CMAKE_BINARY_DIR}/bloaty-prefix
  BINARY_DIR ${BLOATY_BUILD_DIR}
  CMAKE_ARGS ${BLOATY_CMAKE_ARGS}
  CMAKE_GENERATOR Ninja
  BUILD_COMMAND ${CMAKE_COMMAND} --build . --config Release
  INSTALL_COMMAND ${CMAKE_COMMAND} --build . --config Release --target install
  LOG_DOWNLOAD ON
  LOG_CONFIGURE ON
  LOG_BUILD ON
  LOG_INSTALL ON)

# 如果需要初始化 git submodules（当从 git 克隆时）
ExternalProject_Add_Step(
  build-bloaty init-submodules
  COMMAND git submodule update --init --recursive || true
  WORKING_DIRECTORY <SOURCE_DIR>
  DEPENDEES download
  DEPENDERS configure
  ALWAYS FALSE
  LOG ON)

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
