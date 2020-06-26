def _technical_documents_impl(ctx):
    all_reference_srcs = []
    if ctx.attr.references:
        for ref in ctx.attr.references:
#            print(ref)
#            print(ref.files)
            all_reference_srcs.append(ref.files)
#            print(dir(ref))

    reference_files_ds = depset(transitive = all_reference_srcs)

    out_file = ctx.actions.declare_file("%s.preprocessed" % ctx.files.inputs[0].short_path)

    args = [ctx.files.inputs[0].path, out_file.path] + [f.path for f in reference_files_ds.to_list()]

    ctx.actions.run(
        # Input files visible to the action.
        inputs = ctx.files.inputs,
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
    pass

technical_documentation_website = rule(
    implementation = _tech_docs_website_impl,
    attrs = {
        "srcs": attr.label_keyed_string_dict(
            allow_empty = True,
            allow_files = [".md"]
        ),
        "_preprocessor": attr.label(
            default = Label("@technical_documentation_system//preprocessor"),
        )
    }
)
