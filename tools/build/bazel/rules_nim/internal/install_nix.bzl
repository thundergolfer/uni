OSX_OS_NAME = "mac os x"
LINUX_OS_NAME = "linux"
NIM_VERSION = "1.4.8"

def _install_nix_impl(repository_ctx):
    os_name = repository_ctx.os.name.lower()
    install_root = "nim-{version}".format(version = NIM_VERSION)

    if os_name == OSX_OS_NAME:
        url = "TODO"
        integrity_shasum = "TODO"
    elif os_name == LINUX_OS_NAME:
        url = "https://nim-lang.org/download/nim-{version}-linux_x64.tar.xz".format(version = NIM_VERSION)
        integrity_shasum = "c066c251db1b852afef8fd65830788be593dbffd178080de14bf5c512905424d"
        repository_ctx.download_and_extract(
            url = url,
            sha256 = integrity_shasum,
            stripPrefix = install_root,
            output = "",
        )
    else:
        fail("OS '{}' is not supported.".format(os_name))


    build_file_content = """
filegroup(
    name = "exe",
    srcs = ["bin/nim"],
    visibility = ["//visibility:public"],
)
"""

    repository_ctx.file("BUILD.bazel", build_file_content)
    return None


install_nim = repository_rule(
    implementation = _install_nix_impl,
    attrs = {},
)