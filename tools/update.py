import os
import pathlib
import shutil
import sys

USAGE = "USAGE: update.py \"$(git rev-parse --show-toplevel)\""


def add_frontmatter_prefix_to_file(path):
    """
    If (empty) frontmatter isn't added, Hugo will refuse to parse a Markdown file with HTML
    in it EVEN IF unsafe=true is set.
    """
    with open(path, "r") as contents:
        saved = contents.read()
    with open(path, "w") as contents:
        contents.write("""---
---
""")
    with open(path, "a") as contents:
        contents.write(saved)


def main(repo_root: str):
    repo_root_path = pathlib.Path(repo_root)
    docs_root = repo_root_path / "docs" / "source" / "content" / "docs"

    # Clean
    shutil.rmtree(docs_root)

    repo_readmes = list(repo_root_path.glob('**/readme.md')) + list(repo_root_path.glob('**/README.md'))
    for readme in repo_readmes:
        # TODO(Jonathon): Clean this repetitive hack code up.
        if repo_root_path / "docs" in readme.parents:
            print(f"Skipping: {readme}")
            continue

        if ".devcontainer" in str(readme):
            print(f"Skipping: {readme}")
            continue

        if "vendor" in str(readme):
            print(f"Skipping: {readme}")
            continue

        dest = docs_root / readme.relative_to(repo_root_path).parent / "_index.md"
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(readme, dest)
        add_frontmatter_prefix_to_file(dest)

    # The "book" Hugo theme will only display the file tree on the left if each subdirectory
    # contains an _index.md file. It can be empty, so we create empty _index.md files where a
    # subdirectory is missing one.
    for root, dirs, files in os.walk(docs_root):
        if "_index.md" not in root:
            pathlib.Path(root, "_index.md").touch()

    # TODO(Jonathon): Right now relative references to images in Markdown files do not work. Fix that.
    # TODO(Jonathon): Have re-write all the links in the Markdown because otherwise they 404 on my personal website.
    #                 Need to add uni/ prefix.


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(USAGE, file=sys.stderr)
        exit(1)
    repo_root = sys.argv[1]
    main(repo_root=repo_root)
