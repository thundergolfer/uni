load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("//tools/build/bazel/rules_nim/internal:install_nix.bzl", "install_nim")

def nim_rules_dependencies():
    """Declares external repositories that rules_nim depends on. This
    function should be loaded and called from WORKSPACE files."""

    # bazel_skylib is a set of libraries that are useful for writing
    # Bazel rules. We use it to handle quoting arguments in shell commands.
    _maybe(
        git_repository,
        name = "bazel_skylib",
        remote = "https://github.com/bazelbuild/bazel-skylib",
        commit = "3fea8cb680f4a53a129f7ebace1a5a4d1e035914",
    )

    install_nim(
        name = "nim_prebuilt"
    )

def _maybe(rule, name, **kwargs):
    """Declares an external repository if it hasn't been declared already."""
    if name not in native.existing_rules():
        rule(name = name, **kwargs)