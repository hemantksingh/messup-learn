#!/usr/bin/env python3
"""Phase 5 wiring (2026-09-16), kept so the index and checks can be rerun. Run from repo root.

Most useful later: `index` (regenerate README.md from page frontmatter) and `check`.
Manifest-driven steps (links, diagrams, front) expect the yaml files in $WIKI_MANIFESTS.

Steps (each idempotent):
  h1        align every page's H1 to its filename (README.md hubs keep their H1)
  links     apply scratchpad/phase5-links.yaml (replace / remove dead URLs)
  diagrams  export scratchpad/diagrams/*.drawio -> images/<name>.drawio.svg and embed per manifests
  rasters   delete raster images that nothing references
  front     inject frontmatter from scratchpad/phase5-frontmatter-*.yaml
  index     generate README.md from frontmatter
  agents    write AGENTS.md
  check     structural checks
Usage: python3 phase5_wire.py step [step ...]
"""
import os, re, subprocess, sys, urllib.parse, datetime, shutil
from pathlib import Path
try:
    import yaml
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--user", "pyyaml"], check=False)
    import yaml

S = Path(os.environ.get("WIKI_MANIFESTS", "audit/details/phase5"))  # where the yaml manifests and diagrams/*.drawio live
DRAWIO = "/Applications/draw.io.app/Contents/MacOS/draw.io"
AREAS = ["computing", "networking", "web and apis", "data", "messaging", "security", "platform", "cloud", "practice"]
TODAY = datetime.date.today().isoformat()

def pages():
    out = []
    for a in AREAS:
        out += sorted(str(p) for p in Path(a).rglob("*.md"))
    return out

def read(p): return Path(p).read_text(encoding="utf-8")
def write(p, s): Path(p).write_text(s, encoding="utf-8")

def split_front(s):
    if s.startswith("---\n"):
        end = s.find("\n---\n", 4)
        if end != -1:
            return s[4:end], s[end+5:]
    return None, s

def first_h1_index(lines):
    fence = False
    for i, l in enumerate(lines):
        if l.startswith("```"): fence = not fence; continue
        if not fence and l.startswith("# "): return i
    return -1

# ---------------------------------------------------------------- h1
def step_h1():
    n = 0
    for p in pages():
        fm, body = split_front(read(p))
        lines = body.split("\n")
        i = first_h1_index(lines)
        base = Path(p).stem
        if base == "README":
            continue
        if i == -1:
            lines.insert(0, f"# {base}"); lines.insert(1, "")
        elif lines[i] != f"# {base}":
            lines[i] = f"# {base}"
        else:
            continue
        body2 = "\n".join(lines)
        write(p, (f"---\n{fm}\n---\n" if fm is not None else "") + body2)
        n += 1
    print(f"h1: {n} pages aligned")

# ---------------------------------------------------------------- links
def step_links():
    f = S / "phase5-links.yaml"
    if not f.exists(): print("links: no manifest"); return
    items = yaml.safe_load(read(f)) or []
    applied = skipped = 0
    for it in items:
        p = it["file"]; old = it["old"].strip(); act = it.get("action")
        if not Path(p).exists(): skipped += 1; print("  missing file", p); continue
        s = read(p)
        if old not in s: skipped += 1; print("  not found:", p, old[:70]); continue
        if act == "replace" and it.get("new"):
            s = s.replace(old, it["new"].strip())
        elif act == "remove":
            # turn [text](old) into text; bare <old> or old into nothing
            s = re.sub(r"\[([^\]]*)\]\(" + re.escape(old) + r"\)", r"\1", s)
            s = s.replace(f"<{old}>", "").replace(old, "")
        else:
            skipped += 1; continue
        write(p, s); applied += 1
    print(f"links: {applied} applied, {skipped} skipped")

# ---------------------------------------------------------------- diagrams
def rel(frm, to): return urllib.parse.quote(os.path.relpath(to, os.path.dirname(frm)).replace(os.sep, "/"))

def step_diagrams():
    manifests = sorted((S / "diagrams").glob("manifest-*.yaml"))
    entries = []
    for m in manifests: entries += (yaml.safe_load(read(m)) or [])
    Path("images").mkdir(exist_ok=True)
    ok = 0
    for e in entries:
        src = S / "diagrams" / e["file"]
        if not src.exists(): print("  missing source", src.name); continue
        name = src.stem + ".drawio.svg"
        out = Path("images") / name
        r = subprocess.run([DRAWIO, "-x", "-f", "svg", "--embed-diagram", "-o", str(out), str(src)], capture_output=True, text=True)
        if not out.exists(): print("  export failed", src.name, r.stderr[-200:]); continue
        # embed
        page = e["page"]
        if not Path(page).exists(): print("  missing page", page); continue
        s = read(page)
        alt = e["alt"].replace("]", ")").replace("\n", " ").strip()
        title = e.get("title", "").replace('"', "'")
        embed = f'![{alt}]({rel(page, str(out))}' + (f' "{title}"' if title else "") + ")"
        if name in s:
            ok += 1; continue  # already embedded
        replaced = False
        reps = e.get("replaces")
        if reps:
            for old in [x.strip() for x in str(reps).split(",") if x.strip()]:
                pat = re.compile(r"^!\[[^\]]*\]\([^)]*" + re.escape(old) + r"[^)]*\)[ \t]*$", re.M)
                sub = "" if replaced else embed  # second and later olds: remove, do not embed twice
                if pat.search(s):
                    s = pat.sub(sub, s, count=1); replaced = True
                else:
                    pat2 = re.compile(r'<img src="[^"]*' + re.escape(old) + r'"[^>]*>')
                    if pat2.search(s): s = pat2.sub(sub, s, count=1); replaced = True
        if not replaced:
            anchor = e.get("after_heading") or e.get("after_line_containing")
            lines = s.split("\n"); idx = -1
            if anchor:
                for i, l in enumerate(lines):
                    if l.strip() == anchor.strip() or (anchor.strip() in l and not e.get("after_heading")):
                        idx = i; break
            if idx == -1 and e.get("after_heading"):
                # try matching heading text only
                ht = re.sub(r"^#+\s*", "", anchor).strip().lower()
                for i, l in enumerate(lines):
                    if re.match(r"^#+\s", l) and re.sub(r"^#+\s*", "", l).strip().lower() == ht: idx = i; break
            if idx == -1:
                print("  anchor not found for", src.name, "in", page, "->", anchor); continue
            # insert after the first paragraph following the anchor (or right after a non-heading line)
            j = idx + 1
            if e.get("after_heading"):
                while j < len(lines) and lines[j].strip() == "": j += 1
                while j < len(lines) and lines[j].strip() != "" and not lines[j].startswith("#"): j += 1
            lines[j:j] = ["", embed, ""]
            s = "\n".join(lines)
        s = re.sub(r"\n{3,}", "\n\n", s)
        write(page, s); ok += 1
    print(f"diagrams: {ok}/{len(entries)} exported and embedded")

# ---------------------------------------------------------------- rasters
def step_rasters():
    removed = 0
    for img in sorted(Path("images").iterdir()):
        if img.suffix.lower() == ".svg": continue
        used = any(img.name in read(p) for p in pages())
        if not used:
            subprocess.run(["git", "rm", "-q", str(img)], check=False)
            if img.exists(): img.unlink()
            removed += 1; print("  removed", img.name)
    # drawio sources
    for d in Path(".").rglob("*.drawio"):
        if str(d).startswith(("audit", "images")) : continue
        subprocess.run(["git", "rm", "-q", str(d)], check=False); print("  removed source", d)
    print(f"rasters: {removed} removed")

# ---------------------------------------------------------------- front
def yq(s):
    s = str(s).replace('"', "'").strip()
    return '"' + s + '"'

def step_front():
    meta = {}
    for f in sorted(S.glob("phase5-frontmatter-*.yaml")):
        for e in (yaml.safe_load(read(f)) or []): meta[e["path"]] = e
    n = 0
    for p in pages():
        e = meta.get(p)
        base = Path(p).stem
        title = e["title"] if e else ("AWS" if base == "README" else base)
        summary = (e or {}).get("summary", "").strip()
        kind = (e or {}).get("kind", "index" if base == "README" else "concept")
        status = (e or {}).get("status", "current")
        tags = (e or {}).get("tags", [])
        sources = (e or {}).get("sources", [])
        fm_lines = ["---", f"title: {yq(title)}", f"summary: {yq(summary)}", f"kind: {kind}", f"status: {status}", f"last_reviewed: {TODAY}"]
        fm_lines.append("sources:" + ("" if sources else " []"))
        for src in sources: fm_lines.append(f"  - {yq(src)}")
        fm_lines.append("tags: [" + ", ".join(str(t) for t in tags) + "]")
        fm_lines.append("---")
        old_fm, body = split_front(read(p))
        write(p, "\n".join(fm_lines) + "\n" + body.lstrip("\n"))
        n += 1
        if not e: print("  no manifest entry, defaults used:", p)
    print(f"front: {n} pages")

# ---------------------------------------------------------------- index
LABEL = {"computing": "Computing", "networking": "Networking", "web and apis": "Web and APIs", "data": "Data", "messaging": "Messaging",
         "security": "Security", "platform": "Platform", "cloud": "Cloud", "practice": "Practice"}

def step_index():
    out = ["# Mess-up and learn", "",
           "Learnings from some successful and some failed experiments, kept as a wiki of fundamentals in my own words. Each page answers one question in plain language and says where the idea came from. Product detail lives at the source; this is the reasoning I want to be able to rederive.", "",
           "Opinion is marked `> Own view:`. Every page carries frontmatter with a one-line summary, tags, sources and a `last_reviewed` date. Agents: read [AGENTS.md](AGENTS.md) first.", ""]
    for a in AREAS:
        ps = sorted(str(p) for p in Path(a).rglob("*.md"))
        if not ps: continue
        out.append(f"## {LABEL[a]}"); out.append("")
        # hubs first
        ps.sort(key=lambda p: (0 if Path(p).name == "README.md" else 1, p.lower()))
        for p in ps:
            fm, _ = split_front(read(p))
            m = yaml.safe_load(fm) if fm else {}
            title = m.get("title", Path(p).stem)
            summ = m.get("summary", "")
            kind = m.get("kind", "")
            link = urllib.parse.quote(p)
            sub = ""
            if a == "cloud":
                sub = {"aws": "AWS", "azure": "Azure"}.get(Path(p).parts[1], Path(p).parts[1].capitalize()) + ": " if Path(p).name != "README.md" else ""
            tag = " *(opinion)*" if kind == "opinion" else ""
            out.append(f"- [{sub}{title}]({link}){tag}: {summ}")
        out.append("")
    out.append("## About this repository"); out.append("")
    out.append("The September 2026 audit that produced this structure is under [audit/](audit/README.md). It is history, not reference material.")
    out.append("")
    write("README.md", "\n".join(out))
    print("index: README.md written")

# ---------------------------------------------------------------- agents
AGENTS = """# How to use this repository

This is one person's knowledge base of engineering fundamentals, written in their own words. It is not documentation for any product.

- Start at [README.md](README.md), which lists every page with a one-line summary.
- Trust pages with `status: current` in their frontmatter. Treat `needs-review` as possibly stale and `draft` as incomplete. `last_reviewed` says when a human last checked the page.
- Pages with `kind: opinion`, and paragraphs starting `> Own view:`, are the owner's positions. Cite them as opinion, not as fact.
- Product facts (quotas, prices, CLI flags, version numbers) are deliberately kept out. Follow the page's `sources` or the vendor's documentation for those. Where a version changes the concept (TLS 1.3 removed RSA key transport; Kubernetes 1.24 removed dockershim) the page says so.
- Titles equal filenames. Search titles first. Folders are topics: computing, networking, web and apis, data, messaging, security, platform (containers, Kubernetes, delivery, observability), cloud (aws, azure: provider mental models only) and practice (testing, leadership, influence).
- Each page ends with `## How to rederive this` (the reasoning path) and `## Sources`. Tables of requirements, schemas and data are for lookup and are not counted against the page's length budget.
- Diagrams are `images/*.drawio.svg`: a rendered SVG with the draw.io source embedded, so they can be read as pictures and edited in draw.io.
- `audit/` holds the September 2026 audit that produced this structure. It is history, not reference material. Paths in `audit/details/` are pre-migration.
"""
def step_agents():
    write("AGENTS.md", AGENTS); print("agents: AGENTS.md written")

# ---------------------------------------------------------------- check
def step_check():
    bad = []
    def heads(p): return {re.sub(r'[^a-z0-9 -]', '', h.lower()).replace(' ', '-') for h in re.findall(r'^#+\s+(.*)$', read(p), re.M)}
    for p in pages() + ["README.md", "AGENTS.md"]:
        s = read(p)
        fm, body = split_front(s)
        lines = body.split("\n")
        # one H1
        fence = False; h1 = 0
        for l in lines:
            if l.startswith("```"): fence = not fence; continue
            if not fence and l.startswith("# "): h1 += 1
        if h1 != 1: bad.append((p, f"{h1} H1s"))
        # bare fences
        fence = False
        for l in lines:
            if l.startswith("```"):
                if not fence and l.strip() == "```": bad.append((p, "bare fence"))
                fence = not fence
        # links
        for m in re.finditer(r'(?:\]\(|<img src=")((?!https?://|mailto:)[^)"\s]+)', s):
            t = urllib.parse.unquote(m.group(1)); anc = None
            if "#" in t: t, anc = t.split("#", 1)
            tgt = p if t == "" else os.path.normpath(os.path.join(os.path.dirname(p), t))
            if not os.path.exists(tgt): bad.append((p, "missing " + m.group(1)))
            elif anc and tgt.endswith(".md") and anc not in heads(tgt): bad.append((p, "anchor " + m.group(1)))
        # frontmatter
        if p not in ("README.md", "AGENTS.md"):
            if fm is None: bad.append((p, "no frontmatter"))
            else:
                m = yaml.safe_load(fm)
                if m.get("title") != (Path(p).stem if Path(p).stem != "README" else m.get("title")): bad.append((p, "title != filename"))
                if not m.get("summary"): bad.append((p, "empty summary"))
        # alt text = filename?
        for m in re.finditer(r'!\[([^\]]*)\]\(([^)\s]+)', s):
            if m.group(1).strip().lower() in (Path(urllib.parse.unquote(m.group(2))).name.lower(), ""): bad.append((p, "alt is filename: " + m.group(2)))
    print(f"check: {len(bad)} problems"); [print("  ", b) for b in bad]
    # orphans
    for img in sorted(Path("images").iterdir()):
        if not any(img.name in read(p) for p in pages()): print("   orphan image:", img.name)

STEPS = {"h1": step_h1, "links": step_links, "diagrams": step_diagrams, "rasters": step_rasters, "front": step_front, "index": step_index, "agents": step_agents, "check": step_check}
if __name__ == "__main__":
    for st in sys.argv[1:]: STEPS[st]()
