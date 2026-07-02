# Documentation voice

This file covers the *voice* of prose under `docs/` — how to frame a
page so a reader meets the idea before its API surface. It complements
the repository-root `AGENTS.md`, which already governs doctest rules,
commit standards, changelog conventions, and MyST roles. When the two
overlap, the root file wins; this one only answers the question it
leaves open: how should the prose sound?

## Who you are writing for

The default reader runs a pytest suite that talks to PostgreSQL and
wants repeated setup — seeded databases, downloaded files, doc
examples — cached instead of rebuilt on every run. They are fluent in
pytest — fixtures, markers, `conftest.py`, `addopts` — and know their
own database, but you cannot assume they know pgsnap's internals: the
`Snapshot` strategy classes, the difference between SQL emission, a
dump/restore, and a template copy, or the doctest-docutils collector
that runs the examples in these very docs.

A second, smaller reader works *on* pgsnap or against its lower
layers: writing a custom `Snapshot` subclass, extending the collector
in `pytest_pgsnap`, or contributing. Serve them too, but mark their
material opt-in ("for the rarer cases", "advanced") so the default
reader knows they can stop. Never make the common case pay a
comprehension tax for the advanced one.

## Voice

- **Second person, present tense, active.** "You snapshot the seeded
  database", not "A snapshot is created". Address the reader who is
  doing the thing.
- **Concept before API surface.** Open by saying what the strategy or
  fixture *is* and what it does for the reader. The class name, the
  plugin flag, the parameters — those are the last details they need,
  not the first. A page that opens with a class signature has buried
  the idea under its mechanics.
- **Say when they can stop.** Lead with the default and the
  reassurance: most readers never reach for this, the defaults work,
  the advanced parts are optional. Let a skimmer leave after one
  paragraph.
- **Grant permission, don't demand attention.** "Reach for this
  when…", "for the rarer cases" — tell readers they're in the right
  place without implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  wiring most suites need → the one option a few will tune → picking
  a different snapshot strategy → writing your own `Snapshot`
  subclass. Each step is for a smaller audience than the last.
- **Lean on the strategy ladder.** The reader thinks `Snapshot` →
  `FileSnapshot` / `DBSnapshot` → the PostgreSQL strategies (SQL
  emission, dump/restore, template copy); reinforce that ladder when
  you explain what to cache and how. It is the mental model the whole
  toolkit hangs on.
- **Name the trade-off.** If a strategy costs something — a template
  copy needs a parallel database, a dump stores and restores the
  whole database, SQL emission is incremental but fragile — say so,
  and say what it buys ("slower to restore, but the whole state is
  guaranteed"). State it; don't sell it.
- **Frame by concept, not by mechanism.** Don't headline a feature by
  its plugin flag or class name in prose; that names the
  implementation surface, which is the reader's last concern. Name
  the concept. The mechanics vocabulary — a parameter table, the
  `--doctest-docutils-modules` flag — belongs in a reference table or
  the API docs, and only there.

## Examples that run

Prose examples under `docs/` are doctests: `testpaths` includes
`docs`, and the plugin this repo ships collects every `>>>` block in
an `.rst` or `.md` file, so `uv run py.test` runs each one.
Lead with a small, runnable example early rather than after
paragraphs of prose.

- There is no `conftest.py` wiring `doctest_namespace` fixtures, so
  every example builds what it needs — keep examples self-contained
  and deterministic.
- Fence a `>>>` session as a ```` ```python ```` block; use a
  ```` ```console ```` block for shell commands at a `$` prompt.
  `ELLIPSIS` and `NORMALIZE_WHITESPACE` are already on via
  `doctest_optionflags`, so variable output can be elided with `...`.
- Each fenced block runs as its own doctest with a fresh namespace —
  a later block cannot reuse a name an earlier block defined. Repeat
  the setup or merge the blocks; never assume shared state.
- Keep doctests short; complex examples belong in dedicated tests
  under `tests/`, per the root `AGENTS.md`.

## What stays precise

Warm the framing, never the facts. Strategy trade-off notes, value
tables, exact error strings, and class or function cross-references
carry meaning in their exact form — leave them alone. The friendly
voice belongs in the sentences *around* a precise block, introducing
it, not inside it paraphrasing it into vagueness.

## Cross-references

Point the advanced reader at the deep-dive rather than inlining it,
and put the link where their interest peaks — on the phrase that made
them curious ("write your own strategy") — not as a standalone
footnote the eye skips. Use the MyST roles listed in the root
`AGENTS.md` (`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}`,
`{ref}`, `{doc}`). A `{ref}` must match its target's anchor exactly —
anchors mix underscore and hyphen forms across pages
(`pytest_plugin`, `developmental-releases`). A docs build — `make
html` from `docs/` — catches a broken cross-reference; the doctests
do not, so build the docs before you commit.

Link the first prose mention of any symbol that has a useful
destination on that page. This includes Python objects, pgsnap APIs,
pytest concepts with intersphinx targets, topic pages, and external
tools or projects. Use the most specific target available: `{class}`,
`{meth}`, `{func}`, `{mod}`, `{exc}`, or `{attr}` for API objects;
`{ref}` or `{doc}` for documentation pages and section anchors; and a
Markdown link or reference link for external projects. After the
first linked mention on a page, later mentions can stay plain unless
the distance or context makes another link useful.

Do not rely on a later reference section to satisfy the first-mention
rule. If the first occurrence would be a heading or introductory
sentence, link that occurrence or retitle the heading so the first
prose mention can carry the link. Leave command examples, code
blocks, and literal configuration values as code; link the
surrounding prose instead.

## Before you commit

- Does the page open with what the feature *is*, or with how to call
  it?
- Can a reader who needs only the common case stop after the first
  paragraph?
- Is anything framed by its plugin flag or class name that should be
  named by concept instead?
- Are the advanced and lower-level parts clearly marked opt-in?
- Did `uv run py.test` pass — every docs doctest executes, and each
  block stands on its own?
- Did `make html` from `docs/` stay clean — no new warning, no broken
  cross-reference?
