Title: QuakeImpact
Date: 2026-09-10 00:00
Authors: me
Summary: A public-information site on what a major earthquake does to the Lower Mainland
Template: project_detail
save_as: projects/quakeimpact.html
Technologies:nextjs,react,typescript,tailwindcss,netlify
website: https://quakeimpact.ca
Images:projects/quakeimpact/home.png,projects/quakeimpact/after.png,projects/quakeimpact/water.png,projects/quakeimpact/highways.png

### Why I built it

I live in downtown Vancouver, and I am the chef d'îlot for the French community here: the volunteer the French consulate's emergency plan names as the local point of contact if something serious happens in this part of the city.

Preparing for that role meant reading what the province, the region and the utilities have published about a major earthquake. What they describe is slower than what most of us picture: not a minute of shaking followed by a quick recovery, but weeks to months of disruption to water, power, fuel, transportation and communications. Almost none of it is secret. It sits in filings, plans and assessments that nobody outside the field has a reason to open.

QuakeImpact is a small personal project that collects it in one place: what happens to the systems a household depends on, how long each one is out, how widely, and what it is waiting on. It is not published by the consulate, a municipality or any agency.

### What it is

The site walks a reader through a major earthquake in the order they would live it: the shaking, the weeks that follow, getting around, and what to prepare. Every factual claim links to its published source, whether a regulator's filing, a provincial plan, an engineering assessment or a peer-reviewed paper. Impacts on each essential system are expressed as low, medium or high bands, each paired with a one-sentence mechanism and a citation, rather than invented figures. Where no assessment has been published, the site says so.

### How it was built

The site was built with **Claude Code** and **Codex**, working through several distinct stages rather than asking a model to write pages directly:

- **Collect and compile.** Research files, one subject per file, gather what published sources say, each finding tied to a source in a register of several hundred documents.
- **Validate.** Every research file carries a review status recording whether I have checked it against its sources. A claim reaches the site only if the research backs it with a source; assumptions are logged as open research questions instead of being written up as facts.
- **Draft.** Page copy is written from the validated research through a style guide grounded in risk-communication research, which sets the tone, sentence rules and word list.
- **Review.** Drafts are reviewed against the sources and the style guide before being ported into the site, and an automated audit checks the rendered pages on phone and desktop, in light and dark mode.

Keeping these stages separate is what keeps the content consistent and rigorous across dozens of pages written over many sessions.

### Tech stack

The site is a **Next.js** App Router project written in **TypeScript** and **React**, exported as fully static HTML and hosted on **Netlify**. Styling uses **Tailwind CSS** v4 with design tokens defined in CSS. All page content lives in typed modules, and maps and charts are drawn from small open datasets vendored into the repository, so the site has no runtime dependency on external services. Accessibility was a requirement from the start: WCAG AA contrast, no meaning carried by colour alone, and full keyboard navigation.

### Key features

- Thirteen essential systems, each with its own impact band, mechanism and sources
- Inline citation popovers and a full source list
- Vector maps and charts built from open data
- Static export with no runtime dependencies
