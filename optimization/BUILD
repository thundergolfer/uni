load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

py_library(
    name = "gradient_descent",
    srcs = ["gradient_descent.py"],
    deps = [],  # standalone pure-python library
    srcs_version = "PY3",
)

py_test(
    name = "gradient_descent_test",
    srcs = ["gradient_descent_test.py"],
    deps = [":gradient_descent"],
)