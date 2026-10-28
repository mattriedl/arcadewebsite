#!/usr/bin/env python3
"""Create a cPanel overlay, excluding original games and thumbnails."""
from pathlib import Path
import tarfile
root=Path(__file__).resolve().parent
archive=root/'arcadewebsite-redesign.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
 for file in sorted((root/'site').rglob('*')):
  rel=file.relative_to(root/'site')
  if file.is_symlink() or rel.parts[0] in ('games','thumbnails'):continue
  if file.is_file():tar.add(file,arcname=str(rel),recursive=False)
print(str(archive))
