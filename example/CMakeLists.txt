cmake_minimum_required(VERSION 3.2)

find_package(PythonInterp 3.2 REQUIRED)

project(pyBuildInfoExample)

set(BI_ROOT "${CMAKE_SOURCE_DIR}/../")
set(BI_HEADER "${CMAKE_BINARY_DIR}/includeBuildInfo/")
get_filename_component(BI_HEADER ${BI_HEADER} REALPATH)
set(BI_HEADER_FULL "${BI_HEADER}/pybuildinfoexample.hpp")

make_directory("${BI_HEADER}")
include_directories("${BI_HEADER}")

set(BI_DICT "{\\\"build_toolchain\\\":\\\"${CMAKE_CXX_COMPILER_ID}\\\",\\\"build_toolchain_version\\\":\\\"${CMAKE_CXX_COMPILER_VERSION}\\\",\\\"build_target_machine\\\":\\\"${CMAKE_SYSTEM_PROCESSOR}\\\",\\\"build_target_system\\\":\\\"${CMAKE_SYSTEM_NAME}\\\"}")

add_custom_target(
	preBuildInfoExample
    COMMAND ${CMAKE_COMMAND} -E env PYTHONPATH=\"${BI_ROOT}\"
   ${PYTHON_EXECUTABLE} -m pybuildinfo.cmd -o \"${BI_HEADER_FULL}\" -vcs \"${BI_ROOT}\" -dict \"${BI_DICT}\"
)

add_executable(buildInfoExample main.cpp)
add_dependencies(buildInfoExample preBuildInfoExample)
set_property(TARGET buildInfoExample PROPERTY CXX_STANDARD 11)
if(CMAKE_COMPILER_IS_GNUCXX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
endif(CMAKE_COMPILER_IS_GNUCXX)
add_custom_target(buildInfoExample_RUN
  COMMAND buildInfoExample
  DEPENDS buildInfoExample
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
