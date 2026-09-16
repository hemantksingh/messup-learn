# How to use this repository

This is one person's knowledge base of engineering fundamentals, written in their own words. It is not documentation for any product.

- Start at [README.md](README.md), which lists every page with a one-line summary.
- Trust pages with `status: current` in their frontmatter. Treat `needs-review` as possibly stale and `draft` as incomplete. `last_reviewed` says when a human last checked the page.
- Pages with `kind: opinion`, and paragraphs starting `> Own view:`, are the owner's positions. Cite them as opinion, not as fact.
- Product facts (quotas, prices, CLI flags, version numbers) are deliberately kept out. Follow the page's `sources` or the vendor's documentation for those. Where a version changes the concept (TLS 1.3 removed RSA key transport; Kubernetes 1.24 removed dockershim) the page says so.
- Titles equal filenames. Search titles first. Folders are topics: computing, networking, web and apis, data, messaging, security, platform (containers, Kubernetes, delivery, observability), cloud (aws, azure: provider mental models only) and practice (testing, leadership, influence).
- Most pages end with `## How to rederive this` (the reasoning path) and `## Sources`; a few short pages have no Sources section yet. Tables of requirements, schemas and data are for lookup and are not counted against the page's length budget.
- Diagrams are `images/*.drawio.svg`: a rendered SVG with the draw.io source embedded, so they can be read as pictures and edited in draw.io.
- `audit/` holds the September 2026 audit that produced this structure. It is history, not reference material. Paths in `audit/details/` are pre-migration.
