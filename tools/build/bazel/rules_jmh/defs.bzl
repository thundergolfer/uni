"""
Credit to https://github.com/buchgr/rules_jmh for the original code.

- Run with Bazel

    $ bazel run :example-benchmarks -- -f 0 -bm avgt

- Run Standalone

    $ bazel build :example-benchmarks_deploy.jar
    # Shutdown Bazel for it to not interfere with your benchmark
    $ bazel shutdown
    # Run the benchmark
    $ java -jar bazel-bin/example-benchmarks_deploy.jar

"""

def java_jmh_benchmarks(name, srcs, deps=[], tags=[], plugins=[], **kwargs):
    """
    Builds runnable JMH benchmarks.
    This rule builds a runnable target for one or more JMH benchmarks
    specified as srcs. It takes the same arguments as java_binary,
    except for main_class.
    """
    plugin_name = "_{}_jmh_annotation_processor".format(name)
    native.java_plugin(
        name = plugin_name,
        deps = [
            # Using the monorepo's dep list.
            "@maven//:org_openjdk_jmh_jmh_generator_annprocess"
        ],
        processor_class = "org.openjdk.jmh.generators.BenchmarkProcessor",
        visibility = ["//visibility:private"],
        tags = tags,
    )
    native.java_binary(
        name = name,
        srcs = srcs,
        main_class = "org.openjdk.jmh.Main",
        deps = deps + [
            # Using the monorepo's dep list, @maven.
            "@maven//:org_openjdk_jmh_jmh_core"
        ],
        plugins = plugins + [plugin_name],
        tags = tags,
        **kwargs
    )
