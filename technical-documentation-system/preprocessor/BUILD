java_binary(
    name = "preprocessor",
    srcs = [
        "Preprocessor.java",
        "ReferenceProcessingException.java",
    ],
    deps = [],
    main_class = "preprocessor.Preprocessor",
    visibility = [
        "//visibility:public",
    ]
)

java_test(
    name = "TestPreprocessor",
    srcs = ["TestPreprocessor.java"],
    test_class = "preprocessor.TestPreprocessor",
    deps = [
        ":preprocessor",
        "//third_party:junit4",
    ],
)
