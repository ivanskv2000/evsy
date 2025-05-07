#!/usr/bin/env python3

import sys
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION_FILE = ROOT / "VERSION"
PYPROJECT_FILE = ROOT / "backend" / "pyproject.toml"
PACKAGE_JSON_FILE = ROOT / "frontend" / "package.json"

def read_version():
    if not VERSION_FILE.exists():
        print("VERSION file not found.")
        sys.exit(1)
    return VERSION_FILE.read_text().strip()

def write_version(version: str):
    VERSION_FILE.write_text(version + "\n")

def bump_version(version: str, part: str) -> str:
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version)
    if not match:
        print(f"Invalid version: {version}")
        sys.exit(1)

    major, minor, patch = map(int, match.groups())

    if part == "major":
        return f"{major + 1}.0.0"
    elif part == "minor":
        return f"{major}.{minor + 1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        print("Usage: bump_version.py [major|minor|patch]")
        sys.exit(1)

def update_pyproject(version: str):
    if not PYPROJECT_FILE.exists():
        return
    content = PYPROJECT_FILE.read_text()
    content = re.sub(r'version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"', f'version = "{version}"', content)
    PYPROJECT_FILE.write_text(content)

def update_package_json(version: str):
    if not PACKAGE_JSON_FILE.exists():
        return
    data = json.loads(PACKAGE_JSON_FILE.read_text())
    if "version" in data:
        data["version"] = version
        PACKAGE_JSON_FILE.write_text(json.dumps(data, indent=2) + "\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: bump_version.py [major|minor|patch]")
        sys.exit(1)

    part = sys.argv[1]
    old_version = read_version()
    new_version = bump_version(old_version, part)

    write_version(new_version)
    update_pyproject(new_version)
    update_package_json(new_version)

    print(f"Bumped version: {old_version} → {new_version}")

if __name__ == "__main__":
    main()
