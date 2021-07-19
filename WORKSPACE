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
   requirements = "//third_party:requirements.txt",
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

###########
# Nim Lang
###########

load("//tools/build/bazel/rules_nim:deps.bzl", "nim_rules_dependencies")

nim_rules_dependencies()


register_toolchains("//tools/build/bazel/py_toolchain:py_toolchain")

###########
# Scala
###########

skylib_version = "1.0.3"
http_archive(
    name = "bazel_skylib",
    sha256 = "1c531376ac7e5a180e0237938a2536de0c54d93f5c278634818e0efc952dd56c",
    type = "tar.gz",
    url = "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/{}/bazel-skylib-{}.tar.gz".format(skylib_version, skylib_version),
)

rules_scala_version = "e7a948ad1948058a7a5ddfbd9d1629d6db839933"
http_archive(
    name = "io_bazel_rules_scala",
    sha256 = "76e1abb8a54f61ada974e6e9af689c59fd9f0518b49be6be7a631ce9fa45f236",
    strip_prefix = "rules_scala-%s" % rules_scala_version,
    type = "zip",
    url = "https://github.com/bazelbuild/rules_scala/archive/%s.zip" % rules_scala_version,
)

# Stores Scala version and other configuration
# 2.12 is a default version, other versions can be use by passing them explicitly:
# scala_config(scala_version = "2.11.12")
load("@io_bazel_rules_scala//:scala_config.bzl", "scala_config")
scala_config()

load("@io_bazel_rules_scala//scala:scala.bzl", "scala_repositories")
scala_repositories()

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")
rules_proto_dependencies()
rules_proto_toolchains()

load("@io_bazel_rules_scala//scala:toolchains.bzl", "scala_register_toolchains")
scala_register_toolchains()
