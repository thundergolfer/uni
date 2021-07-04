## Docs

You can get a basic webserver to serve these static files by doing:

```
cd "$(git rev-parse --show-toplevel)/docs"
python3 -m http.server
```

### The Setup

This repo's documentation uses the Hugo static site generator. At the moment the `hugo` CLI
is installed with `brew` but in future it will be downloaded within Bazel. 

The source for the static site is contained within [docs/source](/docs/source). 

A Github Action runs `hugo` and builds the site into `docs/` and those built files are committed to
the `gh-pages` branch, which is where Github Pages deploys from.

**To update the source files for the documentation, run `./tools/update.sh`**.

This copies/updates Markdown files into `docs/source` so that Hugo can build them into the site.  
