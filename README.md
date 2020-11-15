<p align="center">
  <img src="https://user-images.githubusercontent.com/12058921/85215787-98fc8480-b3c0-11ea-8d11-3f5eab64144b.png" height="150px"/>
</p>

<h1 align="center"><code>technical-documentation-system</code></h1>
<p align="center">
    <a href="https://github.com/thundergolfer/technical-documentation-system/actions/">
        <img src="https://github.com/thundergolfer/technical-documentation-system/workflows/CI/badge.svg">
    </a>
</p>

---

This documentation system exists as an experiment in providing a few features that I am coming to believe help ensure great technical documentation:

1. **Code updates and any required changes to relevant documentation can be completed in _one workflow_, a pull request.** 
    * No jumping into [_Confluence_](https://www.atlassian.com/software/confluence) once a pull request is merged.
2. **Code in documentation should _run_.** Any code shown in technical documentation has automated testing for compilation and format.
    * No copy-pasting code from docs and finding a referenced object has been removed/renamed or that there's a missing semicolon. 
3. **Code in documentation should be tested.** Any code functionality shown in technical documentation can be unit or integration tested.
    * No more forgetting to update documentation when you change the behaviour of your code.
    
> **Note:** This documentation system is built to integrate with the [Bazel](https://bazel.build/) build system. 💚🌿 
    
## Usage

This system acts a pre-processor, taking Markdown documentation files as input, converting special references to code targets into 
'materialised' code blocks and returning Markdown files as output.

During pre-processing, the Bazel build system can also run tests and other checks on referenced code, as referenced code just a 
target in the build graph.

To provide this functionality, **`technical-documentation-system`** exposes the `technical_documents` Bazel rule:

```python
technical_documents(
    name = "doc_1",
    inputs = ["hello-world.md"],
    references = [
        "//foo/bar",
        "//bee/boo:biz",
    ],
)
```

For detailed documentation of the rule, see: [`TODO.md`]().

### Basic Static Documentation Webserver.

While the system is designed to be agnostic of the particular documentation framework used, a minimal 'render and serve' engine
is provided. It is exposed via the `technical_documentation_website` Bazel rule:

```python
technical_documentation_website(
    name = "all_docs",
    srcs = {
        "//:doc_1": "/foo"  # <key = document> : <value = position in website's doc-tree>
    }
)
```

Use `bazel run //path/to:all_docs` to run the minimal document server at [localhost:8000](http://localhost:8000/). 🚀

Any Markdown documents in `//:doc_1` will be served under `/foo/`, eg. `localhost/foo/getting-started.md`. 

## Installation

The project has no dependencies, so it's easy to install in your Bazel `WORKSPACE`:

```python
tech_docs_system_version = "<some git-sha>"

http_archive(
    name = "technical_documentation_system",
    sha256 = "",
    strip_prefix = "technical-documentation-system-{version}".format(version = tech_docs_system_version),
    url = "https://github.com/thundergolfer/technical-documentation-system/archive/{version}.tar.gz".format(
        version = tech_docs_system_version,
    ),
)
```

## Development

### Build

`bazel build //...`

### Test

`bazel test //...`
