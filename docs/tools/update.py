import pathlib
import shutil
import sys

USAGE = "USAGE: update.py \"$(git rev-parse --show-toplevel)\""


def main(repo_root: str):
    repo_root_path = pathlib.Path(repo_root)
    docs_root = repo_root_path / "docs" / "source" / "content" / "docs"
    repo_readmes = list(repo_root_path.glob('**/readme.md')) + list(repo_root_path.glob('**/README.md'))

    for readme in repo_readmes:
        if repo_root_path / "docs" in readme.parents:
            print(f"Skipping: {readme}")
            continue

        if ".devcontainer" in str(readme):
            print(f"Skipping: {readme}")
            continue

        dest = docs_root / readme.relative_to(repo_root_path).parent / "_index.md"
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(readme, dest)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(USAGE, file=sys.stderr)
        exit(1)
    repo_root = sys.argv[1]
    main(repo_root=repo_root)
