java_binary(
    name = "server",
    srcs = [
        "MarkdownRenderer.java",
        "Server.java",
        "BaseHandler.java",
    ],
    deps = [
        "@bazel_tools//tools/java/runfiles",
        "//tools/build/docs/technical-documentation-system/vendor/github.com/atlassian/commonmark-java/commonmark",
    ],
    main_class = "server.Server",
    visibility = [
        "//visibility:public",
    ],
    data = glob(["static/*.md", "static/*.html"]),
)
