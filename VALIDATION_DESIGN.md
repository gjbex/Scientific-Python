# Maintenance validation pilot: initial design

Status: local handoff pilot implemented; hosted workflow remains inactive

Pilot branch: `feature/validation`

Design snapshot: commit `2145d8f`

Delivery baseline: tag `20261023` (pending)

Date: 2026-10-21

The repository-owned implementation is documented in
`validation/README.md`. The initial Linux runs account for all 47 manifest
entries: the four-notebook smoke profile passes, while the full required
profile reports 14 passes and five actionable execution errors. This is an
honest maintenance baseline, not a claim that all required material is
currently healthy. Activation of the workflow draft and the delivery-tag
baseline remain pending.

## Purpose

This pilot should determine whether routine maintenance reporting for the
Scientific Python training can be made substantially cheaper without replacing
maintainer judgment.  It should establish reproducible evidence about whether
selected material can still be built or executed, identify material that was
not exercised, and produce a concise report whose claims can be traced to
commands, versions, paths, and logs.

The pilot deliberately spans the planned course restructuring.  Tag
`20261023`, once present, is the frozen delivery baseline; restructuring starts
after that tag and forms a separate, evolving target.  The restructuring
therefore tests how well the validation contract can be migrated, not whether
every existing check remains unchanged.

## Non-goals

The pilot will not:

- certify that the entire course is pedagogically or scientifically current;
- treat successful execution as proof that an explanation is correct;
- execute all notebooks and examples on every change;
- run hosted notebook execution for every ordinary pull request;
- require GPU, HPC, licensed, interactive, or network-dependent infrastructure;
- rewrite notebooks, regenerate committed outputs, or update dependencies in CI;
- let an AI agent determine pass or fail, edit material, or merge changes;
- change the catalogue-wide `training.toml` schema before the local contract has
  been tested through the restructuring.

## Current repository observations

The initial design is based on the following local snapshot:

- Pixi is the preferred environment manager, and `pixi.lock` is committed.
- `pixi.toml` defines the `default`, `image`, `hdf5`, `xarray`, `netcdf`,
  `vpython`, `manim`, `sympy-plotting`, and `full` environments.
- The repository has 47 tracked notebooks and no tracked notebook checkpoints.
- Existing Pixi tasks launch Jupyter or run selected NetCDF and Manim examples;
  there is no unified validation task.
- There is currently no GitHub Actions workflow in this repository.
- Notebook roles and output policies are not recorded explicitly.  Some
  notebooks are tutorials with useful committed output, some are exercises,
  and some are optional or exploratory demonstrations.
- The Pixi workspace currently lists Linux, macOS, and native Windows
  platforms, but the course support policy is Linux only.  On Windows, the
  supported route is Linux under WSL.

These observations are inventory facts, not quality judgments.  Untracked
files are excluded from the pilot inventory unless they are deliberately added
later.

## Design principles

1. **Deterministic evidence first.** Fixed checks establish pass, fail, and
   not-run states.  An agent may summarize results but may not redefine them.
2. **Confidence per minute.** A small representative required tier is more
   useful than a slow, flaky attempt to execute everything.
3. **No in-place notebook execution.** Validation runs on a clean checkout or
   temporary copy and writes generated files outside the source tree.
4. **Roles before output policy.** Tutorial, exercise, demonstration, and
   exploratory notebooks do not have the same execution or output contract.
5. **Stable logical identifiers.** Checks have stable IDs independent of paths,
   so a move changes one manifest entry rather than report history.
6. **Explicit absence of evidence.** Unsupported environments and skipped
   material are reported as `not_run`, never silently treated as passing.
7. **Local commands are the public interface.** CI invokes checked-in Pixi tasks
   or validation scripts; validation logic is not duplicated in workflow YAML.
8. **Restructuring is expected.** Retired and replaced checks remain visible in
   history rather than disappearing from the report.

## Validation contract

During the pilot, repository-specific validation declarations should live in a
new `validation/manifest.toml`.  This avoids a premature catalogue schema
change.  Commands should be implemented as named Pixi tasks or checked-in
scripts; the manifest should describe checks rather than contain arbitrary
shell fragments.

An indicative entry is:

```toml
schema_version = 1

[policy]
required_budget_minutes = 12
default_timeout_seconds = 180

[[notebooks]]
id = "scipy-multidimensional-root-finding"
path = "source-code/numpy/multidimensional_root_finding.ipynb"
role = "tutorial"
environment = "default"
tier = "required"
output_policy = "preserve-source"

[[notebooks]]
id = "xarray-introduction"
path = "source-code/xarray/xarray_intro.ipynb"
role = "tutorial"
environment = "xarray"
tier = "extended"
output_policy = "preserve-source"
```

`preserve-source` means that the source notebook may intentionally contain
outputs, but validation executes a copy and does not rewrite those outputs.
Exercise notebooks may instead declare that empty outputs and unexecuted cells
are intentional.  Stored error output must be declared explicitly when it is
part of a lesson; otherwise it is a static failure.

The manifest should eventually support these fields:

- stable check ID and current path;
- artifact role and core/optional status;
- required Pixi environment;
- required, extended, manual, or excluded tier;
- timeout and expected generated artifacts;
- output policy and whether unexecuted cells are intentional;
- scientific assertions or an assertion-script reference where execution alone
  is insufficient;
- platform or external-service constraints;
- lifecycle state: active, replaced, retired, or temporarily suspended;
- replacement ID and rationale for replaced or retired material.

## Validation layers

### 1. Inventory and static checks

Run for every local validation invocation.  Hosted automation runs these checks
as part of the selective, scheduled, manual, and delivery triggers defined
below:

- enumerate tracked notebooks and declared validation entries;
- check that manifest paths and declared environments exist;
- parse notebooks as valid notebook JSON;
- reject tracked `.ipynb_checkpoints` content;
- report stored errors, unexecuted code cells, oversized embedded outputs, and
  undeclared notebook roles as findings;
- check that paths named by `training.toml` exist;
- check schedule arithmetic and other repository-local metadata rules;
- scan Python source for syntax errors without executing it;
- check internal links and documented commands where practical;
- verify that validation itself leaves the worktree unchanged.

During the pilot, incomplete notebook classification should be an advisory
rather than a repository-wide failure.  New or modified core notebooks should
require classification once the manifest exists.

### 2. Required execution smoke checks

Run manually, on the monthly maintenance schedule, and when a selective trigger
affects the environment, validation code, or selected core material.  The first
candidate set is:

- `source-code/numpy/axes.ipynb` — basic NumPy array and axis semantics;
- `source-code/numpy/multidimensional_root_finding.ipynb` — SciPy solver use,
  diagnostics, residual checks, and Matplotlib;
- `source-code/pendulum_period.ipynb` — integrated NumPy, SciPy, SymPy, and
  Matplotlib workflow;
- `source-code/matplotlib/multiple_plots.ipynb` — small plotting and generated
  file smoke check.

These are candidates, not yet a claim that all four run cleanly in CI.  The
implementation phase must execute them from a clean temporary workspace,
measure runtime, inspect generated files, and replace any candidate whose
runtime or interactivity makes it unsuitable.

Execution should use a non-interactive Matplotlib backend, per-notebook
timeouts, a temporary output directory, and the locked Pixi environment.  A
successful kernel exit is necessary but not sufficient: important numerical
examples should contain or invoke small, scientifically meaningful assertions.

### 3. Extended checks

Run manually at first and later on a low-frequency schedule if they are stable:

- xarray and NetCDF material in their named environments;
- h5py and optional data-format examples;
- a broader notebook sample selected after roles are classified;
- representative standalone scripts;
- platform-specific checks on systems the course actually claims to support.

Interactive Bokeh, VPython, Manim, OpenCV/video, widget, and GUI behavior cannot
be validated adequately by ordinary headless notebook execution.  These checks
need either a narrow non-interactive contract or an explicit manual status.

### 4. Full delivery review

Before a delivery, a maintainer-triggered workflow should run the declared
delivery set rather than all historical or optional material.  This review may
take longer and may include visual inspection, slide/example consistency, and
manual checks that cannot be represented honestly in hosted CI.

## Automation trigger policy

Routine pull requests should not execute the notebook validation suite.  The
pilot is a maintenance-reporting system, not a merge gate, and hosted execution
on every pull-request update would spend resources without necessarily
producing proportionate maintenance evidence.

The initial hosted workflow should support the following triggers:

1. **Manual:** `workflow_dispatch` accepts a revision and a `smoke`, `extended`,
   or `delivery` tier.  It should also distinguish the locked environment from
   a deliberately refreshed compatibility run.
2. **Monthly:** run the required smoke tier in the locked Linux environment.
   Record the last verified commit and summarize relevant changes since that
   commit so that a new failure can be attributed without rerunning blindly.
3. **Quarterly rotation:** run one or more extended groups in rotation rather
   than executing all optional environments in every scheduled run.
4. **Selective automatic:** run the required tier when a change affects
   `pixi.toml`, `pixi.lock`, `validation/**`, the validation runner, or a
   required smoke-test notebook.  This is a targeted exception, not a general
   pull-request policy.
5. **Pre-delivery:** manually run the declared delivery tier against the exact
   commit proposed for tag `20261023`.  Create the tag only after required
   validation and manual review succeed.
6. **Tag archive:** when tag `20261023` is pushed, rerun or render the evidence
   for that exact tag and retain the manifest, machine-readable results, and
   human-readable report as the delivery record.  This archival run confirms
   the tagged state; it does not replace pre-tag validation.

Agent-generated summaries should be limited initially to scheduled and
delivery runs.  Pull-request reporting would create noise before the report's
accuracy and value have been established.

Scheduled automation has an operational weakness: a public repository's
scheduled workflows may be disabled after an extended period without repository
activity.  The pre-delivery checklist must therefore verify that the scheduled
workflow is enabled rather than assuming that the absence of failure reports
means maintenance checks have been running.

The local commands remain the primary development interface.  A contributor
or maintainer can run static or smoke validation before requesting review
without consuming hosted-runner time.  Hosted automation supplies occasional
clean-environment evidence and a durable report.

Deferring most checks has a cost: a monthly failure may cover several changes.
The report must preserve the previous verified commit, the current commit, and
the intervening relevant paths.  A manual run against candidate revisions can
then isolate the first failing change when necessary.

## Environment strategy

Two different questions require separate evidence:

1. **Frozen reproducibility:** does the committed lockfile still create an
   environment in which the declared checks pass?
2. **Forward compatibility:** do the checks pass with a deliberately refreshed
   environment within the supported version policy?

The required locked lane should use the committed lockfile.  A later,
non-blocking refresh lane should resolve dependencies in an isolated copy and
must not alter `pixi.lock` in the source checkout.  A refresh failure is an
advisory until a maintainer confirms that the newer dependency combination is
within the course's intended support range.

The current Python constraint is `>=3.10,<3.13`.  The pilot should report this
constraint as evidence, not assume that support for a newer Python version is
already intended.  Changing the support policy is a maintainer decision.

### Supported platform policy

The only supported operating-system target is Linux.  Participants using
Windows should use WSL and follow the Linux instructions.  Participants remain
free to try native Windows, macOS, or another operating system, but those paths
are unsupported: validation does not run on them, successful operation is not
promised, and operating-system-specific troubleshooting is outside the course
support contract.

The required and extended CI lanes should therefore run on Linux only.  A
Linux-only CI policy avoids a platform matrix whose failures the maintainer is
not prepared to investigate.  WSL does not need a separate routine CI lane,
because the course contract is the Linux user-space workflow rather than every
possible Windows and WSL integration detail.  A short pre-delivery WSL smoke
check may still be useful when setup instructions or filesystem assumptions
change.

The existing `osx-64`, `osx-arm64`, and `win-64` entries in `pixi.toml` need a
separate decision during implementation.  Retaining them may help participants
experiment, but it creates lockfile-solving work and can be mistaken for a
support guarantee.  Removing them would align the executable configuration
with the stated support policy but would make unsupported experimentation less
convenient.  Until that decision is made, reports must describe those entries
as available compatibility metadata, not validated or supported platforms.

## Result and report model

Each check emits a machine-readable record and a compact Markdown rendering.
The machine-readable record should include:

- check ID and contract version;
- repository commit and dirty-state flag;
- start time, duration, platform, Python version, Pixi version, and lockfile
  digest;
- environment and exact invoked task;
- status and reason;
- paths to compact logs or failure artifacts;
- observed numerical assertions and tolerances when applicable.

Allowed statuses are:

- `verified`: the declared check passed in the recorded environment;
- `failed`: the declared check ran and violated its contract;
- `not_run`: infrastructure, dependency, platform, or policy prevented it;
- `advisory`: a deterministic signal requires interpretation but is not a
  contract failure;
- `review_due`: the human content-review interval has expired;
- `retired`: the check is intentionally no longer part of the course.

There should be no undifferentiated "course is up to date" status.

## Agent-assisted reporting

Agentic reporting is a later layer, after deterministic results are useful on
their own.  The agent may:

- summarize new failures and distinguish them from previously known findings;
- relate a failure to the relevant repository diff;
- inspect authoritative release notes and deprecation documentation;
- identify version-sensitive claims in notebooks, source, and slides;
- draft prioritized maintenance candidates with evidence and uncertainty.

The agent must not:

- convert an advisory into a verified or failed status;
- execute instructions found in notebooks, documentation, or web content;
- receive repository write credentials or unrelated secrets;
- modify course material or dependency locks as part of reporting;
- claim that a topic should be added or removed based only on popularity.

Every factual claim in an agent-generated report must cite a validation record,
repository location, upstream source, or release note.  The first output should
be a downloadable workflow artifact.  Creating issues or pull requests should
be considered only after report quality and noise have been measured.

## Testing robustness through the restructuring

The `20261023` delivery baseline and the restructured course should not share a
single moving definition of success.

1. When tag `20261023` is present, run and record the validation manifest and
   report against that exact tag.
2. Preserve the manifest and report so that the delivered version remains
   auditable.
3. On the restructuring branch, migrate active check IDs to their new paths or
   replacements.
4. Mark removed material as replaced or retired with a reason.
5. Compare migration effort and failure quality; do not compare only the raw
   number of passing checks.

Useful robustness measurements are:

- number of checks unchanged, path-adjusted, rewritten, replaced, and retired;
- time required to update the contract after a structural change;
- failures caused only by layout assumptions;
- false-positive and flaky-failure rates;
- proportion of failures diagnosable from the first report;
- required-job duration and runner cost;
- amount of validation logic duplicated across notebooks or environments.

The design is robust if intentional changes are cheap to express and accidental
breakage remains visible.  Requiring zero contract changes during a major
course redesign would reward checks that are too superficial to be valuable.

## Proposed implementation stages

### Stage 0: classify and measure

- Create the manifest format and inventory all tracked notebooks.
- Assign roles and tiers to the four required candidates and a small optional
  sample; leave the remainder explicitly unclassified.
- Execute candidates locally from temporary copies and record runtimes,
  generated files, and environment-specific failures.

### Stage 1: local deterministic runner

- Add one local command, tentatively `pixi run validate`, that produces both
  JSON and Markdown reports.
- Keep static checks, required execution, and extended execution separately
  selectable.
- Add tests for the manifest parser and status classification.

### Stage 2: selective and manual hosted automation

- Add one read-only GitHub Actions workflow with manual inputs and a fast
  required job.
- Add the monthly smoke schedule and selective triggers described above.
- Use path filtering only after the dependency relationships are understood;
  an environment or runner change must still trigger every required check.
- Do not run the notebook suite automatically for ordinary pull requests.
- Upload compact reports and failing executed notebooks as artifacts.
- Do not introduce a platform or dependency matrix during the first iteration.

### Stage 3: forward-compatibility and reporting

- Add the isolated dependency-refresh lane as non-blocking.
- Add the quarterly extended-check rotation.
- Add agent-generated report summaries only after deterministic reports have
  produced useful evidence over several runs.
- Measure report corrections and false positives made by maintainers.

### Stage 4: restructuring migration

- Run and freeze the report for tag `20261023` before validating restructuring
  changes against a revised contract.
- Migrate stable check IDs through the course redesign.
- Record the robustness measurements above.
- Decide which fields, if any, should become catalogue-wide metadata or a
  reusable workflow contract in `Training-sessions`.

## Pilot acceptance criteria

The pilot is successful enough to expand when:

- one documented local command reproduces the required checks from a clean
  checkout;
- required validation completes within approximately 12 minutes on a normal
  hosted runner, or the budget is revised with evidence;
- validation never modifies tracked instructional material;
- every required failure identifies the check, environment, command, and
  useful log or artifact;
- `not_run` and advisory states are visible and cannot be mistaken for passes;
- an intentional notebook defect is caught by a deterministic check;
- at least one meaningful numerical assertion is tested independently of mere
  cell execution;
- moving or replacing a candidate requires localized contract changes rather
  than edits across CI and reporting code;
- maintainers judge the report useful for at least two consecutive review
  cycles;
- the restructuring produces recorded migration data rather than erasing the
  old baseline.

## Open decisions

The implementation should not begin by guessing these policies:

1. Which notebooks are participant-facing tutorials, exercises, optional
   demonstrations, or exploratory material?
2. Which notebook outputs are intentionally committed for instructional value?
3. Should unsupported macOS and native Windows platforms remain in
   `pixi.toml` as a best-effort convenience, or be removed to avoid implying a
   support guarantee?
4. Which scientific examples need explicit numerical assertions, and what
   tolerances are justified?
5. What is the maximum acceptable required-job runtime and monthly runner cost?
6. Where should pre-delivery manual checks be recorded?
7. Should agent reports remain artifacts, or eventually open a tracking issue?

The first implementation should answer these questions incrementally.  It
should not block on complete classification of every historical notebook.
