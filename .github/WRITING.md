# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, `CHANGES`, commit messages, docstrings, and source comments —
every surface a reader reaches.

For environment setup, the gates, and pull request workflow, see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Voice

Three surfaces, one voice. A docstring says what a caller may rely on; a
`CHANGES` entry says what changed; prose says what happens. All three are
present tense, lead with the thing being described, and stop. Why it was
built that way belongs in the commit message, which is timestamped and
attached to the diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks.
Prefer short declarative sentences, one operational fact each. Do not
explain Python to Python developers; do explain this project's semantics.

Type annotations describe shape. Documentation describes meaning. A
sentence that restates a signature has said nothing.

Use MUST, SHOULD, and MAY only where the normative sense is meant. Say what
actually happens rather than that something is "supported".

| Instead of                       | Prefer                            |
| --------------------------------- | ---------------------------------- |
| "We added…"                       | "`Snapshot` now accepts…"          |
| "New and improved"                | "`DBSnapshot` now…"                |
| "powerful", "seamless"            | state the capability               |
| "easily", "simply", "just"        | omit                               |
| "simple", "obvious", "intuitive"  | omit                                |
| "robust"                          | name the failure that is handled   |
| "comprehensive"                   | name what is covered               |
| "production-ready"                | state the guarantee                |
| "optimized", "blazingly fast"     | give the magnitude                 |
| "various fixes"                   | name the components                |
| "under the hood"                  | omit unless observable             |
| "please note that", "note that"   | state the fact                     |
| "leverage", "utilize"             | "use"                              |
| "delve into"                      | "read", or omit                    |
| "best practices"                  | name the practice                  |
| "in order to"                     | "to"                               |

## Who you are writing for

The default reader runs a pytest suite that talks to PostgreSQL and wants
repeated setup — seeded databases, downloaded files, doc examples — cached
instead of rebuilt on every run. They are fluent in pytest (fixtures,
markers, `conftest.py`, `addopts`) and know their own database, but you
cannot assume they know pgsnap's internals: the `Snapshot` strategy
classes, the difference between SQL emission, a dump/restore, and a
template copy, or the doctest collection that runs the examples in these
docs.

A second, smaller reader works *on* pgsnap or against its lower layers:
writing a `Snapshot` subclass, wiring the pytest integration, or
contributing. Serve them too, but mark their material opt-in — "for the
rarer cases", "advanced" — so the default reader knows they can stop.
Never make the common case pay a comprehension tax for the advanced one.

Rules that follow:

- **Second person, present tense, active.** "You snapshot the seeded
  database", not "A snapshot is created". Address the reader who is doing
  the thing.
- **Concept before API surface.** Open by saying what the strategy or
  class *is* and what it does for the reader. The class name and its
  parameters are the last details they need, not the first. A page that
  opens with a signature has buried the idea under its mechanics.
- **Say when they can stop.** Lead with the default and the reassurance.
  Let a skimmer leave after one paragraph.
- **Grant permission, do not demand attention.** "Reach for this when…"
  tells readers they are in the right place without implying they must
  read on.
- **Progressive disclosure.** Order by how many readers need it: the
  common case, then the one option a few will tune, then the lower-level
  primitive. Each step is for a smaller audience than the last.
- **Lean on the strategy ladder.** The reader thinks `Snapshot` →
  `FileSnapshot` / `DBSnapshot` → the PostgreSQL strategies (SQL emission,
  dump/restore, template copy); reinforce that ladder rather than
  introducing a competing vocabulary.
- **Name the trade-off.** If a strategy costs something — a template copy
  needs a parallel database, a dump stores and restores the whole
  database, SQL emission is incremental but fragile — say so, and say
  what it buys. State it; do not sell it.
- **Frame by concept, not by mechanism.** Do not headline a feature by its
  class name in prose; that names the implementation surface, which is
  the reader's last concern. Name the concept instead. The mechanics
  vocabulary belongs in a reference table or the API docs.

## README

A README is the shortest path from "what is this?" to competent use, not
the project's autobiography.

The first sentence is a contract. It says what abstraction the reader has
been handed, concretely enough to tell this package apart from the
neighbouring one.

Get to a runnable command before anything the reader can skip. A logo, a
mission statement, and three paragraphs of history in front of the install
line all cost the same thing.

State the minimum Python version and meaningful platform constraints in
prose, not only in badges. `requires-python` in `pyproject.toml` is the
authority; the README must agree with it.

Name the distribution and the import separately wherever they differ —
`pytest-pgsnap` installs, `pgsnap` imports. That distinction prevents a
Python-specific class of confusion. Name the executable too, wherever the
project has one.

Examples are executable, not illustrative fiction. Never
`your-command <some-options>`. See
[Documented examples that run](#documented-examples-that-run) for which
blocks are executed and how to write one that qualifies.

Document the semantic model, not the flag list. What a call costs, what it
guarantees, and what state it leaves behind matter more than an
enumeration a docstring or `--help` already gives.

State defaults explicitly — defaults are API. State negative guarantees
where they exist: "does not register a pytest plugin", "no network
access". They establish boundaries faster than any amount of description.

Headings stay conventional and stable, because people deep-link them.
Badges are few and load-bearing.

## Documented examples that run

Examples in this repository are tests, when they are written to run.

**A fence tag is cosmetic. Only a `>>> ` prompt executes.** A block written
as

    ```python
    server = Server()
    ```

is prose that looks like a test. Nothing collects it, nothing runs it, and
it can be wrong for years. The same block written with prompts is a test:

    ```python
    >>> server = Server()
    ```

This is the single most expensive mistake available when editing
documentation, because removing the prompts leaves a green test suite and
a silently deleted test. When editing a file that contains examples, count
the prompts before and after.

**The fence tag is `python`.** Not `pycon`, not bare.

**Where examples run, in this repository.** `[tool.pytest.ini_options]` in
`pyproject.toml` sets:

```toml
addopts = "--tb=short --no-header --showlocals --doctest-modules"
doctest_optionflags = "ELLIPSIS NORMALIZE_WHITESPACE"
testpaths = ["tests", "docs", "src"]
```

- `--doctest-modules` runs `>>> ` examples embedded in docstrings under
  `src/` and `tests/`.
- `.md` and `.rst` files under `docs/` are collected for their `>>> `
  blocks by the `doctest-docutils` pytest plugin, which ships as part of
  the `gp-libs` dev dependency (`pyproject.toml`'s `dev` and `docs`
  groups), not by this package. This package registers no pytest plugin
  of its own — see
  [Documenting fixtures and markers](#documenting-fixtures-and-markers).
- **`README.md` is not in `testpaths`.** A `>>> ` block added there is not
  collected or run, no matter how it is fenced. There are currently no
  `>>> ` blocks in `README.md`; if one is ever added, either add
  `README.md` to `testpaths` and confirm it collects, or do not claim it
  is tested.
- There is no `conftest.py` anywhere in this repository, so no
  `doctest_namespace` fixture adds names to a block's globals. Every
  example must build what it needs; a block cannot assume a name exists
  unless it defines it.
- Each fenced block runs as its own doctest with a fresh namespace — a
  later block cannot reuse a name an earlier block defined. Repeat the
  setup or merge the blocks; never assume shared state.

**`# doctest: +SKIP` is not permitted.** It is a workaround that tests
nothing.

**Do not downgrade a doctest to a non-executed block to make it pass.** A
`.. code-block::` or an unprompted fence does not run. If an example
cannot pass, fix the example or fix the code.

**Option flags.** `ELLIPSIS` and `NORMALIZE_WHITESPACE` are enabled
globally, so `...` elides variable output and whitespace differences do
not fail a comparison. Reach for an inline `# doctest: +FLAG` only for the
block that needs it.

**Docstring examples** use the NumPy `Examples` section:

    Examples
    --------
    >>> from pgsnap.core import FileSnapshot, Snapshot
    >>> issubclass(FileSnapshot, Snapshot)
    True

## Documenting fixtures and markers

`pytest-pgsnap`'s name and its `Framework :: Pytest` classifier declare
pytest-plugin intent, but at this version it registers no pytest entry
point and ships no working fixture or marker. `PytestFixtureCache` and
`SideEffectMark` in `pgsnap.core` are undocumented-behaviour stub classes,
not a public API. **Do not document a fixture or marker as available until
it is wired into pytest** — an entry point, a `@pytest.fixture`
definition, or a `pytest_configure` marker registration — and covered by a
test that exercises it.

When a fixture ships, document:

- **Name and scope.** `function`, `module`, `session`, or `package`, and
  why that scope was chosen if it is not the default.
- **What it yields.** The concrete type, and what it represents — a live
  connection, a filesystem path, a strategy object.
- **Teardown guarantee.** Whether cleanup runs on failure as well as
  success, and what "clean up" means for that fixture — drop a database,
  remove a file, roll back a transaction.

When a marker ships, document its arguments and what registering it
enables or skips.

A fixture or marker's name, scope, or yielded type is public API once it
ships. Renaming it, changing its scope, or changing what it yields is a
breaking change — see [The changelog](#the-changelog).

## The changelog

`CHANGES` is the changelog. It is rendered as the project's changelog page
at `docs/history.md`.

A ledger, not a narrative. It is scanned, and the question a reader is
asking is whether an entry affects them.

**Release entry boilerplate.** Every release header is
`## pytest-pgsnap X.Y.Z (YYYY-MM-DD)`. The file opens with a
`## pytest-pgsnap X.Y.Z (unreleased)` placeholder block fenced by
`<!-- KEEP THIS PLACEHOLDER ... -->` and
`<!-- END PLACEHOLDER ... -->` HTML comments — new entries land
immediately below the END marker, never above it.

**Unreleased entries carry no lead paragraph.** Speaking for a release —
what the version "is", "ships", or "focuses on" — is presumptuous before
its scope is final. Only the person cutting the release writes that lead
paragraph. Never write or edit it from a feature branch, and never ask or
imply that a release should happen.

**Released entries open with a multi-sentence lead paragraph.** Plain
prose, no italic. Open with the version as sentence subject
("*pytest-pgsnap X.Y.Z ships …*") so the lead is self-contained when
excerpted. Two to four sentences on what shipped and who cares —
user-visible takeaways, not internal mechanism. Cross-reference detail
docs with `{ref}` to keep the lead compact.

**Each deliverable is a section, not a bullet.** Inside `### What's new`,
every distinct deliverable gets a `#### Deliverable title (#NN)` heading
naming it in user vocabulary, followed by one to three prose paragraphs.
Do not wrap a paragraph in `- ` — bullets are for enumerable lists, not
paragraph containers.

**The deliverable test.** Before writing an entry, ask: "What's the
deliverable, in user vocabulary?" If that cannot be answered in one
sentence, the entry is not ready. Mechanism belongs in the pull request
description and code comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`,
`### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`,
`### Development`. Dev tooling (helper scripts, internal automation)
lives under `### Development`.

**Breaking changes ship their migration inline**, not a pointer to one:
change, old, new, reason, with concrete inline code (a `# Before` /
`# After` fenced block) where a code change is involved. Give a breaking
change its own subheading at the top of the entry — never bury it
mid-entry. **Renaming, removing, or rescoping a fixture or marker is a
breaking change**, per
[Documenting fixtures and markers](#documenting-fixtures-and-markers).

**Dependency floor bumps** use the form
``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`,
occasionally `### Documentation`) with three or more genuinely small items
use bullets — one line each, never paragraphs. If a bullet swells past two
lines, promote it to a `#### Title (#NN)` heading with prose body.

**Always link autodoc'd APIs.** Any class, method, function, exception, or
attribute with its own rendered page is cited via the matching MyST role —
never with plain backticks. See
[MyST roles and cross-references](#myst-roles-and-cross-references).

**Anti-patterns.**

- Fragile metrics that go stale silently — token ceilings, third-party
  version pins, percent benchmarks, exact byte counts. Describe the
  capability, not the math.
- Private symbols and internal jargon.
- Walls of text dressed up as bullets.
- Breaking changes buried mid-entry instead of given their own subheading.

**Summarization style.** When asked "what changed in the latest version?",
lead with the entry's lead paragraph (paraphrased if needed), followed by
each `####` deliverable heading under `### What's new` with a one-sentence
summary. Cite `(#NN)` only if source links are requested. Do not invent
versions, dates, or numbers not present in `CHANGES`, and do not quote
line numbers or file offsets — those shift as the file evolves.

## Docstrings

The prime directive: never restate the type. The annotation is the source
of truth; the docstring carries what the annotation cannot.

This is documentation debt wearing a docstring:

    def get_path(snapshot: Snapshot) -> Path:
        """Get the snapshot's path.

        Parameters
        ----------
        snapshot : Snapshot
            The snapshot.

        Returns
        -------
        Path
            The path.
        """

Document instead the dimensions the type system cannot encode: mutation,
ownership, ordering, timing, failure, idempotence, concurrency, units and
ranges, boundary behaviour, platform differences, and any security
boundary — what is executed versus what is only read.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. Do not repeat an
introspectable signature.

Ruff (`pydocstyle`, `numpy` convention) is the enforced dialect.

**Classes with fields** — `NamedTuple`, dataclasses — document every field
in an `Attributes` section:

```python
class SnapshotResolution(t.NamedTuple):
    """Outcome of deciding which snapshot a fixture should restore from.

    Attributes
    ----------
    path : pathlib.Path | None
        Snapshot to restore from, or ``None`` on a cache miss.
    """
```

Autodoc renders every field whether or not you describe it, so an
undocumented `NamedTuple` field ships to the API docs as "Alias for field
number 0" and a dataclass field ships bare. Document all of them — a class
with three fields and two documented still ships a stub for the third.

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real
time rediscovering intent, an invariant, a constraint, or a failure mode
the code and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write
this comment, at this length? Those projects state the constraint and
stop. They do not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that
hand-syncs a value the code owns — a count, an offset, a line reference, a
duplicated constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several
facts, in which case split it, or arguing, in which case cut it to the
fact.

Rationale, alternatives weighed, and the story of how the code got here
belong in the commit message: timestamped, attached to the exact diff,
and free to maintain.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, lifetime, and concurrency
  requirements that types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not
  reintroduce the bug.
- A high-level sketch of an algorithm whose local operations do not
  reveal the whole.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- Speculation about future requirements.
- History version control already holds, including commented-out code.
- Ticket and issue numbers. They say nothing to a reader without tracker
  access, and they rot when the tracker moves. Unfinished work goes in
  the tracker, not the source.
- Transient observations — "currently", "for now", "the latest release" —
  that go stale with no nearby edit.

### The upkeep gate in practice

It reaches values that track our own code. It does not reach frozen
external facts.

Bad (Delete):

```python
# There are 12 strategies left to implement for the snapshot taxonomy.
```

Good (Keep):

```python
# CPython < 3.11 has no ExceptionGroup, so this branch stays.
```

### Documentation exception

NumPy-style `Parameters`, `Returns`, and `Attributes` sections, minimal
usage examples, and executable doctests on public API are exempt from the
loss gate — they serve the caller, not the maintainer, and a doctest that
runs is also a test. They are exempt from nothing else. Ceiling: a good
man page entry.

## Terminology and capitalization

Pick the domain noun and keep it. This project calls the unit of work a
**snapshot**; do not call it a cache, a backup, or a checkpoint in the
same breath. Keep the strategy ladder's names exact — `Snapshot`,
`FileSnapshot`, `DBSnapshot`, and the three PostgreSQL strategies — rather
than paraphrasing a class name into a description.

Stable vocabulary is what makes search, deep links, and an agent's
retrieval work at all.

Python and PyPI keep their own capitalisation. Distribution names are
written as they are published.

Do not write counts into prose — how many classes exist, how many tests
there are. They go stale silently and no reader needs them.

## MyST roles and cross-references

Docs are MyST Markdown built with Sphinx. Class references use `{class}`,
methods use `{meth}`, functions use `{func}`, modules use `{mod}`,
exceptions use `{exc}`, attributes use `{attr}`, internal anchors use
`{ref}`, doc-path links use `{doc}`. Plain backticks are correct for code
syntax, environment variables, parameter names, and file paths that are
not doc pages — anything without an autodoc destination.

Link the first prose mention of any symbol that has a useful destination
on that page: Python objects, pgsnap APIs, pytest concepts with
intersphinx targets, topic pages, and external tools. Use the most
specific target available. After the first linked mention on a page,
later mentions can stay plain unless distance or context makes another
link useful. If the first occurrence would be a heading or introductory
sentence, link that occurrence or retitle the heading so the first prose
mention can carry the link. Leave command examples, code blocks, and
literal configuration values as code; link the surrounding prose instead.

A `{ref}` must match its target's anchor exactly — anchors mix underscore
and hyphen forms across pages (`pytest_plugin`, `developmental-releases`).
A docs build (`sphinx-build -b html docs docs/_build/html`) catches a
broken cross-reference; the doctests do not, so build the docs before you
commit a page that adds or moves an anchor.

## Markdown

Prose wraps at 80 columns. Table rows, badge lines, and long links are
exempt, because breaking them harms rendering. A pull request or issue
body does not wrap at all: GitHub renders a single newline as a space in a
file and as a line break in a comment, so a wrapped comment body arrives
as ragged stubs.

GitHub alert blocks — `> [!NOTE]`, `> [!WARNING]` — render as literal text
outside GitHub, so reserve them for at most one load-bearing warning per
document. Write the sentence so it carries the fact on its own, and a
renderer that drops the marker loses nothing.

Do not use a local absolute path or an email address in anything
published.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action. Executed examples are exempt — the test suite runs them,
nobody pastes them.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is
  then one logical command.
- **Explanations go in prose above the block**, never as `#` comments
  inside it.
- **Command menus are per-command blocks with prose lead-ins**, not
  tables.
- **Shell commands use the `console` tag with a `$ ` prefix.** This
  separates interactive commands from scripts and enables prompt-aware
  copy.
- **Split long commands with `\`** — one flag or flag+value pair per
  indented continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing
`(#NN)` pull request reference, and wrap body lines at 72. Separate the
`why:` and `what:` blocks with a blank line.

Routine maintenance commits drop the colon and take a capitalised
description, which is what distinguishes them at a glance in
`git log --oneline`:

```
py(deps[dev]) Bump dev packages
ai(rules[AGENTS]) Judge comments by three gates
```

Everything that changes behaviour keeps the colon.

Common types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **ci**: Workflow and pipeline changes
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (`CLAUDE.md`)
- **ai(claude[command])**: Claude Code command changes

Example:

```
Core(feat[strategy]): Add a Snapshot subclass hook

why: Let a caller register a custom strategy.

what:
- Add a register hook to Snapshot
- Document the extension point
```

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

### Release commits

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow.

A release commit subject is plain and short: `Tag v<version>`. The
detailed why and what go in the body. Do not use the
`Scope(type[detail]):` format for a release — it buries the lede.

## Slop prevention

Treat AI slop as review-hostile noise, not as proof that text or code is
wrong. The goal is to maximise information density.

- **AI signatures.** No "Generated by", no conversational filler, no
  unexplained emoji, no tool metadata.
- **Brittle references.** No hard-coded line numbers, fragile file
  counts, dated "as of" claims, bare SHAs, or local absolute paths.
  Evidence is exempt: keep exact counts, dates, and SHAs when they serve
  as evidence in benchmark results, stack traces, or lockfiles.
- **Diff narration.** Do not restate what moved, was renamed, or was
  removed in anything the reader holds alongside the diff: code,
  docstrings, README, or a pull request description. The diff and the
  commit message already carry it.
- **Branch-internal narrative.** Do not mention intermediate states,
  abandoned approaches, or "no longer" behaviour unless users of a
  published release actually experienced the old state.
- **Low-value scaffolding.** No ownerless TODOs, unused future-proofing,
  debug artefacts, or defensive wrappers around failure modes nothing can
  reach.
- **Prose inflation.** The diction table under [Voice](#voice) governs;
  replace an inflated word with a concrete description of behaviour,
  constraints, or trade-offs.
- **Coded labels.** Write rules and findings as plain imperatives. No
  `[R1]`, `Option B`, or any index a reader has to decode.

Preserve the "why". Never delete a comment documenting an invariant, a
protocol constraint, a platform quirk, or an upstream workaround — those
are the facts [Source comments](#source-comments) keeps, and every other
comment is judged by it.

A useful description explains what changed for the system or the reader;
it is not an inventory of files or functions the diff already shows.

### Durable source links

Link to a pinned revision, never to trunk, when citing a specific claim
about the code. A pinned permalink is not a brittle reference; an
unlinked SHA dropped into prose is. `blob/main/…` links rot silently —
the file moves, lines shift, and the anchor lands on unrelated code while
still resolving.

- Prefer a release tag (`blob/v0.0.10/…`). Most durable, and it tells the
  reader which released version the claim held for.
- Otherwise use a 7-char commit ref (`blob/9a29b1a/…`) reachable from
  trunk. Use when there is no tag or the claim is about unreleased code.
  Never a PR-head SHA — it can be rebased or garbage-collected.
- Reserve `blob/main/…` for living documents meant to always show the
  latest state, such as [CONTRIBUTING.md](CONTRIBUTING.md) itself.
- Line anchors (`#L120-L145`) are only safe on a pinned ref.

### The published-release test

When judging whether a detail is branch-internal narrative, use trunk —
not an intermediate state inside the branch making the change — as the
baseline. Ask: did users of the most recently published release ever
experience this old name, old behaviour, or bug? If no, it is
branch-internal narrative: it belongs in the commit message, and the
artefact describes only the final state.

### Cleanup in hindsight

Applying these rules retroactively inside a feature branch starts by
diffing against trunk to see which commits the branch actually
introduced. For commits the branch introduced, `fixup!` commits with
`git rebase --autosquash` address each one at its source, or a single
cleanup commit at the branch tip is acceptable. Leave commits from trunk
or a parent branch alone unless the user opts in.
