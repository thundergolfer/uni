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
    docs = []

    for label, path_prefix in ctx.attr.srcs.items():
        doc_files = label.files.to_list()
        docs.extend(doc_files)
        # Map each document under the label's outputs (likely a label for a `technical_documents` target) to the
        # URL subpath is will be served under, and pair that with the document's runfiles location in the WORKSPACE.
        for doc_file in doc_files:
            url_path = "{}/{}".format(path_prefix, doc_file.short_path.replace(".preprocessed", ""))
            runfiles_location = ctx.workspace_name + "/" + doc_file.short_path
            args.extend([
                url_path,
                runfiles_location
            ])

    executable_script = [
        "#!/usr/bin/env bash",
        "{exe} {arguments}".format(
            exe=ctx.executable._webserver.short_path,
            arguments=" ".join(args),
        ),
    ]

    ctx.actions.write(
        output = output,
        content = "\n".join(executable_script),
    )

    runfiles = ctx.runfiles(
        files = docs + [ctx.executable._webserver],
    )

    return DefaultInfo(
        executable = output,
        runfiles = runfiles.merge(ctx.attr._webserver[DefaultInfo].default_runfiles),
    )

technical_documentation_website = rule(
    implementation = _tech_docs_website_impl,
    attrs = {
        "srcs": attr.label_keyed_string_dict(
            allow_empty = True,
            allow_files = [".md", ".md.preprocessed"]
        ),
        "_webserver": attr.label(
            cfg = "host",
            default = Label("@technical_documentation_system//server"),
            executable = True,
            providers = [JavaInfo],
        ),
    },
    executable = True,
)
