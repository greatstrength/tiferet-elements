# Domain Vision Statement — Tiferet Elements

**Status:** Draft · **Domain:** `tiferet-elements` · **Code:** `tiferet_elements/` · **Branch:** `main`

## The bet: build on the supported door, not the one propped open

Streamlit is the fastest way most teams have to put a working, data-driven application in front of real users. Its trade-off is the interface: you get a fixed set of plain controls, and anything richer — a proper button and form system, publication-quality charts, an embedded code editor — has to come from somewhere else.

For several years that somewhere else has been a community library, `okld/streamlit-elements`, which brings Material UI, Nivo charts, and the Monaco editor into Streamlit. It works by reaching into a part of Streamlit that Streamlit never promised to keep stable. In May 2024 that part moved, and user interactions stopped being reported back to the application at all ([okld/streamlit-elements#35](https://github.com/okld/streamlit-elements/issues/35)). The issue is still open, with no fix from the maintainer, more than two years later.

What that costs is not theoretical. Teams either freeze their Streamlit version and forgo two years of fixes, or they ship a script that edits the installed library's own source files during every build — a workaround the community wrote itself, then had to rewrite when the next Streamlit release broke it again, and which still does not work for everyone who tries it. Either way, a core piece of the product's interface rests on something nobody maintains.

The same Streamlit release that broke the old approach also shipped a public, supported way for a component to report interactions back to the application. **Tiferet Elements is a bet that the right response is to build on that supported path and maintain it, rather than keep patching around a closed door.**

## What this domain makes real

Tiferet Elements is a small library that lets any Streamlit application present Material UI controls, Nivo charts, and the Monaco code editor, and respond when a user clicks, types, or selects something — using only the interaction path Streamlit publicly supports. Nothing is patched; nothing reaches into another project's internals. The browser-side visuals from the existing ecosystem were never the broken part. The wiring behind them was, and that is what this package owns.

## What we get for it

### Upgrading Streamlit stops being a gamble
Because the connection uses a published, supported entry point, a Streamlit upgrade is an ordinary upgrade. Teams get security fixes and new platform features on the normal schedule instead of choosing between a current runtime and a working interface.

### Failure stops being silent
The old breakage did not raise an error. Buttons simply stopped responding, and the application looked fine while doing nothing. Interactions here are accounted for explicitly: every control that can be interacted with is registered before the screen is shown, and an interaction that arrives with no one listening is a reported error, not a shrug.

### Any Streamlit app can adopt it
This is a general-purpose library, not a Tiferet accessory. It needs a Streamlit application and nothing else — no adoption of a wider framework, no restructuring of an existing app, no all-or-nothing migration. A team can put one richer control on one screen and keep everything else exactly as it is.

### You install only what you use
The Streamlit support is an optional add-on, so installing the package does not drag Streamlit into environments that do not want it.

## The core of the work

Everything the library does follows one path:

> **Describe** the screen you want → **register** who is listening to each part of it → **deliver** each reported interaction to exactly the right listener.

The description and the registry are rebuilt on every pass, so what is on screen and what can respond to it can never drift apart. The listener registry is the heart of it: each interactive part is given an identifier when the screen is described, and one small, generic delivery step routes whatever comes back to the handler that claimed that identifier.

The design commitment is that **describing a screen and keeping the registry are Streamlit-free**. Only a thin, clearly separated edge knows how to mount the result inside Streamlit and receive its reports. Supporting a second host later means writing another edge, not rebuilding the library — and the part most likely to break with an upstream change is also the smallest part to fix.

## What it deliberately does not do

It has no concept of features, views, or pages. That vocabulary — how an application is organized into screens and workflows — belongs to `tiferet-streamlit`, and this package neither defines it nor depends on that package. Nor does it own the application session: it hands back a plain, ready-to-use piece that the host application wires into its own lifecycle, so an app using both packages never has two things competing to run the show.

It is also not a fork or a rescue of `okld/streamlit-elements`, not a general-purpose framework for building Streamlit components, and not a reimplementation of Material UI, Nivo, or Monaco. Its single job is to connect those widgets to a Streamlit application over a supported path, and to keep that connection working.

---

*Companion document:* `docs/core-domain-distillation.md` — the detailed walkthrough of the domain's vocabulary, behaviors, and the relationships between its parts.
