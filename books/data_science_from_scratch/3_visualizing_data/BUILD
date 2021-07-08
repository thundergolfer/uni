load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@pypi//:requirements.bzl", "requirement")

py_binary(
    name = "visualizing_data",
    srcs = ["visualizing_data.py"],
    deps = [
        requirement("matplotlib")
    ]
)
