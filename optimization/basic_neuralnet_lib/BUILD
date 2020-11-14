load("@mypy_integration//:mypy.bzl", "mypy_test")
load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

py_library(
    name = "basic_neuralnet_lib",
    srcs = glob(["*.py"],  exclude=["demo.py"]),
    deps = [
        requirement("numpy"),
    ],
    srcs_version = "PY3",
)

py_binary(
    name = "demo",
    srcs = ["demo.py"],
    deps = [
        ":basic_neuralnet_lib",
    ],
)

# A Bazel test target that will run MyPy checking over the library's code.
mypy_test(
    name = "mypy_test",
    deps = [
        ":basic_neuralnet_lib",
    ],
)
