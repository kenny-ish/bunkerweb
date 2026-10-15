from pathlib import Path
import re

CSS = Path("src/ui/app/static/css/pages/logs.css").read_text(encoding="utf-8")
LAYOUT_CSS = Path("src/ui/app/static/css/overrides/layout.css").read_text(encoding="utf-8")

search_match = re.search(r"\.ace_search\s*\{[^}]*z-index:\s*(\d+)", CSS)
sticky_match = re.search(r"\.sticky-card\s*\{[^}]*z-index:\s*(\d+)", LAYOUT_CSS)
assert search_match, "The logs page must set an explicit z-index for the ACE search box"
assert sticky_match, "The shared sticky toolbar must set an explicit z-index"
search_z_index = int(search_match.group(1))
sticky_z_index = int(sticky_match.group(1))
assert search_z_index > sticky_z_index, f"The ACE search box z-index ({search_z_index}) must be above " f"the sticky toolbar z-index ({sticky_z_index})"
print(f"log search z-index ok: {search_z_index} > {sticky_z_index}")
