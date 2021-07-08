load("@rules_python//python/pip_install:requirements.bzl", "compile_pip_requirements")

package(default_visibility = ["//visibility:public"])

# Update dependencies with:
# bazel run //third_party:requirements.update
compile_pip_requirements(
    name = "requirements",
    extra_args = [
        "--allow-unsafe",
    ],
)

# Vendored third-party dependencies are used to simplify project's WORKSPACE and
# make it easier to avoid burdening users's WORKSPACEs with this project's dependencies.
#
# This project shouldn't need too many dependencies at all.

java_import(
    name = "junit4",
    jars = [
        "hamcrest/hamcrest-core-1.3.jar",
        "junit/junit-4.13.jar",
    ],
)
