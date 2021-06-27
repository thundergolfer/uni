load("@bazel_skylib//lib:shell.bzl", "shell")

def nim_compile(ctx, nim_exe, projectfile, srcs, out):
    """
    Compiles a single Nim package from sources.

    Args:
        ctx: analysis context.
        nim_exe: in-build Nim executable.
        projectfile: root source file. See: https://nim-lang.org/docs/nimc.html#compiler-usage-command-line-switches
        srcs: list of source Files to be compiled.
        out: output executable file.
    """
    cmd = "{nim} compile -o:{out} --nimcache:{gendir} {projectfile}".format(
        nim = nim_exe.path,
        out = shell.quote(out.path),
        gendir = shell.quote(ctx.genfiles_dir.path),
        projectfile = shell.quote(projectfile.path),
    )
    ctx.actions.run_shell(
        outputs = [out],
        inputs = srcs + [nim_exe],
        command = cmd,
        mnemonic = "NimCompile",
        use_default_shell_env = True,
    )
