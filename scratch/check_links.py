import re
from pathlib import Path

vault = Path("Eduvia Notes")
all_notes = {}
total_files = 0
for p in vault.rglob("*.md"):
    total_files += 1
    rel = p.relative_to(vault).as_posix()
    all_notes[rel.lower()] = rel
    all_notes[rel.lower() + ".md"] = rel
    all_notes[p.stem.lower()] = rel

print(f"Total notes found in vault: {total_files}")

link_pattern = re.compile(r"\[\[([^\]]+)\]\]")
broken = []
total_links = 0

for p in sorted(vault.rglob("*.md")):
    content = p.read_text(encoding="utf-8", errors="ignore")
    for m in link_pattern.finditer(content):
        total_links += 1
        raw_link = m.group(1)
        # strip alias
        target = raw_link.split("|")[0].strip()
        # strip heading
        target = target.split("#")[0].strip()
        if not target:
            continue  # same page heading link

        # normalize
        clean_target = target
        if clean_target.endswith(".md"):
            clean_target = clean_target[:-3]
        clean_target = clean_target.strip()
        target_lower = clean_target.lower()
        target_stem = Path(clean_target).stem.lower()

        # check if in all_notes
        matched = False
        if target_lower in all_notes or (target_lower + ".md") in all_notes:
            matched = True
        elif target_stem in all_notes:
            matched = True

        if not matched:
            broken.append((p.relative_to(vault).as_posix(), raw_link, clean_target))

print(f"Total wikilinks scanned: {total_links}")
print(f"Broken links count: {len(broken)}")
for src, raw, clean in broken:
    print(f"  IN: {src} -> LINK: [[{raw}]] (Clean Target: {clean})")
