#!/usr/bin/env python3
"""Validate this repository's canonical layout; not a general YAML or security audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKILL_DIR = "skills/resolver-casos-complexos"
SKILL_FILES = (
    "SKILL.md", "LICENSE", "agents/openai.yaml", "assets/registro.md",
    "references/evidencias.md", "references/decisoes.md",
    "references/continuidade.md", "references/dados-e-fontes.md",
)
PUBLIC_FILES = tuple(sorted((
    ".gitattributes", ".gitignore", ".github/workflows/validate.yml",
    "AGENTS.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE", "README.md", "VERSION",
    "evals/README.md", "evals/RESULTADOS.md", "evals/casos.json", "evals/execucoes.json",
    "evals/saidas/fornecedor-com-skill.md", "evals/saidas/fornecedor-sem-skill.md",
    "tools/validar_distribuicao.py", "tools/empacotar.py",
    "tests/test_distribuicao.py",
    *(f"{SKILL_DIR}/{name}" for name in SKILL_FILES),
)))
LINK = re.compile(r"\[[^\]]*\]\(([^\s)]+)\)")
EXPOSURE = (
    re.compile(r"oai-" + r"library://"),
    re.compile(r"lib" + r"file_[a-f0-9]{8,}", re.I),
    re.compile(r"[A-Za-z]:[\\/](?:Users|home)[\\/]", re.I),
    re.compile(r"/(?:Users|home|root|workspace|mnt/data)/"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
)


def read_text(path: Path) -> str:
    """Normalize line endings so a Windows checkout remains valid."""
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


def without_fences(text: str) -> str:
    return re.sub(r"(?ms)^`{3}[^\n]*\n.*?^`{3}\s*$", "", text)


def anchors(text: str) -> set[str]:
    found: set[str] = set()
    counts: dict[str, int] = {}
    for title in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", without_fences(text)):
        slug = re.sub(r"[^\w\-\s]", "", re.sub(r"<[^>]+>", "", title).lower())
        slug = re.sub(r"\s", "-", slug)
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(slug if count == 0 else f"{slug}-{count}")
    return found


def validate_skill(root: Path, version: str | None = None) -> list[str]:
    """Check an isolated installable folder, without relying on repository files."""
    errors: list[str] = []
    root = root.resolve()
    for name in SKILL_FILES:
        if not (root / name).is_file():
            errors.append(f"Skill file missing: {name}")
    try:
        skill = read_text(root / "SKILL.md")
        match = re.match(r"\A---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: (.+)\n---\n", skill)
        if not match:
            errors.append("Invalid canonical frontmatter")
        else:
            name, raw = match.groups()
            if name != root.name or len(name) > 64:
                errors.append("Skill name does not match its directory")
            description = json.loads(raw)
            if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
                errors.append("Invalid description")
        if len(skill.splitlines()) >= 500:
            errors.append("SKILL.md must remain below 500 lines")
        if version and f"Versão {version}." not in skill:
            errors.append("Skill version mismatch")
        links = LINK.findall(without_fences(skill))
        for name in SKILL_FILES:
            if name.startswith(("references/", "assets/")) and name not in links:
                errors.append(f"Resource not linked directly: {name}")
        for path in root.rglob("*.md"):
            for target in LINK.findall(without_fences(read_text(path))):
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                destination = (path.parent / unquote(target.split("#")[0])).resolve()
                if not destination.is_relative_to(root):
                    errors.append(f"Skill dependency outside installable folder: {path.name}")
        ui = read_text(root / "agents/openai.yaml").strip()
        lines = ui.splitlines()
        if not lines or lines[0] != "interface:":
            errors.append("Missing interface mapping")
        values = {}
        for line in lines[1:]:
            field = re.fullmatch(r"  ([a-z_]+): (.+)", line)
            if not field or field[1] in values:
                errors.append("Invalid or duplicate interface field")
                continue
            value = json.loads(field[2])
            if not isinstance(value, str) or not value.strip():
                errors.append("Invalid interface string")
            else:
                values[field[1]] = value
        if set(values) != {"display_name", "short_description", "default_prompt"}:
            errors.append("Incomplete interface metadata")
        if not 25 <= len(values.get("short_description", "")) <= 64:
            errors.append("Invalid interface description length")
        if "$resolver-casos-complexos" not in values.get("default_prompt", ""):
            errors.append("Default prompt does not invoke the skill")
        if "MIT License" not in read_text(root / "LICENSE"):
            errors.append("Bundled license is missing")
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        errors.append(f"Cannot parse skill: {type(error).__name__}")
    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    if not root.is_dir():
        return ["Repository directory not found"]
    actual = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        name = relative.as_posix()
        if path.is_symlink():
            errors.append(f"Symlink not allowed: {name}")
        elif path.is_file():
            actual[name] = path
    for name in sorted(set(PUBLIC_FILES) - set(actual)):
        errors.append(f"Missing file: {name}")
    for name in sorted(set(actual) - set(PUBLIC_FILES)):
        errors.append(f"Unexpected file: {name}")
    texts = {}
    for name, path in actual.items():
        try:
            text = read_text(path)
            texts[path.resolve()] = text
            if text.startswith("\ufeff") or "\x00" in text:
                errors.append(f"Unexpected BOM or NUL: {name}")
            if any(pattern.search(text) for pattern in EXPOSURE):
                errors.append(f"Review potential private path or secret: {name}")
        except (OSError, UnicodeError):
            errors.append(f"Cannot read UTF-8: {name}")
    version = texts.get(root / "VERSION", "").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("Invalid VERSION")
    errors.extend(validate_skill(root / SKILL_DIR, version))
    if texts.get(root / "LICENSE") != texts.get(root / SKILL_DIR / "LICENSE"):
        errors.append("Repository and skill licenses differ")
    for name, marker in (
        ("README.md", f"Versão: {version}."),
        ("CHANGELOG.md", f"## {version} "),
        ("evals/RESULTADOS.md", f"versão {version}"),
    ):
        if marker not in texts.get(root / name, ""):
            errors.append(f"Version mismatch: {name}")
    for path, text in texts.items():
        if path.suffix != ".md":
            continue
        for target in LINK.findall(without_fences(text)):
            target = unquote(target.strip("<>"))
            if urlsplit(target).scheme:
                continue
            filepart, _, fragment = target.partition("#")
            destination = (path.parent / filepart).resolve() if filepart else path
            if not destination.is_relative_to(root):
                errors.append(f"Link outside repository: {path.relative_to(root)}")
            elif not destination.is_file():
                errors.append(f"Broken link: {path.relative_to(root)} -> {target}")
            elif fragment and fragment not in anchors(texts.get(destination, "")):
                errors.append(f"Broken anchor: {path.relative_to(root)} -> {target}")
    try:
        cases = json.loads(texts.get(root / "evals/casos.json", ""))
        if not isinstance(cases, list) or not cases:
            raise ValueError
        ids = []
        for case in cases:
            if not isinstance(case, dict) or not re.fullmatch(r"[a-z0-9_]+", case.get("id", "")):
                raise ValueError
            if not isinstance(case.get("solicitacao"), str) or not case["solicitacao"].strip():
                raise ValueError
            if not isinstance(case.get("criterios_de_revisao"), list) or not case["criterios_de_revisao"]:
                raise ValueError
            if not all(isinstance(c, str) and c.strip() for c in case["criterios_de_revisao"]):
                raise ValueError
            ids.append(case["id"])
        if len(ids) != len(set(ids)):
            raise ValueError
        runs = json.loads(texts.get(root / "evals/execucoes.json", ""))
        if not isinstance(runs.get("execucoes"), list) or runs.get("versao") != version:
            raise ValueError
        snapshots = runs.get("distribuicao_skill_sha256")
        if not isinstance(snapshots, dict) or set(snapshots) != set(SKILL_FILES):
            raise ValueError
        for name, expected_hash in snapshots.items():
            content = texts.get(root / SKILL_DIR / name, "")
            current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            if current_hash != expected_hash:
                errors.append(f"Evaluation snapshot differs from skill: {name}")
        for run in runs["execucoes"]:
            if run.get("caso") not in ids or run.get("estado") not in {"concluida", "interrompida"}:
                raise ValueError
            output = run.get("saida")
            if run["estado"] == "concluida" and (not isinstance(output, str) or output not in PUBLIC_FILES):
                raise ValueError
            if run["estado"] == "interrompida" and output is not None:
                raise ValueError
    except (ValueError, TypeError, AttributeError):
        errors.append("Invalid evaluation data")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--list-files", action="store_true")
    args = parser.parse_args()
    errors = validate(Path(args.repo))
    if errors:
        print("\n".join("ERROR: " + error for error in errors))
        return 1
    print("\n".join(PUBLIC_FILES) if args.list_files else f"PASS: {len(PUBLIC_FILES)} files; layout, canonical metadata, local links, versions and evaluation records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

