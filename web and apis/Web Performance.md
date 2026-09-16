---
title: "Web Performance"
summary: "What the Core Web Vitals measure, how lab and field data differ, and which levers move them."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "web.dev, Web Vitals and the metric articles linked from it"
  - "Lighthouse performance scoring (Chrome Developers)"
  - "Google Search Central, page experience"
  - "Chrome UX Report (CrUX)"
tags: [web-performance, core-web-vitals, lcp, inp, cls, seo]
---
# Web Performance

A page is fast when the user sees what they came for quickly, can act on it without waiting, and nothing jumps around. Three metrics, the Core Web Vitals, measure those three things: LCP, INP and CLS. Everything else in a report is a floor under them (TTFB), a lab stand-in for one of them (TBT), or a legacy event that measured the document, not the user.

## Why it matters

Users leave slow pages. Since 2021 Google's page experience signal has used the Core Web Vitals as one ranking input among many. Between comparable pages the faster one wins.

## Lab vs field

A lab tool (Lighthouse, WebPageTest) loads the page once on a simulated device and network with a cold cache. Nobody clicks or scrolls.

Field data (CrUX, or your own real user monitoring, RUM) comes from real visitors on their own devices over the whole visit, reported at the 75th percentile (p75): the value three quarters of visits beat. Google judges every threshold at p75 in the field.

They disagree because the lab is one device and the field is a distribution that slow phones pull upwards; nobody interacts in the lab, so INP cannot be measured there and TBT stands in; nobody scrolls, so late layout shifts never appear; and the lab cache is empty. Diagnose in the lab, judge in the field.

## The three Core Web Vitals

"Good" means the p75 field value is under the threshold.

![A page-load timeline from navigation start with TTFB (first byte of the HTML), FCP (first content painted), LCP (largest image or text block painted) and a later layout shift that counts toward CLS marked left to right. Below it a main-thread lane shows two long tasks with the part of each beyond 50 ms shaded and labelled as counting toward TBT. A tap arrives during the first long task and waits; the time from that input to the next painted frame is labelled INP.](../images/web-performance-timeline.drawio.svg "Web performance metrics on a page load")

**Largest Contentful Paint (LCP), good under 2.5 s.** Time from navigation start until the largest image or text block in the viewport is painted. Moved by server response time, render-blocking CSS and scripts in the head, and the LCP image: large, lazy-loaded, or referenced only from CSS or JavaScript means it starts late.

**Interaction to Next Paint (INP), good under 200 ms.** For every click, tap and key press, the time from input to the next painted frame; INP is roughly the worst of them. It became a Core Web Vital in March 2024, replacing First Input Delay, which measured only the first interaction. Moved by long tasks on the main thread. The browser has one thread for JavaScript, input and painting, so a 300 ms task makes a tap during it wait up to 300 ms.

**Cumulative Layout Shift (CLS), good under 0.1.** A score, not a time. Each unexpected movement of visible content scores by how much of the viewport moved and how far; CLS is the largest burst of shifts in the visit. Moved by images without width and height attributes (no space is reserved, so text jumps) and content injected above existing content (banners, cookie notices).

## Supporting metrics

**Time to First Byte (TTFB), good under 0.8 s.** From the start of navigation to the first byte of the HTML. Not visible by itself, but a floor under everything: nothing paints before the first byte, so FCP and LCP can never be lower than TTFB. Moved by server work, distance to the server (a CDN helps) and redirects.

**First Contentful Paint (FCP).** Time until the browser paints anything from the DOM: text, an image, a non-white canvas.

**Speed Index.** How quickly the visible part of the page fills in, scored from a video of the load.

**Total Blocking Time (TBT).** A long task holds the main thread for more than 50 ms. For each long task between FCP and TTI, take the portion beyond 50 ms and sum; a 300 ms task contributes 250 ms. TBT is the lab proxy for INP.

**Time to Interactive (TTI).** Historical. After FCP, find the first five-second window with no long tasks and at most two requests in flight; TTI is the end of the last long task before it. Lighthouse removed it from the performance score in version 10 (2023).

**`DOMContentLoaded` and `load`.** Legacy browser events. `DOMContentLoaded` fires when the HTML is parsed and deferred scripts have run. `load` fires when the document and its sub-resources (images, stylesheets, frames) have finished. Anything fetched afterwards by script is invisible to both, and on a client-rendered page `load` can fire on a blank screen. That is why "load under 2 seconds" stopped being the target.

## The levers

- **Fewer and smaller bytes.** Compress text (Brotli or gzip), serve images at the displayed size in a modern format, ship only the JavaScript the page uses.
- **Fewer round trips.** HTTP/1.1 serialises requests per connection; HTTP/2 multiplexes them and HTTP/3 removes the remaining head-of-line blocking. See [HTTP](HTTP.md).
- **Caching.** Repeat visitors should not fetch what has not changed. See [HTTP Caching](HTTP%20Caching.md).
- **Rendering mode.** Server-side or static rendering gives the browser something to paint before any JavaScript runs; client-side rendering moves that work onto the main thread. See [Rendering Patterns](Rendering%20Patterns.md).
- **Less main-thread JavaScript.** Break long tasks up and defer what the first paint does not need.

## SEO

A search engine can only index what it can see. Server-rendered and static HTML is indexed on the first pass; client-rendered content is indexed by Google after a [deferred rendering step](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics). Rendering mode is therefore also an SEO choice. The rest is in Google's [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide).

Deep, long URL paths have three costs:

- Keywords in the URL are diluted: the longer the path, the less weight each word carries.
- Pages far from the root are treated as less important than pages near it.
- The URL is harder to reuse: a path that encodes today's navigation breaks at the next redesign, and a long URL is harder to print in a campaign.

## Tools

- **Lighthouse** (Chrome DevTools or CLI): lab audit with a list of fixes.
- **PageSpeed Insights**: Lighthouse on Google's servers, with CrUX field data for the URL beside it.
- **WebPageTest** (now a Catchpoint product): lab tests from chosen locations and devices.
- **CrUX dashboard**: a site's p75 field history over time.

## How to rederive this

- Three user experiences: content is here, I can act, it is stable. LCP, INP, CLS measure them in that order.
- The lab cannot click or scroll, so INP needs the field and TBT stands in.
- Nothing paints before the first byte, so TTFB bounds FCP and LCP.

## Sources

- web.dev, Web Vitals and the metric articles linked from it: https://web.dev/articles/vitals
- Lighthouse performance scoring: https://developer.chrome.com/docs/lighthouse/performance/performance-scoring
- Google Search Central, page experience: https://developers.google.com/search/docs/appearance/page-experience
- Chrome UX Report: https://developer.chrome.com/docs/crux
