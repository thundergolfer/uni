workspace(name = "uni")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

#############################
# Python
#############################

load("//tools/build/bazel/py_toolchain:py_interpreter.bzl", "python_build_standalone_interpreter")

python_build_standalone_interpreter(
    name = "python_interpreter",
)

rules_python_version = "0.3.0"

http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/{version}/rules_python-{version}.tar.gz".format(version = rules_python_version),
    sha256 = "934c9ceb552e84577b0faf1e5a2f0450314985b4d8712b2b70717dc679fdc01b",
)

load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
   name = "pypi",
   requirements = "//:requirements.txt",
   python_interpreter_target = "@python_interpreter//:python/install/bin/python3.8"
)

#############################
# MyPy
#############################

mypy_integration_version = "0.2.0"

http_archive(
    name = "mypy_integration",
    sha256 = "621df076709dc72809add1f5fe187b213fee5f9b92e39eb33851ab13487bd67d",
    strip_prefix = "bazel-mypy-integration-{version}".format(version = mypy_integration_version),
    urls = [
        "https://github.com/thundergolfer/bazel-mypy-integration/archive/refs/tags/{version}.tar.gz".format(version = mypy_integration_version),
    ],
)

load(
    "@mypy_integration//repositories:repositories.bzl",
    mypy_integration_repositories = "repositories",
)
mypy_integration_repositories()

load("@mypy_integration//:config.bzl", "mypy_configuration")
mypy_configuration("//tools/build/typing:mypy.ini")

load("@mypy_integration//repositories:deps.bzl", mypy_integration_deps = "deps")

mypy_integration_deps(
    "//tools/build/typing:mypy_version.txt",
    python_interpreter_target = "@python_interpreter//:python/install/bin/python3.8"
)

##########
# C++
##########

http_archive(
    name = "googletest",
    build_file = "@//third_party:BUILD.googletest",
    sha256 = "9dc9157a9a1551ec7a7e43daea9a694a0bb5fb8bec81235d8a1e6ef64c716dcb",
    urls = ["https://github.com/google/googletest/archive/release-1.10.0.tar.gz"],
    strip_prefix = "googletest-release-1.10.0",
)

##########
# JVM
##########

RULES_JVM_EXTERNAL_TAG = "4.0"
RULES_JVM_EXTERNAL_SHA = "31701ad93dbfe544d597dbe62c9a1fdd76d81d8a9150c2bf1ecf928ecdf97169"

http_archive(
    name = "rules_jvm_external",
    strip_prefix = "rules_jvm_external-%s" % RULES_JVM_EXTERNAL_TAG,
    sha256 = RULES_JVM_EXTERNAL_SHA,
    url = "https://github.com/bazelbuild/rules_jvm_external/archive/%s.zip" % RULES_JVM_EXTERNAL_TAG,
)

load("@rules_jvm_external//:defs.bzl", "maven_install")

maven_install(
    artifacts = [
        "junit:junit:4.12",
        "io.projectreactor:reactor-core:3.4.6",
        "io.rsocket:rsocket-core:1.0.2",
        "io.rsocket:rsocket-transport-netty:1.0.2",
        "org.openjdk.jmh:jmh-core:1.31",
        "org.openjdk.jmh:jmh-generator-annprocess:1.31",
        "org.slf4j:slf4j-simple:1.7.30",
        "org.slf4j:slf4j-api:1.7.30",
        "io.netty:netty-buffer:4.1.51.Final",
    ],
    repositories = [
        # Private repositories are supported through HTTP Basic auth
        "http://username:password@localhost:8081/artifactory/my-repository",
        "https://maven.google.com",
        "https://repo1.maven.org/maven2",
    ],
)



register_toolchains("//tools/build/bazel/py_toolchain:py_toolchain")
