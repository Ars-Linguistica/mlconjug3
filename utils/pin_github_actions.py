"""
Pin GitHub Actions in workflow YAML files to immutable commit SHAs.

Usage:
    python pin_github_actions.py path/to/workflow.yml
"""

import re
import sys
import requests
from pathlib import Path

GITHUB_API = "https://api.github.com/repos"


# -----------------------------
# Resolve tag → commit SHA
# -----------------------------
def resolve_sha(repo: str, tag: str) -> str:
    """
    Resolve a GitHub Action tag to a commit SHA.
    """
    url = f"{GITHUB_API}/{repo}/git/ref/tags/{tag}"
    r = requests.get(url)

    if r.status_code != 200:
        raise RuntimeError(f"Failed to resolve {repo}@{tag}: {r.text}")

    data = r.json()

    # annotated tag → dereference
    if data["object"]["type"] == "tag":
        tag_url = data["object"]["url"]
        tag_data = requests.get(tag_url).json()
        return tag_data["object"]["sha"]

    return data["object"]["sha"]


# -----------------------------
# Parse and replace YAML
# -----------------------------
USES_PATTERN = re.compile(r"uses:\s*([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)@([a-zA-Z0-9_.-]+)")


def pin_file(file_path: Path):
    """
    Replace all action tags in a workflow file with pinned SHAs.
    """
    content = file_path.read_text()

    def replacer(match):
        repo = match.group(1)
        tag = match.group(2)

        try:
            sha = resolve_sha(repo, tag)
            return f"uses: {repo}@{sha}  # pinned from {tag}"
        except Exception as e:
            print(f"[WARN] Skipping {repo}@{tag}: {e}")
            return match.group(0)

    new_content = USES_PATTERN.sub(replacer, content)

    file_path.write_text(new_content)
    print(f"✔ Updated: {file_path}")


# -----------------------------
# CLI entry
# -----------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python pin_github_actions.py <workflow.yml>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    pin_file(file_path)


if __name__ == "__main__":
    main()
