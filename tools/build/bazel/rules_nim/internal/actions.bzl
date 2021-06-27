load("@bazel_skylib//lib:shell.bzl", "shell")

def nim_compile(ctx, projectfile, srcs, out):
    """
    Compiles a single Nim package from sources.

    Args:
        ctx: analysis context.
        projectfile: root source file. See: https://nim-lang.org/docs/nimc.html#compiler-usage-command-line-switches
        srcs: list of source Files to be compiled.
        out: output executable file.
    """
    cmd = "nim compile -o:{out} --nimcache:{gendir} {projectfile}".format(
        out = shell.quote(out.path),
        gendir = shell.quote(ctx.genfiles_dir.path),
        projectfile = shell.quote(projectfile.path),
    )
    ctx.actions.run_shell(
        outputs = [out],
        inputs = srcs,
        command = cmd,
        mnemonic = "NimCompile",
        use_default_shell_env = True,
    )
