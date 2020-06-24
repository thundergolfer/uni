java_binary(
    name = "server",
    srcs = [
        "Server.java",
        "StaticFileHandler.java",
    ],
    deps = ["@bazel_tools//tools/java/runfiles"],
    main_class = "server.Server",
    visibility = [
        "//visibility:public",
    ],
    data = glob(["static/*.md", "static/*.html"]),
)
