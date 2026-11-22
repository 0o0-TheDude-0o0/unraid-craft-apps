#!/usr/bin/env python3
"""Update pinned x86-64 ArtCraft releases from GitHub release metadata."""

import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
VERSION = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def version_tuple(tag):
    match = VERSION.fullmatch(tag)
    if match is None:
        raise ValueError(f"Unsupported release tag: {tag!r}")
    return tuple(map(int, match.groups()))


def fetch_release(app):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "craft-apps-release-checker",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(
        f"https://api.github.com/repos/storytold/{app}/releases/latest",
        headers=headers,
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except (HTTPError, URLError) as error:
        raise RuntimeError(f"Could not fetch latest {app} release: {error}") from error


def plan_updates(versions_dir, get_release=fetch_release):
    locks = sorted(versions_dir.glob("*.lock"))
    if not locks:
        raise ValueError(f"No app locks found in {versions_dir}")

    updates = []
    for lock in locks:
        app = lock.stem
        if re.fullmatch(r"[a-z][a-z0-9-]*", app) is None:
            raise ValueError(f"Unexpected app name: {app!r}")
        lines = lock.read_text().splitlines()
        if len(lines) != 3 or not SHA256.fullmatch(lines[1]) or not SHA256.fullmatch(lines[2]):
            raise ValueError(f"Invalid lock file: {lock}")

        old_tag = lines[0]
        old_version = version_tuple(old_tag)
        release = get_release(app)
        if release.get("draft") or release.get("prerelease"):
            raise ValueError(f"Latest {app} release is not stable")
        new_tag = release["tag_name"]
        new_version = version_tuple(new_tag)
        asset_name = f"{app}-{new_tag.lstrip('v')}-linux-x86_64.deb"
        assets = [asset for asset in release["assets"] if asset["name"] == asset_name]
        if len(assets) != 1:
            raise ValueError(f"Expected one {asset_name} asset in {new_tag}; found {len(assets)}")
        digest = assets[0].get("digest")
        if not isinstance(digest, str) or not digest.startswith("sha256:"):
            raise ValueError(f"Missing SHA-256 digest for {asset_name}")
        new_sha = digest.removeprefix("sha256:")
        if not SHA256.fullmatch(new_sha):
            raise ValueError(f"Invalid SHA-256 digest for {asset_name}")

        if new_version < old_version:
            raise ValueError(f"Latest {app} release {new_tag} is older than pinned {old_tag}")
        if new_version == old_version:
            if new_sha != lines[1]:
                raise ValueError(f"{app} asset changed without a new release tag: {new_tag}")
            continue

        # ARM64 is deferred; keep its existing checksum until that build is supported.
        updates.append((lock, old_tag, new_tag, new_sha, lines[2]))
    return updates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report updates without writing locks")
    args = parser.parse_args()

    updates = plan_updates(ROOT / "versions")
    for lock, old_tag, new_tag, new_sha, arm_sha in updates:
        print(f"{lock.stem}: {old_tag} -> {new_tag}")
        if not args.dry_run:
            lock.write_text(f"{new_tag}\n{new_sha}\n{arm_sha}\n")
    print(f"{len(updates)} app release(s) changed")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, RuntimeError) as error:
        print(f"Release check failed: {error}", file=sys.stderr)
        sys.exit(1)
