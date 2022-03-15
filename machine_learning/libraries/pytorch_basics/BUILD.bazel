load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@pypi//:requirements.bzl", "requirement")

py_binary(
    name = "fashion_mnist",
    srcs = ["fashion_mnist.py"],
    deps = [
        requirement("torch"),
        requirement("torchvision"),
    ],
)
