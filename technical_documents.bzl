def _technical_documents_impl(ctx):
    all_reference_srcs = []
    if ctx.attr.references:
        for ref in ctx.attr.references:
            all_reference_srcs.append(ref.files)

    reference_files_ds = depset(transitive = all_reference_srcs)

    reference_files_list = reference_files_ds.to_list()

    for input_md_file in ctx.files.inputs:
        out_file = ctx.actions.declare_file("%s.preprocessed" % input_md_file.short_path)
        args = [input_md_file.path, out_file.path] + [f.path for f in reference_files_list]
        ctx.actions.run(
            # Input files visible to the action.
            inputs = [input_md_file] + reference_files_list,
            # Output files that must be created by the action.
            outputs = [out_file],
            arguments = args,
            progress_message = "Running preprocessor, outputting to %s" % out_file.short_path,
            executable = ctx.executable._preprocessor,
        )

    return [DefaultInfo(files = depset([out_file]))]


technical_documents = rule(
    implementation = _technical_documents_impl,
    attrs = {
        "inputs": attr.label_list(
            allow_empty = False,
            doc = "TODO",
            allow_files = [".md"]
        ),
        "references": attr.label_list(
            allow_empty=True,
            allow_files=True,
            doc="TODO",
        ),
        "_preprocessor": attr.label(
            executable = True,
            cfg = "host",
            default = Label("@technical_documentation_system//preprocessor"),
        )
    },
)

def _tech_docs_website_impl(ctx):
    output = ctx.actions.declare_file("docs_webserver.sh")
    args = []
    ctx.actions.expand_template(
        template = ctx.file._template,
        output = output,
        substitutions = {
            "{EXE}": ctx.executable._webserver.short_path,
            "{ARGS}": " ".join(args),
        },
        is_executable=True
    )
    runfiles = ctx.runfiles(
        files = [ctx.executable._webserver, ctx.attr._webserver.files_to_run.executable] + ctx.attr._webserver.files.to_list(),
    )
    runfiles.merge(ctx.attr._webserver.default_runfiles)
    runfiles.merge(ctx.attr._webserver.data_runfiles)

    return DefaultInfo(
        runfiles = runfiles,
        executable = output,
    )

technical_documentation_website = rule(
    implementation = _tech_docs_website_impl,
    attrs = {
        "srcs": attr.label_keyed_string_dict(
            allow_empty = True,
            allow_files = [".md"]
        ),
        "_webserver": attr.label(
            default = Label("@technical_documentation_system//server"),
            providers = [JavaInfo],
            executable = True,
            cfg = "target",
        ),
        "_template": attr.label(
            default = Label("@technical_documentation_system//templates:run_docs_webserver.sh.tpl"),
            allow_single_file = True,
        )
    },
    executable = True,
)
