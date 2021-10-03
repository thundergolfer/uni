load("@rules_java//java:defs.bzl", "java_test")
load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

py_test(
    name = "binary_search_test",
    srcs = ["binary_search.py"],
    main = "binary_search.py",
)

java_test(
    name = "BinarySearch",
    srcs = ["BinarySearch.java"],
    test_class = "algorithms.named.BinarySearch",
    deps = [
        "//third_party:junit4",
    ],
)

java_test(
    name = "BFS",
    srcs = ["BFS.java"],
    test_class = "algorithms.named.BFS",
    deps = [
        "//third_party:junit4",
    ],
)

java_test(
    name = "DFS",
    srcs = ["DFS.java"],
    test_class = "algorithms.named.DFS",
    deps = [
        "//third_party:junit4",
    ],
)


java_test(
    name = "LinkedList",
    srcs = ["LinkedList.java"],
    test_class = "algorithms.named.LinkedList",
    deps = [
        "//third_party:junit4",
    ],
)

java_test(
    name = "TopologicalSort",
    srcs = ["TopologicalSort.java"],
    test_class = "algorithms.named.TopologicalSort",
    deps = [
        "//third_party:junit4",
    ],
)
