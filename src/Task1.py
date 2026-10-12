"""Task 1: check pinned dependencies in requirements.txt against the PyPI JSON API."""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

PYPI_URL = "https://pypi.org/pypi/{path}/json"
TIMEOUT_SECONDS = 15


def fetch_json(path: str) -> dict | None:
    """Return the parsed PyPI JSON for ``path``, or ``None`` if PyPI answers 404."""
    try:
        with urllib.request.urlopen(PYPI_URL.format(path=path), timeout=TIMEOUT_SECONDS) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def read_requirements(path: Path) -> list[tuple[str, str]]:
    """Read ``name==version`` lines, ignoring blank lines and comments."""
    pins = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, _, version = line.partition("==")
        pins.append((name.strip(), version.strip()))
    return pins


def main(requirements_file: str = "requirements.txt") -> None:
    pins = read_requirements(Path(requirements_file))
    missing_packages = 0
    missing_versions = 0
    oldest: tuple[str, str, str] | None = None  # (upload_time, name, version)

    for name, version in pins:
        release = fetch_json(f"{name}/{version}")
        if release is None:
            # Release not found: is it the package or only the version?
            if fetch_json(name) is None:
                missing_packages += 1
            else:
                missing_versions += 1
            continue

        files = release["urls"]
        if files:  # the first file's upload time decides the release date
            upload_time = files[0]["upload_time"]
            if oldest is None or upload_time < oldest[0]:
                oldest = (upload_time, name, version)

    print(f"Dependencies checked: {len(pins)}")
    print(f"Package not on PyPI: {missing_packages}")
    print(f"Version not on PyPI: {missing_versions}")
    if oldest:
        upload_time, name, version = oldest
        print(f"Oldest pinned release: {name}=={version} ({upload_time[:4]})")
    else:
        print("Oldest pinned release: none")


if __name__ == "__main__":
    main(*sys.argv[1:])
