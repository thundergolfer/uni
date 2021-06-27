OSX_OS_NAME = "mac os x"
LINUX_OS_NAME = "linux"
NIM_VERSION = "1.4.8"

def _install_nix_impl(repository_ctx):
    os_name = repository_ctx.os.name.lower()
    install_root = "nim-{version}".format(version = NIM_VERSION)

    if os_name == OSX_OS_NAME:
        # There's no pre-built binary for Mac OS so we'll need to compile from the source distribution.
        # This is NOT hermetic as it relies on a C compiler (clang) but it's not worse than the status-quo
        # situation in these rules which was looking for a 'nim' binary on the $PATH.
        source_dist_url = "https://nim-lang.org/download/nim-1.4.8.tar.xz"
        sha256_integrity_shasum = "b798c577411d7d95b8631261dbb3676e9d1afd9e36740d044966a0555b41441a"
        repository_ctx.download_and_extract(
            url = source_dist_url,
            sha256 = sha256_integrity_shasum,
            stripPrefix = install_root,
            output = "",
        )
        repository_ctx.report_progress("Compiling Nim from source. Not hermetic because it will use system's C compiler.")
        # To compile from source the https://nim-lang.org/install_unix.html page instructs that we run the following commands:
        #
        # sh build.sh
        # bin/nim c koch
        # ./koch boot -d:release
        # ./koch tools
        #
        res = repository_ctx.execute(
            ["sh", "build.sh"],
            timeout = 600,
            environment = {},
            quiet = True,
            working_directory = ""
        )
        if res.return_code:
            fail("Error running Nim 'build.sh' build script." + res.stdout + res.stderr)

        res = repository_ctx.execute(
            ["bin/nim", "c", "koch"],
            timeout = 600,
            environment = {},
            quiet = True,
            working_directory = "",
        )
        if res.return_code:
            fail("Error building Nim's 'koch' program." + res.stdout + res.stderr)

        res = repository_ctx.execute(
            ["./koch", "boot", "-d:release"],
            timeout = 600,
            environment = {},
            quiet = True,
            working_directory = "",
        )
        if res.return_code:
            fail("Error running Nim's './koch boot' program." + res.stdout + res.stderr)

        res = repository_ctx.execute(
            ["./koch", "tools"],
            timeout = 600,
            environment = {},
            quiet = True,
            working_directory = "",
        )
        if res.return_code:
            fail("Error running Nim's './koch tools' program." + res.stdout + res.stderr)

    elif os_name == LINUX_OS_NAME:
        url = "https://nim-lang.org/download/nim-{version}-linux_x64.tar.xz".format(version = NIM_VERSION)
        sha256_integrity_shasum = "c066c251db1b852afef8fd65830788be593dbffd178080de14bf5c512905424d"
        repository_ctx.download_and_extract(
            url = url,
            sha256 = sha256_integrity_shasum,
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
