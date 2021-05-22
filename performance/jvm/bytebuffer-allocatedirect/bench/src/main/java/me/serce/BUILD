load("@rules_java//java:defs.bzl", "java_library", "java_binary")
load("//tools/build/bazel/rules_jmh:defs.bzl", "java_jmh_benchmarks")

package(default_visibility = ["//performance/jvm:__subpackages__"])

java_jmh_benchmarks(
    name = "benchmarks",
    srcs = glob(["*.java"]),
)
