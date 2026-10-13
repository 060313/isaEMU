cmake_minimum_required(VERSION 3.16)
project(isa_sim LANGUAGES CXX)

# 构建约束（SAD 5.1.4）：C++17；内核层零第三方链接
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()

# ---------------------------------------------------------------- 内核库（零第三方）
# SS-1 模拟执行内核 + SS-2 ISA 抽象 + SS-3 比对
# 这一层不链接任何第三方库，是「零第三方链接」硬规则的载体。
file(GLOB_RECURSE KERNEL_SRC CONFIGURE_DEPENDS
  "${CMAKE_CURRENT_SOURCE_DIR}/src/core/*.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/isa/*.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/compare/*.cpp")

add_library(isa_kernel STATIC ${KERNEL_SRC})
target_include_directories(isa_kernel PUBLIC
  "${CMAKE_CURRENT_SOURCE_DIR}/include"
  "${CMAKE_CURRENT_SOURCE_DIR}/src")

# ---------------------------------------------------------------- 服务库
# SS-4 适配 + SS-5 领域服务 + SS-6 集成 API + SS-8 基础服务
# 设计预留：序列化约定使用 nlohmann/json（6.5.2 约定③），骨架阶段以 std::string 承载
# JSON 文本以保持零依赖；接入第三方时在此处 find_package / FetchContent。
file(GLOB_RECURSE SERVER_SRC CONFIGURE_DEPENDS
  "${CMAKE_CURRENT_SOURCE_DIR}/src/adapt/*.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/domain/*.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/api/*.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/base/*.cpp")

add_library(isa_server STATIC ${SERVER_SRC})
target_link_libraries(isa_server PUBLIC isa_kernel)

# ---------------------------------------------------------------- 可执行
add_executable(isa_sim "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp")
target_link_libraries(isa_sim PRIVATE isa_server)

if(WIN32)
  set_target_properties(isa_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
endif()

# ---------------------------------------------------------------- 冒烟测试
enable_testing()
add_executable(isa_smoke "${CMAKE_CURRENT_SOURCE_DIR}/tests/smoke_test.cpp")
target_link_libraries(isa_smoke PRIVATE isa_server)
add_test(NAME smoke COMMAND isa_smoke)
