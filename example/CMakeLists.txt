cmake_minimum_required(VERSION 2.8)

project(pyBuildInfoExample)

set(BI_HEADER "${CMAKE_CACHEFILE_DIR}/includeBuildInfo/")

make_directory("${BI_HEADER}")
include_directories("${BI_HEADER}")

add_executable(buildInfoExample main.cpp)

set(BI_INP "{\\\"build_toolchain\\\": \\\"${CMAKE_CXX_COMPILER_ID}\\\", \\\"build_toolchain_version\\\": \\\"${CMAKE_CXX_COMPILER_VERSION}\\\", \\\"build_target_machine\\\": \\\"${CMAKE_SYSTEM_PROCESSOR}\\\", \\\"build_target_system\\\": \\\"${CMAKE_SYSTEM_NAME}\\\"}")

set(BI_PY "exec('import sys\\nsys.path.append(\\'${CMAKE_SOURCE_DIR}/../\\')\\nimport pybuildinfo.run\\npybuildinfo.run.run()')")

set(BI_SCM "${CMAKE_SOURCE_DIR}/../")

add_custom_command(
	TARGET buildInfoExample
	PRE_BUILD
	COMMAND python -c \"${BI_PY}\" --out \"${BI_HEADER}/buildinfoexample.hpp\" --dir \"${BI_SCM}\" --in \"${BI_INP}\"
)
