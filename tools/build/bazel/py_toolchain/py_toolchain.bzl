def _foo(repository_ctx):
    os_name = repository_ctx.os.name.lower()
    # TODO(Jonathon): This can't differentiate ARM (Mac M1) from old x86.
    # TODO(Jonathon: Support Linux.
    if os_name == "mac os x":
        url = "https://github.com/indygreg/python-build-standalone/releases/download/20210228/cpython-3.8.8-x86_64-apple-darwin-pgo+lto-20210228T1503.tar.zst"
    elif os_name == "linux":
        url = "https://github.com/indygreg/python-build-standalone/releases/download/20210228/cpython-3.8.8-x86_64-unknown-linux-gnu-pgo+lto-20210228T1503.tar.zst"
    else:
        fail("OS '{}' is not supported.".format(os_name))

    repository_ctx.download(
        url = [url],
        integrity = "",
        output = "python.tar.zst",
    )
    # TODO(Jonathon): NOT HERMETIC. Need to install 'unzstd' in rule and use it.
    unzstd_bin_path = repository_ctx.which("unzstd")
    res = repository_ctx.execute([unzstd_bin_path, "python.tar.zst"])
    if res.return_code:
        fail("error decompressiong zstd" + res.stdout + res.stderr)
    else:
        res = repository_ctx.execute(["ls"])
        print(res.stdout)
    res = repository_ctx.execute(["tar", "-xvf", "python.tar"])
    if res.return_code:
        fail("error extracting Python runtime:\n" + res.stdout + res.stderr)
    repository_ctx.delete("python.tar.zst")
    repository_ctx.delete("python.tar")

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

#    repository_ctx.template("BUILD", Label(repository_ctx.name +  "//" + ":BUILD"), {})
    repository_ctx.file("BUILD.bazel", BUILD_FILE_CONTENT)
#    native.register_toolchains("bee")
    return None


foo = repository_rule(
    implementation=_foo,
    local=True,  # TODO(Jonathon): Don't think this should be local.
    attrs={}
)
