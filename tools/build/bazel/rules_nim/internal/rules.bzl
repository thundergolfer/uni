load(":actions.bzl", "nim_compile")

def _nim_binary_impl(ctx):
    # Declare an output file for the main package and compile it from srcs.
    executable = ctx.actions.declare_file(ctx.label.name)
    nim_exe= ctx.executable._nim
    nim_compile(
        ctx,
        nim_exe = nim_exe,
        projectfile = ctx.file.projectfile,
        srcs = ctx.files.srcs,
        out = executable,
    )

    # Return the DefaultInfo provider. This tells Bazel what files should be
    # built when someone asks to build a nim_binary rule. It also says which
    # one is executable (in this case, there's only one).
    return [
        DefaultInfo(
            files = depset([executable]),
            executable = executable,
        )
    ]


nim_binary = rule(
    _nim_binary_impl,
    attrs = {
        "srcs": attr.label_list(
            allow_files = [".nim"],
            doc = "Source files to compile for this package",
        ),
        "projectfile": attr.label(
            allow_single_file = True,
            doc = "Nim 'projectfile' to compile for this package",
            mandatory = True,
        ),
        "_nim": attr.label(
            allow_single_file = True,
            default = "@nim_prebuilt//:exe",
            executable = True,
            cfg = "exec",
        )
    },
    doc = "Builds an executable program from Nim-lang source code",
    executable = True,
)