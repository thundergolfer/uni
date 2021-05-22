java_binary(
    name = "Main",
    srcs = glob(["*.java"]),
    deps = [
        "@maven//:io_rsocket_rsocket_core",
        "@maven//:io_rsocket_rsocket_transport_netty",
        "@maven//:org_slf4j_slf4j_api",
        "@maven//:org_slf4j_slf4j_simple",
        "@maven//:io_projectreactor_reactor_core",
        "@maven//:io_netty_netty_buffer",
    ],
    visibility = ["//performance/jvm:__subpackages__"],
)
