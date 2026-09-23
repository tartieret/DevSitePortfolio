Title: QuakeImpact
Date: 2026-09-10 00:00
Authors: me
Summary: A public-information site on what a major earthquake does to the Lower Mainland
Template: project_detail
save_as: projects/quakeimpact.html
Technologies:nextjs,react,typescript,tailwindcss,netlify
website: https://quakeimpact.ca
Images:projects/quakeimpact/home.png,projects/quakeimpact/after.png,projects/quakeimpact/water.png,projects/quakeimpact/highways.png

### What it is

QuakeImpact is a small side project: a public-information website about what a major earthquake would do to the Lower Mainland of British Columbia. Most people picture a minute of violent shaking followed by a recovery that arrives from outside. The published planning documents describe something different: weeks to months of disruption to water, power, fuel, transportation and communications, with outside help slow to arrive because the whole coast needs it at once.

The site walks a reader through that sequence in the order they would live it: the shaking, the weeks that follow, getting around, and what to prepare. It compares two scenarios side by side wherever they differ, a Cascadia M9 megathrust earthquake and a shallow M7 crustal earthquake under the Strait of Georgia.

### How it is built

The content is a synthesis of published work rather than new analysis. Every claim links to a source kept in a research register of several hundred documents, including provincial and municipal emergency plans, utility filings, engineering studies and accounts of past earthquakes such as Christchurch 2011. Impacts on each essential system are expressed as low, medium or high bands per scenario, each paired with a one-sentence mechanism and a citation, instead of invented figures.

Maps and charts are drawn from small datasets vendored into the repository, so the site has no runtime dependency on external services. Accessibility was treated as a requirement from the start: WCAG AA contrast, no meaning carried by colour alone, keyboard navigation, and support for phone widths and dark mode.

### Tech stack

The site is a **Next.js** App Router project written in **TypeScript** and **React**, exported as fully static HTML and hosted on **Netlify**. Styling uses **Tailwind CSS** v4 with design tokens defined in CSS. All page content lives in typed modules, so adding a new system or scenario is a single data entry that then appears on every page where it belongs.

### Key features

- Two earthquake scenarios compared side by side
- Thirteen essential systems, each with its own impact band, mechanism and sources
- Inline citation popovers and a full source list
- Vector maps and charts built from vendored open data
- Static export with no runtime dependencies
