cc_library(
    name = "base",
    srcs = [
        "cpp_standards.h"
    ],
)

cc_test(
    name = "add_binary_test",
    srcs = [
        "add_binary_test.cc",
        "add_binary.h"
    ],
    copts = ["-Iexternal/gtest/include"],
    deps = [
        "@gtest//:main",
        ":base",
    ],
)
