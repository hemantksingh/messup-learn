# Phase 3 rewrite brief (shared by every rewrite agent)

Repo: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn (git). Today is 2026-09-16. Do NOT commit. Edit only the file(s) your assignment names.

## What this wiki is

The owner's words: "A reference for foundational knowledge at the fundamental level, not a copy of content available elsewhere at the source. A repository of knowledge gained by understanding the basics, in language without fancy words that I can understand clearly and rederive concepts from or refer back to." Agents will also read it, so every claim must be true and opinion must be visibly separated from fact.

Read first, in this order: `audit/wiki-plan.md` (purpose, design rules, page contract), the row for your page in `audit/file-triage.md`, the findings for your page in the `audit/details/` file named in your assignment (paths there are pre-migration; `audit/phase1-moves.md` maps old to new), then the current page in full, then the related pages your assignment lists (read-only, for cross-links and to avoid duplication).

## How to rewrite

1. **Start from the question the page answers**, stated in your assignment. The first paragraph answers it in plain words. Then the derivation. Then details. Do not start from the old text and patch it.
2. **This is the owner's notebook, not a textbook.** Keep the owner's own sentences, examples and analogies wherever they are correct (the bank-account example, the sudoku example, the worked subnet arithmetic, the boxing-coach analogy, and so on). When you add explanation, write it the way you would explain it to yourself, not the way a reference manual would. No encyclopedic tone, no "In this section we will", no lists of products for their own sake.
3. **Rederive, don't recite.** Where the concept allows, show why it is true from something simpler (why a hash cannot give confidentiality; why partitions force a choice between C and A; why the ephemeral port limit is per client not per server). End with a short `## How to rederive this` section (3 to 6 bullets) where it fits: the reasoning path someone could follow to reconstruct the page from memory.
4. **Correct by construction.** Every WRONG and STALE finding in the audit must be absent from the result. Where a fact depends on a version or date and that changes the concept (TLS 1.3 removed RSA key transport; Kubernetes 1.24 removed dockershim; INP replaced FID in March 2024), state it. Otherwise leave version numbers, quotas, prices and CLI flags out; link the source instead.
5. **Name sources.** Borrowed ideas get an inline mention ("Kleppmann calls this...") and a `## Sources` section at the end (books, RFCs, talks, papers). Verbatim pasted passages must not survive; either quote with attribution or rewrite.
6. **Mark the owner's stance** with a blockquote starting `> Own view:` for opinions and personal heuristics. Everything else is derived or sourced.
7. **Structure.** Exactly one H1, equal to the filename without `.md`. Sections start at H2. No frontmatter (Phase 5 adds it). Every code fence has a language. Keep existing image embeds where the picture still fits the corrected text, with descriptive alt text (never the filename); do not add new images; if an old image contradicts the text, remove the embed and say in your report which diagram Phase 5 should draw. Relative links to other pages use the current lowercase paths, URL-encoded spaces (`../networking/TLS%20Certificates.md`).
8. **Style.** Short sentences. No em-dashes or en-dashes; use a comma, colon or full stop. No marketing adjectives. British spelling as the owner uses it (behaviour, organisation). No employer or personal data.
9. **Length.** Your assignment gives a target. Do not pad to reach it and do not exceed it by more than a third. Cutting the old text is expected: about a third of most pages is catalogue or paste.
10. **Verify** with WebSearch/WebFetch only when you are unsure of a high-severity fact you are about to assert. Do not add facts you cannot stand behind; leave them out.

## Report

Write to the scratchpad path your assignment gives and return the same content: (a) the question the page now answers, (b) what was kept from the original (owner's examples and passages), (c) what was dropped and why, (d) what was added and the source for each non-obvious claim, (e) diagrams Phase 5 should draw or redraw for this page, (f) open questions for the owner.
