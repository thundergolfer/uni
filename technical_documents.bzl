def _technical_documents_impl(ctx):
    out_file = ctx.actions.declare_file("%s.dummy" % ctx.attr.name)

    ctx.actions.run_shell(
        # Input files visible to the action.
        inputs = ctx.files.inputs,
        # Output files that must be created by the action.
        outputs = [out_file],
        # The progress message uses `short_path` (the workspace-relative path)
        # since that's most meaningful to the user. It omits details from the
        # full path that would help distinguish whether the file is a source
        # file or generated, and (if generated) what configuration it is built
        # for.
#        progress_message = "Getting size of %s" % in_file.short_path,
        # The command to run. Alternatively we could use '$1', '$2', etc., and
        # pass the values for their expansion to `run_shell`'s `arguments`
        # param (see convert_to_uppercase below). This would be more robust
        # against escaping issues. Note that actions require the full `path`,
        # not the ambiguous truncated `short_path`.
        command = "echo \"$1\" > \"$2\"",
        arguments = [ctx.files.inputs[0].path, out_file.path]
    )

    return [DefaultInfo(files = depset([out_file]))]


technical_documents = rule(
    implementation = _technical_documents_impl,
    attrs = {
        "inputs": attr.label_list(
            allow_empty = False,
            doc = "TODO",
            allow_files = [".md"]
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
