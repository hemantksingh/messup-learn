# Phase 3 report: Web Performance

File rewritten: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/web and apis/Web Performance.md (not committed). Final length 1068 words by `wc -w` (the count includes URLs and markup). Tightened after the owner's mid-task feedback: short sentences, no connective filler, no `> Own view:` text, rederive section cut to three bullets. One H1 "Web Performance", sections at H2, no dashes, British spelling, no frontmatter, no images (the page had none). Relative links resolve to HTTP.md, HTTP%20Caching.md and Rendering%20Patterns.md in the same folder.

## (a) Question the page now answers

What do the web performance metrics actually measure, which ones matter, and what moves them. The opening paragraph gives the answer: three user experiences (content is here, I can act on it, it is stable) are measured by LCP, INP and CLS; everything else is a floor under them (TTFB), a lab stand-in (TBT) or a legacy event that measured the document rather than the user.

## (b) Kept from the original

- Faster pages reduce bounce rate and help search ranking, now grounded in the 2021 page experience signal rather than the 2010 announcement.
- The owner's URL-structure points: keyword dilution in long URLs, page importance falling with depth, and reusability across redesigns plus print-friendliness (the last two folded into one line). Given the lead-in "Deep, long URL paths have three costs" and stated neutrally.
- The lab versus real-world distinction the old PSI paragraph hinted at, expanded into the lab vs field section.
- The tool set: Lighthouse, PageSpeed Insights, WebPageTest, with CrUX added.
- The metric list (TTFB, start render as FCP, load time, TTI, TBT, LCP, CLS), each redefined.

## (c) Dropped and why

- H1 "Search Engine Optimization": replaced with the filename.
- Retired PDF SEO starter guide link: replaced by the HTML SEO Starter Guide.
- 2010 "2 seconds or less" load-time target and the 2010 site-speed ranking post: `load` is a legacy event, not a user metric; the ranking basis is Core Web Vitals since 2021.
- "Top-performing sites render LCP in about 1,220 ms": Lighthouse's score-100 reference point; replaced by the CWV 2.5 s p75 threshold.
- TTFB "does not impact the overall user experience significantly": wrong, since FCP and LCP cannot be lower than TTFB; the page now states the floor relationship.
- The wrong TBT definition ("sum of all time periods between FCP and TTI") and the wrong TTI definition (time after async downloads finish).
- Pasted WebPageTest glossary text, the kissmetrics link, and the `utm_source` parameters on the Lighthouse link.
- Lighthouse weighting percentages and log-normal scoring detail: version-specific; linked instead.
- The "load time includes" five-step list: compressed into the `load` versus `DOMContentLoaded` explanation.
- Fourth URL bullet (advertising) merged into the reusability bullet.

## (d) Added, with sources

- Core Web Vitals thresholds at p75: LCP 2.5 s, INP 200 ms, CLS 0.1; INP replaced FID in March 2024. Source: web.dev/articles/vitals and the INP article.
- INP definition (all interactions, roughly the worst); CLS definition (largest burst of unexpected shifts, scored by viewport fraction and distance). Source: web.dev INP and CLS articles.
- TTFB 0.8 s threshold and the floor argument (nothing paints before the first byte). Source: web.dev TTFB article.
- TBT: sum of the portion beyond 50 ms of each long task between FCP and TTI, with a 300 ms to 250 ms worked example. Source: web.dev TBT article, Lighthouse scoring guide.
- TTI definition (first 5 s quiet window with no long tasks and at most two in-flight requests; TTI is the end of the last long task before it) and its removal from the Lighthouse score in version 10, 2023. Source: Lighthouse documentation and Lighthouse 10 release notes.
- `DOMContentLoaded` fires after parsing and deferred scripts; `load` after sub-resources. Source: HTML living standard / MDN.
- Lab vs field: one synthetic run on a simulated device with a cold cache and no interaction, versus a real-user distribution at p75; why they disagree. Source: web.dev "Lab and field data differences".
- Page experience signal uses Core Web Vitals since 2021, as one signal among many. Source: Google Search Central, "Understanding page experience".
- Google indexes client-rendered content after a deferred rendering step. Source: Google Search Central, JavaScript SEO basics (linked inline in the SEO section).
- WebPageTest is now a Catchpoint product.
- Five levers linking HTTP.md (HTTP/2 multiplexing, HTTP/3 head-of-line blocking), HTTP Caching.md and Rendering Patterns.md, plus compression and main-thread JavaScript.
- `## How to rederive this` (3 bullets) and `## Sources` (4 entries).

## (e) Diagrams for Phase 5

The page had no images and none were added. One diagram would help: a navigation timeline with TTFB, FCP and LCP marked along the top, a main-thread lane below with long tasks and the slices beyond 50 ms shaded (TBT), and an input arrow landing during a long task with the wait to the next paint marked as INP. Suggested file: `images/web-performance-timeline.drawio.svg`.

## (f) Open questions for the owner

1. Group 7 of the overlaps audit recommended a separate SEO page; the assignment kept SEO as one short section here. Split it if it grows beyond crawlability and URL structure.
2. The three URL-structure points are stated as fact but are unsourced heuristics. Add a source or soften the wording if you want them read as opinion.
3. HTTP.md still carries the "sprites and concatenation hurt under HTTP/2" performance content. This page links to it rather than repeating it; confirm that split.
4. To stay under the word ceiling the page omits the CLS rule that shifts within 500 ms of user input are excluded, and the fact that TBT has the largest Lighthouse weight. Both are in the linked sources; say if either should come back.
