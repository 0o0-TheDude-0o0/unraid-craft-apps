import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "build" / "check-releases.py"
SPEC = importlib.util.spec_from_file_location("check_releases", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class ReleaseCheckerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.versions = Path(self.directory.name)
        self.lock = self.versions / "photocraft.lock"
        self.lock.write_text(f"v1.2.3\n{'a' * 64}\n{'b' * 64}\n")

    def tearDown(self):
        self.directory.cleanup()

    def release(self, tag="v1.2.4", digest=None, assets=True):
        version = tag.removeprefix("v")
        return {
            "tag_name": tag,
            "draft": False,
            "prerelease": False,
            "assets": ([{
                "name": f"photocraft-{version}-linux-x86_64.deb",
                "digest": f"sha256:{digest or 'c' * 64}",
            }] if assets else []),
        }

    def test_new_release_updates_only_x86_hash(self):
        updates = checker.plan_updates(self.versions, lambda app: self.release())
        self.assertEqual(len(updates), 1)
        self.assertEqual(updates[0][2:], ("v1.2.4", "c" * 64, "b" * 64))
        self.assertEqual(self.lock.read_text().splitlines()[0], "v1.2.3")

    def test_same_release_is_unchanged(self):
        updates = checker.plan_updates(
            self.versions, lambda app: self.release("v1.2.3", "a" * 64)
        )
        self.assertEqual(updates, [])

    def test_replaced_asset_requires_review(self):
        with self.assertRaisesRegex(ValueError, "asset changed without a new release tag"):
            checker.plan_updates(self.versions, lambda app: self.release("v1.2.3"))

    def test_missing_x86_asset_does_not_advance_lock(self):
        with self.assertRaisesRegex(ValueError, "Expected one"):
            checker.plan_updates(self.versions, lambda app: self.release(assets=False))
        self.assertEqual(self.lock.read_text().splitlines()[0], "v1.2.3")

    def test_older_latest_release_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "older than pinned"):
            checker.plan_updates(self.versions, lambda app: self.release("v1.2.2"))


if __name__ == "__main__":
    unittest.main()
