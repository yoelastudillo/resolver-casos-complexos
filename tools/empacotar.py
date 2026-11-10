#!/usr/bin/env python3
"""Build a deterministic tar.gz using the validated public file list."""
from __future__ import annotations
import argparse
import gzip
import io
import tarfile
from pathlib import Path
from validar_distribuicao import PUBLIC_FILES, validate


def package(root: Path, output: Path) -> None:
    root, output = root.resolve(), output.resolve()
    if output.is_relative_to(root):
        raise ValueError("Write the archive outside the repository directory")
    errors = validate(root)
    if errors:
        raise ValueError("\n".join(errors))
    # Exclusive creation prevents accidental overwrite.
    with output.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for name in PUBLIC_FILES:
                    data = (root / name).read_bytes().replace(b"\r\n", b"\n")
                    info = tarfile.TarInfo("resolver-casos-complexos/" + name)
                    info.size = len(data)
                    info.mode = 0o644
                    info.mtime = 0
                    archive.addfile(info, io.BytesIO(data))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="New .tar.gz path outside the repository")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    try:
        package(Path(args.repo), Path(args.output))
    except (ValueError, OSError) as error:
        parser.exit(1, f"ERROR: {error}\n")
    print("Archive created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

