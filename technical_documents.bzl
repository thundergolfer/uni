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


def _dict_to_pairs_of_strings(d):
    result = []
    for key, val in d.items():
        result.append(key)
        result.append(val)
    return result


def _tech_docs_website_impl(ctx):
    output = ctx.actions.declare_file("docs_webserver.sh")
    map_url_path_to_doc = {}
    map_url_path_to_label = {}  # Maintained only for more user friendly error messages.
    docs = []

    for target, path_prefix in ctx.attr.srcs.items():
        doc_files = target.files.to_list()
        docs.extend(doc_files)
        # Map each document under the target's outputs (likely a `technical_documents` target) to the
        # URL subpath is will be served under, and pair that with the document's runfiles location in the WORKSPACE.
        for doc_file in doc_files:
            url_path = "{}/{}".format(path_prefix, doc_file.short_path.replace(".preprocessed", ""))
            runfiles_location = ctx.workspace_name + "/" + doc_file.short_path
            if url_path in map_url_path_to_doc:
                err_msg = (
                    "Found duplicate. '{url_p}' already maps to '{curr_doc}' from the '{curr_label}' target, so " +
                    "cannot also map to '{new_doc}' from the '{new_label}' target"
                )
                print(type(map_url_path_to_label[url_path]))
                fail(err_msg.format(
                    url_p=url_path,
                    curr_doc=map_url_path_to_doc[url_path],
                    curr_label = map_url_path_to_label[url_path],
                    new_doc=runfiles_location,
                    new_label=target.label,
                ))
            map_url_path_to_doc[url_path] = runfiles_location
            map_url_path_to_label[url_path] = target.label

    args = _dict_to_pairs_of_strings(d=map_url_path_to_doc)
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
