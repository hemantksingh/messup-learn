# Blog post candidates: review and outlines

Written 2026-09-16 from the approved plan. The blog is the Jekyll site in `../hemantksingh.github.io`; drafts live in its `_drafts/` folder (see Workflow). Includes a review of the one draft already there.

## Context

The messup-learn repo is being curated into a wiki of fundamentals in the owner's own words (see `audit/wiki-plan.md`). The owner also wants to publish some of those learnings as blog posts on a separate static-site repo, and named `Tools/Web Frameworks.md`, `Tools/Testing.md` and the `People/` folder as candidates. They asked for a review with pushback.

This plan does three things: sets the rule for what makes a wiki page versus a blog post, ranks the candidates (including two the owner did not name and three named ones I advise against), and gives each viable post a thesis, outline and the list of fixes it needs before it can be published. Scope is assess and outline only; the owner writes the posts.

## The rule: wiki page vs blog post

A **wiki page** answers "how does X work" and is timeless, referenceable, and in plain words. A **blog post** makes an argument or tells a story from experience, has a date and a point of view, and links to the wiki page as its reference. Every post below is a derivative of a corrected wiki page, never of the current raw note. Reasons:

1. Errors that are tolerable in private notes are embarrassing in public. All named candidates carry factual errors (listed per post).
2. Publishing raises the bar on attribution. Several People files paraphrase Carnegie, Fisher and Ury, Coyle, Sinek, Pink, Voss and Center for Creative Leadership course material without naming them. In a private note that is fine. On a blog it reads as claiming their frameworks as yours.
3. A post needs a thesis. Summaries of other people's books do not have one.

## Assessment of the named candidates

### `Tools/Testing.md`: yes, strongest candidate

Own voice, own argument, own experience ("I have been part of teams where..."). The central idea is genuinely useful and not the standard framing: stop asking whether a test is a unit or integration test and ask whether it does I/O. The report-generator example (SQL is the fragile part, so integration-test it) is the kind of concrete judgement readers want.

Fixes before publishing (line numbers in the current file):
- L30 says BDD "isn't about team collaboration". Dan North, cited at L3, defines BDD around the collaboration that produces shared examples. Rephrase: not about tools, is about behaviour and the conversations that describe it.
- L53-58 attributes the "no filesystem, no database" rules to Kent Beck. Beck's point is isolation between tests; the I/O rules are Michael Feathers (2005). The "no I/O" definition is yours. Say so.
- L112 says JMeter cannot integrate with CI. JMeter runs headless from `.jmx` files and has long-standing CI integrations. Keep the point that code-first tools (Locust, k6) are easier to review.
- L113 `npm benchmark` is not a command and the link is to a Go templating repo. Remove.
- L62-68 Karma, PhantomJS, IE and Jasmine-for-Angular are all dead. Either cut the tooling section (recommended for a post) or refresh to Vitest/Jest and Playwright.
- L79-81 chakram and apickli are unmaintained. Cut.
- L85-119 the performance section is AWS Lambda specific and reads like a checklist, not an argument. Cut from this post. Possibly a second, smaller post later ("Quantify the business cost before you tune a Lambda") if the owner has a real story to attach.
- Spelling: invovles, gaurantee, behavours, inseperable, "There could cases".

Proposed post: **"Is it a unit test? Wrong question. Does it do I/O?"** Outline: (1) what tests are for, confidence not defect-counting; (2) TDD does not give you good design for free, I/O separation does; (3) test behaviour, not classes, with the mirroring-versus-behaviour diagram redrawn as your own; (4) when to skip the separation and integration-test the whole thing, with the report-generator example; (5) the one question to ask. Roughly 1,200 words. Wiki reference: Practice / Testing Strategy.

### `Tools/Web Frameworks.md`: half yes

Lines 5-60 are a real argument: pick SSR, CSR or SSG per page, with an e-commerce site worked through (home, listings, cart, about), and then what micro-frontends do to that choice (each fragment fetches its own data, so SSR gets slow and duplicated; CSR and SSG fit better). That is a post. Lines 75-179 are a survey of jQuery, Angular, React, Next.js, Node and ASP.NET that exists in every framework's docs and carries four factual errors. Do not publish that half.

Fixes before publishing the first half:
- L12 says CSR is bad for screen readers because HTML "may not be fully generated". Screen readers read the live DOM. The real CSR accessibility risk is focus management and route-change announcements. Rewrite.
- L17 Gatsby is in maintenance; use Astro or Eleventy as the SSG example.
- L21-30 the hybrid recipe is good. Add one sentence on where the decision is made in practice (per route in Next.js or Astro) without turning it into a framework tutorial.
- Add the missing counterpoint: SSR is not free either (server cost, cache invalidation, time to first byte). The current text is one-sided in favour of SSR.
- Errors in the half you are not publishing, for the wiki fix later: L101 Angular described as AngularJS MVC; L109 JSX embeds markup in JavaScript, not the reverse; L138 "static (SSR)" should be SSG; L141 Next.js has no native PWA support; L158-160 Blazor hosting models are not Razor Pages modes.

Proposed post: **"Pick the rendering mode per page, not per site (and what micro-frontends do to that)"**. Outline: (1) three modes in one paragraph each, no framework names; (2) the e-commerce walkthrough as a table (page, mode, why); (3) the micro-frontend section largely as written; (4) closing rule: rendering mode is a per-route decision driven by freshness, personalisation and indexing. Roughly 1,000 words. Wiki reference: Web and APIs / Rendering Patterns.

### `People/Capabilites.md`: one post hidden inside it

The Architect section (L16-41) opens with a real question, "what does an architect offer self-empowered agile teams?", and answers it in your own words: de-risk delivery, look inward and outward, from player to coach, work in the open. That is a post. The Engineering Leadership and Software Engineer profiles are competency lists, not arguments. The interviewing half (L89-121) is not for publishing.

Fixes: L45-51 is pasted verbatim from `DevOps/Overview.md` and paraphrases Donovan Brown's DevOps definition without credit; not needed for this post. L111 is a verbatim ThoughtWorks sentence; not needed. "player to coach" also appears in Leadership.md L25; use it once.

Proposed post: **"What is an architect for, when the team is supposed to be self-organising?"** Outline: (1) the tension, product owner sees the customer, who sees the engineer; (2) five things the role actually does, each with one concrete example from your experience; (3) what it must not do, be the bottleneck or make drastic decisions for the team; (4) how you would measure whether it is working. Roughly 900 words. Wiki reference: Practice / Roles and Hiring.

### `People/Influence.md`: yes, if you name the sources openly

Structure and examples are yours (the delivery-date "No", the outage-driven NFR argument, "get curious not furious"). The techniques are Carnegie (bait the hook, Ford quote), Fisher and Ury (objective criteria, interests over positions), Voss (labels and mirrors), IDEO ("how might we"). None is named in the file. A post that says "here is what I took from these four sources and how I apply it in engineering conversations" is honest, useful and has a thesis. A post that presents the techniques as yours is not.

Fixes: add a Sources block naming all four; L20 "get a yes" conflicts with Voss's own advice to aim for "that's right" rather than "yes", pick one; L24 Ford quote is via Carnegie and slightly misquoted; fold in the three sections of `Negotiation.md` that duplicate this file, then that file has no separate purpose.

Proposed post: **"Influencing without authority: what I use from four books, in engineering meetings"**. Roughly 1,200 words. Wiki reference: Practice / Influence and Negotiation.

### `People/Leadership.md`: not as a conversion. Maybe one fresh post

Pushback. This is course notes plus a synthesis of five authors, with the worst attribution record in the repo: Schein's name and book title wrong (L7), DLOQ given five dimensions when it has seven and two of the five do not exist (L17-22), SBI written as SIB (L81), William James's line implied to be Dewey's (L79), a Pink paraphrase in quotation marks (L87), a truncated sentence (L7). Converting it would mean publishing other people's frameworks, some wrong, under your name.

What is yours here: the Community of Practice reframing (L122-123), the "come to a 0 or 100 percent position with senior stakeholders" and "bounce the question back" moves (L64-67). Those could seed a short, fresh post on **"How I answer senior stakeholders when I don't have the answer yet"**. Write it from scratch, do not convert the file.

### `People/Negotiation.md`: no

An uncited summary of *Getting to Yes* using the book's own headings. Three of its sections already appear in Influence.md. Merge it there and cite the book.

### `People/Self Awareness.md`: no, for a professional site

Pushback. It is a personal spiritual essay (Dandapani, Vedanta, energy and vibration) with a debunked statistic presented as a Microsoft study (L5), a miscounted list of pramanas (L45-51), an apocryphal Tesla quote (L62), and a paragraph pasted twice (L64 and L80). Alongside technical posts it would cost credibility. If the site is explicitly personal and you want it there, that is your call, but rewrite it as clearly personal reflection and cut the statistic and the quotes you cannot source. The only part that connects to the rest of the blog is the tail (L74-92, make your goal a shared goal; profit is oxygen not purpose), which could be a short standalone reflection.

## Review of the existing draft

`../hemantksingh.github.io/_posts/2026-09-01-the-anatomy-of-high-velocity-engineering-teams.markdown` (untracked). It is a conversion of `People/Leadership.md`, the file this review advises against converting, and it shows why.

**What works.** The five-section structure is clear. Section 5 (repeat expectations) and the "over-functioning" framing in section 2 are yours and read well. The checklist at the end is a good device. `description:` in the frontmatter is a good addition the older posts lack.

**What needs fixing before it publishes.**

1. **Borrowed material is presented as yours, and one attribution is wrong.** Section 1 cites "*The Corporate Culture*" by Schein; the book is *The Corporate Culture Survival Guide*, and the quote is truncated (it continues "...of external adaptation and internal integration"). The "30% to 40%" figure is Will Felps's "bad apple" research (Felps, Mitchell and Byington, 2006), popularised in Coyle's *The Culture Code*, which is also where "I messed up" as the leader's most important sentence comes from. "Direction, Alignment and Commitment" is a Center for Creative Leadership model. None is named. The 2020 "Six rules" post names Carroll, Ford and Goldratt for every borrowed line; hold this one to the same standard.
2. **The title makes a claim the body never tests.** "Leadership trumps code" needs at least one story where the technical fix was proposed, the leadership fix was applied instead, and the delivery changed. Section 1 has the setup ("we need to rewrite it in Rust") and no payoff. The "20% technical, 80% people" split is asserted with no source; either drop the numbers or own them as a rule of thumb.
3. **Voice.** Compare with "Six rules for tech leadership" (2020): first person, concrete tools you used (GitOps, ADRs, C4), examples from projects. The draft is in framework voice: "Here is the operational framework", "Summary Checklist for Engineering Leaders", "Vulnerability as a Strategic Asset". Your own examples from Leadership.md, the Community of Practice reframing and the "0 or 100 percent position" move, are absent. Put them in and cut the abstractions.
4. **Overlap with what you already published.** "Six rules" (2020) already covers know your goal, know your team, get the business on board. Sections 2 and 3 of the draft restate parts of it. Either link to it and go deeper on one thing, or reframe the draft as "what I got wrong in the six rules, five years on".
5. **The closing paragraph changes register.** A consulting call to action ("I advise scale-up founders, CTOs, and investors...") is fine if the site's purpose has shifted, but no other post has one and the tagline is personal. Decide deliberately.
6. **It will publish on the next push.** It sits in `_posts` with a date in the past. Jekyll treats that as live. Move it to `_drafts/` (no date prefix needed there) until it is ready; `jekyll serve --drafts` previews it.

**Recommendation.** Do not publish as is. Either rework it around one story with sources named, or shelve it and write the smaller fresh piece suggested above ("How I answer senior stakeholders when I don't have the answer yet"), which is entirely your material.

## Existing posts the new ones should link to

- **"Are mocks worth it?" (2015)** is the direct ancestor of the Testing post. Ten years on, the position has moved from "mock only at architectural boundaries" to "ask whether the test does I/O". Open the new post with that link; it shows the thinking is yours and has a history.
- **"Six rules for tech leadership" (2020)** already covers "know your goal", which is the tail of Self Awareness.md. The optional "goal as a shared goal" piece proposed below is therefore already published; drop it.
- **"Services, microservices and bounded context" (2015)** overlaps the Service Orientation candidate. Read it before writing so the new post extends rather than repeats it.

## Two candidates you did not name

- **`Distributed Systems/Service Orientation.md`** is already an opinion essay in your voice: when and why to distribute, capability mapping, isolation versus coordination. It needs Fowler's First Law of Distributed Object Design attributed (L33) and the capability-equals-bounded-context claim softened (L23). Otherwise it is closer to a finished post than anything in People/. Thesis: **"Don't distribute. And if you must, distribute along business capabilities."**
- **`Distributed Systems/Consistency Models.md`**, after its rewrite. The audit found the core definitions wrong (strict consistency equated with linearizability, CAP inverted at L65, read-your-writes stated backwards). Once rewritten, a post that rederives linearizability, serializability and strict serializability from first principles in plain words is exactly the kind of thing the wiki is for and is rarely done well in public. Thesis: **"Serializability, linearizability and the word 'strict': rederived without the jargon."** Do not write this until the wiki page is fixed.

## Recommended order

1. Testing (fixes are small, voice is already right).
2. Rendering patterns per page.
3. What is an architect for.
4. Service Orientation.
5. Influence, with sources named.
6. Consistency models, after the wiki rewrite.
7. Optional short piece: answering senior stakeholders when you do not have the answer yet. (The "goal as a shared goal" idea is already covered by the 2020 "Six rules" post.)

Not converting: Leadership as-is, Negotiation, Self Awareness as-is, the framework survey half of Web Frameworks, the interviewing half of Capabilites.

## Workflow

The blog is the Jekyll site at `../hemantksingh.github.io` (GitHub Pages, `github-pages` gem, `jekyll-seo-tag`, served locally with `make`). Drafts live there, not in this repo.

- **Fix the wiki page first.** The fixes above are a subset of `audit/file-triage.md`. The post is written from the corrected page.
- **Draft in `_drafts/`**, not `_posts/`. Jekyll publishes anything in `_posts/` with a past date on the next push; `_drafts/` is only rendered with `jekyll serve --drafts`. Filename is the slug with no date prefix; on publishing, move it to `_posts/YYYY-MM-DD-slug.markdown`. The Makefile's serve target needs `--drafts` added to preview them.
- **Frontmatter follows the existing posts**: `layout: post`, `title`, `date` (ISO with offset, as the other posts), `author: Hemant Kumar`, `tags` (comma-separated string), `categories: kodekitab`, `comments: true`, `description` (one sentence; `jekyll-seo-tag` uses it). Add `source_page: <relative path in messup-learn>` so the derivation is recorded; Jekyll ignores unknown keys.
- **Dating.** `date` is the day the post goes public, not the wiki page's last commit. Three reasons: the Writing page, the home page and `feed.xml` all sort and display by `date`, so a post dated 2024 would appear below the 2026 posts and RSS readers would never surface it; the wiki commit date is not when the thinking happened either (Testing.md was last touched in July 2026 for wording, but its argument dates from 2022); and every existing post is dated within days of its commit, so the site has never been backdated. To show the idea is older than the post, say so in the first paragraph ("I first wrote this down in 2022 after...") and, for later revisions, use `modified_time`, which the site already uses on two posts.
- **Link both ways.** Each post ends with a one-line reference to its wiki page. Each wiki page with a published post lists the URL in its `posts:` frontmatter field.
- **Diagrams.** Reuse the page's `.drawio.svg`; copy it to `assets/` in the blog repo and embed via `{{ site.url }}/assets/<name>.svg`, matching how the site references images. Nothing raster.
- **Publish.** Move the file from `_drafts/` to `_posts/` with the publication date in the filename and frontmatter, commit, push. Record the URL in the wiki page.

## Verification

- Every published post has a `source_page` that exists and has `status: current` in its frontmatter.
- Every factual fix listed under its post is present in the wiki page (grep for the old wording returns nothing).
- Every quotation or borrowed technique in a post names its source in the text.
- `audit/tools/linkcheck.sh` passes on the post files.
- A reader who has never seen the repo can read each post standalone; the wiki link is a reference, not a dependency.
