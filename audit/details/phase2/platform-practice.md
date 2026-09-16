# Phase 2 report: platform and practice pages (2026-09-16)

Seven files edited, nothing committed, no other file touched. Every replacement was an exact-match string edit asserted to occur once. Checks run after editing: exactly one H1 per file (the extra `# ` hits in Kubernetes Security are shell comments inside `sh` fences), every code fence tagged, no leading blank line, every relative link resolves, no em-dash introduced (the two in changed lines are pre-existing on Testing Strategy line 38 or inside the verbatim ThoughtWorks quotation). Web-verified: Carnegie's Ford wording, the Amazon principles URL (`https://www.amazon.jobs/en/principles`), kube-hunter's README notice ("not under active development anymore", recommends Trivy), and that the SRE Workbook chapter linked on the DevOps page contains the quoted sentence (quoted exactly, "one tool for the SREs").

`git status` also shows around 26 other modified files under `cloud/` and `fundamentals/` from parallel phase-2 agents. I did not touch them.

## fundamentals/platform/Kubernetes Security.md

- was: leading blank line, H1 "Securing the API Server" → now: H1 "Kubernetes Security", "Securing the API Server" demoted to H2
- was: "Client Certificates - most commonly used way to authenticate ... e.g. in managed cloud service like AKS" → now: certificates are used by cluster components and are the bootstrap and break-glass path for admins; humans on AKS, EKS, GKE normally use OIDC or cloud IAM tokens; CN carries the user, O carries groups
- was: "Authentication Tokens - HTTP Authorization header" and "Basic HTTP - uses static password files" → now: bearer-token sources listed (static token file, bootstrap tokens, service account tokens, OIDC ID tokens, webhook); separate sentence that `--basic-auth-file` was removed in 1.19. The existing OIDC paragraph kept as the OIDC detail.
- was: CSR API described with no version → now: `certificates.k8s.io/v1` (since 1.19), every request needs a `signerName`, e.g. `kubernetes.io/kube-apiserver-client`
- was: "Running a pod in kunernetes without a specified service account runs it with the default service account." → now: typo fixed; since 1.24 tokens are bound projected tokens, long-lived token Secrets are not auto-created; `automountServiceAccountToken: false` is the hardening default
- was: "All tenants share the master control plane ... API priority and fairness by using the `--max-requests-inflight` flag" → now: "control plane"; APF (GA 1.29) via `FlowSchema` and `PriorityLevelConfiguration`; the two inflight flags only set the total budget
- was: bare `https://sysdig.com/products/kubernetes-security/` bullet → now: one sentence on CIS Kubernetes Benchmark, Pod Security Standards and admission policy (Kyverno, Gatekeeper, built-in `ValidatingAdmissionPolicy`)
- was: bare kube-hunter link → now: notes it is no longer under active development and its README points to Trivy, which also runs the CIS checks kube-bench covers
- was: no pod security content → now: new H2 "Pod security" (4 bullets, 6 lines): PSP removed in 1.25, Pod Security Admission with privileged/baseline/restricted, default-deny NetworkPolicy, Secrets encryption at rest or KMS, audit logging
- was: `![default-cluster-roles.png]` → now: alt text "The four default ClusterRoles (cluster-admin, admin, edit, view) and what each can do within a namespace"

Skipped: DUPLICATE row for `kubectl config view --raw` (the cheat sheet was merged into fundamentals/platform/Kubernetes.md and that file no longer contains the command, so there is nothing to link to). Trivial typos "kubelete", "CFSSSL" left (Low, not on lines with a finding).

## fundamentals/platform/DevOps and Delivery.md

- was: H1 "DevOps" → now: "DevOps and Delivery"
- was: "DevOps capabilities" definition plus three role bullets duplicating Roles and Hiring → now: definition sentence kept (it is the DevOps definition) plus one sentence linking to `../../practice/Roles%20and%20Hiring.md` for the role profile; the three bullets removed here and kept on the Roles page (see interpretation note below)
- was: four DORA metrics with "mean time to restore (MTTR)" → now: five keys since 2021 (lead time for changes, deployment frequency, failed deployment recovery time, change failure rate, reliability), with a note that MTTR was renamed failed deployment recovery time in the 2023 report
- was: "RTO is time taken to recover from a disaster ... therefore RTO will normally be higher than MTTR" → now: RTO is an agreed maximum time to restore set in advance; MTTR is a measured mean over real incidents
- was: "Graphana" (twice) → now: "Grafana"
- was: unattributed SRE-book sentences → now: blockquote attributed to the SRE Workbook chapter already linked at the top of the page; the owner's closing sentence kept outside the quote
- was: "OS installation abd patches ... *Terraform and Cloudformation*" → now: "and"; tools list is Terraform, OpenTofu, CloudFormation, AWS CDK, Bicep, Pulumi
- was: "*Chef, Ansible, Puppet and SaltStack* are popular, open-source examples" → now: "popular examples"; Ansible is open source; Chef, Puppet and SaltStack are source-available or ship as commercial builds
- was: three pasted Octopus Deploy paragraphs including the IIS/MSMQ example and a "Blue Green" list that described an in-place deployment with a maintenance window → now: two neutral sentences on configuration management (desired state, converge) versus deployment orchestration (ordered steps through environments) and one short paragraph of real blue/green steps (two identical environments, deploy to the idle one, switch traffic at the load balancer or DNS, keep the old one because switching back is the rollback)

The Phase 1 "Separate deployment from release" section was left as is.

## practice/Testing Strategy.md

- was: H1 "Testing approach" → now: "Testing Strategy"
- was: "The role of dedicated testers might diminish" → now: "North argues that the role of dedicated testers might diminish"
- was: "It isn't about tools like `Cucumber` or team collaboration but shifting perspective" → now: not about tools; it is about collaboration (the conversations that produce shared examples) and describing observable behaviour
- was: "According to the definition by Kent Beck a unit test ... shared resources like file systems and databases are not touched" → now: Beck's point is isolation between tests; the no-database/network/filesystem rules are Michael Feathers (2005); the "no I/O" definition is labelled "My own working definition"
- was: Jasmine/Mocha, spec-runner.html, Karma, Chrome/Firefox/IE/PhantomJS, "Jasmine is more commonly used in angular projects" → now: Vitest and Jest with jsdom or happy-dom, Mocha and Jasmine as older alternatives, Playwright for real browsers. No claim about Angular's current default (unverified).
- was: "GUI based tools like JMeter ... CI/CD integration isn't well supported" → now: JMeter plans are `.jmx` files run headless in CI (`jmeter -n -t plan.jmx`); code-first tools (Locust, k6) are still easier to review in a pull request
- was: "`npm benchmark` can be used for local performance testing" + templ link → now: removed
- was: chakram and apickli links → now: removed together with their lead-in sentence ("For testing REST APIs with outside-in tests ...") which would otherwise dangle
- was: first-person "I have been part of teams" paragraph → now: same paragraph with a leading "> Own view:" blockquote marker, only that paragraph
- was: invovles, gaurantee, behavours, inseperable, "There could  cases", "the your" → now: fixed
- was: `![Testing behaviour]` → now: alt text describing both halves (one-to-one mirroring tests versus a single PlaceOrderTest through behaviour)

Skipped: moving the performance-testing section (CLASSIFY, later phase, as instructed). "1GB RAM initially recommended" OPINION row (Medium, not in the assigned list). Existing em-dashes on lines not otherwise wrong left in place.

## practice/Leadership.md

- was: "In *The Corporate Culture*, Schien defines culture as" → now: "In *The Corporate Culture Survival Guide*, Edgar Schein defines culture as"
- was: truncated "by encouraging specific behaviors that" → now: "by encouraging specific behaviours." (completed by truncation, nothing invented)
- was: "scientific experiments have shown jerks diminish a team's performance by 30-40%" → now: attributed to Will Felps's bad-apple experiments (2006) as reported in Coyle's *The Culture Code*
- was: no attribution for the safety/vulnerability/purpose framing → now: one sentence on the Culture line attributing it to Coyle
- was: "Dimensions of Learning Organizations Questionnaire (DLOQ) ... five dimensions" with two invented names and generated-sounding descriptions → now: "Dimensions of the Learning Organization Questionnaire (DLOQ, Marsick and Watkins)" with the seven real dimensions, no descriptions
- was: "Direction Alignment and Commitment (DAC)" → now: "Direction, Alignment and Commitment (DAC), a Center for Creative Leadership (CCL) model"
- was: "where your are may use your influence" → now: "where you use your influence"
- was: self-awareness subsection with no link → now: one sentence linking `Self%20Awareness.md` and stating the two pages use the word differently (inner practice there, how you are perceived here)
- was: "Closed positions like crossed arms represent defensiveness" etc. → now: "are commonly read as"
- was: William James's line placed as if Dewey's; Carnegie passage unattributed → now: James named for "the deepest principle in human nature is the craving to be appreciated"; the whole passage attributed to Carnegie once in the lead-in sentence
- was: "SIB (Situation Behavior and Impact)" → now: "SBI (Situation-Behavior-Impact) technique from CCL"
- was: limbic-brain claim stated as fact → now: "Simon Sinek (*Start With Why*) argues ..." with "Treat this as a simplification, not settled neuroscience"
- was: Pink paraphrase in quotation marks → now: "Daniel Pink (*Drive*) argues that engagement comes from **autonomy, mastery and purpose**."
- was: two carrot-and-stick sentences (conditional vs blanket) → now: the Motivation one harmonised to Pink's conditional version
- was: "[labels and mirrors]" link unattributed → now: "Chris Voss's [labels and mirrors]"
- was: Community of Practice example inside Carnegie material → now: prefixed "Own example:" (also fixed "is a something")
- was: bare tweet link in Resources → now: removed (contents could not be verified to describe)
- was: no Sources section → now: "## Sources" (Coyle, Carnegie, Pink, Sinek, Voss, CCL for DAC and SBI only) added before the existing "## Resources"

Skipped (OPINION rows not in the assigned list): the "why/what/how/now what" communication-course notes, the scripted conversation openers ("Hey Brad"), the Schwab anecdote line, the Dweck/Pink effort-praise line, the "100% sure" vs Influence tension, the Motivation/Engage DUPLICATE (merging sections is restructuring).

## practice/Influence and Negotiation.md

- was: H1 "Influencing others" → now: "Influence and Negotiation"
- was: "**Get a yes**" → now: "**Aim for \"that's right\"**" with one sentence that Voss warns against chasing a "yes"
- was: "If there is one secret of success ... as well as your own - Henry Ford" → now: exact Carnegie wording ("If there is any one secret of success ... as well as from your own") attributed "Henry Ford, as quoted in Carnegie"
- was: "provide psychological safety ... showing your vulnerabilities" unattributed → now: "(Amy Edmondson's term)" and "Coyle calls this the vulnerability loop"
- was: "questions like 'How might we...?'" → now: "IDEO's question 'How might we...?'"

Deviation: one bullet (Edmondson: psychological safety; Coyle: vulnerability loop) appended to the Phase 1 "Sources" section so the two new attributions have a source entry; nothing else in that section changed.

Skipped: removing the "summarise their position", "Invent", and "Use objective criteria" sections. The appended Getting to Yes summary paraphrases them; they are not word-for-word duplicates, so left as instructed. The "Its not about you, its about the mission" quote (OPINION, not listed). Phase 1 "Negotiation" and "Sources" sections left in place.

## practice/Roles and Hiring.md

- was: H1 "Capabilities" → now: "Roles and Hiring"
- was: "Someone who can work within organizations to bring **people, processes and products** together..." (Donovan Brown wording duplicated from the DevOps page) → now: one sentence linking to `../fundamentals/platform/DevOps%20and%20Delivery.md` for the definition; the three role bullets kept here
- was: "(i.e. reorganising them ... adopt DevOps culture by having" with no closing parenthesis → now: parenthesis closed after "DevOps culture"
- was: "IAAS, PAAS or FAAS" → now: "IaaS, PaaS or FaaS"
- was: "* TDD - demonstrate understanding of" → now: "* Testing (see [Testing Strategy](Testing%20Strategy.md)) - demonstrate understanding of"; sub-bullets kept as the interview checklist
- was: REST APIs bullet with no link → now: links `../fundamentals/web%20and%20apis/REST.md`
- was: "Active lsitening", "stratgy", "busniess" → now: fixed
- was: "[Amazon leadership questions](yoreoyster blog) is a good place to start" → now: Amazon's own Leadership Principles page (`https://www.amazon.jobs/en/principles`) as primary, blog kept as secondary
- was: ThoughtWorks sentence pasted unmarked → now: in quotation marks, "As the ThoughtWorks article puts it:"
- was: labels and mirrors unattributed → now: "Chris Voss's [labels and mirrors]"

Skipped: Donovan Brown attribution (not in the assigned list; the wording now lives only on the DevOps page). OPINION framing rows for the role profiles (5-14, 18-20). "Player to coach" DUPLICATE with Leadership (Medium, but a one-phrase overlap; removing would strip the Architect profile).

## practice/Self Awareness.md

- was: no preface → now: "Personal reflections, drawing mainly on Dandapani and Swami Parthasarathy; not engineering guidance" directly under the H1
- was: "Ramana Maharishi" → now: "Ramana Maharshi"
- was: goldfish/Microsoft eight-second sentence plus the dependent "How do you expect to solve the world's problems when your average attention span is eight seconds?" → now: both deleted (the second made no sense without the first)
- was: Dandapani cited only at the concentration paragraph → now: cited at first use ("Dandapani teaches that there are a few things..."); later mention de-linked to avoid a double link
- was: italicised awareness/energy quote unattributed → now: "- Dandapani, following his teacher Gurudeva Sivaya Subramuniyaswami"
- was: "sates", "at most", "rationale", "pe part", "can can" → now: "states", "utmost", "rationalise", "be part", "can"
- was: "research has also found people who are introspective are more likely to ruminate" → now: "Tasha Eurich's research (*Insight*, 2017) has also found..."
- was: "According to Indian epistemology and ... *Vedanta*, knowledge can be acquired through four pramanas" followed by five bullets → now: Nyaya lists four (the bullets), Advaita Vedanta six (adding postulation and non-apprehension); the "experience" bullet removed from the pramana list
- was: orphan list (education, experience, intuition, experience without learning) → now: given the lead-in "Four ways people learn:"
- was: "In *Vedanta* knowledge is acquired by 20% reading and 80% thinking" → now: "A modern teacher's rule of thumb, often attributed to Swami Parthasarathy, is that..."
- was: "Nikola Tesla said ..." → now: "A line attributed to Nikola Tesla, with no verified primary source: ..."
- was: "Life is a manifestation..." paragraph twice → now: the second (whole paragraph under "Make your goal a shared goal"; every sentence in it repeated an earlier line) deleted, first kept
- was: "If you want to go fast travel alone..." unattributed → now: "(often called an African proverb, origin unknown)"
- was: closing profit paragraphs plain → now: the three closing paragraphs (from "Does this mean you give up everything..." to the end) wrapped in one blockquote starting "> Own view:"; the inner quote line stays as an italic line inside it

Skipped (OPINION, not listed): "If you work just for yourself..." quote, the "Intrinsic motivation ... Commitment is intrinsic motivation in action" CCL-register sentences, the three will-power practices attribution, the "Believe that you have the ability to create whatever you want" line. CLASSIFY (move to a Personal folder) skipped as instructed.

## Interpretation note: the DevOps / Roles and Hiring duplicate

The instructions asked both pages to replace the shared paragraph with one sentence plus a link to the other. Done literally on both sides the content would have vanished and each page would point at an empty target. Resolution: the DevOps definition sentence stays on the DevOps page; the three role-profile bullets stay on Roles and Hiring (with the parenthesis closed and IaaS/PaaS/FaaS fixed, which only makes sense if they survive); each page carries one sentence and a relative link to the other.
