# Phase 4 brief: trim and split (shared by every Phase 4 agent)

Repo: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn (git). Today is 2026-09-16. Do NOT commit. Edit only the files your assignment names, plus inbound links as described in rule 8.

## What this wiki is

The owner's words: "A reference for foundational knowledge at the fundamental level, not a copy of content available elsewhere at the source ... in language without fancy words that I can understand clearly and rederive concepts from." And on style: "the language needs to be w/o AI slop, text is brief and simple aligned with my style."

Read first: `audit/wiki-plan.md` (purpose, design rules, page contract), your page's rows in `audit/file-triage.md` and in the `audit/details/` file your assignment names (paths there are pre-migration; `audit/phase1-moves.md` maps old to new), the current page in full, and `practice/Testing Strategy.md` for the owner's voice.

## The job

A TRIM keeps the fundamental and cuts the catalogue, vendor text, pasted passages and product detail around it. A SPLIT separates two topics into two pages, each answering one question. In both cases the surviving text is the owner's where it is correct; you add only what a fix or a join needs.

## Rules

1. **Length budget: 3,000 words of body prose is the hard ceiling for any page; your assignment gives a lower target.** Count prose only: exclude code fences and table rows. Tables of requirements, contracts, schemas and data are read by lookup and are not counted. If a page would still be over budget, split it or move the overflow to an appendix page named in your assignment. Never fix length with denser prose.
2. **Owner's notebook, not a textbook.** Keep the owner's sentences, examples and analogies where correct. No encyclopedic tone, no "In this section", no lists of products for their own sake. One or two product names per concept, as examples, is fine.
3. **Brief and plain.** Short sentences, one idea each. Cut connective filler ("In practice", "It is worth noting", "Importantly", "In essence", "Note that", "Essentially"), rhetorical questions, restating summaries, stacked hedges, padding adjectives ("robust", "crucial", "seamless"). British spelling. No em-dashes or en-dashes.
4. **Correct by construction.** Every WRONG, STALE and INCONSISTENT finding against the page must be absent from the result. Where a version or date changes the concept, state it; otherwise leave versions, quotas and prices out and link the source.
5. **Sources.** Pasted passages either become a short attributed quotation or are rewritten. Each page ends with a `## Sources` section. Borrowed frameworks are named inline once.
6. **Own view.** A `> Own view:` block may contain only sentences the owner wrote (check `git show HEAD:"<path>"`). Do not invent stances; state such points neutrally.
7. **Structure.** Exactly one H1 equal to the filename without `.md`. Sections start at H2. No frontmatter. Every code fence has a language. Keep existing image embeds only where the picture still fits, with descriptive alt text; remove embeds that no longer fit and list them in your report. A closing `## How to rederive this` of 3 to 5 one-line bullets where it fits.
8. **Link integrity is your responsibility when you split, rename or move sections.** Before finishing, run `grep -rn "<old filename or anchor>" fundamentals cloud practice` and update every inbound link and anchor to the new location. Use current lowercase paths with `%20` for spaces. Report every link you changed.
9. **Verify** with WebSearch/WebFetch only when unsure of a high-severity fact you are about to assert. Otherwise leave it out.

## Report

Write to the scratchpad path your assignment gives and return the same content: (a) the question each resulting page answers, (b) before and after prose word counts per page, (c) what was cut and why (by category), (d) what was moved where, (e) inbound links changed, (f) diagrams Phase 5 should draw or tables it should build, (g) open questions for the owner.
