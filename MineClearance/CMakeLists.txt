cmake_minimum_required(VERSION 3.3)
project(MineClearance)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    main.cpp MineClearance.h MineClearance.cpp)

add_executable(MineClearance ${SOURCE_FILES})