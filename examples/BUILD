load("@technical_documentation_system//:technical_documents.bzl", "technical_documents", "technical_documentation_website")

technical_documents(
    name = "docs",
    inputs = ["hello_world.md"],
    references = [
        "//demo_code:hello_world",
    ]
)

technical_documentation_website(
    name = "website",
    srcs = {},
)
