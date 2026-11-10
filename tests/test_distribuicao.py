"""Regression tests for distribution failures, using isolated temporary copies."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
from validar_distribuicao import PUBLIC_FILES, SKILL_DIR, validate, validate_skill
from empacotar import package


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-distribution-test-")
        self.base = Path(self.temp.name).resolve()
        self.assertTrue(self.base.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.root = self.base / "repo"
        for name in PUBLIC_FILES:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, target)

    def tearDown(self):
        # Cleanup is restricted to the unique temporary directory verified above.
        self.temp.cleanup()

    def replace(self, name, old, new):
        target = self.root / name
        text = target.read_text(encoding="utf-8")
        self.assertIn(old, text)
        target.write_text(text.replace(old, new), encoding="utf-8", newline="\n")

    def test_current_distribution(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_interface_mapping(self):
        self.replace(f"{SKILL_DIR}/agents/openai.yaml", "interface:\n", "")
        self.assertTrue(any("interface mapping" in e for e in validate(self.root)))

    def test_duplicate_interface_field(self):
        target = self.root / SKILL_DIR / "agents/openai.yaml"
        with target.open("a", encoding="utf-8") as stream:
            stream.write('  display_name: "Duplicated"\n')
        self.assertTrue(any("duplicate" in e for e in validate(self.root)))

    def test_crlf_checkout(self):
        for target in self.root.rglob("*"):
            if target.is_file():
                target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.assertEqual(validate(self.root), [])

    def test_missing_bundled_license(self):
        (self.root / SKILL_DIR / "LICENSE").unlink()
        self.assertTrue(any("LICENSE" in e for e in validate(self.root)))

    def test_isolated_skill(self):
        isolated = self.base / "resolver-casos-complexos"
        shutil.copytree(self.root / SKILL_DIR, isolated)
        version = (self.root / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(validate_skill(isolated, version), [])

    def test_dependency_outside_skill(self):
        target = self.root / SKILL_DIR / "SKILL.md"
        with target.open("a", encoding="utf-8") as stream:
            stream.write("\n[External dependency](../../README.md)\n")
        self.assertTrue(any("outside installable folder" in e for e in validate(self.root)))

    def test_broken_link(self):
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[Missing](missing.md)\n")
        self.assertTrue(any("Broken link" in e for e in validate(self.root)))

    def test_broken_anchor(self):
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[Missing](README.md#nonexistent-section)\n")
        self.assertTrue(any("Broken anchor" in e for e in validate(self.root)))

    def test_extra_file(self):
        (self.root / "case-note.txt").write_text("synthetic", encoding="utf-8")
        self.assertTrue(any("Unexpected file" in e for e in validate(self.root)))

    def test_invalid_evaluation_json(self):
        (self.root / "evals/casos.json").write_text("{}", encoding="utf-8")
        self.assertTrue(any("evaluation" in e for e in validate(self.root)))

    def test_version_drift(self):
        (self.root / "VERSION").write_text("9.0.0\n", encoding="utf-8")
        self.assertTrue(any("version" in e.lower() for e in validate(self.root)))

    def test_evaluation_snapshot_drift(self):
        target = self.root / SKILL_DIR / "references/evidencias.md"
        with target.open("a", encoding="utf-8") as stream:
            stream.write("\nChanged behavior.\n")
        self.assertTrue(any("snapshot differs" in e for e in validate(self.root)))

    def test_exposure_pattern(self):
        key = "access_" + "token"
        value = "synthetic-" + "value-0123456789"
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write(f'\n{key} = "{value}"\n')
        self.assertTrue(any("potential" in e for e in validate(self.root)))

    def test_reproducible_archive_and_no_overwrite(self):
        first, second = self.base / "first.tar.gz", self.base / "second.tar.gz"
        package(self.root, first)
        package(self.root, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with self.assertRaises(FileExistsError):
            package(self.root, first)

    def test_reject_output_inside_repository(self):
        with self.assertRaises(ValueError):
            package(self.root, self.root / "bad.tar.gz")


if __name__ == "__main__":
    unittest.main()

