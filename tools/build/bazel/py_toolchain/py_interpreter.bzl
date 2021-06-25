def _python_build_standalone_interpreter_impl(repository_ctx):
    os_name = repository_ctx.os.name.lower()
    # TODO(Jonathon): This can't differentiate ARM (Mac M1) from old x86.
    # TODO(Jonathon: Support Windows.
    if os_name == "mac os x":
        url = "https://github.com/indygreg/python-build-standalone/releases/download/20210228/cpython-3.8.8-x86_64-apple-darwin-pgo+lto-20210228T1503.tar.zst"
        integrity_shasum = "4c859311dfd677e4a67a2c590ff39040e76b97b8be43ef236e3c924bff4c67d2"
    elif os_name == "linux":
        url = "https://github.com/indygreg/python-build-standalone/releases/download/20210228/cpython-3.8.8-x86_64-unknown-linux-gnu-pgo+lto-20210228T1503.tar.zst"
        integrity_shasum = "74c9067b363758e501434a02af87047de46085148e673547214526da6e2b2155"
    else:
        fail("OS '{}' is not supported.".format(os_name))

    repository_ctx.download(
        url = [url],
        sha256 = integrity_shasum,
        output = "python.tar.zst",
    )

    # TODO(Jonathon): NOT HERMETIC. Need to install 'unzstd' in rule and use it.
    unzstd_bin_path = repository_ctx.which("unzstd")
    if unzstd_bin_path == None:
        fail("On OSX and Linux this Python toolchain requires that the zstd and unzstd exes are available on the $PATH, but it was not found.")

    if os_name == "mac os x":
        res = repository_ctx.execute([unzstd_bin_path, "python.tar.zst"])

        if res.return_code:
            fail("error decompressiong zstd" + res.stdout + res.stderr)

        res = repository_ctx.execute(["tar", "-xvf", "python.tar"])
        if res.return_code:
            fail("error extracting Python runtime:\n" + res.stdout + res.stderr)
        repository_ctx.delete("python.tar")
    elif os_name == "linux":
        # Linux's GNU tar supports zstd out-of-the-box
        res = repository_ctx.execute(["tar", "-axvf", "python.tar.zst"])
        if res.return_code:
            fail("error extracting Python runtime:\n" + res.stdout + res.stderr)
    else:
        fail("OS '{}' is not supported.".format(os_name))
    repository_ctx.delete("python.tar.zst")

    python_build_data = json.decode(repository_ctx.read("python/PYTHON.json"))

    BUILD_FILE_CONTENT = """
filegroup(
    name = "files",
    srcs = glob(["install/**"], exclude = ["**/* *"]),
    visibility = ["//visibility:public"],
)

filegroup(
    name = "interpreter",
    srcs = ["python/{interpreter_path}"],
    visibility = ["//visibility:public"],
)
""".format(interpreter_path = python_build_data["python_exe"])

    repository_ctx.file("BUILD.bazel", BUILD_FILE_CONTENT)
    return None


python_build_standalone_interpreter = repository_rule(
    implementation=_python_build_standalone_interpreter_impl,
    local=True,  # TODO(Jonathon): Don't think this should be local.
    attrs={}
)
