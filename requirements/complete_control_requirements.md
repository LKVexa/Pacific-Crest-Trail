# Pacific Crest Trail Training Adventure Complete Detailed Control Checklists

Version 1.0 | 1 October 2026

465 original controls | 3,720 detailed child controls | 23 control groups

[Checklist index and component volumes](PCT_Control_Checklists_Index.md) · [Original baseline](PCT_Training_Adventure_Checklist.md) · [Control register](PCT_Control_Checklists_Register.json)

The required entry point is a `.cmd` launcher invoking PowerShell. It starts or reuses the verified owned service at `http://127.0.0.1:<port>` and opens the selected daily dossier. Repository-local SQLite records are authoritative. Each launch is logged; an unfinished day resumes. Only deliberate, eligible day completion commits the next-leg pointer. Actual workouts, sourced trail facts, and fictional game state retain separate meanings. Real calendar dates do not automatically advance expedition days.

## Evidence and disposition rules

All checkboxes start unchecked. These are proposed requirements and verification tasks, not proof of implemented software or completed assessment. Select the actual release scope before marking optional integrations or expansion features applicable. A personal local installation may assign several responsibilities to one person; the role names do not require a large organization.

For each child control, record applicability, accountable owner, implementation or content reference, verification method, evidence reference, reviewer and date, and the exact build, schema, route, content, and rules versions reviewed. Track status as not started, in progress, implemented, verification failed, verified, or exception accepted. Record not applicable separately with rationale and scope.

Check a child only after its stated result is supported by reviewed evidence. Mark its parent verified only when all applicable children are verified and any exceptions are explicitly accepted. An exception records impact, compensation, owner, expiry, and review trigger. Missing evidence and deferred work remain visible. Evidence can be a code inspection, schema, authored fixture, source or rights review, manual walkthrough, automated check, reconciliation report, or isolated recovery exercise as appropriate to the requirement.

The eight children beneath each parent are tailored to that requirement. Their order generally moves from definition and implementation constraints through normal behavior, boundary or failure verification, and control-specific acceptance evidence. Preserve the parent and child IDs in implementation tasks, test records, and defect reports.

## Contents

| Group | Control scope | Parents | Children |
| --- | --- | ---: | ---: |
| GOV | [Governing product and architecture controls](#gov-governing-product-and-architecture-controls) | 20 | 160 |
| C01 | [Route and stage planner](#c01-route-and-stage-planner) | 20 | 160 |
| C02 | [Daily dossier publishing system](#c02-daily-dossier-publishing-system) | 20 | 160 |
| C03 | [Photograph and media library](#c03-photograph-and-media-library) | 20 | 160 |
| C04 | [Training planner](#c04-training-planner) | 20 | 160 |
| C05 | [Workout companion](#c05-workout-companion) | 20 | 160 |
| C06 | [Workout logger](#c06-workout-logger) | 20 | 160 |
| C07 | [Campaign progression engine](#c07-campaign-progression-engine) | 20 | 160 |
| C08 | [Branching decision engine](#c08-branching-decision-engine) | 20 | 160 |
| C09 | [Encounter scheduler](#c09-encounter-scheduler) | 20 | 160 |
| C10 | [Virtual resource system](#c10-virtual-resource-system) | 20 | 160 |
| C11 | [Trail knowledge activities](#c11-trail-knowledge-activities) | 20 | 160 |
| C12 | [Characters and story continuity](#c12-characters-and-story-continuity) | 20 | 160 |
| C13 | [Camp journal and collection](#c13-camp-journal-and-collection) | 20 | 160 |
| C14 | [Training and preparation dashboard](#c14-training-and-preparation-dashboard) | 20 | 160 |
| C15 | [Web application shell](#c15-web-application-shell) | 35 | 280 |
| C16 | [Content administration and quality controls](#c16-content-administration-and-quality-controls) | 20 | 160 |
| C17 | [CMD and PowerShell launch orchestration](#c17-cmd-and-powershell-launch-orchestration) | 20 | 160 |
| C18 | [Repository hike history and next leg state](#c18-repository-hike-history-and-next-leg-state) | 20 | 160 |
| C19 | [Loopback HTTP service and local dossier delivery](#c19-loopback-http-service-and-local-dossier-delivery) | 20 | 160 |
| SCN | [Scenario design controls](#scn-scenario-design-controls) | 12 | 96 |
| INT | [System integration acceptance controls](#int-system-integration-acceptance-controls) | 20 | 160 |
| REL | [Release and operational acceptance controls](#rel-release-and-operational-acceptance-controls) | 18 | 144 |
| Total | All controls | 465 | 3,720 |

## GOV Governing product and architecture controls

**Accountable roles:** Product and architecture owner, with affected domain reviewers; one person may hold several roles.

**Required evidence:** Product charter; component responsibility matrix; architecture decisions; data and metric dictionaries; risk register; selected release scope; traceability record template.

**Exit criterion:** The scope, data domains, progression semantics, responsibilities, and release boundaries are explicit enough that a reviewer can distinguish required behavior from optional expansion without interpreting story prose.

### Control GOV 01

**Original requirement GOV.01:** Approve a product charter identifying the intended user, real training goals, daily dossier experience, supported equipment context, and boundaries of the initial release.

- [ ] **GOV.01.01** Identify the intended local user, supported participation contexts, and initial exclusions in a dated charter approved by the product owner.
- [ ] **GOV.01.02** Describe real training objectives as user supplied preparation outcomes, with examples distinguishing activity evidence from fictional expedition achievements and entertainment.
- [ ] **GOV.01.03** Specify the complete dossier journey from launcher invocation through briefing, accepted activity, pending decisions, camp reflection, and explicit day completion.
- [ ] **GOV.01.04** Inventory supported equipment and manual participation paths, including unknown device capabilities, absent measurements, and assignments that require no exercise equipment.
- [ ] **GOV.01.05** List required release components and optional capabilities, with an applicability decision and rationale for every feature excluded from the initial deployment.
- [ ] **GOV.01.06** Map charter promises to acceptance controls, marking any unsupported promise as deferred before publishing onboarding language or pilot instructions to users.
- [ ] **GOV.01.07** Review interrupted sessions, offline launches, recovery participation, and return after absence against the charter without introducing additional physical training obligations.
- [ ] **GOV.01.08** Record approval date, charter revision, accountable owner, review evidence, and change triggers; require scope revisions to identify affected controls and releases.

### Control GOV 02

**Original requirement GOV.02:** Define preparation outcomes separately for physical activity, trail familiarity, equipment practice, and planning judgment; do not collapse them into an unexplained numerical readiness score.

- [ ] **GOV.02.01** Define physical activity outcomes using recorded categories and quantities, including measurement coverage, without asserting that participation predicts fitness or medical readiness.
- [ ] **GOV.02.02** Specify trail familiarity outcomes through reviewed learning activities, source dates, and recorded responses, separately from the distance traveled in fictional stages.
- [ ] **GOV.02.03** Define equipment practice outcomes with task evidence, equipment identity where supplied, observation dates, and unresolved issues rather than universal proficiency claims.
- [ ] **GOV.02.04** Describe planning judgment outcomes using decision rationales and reviewed scenario criteria, distinguishing educational evaluation from certification of real wilderness competence.
- [ ] **GOV.02.05** Create an outcome matrix connecting each preparation domain to its source records, display labels, calculation rules, and limitations for the selected release.
- [ ] **GOV.02.06** Review dashboard and reward designs for accidental combination of unlike outcomes; prohibit unexplained weighting that produces an apparently validated numerical readiness result.
- [ ] **GOV.02.07** Test representative recovery, knowledge, equipment, and walking participation examples against the matrix, verifying that each contributes only to its specified preparation domains.
- [ ] **GOV.02.08** Approve domain descriptions and evidence requirements with the training and content reviewers, retaining disputed interpretations and their resolutions in the governance record.

### Control GOV 03

**Original requirement GOV.03:** Create separate authoritative models for real activity, sourced geographic facts, and fictional campaign state; define which services can read or change each model.

- [ ] **GOV.03.01** Document separate schemas for actual workouts, sourced route facts, and fictional campaign state, including stable identities, ownership, versioning, and authoritative storage.
- [ ] **GOV.03.02** Create a service permission matrix identifying read and mutation operations for each domain, with explicit prohibition of narrative writes into physical assignment fields.
- [ ] **GOV.03.03** Specify cross-domain references by identifiers and revisions, preventing copied display values from becoming independent authoritative measurements or alternative route fact records.
- [ ] **GOV.03.04** Review SQLite relationships and transaction boundaries so campaign credits reference effective workouts while corrections preserve the original measurement and causal revision history.
- [ ] **GOV.03.05** Specify browser access through validated loopback APIs; prohibit browser cache, generated HTML, and media metadata from independently changing authoritative training or campaign state.
- [ ] **GOV.03.06** Design boundary tests that submit campaign mileage as physical distance and fictional fatigue as assignment changes, requiring rejection without partial database mutation.
- [ ] **GOV.03.07** Document repair ownership when a cross-domain reference is missing or stale, including retained evidence, visible unavailable states, and safe regeneration procedures.
- [ ] **GOV.03.08** Approve schema diagrams, permission matrix, boundary test evidence, and migration responsibilities before enabling dependent components in the release publication manifest.

### Control GOV 04

**Original requirement GOV.04:** Classify displayed information as sourced fact, dated observation, supplied scenario assumption, fictional event, illustration, or estimate; specify where each classification must be visible.

- [ ] **GOV.04.01** Create a classification vocabulary defining sourced fact, dated observation, supplied scenario assumption, fictional event, illustration, and estimate with distinct user-facing meanings.
- [ ] **GOV.04.02** Inventory dossier, map, companion, journal, dashboard, and export surfaces where classifications must appear, including compact views and accessibility equivalents for labels.
- [ ] **GOV.04.03** Require factual items to link source identity and applicable date, while observations identify observation time and estimates disclose their calculation assumptions and uncertainty.
- [ ] **GOV.04.04** Specify visible fictional and illustrative labels where realistic narrative or imagery could be mistaken for geographic evidence, equipment measurements, or present trail conditions.
- [ ] **GOV.04.05** Define mixed-content labeling rules for cards containing both factual locations and fictional events, preserving the classification of each meaningful statement or displayed quantity.
- [ ] **GOV.04.06** Review missing, conflicting, or outdated classification metadata; require correction or visible qualification before publication rather than silently defaulting every item to fact.
- [ ] **GOV.04.07** Exercise representative content through browser rendering and export, checking that responsive layout, text enlargement, and screen-reader output retain the required information classifications.
- [ ] **GOV.04.08** Retain the classification matrix, reviewed examples, defect resolutions, and publishing checks as evidence for every content release covered by the approved labeling policy.

### Control GOV 05

**Original requirement GOV.05:** Establish a hard boundary preventing narrative rules, resource depletion, random outcomes, and generated prose from modifying physical training assignments or issuing treadmill commands.

- [ ] **GOV.05.01** Document the boundary between narrative evaluation and accepted training assignments, listing every physical target field and every service authorized to modify those fields.
- [ ] **GOV.05.02** Review event, resource, randomization, and prose generation contracts to ensure outputs contain fictional consequences only and cannot invoke assignment mutation or equipment control operations.
- [ ] **GOV.05.03** Require physical target changes to originate from the accepted plan workflow, with explicit values, user acceptance, and durable revision evidence before they take effect.
- [ ] **GOV.05.04** Inspect the selected runtime and dependency interfaces for treadmill command capabilities; exclude any automatic control route from the initial companion and document that architectural decision.
- [ ] **GOV.05.05** Create adversarial scenarios involving storms, exhausted resources, character injury, and lost encounters, verifying that each leaves physical duration, speed, incline, and distance targets unchanged.
- [ ] **GOV.05.06** Test malformed narrative payloads containing equipment commands or target overrides, requiring validation failure without execution, hidden acceptance, or persistence into training records.
- [ ] **GOV.05.07** Specify incident handling for a discovered boundary breach, including disabling the affected rule, preserving causal evidence, and identifying assignments requiring user-visible correction.
- [ ] **GOV.05.08** Require product, training, and integrity reviewers to sign the boundary assessment and negative-test evidence before release; unresolved target-changing paths fail the release gate.

### Control GOV 06

**Original requirement GOV.06:** Define the relationship between the real training calendar and the expedition itinerary, including partial sessions, virtual rest days, skipped stages, and return after absence.

- [ ] **GOV.06.01** Define real-calendar entities and expedition-day entities separately, documenting their identifiers, timezone interpretation, relationships, and independent advancement conditions in the chronology specification.
- [ ] **GOV.06.02** Specify how partial workouts accumulate across real dates toward one hike day while preserving the actual recording dates and the unfinished virtual stage identity.
- [ ] **GOV.06.03** Describe virtual rest-day participation and accepted recovery assignments, distinguishing story chronology changes from fabricated physical distance, movement duration, or ascent measurements.
- [ ] **GOV.06.04** Define skipped-stage and transport records with reason, policy, and route effects, ensuring that skipped virtual mileage never appears as actual walking evidence.
- [ ] **GOV.06.05** Document return-after-absence behavior that resumes committed unfinished state without catching up expedition days, generating workouts, or increasing future targets because real days elapsed.
- [ ] **GOV.06.06** Specify explicit day completion as the sole committed successor operation; launches, midnight changes, page views, and generated dossiers have no independent advancement authority.
- [ ] **GOV.06.07** Review example timelines containing overnight sessions, several workouts per stage, recovery days, and long absences, confirming separate calendars and correctly retained activity dates.
- [ ] **GOV.06.08** Approve the chronology examples, mapping policy revision, user explanation, and component contracts together so every calendar and report implements the same documented relationships.

### Control GOV 07

**Original requirement GOV.07:** Select the enabled progression modes and specify the default; explain conversions before crediting activity and preserve the policy version used for each credit.

- [ ] **GOV.07.01** List enabled distance, chapter, and scaled modes, identifying the default and recording a reason for modes deferred or disabled in the selected release.
- [ ] **GOV.07.02** Specify each mode's eligible sources, conversion parameters, threshold units, partial-credit rules, rounding representation, carryover treatment, and correction behavior before awarding any credit.
- [ ] **GOV.07.03** Create a user-facing explanation showing actual input and expected virtual result for each enabled mode, including preparation tasks and unavailable measurements where relevant.
- [ ] **GOV.07.04** Require each effective credit to retain its progression policy identity and revision, protecting historical interpretation when the selected mode or conversion parameters later change.
- [ ] **GOV.07.05** Define mode-change approval and effective dates, with previewed impacts and deliberate historical migration decisions rather than implicit reapplication to all existing campaign records.
- [ ] **GOV.07.06** Review boundary examples where surplus credits exceed several stages, ensuring no mode bypasses mandatory decisions or advances committed next-leg state without explicit day completion.
- [ ] **GOV.07.07** Reconcile independently calculated conversion examples against implemented rule outputs and inspect negative cases for ineligible categories, missing required quantities, and unsupported mode configurations.
- [ ] **GOV.07.08** Publish the approved mode matrix, explanatory examples, calculation evidence, and migration policy with the release manifest; reject credits lacking an attributable policy version.

### Control GOV 08

**Original requirement GOV.08:** Assign accountable owners for each component and reviewers for geography, training content, narrative, media rights, accessibility, data integrity, security, and releases.

- [ ] **GOV.08.01** Assign one accountable owner to each component, recording responsibilities, expected deliverables, escalation paths, and any delegated implementation work in the responsibility matrix.
- [ ] **GOV.08.02** Name geography and training reviewers with defined review scopes, distinguishing source verification and content limitations from claims of professional certification or individualized prescription approval.
- [ ] **GOV.08.03** Assign narrative and media-rights reviewers to continuity, classification, attribution, licensing, and withdrawal decisions, including replacement responsibility when an asset becomes unavailable or disallowed.
- [ ] **GOV.08.04** Define accessibility, integrity, and security review responsibilities with concrete artifacts such as keyboard evidence, ledger reconciliation, transaction recovery results, and loopback boundary assessments.
- [ ] **GOV.08.05** Identify the release approver and rollback authority, ensuring acceptance decisions reference reviewed evidence, outstanding exceptions, and the exact application, database, and content versions.
- [ ] **GOV.08.06** Document permissible role combinations for a small project and identify where a second review is needed for unresolved factual, integrity, or training-boundary concerns.
- [ ] **GOV.08.07** Specify reviewer absence and ownership-transfer procedures so critical defects, source corrections, and privacy requests have an accountable handler throughout pilot and release support.
- [ ] **GOV.08.08** Approve the dated responsibility matrix and verify every required control group has an owner and relevant reviewer before assigning implementation or publication acceptance status.

### Control GOV 09

**Original requirement GOV.09:** Maintain an architecture decision register covering application boundaries, authoritative records, persistence, synchronization, rule execution, and content versioning.

- [ ] **GOV.09.01** Create an architecture decision register with stable decision IDs, context, alternatives, selected approach, rationale, owner, approval date, and consequences for acceptance requirements.
- [ ] **GOV.09.02** Record application boundaries across CMD, PowerShell, local service, browser interface, SQLite, dossier files, diagnostics, and exports, including which component owns each mutation.
- [ ] **GOV.09.03** Document SQLite authority, schema migration strategy, transactional durability expectations, backup consistency, and recovery procedures for missing or incompatible repository state before implementation starts.
- [ ] **GOV.09.04** Specify synchronization as local API requests with expected revisions and idempotency identifiers, documenting stale-tab conflicts and visibly unsaved drafts when the service is unavailable.
- [ ] **GOV.09.05** Record rule execution location, deterministic inputs, version pinning, event ordering, and the prohibition on narrative mechanisms changing accepted physical assignments or equipment behavior.
- [ ] **GOV.09.06** Define published dossier immutability, content release manifests, artifact staging, and recovery behavior when database references exist but generated files are missing or corrupted.
- [ ] **GOV.09.07** Review a complete launch-and-completion walkthrough against the decision register, identifying unowned responsibilities or contradictions before dependent components adopt incompatible architectural assumptions.
- [ ] **GOV.09.08** Require decision amendments to list affected schemas, tests, controls, and migration actions, retaining superseded rationale so reviewers can reconstruct the supported release architecture.

### Control GOV 10

**Original requirement GOV.10:** Define immutable published records and mutable user records, their retention, revision, withdrawal, and correction policies; prohibit silent rewriting of established campaign history.

- [ ] **GOV.10.01** Inventory published dossier snapshots, route releases, accepted completion records, workout revisions, journals, and user preferences, assigning each an immutable or mutable lifecycle classification.
- [ ] **GOV.10.02** Define revision and correction mechanisms that retain attributable prior outcomes where required, distinguishing edited user content from replacement of an established campaign event or branch.
- [ ] **GOV.10.03** Set retention periods and deletion applicability by record class, identifying the minimal provenance allowed after withdrawal without assuming indefinite retention of sensitive training detail.
- [ ] **GOV.10.04** Specify content withdrawal behavior for inaccurate facts or revoked media, including unavailable markers, replacement artifacts, source references, and explicit preservation of historical event meanings.
- [ ] **GOV.10.05** Prohibit silent changes to completed campaign history during regeneration, migration, or dashboard recalculation; require correction annotations identifying actor, reason, affected revision, and effective outcome.
- [ ] **GOV.10.06** Review replay and restore examples with superseded plans, corrected workouts, withdrawn photographs, and edited reflections, ensuring policy distinctions remain visible in history and exports.
- [ ] **GOV.10.07** Document repair authority and user notification criteria when published artifacts must be replaced, including reversible staging and preservation of a reviewable correction trail.
- [ ] **GOV.10.08** Approve the lifecycle table, retention rules, correction examples, and immutable-record enforcement evidence before permitting publication, historical migration, or managed deletion features in production.

### Control GOV 11

**Original requirement GOV.11:** Publish a metric and units dictionary covering actual distance, virtual distance, elapsed time, moving time, pause time, unknown intervals, incline exposure, and completion status.

- [ ] **GOV.11.01** Define actual distance and virtual distance as separate metrics with canonical units, source domains, precision, rounding policy, and explicit prohibition on substituting one for another.
- [ ] **GOV.11.02** Specify elapsed duration as moving plus stationary plus unknown observations, with examples proving that application pause overlaps observations rather than becoming an additional duration term.
- [ ] **GOV.11.03** Describe aggregate self-reported durations separately from evidence-backed interval partitions, identifying unavailable breakdowns and avoiding invented moving time when only elapsed time was supplied.
- [ ] **GOV.11.04** Define incline observations, achieved exposure, requested prompts, and virtual ascent separately, with formulas, coverage requirements, and uncertainty labels for every supported derived quantity.
- [ ] **GOV.11.05** Specify completion statuses for workouts, assignments, and hike days, including partial, skipped, cancelled, and committed completion meanings without treating launches as exercise or completion.
- [ ] **GOV.11.06** Create conversion examples for every supported quantity using canonical and original units, including null, meaningful zero, threshold equality, and display-rounding boundary cases.
- [ ] **GOV.11.07** Review labels across forms, APIs, dashboards, generated dossiers, and exports against the dictionary, requiring identical definitions or an explicitly named alternative metric interpretation.
- [ ] **GOV.11.08** Version and approve the dictionary with independent calculation evidence; require stored and exported metric records to identify the definition revision applicable to their interpretation.

### Control GOV 12

**Original requirement GOV.12:** Record the author, source, version, and review status of supplied training content; use user-authored or reviewed assignments without inventing personalized prescriptions from fictional trail demands.

- [ ] **GOV.12.01** Create an intake record for each supplied training plan or template containing author, origin, source reference, version, creation date, and permitted use context.
- [ ] **GOV.12.02** Document review status and review scope, including reviewer identity where applicable, limitations, excluded audiences, and whether assignments are user authored, imported, or appropriately reviewed.
- [ ] **GOV.12.03** Require assignments to reference the supplied plan revision accepted by the user, preserving that reference in actual workout records and historical adherence calculations after plan changes.
- [ ] **GOV.12.04** Review every physical target field for attributable plan origin; reject targets inferred from fictional grade, weather, fatigue, pack depletion, or prose generation without accepted supplied content.
- [ ] **GOV.12.05** Specify behavior for missing authorship, unclear review scope, and obsolete imported templates, including visible limitations, withheld publication, or a recorded user-authored acceptance decision.
- [ ] **GOV.12.06** Inspect guidance language for individualized diagnostic or medical claims and unsupported progression prescriptions, requiring revision into the accepted plan's documented scope before release.
- [ ] **GOV.12.07** Test representative fictional setbacks and route changes against supplied assignments, demonstrating unchanged physical targets and a deliberate acceptance step for any independently proposed plan revision.
- [ ] **GOV.12.08** Retain source records, review comments, accepted versions, limitations, and boundary-test evidence in the publication manifest so reviewers can trace every supplied training instruction.

### Control GOV 13

**Original requirement GOV.13:** Design missed-session, partial-session, resource-exhaustion, and story-failure behavior so that continued participation never depends on unplanned additional exertion.

- [ ] **GOV.13.01** Define missed-session behavior that preserves recorded activity and planned history, offering postponement or accepted alternatives without calculating compulsory compensatory duration, distance, speed, or incline.
- [ ] **GOV.13.02** Specify partial-session continuation with retained actual quantities, incomplete assignment status, and an explicit choice to resume, shorten, substitute, or leave work partial under accepted rules.
- [ ] **GOV.13.03** Describe resource-exhaustion recovery as fictional decisions or adjusted campaign state, with no dependency on buying progress through additional unplanned exertion or changed physical targets.
- [ ] **GOV.13.04** Author story-failure continuation paths that retain participation access, pending choices, and educational meaning while keeping workout assignments independent of fictional success or failure consequences.
- [ ] **GOV.13.05** Review reminder, achievement, and debrief wording for pressure to extend workouts, preserving configurable notices and accepted recovery or preparation participation as legitimate documented alternatives.
- [ ] **GOV.13.06** Exercise combined cases involving missed sessions, exhausted resources, unresolved decisions, and a long absence, requiring a usable continuation path without adding physical training requirements.
- [ ] **GOV.13.07** Document escalation and repair when content accidentally blocks participation behind exertion, identifying the responsible rule, replacement path, and affected campaign or assignment records.
- [ ] **GOV.13.08** Approve continuation scenarios with product and training reviewers, retaining expected outcomes and user-facing examples as release evidence for all enabled failure and recovery mechanisms.

### Control GOV 14

**Original requirement GOV.14:** Identify the authoritative source and conflict policy for every shared quantity; document whether conflicts can merge automatically or require a user decision.

- [ ] **GOV.14.01** Inventory every shared quantity, including assignment targets, workout metrics, interval classifications, credits, resources, route chainage, completion status, and dashboard totals with authoritative source ownership.
- [ ] **GOV.14.02** Define source-of-truth relationships for derived quantities, recording input revisions, calculation policies, and invalidation rules rather than allowing derived caches to overwrite their originating records.
- [ ] **GOV.14.03** Classify conflicts as mergeable independent additions, deterministic recalculations, or incompatible revisions requiring explicit user reconciliation, with examples for each enabled mutation type and quantity.
- [ ] **GOV.14.04** Specify expected-revision checks and mutation identities across browser tabs, establishing which conflicts reject writes and which accepted events can safely contribute through a documented merge rule.
- [ ] **GOV.14.05** Document measurement arbitration when multiple sources describe one workout, ensuring per-metric selection and retained provenance without summing duplicated physical activities or guessed timestamp merges.
- [ ] **GOV.14.06** Create conflict examples for simultaneous plan edits, competing branches, correction versus completion, and duplicate imports, recording the expected preserved state and user reconciliation path.
- [ ] **GOV.14.07** Define recovery ownership for interrupted transactions or pending recalculations, requiring database reconciliation before cached or provisional values are presented as current authoritative shared quantities.
- [ ] **GOV.14.08** Approve the authority and conflict matrix with integration evidence demonstrating consistent decisions across components, including rejected stale writes and successful replay of safely mergeable events.

### Control GOV 15

**Original requirement GOV.15:** Set reference hardware, browser support, storage, accessibility, latency, and content-loading budgets before pilot testing; record the basis for the selected thresholds.

- [ ] **GOV.15.01** Identify reference computer hardware, operating system, storage medium, browser versions, and expected dataset sizes used to establish reproducible pilot performance and usability acceptance conditions.
- [ ] **GOV.15.02** Set launch-readiness, durable-save acknowledgement, dossier-rendering, and dashboard-response budgets, recording user needs and measurement methods rather than unexplained numerical targets without practical context.
- [ ] **GOV.15.03** Define storage limits for database, generated dossiers, media cache, diagnostics, exports, and backups, including reserve capacity and visible disk-exhaustion behavior for canonical writes.
- [ ] **GOV.15.04** Specify accessibility acceptance conditions for keyboard access, screen readers, contrast, text enlargement, reduced motion, and typical treadmill viewing distances with documented review methods.
- [ ] **GOV.15.05** Document browser support assumptions for monotonic timing, background throttling, asset formats, and recovery after suspension, identifying unsupported behavior and the required visible fallback states.
- [ ] **GOV.15.06** Measure representative first launch, warm resume, large-history dashboard, and missing-asset scenarios on reference hardware, recording median and upper-bound results against the selected release budgets.
- [ ] **GOV.15.07** Review boundary conditions including low disk space, offline internet, stale tabs, long histories, and enlarged text; record failures, mitigations, and scope exceptions before pilot acceptance.
- [ ] **GOV.15.08** Approve thresholds, measurement evidence, equipment assumptions, and revisit triggers together, requiring retesting when runtime, content volume, supported browsers, or reference hardware materially changes.

### Control GOV 16

**Original requirement GOV.16:** Define repository-local persistence as authoritative and loopback-only serving as the required deployment; browser cache deletion, port changes, and offline internet status must not alter saved hike history.

- [ ] **GOV.16.01** Document the repository SQLite database and referenced dossier manifests as authoritative hike state, with browser storage designated a replaceable presentation cache rather than persistence evidence.
- [ ] **GOV.16.02** Specify loopback binding to the validated local address and selected port, including origin checks, owned-instance identification, and rejection of unintended network-interface serving in release configuration.
- [ ] **GOV.16.03** Define repository resolution from launcher location, preventing browser working directories, URL port values, or cached paths from selecting a different authoritative campaign database.
- [ ] **GOV.16.04** Describe incomplete-day resume and committed-next-leg resolution using database records, distinguishing run logging from workout creation, generated dossier availability, and explicit hike-day completion authority.
- [ ] **GOV.16.05** Test browser cache deletion and a changed service port, requiring identical campaign identity, workout totals, unfinished-day status, and committed successor state after local launcher restart.
- [ ] **GOV.16.06** Exercise offline internet with already available dossier assets, verifying successful local history retrieval while distinguishing missing remote assets from a failed canonical loopback service connection.
- [ ] **GOV.16.07** Document backup and recovery responsibilities for repository-local state, including manifest reconciliation when restored database rows reference missing dossier snapshots or media files after interruption.
- [ ] **GOV.16.08** Approve deployment-boundary evidence, cache-replacement tests, and restart reconciliation results before release; any optional remote capability requires a separate applicability and privacy decision record.

### Control GOV 17

**Original requirement GOV.17:** Maintain a data inventory, access matrix, retention schedule, diagnostic-redaction rules, and external integration register for the features actually enabled.

- [ ] **GOV.17.01** Inventory enabled data fields, local files, derived records, diagnostics, exports, and backup copies, recording purposes, sensitivity, authoritative ownership, and whether collection is required or optional.
- [ ] **GOV.17.02** Create an access matrix covering local profile, filesystem users, launcher, service, browser origin, content tools, and export operations, with explicit privilege and boundary assumptions.
- [ ] **GOV.17.03** Assign retention and deletion rules by data class, including optional background information, notes, source observations, audit revisions, generated personal dossiers, and managed backup retention windows.
- [ ] **GOV.17.04** Define diagnostic redaction patterns and approved log fields so failures can be investigated without exposing workout notes, optional biometrics, personal background, or sensitive configuration values.
- [ ] **GOV.17.05** Register each enabled external integration with purpose, data transferred, authorization path, source identifiers, dependency behavior, and deletion limitations; record disabled integrations as outside current deployment scope.
- [ ] **GOV.17.06** Review representative collection, export, debugging, and restore journeys against the inventory, checking that undocumented fields or unmanaged copies are identified before acceptance or user privacy explanations.
- [ ] **GOV.17.07** Specify incident response for accidental sensitive logging or unauthorized origin access, including containment, affected-data assessment, repair ownership, and review of retained local diagnostic copies.
- [ ] **GOV.17.08** Approve the inventory, access matrix, retention schedule, redaction examples, and integration register together, requiring an update whenever an enabled feature changes collection or data movement.

### Control GOV 18

**Original requirement GOV.18:** Establish traceability from each released dossier and rule to its sources, dependencies, tests, reviewer, and publication manifest.

- [ ] **GOV.18.01** Define a traceability record linking each published dossier identity to route release, itinerary, training snapshot, progression policy, narrative assets, source references, and publication manifest revision.
- [ ] **GOV.18.02** Require released rules to identify deterministic inputs, dependency versions, owner, reviewed behavior, applicable acceptance controls, and the tests that establish the supported operational contract.
- [ ] **GOV.18.03** Specify reviewer identities and review dates for factual, training, narrative, rights, accessibility, integrity, and security evidence where those concerns apply to each published artifact.
- [ ] **GOV.18.04** Record immutable artifact hashes or equivalent verified identities, enabling a reviewer to distinguish the deployed dossier and rule contents from later working copies or withdrawn revisions.
- [ ] **GOV.18.05** Define handling for missing dependencies, revoked media, stale facts, and superseded rules, including blocked publication, qualified availability, and attributable replacement without silently changing campaign history.
- [ ] **GOV.18.06** Exercise traceability from a displayed metric or story consequence back to committed source revisions and reviewed rules, verifying a complete explanation without reliance on transient browser state.
- [ ] **GOV.18.07** Perform reverse-impact review from a corrected source or rule revision to affected dossiers, credits, tests, and releases, recording remediation decisions and retained historical interpretation.
- [ ] **GOV.18.08** Approve manifest completeness and sampled bidirectional trace results as release evidence, rejecting artifacts that lack required sources, accountable review, pinned dependencies, or reproducible publication identity.

### Control GOV 19

**Original requirement GOV.19:** Maintain a risk and limitation register covering misleading imagery, outdated information, duplicate credit, lost activity, inaccessible interactions, and unauthorized training changes, with concrete mitigations and owners.

- [ ] **GOV.19.01** Create risk records with stable IDs, concrete failure scenario, affected data or user outcome, likelihood basis, impact, owner, mitigation, verification evidence, and residual limitation.
- [ ] **GOV.19.02** Assess misleading imagery and outdated geographic information, assigning labeling, source-date review, withdrawal, and contextual fallbacks to identifiable content owners and publication checks for affected artifacts.
- [ ] **GOV.19.03** Analyze duplicate-credit scenarios involving retries, multiple sources, stale tabs, and lost responses, linking each to uniqueness constraints, source arbitration, and ledger reconciliation evidence for release acceptance.
- [ ] **GOV.19.04** Document lost-activity risks from write failures, disk exhaustion, interrupted sessions, and service termination, identifying durable checkpoints, unknown-gap reconciliation, and visibly unsaved recovery artifacts as mitigations.
- [ ] **GOV.19.05** Assess inaccessible interaction risks across scheduling, walking controls, decisions, and charts, defining equivalent keyboard or textual paths and review evidence for each essential participation operation.
- [ ] **GOV.19.06** Record unauthorized training-change risks from narrative rules, imports, proposed plans, and retrospective edits, assigning target-origin validation and explicit acceptance controls to responsible implementation and training reviewers.
- [ ] **GOV.19.07** Review combined failures and residual limitations during pilot scenarios, updating risk status from observed evidence rather than claiming elimination based solely on an implemented mitigation feature.
- [ ] **GOV.19.08** Approve unresolved risks and time-bounded exceptions with owners and revisit triggers; block release for risks whose missing mitigations violate authoritative accounting or the physical-training boundary.

### Control GOV 20

**Original requirement GOV.20:** Define the pilot and production scope, deferred functionality, support owner, release gates, rollback authority, and user data export path.

- [ ] **GOV.20.01** Define pilot participants, supported hardware, content subset, enabled progression modes, and expected support period, documenting how pilot scope differs from the production release baseline requirements.
- [ ] **GOV.20.02** List deferred features with user-visible implications, applicability rationale, dependency assumptions, and reconsideration triggers so incomplete optional work cannot be mistaken for a verified production capability.
- [ ] **GOV.20.03** Name the support owner and escalation route for launch failures, corrupted dossiers, activity corrections, privacy requests, and inaccessible interactions, including availability expectations and diagnostic boundaries.
- [ ] **GOV.20.04** Establish release gates tied to verified integrity, training separation, source review, accessibility, recovery exercises, and unresolved-risk acceptance for the exact application and content versions being deployed.
- [ ] **GOV.20.05** Assign rollback authority and define rollback triggers, compatible database handling, preserved user state, artifact reconciliation, and communication responsibilities when a released version fails an essential requirement.
- [ ] **GOV.20.06** Document the user data export path, supported formats, included record definitions, optional sensitive detail, and instructions for retrieving committed history without a mandatory cloud account.
- [ ] **GOV.20.07** Conduct a pilot exit review using observed defects, support cases, budget measurements, and user interpretation evidence, recording whether scope expansion satisfies the production gates or requires remediation.
- [ ] **GOV.20.08** Approve the scope manifest, gate results, support plan, rollback exercise, and export evidence before production designation, retaining the accountable decision and all accepted deployment limitations.

## C01 Route and stage planner

**Accountable owners:** Route-data owner for geographic integrity; itinerary-product owner for stage design. A publishing reviewer approves unresolved anomalies and migration decisions.

**Interfaces:** Consumes source route geometry, elevation inputs, landmark records, itinerary preferences, and saved campaign route positions from authoritative repository-local SQLite storage. Produces immutable `RouteRelease`, `RouteSegment`, `RoutePosition`, `StagePlan`, and `ItineraryVersion` records for the local dossier service, maps, events, and campaign progression. It supplies geography; the training planner owns physical assignments.

**Required evidence:** Schema definitions; source manifest; original-input checksums; processing configuration; topology and elevation validation reports; stage-boundary report; reproducibility example; migration rehearsal; reviewed exception register.

**Exit criterion:** Every released stage resolves to an immutable route position and saved campaign origin, joins its itinerary without unexplained gaps or duplicate credit, and survives revision/recovery tests. Repeated launch resumes an unfinished stage; only explicit day completion advances the next leg. No itinerary output can silently alter a physical training assignment.

### Control C01 01

**Original requirement C01.01:** Publish versioned schemas, required fields, coordinate/unit conventions, stable identifiers, validation rules, and compatibility policies for all route and itinerary records.

- [ ] **C01.01.01** Enumerate RouteRelease, RouteSegment, RoutePosition, StagePlan, and ItineraryVersion fields with types, requiredness, identifiers, references, and explicit unknown-value representations for reviewers.
- [ ] **C01.01.02** Specify coordinate ordering, canonical distance units, numeric precision, direction encoding, and chainage origin; include accepted examples for each record family.
- [ ] **C01.01.03** Implement schema validation at route import and stage publication boundaries; reject unrecognized versions before creating authoritative route or campaign records.
- [ ] **C01.01.04** Define additive versus breaking schema changes, supported reader versions, and migration ownership; preserve previously published route identifiers through every supported migration.
- [ ] **C01.01.05** Exercise missing identifiers, null required coordinates, invalid direction values, out-of-range chainage, and incompatible versions; verify each rejection names the offending field.
- [ ] **C01.01.06** Round-trip representative route and itinerary records through serialization and SQLite persistence; assert identities, references, precision, and declared unknown values remain unchanged.
- [ ] **C01.01.07** Interrupt an import containing mixed valid and invalid records; verify no partially accepted route release becomes selectable by itinerary generation.
- [ ] **C01.01.08** Archive schema versions, compatibility matrix, validation fixtures, rejection results, and reviewer approval; require complete field coverage and zero unresolved identity ambiguities.

### Control C01 02

**Original requirement C01.02:** Retain the source organization, original release identifier, retrieval time, source URL, original checksum, license, attribution requirements, and processing history for each imported dataset.

- [ ] **C01.02.01** Define an import manifest containing publisher, original release ID, retrieval timestamp, source URL, original checksum, license, attribution, and processing-step references.
- [ ] **C01.02.02** Capture provenance before transforming geometry; retain the acquired original beneath an approved repository root and link it to the manifest.
- [ ] **C01.02.03** Compute the original checksum independently from processed-data checksums; verify identical acquired bytes produce identical recorded digests across repeated local imports.
- [ ] **C01.02.04** Record each filtering, transformation, segmentation, and elevation enrichment step with executable version, parameters, input checksum, output checksum, operator, and timestamp.
- [ ] **C01.02.05** Reject publication when source identity, usable permission evidence, original checksum, or attribution obligations are missing; preserve incomplete imports for documented review.
- [ ] **C01.02.06** Test redirected sources, unavailable source pages, identical releases under different filenames, and changed bytes under reused release names; prohibit silent provenance replacement.
- [ ] **C01.02.07** Reconstruct one published route from retained inputs and processing records; compare the resulting geometry and checksum against the approved release manifest.
- [ ] **C01.02.08** Retain a reviewed provenance reconciliation listing every imported dataset; accept only when all published segments resolve to complete, attributable source manifests.

### Control C01 03

**Original requirement C01.03:** Declare horizontal coordinate reference systems, distance conventions, elevation units, vertical datum when known, transformation methods, and precision; represent unknown metadata explicitly.

- [ ] **C01.03.01** Specify horizontal reference-system identifier, axis order, distance convention, elevation unit, vertical datum status, transformation pipeline, and declared coordinate precision per dataset.
- [ ] **C01.03.02** Represent unknown reference metadata explicitly; distinguish unavailable vertical datum from a known datum and prohibit inferred labels based solely on filenames.
- [ ] **C01.03.03** Validate imported coordinates against their declared reference system and expected geographic extent before any distance, elevation, or route-position calculation proceeds.
- [ ] **C01.03.04** Record transformation libraries, grid dependencies, parameters, precision limits, and source/output reference systems; pin these inputs to the processed route release.
- [ ] **C01.03.05** Compare transformed control points and independently calculated sample distances with declared tolerances; retain coordinate, unit, and residual values for reviewer inspection.
- [ ] **C01.03.06** Exercise swapped axes, incorrect unit declarations, unavailable transformation resources, and unsupported datums; block affected calculations rather than silently using fallback coordinates.
- [ ] **C01.03.07** Display permitted uncertainty or unavailable-elevation labels consistently in stage maps and profiles; ensure unknown metadata does not appear as zero elevation.
- [ ] **C01.03.08** Archive the reference-system review and conversion residual report; require every published dataset to have an approved convention or explicitly accepted limitation.

### Control C01 04

**Original requirement C01.04:** Reference locations by immutable route release, segment identifier, direction, and chainage; persist the campaign's completed endpoint and pending next-leg origin in local SQLite, with names and displayed mileage outside the primary identity.

- [ ] **C01.04.01** Define immutable route-position keys from route release, segment, direction, and chainage; keep landmark names and formatted mileage as separate display attributes.
- [ ] **C01.04.02** Create SQLite foreign keys and range constraints linking completed endpoints and pending next-leg origins to the pinned route release and segment.
- [ ] **C01.04.03** Specify precision and equality rules for chainage comparisons so adjacent-stage joins remain stable despite display rounding or alternative unit preferences.
- [ ] **C01.04.04** Restrict continuation-pointer writes to validated completion or audited migration services; route labels, browser cache, and launcher configuration cannot authorize position changes.
- [ ] **C01.04.05** Load a saved endpoint after repository restart and reconstruct its geometry independently; verify resolved coordinates and direction match the original persisted identity.
- [ ] **C01.04.06** Rename landmarks and switch mileage display units without migration; assert saved route-position keys and generated next-stage origins remain byte-for-byte equivalent.
- [ ] **C01.04.07** Reject missing segments, incompatible route releases, negative chainage, and beyond-end positions; preserve the prior continuation pointer after every failed update.
- [ ] **C01.04.08** Retain database constraint results and restart evidence; accept only when all completed endpoints and pending origins resolve without reliance on displayed names.

### Control C01 05

**Original requirement C01.05:** Model route topology explicitly, including main route, alternates, junctions, connectors, termini, and discontinuities; maintain direction-aware adjacency relationships.

- [ ] **C01.05.01** Model directed topology nodes and edges for main route, alternate routes, connectors, junctions, termini, and documented discontinuities with stable release-bound identifiers.
- [ ] **C01.05.02** Specify entry and exit positions, permitted travel directions, junction membership, and alternate rejoining rules; distinguish geometric intersections from traversable connections.
- [ ] **C01.05.03** Persist adjacency with referential integrity; require every selectable transition to resolve to known route positions within the same compatible release.
- [ ] **C01.05.04** Validate that each declared terminus has the expected incoming/outgoing adjacency and that internal segments do not become accidental disconnected components.
- [ ] **C01.05.05** Generate stages crossing a connector and rejoining an alternate; verify traversal follows declared edges and contains no invented straight-line connection.
- [ ] **C01.05.06** Exercise reverse traversal, one-way restrictions, ambiguous multi-edge junctions, missing connectors, and disconnected alternates; require explicit selection or a blocking topology error.
- [ ] **C01.05.07** Recover from an interrupted topology import by retaining the previously approved graph; incomplete adjacency records must never enter the selectable release.
- [ ] **C01.05.08** Publish a reviewed topology graph and reachability report; accept only when every itinerary transition is connected or carries an explicit transfer/discontinuity record.

### Control C01 06

**Original requirement C01.06:** Validate geometry for gaps, duplicates, incorrect direction, ambiguous junctions, unintended intersections, and implausible endpoints; record reviewed exceptions and their consequences.

- [ ] **C01.06.01** Define geometry validation thresholds for endpoint separation, duplicate vertices, reversed orientation, intersection ambiguity, and source-appropriate implausible lengths before processing begins.
- [ ] **C01.06.02** Run validation against original and processed geometry; retain offending segment IDs, coordinates, measured values, threshold versions, and diagnostic map references.
- [ ] **C01.06.03** Distinguish legitimate switchbacks and grade-separated crossings from accidental topology joins; require geographic review before converting any detected intersection into adjacency.
- [ ] **C01.06.04** Create an exception record for each accepted anomaly stating rationale, affected stages, confidence, consequence, owner, reviewer, and required visible limitation.
- [ ] **C01.06.05** Seed fixtures with gaps, duplicates, reversed segments, ambiguous junctions, unintended crossings, and displaced termini; verify each validator detects its intended defect.
- [ ] **C01.06.06** Verify clean reference geometry passes without manufacturing exceptions; compare flagged counts and classifications against an independently reviewed anomaly inventory for the release.
- [ ] **C01.06.07** On validation interruption or unavailable reference inputs, keep the release unpublished; resume against the same checksummed inputs rather than mixing partially reviewed results.
- [ ] **C01.06.08** Archive diagnostic geometry, reviewer dispositions, and corrected outputs; require zero unexplained blocking anomalies and complete traceability for every retained geographic exception.

### Control C01 07

**Original requirement C01.07:** Enforce stage-boundary invariants: adjacent stages share a route position; gaps, repeats, skips, and transfers require explicit records; credited distance must not double-count overlapping geometry.

- [ ] **C01.07.01** Define stage start/end identity, adjacency equality, overlap accounting, transfer type, skip reason, and explicit gap/repeat records in the stage-plan schema.
- [ ] **C01.07.02** Calculate credited route distance from directed traversed intervals rather than summing display distances; identify duplicate intervals shared across stages and alternate paths.
- [ ] **C01.07.03** Enforce adjacent-stage endpoint matching during itinerary publication; require a typed transition record whenever the next origin differs from the previous endpoint.
- [ ] **C01.07.04** Specify intentional revisits separately from first-pass credit; document whether repeated geometry contributes narrative distance while retaining unique eligible progression accounting.
- [ ] **C01.07.05** Construct contiguous, overlapping, zero-length, skipped, and transferred itineraries; independently reconcile their traversed intervals and expected credited distances across stage boundaries.
- [ ] **C01.07.06** Reject unexplained discontinuities and accidental duplicate coverage; verify failed itinerary publication leaves the previously selected itinerary and campaign continuation pointer unchanged.
- [ ] **C01.07.07** Exercise stage splitting and merging at rounded chainages; confirm shared positions remain exact and no fractional distance is lost or credited twice.
- [ ] **C01.07.08** Publish a stage-boundary ledger and interval reconciliation; accept only when every discontinuity is explained and aggregate credited distance matches independently expected coverage.

### Control C01 08

**Original requirement C01.08:** Version elevation sampling, smoothing, ascent, descent, grade, and distance calculations; retain input resolution and uncertainty, and flag unresolved artifacts.

- [ ] **C01.08.01** Specify elevation input resolution, sampling interval, smoothing parameters, ascent/descent rules, grade denominator, distance method, and uncertainty fields with explicit calculation versions.
- [ ] **C01.08.02** Retain source elevation samples and processing configuration separately from derived profiles; link each stage statistic to immutable input and algorithm identifiers.
- [ ] **C01.08.03** Define handling for missing samples, flat sections, spikes, duplicated coordinates, short segments, and undefined grade; distinguish unknown values from genuine zero measurements.
- [ ] **C01.08.04** Validate unit conversion and direction changes before aggregation; preserve canonical quantities while documenting rounding rules used in maps, profiles, and stage summaries.
- [ ] **C01.08.05** Compare ascent, descent, grade, and distance on independently calculated synthetic profiles containing flat, ascending, descending, and alternating sections within declared tolerances.
- [ ] **C01.08.06** Inject sampling gaps and extreme spikes; verify flagged artifacts cannot silently generate confident stage difficulty statements or alter approved physical training assignments.
- [ ] **C01.08.07** Recompute a published profile after restart from pinned inputs; require identical derived values or a documented numeric tolerance with reproducibility evidence.
- [ ] **C01.08.08** Archive calculation fixtures, uncertainty review, and artifact dispositions; accept only when every displayed terrain statistic identifies its derivation and unresolved limitations.

### Control C01 09

**Original requirement C01.09:** Associate landmarks with route positions, geographic confidence, source references, stage relevance, and visibility relationships; distinguish an on-route feature from a distant view.

- [ ] **C01.09.01** Define landmark records with route-position references, feature identity, source assertions, geographic confidence, stage relevance, viewing relationship, and optional distance/bearing metadata.
- [ ] **C01.09.02** Distinguish on-route landmarks, nearby features, and distant visible features; require a reviewed association category before inclusion in any stage dossier.
- [ ] **C01.09.03** Validate route-release compatibility, chainage bounds, source references, and direction-dependent landmark order when importing or assigning landmarks to itinerary stages locally.
- [ ] **C01.09.04** Record viewing evidence and visibility limitations; do not infer that a feature is visible merely because its coordinates lie near the route.
- [ ] **C01.09.05** Test a stage with on-route and distant landmarks; confirm captions, map symbols, and ordering communicate each relationship without implying a physical visit.
- [ ] **C01.09.06** Reject orphaned positions and conflicting location claims; route an uncertain association into review with its competing evidence rather than choosing a convenient location.
- [ ] **C01.09.07** Revise a landmark name or confidence assessment; preserve published historical associations and expose the approved correction through versioned dependencies and annotations.
- [ ] **C01.09.08** Retain a reviewed landmark-association sample and coverage report; require all displayed landmarks to resolve to supported positions and explicit viewing classifications.

### Control C01 10

**Original requirement C01.10:** Model stopping locations with provenance and applicability dates; distinguish a fictional narrative destination from a verified real-world campsite or facility.

- [ ] **C01.10.01** Define stopping-location identity, geographic position, source evidence, applicability dates, facility/campsite classification, fictional status, and unresolved availability attributes in the content schema.
- [ ] **C01.10.02** Separate verified location attributes from authored destination names and scenario-specific availability; identify which fields are factual, fictional, dated, or unknown.
- [ ] **C01.10.03** Require geographic and editorial approval before describing a stop as a real campsite or facility; absence of evidence cannot become implied verification.
- [ ] **C01.10.04** Specify expiry and correction behavior for dated stopping information; prevent stale applicability records from entering newly published dossiers without a reviewed limitation.
- [ ] **C01.10.05** Inspect real, fictional, historically documented, and unknown stops; verify their captions and explanations identify category and date wherever the distinction affects interpretation.
- [ ] **C01.10.06** Exercise unavailable facilities, unsupported campsite claims, missing dates, and conflicting sources; provide a clearly labeled narrative substitute or block misleading destination publication.
- [ ] **C01.10.07** Apply a stop correction to an unfinished campaign through the approved workflow; preserve completed destinations and add traceable annotations rather than rewriting history.
- [ ] **C01.10.08** Archive stopping-location reviews and display examples; accept only when every released destination has complete provenance or an explicit, visibly fictional classification.

### Control C01 11

**Original requirement C01.11:** Generate the next stage from the saved next-leg origin, route release, and explicit itinerary inputs; persist the algorithm version and reproducibility inputs, and resume an unfinished stage instead of generating another on launch.

- [ ] **C01.11.01** Specify stage-generation inputs comprising campaign/day reservation, committed origin, pinned route release, direction, itinerary preferences, algorithm version, and deterministic seed where applicable.
- [ ] **C01.11.02** Read authoritative continuation state inside the reservation operation; never derive the origin from browser preferences, current date, displayed mileage, or launch count.
- [ ] **C01.11.03** Persist a unique generation job and complete input snapshot before producing stage geometry; bind every generated artifact to the reserved campaign/day identity.
- [ ] **C01.11.04** On later launch, query for an unfinished stage first and reuse its saved plan; create another reservation only when continuation rules permit it.
- [ ] **C01.11.05** Generate the same reserved day twice with identical inputs; compare origin, endpoint, stage geometry, algorithm metadata, and dependency references for reproducible equality.
- [ ] **C01.11.06** Change preferences after reservation and attempt adoption; reject mismatched inputs unless an explicit revision operation records the change and preserves established history.
- [ ] **C01.11.07** Interrupt generation after reservation and restart through the launcher; resume the same job or documented failed state without consuming another expedition day.
- [ ] **C01.11.08** Retain reproducibility and relaunch traces; accept only when every generated stage identifies committed origin inputs and all unfinished-stage launches preserve day identity.

### Control C01 12

**Original requirement C01.12:** Keep fictional stage distance independent of actual workout requirements; prevent itinerary generation, route difficulty, or narrative consequences from escalating physical assignments.

- [ ] **C01.12.01** Define distinct fields and units for fictional stage distance and physical assignment targets; prohibit shared writable quantities that could couple their meanings.
- [ ] **C01.12.02** Document the route planner's output contract as geographic/narrative data only; grant physical-target mutation authority exclusively to the accepted training-plan change operation.
- [ ] **C01.12.03** Inspect difficulty labels, elevation profiles, and stage descriptions for wording that implies mandatory matching exertion; revise ambiguous instructions before editorial approval.
- [ ] **C01.12.04** Create long, steep, flat, shortened, and alternate stages against one accepted assignment; verify physical duration, distance, and equipment prompts remain unchanged.
- [ ] **C01.12.05** Inject itinerary rules requesting increased incline or compensatory distance; reject unsupported effects and retain the offending rule identity in diagnostic evidence.
- [ ] **C01.12.06** Test narrative setbacks and route substitutions after partial activity; preserve recorded workout quantities and assignment criteria despite changed fictional destination or route difficulty.
- [ ] **C01.12.07** Recover an interrupted itinerary revision and compare training snapshots before and after; no failed or successful route operation may silently rewrite physical targets.
- [ ] **C01.12.08** Archive interface access review and boundary-test results; accept only when all route-driven changes preserve physical assignments unless separately accepted by the user.

### Control C01 13

**Original requirement C01.13:** Handle northbound and southbound traversal consistently, including landmark order, ascent/descent inversion, stage endpoints, and alternate-entry/exit positions.

- [ ] **C01.13.01** Specify direction-dependent chainage interpretation, ordered landmarks, endpoint orientation, alternate-entry/exit mapping, and ascent/descent derivation for both northbound and southbound traversal modes.
- [ ] **C01.13.02** Resolve each itinerary direction through the same canonical geometry and explicit directed topology; avoid maintaining independently drifting copies of reversed route facts.
- [ ] **C01.13.03** Generate matched forward and reverse stages over identical geometry; confirm endpoint exchange, reversed landmark order, equal distance, and exchanged ascent/descent within tolerance.
- [ ] **C01.13.04** Exercise alternate entry and rejoin points in both directions; verify selected connectors remain reachable and no reverse transition bypasses declared adjacency restrictions.
- [ ] **C01.13.05** Test stages beginning exactly at junctions, termini, or repeated landmark positions; require deterministic ordering with documented tie rules and no duplicated feature records.
- [ ] **C01.13.06** Reject an unsupported reverse alternate with a specific route limitation; preserve the campaign's saved origin and allow selection of a reviewed supported path.
- [ ] **C01.13.07** Restart a southbound unfinished day and inspect generated dossier references; ensure neither launcher defaults nor display sorting silently restores northbound interpretations.
- [ ] **C01.13.08** Archive bidirectional geometry and topology comparisons; accept only when every supported direction has complete endpoint, landmark, terrain, and alternate-transition verification evidence.

### Control C01 14

**Original requirement C01.14:** Keep hypothetical weather, resource availability, and authored obstacles outside canonical route facts; link scenarios to route versions and disclose their assumptions.

- [ ] **C01.14.01** Define separate scenario-condition records for hypothetical weather, resource availability, and obstacles; reference route versions without adding those conditions to canonical geometry.
- [ ] **C01.14.02** Require each scenario condition to carry authored assumption text, temporal context, provenance classification, applicable stage range, and responsible content revision identifiers.
- [ ] **C01.14.03** Expose assumption labels alongside maps, obstacle choices, and availability descriptions; verify users can distinguish scenario conditions from source-backed permanent route attributes.
- [ ] **C01.14.04** Restrict route-data services from persisting event effects as route facts; fictional depletion, closures, or storms may update only the authorized campaign scenario domain.
- [ ] **C01.14.05** Run one route release under two contrasting scenario sets; compare canonical segments, landmarks, elevation, and positions for identical values despite different narrative outcomes.
- [ ] **C01.14.06** Exercise missing assumption labels, expired observations, and ambiguous current-weather wording; block misleading publication or replace it with an explicit hypothetical presentation.
- [ ] **C01.14.07** Correct a scenario assumption after publication; preserve the route release and completed scenario history while applying approved, versioned corrections to affected unfinished content.
- [ ] **C01.14.08** Retain route/scenario separation results and editorial samples; accept only when every condition affecting a choice has an identifiable classification and disclosed assumption.

### Control C01 15

**Original requirement C01.15:** Provide an editing preview showing continuity, distance changes, missing dossiers, displaced landmarks, and effects on published content before accepting an itinerary revision.

- [ ] **C01.15.01** Define itinerary-preview output listing changed positions, discontinuities, distance deltas, landmark displacement, missing dossiers, and affected published dependencies before any revision commitment.
- [ ] **C01.15.02** Run proposed edits against a copy of pinned itinerary and campaign references; prevent preview generation from modifying authoritative stages or continuation state.
- [ ] **C01.15.03** Present previous and proposed start/end identities, algorithm inputs, and derived distances; identify skipped or duplicated geometry through explicit interval comparisons and warnings.
- [ ] **C01.15.04** Calculate displaced landmark and dossier coverage impacts across every affected stage; flag dependencies needing revision rather than silently reassociating previously published materials.
- [ ] **C01.15.05** Preview stage split, merge, alternate substitution, deletion, and direction change; independently verify reported continuity and distance effects against expected reference itineraries.
- [ ] **C01.15.06** Attempt commitment with unresolved blocking gaps or missing required dossiers; reject it and retain the original itinerary selection with actionable issue references.
- [ ] **C01.15.07** Interrupt preview or cancel approval after review; verify no reservation, completion, or next-leg update occurred and the proposal remains recoverable or explicitly discarded.
- [ ] **C01.15.08** Archive approved previews with reviewer decisions and revision IDs; accept only when committed edits match the inspected proposal and all blocking impacts are resolved.

### Control C01 16

**Original requirement C01.16:** Preserve completed campaign stages against route updates; migrate saved local positions through an explicit audited operation. Advance the next-leg origin only when the current day is explicitly completed, never because a launcher ran or a browser opened.

- [ ] **C01.16.01** Define immutable completed-stage records and a migration request containing old/new route positions, mapping evidence, affected pending stages, reason, actor, and expected revision.
- [ ] **C01.16.02** Restrict next-leg advancement to explicit complete-day transactions; launcher start, page opening, midnight, browser refresh, and service shutdown lack continuation-write authority.
- [ ] **C01.16.03** Map saved positions into a new release through an inspected preview; require unresolved segment or chainage ambiguity to block migration rather than guess mileage.
- [ ] **C01.16.04** Preserve completed geometry, dossier references, route release, and causal history; record migrated continuation as a separate attributable operation with reversible mapping evidence.
- [ ] **C01.16.05** Exercise route revision before and after completion; verify only approved migration changes saved pending positions while completed-stage snapshots retain original references.
- [ ] **C01.16.06** Repeat complete-day submission and simulate a stale-tab completion; assert one completion result, one pointer advance, and rejection of superseded source-day identities.
- [ ] **C01.16.07** Interrupt the migration or completion transaction; restart and require either the original coherent pointer or the fully committed new position, never a partial mixture.
- [ ] **C01.16.08** Archive migration rehearsal and launch-versus-completion evidence; accept only when all pointer changes have an authorized completion or audited migration cause with preserved history.

### Control C01 17

**Original requirement C01.17:** Make generation idempotent by campaign/day identifier and bind outputs to the saved starting position; use local SQLite transactions and atomic snapshot publication so interruptions or concurrent launches cannot expose duplicate or partial stages.

- [ ] **C01.17.01** Create unique campaign/day stage-generation identities and persist starting-position fingerprints, algorithm inputs, job state, and artifact manifests under enforced SQLite uniqueness constraints.
- [ ] **C01.17.02** Reserve generation work transactionally against the expected campaign revision; competing launches must receive the same reservation or an explicit recoverable contention response.
- [ ] **C01.17.03** Write stage files into job-specific staging directories, validate dependencies and checksums, then rename verified artifacts on the same volume before recording publication readiness.
- [ ] **C01.17.04** Specify reconciliation for staged-only files, renamed artifacts without markers, markers with missing files, and abandoned jobs; filesystem publication remains separate from database transactions.
- [ ] **C01.17.05** Launch simultaneous generation requests for one day; verify one authoritative stage, one approved artifact identity, and consistent origin binding across all returned responses.
- [ ] **C01.17.06** Crash at reservation, write, validation, rename, and marker boundaries; restart and verify no partial stage becomes ready or increments the next-leg pointer.
- [ ] **C01.17.07** Submit repeated requests with changed origins or pinned inputs; reject incompatible adoption and retain the original reservation plus a traceable conflict explanation.
- [ ] **C01.17.08** Archive concurrency and crash-boundary results with artifact/database reconciliation; accept only when every recovery produces one coherent stage or an explicit nonready failure.

### Control C01 18

**Original requirement C01.18:** Define handling for missing geometry, unavailable elevation, unsupported alternates, and uncertain landmarks; block structurally invalid stages and visibly label permitted fidelity reductions.

- [ ] **C01.18.01** Define fidelity tiers and blocking conditions for missing geometry, elevation absence, unsupported alternates, uncertain landmarks, and incomplete topology with responsible review owners.
- [ ] **C01.18.02** Require complete connected geometry and valid route positions for structural acceptance; informational degradation cannot authorize an invented segment or guessed continuation endpoint.
- [ ] **C01.18.03** Specify permitted elevation omission and landmark uncertainty displays; preserve unknown quantities and disclose the missing evidence beside affected maps, profiles, and dossier sections.
- [ ] **C01.18.04** Implement generation responses identifying each unavailable dependency, permitted fallback, and blocked output; ensure callers distinguish degraded-ready stages from structurally invalid stages.
- [ ] **C01.18.05** Generate fixtures with missing elevation and uncertain landmarks; verify approved stages retain real geometry, visible limitations, and no fabricated terrain or feature claims.
- [ ] **C01.18.06** Exercise disconnected geometry and unsupported alternate selections; block publication while preserving the reservation and provide a reviewed reconfiguration or repair path.
- [ ] **C01.18.07** Restore dependencies after failure and retry the same reservation; verify the repaired stage retains its original campaign/day identity and records the new validated input revision.
- [ ] **C01.18.08** Archive degradation-policy reviews and fixture results; accept only when every reduced-fidelity output is labeled and all structurally invalid route plans remain unpublished.

### Control C01 19

**Original requirement C01.19:** Verify direction reversal, alternates, zero-length/overlapping stages, skipped sections, route revision, interrupted generation, repeated launches, completion retry, and restart from saved unfinished or completed positions.

- [ ] **C01.19.01** Create a route-planner verification matrix covering both directions, alternates, zero-length stages, overlap, skips, revisions, interrupted generation, repeated launches, and completion retries.
- [ ] **C01.19.02** Specify independent expected route positions, traversed intervals, credited distance, dossier identity, and continuation state for every case before executing implementation verification.
- [ ] **C01.19.03** Exercise saved unfinished and completed campaigns through the actual CMD/PowerShell startup flow; compare selected day and stage origin with authoritative database expectations.
- [ ] **C01.19.04** Run reverse and alternate paths across reviewed topology fixtures; verify endpoint ordering, rejoin continuity, swapped terrain metrics, and absence of unexplained distance duplication.
- [ ] **C01.19.05** Inject interruptions and concurrent generation around SQLite and artifact boundaries; reconcile reservations, ready manifests, staging remnants, and pointer state after every restart.
- [ ] **C01.19.06** Repeat and lose completion acknowledgments; verify idempotent completion preserves one causal record and advances the pointer exactly once from the intended source day.
- [ ] **C01.19.07** Record observed failures with reproducible inputs and responsible owners; rerun affected cases after correction and preserve both original failure and confirming evidence.
- [ ] **C01.19.08** Archive a signed or attributable verification matrix; accept only when every listed scenario passes or has an explicitly approved, bounded release exception.

### Control C01 20

**Original requirement C01.20:** Produce a reviewed geographic coverage report and stage-continuity report for every published itinerary; link each unresolved exception to an owner and disposition.

- [ ] **C01.20.01** Define report schemas for geographic coverage, stage continuity, source versions, missing dependencies, overlap intervals, direction support, and unresolved exception ownership per published itinerary.
- [ ] **C01.20.02** Generate reports from the exact immutable itinerary and route manifests selected for publication; include checksums so reviewers can detect stale or mismatched report inputs.
- [ ] **C01.20.03** Reconcile stage start/end joins and total credited intervals independently; identify every gap, repeat, skipped section, transfer, and uncertain landmark with stable identifiers.
- [ ] **C01.20.04** Quantify coverage by region, stage, route branch, and fidelity tier; distinguish authored availability from verified geographic completeness instead of claiming blanket trail coverage.
- [ ] **C01.20.05** Require geographic reviewers to inspect anomalous positions and coverage omissions; record disposition, user-visible consequences, remediation owner, and revisit trigger for each retained exception.
- [ ] **C01.20.06** Deliberately introduce one missing stage and one overlapping interval; verify report generation detects both and blocks unreviewed publication under the selected release gates.
- [ ] **C01.20.07** Regenerate reports after approved itinerary revision; preserve previous reports with their release and confirm new reports do not erase historical exception decisions.
- [ ] **C01.20.08** Archive approved coverage and continuity reports beside release manifests; accept only when every published itinerary has matching reports and zero unowned unresolved exceptions.

## C02 Daily dossier publishing system

**Accountable owners:** Dossier editor for completeness and narrative quality; factual reviewers for relevant claims; technical publisher for release integrity. Author, reviewer, approver, publisher, and correction responsibilities must be assigned, although a small team may combine roles.

**Interfaces:** Consumes approved stage plans, media assets, learning activities, training-assignment references, event definitions, and authoritative repository-local SQLite campaign state. Produces immutable versioned `DayDossier` snapshots and local package manifests served by the PowerShell-started local service at `http://127.0.0.1:<port>`. Browser state is a client cache; persistent progress belongs to the local service.

**Required evidence:** Dossier schema; SQLite day/publication schema; template specification; authored sample days; assertion-to-source links; approval history; local path/dependency manifests; staged-file/rename/publication-marker reconciliation results; launch-versus-completion tests; accessibility review; correction and rollback rehearsal.

**Exit criterion:** The local service can generate, serve, resume, explicitly complete, and revisit a day with consistent facts, assets, training references, and branch history. Later launcher runs resume unfinished snapshots or use the saved completed endpoint for the next leg. Partial publication, optional missing content, and corrections cannot corrupt actual training or completed-day records.

### Control C02 01

**Original requirement C02.01:** Define required dossier fields for stage identity, introduction, gallery, map, elevation, training reference, morning decision, encounters, lesson, camp debrief, and next-stage preview.

- [ ] **C02.01.01** Specify dossier fields, types, requiredness, ordering, and references for stage identity, introduction, gallery, map, elevation, assignment, morning decision, encounters, lesson, debrief, and preview.
- [ ] **C02.01.02** Define minimum content and empty-state rules for each section; distinguish intentionally absent optional content from missing required records or unresolved placeholders.
- [ ] **C02.01.03** Implement template validation against the dossier schema before rendering; require stage and assignment references to resolve to their pinned authoritative record versions.
- [ ] **C02.01.04** Specify text equivalents and descriptive summaries for map/elevation sections so required information remains available when graphical dependencies are absent or inaccessible.
- [ ] **C02.01.05** Render complete, minimal, recovery-day, and partial-session dossiers; confirm every required section appears with its intended data source and correctly labeled optional omissions.
- [ ] **C02.01.06** Submit missing stage identities, empty required lessons, broken encounter references, and invalid preview shapes; reject publication with section-specific messages and retained validation results.
- [ ] **C02.01.07** Interrupt section assembly and retry against the same reservation; verify no truncated dossier is marked ready or adopted as a complete daily snapshot.
- [ ] **C02.01.08** Archive the field contract, representative dossiers, and completeness results; accept only when every published dossier satisfies all applicable required-section checks without unresolved placeholders.

### Control C02 02

**Original requirement C02.02:** Associate factual assertions with evidence records; label fictional characters, encounters, hypothetical conditions, and interpretive content at the point where distinction matters.

- [ ] **C02.02.01** Define assertion records containing claim text, evidence references, classification, source date, applicability, reviewer, and locations where factual or fictional distinctions must appear.
- [ ] **C02.02.02** Attach each geographic or instructional factual assertion to supporting evidence; generated wording may not introduce unsupported claims absent from the approved assertion set.
- [ ] **C02.02.03** Specify labels for fictional characters, encounters, hypothetical conditions, and interpretation; require classification beside choices where omission could change the user's understanding.
- [ ] **C02.02.04** Review mixed paragraphs containing facts and narrative assumptions; split or annotate statements when a section-level label would conceal materially different evidence status.
- [ ] **C02.02.05** Inspect representative dossiers for assertion-to-source coverage; trace every sampled factual claim to the exact evidence supporting its expressed level of confidence.
- [ ] **C02.02.06** Seed unsupported claims and fictional weather written as current fact; verify editorial publication gates reject both while preserving corrected drafts for reviewed resubmission.
- [ ] **C02.02.07** Handle retired or corrected evidence by identifying dependent assertions and affected dossiers; apply approved annotations or withdrawal without silently replacing completed historical wording.
- [ ] **C02.02.08** Archive assertion mappings and classification display reviews; accept only when all released factual assertions are supported and all materially fictional content is visibly distinguished.

### Control C02 03

**Original requirement C02.03:** Pin local dossier snapshots to immutable route, media, lesson, event, and template versions; retain dependency manifests, checksums, and SQLite references to repository-relative snapshot/package paths.

- [ ] **C02.03.01** Define dependency manifests pinning route, media, lesson, event, and template identifiers, immutable revisions, checksums, package roots, and repository-relative snapshot paths.
- [ ] **C02.03.02** Create SQLite snapshot references that bind dossier identity to the approved manifest checksum; prohibit loose latest-version references inside published daily content.
- [ ] **C02.03.03** Validate dependency existence, revision compatibility, rights status, and checksums before packaging; reject any asset resolving outside configured repository-local publication roots.
- [ ] **C02.03.04** Specify how repeated launches locate the saved immutable package; browser caches and current catalog selections cannot substitute newer dependencies for pinned dossier inputs.
- [ ] **C02.03.05** Publish a dossier, update its source catalogs, and reopen it; verify all rendered dependencies retain original approved revisions unless an explicit correction applies.
- [ ] **C02.03.06** Exercise mismatched checksums, unavailable versions, escaping paths, and missing manifest entries; block ready status and identify the specific dependency requiring repair.
- [ ] **C02.03.07** Interrupt packaging between file creation and database association; reconcile against job identity and checksums before adopting or deleting any staged artifact.
- [ ] **C02.03.08** Archive manifest/file/database reconciliation results; accept only when every ready snapshot resolves to a complete validated dependency package using safe repository-relative references.

### Control C02 04

**Original requirement C02.04:** Persist campaign/day identifiers, saved route origin/endpoint, editorial state, locale, configuration, publication time, corrections, and replacement relationships in local SQLite; keep operational launch logs distinct from hike-day history.

- [ ] **C02.04.01** Define SQLite dossier/day metadata for campaign identity, reservation, route origin/endpoint, editorial state, locale, configuration, publication timestamps, correction lineage, and replacement relationships.
- [ ] **C02.04.02** Enforce unique campaign/day references and foreign keys to route positions and manifests; mutable editorial metadata cannot obscure the immutable published snapshot identity.
- [ ] **C02.04.03** Keep launch/run diagnostics in separate records from hike-day and completion history; associate them through references without interpreting invocation count as expedition progression.
- [ ] **C02.04.04** Record corrections and replacements as attributable relationships with reason and affected revision; preserve the prior published record rather than overwriting its established metadata.
- [ ] **C02.04.05** Persist and reload a published dossier after service restart; compare every identity, locale, configuration, route-position, and correction field against its original committed values.
- [ ] **C02.04.06** Reject orphaned campaigns, inconsistent endpoints, illegal replacement cycles, and duplicate day publication identities; retain coherent previous metadata after failed writes or stale requests.
- [ ] **C02.04.07** Simulate a launch-log failure after a ready dossier exists; preserve hike-day history and report the operational logging problem without fabricating or deleting completion records.
- [ ] **C02.04.08** Archive schema constraints and restart/correction evidence; accept only when dossier metadata is durable, lineage is acyclic, and launcher activity remains distinguishable from hike progression.

### Control C02 05

**Original requirement C02.05:** Define allowed personalization fields and their inputs; distinguish approved invariant content from fields assembled dynamically for a particular player.

- [ ] **C02.05.01** Inventory allowed personalization fields with source records, type/range constraints, rendering locations, consent or preference basis, and invariant-content boundaries for each dossier template.
- [ ] **C02.05.02** Specify approved assembly functions for player names, selected interests, branch history, and presentation preferences; identify which substitutions must be escaped or constrained.
- [ ] **C02.05.03** Restrict personalization from rewriting route facts, source attributions, scenario assumptions, physical targets, or previously approved learning explanations unless an explicit reviewed revision authorizes it.
- [ ] **C02.05.04** Validate supplied personalization before rendering; treat unavailable optional inputs as documented neutral defaults rather than inferred health, ability, identity, or readiness attributes.
- [ ] **C02.05.05** Render contrasting profiles against one invariant template; compare factual text, assignment references, evidence links, and mandatory explanations for identical approved content.
- [ ] **C02.05.06** Submit oversized names, markup payloads, missing interests, and unexpected personalization keys; verify safe rendering, clear rejection, or documented neutral fallback without schema drift.
- [ ] **C02.05.07** On failed assembly, preserve the reserved day and previous coherent snapshot; retry with the same validated inputs and record any explicit preference revision.
- [ ] **C02.05.08** Archive personalization field inventory and invariant comparisons; accept only when every dynamic field has an authorized input and all protected content remains intact.

### Control C02 06

**Original requirement C02.06:** Store real training date, fictional expedition day, scenario season/date, photo capture dates, and source freshness independently; handle timezone changes without renumbering expedition days.

- [ ] **C02.06.01** Define independent representations for real training timestamps, fictional expedition-day sequence, scenario season/date, image capture precision, and source acquisition/review freshness with explicit temporal semantics.
- [ ] **C02.06.02** Store named timezone and relevant offsets for actual timestamps; retain date-only and unknown capture-date values without inventing midnight timestamps or calendar precision.
- [ ] **C02.06.03** Bind expedition-day numbering to campaign records rather than computed real-date differences; scenario dates remain authored inputs independent of the computer's current clock.
- [ ] **C02.06.04** Specify display labels separating actual dates, fictional dates, historical photographs, and dated source observations wherever simultaneous presentation could imply contemporaneous conditions.
- [ ] **C02.06.05** Test midnight crossing, daylight-saving changes, manual clock shifts, timezone travel, and multi-date partial sessions; verify expedition numbering and pinned scenario context remain unchanged.
- [ ] **C02.06.06** Render unknown, year-only, month-only, and exact photo dates; ensure captions preserve precision and never imply those images depict the player's real session.
- [ ] **C02.06.07** Restart a dossier after timezone preference changes; reconstruct actual-date presentation while preserving stored timestamps, fictional day identity, source freshness, and historical publication context.
- [ ] **C02.06.08** Archive temporal fixtures and rendered examples; accept only when every displayed date is correctly classified and no clock/calendar event independently advances the expedition.

### Control C02 07

**Original requirement C02.07:** Implement explicit draft, review, approved, published, corrected, withdrawn, and archived transitions with role authorization, validation gates, and audit events.

- [ ] **C02.07.01** Specify allowed draft, review, approved, published, corrected, withdrawn, and archived transitions with actors, prerequisites, required evidence, and illegal-transition outcomes in a lifecycle table.
- [ ] **C02.07.02** Implement transition validation through the local service with expected revisions; grant publication and withdrawal authority only to configured responsible roles or documented combined-role ownership.
- [ ] **C02.07.03** Require review completion and publication validation before entering approved/published states; preserve reviewer identity, decisions, reasons, and exact content revision in audit events.
- [ ] **C02.07.04** Define corrected and replacement relationships without permitting edits to immutable published snapshots; archive prior revisions and retain their campaign references for historical review.
- [ ] **C02.07.05** Exercise every legal lifecycle transition and inspect state, revision, actor, timestamps, evidence references, and rendered availability against independently specified expected records.
- [ ] **C02.07.06** Attempt direct draft-to-published transitions, missing approvals, unauthorized withdrawals, and stale revisions; reject each request without modifying prior lifecycle state or publication pointers.
- [ ] **C02.07.07** Interrupt a lifecycle commit and repeat the request; require one durable transition event or an explicit failure with a recoverable retry path.
- [ ] **C02.07.08** Archive transition coverage and role-review evidence; accept only when all legal transitions are tested and no unsupported path bypasses required review or audit recording.

### Control C02 08

**Original requirement C02.08:** Validate publication completeness: required fields, evidence, available images, rights, alternative text, valid links, route continuity, reachable event branches, and resolved placeholders.

- [ ] **C02.08.01** Create a publication validator inventory for required fields, evidence coverage, local images, rights, alternative text, links, route joins, reachable branches, and unresolved placeholders.
- [ ] **C02.08.02** Specify blocking severity and permitted exception rules for each validator; record affected content IDs and the exact manifest version under examination.
- [ ] **C02.08.03** Run validators against assembled snapshots and bundled dependencies rather than drafts alone; verify packaged captions, rights, and links match the actual served files.
- [ ] **C02.08.04** Resolve external evidence links separately from required local dependencies; document when unavailable references require review while ensuring essential dossier operation remains internet-independent.
- [ ] **C02.08.05** Seed one defect in each validation category and execute the gate; confirm every blocking defect prevents ready publication with a specific actionable result.
- [ ] **C02.08.06** Publish a fully valid reference dossier and manually inspect its stage continuity and branch reachability; verify automated acceptance does not conceal semantic editorial defects.
- [ ] **C02.08.07** Interrupt validation or lose a dependency after approval; rerun integrity checks before readiness and refuse a stale validation receipt for changed package bytes.
- [ ] **C02.08.08** Archive validator configuration, seeded defects, manual review, and publication receipts; accept only when all applicable checks pass against the exact released package checksum.

### Control C02 09

**Original requirement C02.09:** Reference an independently maintained physical assignment; display actual completion criteria and the campaign progression rule without embedding hidden exercise changes in narrative prose.

- [ ] **C02.09.01** Define the dossier assignment reference contract with stable assignment ID, plan revision, actual completion rule, optional physical targets, and pinned progression-policy identity.
- [ ] **C02.09.02** Fetch assignment data from the independently maintained training model; render accepted values without deriving duration, distance, speed, or incline from stage narrative.
- [ ] **C02.09.03** Display real assignment criteria and fictional progression conversion separately with clear units; include partial, recovery, and preparation criteria when those modes are enabled.
- [ ] **C02.09.04** Review prose and branching explanations for hidden extra exercise instructions; reject story wording that changes physical requirements without a separately accepted plan revision.
- [ ] **C02.09.05** Render long and difficult fictional stages against a fixed assignment; compare displayed targets with authoritative training records and independently verify the progression explanation.
- [ ] **C02.09.06** Exercise missing assignments, stale revisions, unknown targets, and unsupported equipment prompts; provide an explicit unresolved state rather than inventing a replacement physical demand.
- [ ] **C02.09.07** Update an assignment through its approved operation during an unfinished day; record the chosen reference revision and avoid silently replacing completed assignment history.
- [ ] **C02.09.08** Archive assignment-reference and narrative-boundary reviews; accept only when every physical criterion matches its authoritative version and no dossier text introduces unaccepted exercise changes.

### Control C02 10

**Original requirement C02.10:** Classify content as preparation, brief walking presentation, or post-workout interaction; substantial decisions remain deferrable and never require a rapid response while walking.

- [ ] **C02.10.01** Classify each dossier section and interaction as preparation, brief walking presentation, or post-workout work; define engagement and deferral rules for substantive choices.
- [ ] **C02.10.02** Set walking-presentation limits for text length, interaction count, audio initiation, and sustained attention using the declared viewing-context budget and reviewed reference scenarios.
- [ ] **C02.10.03** Provide decide-later operations for complex branches, calculations, shopping, and lessons; persist pending identity and ensure users can resume them after finishing physical activity.
- [ ] **C02.10.04** Keep rapid-response timers and mandatory simultaneous walking decisions outside essential flows; optional timed content must have an equally complete untimed path.
- [ ] **C02.10.05** Walk through every substantive interaction in walking mode; verify postponement preserves options, consequences, and narrative eligibility without altering the accepted physical assignment.
- [ ] **C02.10.06** Exercise ignored prompts, prolonged deferral, background tabs, and finishing before choices; confirm no silent default branch or extra workout duration is imposed.
- [ ] **C02.10.07** Restart with deferred decisions and open the camp debrief; restore pending choices with original content versions and clear indication of their unresolved state.
- [ ] **C02.10.08** Archive interaction classifications and walking-context review results; accept only when every substantive choice remains reachable, deferrable, and independent of rapid physical-session engagement.

### Control C02 11

**Original requirement C02.11:** Assemble against the saved day reservation and route origin; persist its exact configuration/version. Resume the unfinished snapshot on later launches, and reject adoption of snapshots whose campaign/day, origin, or pinned manifest differs from the reservation.

- [ ] **C02.11.01** Define a reservation fingerprint containing campaign/day, route origin, pinned manifest, locale, generation configuration, and version; store it before dossier assembly begins.
- [ ] **C02.11.02** Load the authoritative reserved day from SQLite and compare every assembled snapshot identifier with its fingerprint; current browser selections cannot replace saved reservation values.
- [ ] **C02.11.03** Persist the exact validated assembly inputs and adopt snapshots only through matching job/publication records; reject files whose appearance resembles the expected day but identity differs.
- [ ] **C02.11.04** On launch, prefer the saved unfinished snapshot; check coherence and permitted correction state before generating missing content for the same reserved day.
- [ ] **C02.11.05** Relaunch repeatedly with changed port, cleared browser cache, and changed local date; verify the same day identity, origin, manifest, and configuration are restored.
- [ ] **C02.11.06** Attempt adoption of another campaign's package, different origin, or newer manifest; reject each mismatch with evidence identifying the conflicting reservation field.
- [ ] **C02.11.07** Interrupt assembly after reservation and recover the job; retain the original fingerprint and leave continuation unchanged until the explicit complete-day operation succeeds.
- [ ] **C02.11.08** Archive reservation/adoption and relaunch traces; accept only when every adopted snapshot matches its saved reservation and unfinished days never regenerate into different authoritative context.

### Control C02 12

**Original requirement C02.12:** Validate prerequisites, recurring characters, unresolved events, resources, and tomorrow's preview against the player's actual branch history; avoid displaying impossible future outcomes.

- [ ] **C02.12.01** Define dossier precondition checks for selected branches, recurring-character states, unresolved events, resource balances, mandatory decisions, and permissible next-stage preview outcomes.
- [ ] **C02.12.02** Read those inputs from one coherent campaign revision; record the revision and causal references used when assembling branch-dependent text or preview selections.
- [ ] **C02.12.03** Require characters and event prerequisites to match persisted history; suppress or replace content whose assumptions conflict with known decisions, location, or unresolved consequences.
- [ ] **C02.12.04** Limit tomorrow's preview to committed geography and conditional possibilities; disclose uncertainty rather than describing unresolved branch outcomes as established future facts.
- [ ] **C02.12.05** Render dossiers for mutually exclusive branches and exhausted resources; independently compare dialogue, available choices, and previews against the corresponding expected campaign records.
- [ ] **C02.12.06** Seed absent prerequisites, impossible character returns, stale balances, and uncompleted mandatory events; reject contradictory assembly or provide the explicitly authored recovery variant.
- [ ] **C02.12.07** Change campaign state during assembly and attempt publication; require revision revalidation or safe regeneration so a mixed-state dossier never becomes ready.
- [ ] **C02.12.08** Archive branch-consistency matrices and sample previews; accept only when every published dependent section resolves to compatible history and no impossible future outcome is asserted.

### Control C02 13

**Original requirement C02.13:** Present geographically relevant imagery with captions, credits, representation labels, and seasonal context; expose missing or representative coverage rather than implying exact coverage.

- [ ] **C02.13.01** Define gallery entries linking geographic association, representation class, capture-date precision, seasonal context, caption, credit, accessible description, and rights-approved rendition identifiers.
- [ ] **C02.13.02** Select imagery by stage relevance using reviewed associations; exact-location claims require supported location evidence rather than visual resemblance or nearby file naming.
- [ ] **C02.13.03** Display nearby, representative, historical, reconstructed, or illustrative labels where omission could mislead; separate photo capture conditions from hypothetical dossier weather and season.
- [ ] **C02.13.04** Specify honest missing-coverage presentations with text, maps, or labeled regional images; expose an exact-location gap instead of implying a substitute depicts the stage.
- [ ] **C02.13.05** Review galleries for contrasting regions and seasons; trace each image to its position, rights, caption, and representation decision in the media catalog.
- [ ] **C02.13.06** Introduce incorrect location links, absent credits, unknown capture dates, and unavailable renditions; verify blocking review or visibly informative fallback according to publication rules.
- [ ] **C02.13.07** Withdraw a primary image during an unfinished day; apply the approved replacement workflow while preserving campaign identity and historical media references for completed snapshots.
- [ ] **C02.13.08** Archive geographic gallery reviews and fallback screenshots; accept only when every displayed image has correct attribution, explicit relevance, and nonmisleading seasonal/capture context.

### Control C02 14

**Original requirement C02.14:** Provide structured headings, readable typography, captions, keyboard interaction, meaningful image descriptions, reduced-motion presentation, and text equivalents for map/elevation information.

- [ ] **C02.14.01** Specify heading hierarchy, text sizing, contrast, caption relationships, focus order, keyboard actions, reduced-motion behavior, and map/elevation text equivalents for dossier templates.
- [ ] **C02.14.02** Use semantic controls and programmatic labels for navigation and choices; associate instructions, errors, credits, and image descriptions with the relevant rendered content.
- [ ] **C02.14.03** Provide route-position and terrain summaries conveying essential graphical information in text; verify the alternatives contain the same units, uncertainty, and source classifications.
- [ ] **C02.14.04** Preserve readable layout under magnification and narrow displays; required content and completion controls must remain reachable without overlapping panels or clipped text.
- [ ] **C02.14.05** Complete every dossier action by keyboard and representative screen reader; verify headings, image descriptions, status messages, and choice consequences are announced meaningfully.
- [ ] **C02.14.06** Exercise disabled images, reduced motion, long captions, enlarged text, and unavailable graphical assets; retain equivalent access to geography, assignments, branches, and debriefs.
- [ ] **C02.14.07** Correct accessibility defects in the template and regenerate affected preview snapshots; confirm fixes do not remove required content or alter pinned campaign outcomes.
- [ ] **C02.14.08** Archive accessibility assessment, device/browser scope, and resolved-defect evidence; accept only when all applicable declared accessibility criteria pass or have explicitly bounded approved exceptions.

### Control C02 15

**Original requirement C02.15:** Package approved dependencies beneath configured repository-local media/package roots and serve them locally; retain assignment, decisions, and journal without internet access, accounts, or remote services.

- [ ] **C02.15.01** Inventory all required local dependencies for assignments, choices, journal editing, maps, images, lessons, and templates; define approved repository-relative package/media roots.
- [ ] **C02.15.02** Package approved content and rights metadata beneath those roots with checksummed manifests; required functionality cannot depend on cloud accounts or remote-service authorization.
- [ ] **C02.15.03** Validate served dependency paths against canonical roots, including decoded traversal and escaping links; prevent packages from referencing database, logs, credentials, or private unrelated files.
- [ ] **C02.15.04** Define offline readiness separately from local-service availability; internet loss permits normal durable interactions while loopback failure must expose unsaved or unavailable state.
- [ ] **C02.15.05** Disconnect internet and complete assignment recording, a branch decision, lesson, and journal save; verify committed database records and subsequent reload without remote requests.
- [ ] **C02.15.06** Remove a required local dependency and retry publication; block readiness or use an explicitly approved informative fallback with no unrelated or misleading substitution.
- [ ] **C02.15.07** Restart the service offline and revisit the saved dossier; reconcile package checksums, pending decisions, and journal revisions against authoritative local records.
- [ ] **C02.15.08** Archive dependency closure, network-disconnected journey, and path-boundary evidence; accept only when essential dossier interactions work locally and every delivered file belongs to approved roots.

### Control C02 16

**Original requirement C02.16:** Stage files with checksums, rename the verified snapshot atomically on the same volume, then commit a recoverable SQLite publication marker. Treat filesystem and database operations as separate steps; mark ready only when reconciliation confirms a coherent snapshot, and leave hike progression unchanged after failed generation.

- [ ] **C02.16.01** Specify publication-job states for reserved, staging, validated, renamed, database-marked, reconciled-ready, and failed, with recoverable transitions and stable job/reservation identifiers.
- [ ] **C02.16.02** Write files into a job-specific staging directory; validate schema, dependencies, rights, and checksums before a same-volume atomic rename exposes the verified snapshot.
- [ ] **C02.16.03** Commit publication markers separately in SQLite after file publication; document that database rollback cannot undo renamed files and requires explicit reconciliation handling.
- [ ] **C02.16.04** Define recovery for missing markers, absent renamed files, checksum mismatches, leftover staging, and incomplete dependencies; only coherent marker/file pairs may become ready.
- [ ] **C02.16.05** Inject failures before and after every file-write, validation, rename, database-commit, and readiness boundary; inspect recovery against independently specified expected job states.
- [ ] **C02.16.06** Simulate disk exhaustion, access denial, database lock, and checksum corruption; verify generation failure leaves day identity and the committed next-leg pointer unchanged.
- [ ] **C02.16.07** Retry interrupted jobs with the same reservation and input manifest; adopt verified artifacts or regenerate safely without publishing duplicate snapshots or partial dependency sets.
- [ ] **C02.16.08** Archive crash-boundary and reconciliation evidence; accept only when all publication states recover to one verified ready package or an explicitly nonready, progression-preserving failure.

### Control C02 17

**Original requirement C02.17:** Define correction behavior for unfinished/completed days and preserve completed snapshots. Require an explicit idempotent completion request that transactionally records the day log and next-leg endpoint; refresh, launch, and process exit cannot complete a day.

- [ ] **C02.17.01** Define correction policies for reserved, active, unfinished, and completed days, identifying annotation, substitution, withdrawal, and replacement operations that preserve immutable completed snapshots.
- [ ] **C02.17.02** Specify complete-day request fields including source day, expected campaign/day revision, idempotency key, accepted evidence, final endpoint, and mandatory-choice acknowledgment where applicable.
- [ ] **C02.17.03** Commit day completion, day log, accepted causal records, and next-leg pointer together within one SQLite transaction; report success only after durable commit.
- [ ] **C02.17.04** Restrict completion authority to the explicit user operation; launcher events, page refresh, browser closure, service exit, and calendar changes cannot invoke equivalent advancement.
- [ ] **C02.17.05** Correct one unfinished and one completed dossier; verify allowed current-content behavior while original completed snapshot identity, history, and completion endpoint remain available.
- [ ] **C02.17.06** Retry completion after losing the response and issue a stale-tab request; require one effective completion and rejection of superseded day or incompatible revisions.
- [ ] **C02.17.07** Interrupt correction and completion at persistence boundaries; restart and reconcile preserved snapshots, annotations, day status, and continuation state without partially advanced history.
- [ ] **C02.17.08** Archive correction and completion traces; accept only when each correction is attributable and every pointer advance corresponds to exactly one explicit committed source-day completion.

### Control C02 18

**Original requirement C02.18:** Support targeted withdrawal and rollback with usable substitute content; identify affected campaigns and prevent stale caches from restoring prohibited or invalid material.

- [ ] **C02.18.01** Define withdrawal records specifying affected content/version, reason, severity, effective time, replacement package, dependent campaigns, cache action, reviewer, and rollback eligibility conditions.
- [ ] **C02.18.02** Compute affected dossier, media, lesson, event, package, and campaign dependencies before withdrawal; distinguish completed historical references from currently deliverable prohibited material.
- [ ] **C02.18.03** Require a verified coherent substitute or informative withdrawal presentation; preserve usable assignment, logging, decision, and journal functions whenever their dependencies remain valid.
- [ ] **C02.18.04** Change the approved release pointer transactionally while retaining immutable prior packages; forbid rollback to a version that remains prohibited or rights-incompatible.
- [ ] **C02.18.05** Withdraw a live dependency and reopen affected unfinished dossiers; verify replacements carry correct identity/labels and all affected delivery paths obey the withdrawal decision.
- [ ] **C02.18.06** Serve stale browser caches and old package requests after withdrawal; require revalidation or denial so prohibited content cannot become current through cache restoration.
- [ ] **C02.18.07** Interrupt withdrawal or rollback and restart; reconcile pointers, replacement availability, blocked asset identities, and campaign history while leaving completion and next-leg state intact.
- [ ] **C02.18.08** Archive impact lists, substitution reviews, cache tests, and rollback rehearsal; accept only when targeted withdrawal reaches every application-controlled delivery path without corrupting saved history.

### Control C02 19

**Original requirement C02.19:** Review representative complete dossiers across regions, seasons, progression modes, languages where supported, and display sizes; assess clarity of facts, fiction, assignment, choices, and consequences.

- [ ] **C02.19.01** Define a representative dossier review matrix spanning content regions, scenario seasons, enabled progression modes, supported languages, recovery/partial days, and declared display sizes.
- [ ] **C02.19.02** Select samples from exact candidate manifests and retain campaign configurations; reviewers must inspect actual rendered packages rather than template descriptions or editorial drafts alone.
- [ ] **C02.19.03** Assign factual, narrative, assignment, choice-consequence, accessibility, and locale reviewers; record criteria and accountable dispositions when one person performs several review roles.
- [ ] **C02.19.04** Compare every sampled dossier's source classifications, training criteria, choices, consequences, captions, and next-stage preview against its authoritative records and approved authored intent.
- [ ] **C02.19.05** Review long translations, seasonal mismatches, small screens, and sparse imagery; detect clipped content, misleading dates, ambiguous units, or choices obscured by visual layout.
- [ ] **C02.19.06** Record defects with package identity, reproducible viewport/profile, severity, owner, and expected correction; prevent unresolved material confusion from receiving unqualified acceptance.
- [ ] **C02.19.07** Rebuild corrected samples and review affected neighboring configurations; confirm fixes preserve branch history, assignment references, and the declared information classification across variants.
- [ ] **C02.19.08** Archive the completed sample matrix and reviewer decisions; accept only when every declared dimension is represented and material clarity defects are resolved or explicitly excepted.

### Control C02 20

**Original requirement C02.20:** Verify missing dependencies, expired rights, divergent branches, interrupted local publication, database locks, repeated launches, refresh, completion retry, service restart, offline use, correction, and rollback.

- [ ] **C02.20.01** Specify publication/recovery verification cases for missing dependencies, expired rights, conflicting branches, interrupted file/database publication, locks, relaunch, refresh, completion retries, and rollback.
- [ ] **C02.20.02** Record initial campaign/day state, manifests, fault boundary, operation identity, expected response, ready status, completion count, and next-leg position for each case.
- [ ] **C02.20.03** Run scenarios through the actual loopback service and CMD/PowerShell launcher; include browser-cache deletion and offline internet without bypassing authoritative publication or completion paths.
- [ ] **C02.20.04** Verify missing/expired dependencies prevent prohibited delivery while usable fallback content remains accurately labeled; confirm divergent branch snapshots cannot be adopted for another history.
- [ ] **C02.20.05** Inject database locks and service restart before and after publication/completion commits; require recoverable nonready states or one coherent committed result with deduplicated effects.
- [ ] **C02.20.06** Apply corrections and rollback during unfinished and completed campaigns; inspect pinned snapshots, withdrawn caches, assignment records, day logs, and continuation for expected preservation.
- [ ] **C02.20.07** Retain failed cases with fault logs and manifest/database reconciliation; rerun targeted scenarios after repair and link final outcomes to the corrected implementation/content revision.
- [ ] **C02.20.08** Archive the complete dossier verification matrix; accept only when every specified lifecycle/failure scenario passes and launch, refresh, or retry never creates duplicate advancement.

## C03 Photograph and media library

**Accountable owners:** Media custodian for originals and metadata; rights reviewer for permissions; geographic editor for location relevance; accessibility reviewer for descriptions and media alternatives.

**Interfaces:** Consumes licensed photographs, recordings, permission records, and geographic evidence. Stores authoritative asset/rights metadata in local SQLite and originals/renditions beneath configured repository-local media roots. Produces `MediaAsset`, `AssetRendition`, `RightsGrant`, `GeographicAssociation`, attribution records, and local-service delivery manifests for dossiers and journals.

**Required evidence:** Local asset/rights schemas; permission records; originals and checksums; repository-relative path manifest; location-review samples; rendition configuration; coverage report; visual/accessibility review; traversal, relocation, withdrawal, and integrity results.

**Exit criterion:** Every published asset has a verified permitted use, traceable geographic relevance, complete presentation metadata, and tested deliverable renditions. Missing or withdrawn assets degrade the experience transparently without substituting misleading scenery.

### Control C03 01

**Original requirement C03.01:** Publish schemas linking each media asset to immutable originals, processing history, geographic associations, rights grants, captions, accessible descriptions, and available renditions.

- [ ] **C03.01.01** Specify MediaAsset, OriginalFile, ProcessingStep, GeographicAssociation, RightsGrant, CaptionRevision, AccessibleDescription, and AssetRendition schemas with stable identifiers, required fields, reference rules, and version compatibility.
- [ ] **C03.01.02** Define immutable original-file identity separately from mutable editorial metadata; retain original checksums and prohibit replacement of source bytes under an existing original identifier.
- [ ] **C03.01.03** Link each rendition to its original and processing configuration; require geographic association, rights, caption, and accessibility references before any asset becomes publishable.
- [ ] **C03.01.04** Represent unknown capture/location metadata explicitly and define media-type-specific requirements; absent audio transcripts and missing photograph descriptions must receive separate applicability decisions.
- [ ] **C03.01.05** Round-trip representative photographs and recordings through catalog import, SQLite storage, and manifest export; compare references and metadata against independently prepared expected records.
- [ ] **C03.01.06** Reject orphaned renditions, unsupported schema versions, missing originals, circular processing lineage, and invalid rights references; retain incomplete imports outside the published media catalog.
- [ ] **C03.01.07** Interrupt catalog creation and retry using stable asset identity; verify partial schema records cannot produce a deliverable rendition or inconsistent publication dependency.
- [ ] **C03.01.08** Archive schemas, lineage diagrams, constraint results, and reviewer decisions; accept only when every published asset resolves to complete original, rendition, rights, and presentation records.

### Control C03 02

**Original requirement C03.02:** Retain original checksum, asset identifier, MIME type, dimensions, duration, acquisition time, creator, and ingestion trail in local SQLite; reference files through validated repository-relative paths.

- [ ] **C03.02.01** Define acquisition records for immutable asset ID, checksum, detected MIME, dimensions, duration where applicable, creator, acquisition time, source, and ingestion-operation identity.
- [ ] **C03.02.02** Inspect file signatures and media headers rather than trusting extensions; store detected properties and original metadata with explicit unknown representations for unavailable values.
- [ ] **C03.02.03** Normalize file references to repository-relative paths and validate their resolved locations beneath configured media roots before registering originals or exposing delivery manifests.
- [ ] **C03.02.04** Record every ingest/copy operation with input origin, destination, checksum result, actor, timestamp, and outcome; duplicate ingestion must not overwrite an existing asset's history.
- [ ] **C03.02.05** Import known photographs and recordings and independently compare dimensions, duration, MIME, checksum, and SQLite references against their verified source files locally.
- [ ] **C03.02.06** Exercise mismatched extensions, malformed headers, absolute external paths, escaping links, absent creators, and oversized metadata; reject unsafe references while preserving legitimate unknown values.
- [ ] **C03.02.07** Relocate the repository and reopen registered assets; verify relative paths still resolve and unavailable files receive explicit errors rather than substituted catalog entries.
- [ ] **C03.02.08** Archive ingestion/property reconciliation and path tests; accept only when registered originals match their detected properties and every delivered reference stays beneath approved media roots.

### Control C03 03

**Original requirement C03.03:** Record coordinates when known, depicted feature, viewing direction when known, location evidence, route proximity, and editorial confidence; preserve unknown values rather than inventing metadata.

- [ ] **C03.03.01** Define geographic metadata fields for coordinates/reference system, depicted feature, optional viewing direction, evidence references, route proximity, confidence, reviewer, and assessment revision.
- [ ] **C03.03.02** Separate camera location from depicted-feature location; identify which coordinate meaning is known and preserve unknown positions or bearings without invented numeric defaults.
- [ ] **C03.03.03** Associate imagery with immutable route releases and positions using reviewed evidence; visual resemblance alone cannot establish an exact-location link or high-confidence classification.
- [ ] **C03.03.04** Specify proximity calculations and confidence vocabulary, including ambiguous multi-feature scenes; retain competing location claims and their dispositions in the geographic review record.
- [ ] **C03.03.05** Compare known-location images with independently checked route proximity and feature associations; confirm captions and maps reflect the reviewed camera/feature distinction accurately.
- [ ] **C03.03.06** Remove EXIF coordinates or supply conflicting captions and coordinates; verify unknown/contested metadata remains explicit and exact-location publication waits for appropriate evidence.
- [ ] **C03.03.07** Revise an association after discovering a mismatch; identify dependent dossiers and apply the approved correction workflow while preserving prior published metadata references.
- [ ] **C03.03.08** Archive association evidence and geographic-confidence review; accept only when every exact-location claim is supported and unknown position/direction values are visibly unasserted.

### Control C03 04

**Original requirement C03.04:** Classify relevance as exact location, nearby location, representative region, historical, reconstructed, or illustrative; display the classification whenever omission could mislead.

- [ ] **C03.04.01** Define relevance categories and decision criteria for exact location, nearby location, representative region, historical, reconstructed, and illustrative imagery with approved display labels.
- [ ] **C03.04.02** Specify where classification must appear in galleries, captions, full-screen views, journals, exports, and source lists when absence would imply unsupported geographic accuracy.
- [ ] **C03.04.03** Require editorial classification before asset selection; exact-location status depends on reviewed evidence, while generated or reconstructed images retain explicit illustration/reconstruction categories.
- [ ] **C03.04.04** Store classification per geographic use when one image supports different contexts; avoid treating a catalog-wide label as proof for every stage association.
- [ ] **C03.04.05** Render one asset from each category in dossier and export views; verify the displayed wording communicates its relevance without requiring source-page inspection.
- [ ] **C03.04.06** Attempt to publish representative-region or generated imagery under an exact-stage caption; reject or relabel the use and record the responsible editorial decision.
- [ ] **C03.04.07** Change an association classification after publication; propagate approved correction notices and prevent stale current views from restoring a misleading exact-location label.
- [ ] **C03.04.08** Archive category rules and rendered classification samples; accept only when every potentially misleading use exposes the correct reviewed relevance classification at its point of interpretation.

### Control C03 05

**Original requirement C03.05:** Store capture-date precision, season, observed conditions, and historical context separately from scenario weather or the player's expedition date.

- [ ] **C03.05.01** Define capture date with explicit precision, observed season, depicted conditions, historical context, evidence, and uncertainty; keep scenario weather/date fields in separate records.
- [ ] **C03.05.02** Preserve unknown, year-only, month-only, and exact dates without inventing missing components; record whether capture information came from EXIF, creator statements, or editorial evidence.
- [ ] **C03.05.03** Specify captions identifying historical and seasonal context wherever photographs could otherwise imply current conditions or match the player's fictional or real training date.
- [ ] **C03.05.04** Validate temporal consistency without inferring weather from calendar alone; inconsistent EXIF and source dates must trigger review rather than silent preference for one source.
- [ ] **C03.05.05** Render seasonal imagery under contrasting scenario dates and current computer dates; verify capture context remains independent and hypothetical weather does not overwrite observed conditions.
- [ ] **C03.05.06** Import dates with timezone ambiguity, future capture claims, and conflicting sources; flag them for review while retaining the original supplied evidence and precision.
- [ ] **C03.05.07** Correct capture metadata after publication through versioned editorial records; completed dossiers retain original context plus approved annotations rather than rewritten historical imagery dates.
- [ ] **C03.05.08** Archive temporal metadata fixtures and caption reviews; accept only when every date preserves its supported precision and historical photographs cannot masquerade as current observations.

### Control C03 06

**Original requirement C03.06:** Record rights holder, permission evidence, allowed channels, modification restrictions, required attribution, expiration, and revocation terms; distinguish asset ownership from a permitted use.

- [ ] **C03.06.01** Define rights grants with holder identity, permission evidence, allowed use channels, modification restrictions, attribution wording, expiration, revocation terms, and assessment/version references.
- [ ] **C03.06.02** Separate ownership, possession, and permission-to-use statuses; acquired originals remain unusable for publication until the intended channel is covered by valid evidence.
- [ ] **C03.06.03** Record grant applicability to originals, derivative renditions, offline packages, and exports; identify required conditions such as credit placement or limits on alteration.
- [ ] **C03.06.04** Specify time evaluation, uncertain expiration, and revocation handling; missing or ambiguous permission terms require reviewer disposition rather than an unrestricted-use default.
- [ ] **C03.06.05** Evaluate sample owned, licensed, permission-granted, restricted, and expired assets against actual dossier/export uses; independently verify every allowed/denied decision with the evidence record.
- [ ] **C03.06.06** Submit absent permission documents, incompatible channels, prohibited crops, and incomplete required attribution; block affected uses while retaining catalog records for correction or replacement.
- [ ] **C03.06.07** Update or revoke a grant and resolve its dependencies; preserve prior permission evidence and record which current delivery paths require removal or revised attribution.
- [ ] **C03.06.08** Archive rights assessments and intended-use matrices; accept only when every published use has an applicable valid grant and all permission conditions are implemented.

### Control C03 07

**Original requirement C03.07:** Define caption, alternative-text, transcript, and credit fields with locale and editorial versioning; prohibit essential geographic interpretation from existing only in a filename.

- [ ] **C03.07.01** Specify localized caption, alternative text, transcript, credit, editorial revision, language, reviewer, and requiredness fields appropriate to each enabled media type and use.
- [ ] **C03.07.02** Separate descriptive accessibility text from source/credit text and decorative-image decisions; essential geographic meaning belongs in visible captions or equivalent accessible content.
- [ ] **C03.07.03** Define locale fallback behavior that preserves meaning and attribution; missing translations must be disclosed or use approved fallback language without empty essential descriptions.
- [ ] **C03.07.04** Version editorial changes independently from immutable originals and renditions; pin published dossiers to the exact caption, description, transcript, and credit revisions reviewed.
- [ ] **C03.07.05** Inspect images with uninformative filenames and recordings without speech transcripts; verify published presentation conveys location, representation, and essential media content through explicit fields.
- [ ] **C03.07.06** Exercise empty descriptions, duplicated filename text, unsupported locale tags, stale captions, and missing credits; reject incomplete essential presentation metadata before publication.
- [ ] **C03.07.07** Correct a translated caption or transcript and identify dependent packages; use approved replacement/annotation behavior while preserving the wording delivered in completed historical snapshots.
- [ ] **C03.07.08** Archive localized presentation metadata and accessibility review results; accept only when all essential interpretation is available without filenames and all enabled media alternatives are complete.

### Control C03 08

**Original requirement C03.08:** Validate dossier and export uses against rights grants before publication and delivery; reject incompatible use and identify every affected dependency.

- [ ] **C03.08.01** Define a rights-use evaluator taking asset/rendition, grant revision, destination channel, requested modifications, attribution implementation, publication/delivery time, and export package context.
- [ ] **C03.08.02** Run evaluation before package publication and current delivery; cached approval cannot authorize a use after its grant expires, is revoked, or becomes incompatible.
- [ ] **C03.08.03** Build reverse dependencies for every dossier, gallery, offline package, journal, and export using the asset; expose affected identities when an intended use fails.
- [ ] **C03.08.04** Require incompatible uses to block or select a reviewed permitted substitute; avoid repairing rights failures by silently removing credit or weakening restriction labels.
- [ ] **C03.08.05** Test allowed dossier viewing and denied export against one channel-restricted grant; confirm decisions match independent rights-review expectations and identify all impacted dependencies.
- [ ] **C03.08.06** Exercise expired grants, absent permission evidence, forbidden alterations, and unauthorized redistribution requests; verify no prohibited rendition enters a new package or delivery response.
- [ ] **C03.08.07** Simulate grant change between validation and publication; recheck the effective grant or reject stale approval, then recover through an attributable reviewed replacement operation.
- [ ] **C03.08.08** Archive rights-evaluation cases and dependency impact reports; accept only when all published/delivered uses satisfy effective grants and every failed use has identifiable affected dependencies.

### Control C03 09

**Original requirement C03.09:** Preserve required credits in galleries, dossier sources, offline packages, and journal exports as applicable to the relevant grant.

- [ ] **C03.09.01** Specify credit placement, exact required wording, source links where required, locale handling, and attribution persistence for galleries, dossier sources, packages, and journal exports.
- [ ] **C03.09.02** Link rendered credits to grant versions and asset identities; distinguish creator credit from permission evidence so compliant presentation does not imply unsupported ownership.
- [ ] **C03.09.03** Include attribution records in offline manifests and human-readable exports; verify required credits remain available when external websites and interactive gallery controls are inaccessible.
- [ ] **C03.09.04** Define credit behavior for crops, composites, multiple assets, thumbnails, and substitute imagery; preserve every relevant grant's conditions rather than displaying one generic gallery credit.
- [ ] **C03.09.05** Inspect packaged files and printed/exported journal samples independently; confirm all used assets retain their applicable attribution in required locations with readable formatting.
- [ ] **C03.09.06** Delete credits from one template and omit an offline attribution file; require publication/export validation to detect both defects and block noncompliant artifacts.
- [ ] **C03.09.07** Replace an asset during withdrawal recovery; update its credits and maintain prior historical attribution references without miscrediting the substitute or erasing original provenance.
- [ ] **C03.09.08** Archive channel-by-channel attribution checks and rendered samples; accept only when every applicable grant condition is satisfied across all application-controlled presentation and export paths.

### Control C03 10

**Original requirement C03.10:** Review identifiable people, sensitive location details, culturally significant subjects, and captions for permission and editorial suitability; record the decision and its evidence.

- [ ] **C03.10.01** Define review categories for identifiable people, sensitive coordinates, culturally significant subjects, permission evidence, caption tone, intended audience, and editorial suitability decisions.
- [ ] **C03.10.02** Inventory assets requiring subject/context review before publication; record reviewer competence or consultation basis and the precise use scope of any permission provided.
- [ ] **C03.10.03** Separate permission sufficiency from editorial suitability; possession or broad image licensing does not automatically approve sensitive subject descriptions or unnecessary location-detail exposure.
- [ ] **C03.10.04** Specify approved handling for uncertain permission, contested captions, and sensitive metadata, including restricted publication, location generalization, replacement, or withheld use with documented reasons.
- [ ] **C03.10.05** Inspect representative assets in each review category; verify captions, visible location details, metadata, and export uses conform to their recorded review decisions.
- [ ] **C03.10.06** Introduce identifying captions or sensitive coordinates not covered by approval; block the affected use and preserve the issue for explicit review rather than automatic publication.
- [ ] **C03.10.07** Apply an approved redaction or removal and trace dependent dossiers/packages; verify the change reaches controlled renditions and exports without corrupting unrelated asset records.
- [ ] **C03.10.08** Archive decisions, permission references, redaction scope, and final-use review; accept only when every flagged subject/context has an attributable suitability disposition matching released content.

### Control C03 11

**Original requirement C03.11:** Review whether cropping, enhancement, compositing, or generation changes perceived geography or conditions; document material edits and display appropriate disclosure.

- [ ] **C03.11.01** Define material-edit criteria for cropping, enhancement, color changes, object removal, compositing, and generation, focusing on altered geography, visibility, weather, season, or trail conditions.
- [ ] **C03.11.02** Record transformations and edited-region descriptions with original/rendition checksums; preserve immutable originals so reviewers can directly compare geographic meaning before and after editing.
- [ ] **C03.11.03** Require geographic/editorial review when edits remove context, move features, change apparent exposure, or synthesize scenery; ordinary format conversion follows documented nonmaterial processing rules.
- [ ] **C03.11.04** Specify disclosure wording and placement for materially edited, composite, reconstructed, or generated imagery; labels must accompany the asset wherever geographic interpretation depends on authenticity.
- [ ] **C03.11.05** Compare original and final hero images side by side; document whether terrain, trail location, environmental conditions, or feature relationships remain faithful to supported evidence.
- [ ] **C03.11.06** Attempt exact-location publication of composites or generated trail scenes without disclosure; reject misleading use and retain the editorial reason plus approved representation alternative.
- [ ] **C03.11.07** Discover an undisclosed edit in a published rendition; identify affected packages and apply explicit correction/withdrawal rather than silently replacing the original under unchanged identity.
- [ ] **C03.11.08** Archive edit reviews, before/after comparisons, and disclosure samples; accept only when every material alteration has documented reasoning and visible classification appropriate to its actual representation.

### Control C03 12

**Original requirement C03.12:** Generate responsive renditions locally with recorded transformations, safe crop regions, orientation correction, and format settings; atomically publish files and retain a reproducible relationship to the original.

- [ ] **C03.12.01** Specify rendition profiles containing target dimensions, format, quality, orientation handling, color settings, crop constraints, transformation version, and performance budgets for supported displays.
- [ ] **C03.12.02** Derive renditions locally from checksummed originals; store input identity, complete processing parameters, output checksum, dimensions, MIME, and reproduction relationship in catalog records.
- [ ] **C03.12.03** Define safe crop regions and feature-preservation rules; require editorial review if responsive cropping can remove essential terrain, landmark context, credits, or representation labels.
- [ ] **C03.12.04** Write outputs into staging, validate them, and atomically rename verified files on the same volume; register readiness only after catalog/file reconciliation succeeds.
- [ ] **C03.12.05** Generate portrait, landscape, panoramic, rotated, and transparent fixtures; inspect each rendition profile for correct orientation, preserved safe regions, and declared format/dimension compliance.
- [ ] **C03.12.06** Inject failed encoding, unsupported color metadata, and interrupted output writes; ensure corrupted/partial files cannot become manifest dependencies or replace verified existing renditions.
- [ ] **C03.12.07** Regenerate a selected rendition from retained original and pinned parameters; compare checksums or documented encoder equivalence and preserve attribution/geographic metadata throughout processing.
- [ ] **C03.12.08** Archive transformation configurations, crop approvals, reproduction results, and interruption evidence; accept only when every delivered rendition is valid, traceable, and reproducibly derived from its original.

### Control C03 13

**Original requirement C03.13:** Validate rendered quality, orientation, color handling, sharpness, dimensions, file size, and corruption; visually inspect photographs used as primary dossier imagery.

- [ ] **C03.13.01** Define media-quality acceptance thresholds for dimensions, byte size, orientation, color handling, sharpness, artifact visibility, and corruption detection for each primary-image delivery profile.
- [ ] **C03.13.02** Inspect decoded files rather than metadata alone; verify successful full decoding, expected dimensions, supported format, and checksum agreement before marking rendition quality accepted.
- [ ] **C03.13.03** Specify reference viewing conditions and primary-image review scope; reviewers must assess geographic readability and photographic clarity at actual dossier display sizes.
- [ ] **C03.13.04** Compare color-managed output with the approved original and inspect orientation/crop behavior; record any accepted limitations caused by unavailable profiles or low-resolution source material.
- [ ] **C03.13.05** Review representative hero imagery across supported sizes; confirm essential trail/landmark context remains legible and compression does not create materially misleading apparent features.
- [ ] **C03.13.06** Seed truncated files, rotated EXIF cases, undersized images, severe artifacts, and oversized outputs; require accurate detection or rejection before package publication proceeds.
- [ ] **C03.13.07** Replace rejected renditions through controlled regeneration and repeat visual review; preserve original identity and prevent quality fixes from bypassing rights or geographic-edit approval.
- [ ] **C03.13.08** Archive automated property checks and primary-image visual decisions; accept only when every hero rendition meets declared thresholds or carries a specifically approved visible limitation.

### Control C03 14

**Original requirement C03.14:** Define loading budgets, lazy loading, placeholders, local cache eviction, and local-service delivery behavior; validate paths beneath approved media/package roots and reject traversal or escaping links.

- [ ] **C03.14.01** Set image byte/count budgets, initial-load limits, lazy-load thresholds, placeholders, retry behavior, cache quotas, and eviction rules for named reference devices and browsers.
- [ ] **C03.14.02** Define local media delivery endpoints resolving validated repository-relative catalog paths; canonicalize requested paths and verify resulting files stay beneath approved media/package roots.
- [ ] **C03.14.03** Reject traversal, encoded separators, absolute-path requests, escaping filesystem links, and private-file references before reading bytes; record useful diagnostics without exposing unrelated repository contents.
- [ ] **C03.14.04** Preserve layout stability with known aspect ratios and informative placeholders; lazy-loaded assets must retain captions, credits, relevance labels, and accessible descriptions when loading fails.
- [ ] **C03.14.05** Measure first-dossier and long-gallery loading against configured budgets; confirm deferred images load when needed and cache eviction preserves authoritative history and package references.
- [ ] **C03.14.06** Exercise malformed paths, deleted files, cache exhaustion, and simultaneous image requests; verify safe denial or informative fallback without serving database, logs, or unapproved files.
- [ ] **C03.14.07** Relocate the repository and change service port after cache population; revalidate catalog roots and rebuild replaceable caches without altering media identities or hike state.
- [ ] **C03.14.08** Archive delivery-boundary and performance results; accept only when loading budgets pass, all unsafe requests are rejected, and evictions never change authoritative campaign or media records.

### Control C03 15

**Original requirement C03.15:** Validate checksums after acquisition or local copy; support resumable imports and duplicate detection, and exclude temporary/partial files from published dossier manifests.

- [ ] **C03.15.01** Define resumable import jobs with source identity, expected size/checksum, verified chunks where used, temporary paths, progress state, duplicate key, and final validation result.
- [ ] **C03.15.02** Compute checksums after acquisition and every authoritative local copy; compare actual bytes with the expected original digest before registering a usable media asset.
- [ ] **C03.15.03** Specify duplicate policy distinguishing identical bytes, different renditions, and reused filenames; merge only approved metadata relationships without overwriting conflicting provenance or rights evidence.
- [ ] **C03.15.04** Keep temporary/partial files outside approved manifests and served roots; file naming alone cannot authorize publication before checksum and catalog readiness checks succeed.
- [ ] **C03.15.05** Interrupt a large local import and resume it; verify final checksum, asset identity, ingestion history, and dependency records match an uninterrupted reference import.
- [ ] **C03.15.06** Import identical bytes under multiple names and changed bytes under one reused name; confirm deterministic duplicate detection and preservation of distinct original identities when necessary.
- [ ] **C03.15.07** Inject checksum mismatch, missing source, disk exhaustion, and abandoned partial jobs; block publication and provide attributable retry/cleanup procedures that leave verified originals intact.
- [ ] **C03.15.08** Archive import-state traces and duplicate/integrity reconciliation; accept only when every published original is fully verified and no incomplete file can enter a dossier manifest.

### Control C03 16

**Original requirement C03.16:** Provide informative substitutions for unavailable imagery; do not silently substitute an unrelated photograph or obscure an exact-location coverage gap.

- [ ] **C03.16.01** Define unavailable-image states and substitution options covering missing files, revoked rights, corruption, absent exact coverage, unsupported formats, and incomplete geographic associations.
- [ ] **C03.16.02** Select fallback text, maps, or reviewed representative imagery using explicit stage relevance and rights rules; never infer equivalent geographic accuracy from visual similarity.
- [ ] **C03.16.03** Display the reason for unavailable imagery and the substitute's actual representation class; preserve an exact-location coverage gap even when a regional image is usable.
- [ ] **C03.16.04** Keep essential assignment, choice, lesson, and journal interactions available despite gallery failure; ensure alternative content carries meaningful descriptions and accessible presentation.
- [ ] **C03.16.05** Remove the exact-location hero image from a sample dossier; verify the fallback identifies missing coverage and does not claim the replacement depicts that location.
- [ ] **C03.16.06** Attempt unrelated-region and undisclosed illustrative substitutions; reject them through editorial/dependency validation while retaining the original missing-image condition for responsible review.
- [ ] **C03.16.07** Restore the original or approve a new substitute through versioned replacement; reconcile current delivery and historical references without silently changing completed gallery provenance.
- [ ] **C03.16.08** Archive fallback scenarios and geographic review decisions; accept only when all unavailable-image states remain informative and every substitute has disclosed, supported relevance and permitted use.

### Control C03 17

**Original requirement C03.17:** Propagate expiry, revocation, deletion, and replacement across dossiers, delivery manifests, caches, and exports under application control; document limits of recalling already exported material.

- [ ] **C03.17.01** Define expiry/revocation/removal events with asset/grant identity, effective time, affected renditions, replacement, reason, owner, and application-controlled recall scope versus independent-copy limitations.
- [ ] **C03.17.02** Maintain reverse dependency indexes for dossiers, manifests, caches, exports, and current galleries; compute the full impact before executing any withdrawal or replacement action.
- [ ] **C03.17.03** Disable prohibited current delivery and rebuild or invalidate controlled packages/caches; preserve evidence and historical references without continuing to expose withdrawn bytes where removal is required.
- [ ] **C03.17.04** Specify notification/annotation and replacement behavior for previously exported material; record independent copies as beyond application control rather than claiming complete recall or deletion.
- [ ] **C03.17.05** Expire and revoke test grants with active dependencies; verify every controlled delivery/export route blocks the affected assets or adopts an approved correctly credited substitute.
- [ ] **C03.17.06** Open cached galleries and old package URLs after removal; require revalidation or denial and verify stale clients cannot restore a prohibited current rendition.
- [ ] **C03.17.07** Interrupt propagation and restart the service; resume from a durable affected-dependency ledger and reconcile completed actions without deleting unrelated images or campaign state.
- [ ] **C03.17.08** Archive impact counts, cache/export checks, and recall limitations; accept only when all controlled dependencies obey the event and unresolved independent-copy limits are explicitly documented.

### Control C03 18

**Original requirement C03.18:** Report coverage by stage, region, season, representation, accessibility, rights, and verified local-file availability; identify missing files after repository relocation and assign owners to coverage gaps.

- [ ] **C03.18.01** Define coverage report dimensions for stage, region, season, representation class, accessibility completeness, effective rights, and verified local-file availability with explicit denominator definitions.
- [ ] **C03.18.02** Generate coverage from the released route itinerary and media catalog versions; distinguish catalog entries from physically available, rights-valid, deliverable files under approved local roots.
- [ ] **C03.18.03** Report exact-location coverage separately from representative and illustrative substitutes; count unknown seasons and incomplete descriptions explicitly rather than folding them into verified coverage.
- [ ] **C03.18.04** Assign an accountable owner, severity, remediation target, and disposition to each material gap; link reports to affected stage/dossier publication decisions and honest coverage statements.
- [ ] **C03.18.05** Relocate a test repository and run file verification; identify missing originals/renditions without depending on stale absolute paths or previously populated browser caches.
- [ ] **C03.18.06** Seed absent files, expired rights, missing alternative text, and representative-only stages; confirm each gap appears in the correct dimension with accurate affected counts.
- [ ] **C03.18.07** Repair or accept a gap and regenerate the report; preserve earlier release reports while confirming new coverage reflects verified files and effective permissions.
- [ ] **C03.18.08** Archive coverage reports and gap ownership decisions; accept only when all published stages are accounted for and every actionable media gap has a reviewed disposition.

### Control C03 19

**Original requirement C03.19:** Verify corrupt files, orientation, incorrect location links, absent credits, incompatible rights, expiration, interrupted local imports, path traversal, repository relocation, deleted files, and local delivery without internet.

- [ ] **C03.19.01** Build a media verification matrix covering corruption, orientation, incorrect associations, missing credits, incompatible/expired rights, interrupted imports, traversal, relocation, deletion, and internet-free delivery.
- [ ] **C03.19.02** Specify source bytes, catalog/grant versions, request paths, injected fault, expected delivery result, substitution label, and affected dependency counts before each case executes.
- [ ] **C03.19.03** Test complete decoding and orientation with deliberately corrupted and EXIF-rotated files; confirm unusable renditions never pass publication readiness or misleadingly replace verified imagery.
- [ ] **C03.19.04** Exercise geographic mismatches and credit/rights failures through actual dossier/export paths; verify blocking decisions and trace affected dependencies back to the responsible media record.
- [ ] **C03.19.05** Run encoded traversal, escaping-link, and relocated-root fixtures against loopback delivery; ensure private repository files remain inaccessible and valid relative assets still resolve.
- [ ] **C03.19.06** Interrupt imports at partial-write and final-copy boundaries, then delete approved files; verify checksum recovery, partial-file exclusion, and informative unavailable-media behavior after restart.
- [ ] **C03.19.07** Disconnect external internet and browse complete local galleries; confirm captions, credits, classifications, and required image alternatives remain usable without remote resource requests.
- [ ] **C03.19.08** Archive case results and reconciliation evidence; accept only when every listed failure is detected and recovery preserves rights, geographic truth, local-file boundaries, and asset identity.

### Control C03 20

**Original requirement C03.20:** Conduct visual and accessibility review of final gallery renditions, captions, alternative text, credit presentation, and mobile/tablet layouts; retain results with the release.

- [ ] **C03.20.01** Define final-gallery review scope covering actual served renditions, captions, alternative text, credits, classification labels, mobile/tablet layouts, zoom, focus, and interactive image controls.
- [ ] **C03.20.02** Select representative portrait, panoramic, sparse, historical, illustrative, and geographically exact galleries from the candidate release; retain exact asset/template versions and viewing dimensions.
- [ ] **C03.20.03** Inspect primary images for correct crop, orientation, clarity, and geographic context; verify visible captions and credits refer to the rendered rendition's approved asset.
- [ ] **C03.20.04** Review alternative descriptions with keyboard and representative screen reader; ensure essential location/representation meaning is understandable without seeing images and decorative choices are justified.
- [ ] **C03.20.05** Exercise mobile/tablet orientation changes, enlarged text, missing images, long credits, and gallery dialogs; confirm labels remain readable and controls remain reachable without overlap.
- [ ] **C03.20.06** Record defects by asset, template, viewport, severity, owner, and required correction; include misleading imagery and inaccessible controls as explicit release disposition items.
- [ ] **C03.20.07** Regenerate or edit affected presentation and repeat the relevant final-view checks; verify repairs preserve rights, metadata, approved geographic associations, and accessible equivalents.
- [ ] **C03.20.08** Archive final rendered samples and reviewer acceptance with the release; accept only when every selected gallery passes declared visual/accessibility criteria or has a bounded approved exception.

## C04 Training planner

**Accountable owner:** Training Product Lead. **Technical owner:** Application Engineering. **Reviewers:** Accessibility, Privacy, and a qualified reviewer for any supplied training guidance. **Interfaces:** Loopback service and repository-local SQLite; user preferences and equipment profile; persisted route/dossier planner; workout logger; progression engine; dashboard; notification preferences.

**Required evidence:** Versioned SQLite schemas and metric dictionary; two-calendar specification; assignment-state transition table; sample reviewed/user-authored plans; equipment validation cases; stale-revision and restart demonstrations; accessibility results; reviewer disposition for supplied guidance.

**Exit criterion:** A user can create, reschedule, partially complete, and revise a plan through the local service, then relaunch and recover the committed version without changing completed records, duplicating actual activity, or allowing fictional events to modify physical targets.

### Control C04 01

**Original requirement C04.01:** Define repository-local SQLite records for `TrainingPlan` with stable ID, local profile, revision, author, optional reviewer and review scope, origin (`user_authored`, `imported`, `reviewed`), status, creation time, effective dates, goals, timezone, and referenced assignments. Preserve the plan version associated with each recorded workout; browser storage is not the authority.

- [ ] **C04.01.01** Specify the TrainingPlan schema with stable identity, local profile, revision, authorship, review scope, origin, lifecycle status, timestamps, effective dates, goals, and timezone.
- [ ] **C04.01.02** Create validated assignment references with foreign-key relationships to the applicable plan revision, preventing orphaned assignments and ambiguous ownership between local profiles or superseded plans.
- [ ] **C04.01.03** Implement origin and status enumerations, accepting absent optional reviewers while rejecting unknown origins, invalid effective-date ordering, missing authorship, and incompatible plan-state transitions.
- [ ] **C04.01.04** Persist accepted plan creation and revisions through service-owned SQLite transactions, returning the committed identity and revision rather than treating browser storage as successful authoritative persistence.
- [ ] **C04.01.05** Pin applicable plan revisions to assigned workouts and historical assignment snapshots; preserve explicit null or unassigned relationships when valid activity has no associated plan.
- [ ] **C04.01.06** Exercise creation, import, optional review, and supersession using representative plans, confirming full field round-trip fidelity through the service and repository database after browser cache deletion.
- [ ] **C04.01.07** Interrupt plan persistence before and after commit, verifying no partial assignment relationships and a recoverable retry that returns the same effective plan mutation outcome.
- [ ] **C04.01.08** Inspect schema, API, and restart evidence; accept when assigned workouts resolve their historical plan revisions and valid unassigned workouts retain explicit null or unassigned relationships.

### Control C04 02

**Original requirement C04.02:** Define `TrainingAssignment` with stable ID, plan revision, activity category, scheduling representation, optional duration/distance targets, optional equipment prompts, preparation task, explicit completion rule, notes, and state. Distinguish missing targets from zero targets and avoid mandatory biometric fields.

- [ ] **C04.02.01** Define TrainingAssignment fields and requiredness for stable identity, plan revision, category, schedule representation, optional targets, equipment prompts, preparation task, completion rule, notes, and state.
- [ ] **C04.02.02** Represent missing duration or distance as null and explicit zero as a meaningful value, with separate validation paths and visible explanations in assignment editing and review.
- [ ] **C04.02.03** Specify completion-rule structures for activity, preparation, knowledge, and recovery categories, including evidence requirements and whether partial completion is accepted without fabricated physical measurements.
- [ ] **C04.02.04** Validate assignment membership against the referenced plan revision and reject conflicting categories, malformed scheduling representations, duplicate identities, or unsupported completion-rule types before database commitment.
- [ ] **C04.02.05** Provide editing and readback views that preserve optional prompts and notes without requiring biometric input, guessed targets, or invented equipment values for an otherwise valid assignment.
- [ ] **C04.02.06** Test assignments with no numeric targets, one target, multiple permitted targets, zero targets, and preparation-only evidence against independently defined completion expectations for each supported category.
- [ ] **C04.02.07** Verify assignment serialization and relaunch round trips preserve null-versus-zero distinctions, stable references, explicit completion rules, schedule representation, and the latest accepted assignment state.
- [ ] **C04.02.08** Review schema, fixture records, rendered forms, and completion evaluation results; reject release if absent targets acquire defaults or optional biometrics become mandatory participation fields.

### Control C04 03

**Original requirement C04.03:** Publish unit, precision, and range contracts for every quantity. Persist canonical values and original entered values/units, reject ambiguous conversions, and apply display rounding without changing the stored assignment or completion threshold.

- [ ] **C04.03.01** Publish a field-level quantity contract listing canonical units, accepted input units, supported precision, bounds, null semantics, and whether zero has a valid assignment meaning.
- [ ] **C04.03.02** Persist canonical values alongside the original entered number and units, retaining conversion policy identity so a reviewer can reconstruct the accepted physical target without display rounding.
- [ ] **C04.03.03** Implement explicit conversions with documented numeric representation and reject unrecognized unit strings, incompatible dimensions, ambiguous abbreviations, overflow, and values outside the declared assignment range.
- [ ] **C04.03.04** Apply display rounding solely in presentation, ensuring comparison and completion evaluation use the canonical stored target at its supported precision rather than rounded visible text.
- [ ] **C04.03.05** Provide validation messages that identify the quantity, entered unit, violated contract, and correction action without silently substituting a nearby supported or larger physical target.
- [ ] **C04.03.06** Calculate representative distance, duration, incline, and speed conversions independently, covering decimal inputs, boundary values, negative values, nulls, and exact threshold equality for enabled fields.
- [ ] **C04.03.07** Test editing and export round trips across display-unit changes, verifying unchanged canonical targets, original-entry provenance, and identical completion results before and after relaunch or browser refresh.
- [ ] **C04.03.08** Accept the conversion contract only with reviewed calculations, persisted-value inspection, and threshold evidence demonstrating that presentation precision cannot alter an assignment or its completion outcome.

### Control C04 04

**Original requirement C04.04:** Maintain two independent calendars: real training dates/times and fictional expedition days/stages. Persist an explicit mapping policy and `hike_day_id` relationships; elapsed real days, launcher executions, page views, and generated dossiers must not advance expedition days or modify workload.

- [ ] **C04.04.01** Create independent models for real training dates and fictional expedition days, linking assignments to hike_day_id only through an explicit versioned mapping policy with documented semantics.
- [ ] **C04.04.02** Store actual scheduling timestamps and timezone separately from itinerary day numbers, stage identity, route position, and the campaign's committed completion and next-leg references in SQLite.
- [ ] **C04.04.03** Define permitted assignment-to-day relationships for several real sessions, unassigned activity, preparation participation, and virtual rest days without inventing exercise from the existence of a mapping.
- [ ] **C04.04.04** Implement launch and page-read operations as state retrieval, ensuring they never update workload, mark assignments completed, or increment fictional day counters because a calendar date changed.
- [ ] **C04.04.05** Test midnight crossings, repeated launcher executions, dossier generation, clock changes, and browser refresh against a saved unfinished day, requiring unchanged assignment targets and committed itinerary position.
- [ ] **C04.04.06** Exercise explicit day completion and verify that only its accepted service transaction updates fictional chronology while actual workout dates and real training schedule remain independently preserved.
- [ ] **C04.04.07** Recover a campaign after service restart and cleared browser cache, comparing both calendars and mapping revisions with the committed database rather than client timestamps or remembered display state.
- [ ] **C04.04.08** Review schema relationships, timeline fixtures, and launch/completion evidence; accept only when every cross-calendar effect has an attributable policy and no passive event changes training workload.

### Control C04 05

**Original requirement C04.05:** Represent date-only tasks, local scheduled times, named timezones, recurring rules, exception dates, and rescheduling distinctly. Define behavior for nonexistent/repeated daylight-saving times and for travel between timezones.

- [ ] **C04.05.01** Define distinct schedule representations for date-only tasks, timezone-aware local times, recurrence rules, exception dates, and deliberate rescheduling, with unambiguous API validation and storage fields.
- [ ] **C04.05.02** Persist named timezones and intended local wall time for scheduled sessions, distinguishing an all-day preparation task from an instant inferred at local midnight without user intent.
- [ ] **C04.05.03** Specify nonexistent daylight-saving time handling with a visible edit or accepted adjustment path, preserving the original requested time and preventing silent movement of the training schedule.
- [ ] **C04.05.04** Define repeated-time disambiguation using an explicit offset or occurrence choice, retaining that choice so later rendering and execution select the same intended scheduled instant after restart.
- [ ] **C04.05.05** Document travel behavior for existing and future assignments, distinguishing schedules anchored to original timezone from user-approved local-time rescheduling without silently revising historical adherence dates.
- [ ] **C04.05.06** Expand recurrences deterministically with exceptions and revision identity, preventing duplicate assignments when date ranges overlap, the application relaunches, or the recurrence editor saves repeated requests.
- [ ] **C04.05.07** Test spring gaps, autumn repetitions, overnight sessions, leap dates, recurrence exclusions, and travel changes against independently constructed expected occurrences for date-only and timed assignments separately.
- [ ] **C04.05.08** Inspect persisted schedule provenance and accessible calendar/list output, accepting only when ambiguous cases are explicitly resolved and rescheduling retains attributable original and revised schedule histories.

### Control C04 06

**Original requirement C04.06:** Capture user-described availability, preferred session length, existing activity, goals, equipment, and chosen limits. Document each field's purpose and allow sensitive background details to remain absent; absence must not trigger an invented fitness baseline.

- [ ] **C04.06.01** Define optional profile fields for user-described availability, preferred session length, existing activity, preparation goals, equipment, and chosen limits, documenting the concrete purpose of each collected value.
- [ ] **C04.06.02** Separate scheduling preferences from authoritative physical assignments, ensuring preference changes do not automatically rewrite accepted targets, completion criteria, or workout history without deliberate plan acceptance.
- [ ] **C04.06.03** Provide manual entry and omission paths for sensitive background fields, explaining which optional details improve display or conflict checks without requiring medical or biometric information to participate.
- [ ] **C04.06.04** Validate supported availability structures and chosen limits without interpreting absent activity history as sedentary status, fitness capacity, or permission to generate an individualized physical training baseline.
- [ ] **C04.06.05** Display recorded equipment capabilities as supplied or unknown, retaining provenance and allowing correction instead of inferring speed, incline, endurance, or training tolerance from equipment model assumptions.
- [ ] **C04.06.06** Test empty, partially completed, conflicting, and updated profiles, requiring usable supplied-plan participation and explicit warnings only for conflicts supported by actual entered preferences or limits.
- [ ] **C04.06.07** Verify profile retention, deletion, and diagnostic redaction respect optional sensitivity classifications, and that removing background fields neither destroys workouts nor silently changes accepted assignment targets.
- [ ] **C04.06.08** Review collection wording, omission behavior, database records, and preference-change evidence with the product and training reviewers; accept only when no absent field creates an invented baseline.

### Control C04 07

**Original requirement C04.07:** Model walking, outdoor practice, equipment testing, knowledge activities, planning tasks, and recovery as distinct categories. Give each its own completion evidence; recovery or knowledge completion must never create fabricated walking distance.

- [ ] **C04.07.01** Define separate activity categories for walking, outdoor practice, equipment testing, knowledge, planning, and recovery, with stable category identifiers and domain-specific evidence and completion contracts.
- [ ] **C04.07.02** Specify walking evidence using actual reported or measured quantities, while equipment and outdoor practice allow observations or task records without inferring unsupported walking distance from participation.
- [ ] **C04.07.03** Define knowledge and planning completion using reviewed activity responses or explicit task evidence, retaining source content revisions and distinguishing participation from certification of wilderness competence.
- [ ] **C04.07.04** Represent recovery assignments with their accepted completion rule and narrative eligibility, allowing legitimate plan participation without generating moving-time, physical distance, or ascent values for recovery alone.
- [ ] **C04.07.05** Implement category-aware validation and aggregation so task completion records enter the appropriate preparation totals while only qualifying actual measurements contribute to physical walking and incline metrics.
- [ ] **C04.07.06** Test each category with complete, partial, missing, and incorrect evidence, requiring visible status and rejection of evidence that attempts to fabricate physical quantities from a preparation checkbox.
- [ ] **C04.07.07** Exercise campaign credit and dashboard integration for recovery and knowledge assignments, confirming separately labeled contributions and unchanged actual-distance totals after accepted task completion and service restart.
- [ ] **C04.07.08** Review category schema, evidence examples, calculation outputs, and export labels; accept only when every completion record identifies its category and no nonwalking task invents walking evidence.

### Control C04 08

**Original requirement C04.08:** Support user-authored plans and appropriately reviewed templates with identifiable scope and limitations. Do not generate individualized medical prescriptions or infer physical targets from fictional trail grade, weather, virtual fatigue, encounters, or pack weight.

- [ ] **C04.08.01** Provide a user-authored plan workflow with attributable author, origin, version, effective dates, explicit targets, and accepted completion rules rather than generating personalized physical assignments from story state.
- [ ] **C04.08.02** Define reviewed-template metadata including reviewer scope, intended context, source, limitations, and review status; expose these details before a user accepts the template into their local plan.
- [ ] **C04.08.03** Require imported or edited templates to retain their original provenance and distinguish reviewed source content from subsequent user changes that fall outside the documented review scope.
- [ ] **C04.08.04** Validate physical-target inputs against user-selected limits and supported equipment only, preventing fictional route grade, weather, fatigue, encounters, or pack weight from becoming training-prescription inputs.
- [ ] **C04.08.05** Review supplied guidance for unsupported diagnostic, treatment, injury-avoidance, or individualized medical claims, requiring corrected language and recorded limitations before template publication or acceptance.
- [ ] **C04.08.06** Run adversarial scenarios that change every fictional demand while holding the accepted plan constant, verifying identical physical duration, distance, speed, incline, and equipment prompts in the assignment.
- [ ] **C04.08.07** Test template withdrawal, missing review metadata, and unsupported contexts, providing qualified availability or rejection without silently substituting an invented plan or increasing targets to preserve story progression.
- [ ] **C04.08.08** Approve provenance records, scope explanations, content review, and negative boundary evidence; release only when each enabled plan path is attributable and fictional demands cannot create physical prescriptions.

### Control C04 09

**Original requirement C04.09:** Validate optional treadmill prompts against declared supported incline, decline, increment, and speed capabilities where known, plus user-selected limits. Unknown or unsupported capability must be shown for editing rather than silently replaced with a larger or different physical target.

- [ ] **C04.09.01** Define treadmill capability fields for supported speed, incline, decline, increments, and units, retaining whether values were user supplied, documented, unknown, or not applicable for the chosen equipment.
- [ ] **C04.09.02** Compare optional assignment prompts against both declared equipment capabilities and user-selected limits, preserving the accepted prompt and identifying the precise incompatible field before any proposed revision.
- [ ] **C04.09.03** Validate increment alignment with canonical precision, handling boundary speeds and incline values without rounding an unsupported prompt upward into a larger physical target or unsupported setting.
- [ ] **C04.09.04** Show unknown capabilities as requiring user review or editing where relevant, allowing the prompt to remain absent instead of inferring a safe maximum or substituting different physical work.
- [ ] **C04.09.05** Provide deliberate edits or prompt removal with original value, replacement value, rationale where supplied, expected revision, and user acceptance captured before the assignment changes in SQLite.
- [ ] **C04.09.06** Test absent decline support, fractional increments, unit conversions, minimum and maximum settings, unknown equipment, and user limits stricter than device capabilities against independently expected validation outcomes.
- [ ] **C04.09.07** Exercise equipment-profile changes and stale-tab prompt edits, confirming existing accepted targets remain unchanged until a reviewed revision commits and conflicting proposals remain visibly unresolved to the user.
- [ ] **C04.09.08** Inspect capability provenance, rejected-prompt evidence, UI explanations, and accepted-edit records; accept only when unsupported or unknown settings never become silent replacements or automatic treadmill commands.

### Control C04 10

**Original requirement C04.10:** Provide postponement, substitution, splitting, shortening, cancellation, and resequencing operations with revision history. Preserve completed assignment snapshots and the original schedule; a retrospective edit must not silently change historical adherence.

- [ ] **C04.10.01** Define postponement, substitution, splitting, shortening, cancellation, and resequencing requests with stable mutation identities, affected assignment revisions, original schedules, proposed outcomes, and explicit user acceptance when targets change.
- [ ] **C04.10.02** Retain original assignment and schedule snapshots alongside revision events, distinguishing future plan changes from retrospective corrections so completed historical adherence remains explainable and reproducible after editing.
- [ ] **C04.10.03** Implement splitting with explicit portions and workout references, preventing multiple replacement assignments from counting the same physical activity more than once or increasing total targets without acceptance.
- [ ] **C04.10.04** Validate substitution categories and completion rules, explaining equipment or task differences rather than silently converting missing capabilities into a guessed physical alternative or higher workload.
- [ ] **C04.10.05** Provide cancellation and resequencing semantics that preserve recorded actual activity and completed snapshots, leaving removed future work attributable rather than deleting evidence needed to understand prior schedules.
- [ ] **C04.10.06** Exercise each operation on planned, partial, and completed assignments, checking permitted transitions, target-change acceptance, historical status, and actual-quantity invariants against independently specified expected records.
- [ ] **C04.10.07** Interrupt a multi-assignment revision and retry after service restart, requiring atomic affected-record changes or documented recoverable status without half-applied schedules, duplicated replacements, or lost original snapshots.
- [ ] **C04.10.08** Review revision trails and adherence comparisons before and after retrospective edits; accept only when schedule changes are visible and historical completions retain their applicable accepted assignment versions.

### Control C04 11

**Original requirement C04.11:** Define assignment states and transitions for planned, in-progress, partial, completed, skipped, cancelled, and superseded work. Actual activity remains visible when completion criteria are unmet, and reassignment must not duplicate the underlying workout.

- [ ] **C04.11.01** Publish a state-transition table for planned, in-progress, partial, completed, skipped, cancelled, and superseded assignments, listing triggers, required evidence, authorized operations, and prohibited backward transitions.
- [ ] **C04.11.02** Define how accepted activity begins an assignment and how unmet completion rules yield partial status, preserving effective actual quantities even when assignment completion is unavailable or unsuccessful.
- [ ] **C04.11.03** Specify skipped and cancelled outcomes separately from supersession, retaining reasons where supplied and preventing these states from being represented as completed exercise or zero-valued measured workouts.
- [ ] **C04.11.04** Implement reassignment through stable underlying workout identities and explicit relationships, preserving one effective physical record when an activity contributes to a different accepted assignment or hike day.
- [ ] **C04.11.05** Validate transitions server-side using expected assignment revisions and current evidence, rejecting stale or unsupported requests without mutating workout quantities or partially applying downstream adherence changes.
- [ ] **C04.11.06** Test every allowed transition and representative forbidden pairs, including completed-to-planned edits, cancelled starts, partial-to-completed evidence, and superseded assignment references in historical views and exported records.
- [ ] **C04.11.07** Exercise repeated state requests, reassignment retries, and restart during dependent recalculation, requiring deduplicated effects and unchanged actual totals even when assignment-status refresh remains pending or unavailable.
- [ ] **C04.11.08** Inspect transition logs, displayed partial activity, unique workout references, and reconciliation results; accept only when status changes never erase real activity or duplicate it through reassignment.

### Control C04 12

**Original requirement C04.12:** Require deliberate acceptance of any proposed change to physical training targets. Explain affected assignments and values before commitment; missed sessions and game setbacks must not automatically increase subsequent targets or prescribe compensatory exercise.

- [ ] **C04.12.01** Define a proposed-target-change object containing affected assignment IDs, old and new quantities with units, effective dates, proposal origin, rationale, and expected plan revisions for deliberate review.
- [ ] **C04.12.02** Present all materially changed duration, distance, speed, incline, equipment, and completion fields before commitment, distinguishing accepted values from provisional suggestions and preserving the user's rejection option.
- [ ] **C04.12.03** Require a deliberate acceptance action bound to the displayed proposal revision; changing the proposal or stale underlying plan invalidates prior acceptance until the updated effects are reviewed.
- [ ] **C04.12.04** Persist acceptance and target revisions atomically through the local service, retaining actor, timestamp, mutation identity, and prior values so acceptance evidence survives relaunch and browser cache removal.
- [ ] **C04.12.05** Block missed-session, story-failure, resource-loss, and encounter rules from automatically increasing future targets, adding compensatory assignments, or accepting proposals through unrelated notification or narrative controls.
- [ ] **C04.12.06** Test accept, reject, abandon, repeated acceptance, and simultaneous edits with representative multi-assignment proposals, requiring exactly the reviewed changes and no hidden target modifications in the committed plan.
- [ ] **C04.12.07** Inject write failure and lost acknowledgement after acceptance, keeping failed proposals visibly unsaved while retries recover the committed result without applying the same target increase twice.
- [ ] **C04.12.08** Audit target-change provenance and adversarial game scenarios; accept only when every effective physical-target revision has explicit reviewable acceptance and no compensatory exercise is silently prescribed.

### Control C04 13

**Original requirement C04.13:** Detect schedule conflicts, unavailable equipment, and incompatible assignment requirements without resolving them through guessed substitutions. Allow partial completion and user-approved alternatives; do not block access to the story merely because optional details are absent.

- [ ] **C04.13.01** Specify detectable conflicts for overlapping scheduled sessions, unavailable declared equipment, incompatible assignment requirements, and user-selected availability limits, with evidence fields and severity tied to actual supplied data.
- [ ] **C04.13.02** Implement conflict detection as explainable findings rather than automatic substitutions, naming the conflicting assignments, equipment capabilities, scheduling intervals, or requirements and the values that caused the finding.
- [ ] **C04.13.03** Offer user-approved postponement, partial completion, prompt removal, or alternative assignments with previewed effects and revision history, leaving unresolved conflicts visible instead of guessing equivalent physical targets.
- [ ] **C04.13.04** Distinguish absent optional equipment or background details from proven incompatibility, preserving story access and manual participation without invented device capabilities or assumed training restrictions from missing profile fields.
- [ ] **C04.13.05** Validate conflict resolutions through accepted plan operations, ensuring replacement targets and schedules change only after deliberate approval while completed snapshots and underlying physical records retain their identities.
- [ ] **C04.13.06** Test overlapping times, impossible equipment settings, contradictory requirements, missing optional details, and a valid user-selected alternative, comparing findings and resulting assignments with expected conflicts and accepted outcomes.
- [ ] **C04.13.07** Exercise stale-tab resolution and service interruption, requiring rejected conflicting edits or recoverable proposals without losing the original schedule, duplicating assignments, or blocking unrelated pending story participation.
- [ ] **C04.13.08** Review conflict explanations, accessible resolution controls, and continuation scenarios; accept only when detected conflicts are actionable and optional missing data never becomes an unjustified story-access barrier.

### Control C04 14

**Original requirement C04.14:** Provide recovery and preparation participation rules that reward the accepted plan rather than a universal consecutive-day walking streak. Keep reminders configurable, suppress redundant notifications, and never treat a notification response as workout completion.

- [ ] **C04.14.01** Define participation credit rules for accepted recovery and preparation assignments, explicitly separating them from walking quantities and documenting which plan-specific adherence or narrative outcomes their evidence supports.
- [ ] **C04.14.02** Publish streak definitions based on accepted plan participation, including scheduled nonwalking days, partial work, skipped sessions, and gaps rather than assuming consecutive calendar-day walking is universally required.
- [ ] **C04.14.03** Provide configurable reminder enablement, timing, frequency, and category preferences, respecting timezone-aware schedules and user choices without rewriting assignments or generating additional exercise to sustain a streak.
- [ ] **C04.14.04** Deduplicate reminder identities across recurrence expansion, browser tabs, retries, and relaunches, suppressing redundant messages for already acknowledged, cancelled, postponed, or superseded occurrences under documented rules.
- [ ] **C04.14.05** Keep reminder acknowledgement distinct from assignment completion, requiring the accepted category-specific evidence and completion workflow before any recovery, preparation, or walking task becomes completed in authoritative records.
- [ ] **C04.14.06** Test recovery days, preparation-only participation, missed sessions, postponed reminders, and disabled notifications, verifying expected adherence treatment without fabricated distance, compensatory workload, or false task completion from acknowledgement.
- [ ] **C04.14.07** Exercise daylight-saving changes, long absences, duplicate delivery, and service restart against reminder history, requiring intelligible scheduling and suppressed repeated notices without advancing fictional chronology or real activity.
- [ ] **C04.14.08** Review reminder wording, streak explanations, stored evidence, and user interpretation; accept only when legitimate accepted-plan participation is represented accurately and achievement language does not demand additional exertion.

### Control C04 15

**Original requirement C04.15:** Submit plan changes to the loopback service with mutation IDs and expected revisions, and atomically persist them in SQLite before reporting success. Detect stale-tab edits and reject conflicting writes with a reload/reapply path. During service failure, label browser drafts unsaved; do not treat a local browser queue as canonical persistence.

- [ ] **C04.15.01** Define plan mutation requests with stable mutation ID, expected plan and assignment revisions, validated payload, and canonical response fields identifying committed revisions and durable save status.
- [ ] **C04.15.02** Implement atomic SQLite writes for related plan, assignment, schedule, and acceptance events, rolling back all affected records when validation, revision comparison, or persistence fails before commit.
- [ ] **C04.15.03** Enforce expected-revision checks server-side, rejecting stale-tab proposals with current authoritative values and a clear reload/reapply path that requires review of materially changed physical targets before acceptance.
- [ ] **C04.15.04** Return successful save acknowledgement only after the database commit, distinguishing request receipt, processing, conflict rejection, provisional draft retention, and failed durable persistence in the interface status.
- [ ] **C04.15.05** Retain browser drafts where feasible during service failure, labeling them unsaved and preventing their cached revisions from replacing committed plans or being treated as authoritative accepted target changes.
- [ ] **C04.15.06** Test two tabs editing the same assignment, duplicate retries, lost responses after commit, and invalid multi-record updates, verifying one effective mutation and preserved atomic relationships or explicit rejection.
- [ ] **C04.15.07** Inject database write failure, disk exhaustion, and service termination around transaction boundaries, then relaunch and reconcile draft proposals against committed revisions without silently applying conflicted or unaccepted changes.
- [ ] **C04.15.08** Review transaction evidence, uniqueness constraints, status rendering, and reload/reapply usability; accept only when acknowledged plans survive restart and every uncommitted browser draft remains visibly provisional and recoverable.

### Control C04 16

**Original requirement C04.16:** Provide keyboard-operable scheduling and a chronological list equivalent to the calendar. Announce errors, moved assignments, and changed dates; essential operations must not require dragging, color interpretation, or fine pointer control.

- [ ] **C04.16.01** Provide a chronological assignment list containing the same dates, categories, targets, statuses, and actions as the calendar, ensuring essential scheduling functions remain available without interpreting spatial calendar layout.
- [ ] **C04.16.02** Implement keyboard access for creating, editing, postponing, cancelling, splitting, and resequencing assignments, with visible focus, meaningful control labels, and predictable navigation through dialogs and conflict results.
- [ ] **C04.16.03** Offer direct date and time entry or accessible picker controls for moving assignments, preserving scheduling precision and timezone choices without requiring dragging or finely positioned pointer actions.
- [ ] **C04.16.04** Announce validation errors with field association and correction guidance, moving focus only when helpful and preserving entered values so failed submissions do not force users to reconstruct a draft.
- [ ] **C04.16.05** Expose moved assignments, changed dates, and revised targets through concise status announcements and updated list text, preventing silent successful mutations that are perceptible only through color or position changes.
- [ ] **C04.16.06** Test every essential scheduling workflow using keyboard alone and a screen reader, including errors, recurrence exceptions, stale conflicts, and acceptance dialogs with expected focus placement and retained context.
- [ ] **C04.16.07** Review enlarged text, high contrast, touch targets, and responsive layouts, confirming calendars and lists retain complete assignment information and actions without clipping, overlap, or reliance on color coding.
- [ ] **C04.16.08** Retain accessibility findings and repaired workflow evidence; accept only when calendar/list parity and announced schedule changes are verified for the release's supported browser and assistive-technology combinations.

### Control C04 17

**Original requirement C04.17:** Operate as a local profile without required cloud login. Protect repository-local data through documented filesystem/runtime access boundaries and loopback-origin validation; apply retention/deletion to optional background information, redact diagnostics, and export plan versions, schedules, units, completion rules, and relationships.

- [ ] **C04.17.01** Implement local-profile plan access without requiring registration, remote authentication, or internet, documenting the repository database and local configuration paths used for supplied plans and optional background information.
- [ ] **C04.17.02** Document filesystem and runtime access assumptions, identifying who can read local profile records and how the loopback service restricts origins and access to supported plan operations.
- [ ] **C04.17.03** Apply validation of browser origin and request context to plan mutations, testing rejected untrusted origins without weakening the manual local workflow or depending on a mandatory cloud authorization system.
- [ ] **C04.17.04** Define retention and deletion behavior for optional background fields separately from plan and workout provenance, making omitted or deleted sensitive information unavailable without inventing replacement profile values afterward.
- [ ] **C04.17.05** Redact profile details, optional sensitive notes, and private targets from diagnostics unless explicitly approved fields are required, retaining sufficient mutation and error identifiers for local failure investigation.
- [ ] **C04.17.06** Export plan revisions, schedules, original and canonical units, completion rules, authorship, review scope, and assignment/workout relationships in a documented portable structure with optional sensitive fields scoped deliberately.
- [ ] **C04.17.07** Test offline plan use, origin rejection, background-field deletion, and export round trips, verifying preserved committed plan relationships and no dependency on browser cache or external identity for continued participation.
- [ ] **C04.17.08** Review access documentation, redacted log samples, deletion evidence, and export fidelity; accept only when local privacy boundaries and optional sensitive-data handling match the enabled release configuration.

### Control C04 18

**Original requirement C04.18:** Verify plan/assignment schema validation, numeric conversion, absent targets, unsupported equipment, recurrence exceptions, date-only tasks, and daylight-saving boundaries with representative cases and independently calculated expected results.

- [ ] **C04.18.01** Construct independent schema fixtures covering required plan metadata, optional reviewer absence, invalid origin values, assignment relationships, absent numeric targets, explicit zeros, and unsupported completion-rule structures.
- [ ] **C04.18.02** Calculate expected canonical conversions independently for supported distance, duration, speed, and incline units, including decimal precision, exact thresholds, rounding boundaries, overflow, and rejected incompatible dimensions.
- [ ] **C04.18.03** Create equipment validation cases for unknown capabilities, unsupported decline, invalid increments, and user limits stricter than device ranges, specifying unchanged targets and visible edit-required outcomes.
- [ ] **C04.18.04** Build recurrence fixtures with exception dates, overlapping expansions, cancelled occurrences, and revision changes, requiring stable occurrence identities and no duplicated assignment creation from repeated evaluation or relaunch.
- [ ] **C04.18.05** Define date-only and timezone-aware expected schedules across daylight-saving gaps, repeated times, timezone travel, overnight sessions, and leap dates without inferring arbitrary local-midnight instants for all-day tasks.
- [ ] **C04.18.06** Run validation through both isolated rules and service persistence contracts, comparing rejected requests and accepted database records against independent expectations rather than checking only successful UI rendering.
- [ ] **C04.18.07** Verify negative fixtures leave no partial plan records, assignment references, accepted target changes, or authoritative browser-only state, and that accepted fixtures retain original entered values through reload and export.
- [ ] **C04.18.08** Retain fixture definitions, independent expected calculations, execution results, and resolved discrepancies; accept only when every named boundary category has reviewed positive and negative evidence for the selected release.

### Control C04 19

**Original requirement C04.19:** Verify service restart, stale browser revisions, database write failure, split/reassigned workouts, retrospective plan edits, postponed sessions, recovery completion, and proposed-plan acceptance. Demonstrate that relaunch reloads the persisted plan and unfinished day without changing physical-activity accounting or the fictional calendar.

- [ ] **C04.19.01** Create an integration campaign with accepted plan revisions, partial assignments, recovery tasks, postponed sessions, split activity, and an unfinished hike day, recording independently expected actual totals and calendar state.
- [ ] **C04.19.02** Restart the service and relaunch through CMD and PowerShell, verifying persisted plans and assignment states reload without generating workouts, increasing physical targets, or advancing the unfinished expedition day.
- [ ] **C04.19.03** Exercise stale-tab competing plan edits and database write failure, requiring explicit conflict or unsaved status, atomic preserved records, and a recoverable reload/reapply path with target-change acceptance retained.
- [ ] **C04.19.04** Split and reassign one workout across accepted assignments, comparing canonical allocations and dashboard totals to ensure each physical quantity is counted once despite multiple assignment or hike-day relationships.
- [ ] **C04.19.05** Apply retrospective plan edits and postponement, checking original schedule snapshots, completed adherence interpretation, accepted revision history, and unchanged previously recorded actual physical measurements after downstream recalculation completes.
- [ ] **C04.19.06** Complete recovery and preparation assignments using category-specific evidence, verifying legitimate plan participation without invented distance or moving time and with story availability preserved under the enabled progression policy.
- [ ] **C04.19.07** Accept, reject, and interrupt proposed-plan changes, confirming only reviewed committed targets become effective and lost acknowledgements or retries cannot bypass acceptance or duplicate assignment creation effects.
- [ ] **C04.19.08** Reconcile final database records, actual totals, real-calendar schedules, fictional-day references, and launch logs with initial expectations; retain integration evidence demonstrating passive launches and failures create no activity.

### Control C04 20

**Original requirement C04.20:** Complete accessibility review and content review for supplied guidance; record limitations and unresolved defects. Release only when no game event can increase an assignment and all target-changing operations have an explicit acceptance path.

- [ ] **C04.20.01** Review supplied guidance provenance, author attribution, template review scope, limitations, and accepted-plan origins, identifying unsupported individualized prescriptions or fictional-demand-derived physical targets as release-blocking content defects.
- [ ] **C04.20.02** Complete keyboard and screen-reader scheduling reviews covering calendar/list parity, target-change acceptance, conflict messages, date edits, and error recovery with retained drafts and meaningful focus placement.
- [ ] **C04.20.03** Inspect enlarged-text, contrast, responsive layouts, and pointer-free workflows, documenting defects that could conceal changed values or prevent deliberate acceptance of a proposed physical training revision.
- [ ] **C04.20.04** Trace every target-changing API and interface action to an explicit reviewed acceptance path, including imports, substitutions, retrospective edits, equipment conflicts, and stale-tab reload/reapply behavior for affected assignments.
- [ ] **C04.20.05** Run narrative boundary scenarios involving resource exhaustion, missed sessions, encounters, weather, fatigue, and failure, requiring unchanged accepted physical targets and no automatic treadmill command or compensatory assignment creation.
- [ ] **C04.20.06** Verify unresolved limitations and optional feature exclusions have accountable owners, rationale, affected release boundaries, and user-facing explanations where necessary rather than appearing as silently completed acceptance controls.
- [ ] **C04.20.07** Review persistence and recovery evidence for accepted plans, confirming acknowledged changes survive restart while rejected proposals and uncommitted drafts cannot become effective through browser cache restoration or relaunch.
- [ ] **C04.20.08** Approve release only after content and accessibility reviewers resolve blocking defects and sign the target-boundary evidence, acceptance-path inventory, and documented limitations for the exact supplied plan and application revisions.

## C05 Workout companion

**Accountable owner:** Workout Experience Lead. **Technical owner:** Frontend Engineering. **Reviewers:** Accessibility and Reliability. **Interfaces:** PowerShell-launched loopback service; authoritative SQLite session/day records; persisted daily dossiers/media; training planner; workout logger; encounter engine; progression engine.

**Required evidence:** Session/day state-machine specifications; interval-accounting examples; browser/service lifecycle matrix; SQLite checkpoint/recovery design; explicit completion transaction demonstrations; launcher resume/next-leg cases; media fallbacks; accessibility and treadmill-context usability results.

**Exit criterion:** The local application starts through its launcher, resumes an unfinished day, records actual activity durably, and advances to the correct future leg only after explicit day completion, including recovery after browser or service interruption.

### Control C05 01

**Original requirement C05.01:** Load a service-owned prepared-session snapshot containing `hike_day_id`, session ID when created, assignment/plan revisions, persisted dossier/content revisions, progression policy, source mode, user limits, and asset availability. Opening the launch URL displays or resumes the day; only an explicit start action begins a workout record.

- [ ] **C05.01.01** Define prepared-session snapshot fields for hike day, existing session identity, accepted assignment and plan revisions, persisted dossier versions, progression policy, source mode, user limits, and asset availability.
- [ ] **C05.01.02** Load the snapshot from the local service using committed campaign relationships, rejecting browser-created day identities or content revisions that do not resolve to the repository database and dossier manifest.
- [ ] **C05.01.03** Validate accepted assignment references and progression configuration before enabling start, showing unavailable or incompatible dependencies without substituting fictional targets or silently creating an alternative workout assignment.
- [ ] **C05.01.04** Open or resume the dossier as a read operation, recording permitted launch/view events separately and creating no workout record until a deliberate start action is accepted by the service.
- [ ] **C05.01.05** Reuse the active unfinished session identity when the snapshot indicates recording already began, preserving selected branches, pending interactions, and assignment revisions rather than allocating a second session on relaunch.
- [ ] **C05.01.06** Test first opening, repeated opening, unfinished-session resume, completed-day viewing, and missing assets, comparing created records and displayed references with independently expected read-versus-start effects in SQLite.
- [ ] **C05.01.07** Handle stale snapshots by retrieving current committed revisions before start, retaining intelligible status and requiring explicit reconciliation when accepted assignment or day state changed in another tab.
- [ ] **C05.01.08** Inspect snapshot responses, database relationships, start events, and launch logs; accept only when every companion view is attributable and browser opening alone cannot establish recorded exercise.

### Control C05 02

**Original requirement C05.02:** Specify states `ready`, `active`, `paused`, `interrupted`, `finishing`, and `completed`, with SQLite-persisted transition events and permitted revisions. Prevent competing browser tabs from independently recording the same active session; on relaunch resume the unfinished day/session instead of allocating another day.

- [ ] **C05.02.01** Specify ready, active, paused, interrupted, finishing, and completed states with allowed transitions, required evidence, expected revisions, and explicit actions that may create or finish a workout record.
- [ ] **C05.02.02** Persist each accepted transition event in SQLite with session identity, actor context, timestamp anchors, mutation identity, and resulting revision so the service owns authoritative recording state.
- [ ] **C05.02.03** Define active-session ownership or concurrency coordination across tabs, preventing simultaneous independent streams from allocating duplicate workout records or accepting conflicting interval transitions for the same session identity.
- [ ] **C05.02.04** Implement server-side transition validation, rejecting invalid state pairs, stale revisions, and attempts to reopen completed sessions without a documented correction workflow that preserves original recording history.
- [ ] **C05.02.05** Resume the existing unfinished session and hike day after relaunch, displaying its committed state and known observations rather than interpreting browser closure or launcher execution as session or day completion.
- [ ] **C05.02.06** Test all legal state transitions plus representative invalid and competing-tab transitions, checking exactly one effective session identity and correctly ordered persisted events after accepted requests commit in SQLite.
- [ ] **C05.02.07** Terminate the service during active, paused, and finishing states, then recover committed checkpoints and retry pending transitions without duplicate workouts, lost accepted events, or assumed continuous physical movement.
- [ ] **C05.02.08** Review the state diagram, event ledger, ownership evidence, and recovery results; accept only when every visible authoritative state resolves to a valid durable transition and committed session revision.

### Control C05 03

**Original requirement C05.03:** Define interval accounting on two axes: physical observation (`moving`, `stationary`, `unknown`) and application state (`active`, `paused`, `interrupted`). Elapsed duration equals moving + stationary + unknown; paused duration overlaps those observations and is not added to elapsed or subtracted from moving automatically.

- [ ] **C05.03.01** Define physical-observation intervals as moving, stationary, or unknown and application-state intervals as active, paused, or interrupted, with independent classifications over the same supported elapsed timeline.
- [ ] **C05.03.02** Specify elapsed accounting as the nonoverlapping physical partition sum, requiring moving plus stationary plus unknown to equal elapsed within the declared interval precision and coverage tolerance.
- [ ] **C05.03.03** Store application pause independently as overlapping state coverage, prohibiting addition to elapsed and automatic subtraction from moving when physical observation during pause is available or later supplied.
- [ ] **C05.03.04** Validate interval ordering, clipping, gaps, and physical overlap server-side, assigning uncovered physical periods unknown while allowing legitimate overlap between physical observations and application-state classifications in the ledger.
- [ ] **C05.03.05** Present both axes with explicit labels and reconciliation controls, ensuring users can distinguish an application pause from evidence that a treadmill stopped or walking ceased during that interval.
- [ ] **C05.03.06** Test continuous movement, stationary breaks, unknown gaps, movement during pause, and pause during an unknown interval against independently constructed interval unions and exact expected duration totals.
- [ ] **C05.03.07** Exercise source updates and later user reconciliation, requiring revised physical partitions to preserve independent pause duration and invalidate dependent calculations without inventing observed movement from timer state alone.
- [ ] **C05.03.08** Inspect interval records, duration formulas, visual summaries, and exports; accept only when every elapsed interval has one physical classification and application-state overlap is preserved without double counting.

### Control C05 04

**Original requirement C05.04:** Treat the application timer as evidence of elapsed application time, not evidence that the user walked. Manual confirmation or a valid measurement source establishes physical activity; where it is unobserved, retain an unknown interval or a labeled aggregate self-report.

- [ ] **C05.04.01** Label the companion timer as elapsed application time, documenting that an active timer, background heartbeat, or completed countdown does not independently establish walking duration, distance, or equipment usage.
- [ ] **C05.04.02** Define qualifying manual confirmations and measurement-source evidence for physical activity, retaining source identity, submitted quantities, coverage, and provenance rather than deriving movement merely from application-active intervals.
- [ ] **C05.04.03** Record physically unobserved periods as unknown, allowing a labeled aggregate self-report when the user cannot provide an interval partition without inventing per-second movement or stationary classifications afterward.
- [ ] **C05.04.04** Keep timer observations and actual workout measurements in separate fields, ensuring default form values and completion evaluation cannot silently promote elapsed application time into confirmed moving time.
- [ ] **C05.04.05** Provide clear finish-time reconciliation showing observed, self-reported, and unknown coverage, with explicit choices to leave quantities unavailable or supply actual activity evidence under the logger's validation rules.
- [ ] **C05.04.06** Test starting and leaving the timer active without any physical confirmation, requiring elapsed application records but no earned physical distance, moving duration, or assignment completion inferred from timer activity.
- [ ] **C05.04.07** Exercise valid manual and measured inputs alongside missing and stale evidence, comparing accepted physical quantities and uncertainty labels with the supplied source data rather than narrative pacing or countdown values.
- [ ] **C05.04.08** Review timer wording, evidence rules, committed workout records, and dashboard integration; accept only when every claimed actual activity quantity has qualifying evidence independent of timer execution alone.

### Control C05 05

**Original requirement C05.05:** Use a monotonic clock for intervals within a live recording runtime and wall-clock timestamps with recorded timezone for presentation and persisted anchors. On browser reload or service/process restart, load SQLite checkpoints and classify any unobserved gap as unknown rather than assuming continuous walking.

- [ ] **C05.05.01** Use a monotonic clock for intervals within the live recording runtime, defining precision and sampling behavior independently from wall-clock timestamps displayed to the user or received from the operating system.
- [ ] **C05.05.02** Persist wall-clock anchors with timezone, runtime identity, monotonic checkpoints where meaningful, and session revisions, recognizing that a prior process's monotonic origin cannot be directly compared after restart.
- [ ] **C05.05.03** Specify reconciliation after reload or process restart using committed checkpoint boundaries, classifying unobserved gaps unknown unless independent physical evidence or explicit user reporting supports a different observation.
- [ ] **C05.05.04** Detect clock jumps and timezone changes without producing negative intervals, shortening recorded movement, or adding distance; preserve original timestamp context and annotate discrepancies requiring review in recovered session history.
- [ ] **C05.05.05** Checkpoint timing through the service with expected revisions and durable acknowledgements, ensuring browser timer state is provisional until accepted and recoverable from the repository after client or server failure.
- [ ] **C05.05.06** Test forward and backward wall-clock changes during active and paused states, confirming monotonic live duration remains consistent while persisted presentation timestamps retain explainable timezone and discrepancy metadata.
- [ ] **C05.05.07** Exercise browser reload, service restart, device suspension, and lost checkpoint acknowledgement, requiring stable session identity, deduplicated accepted intervals, and unknown classification for every unsupported observation gap afterward.
- [ ] **C05.05.08** Inspect clock calculations, checkpoint records, discrepancy labels, and independently timed scenarios; accept only when restart cannot imply continuous walking or derive intervals from untrusted wall-clock differences alone.

### Control C05 06

**Original requirement C05.06:** Store source identity, freshness, accepted activity sequence, pending decisions, presentation position, `hike_day_id`, and durable-checkpoint revision in SQLite through the service. Associate the day with a validated persisted dossier; restarting must not regenerate a different authoritative narrative or lose the selected branch.

- [ ] **C05.06.01** Define persisted checkpoint fields for source identity and freshness, accepted activity sequence, pending decision identities, presentation position, hike day, and committed checkpoint revision linked to the current session.
- [ ] **C05.06.02** Associate each checkpoint with validated dossier and content manifest identities, preserving the exact published narrative, accepted assignment, progression policy, and selected branch that were active when the checkpoint committed.
- [ ] **C05.06.03** Store accepted activity sequence and presentation position independently so moving through pictures or captions cannot create physical activity records or change the ordering of accepted measurement evidence.
- [ ] **C05.06.04** Persist pending encounters and decisions through service transactions, retaining selected outcomes and explicit defer status instead of relying on browser memory or regenerating alternatives during resume or refresh.
- [ ] **C05.06.05** Validate checkpoint revision and source sequence ordering, rejecting stale writes or conflicting branches without discarding current committed choices or silently adopting a cached tab's obsolete session presentation state.
- [ ] **C05.06.06** Test relaunch with cleared browser cache and changed service port, comparing recovered day, source freshness, accepted sequence, pending decisions, presentation position, and selected branch with committed checkpoint records.
- [ ] **C05.06.07** Simulate missing or corrupt dossier files, requiring manifest-aware recovery or visible blocked availability without publishing a different authoritative story or changing established branch and completion history automatically.
- [ ] **C05.06.08** Review checkpoint schema, dossier references, sequence validation, and restart evidence; accept only when recovery reconstructs accepted session context and narrative continuity entirely from durable repository-owned records.

### Control C05 07

**Original requirement C05.07:** Explain that pausing the application does not establish whether the treadmill stopped. Allow later reconciliation of activity during a paused interval and preserve the independent pause and movement classifications.

- [ ] **C05.07.01** Explain beside pause controls that pausing the application records interface state and does not confirm the treadmill stopped, walking ceased, or physical recording became unavailable for that period.
- [ ] **C05.07.02** Persist pause and resume boundaries separately from movement observations, retaining timestamps, session revision, and interval identities so later reconciliation does not overwrite the original application-state history or duration.
- [ ] **C05.07.03** Provide reconciliation controls for activity observed or reported during pauses, allowing moving, stationary, unknown, or aggregate descriptions under the logger's supported evidence and precision rules for the interval.
- [ ] **C05.07.04** Validate supplied reconciliation against the affected pause interval and existing physical observations, preventing double-counted duration, overlapping movement assignments, or unsupported conversions from paused time to physical distance values.
- [ ] **C05.07.05** Display paused duration and physical classification with independent labels, including overlapping movement where supported, and preserve uncertainty where the user leaves the physically observed status unknown or unavailable.
- [ ] **C05.07.06** Test movement throughout pause, stationary throughout pause, partial movement during pause, and unresolved observation gaps against expected physical partitions while requiring unchanged independent application-pause duration in all cases.
- [ ] **C05.07.07** Exercise stale reconciliation edits and interrupted saves, keeping accepted classifications durable and conflicting or unsaved drafts visible without altering committed measurements or treating repeated requests as new interval evidence.
- [ ] **C05.07.08** Review interface wording, interval storage, calculations, and exports; accept only when pause remains an independent application-state observation and every physical reinterpretation has explicit attributable reconciliation evidence and history.

### Control C05 08

**Original requirement C05.08:** Handle background tabs, suspended devices, screen locks, browser timer throttling, and navigation. Reconstruct clock intervals without converting a background timeout into physical distance or declaring an unobserved gap stationary.

- [ ] **C05.08.01** Specify lifecycle handling for background tabs, page navigation, screen locks, suspended devices, timer throttling, and browser termination, identifying which application events and physical observations can remain reliably available.
- [ ] **C05.08.02** Capture committed checkpoints and relevant visibility or interruption events where feasible, retaining runtime identity and observation coverage rather than assuming timers execute continuously while the browser is backgrounded or suspended.
- [ ] **C05.08.03** Reconstruct elapsed intervals from valid anchors and evidence after return, preserving unknown gaps when no qualifying physical observation exists instead of declaring those intervals moving or stationary by default.
- [ ] **C05.08.04** Keep source-derived quantities independent from browser callback frequency, ensuring delayed heartbeats, accumulated timeouts, and re-rendering cannot repeatedly credit the same observed activity or fabricate distance during absent callbacks.
- [ ] **C05.08.05** Provide a return-to-session review showing interrupted application state, stale source status, unknown coverage, and recoverable decisions, requiring reconciliation before finalizing unsupported physical quantities into the authoritative workout record.
- [ ] **C05.08.06** Test each lifecycle interruption during active and paused sessions with and without valid external observations, comparing recovered interval partitions and actual quantities against independently known source evidence and gaps.
- [ ] **C05.08.07** Exercise navigation cancellation, browser closure, and service restart after background recording, requiring the same unfinished session and hike day to resume without workout completion or committed next-leg advancement.
- [ ] **C05.08.08** Review lifecycle logs, checkpoint recovery, timeout behavior, and uncertainty displays; accept only when unobserved background gaps remain explicitly unknown and no browser scheduling artifact becomes evidence of physical activity.

### Control C05 09

**Original requirement C05.09:** Provide large, stable controls for pause/resume, finish, audio, and display preferences. Preserve focus after changes, prevent click-through during overlays, and avoid essential controls moving when images or captions load.

- [ ] **C05.09.01** Specify stable placement and usable dimensions for pause/resume, finish, audio, and display controls across companion states, supported screens, and enlarged-text settings.
- [ ] **C05.09.02** Reserve space for images and captions so loading, missing assets, and long text cannot shift essential recording controls beneath an intended pointer action.
- [ ] **C05.09.03** Preserve meaningful focus after pause, resume, preference changes, and dialog closure, restoring the initiating control or a documented next action for keyboard users.
- [ ] **C05.09.04** Prevent overlay click-through and background activation while dialogs are open, containing focus and requiring deliberate confirmation before consequential finish or recording actions.
- [ ] **C05.09.05** Provide accessible names and distinguishable states for controls, ensuring icons, color, and transient messages never provide their only identification during normal session use.
- [ ] **C05.09.06** Test slow media, broken images, repeated clicks, overlays, and state changes, requiring stable controls and no accidental finish, duplicate transition, or hidden activation.
- [ ] **C05.09.07** Review keyboard, touch, magnified text, and treadmill-distance operation with representative users, assessing target separation, focus retention, control recognition, and accidental-dialog recovery.
- [ ] **C05.09.08** Retain interaction observations and repaired layout defects; accept only when every essential control remains reachable, understandable, and stable through supported content-loading and preference changes.

### Control C05 10

**Original requirement C05.10:** Defer substantive decisions until the user chooses to engage. Persist each pending encounter and provide a clear decide-later operation; decision timing must not silently increase, invalidate, or extend the physical workout assignment.

- [ ] **C05.10.01** Represent pending encounters with stable identity, content revision, trigger context, mandatory status, and permitted defer behavior independent from accepted assignments and actual workout evidence.
- [ ] **C05.10.02** Notify users that choices are available without requiring immediate response, preserving recording and allowing deliberate engagement at an appropriate time for their attention context.
- [ ] **C05.10.03** Provide decide-later actions that durably retain options and defer status through refresh, workout finish, browser closure, and subsequent resume of the same unfinished hike day.
- [ ] **C05.10.04** Prohibit decision timing from increasing, extending, or invalidating physical assignments, including automatic penalties or compensatory targets caused by ignored notices or narrative deadlines.
- [ ] **C05.10.05** Expose pending interaction counts and retrieval paths after finishing, distinguishing unresolved fictional-day eligibility from an actual workout that has already been successfully committed.
- [ ] **C05.10.06** Test ignore, engage, defer, revisit, and finish-with-pending cases, verifying unchanged physical targets, retained options, and no automatic choice derived from elapsed workout time.
- [ ] **C05.10.07** Exercise repeated triggers, stale-tab choices, and failed defer writes, requiring one effective interaction, preserved committed options, and explicit conflict or unsaved recovery status.
- [ ] **C05.10.08** Review attention demands and post-finish navigation; accept only when substantive choices remain accessible and successful recording never depends on immediate narrative interaction while exercising.

### Control C05 11

**Original requirement C05.11:** Preload appropriate photographs, captions, and audio within a documented cache budget. Provide geographic/context labels and meaningful asset-error fallbacks; avoid essential information solely in imagery or abrupt automatically playing audio.

- [ ] **C05.11.01** Define preload selection, ordering, file types, and byte budgets using the pinned dossier manifest, supported presentation modes, and locally available photographs, captions, and audio.
- [ ] **C05.11.02** Validate media references and preserve geographic/context labels, illustration classification, attribution, and essential textual information when a selected photograph or audio file is unavailable.
- [ ] **C05.11.03** Prioritize essential captions and controls within the cache budget, ensuring optional decorative asset loading cannot prevent durable recording or hide current session status.
- [ ] **C05.11.04** Provide meaningful failed-asset placeholders and retry controls, preserving instructions, decisions, context, and recording actions rather than displaying empty cards with inaccessible essential content.
- [ ] **C05.11.05** Require deliberate audio playback and configurable preferences, providing transcripts whenever spoken content conveys information and avoiding unexpected autoplay during launch, resume, or picture navigation.
- [ ] **C05.11.06** Test missing, corrupt, oversized, and offline assets, comparing preload usage and text fallbacks with the documented budget while preserving functional essential session controls.
- [ ] **C05.11.07** Clear caches and alter asset availability, requiring reload from pinned manifests rather than unrelated substitutions that change the authoritative narrative or published dossier context.
- [ ] **C05.11.08** Review budget measurements, labels, fallback views, and transcript coverage; accept only when essential information survives asset failures and audio remains deliberate and controllable.

### Control C05 12

**Original requirement C05.12:** Keep story outcomes confined to fictional state. The initial companion has no automatic treadmill-control command path; any equipment prompt must come from the accepted assignment and remain an optional, clearly identified user action.

- [ ] **C05.12.01** Document the initial companion's absent automatic treadmill-control path, inspecting runtime dependencies and equipment interfaces for executable speed, incline, decline, start, or stop operations.
- [ ] **C05.12.02** Bind equipment prompts exclusively to accepted assignment snapshots and plan revisions, retaining their authored values, source identity, supported capabilities, and user-selected physical limits.
- [ ] **C05.12.03** Label prompts as optional user actions and distinguish requested settings from achieved measurements, allowing nonresponse without fabricated observations, automatic equipment operation, or compensatory exercise.
- [ ] **C05.12.04** Restrict narrative outcomes to fictional-state mutations, rejecting event payloads or rule outputs containing physical-target overrides, executable equipment commands, or unauthorized assignment-change requests.
- [ ] **C05.12.05** Require deliberate accepted-plan revision when equipment context changes, showing original and proposed values instead of substituting unsupported settings or increasing workload to match fiction.
- [ ] **C05.12.06** Test storms, steep virtual terrain, exhaustion, random failure, and delayed choices, verifying unchanged accepted physical targets and no emitted equipment commands across companion states.
- [ ] **C05.12.07** Inject malformed narrative overrides, requiring rejection, redacted diagnostics, and preserved plans and workouts with a clear recoverable story-error state or reviewed content fallback.
- [ ] **C05.12.08** Review interfaces, prompt provenance, and boundary evidence; accept only when equipment instructions remain optional accepted-plan content and fictional consequences cannot change physical training values.

### Control C05 13

**Original requirement C05.13:** Show whether values are manual, measured, imported, or estimated and expose stale/unavailable readings. Prioritize actionable recording failures while rate-limiting repeated status messages and screen-reader announcements.

- [ ] **C05.13.01** Define manual, measured, imported, and estimated provenance labels with source identity, observation time, coverage, and quality metadata for every supported displayed actual quantity.
- [ ] **C05.13.02** Specify freshness thresholds and unavailable-source states, retaining last accepted readings with timestamps and stale labels rather than displaying outdated observations as current measured activity.
- [ ] **C05.13.03** Prioritize failed durable saves, revision conflicts, and source loss over optional media notices, ensuring users can identify and recover actionable canonical-recording failures during sessions.
- [ ] **C05.13.04** Rate-limit repeated notices by condition identity while announcing meaningful changes promptly, preserving an accessible status panel for detailed provenance, unsaved information, and recovery actions.
- [ ] **C05.13.05** Offer manual reconciliation or retained uncertainty for stale sources under published selection rules, prohibiting silent extrapolation or promotion of estimated readings into measured observations.
- [ ] **C05.13.06** Test mixed manual and measured fields, stale readings, missing imports, and estimated coverage, comparing selected values and labels against expected source evidence without duplicated quantities.
- [ ] **C05.13.07** Exercise repeated failures and reconnects with screen readers, verifying bounded announcements, persistent unsaved status, appropriate message priority, and clear recovery after committed database reconciliation.
- [ ] **C05.13.08** Review labels, freshness calculations, and notices; accept only when every value's origin and quality are discoverable and recording failures remain actionable without repetitive announcements.

### Control C05 14

**Original requirement C05.14:** Persist accepted checkpoints in SQLite transactions with mutation IDs and expected revisions, and report saved success only after commit. On write failure or disk exhaustion show unsaved state and retain a recoverable browser draft/export where possible; never advance authoritative progress from an uncommitted checkpoint.

- [ ] **C05.14.01** Define checkpoint requests with mutation identity, expected session revision, validated intervals and choices, and responses identifying the committed checkpoint and pending dependent evaluation status.
- [ ] **C05.14.02** Persist checkpoint changes and causal records atomically in SQLite, rejecting stale revisions or invalid partitions and deduplicating requests before they create effective observation or credit changes.
- [ ] **C05.14.03** Report saved status only after commit, distinguishing processing, conflicts, write failures, service loss, and provisional drafts without presenting request receipt or browser cache as persistence.
- [ ] **C05.14.04** On disk exhaustion preserve committed state, show affected unsaved observations, and retain recoverable browser drafts or exports where feasible with explicit provisional identity and status.
- [ ] **C05.14.05** Block uncommitted checkpoints from authoritative assignment completion, credit application, or next-leg advancement, requiring downstream evaluation to consume accepted database revisions rather than optimistic browser counters.
- [ ] **C05.14.06** Test accepted saves, invalid rollback, repeated requests, and lost acknowledgements, requiring one effective revision and preserved interval quantities, pending choices, and deduplicated causal effects.
- [ ] **C05.14.07** Terminate the service around commit and reconcile drafts after relaunch, preserving accepted observations, unknown gaps, and explicit conflicts without losing quantities or counting them twice.
- [ ] **C05.14.08** Review transaction and recovery evidence; accept only when acknowledged checkpoints survive restart and every provisional artifact remains distinct from effective workout, assignment, and campaign state.

### Control C05 15

**Original requirement C05.15:** Run locally with no internet once required dossier/media assets exist. Distinguish loss of external connectivity from loss of the loopback service: the latter prevents canonical mutations. Show local-service-unavailable status, retain provisional draft data if feasible, and reconcile against the database before resuming or finishing.

- [ ] **C05.15.01** Inventory local dossier, content, and media dependencies required for internet-free operation, recording enabled remote capabilities and their explicit deployment boundaries where optional external retrieval remains necessary.
- [ ] **C05.15.02** Disconnect internet with the loopback service healthy, verifying prepared-session retrieval, checkpoint commits, pending decisions, workout finish, and eligible explicit day completion using available repository-owned assets.
- [ ] **C05.15.03** Detect local-service loss separately from external connectivity loss, showing canonical mutation unavailability even when cached pages or internet resources remain accessible through the browser interface.
- [ ] **C05.15.04** Retain provisional drafts where feasible with session identity, expected revision, interval evidence, and choices, keeping them visibly unsaved without independently committing assignments, progress, or workouts.
- [ ] **C05.15.05** Reconcile drafts against current database revisions after reconnect, recovering duplicate committed outcomes or explicit conflicts rather than blindly replaying obsolete cached observations and narrative choices.
- [ ] **C05.15.06** Require durable reconciliation before resume or finish, exposing unknown gaps and unresolved edits without assuming physical movement continued throughout the outage or disconnected interval.
- [ ] **C05.15.07** Test internet loss, local termination, port changes, and delayed reconnect separately, comparing status, drafts, totals, and active-day references with expected service and asset availability.
- [ ] **C05.15.08** Review offline and reconnection evidence; accept only when supported local operation survives external disconnection and canonical service loss cannot produce false saves or completion outcomes.

### Control C05 16

**Original requirement C05.16:** Provide reduced motion, image captions, transcripts where audio is used, adjustable text, visible focus, readable contrast, and on-demand status. Verify that walking mode remains usable at typical treadmill viewing distances.

- [ ] **C05.16.01** Provide reduced-motion settings that remove nonessential animation while preserving state, controls, provenance, pending decisions, and progress meaning without requiring motion to understand essential information.
- [ ] **C05.16.02** Supply meaningful captions and alternative descriptions for imagery, preserving geographic/context classifications, and provide transcripts for audio containing assignment, decision, or recording-status information essential to participation.
- [ ] **C05.16.03** Support adjustable text without truncating targets, timers, captions, status, or recording controls, preserving semantic order and access at supported magnification settings and representative display sizes.
- [ ] **C05.16.04** Provide readable contrast, visible focus, and labeled controls across all session states, using text equivalents for unsaved data, stale sources, and unknown-observation coverage beyond color.
- [ ] **C05.16.05** Offer an on-demand summary of saved revision, source availability, uncertainty, pending decisions, and assignment context, supporting deliberate retrieval without continuous visual attention or repeated announcements.
- [ ] **C05.16.06** Test captions, transcripts, keyboard order, reduced motion, text enlargement, and asset failures, requiring usable recording and reconciliation workflows through presentation changes during active sessions.
- [ ] **C05.16.07** Review typical treadmill viewing conditions with documented display size, distance, and lighting, assessing recognition of status and deliberate pause/finish actions without precision pointing or small text.
- [ ] **C05.16.08** Retain review observations and repaired defects; accept only when essential information has accessible alternatives and walking-mode operation meets documented supported viewing conditions and practical usability limits.

### Control C05 17

**Original requirement C05.17:** Distinguish finish-workout from complete-hike-day. Finishing records one effective actual workout; explicit complete-day submits the day ID, expected revision, and idempotency key to the service transaction that commits eligible progress and the next-leg pointer. Launching, closing the browser, or previewing tomorrow never substitutes for either action.

- [ ] **C05.17.01** Define finish-workout and complete-hike-day as separate commands with distinct labels, prerequisites, expected revisions, mutation identities, and effects on actual activity versus committed fictional successor state.
- [ ] **C05.17.02** Commit finish-workout as one effective actual workout with accepted evidence and assignment references, retaining unresolved decisions and incomplete day requirements rather than automatically closing the fictional stage.
- [ ] **C05.17.03** Require complete-day requests to include day identity, expected revision, and idempotency key, validating evidence and decision status before atomically committing closure, causal effects, and successor.
- [ ] **C05.17.04** Show unresolved fictional requirements after successful workout finish with later engagement or permitted deferral, avoiding additional physical assignments or pressure to extend exercise to resolve narrative eligibility.
- [ ] **C05.17.05** Keep launches, browser closure, previews, generated dossiers, and refreshes separate from both commands, ensuring presentation availability never serves as evidence of actual exercise or explicit day completion.
- [ ] **C05.17.06** Test finish-only, invalid premature completion, finish-then-complete, pending decisions, and retries, requiring distinct records and an unchanged committed successor until that day's eligible explicit completion commits.
- [ ] **C05.17.07** Inject response loss and termination around both commands, then relaunch and verify precisely the accepted workout and day outcomes without duplicate activity, implicit completion, or extra next-leg advancement.
- [ ] **C05.17.08** Review command labels, atomic transactions, and recovery evidence; accept only when finishing records actual activity once and eligible explicit day completion alone advances committed campaign chronology.

### Control C05 18

**Original requirement C05.18:** Exercise reload, navigation, suspension, background throttling, and clock changes in every session state. Verify interval partitioning, paused-overlap semantics, unknown-gap handling, and no unearned movement or distance after recovery.

- [ ] **C05.18.01** Build a lifecycle matrix covering every session state against reload, navigation, suspension, throttling, and clock changes, using independently expected physical observations and application-state intervals.
- [ ] **C05.18.02** Specify expected moving, stationary, and unknown partitions with pause overlap and aggregate-only cases, requiring no movement or distance credit from application timer execution alone.
- [ ] **C05.18.03** Exercise reload and navigation with committed checkpoints and unsaved observations, checking retained session identity, branch context, draft status, and unknown classification for unsupported physical gaps.
- [ ] **C05.18.04** Simulate suspension, screen lock, and delayed callbacks, comparing recovered duration and physical classifications with known evidence rather than browser callback counts or accumulated timeout execution.
- [ ] **C05.18.05** Change clocks and timezones during recording, requiring valid monotonic durations, retained presentation context, nonnegative intervals, and discrepancy explanations without unearned activity or fictional advancement.
- [ ] **C05.18.06** Recover finishing requests and completed-session reloads, verifying mutation reuse, stable workout outcomes, and no second record or reopening of finalized intervals outside an explicit correction workflow.
- [ ] **C05.18.07** Compare companion, logger, dashboard, and exported totals with independent expectations after recovery, checking uncertainty labels and consistent paused-overlap semantics whenever source evidence remains incomplete.
- [ ] **C05.18.08** Retain matrix results and repaired defects; accept only when supported lifecycle/state combinations recover without invented movement, lost accepted observations, incorrect pause arithmetic, or passive completion.

### Control C05 19

**Original requirement C05.19:** Inject disk exhaustion, corrupt/missing persisted dossiers, service termination, response loss after commit, duplicate completion requests, stale-tab writes, and failure during day completion. Relaunch through the `.cmd`/PowerShell path and demonstrate unfinished-day resume or the committed next leg, with deduplicated effects.

- [ ] **C05.19.01** Define failpoints for disk exhaustion, dossier corruption, service termination, response loss, duplicate completion, stale writes, and interrupted day completion with independently expected durable outcomes.
- [ ] **C05.19.02** Inject checkpoint and workout failures around SQLite commit, verifying atomicity, unsaved status, recoverable drafts, and retries that neither lose accepted evidence nor duplicate actual quantities.
- [ ] **C05.19.03** Corrupt a referenced dossier while retaining its manifest, requiring validated recovery or unavailable status without randomized authoritative replacement, invented branches, or progress inferred from regenerated files.
- [ ] **C05.19.04** Submit stale-tab mutations and repeated finish/complete requests, requiring conflicts or deduplicated outcomes with preserved choices, one effective workout, and the appropriate explicit committed day result.
- [ ] **C05.19.05** Terminate completion before and after commit, checking closure, causal effects, and successor references agree with one atomic outcome rather than partial progression or mismatched campaign records.
- [ ] **C05.19.06** Relaunch every case through CMD and PowerShell, verifying owned readiness, distinct run logs, repository identity, and either the unfinished day or exactly the committed next leg.
- [ ] **C05.19.07** Reconcile actual totals, credits, decisions, resources, and next-leg references after recovery, demonstrating per-effect deduplication while retaining unknown gaps and conflicts requiring explicit user review.
- [ ] **C05.19.08** Retain failure and launcher evidence; accept only when recovery produces coherent durable outcomes and browser caches, file timestamps, or dossier availability cannot prove activity or day completion.

### Control C05 20

**Original requirement C05.20:** Perform keyboard, screen-reader, reduced-motion, magnified-text, and walking-context usability reviews. Verify that pending interactions remain available after finishing and that essential session actions do not require sustained visual attention.

- [ ] **C05.20.01** Review every session state with keyboard-only navigation, checking reachable controls, focus order, modal containment, visible focus, and context recovery after failures, deferrals, and accepted transitions.
- [ ] **C05.20.02** Use screen readers to assess assignment context, timer meaning, provenance, source loss, unsaved status, reconciliation, and choices, requiring accurate semantics and bounded actionable announcements.
- [ ] **C05.20.03** Test reduced motion and magnified text through media, overlays, and status changes, preserving stable controls, readable targets, and complete recording functionality without clipping or animation dependence.
- [ ] **C05.20.04** Conduct walking-context sessions at documented viewing distances and lighting, observing deliberate pause/finish actions and status recognition without sustained attention, while recording unsupported placement limitations.
- [ ] **C05.20.05** Finish with several pending interactions, verifying durable retrieval, preserved options, defer status, and camp navigation without repeating exercise or losing established narrative context after recording completes.
- [ ] **C05.20.06** Exercise failed-save and stale-tab recovery accessibly, requiring retained drafts, announced conflicts, understandable persistence status, and deliberate target-change acceptance without silent input loss or implicit completion.
- [ ] **C05.20.07** Review ambiguous wording, attention demands, and timer implications with accessibility and training owners, repairing blocking issues and documenting practical limitations for the exact companion/content release revisions.
- [ ] **C05.20.08** Accept only after essential actions pass supported accessibility and walking reviews, pending interactions remain usable after finish, and documented defects preserve authoritative recording and explicit day-completion boundaries.

## C06 Workout logger

**Accountable owner:** Activity Data Lead. **Technical owner:** Data/Application Engineering. **Reviewers:** Privacy and Quality Assurance. **Interfaces:** Loopback mutation API and repository-local SQLite; manual entry and workout companion; future source adapters; planner; progression ledger; dashboard; export/deletion services.

**Required evidence:** SQLite workout/interval schemas and constraints; source/metric dictionary; validation rules; revision/deletion specifications; arbitration policy; independently calculated sample ledger; stale-revision, retry, and process-restart tests; export/privacy review results.

**Exit criterion:** Every effective activity quantity has inspectable provenance, duplicates cannot inflate totals, corrections/deletions propagate consistently, and uncertain or fictional quantities cannot be displayed as measured physical activity.

### Control C06 01

**Original requirement C06.01:** Define authoritative SQLite `Workout` records with stable ID, local profile, `hike_day_id`, session identity, assignment snapshot/reference, source classification, timestamps/timezone, activity category, duration/distance fields, optional incline/effort/notes, revision, and commit status. Launch/view events belong to a separate event type and cannot create activity quantities.

- [ ] **C06.01.01** Specify Workout fields for identity, local profile, hike day, session, assignment reference, source, timestamps, timezone, category, measurements, optional observations, revision, and commit status.
- [ ] **C06.01.02** Create SQLite relationships to session and historical assignment snapshots, allowing explicitly unassigned activity while rejecting orphaned references or mismatched local-profile ownership before a workout mutation commits.
- [ ] **C06.01.03** Define required and nullable measurement fields, preserving absent distance, incline, or interval breakdown rather than populating unsupported zero quantities or guessed observations from session metadata.
- [ ] **C06.01.04** Represent launch and view events in separate record types with no physical quantities, preventing foreign-key shortcuts or shared constructors from creating workouts merely because dossiers open.
- [ ] **C06.01.05** Expose committed workout identity and revision through the local API, requiring validated canonical persistence before the interface reports recorded actual activity or downstream consumers aggregate its quantities.
- [ ] **C06.01.06** Test complete, minimal manual, preparation-category, imported, and interrupted records, verifying expected required fields, optional omissions, source classification, and assignment relationships in stored and retrieved SQLite rows.
- [ ] **C06.01.07** Relaunch and clear browser caches, requiring identical effective workout records and historical references while new run/view events leave actual quantities and workout count unchanged in all aggregate views.
- [ ] **C06.01.08** Review schema, constraints, validation evidence, and event separation; accept only when each actual quantity resolves to an effective workout and launch/view records cannot fabricate exercise.

### Control C06 02

**Original requirement C06.02:** Implement manual-first entry without requiring device pairing. Preserve entered values, units, and provenance; participation must not implicitly discriminate against manual entries unless an optional feature has explicit published eligibility rules.

- [ ] **C06.02.01** Provide manual workout creation and correction without device pairing, supporting category, timestamps, declared duration meaning, optional distance, and units through accessible local forms and service APIs.
- [ ] **C06.02.02** Persist original entered numbers and units alongside canonical values and manual provenance, retaining the user's definition when an aggregate duration lacks interval-level physical observation evidence.
- [ ] **C06.02.03** Permit missing optional measurements and notes without blocking valid participation, and avoid generating fictitious device identity, calibration metadata, or inferred sensor confidence for manually supplied activity.
- [ ] **C06.02.04** Validate manual quantities under the same published numeric contracts as other sources, showing explicit field errors rather than replacing unusual entries with guessed device-derived or expected training values.
- [ ] **C06.02.05** Define any optional source-specific eligibility restriction before enabling it, explaining affected rewards or import features without silently discounting manual records in ordinary physical-activity totals or plan participation.
- [ ] **C06.02.06** Test manual-only launch, recording, finish, correction, and export with no paired equipment, requiring usable workflows and faithfully preserved quantities, units, provenance, and accepted completion evidence.
- [ ] **C06.02.07** Compare otherwise equivalent manual and measured records across dashboard and campaign rules, verifying equal treatment unless a documented enabled eligibility rule explicitly explains the permitted difference to users.
- [ ] **C06.02.08** Review forms, database provenance, eligibility explanations, and offline evidence; accept only when device-free users can record valid activity and manual values remain attributable through revisions and exports.

### Control C06 03

**Original requirement C06.03:** Keep physical activity fields independent of campaign mileage, simulated ascent, virtual weather, fictional fatigue, and pack resources. A campaign correction must never overwrite the source workout's actual measurement.

- [ ] **C06.03.01** Define physical measurement fields independently from campaign distance, simulated ascent, fictional weather, fatigue, and resources, recording their separate schemas, owners, units, and permitted mutation paths.
- [ ] **C06.03.02** Bind actual workout values to manual or qualifying measurement sources, prohibiting progression outputs, virtual route properties, and story-state fields from serving as replacements for physical observations.
- [ ] **C06.03.03** Implement credit references to source workout revisions rather than copying virtual quantities back into actual distance, incline, duration, or achieved elevation fields during progression evaluation or campaign correction.
- [ ] **C06.03.04** Expose actual and fictional quantities with distinct API names and display labels, rejecting cross-domain payloads that attempt to update source measurements through campaign or narrative endpoints.
- [ ] **C06.03.05** Support campaign corrections as separate revision events, preserving effective physical values and provenance even when credits, route position, branches, or resource balances change under a revised fictional rule.
- [ ] **C06.03.06** Test scaled mileage, simulated ascent, virtual exhaustion, route changes, and resource depletion, requiring unchanged actual workout records and totals while only the intended fictional state is recalculated.
- [ ] **C06.03.07** Inject malformed campaign mutations targeting physical fields, requiring validation rejection, unchanged source revisions, and usable error recovery without partially applying narrative or workout modifications during failed requests.
- [ ] **C06.03.08** Review ownership contracts, database comparisons, and correction evidence; accept only when actual measurements remain independently attributable and every fictional correction preserves its originating physical record unless explicitly corrected separately.

### Control C06 04

**Original requirement C06.04:** Publish canonical duration accounting: elapsed = moving + stationary + unknown where interval evidence supports the partition; paused is an overlapping application-state duration. If only aggregate duration is supplied, preserve its self-reported definition and avoid fabricating an interval breakdown.

- [ ] **C06.04.01** Publish duration definitions for elapsed, moving, stationary, unknown, and overlapping application pause, identifying whether a record supports interval partitioning or only a self-reported aggregate duration.
- [ ] **C06.04.02** Persist physical interval coverage independently from application-state coverage, enforcing elapsed equals moving plus stationary plus unknown at canonical precision without adding or automatically subtracting paused duration.
- [ ] **C06.04.03** Store aggregate-only reports with their declared meaning and unavailable component breakdowns, prohibiting inference that all supplied elapsed minutes were moving or that absent observations were stationary.
- [ ] **C06.04.04** Validate interval timelines for ordering, duplicate segments, unsupported overlap, and gaps, classifying physically uncovered periods unknown while retaining legitimate pause overlap with any physical observation category.
- [ ] **C06.04.05** Provide accessible entry and readback for aggregate definitions and interval reconciliation, allowing users to retain uncertainty rather than demanding fabricated moving/stationary values to complete a valid manual record.
- [ ] **C06.04.06** Test observed partitions, movement during application pause, unknown pauses, and aggregate-only reports against independently constructed expected totals, requiring consistent formulas through logger, companion, dashboard, and export.
- [ ] **C06.04.07** Correct interval classifications and declared aggregate meaning, verifying revision history and dependent recalculation without accidentally duplicating elapsed duration or transforming a pause event into physical measurement evidence.
- [ ] **C06.04.08** Review duration contracts, stored coverage, and independent arithmetic; accept only when all presented breakdowns are supported and aggregate-only self-reports remain visibly distinct from measured interval partitions.

### Control C06 05

**Original requirement C06.05:** Define physical distance and incline metrics, canonical units, precision, rounding, source types, and confidence/quality classifications. Missing distance or incline is null/unavailable, and a zero value requires a recorded meaning.

- [ ] **C06.05.01** Define physical distance and incline quantities with canonical units, supported input units, precision, conversion rules, source classifications, and metric-specific quality or confidence labels in the dictionary.
- [ ] **C06.05.02** Persist original observations alongside canonical values, distinguishing user entries, device observations, imports, and estimates without inferring stronger measurement quality than the recorded source and coverage support.
- [ ] **C06.05.03** Represent missing distance and incline as null or unavailable, requiring explicit recorded meaning for zero values such as confirmed zero distance or an observed level interval where supported.
- [ ] **C06.05.04** Keep display rounding separate from storage and aggregation, ensuring unit changes cannot alter actual quantities, completion comparisons, selected source values, or derived incline coverage used by downstream consumers.
- [ ] **C06.05.05** Validate dimensions, finite values, allowed signs, and unit identifiers, preserving unusual but valid observations for explicit review rather than silently substituting expected equipment or training quantities.
- [ ] **C06.05.06** Test null, meaningful zero, fractional distances, incline percentages, supported alternative units, invalid dimensions, and exact precision boundaries against independent conversion and quality-classification expectations for every enabled field.
- [ ] **C06.05.07** Round-trip records through corrections, local restart, display-unit changes, and export, checking preserved original provenance, canonical values, null distinctions, and consistent precision across source and derived actual metrics.
- [ ] **C06.05.08** Review dictionary entries and calculation evidence; accept only when each displayed physical quantity identifies its definition and missing observations never become zero-valued measurements through storage or presentation defaults.

### Control C06 06

**Original requirement C06.06:** Store optional incline observations with interval duration, source, quality, and reported value. Requested incline is not achieved incline; virtual route ascent is not physical elevation gain; derived exposure requires a disclosed formula and coverage.

- [ ] **C06.06.01** Define incline observations with interval boundaries or duration, reported value, units, source identity, quality, and coverage, retaining optional status when no achieved incline evidence is available.
- [ ] **C06.06.02** Store requested equipment prompts separately from observed incline, preventing accepted assignment settings or the virtual trail profile from automatically creating achieved physical incline or elevation-gain measurements in workouts.
- [ ] **C06.06.03** Specify any derived incline exposure formula, canonical units, eligibility, supported assumptions, and minimum coverage, distinguishing time-weighted exposure from physical elevation gain unless adequate measurement evidence explicitly supports it.
- [ ] **C06.06.04** Represent missing or partial incline intervals as unavailable coverage, displaying the observed fraction and uncertainty rather than filling gaps from prompts, preceding readings, or virtual route ascent values.
- [ ] **C06.06.05** Validate interval durations, overlapping observations, finite incline values, declared device capabilities where relevant, and source changes without silently rewriting unusual achieved observations into planned settings or assumed equipment defaults.
- [ ] **C06.06.06** Test observed level, positive incline, supported decline, partial coverage, missing observations, and requested-only prompts, comparing derived exposure with independently calculated expectations and requiring no physical result from requested settings alone.
- [ ] **C06.06.07** Correct incline intervals and selected source observations, ensuring dependent metrics invalidate and recalculate with new coverage while historical requested prompts and virtual ascent remain independently preserved in their original domains.
- [ ] **C06.06.08** Review observation records, formulas, coverage labels, and actual-versus-requested examples; accept only when achieved incline metrics are attributable and virtual ascent or equipment prompts cannot masquerade as physical measurements.

### Control C06 07

**Original requirement C06.07:** Validate nonnegative quantities, ordered timestamps, moving time not exceeding elapsed time, interval overlap rules, numeric overflow, and unit conversions. Flag unusual values for review without replacing them with guessed corrections.

- [ ] **C06.07.01** Define validation rules for nonnegative supported quantities, timestamp order, moving duration bounds, physical interval overlap, numeric precision, overflow, and dimensionally valid unit conversions in the service contract.
- [ ] **C06.07.02** Validate canonical values after explicit conversion as well as original inputs, rejecting infinities, nonnumeric strings, unsupported precision overflow, and values whose converted representation violates the documented storage or domain bounds.
- [ ] **C06.07.03** Check moving does not exceed elapsed and interval partitions satisfy their supported definitions, handling aggregate-only reports separately rather than requiring fabricated components to pass evidence-based interval validation rules.
- [ ] **C06.07.04** Reject overlapping incompatible physical classifications and duplicate segments while permitting independent application-pause overlap, identifying the affected interval and corrective action in accessible validation messages returned to the logger.
- [ ] **C06.07.05** Flag unusual but valid quantities for deliberate review, retaining original values and source provenance without replacing them with guessed corrections, expected targets, device defaults, or statistically typical measurements.
- [ ] **C06.07.06** Test valid boundaries, negatives, reversed timestamps, moving-over-elapsed, overlap conflicts, conversion overflow, and unusual accepted values against independently defined validation expectations and canonical persisted results for all enabled measurement fields.
- [ ] **C06.07.07** Submit invalid multi-field records and stale corrections, requiring atomic rejection with no partial workouts, source observations, derived credits, or revision events that could change authoritative totals despite the failed validation.
- [ ] **C06.07.08** Review contracts, messages, rejected-write evidence, and accepted unusual records; accept only when validation preserves valid evidence and explains invalid data without silently guessing corrected physical quantities for the user.

### Control C06 08

**Original requirement C06.08:** Establish per-metric source arbitration for future imports. Treadmill and footpod measurements describing one activity must not be summed; retain secondary observations as provenance and explain selection changes.

- [ ] **C06.08.01** Publish per-metric source arbitration rules for enabled imports, specifying precedence, freshness, quality, coverage, and conditions requiring explicit user selection between conflicting observations of one activity.
- [ ] **C06.08.02** Group multiple device observations under stable activity identity where supported, distinguishing alternate measurements of one workout from genuinely separate activities that must retain independent physical totals.
- [ ] **C06.08.03** Select one effective source per metric, retaining secondary observations and exclusion reasons without summing treadmill and footpod distances or durations describing the same underlying workout.
- [ ] **C06.08.04** Preserve original source values, identifiers, timestamps, units, and supplied calibration context, allowing selection changes without destroying the alternate measurement evidence needed for later reconciliation or review.
- [ ] **C06.08.05** Explain changed selection with old and new sources, values, quality, and aggregate effects, requiring deliberate reconciliation when published rules cannot deterministically resolve conflicting valid observations.
- [ ] **C06.08.06** Test dual-source activity, different best sources per metric, stale readings, missing quantities, and distinct sessions, comparing chosen values with independent arbitration expectations and effective activity counts.
- [ ] **C06.08.07** Correct source quality or selection and verify durable revisions plus recalculation, preserving one effective workout while explaining actual-total changes caused by the accepted per-metric evidence change.
- [ ] **C06.08.08** Record import exclusions when disabled; otherwise retain policy, fixture results, provenance evidence, and ledger reconciliation before accepting multiple measurement sources in the enabled logger release.

### Control C06 09

**Original requirement C06.09:** Use stable source identifiers and request idempotency keys backed by SQLite uniqueness constraints. Deduplicate retry effects, including when a response is lost after commit; flag probable overlapping activities for reconciliation rather than merging solely on timestamp similarity.

- [ ] **C06.09.01** Define stable source identities and mutation keys for creation, import, correction, and retry, documenting their scope and relationships to effective workout identity and originating source revision.
- [ ] **C06.09.02** Enforce SQLite uniqueness for accepted mutation and source identities, retaining committed outcomes so duplicate requests return existing records rather than allocating additional workouts or physical quantities.
- [ ] **C06.09.03** Distinguish exact identity duplicates from probable timestamp overlaps, flagging uncertain cases without assuming similar time, quantity, or device context proves identical physical activity or safe automatic merging.
- [ ] **C06.09.04** Reject reused mutation keys with different payloads, preserving the original accepted record and explaining the conflict instead of overwriting it or misclassifying changed input as another retry.
- [ ] **C06.09.05** Provide overlap review with source references and quantities, allowing explicit keep-separate or duplicate-reconciliation decisions under recorded allocation rules rather than irreversible guessed deduplication during import.
- [ ] **C06.09.06** Test concurrent submissions, repeated imports, lost postcommit responses, and altered key reuse, requiring stable returned identities and one effective quantity set for identical causal requests.
- [ ] **C06.09.07** Interrupt ingestion around commit and replay after restart, checking uniqueness and stored outcomes recover accepted activity while uncertain overlaps remain unresolved and visibly available for deliberate reconciliation.
- [ ] **C06.09.08** Review constraints, request fixtures, and overlap decisions; accept only when exact retries have deduplicated effects and timestamp similarity alone cannot delete, merge, or multiply physical activity.

### Control C06 10

**Original requirement C06.10:** Preserve revisions/correction events with prior value, replacement value, actor, timestamp, optional reason, and effective revision. Audit retention follows the published privacy policy; indefinite retention is not an assumed requirement.

- [ ] **C06.10.01** Define correction events containing old and new values, affected fields, actor, timestamp, optional reason, source context, and effective revision tied to stable workout identity in SQLite.
- [ ] **C06.10.02** Require expected revisions and mutation identities for corrections, preserving unchanged source and assignment provenance unless accepted changes explicitly modify those relationships under the published correction rules.
- [ ] **C06.10.03** Record canonical replacements and original-entry units where relevant, enabling reconstruction of altered totals, completion evidence, or campaign credit without relying on stale browser snapshots or diagnostic messages.
- [ ] **C06.10.04** Publish audit retention periods and sensitive-field treatment, distinguishing minimal causal provenance from unlimited retention of private notes or biometric detail and applying approved removal to historical values.
- [ ] **C06.10.05** Show effective correction history and reasons, representing expired or privacy-redacted details as unavailable rather than implying full revision content remains recoverable after configured retention expiry or deletion.
- [ ] **C06.10.06** Test quantity, unit, source, and optional-reason corrections plus stale edits, requiring attributable revisions, preserved untouched fields, and atomic rejection of invalid or conflicting replacements before recalculation.
- [ ] **C06.10.07** Apply retention expiry and sensitive-field deletion to audit records, verifying coherent minimal references and removal of prohibited detail from managed history under the published lifecycle and restore policy.
- [ ] **C06.10.08** Review schemas, history displays, retention results, and exports; accept only when revisions explain effective values and retained private content matches the documented policy rather than indefinite assumptions.

### Control C06 11

**Original requirement C06.11:** Provide split, reassignment, and duplicate-reconciliation operations with explicit quantity-allocation rules. The sum of allocated portions must equal the effective original quantity within documented precision, and aggregates must count physical activity once.

- [ ] **C06.11.01** Define split, reassignment, and duplicate-reconciliation commands with affected identities, expected revisions, explicit allocations, relationship changes, canonical precision, and an accepted attributable decision through the local service.
- [ ] **C06.11.02** Specify conserved quantities and nullable allocation rules, requiring portions to equal effective originals within tolerance without distributing unavailable measurements as zeros or inventing unsupported duration partitions.
- [ ] **C06.11.03** Preserve underlying activity identity during reassignment, preventing multiple assignment or hike-day relationships from creating additional effective physical quantities merely because one workout contributes to different accepted tasks.
- [ ] **C06.11.04** Record duplicate reconciliation with surviving identity, excluded aliases or observations, and reasons, ensuring source and replacement records cannot both contribute the same physical activity after commitment.
- [ ] **C06.11.05** Validate conservation, ownership, category changes, and portion overlap atomically, rejecting stale or inconsistent requests before partial workout, assignment, credit, or aggregate changes become authoritative database state.
- [ ] **C06.11.06** Test unequal splits, residual fractions, reassignment, aliases, and distinct activities against an independent ledger, checking conserved physical quantities and effective counts rather than indiscriminately summing all stored rows.
- [ ] **C06.11.07** Retry operations and interrupt downstream processing, requiring stable portions, deduplicated effects, and recoverable recalculation without doubled activity, lost residuals, or changed effective allocations after local restart.
- [ ] **C06.11.08** Review formulas, queries, revision trails, and reconciliation evidence; accept only when operations conserve documented quantities and downstream actual totals count each underlying physical activity once.

### Control C06 12

**Original requirement C06.12:** Reconcile interrupted sessions and unknown periods through explicit user input or qualifying source evidence. Any extrapolation is separately labeled and must not masquerade as measured movement or distance.

- [ ] **C06.12.01** Identify interrupted periods with stable interval identities, time anchors, source availability, and unknown status, distinguishing unsupported physical gaps from independent application pause and evidence-backed stationary observations.
- [ ] **C06.12.02** Offer explicit reconciliation using declared interval or aggregate meaning, retaining user quantities, units, provenance, and uncertainty without converting elapsed application time or planned targets into actual walking evidence.
- [ ] **C06.12.03** Accept recovered source observations only under published coverage and arbitration rules, retaining source identity and sequence so repeated import or checkpoint replay cannot duplicate the reconciled physical quantities.
- [ ] **C06.12.04** Validate reconciled intervals against elapsed bounds and existing observations, rejecting overlap or duplicated distance while leaving unsupported portions unknown instead of guessing a complete movement partition for display.
- [ ] **C06.12.05** Store extrapolations as estimates with formula, assumptions, and coverage, prohibiting their presentation as measured movement or silent replacement of unavailable physical observations in dashboards and exports.
- [ ] **C06.12.06** Test unknown gaps, partial source recovery, aggregate reports, explicit stationary evidence, and extrapolation against independent totals, coverage, and classification expectations for each supported reconciliation method.
- [ ] **C06.12.07** Exercise stale edits, invalid evidence, response loss, and restart during reconciliation, preserving accepted revisions and unresolved gaps without duplicated observations or false saved status for provisional drafts.
- [ ] **C06.12.08** Review forms, references, estimate labels, and interval arithmetic; accept only when changed classifications have explicit evidence and unknown periods never become measured movement to satisfy display or campaign expectations.

### Control C06 13

**Original requirement C06.13:** Commit accepted record revisions with dependent invalidation/event records in the same SQLite transaction, or a documented recoverable transactional outbox. Track dependency versions so local consumers identify stale calculations and retry after process restart without losing a correction event.

- [ ] **C06.13.01** Map workout revisions to assignment status, credits, journals, and dashboard dependencies, recording source and calculation versions so consumers can identify obsolete results after correction or deletion.
- [ ] **C06.13.02** Choose atomic dependent updates or a SQLite transactional outbox, documenting durability boundaries, pending status, event ordering, and restart recovery ownership for accepted workout mutations and recalculation work.
- [ ] **C06.13.03** Commit source changes with required invalidation events, rolling back if event persistence fails so no acknowledged correction lacks a recoverable notification path to dependent canonical consumers.
- [ ] **C06.13.04** Deduplicate consumption by causal revision and effect identity, allowing repeated delivery without duplicate credit replacement, journal updates, or lost invalidation after a consumer retries interrupted processing.
- [ ] **C06.13.05** Mark derived results pending or stale when input revisions differ, preventing outdated totals or completion evidence from being presented as current authoritative outcomes before recalculation is accepted.
- [ ] **C06.13.06** Test corrections with multiple consumers, delayed processing, repeated events, and calculation failures, comparing eventual results with an independent ledger and requiring intelligible interim pending-state indicators.
- [ ] **C06.13.07** Terminate after source commit before downstream processing, then recover persisted events and verify all consumers reach consistent effective revisions without replaying quantities or advancing committed next-leg state.
- [ ] **C06.13.08** Review durability evidence, dependency queries, and recovery reconciliation; accept only when acknowledged source changes retain downstream work and stale calculations remain distinguishable from committed effective workout values.

### Control C06 14

**Original requirement C06.14:** Route entries/corrections through the local service with expected revisions and mutation IDs. Commit canonical values atomically before reporting success; reject stale-browser conflicts and recover pending server-side work on restart. If the service is unavailable, a retained browser draft remains visibly unsaved until reconciled and committed.

- [ ] **C06.14.01** Define entry and correction requests with mutation identity, expected workout revision, validated source payload, and committed response, requiring service validation rather than browser-created canonical records or cached persistence claims.
- [ ] **C06.14.02** Validate quantities, units, intervals, and relationships before atomic commitment, preserving original entries while ensuring invalid multi-field requests leave no partial workout or historical revision that contributes actual activity.
- [ ] **C06.14.03** Reject stale revisions with current effective values and an explicit reload/reapply path, preventing delayed drafts from overwriting accepted corrections, source selections, split allocations, or deletion decisions.
- [ ] **C06.14.04** Report successful save after commit with effective revision, distinguishing pending recalculation, provisional drafts, processing, service loss, and write failure so users can assess actual evidence persistence.
- [ ] **C06.14.05** Recover persisted server work using causal identities after restart, returning committed outcomes without requiring re-entry or multiplying physical quantities when an earlier durable response never reached the browser.
- [ ] **C06.14.06** Retain service-outage drafts as visibly unsaved and reconcile against current revisions before resubmission, prohibiting blind queue replay or provisional completion and credit claims without accepted database evidence.
- [ ] **C06.14.07** Test valid entries, corrections, stale conflicts, conversion failures, rejected writes, retries, and lost acknowledgements, requiring atomic records, deduplicated quantities, and clear statuses across restart and browser recovery.
- [ ] **C06.14.08** Review contracts, database evidence, status messages, and draft recovery; accept only when acknowledged records survive restart and rejected changes remain distinct from provisional drafts awaiting durable service commitment.

### Control C06 15

**Original requirement C06.15:** Separate optional perceived effort, notes, and biometric fields from required activity fields. Keep them in repository-local storage without required cloud accounts; document filesystem/profile access and loopback-origin protections, exclude sensitive detail from diagnostics, and make any future external export an explicit choice.

- [ ] **C06.15.01** Separate required activity fields from optional effort, notes, and biometrics, documenting purposes and permitting valid manual activity with all sensitive fields absent and no guessed replacements.
- [ ] **C06.15.02** Store enabled optional detail in repository-local records without required cloud accounts or external transmission for ordinary recording, correction, accepted-plan participation, and inspection of committed actual activity history.
- [ ] **C06.15.03** Document filesystem users, profile assumptions, runtime permissions, and loopback-origin access, explaining local protection boundaries without claiming confidentiality against every user able to access the host or repository.
- [ ] **C06.15.04** Validate origins and minimize exposed fields, rejecting untrusted mutations and preventing campaign or companion summaries from automatically receiving unrelated private notes and biometric values in underlying workout records.
- [ ] **C06.15.05** Redact sensitive content from diagnostics by default, retaining safe mutation identities and error categories for investigation without copying optional workout detail into launcher, server, browser, or managed support logs.
- [ ] **C06.15.06** Require deliberate scope and destination approval for future external exports, disclosing included fields and copy limitations rather than treating local participation as permission to share personal activity remotely.
- [ ] **C06.15.07** Test absent optional fields, redacted failures, denied origins, and narrow exports, requiring core recording functionality and no private content outside the selected permitted destinations and managed copies.
- [ ] **C06.15.08** Review schemas, collection wording, access documentation, logs, and export scope; accept only when optional sensitive detail remains omittable and locally governed without implicit sharing or remote identity requirements.

### Control C06 16

**Original requirement C06.16:** Export effective values with units, definitions, provenance, timestamps/timezone, assignment references, revision identifiers, and uncertainty. Define how omitted/deleted sensitive fields appear in exports and downstream campaign references.

- [ ] **C06.16.01** Define portable effective records with values, units, duration meaning, provenance, timestamps, timezone, assignment references, revisions, quality, and uncertainty rather than undocumented numbers detached from their source interpretation.
- [ ] **C06.16.02** Distinguish source records, derived summaries, and fictional references, documenting splits, duplicate exclusions, corrections, and aggregate reports so recipients can count physical activity once without treating secondary observations as additional workouts.
- [ ] **C06.16.03** Offer deliberate period and sensitive-field selection, retaining definitions and references while representing omitted notes, nulls, and privacy-redacted values honestly without manufacturing zero measurements or false collection claims.
- [ ] **C06.16.04** Specify representation of deleted sensitive detail and retained campaign provenance, preventing new exports from restoring private content through historical revisions, generated dossiers, or obsolete browser caches beyond retention permissions.
- [ ] **C06.16.05** Generate from committed revisions with format version, filters, generation time, and input coverage, excluding provisional browser entries and identifying pending calculations instead of silently exporting stale values as current authority.
- [ ] **C06.16.06** Test mixed units, nulls, zeros, aggregate reports, source changes, corrections, and splits against an independent ledger, requiring faithful definitions and provenance without duplicated secondary measurements in effective quantities.
- [ ] **C06.16.07** Exercise omission and deletion scopes, verifying current exports follow selected policy while explaining that unmanaged copied files remain separate artifacts outside verified application deletion and propagation coverage.
- [ ] **C06.16.08** Review format documentation, samples, traceability, and ledger agreement; accept only when exports distinguish missing, omitted, estimated, derived, and fictional values and faithfully reproduce effective actual records.

### Control C06 17

**Original requirement C06.17:** Implement deletion consistently across SQLite records, derived aggregates, generated journal/dossier references, and managed local exports/backups under the retention policy. Explain campaign-credit effects and preserved minimal provenance; never imply that an unmanaged copied export has also been deleted.

- [ ] **C06.17.01** Define deletion scope for values, sensitive fields, revisions, observations, and minimal provenance under the retention policy, avoiding assumptions of universal erasure or indefinite retention for all related content.
- [ ] **C06.17.02** Apply service-owned idempotent deletion with expected revisions, ensuring removed effective quantities no longer contribute actual totals or current workout evidence while permitted reduced references remain attributable and coherent.
- [ ] **C06.17.03** Propagate removal to derived totals and managed journal/dossier references with durable invalidation, showing pending state and preventing regeneration from restoring removed private detail through stale caches or historical content.
- [ ] **C06.17.04** Document managed export and backup treatment including expiry, invalidation, and restore-time deletion replay, identifying remaining recovery windows rather than claiming instant removal of every archival copy or physical storage trace.
- [ ] **C06.17.05** Explain credit recalculation and historical completion annotations before deletion, preventing removed sources from implicitly completing another day, advancing committed successor state, or silently rewriting established fictional branches.
- [ ] **C06.17.06** Test workouts, sensitive fields, split portions, duplicate aliases, and completed-dossier references, comparing effective totals and retained provenance with policy expectations after required propagation and dependent recalculation processing completes.
- [ ] **C06.17.07** Restart propagation and restore managed backups, requiring persistent tombstones or invalidations to prevent resurrection while explicitly excluding unmanaged copied exports from verified deletion results and success claims.
- [ ] **C06.17.08** Review database, aggregate, artifact, export, and backup evidence; accept only when managed deletion matches policy, limitations remain visible, and campaign effects preserve the explicit completion boundary.

### Control C06 18

**Original requirement C06.18:** Verify decimal conversions, absent values, zero values, invalid durations, overlapping intervals, aggregate-only manual reports, counter-reset imports, and mixed-source arbitration using known expected ledger results.

- [ ] **C06.18.01** Build independent ledger fixtures for decimal conversions, nulls, meaningful zeros, duration errors, physical overlap, paused overlap, and aggregate reports with expected canonical values and validation outcomes recorded beforehand.
- [ ] **C06.18.02** Calculate precision and conversion expectations independently for short distances, fractions, supported incline units, extreme inputs, and thresholds rather than reproducing implementation arithmetic as the assumed correct reference baseline.
- [ ] **C06.18.03** Specify null and zero source meanings, requiring queries, charts, and exports preserve unavailable-versus-observed distinctions without filling missing measurements from defaults, accepted prompts, or fictional route values.
- [ ] **C06.18.04** Test reversed anchors, moving-over-elapsed, overlapping physical classes, duplicate segments, and precision limits, requiring rejection while allowing legitimate independent application-pause overlap under the two-axis duration contract.
- [ ] **C06.18.05** Create aggregate-only self-reports with differing declared meanings, requiring retained definitions and absent partitions rather than invented movement breakdowns supplied merely to satisfy interval-based calculation or display expectations.
- [ ] **C06.18.06** Where enabled, test reset counters, device changes, repeated sequences, and conflicting sources against independent arbitration expectations, preventing overlap and resets from creating summed extra distance or duplicated duration.
- [ ] **C06.18.07** Run fixtures through validation, persistence, correction, dashboard, and export, checking ledger agreement and provenance; record disabled import scenarios with not-applicable rationale rather than claiming unimplemented behavior was verified.
- [ ] **C06.18.08** Retain expected ledgers, source decisions, results, and repaired discrepancies; accept only when physical quantities, uncertainty, interval semantics, and enabled imports match independent evidence without invented or duplicated activity.

### Control C06 19

**Original requirement C06.19:** Verify retry deduplication after lost responses, stale-tab revisions, split/merge accounting, service interruption, unknown-gap reconciliation, deletion propagation, and durable downstream recalculation. Include failpoints before/after SQLite commit and demonstrate that opening or relaunching a dossier records no invented workout.

- [ ] **C06.19.01** Define fault cases for lost responses, retries, stale tabs, splits, interruption, gaps, deletion, and recalculation with independently expected identities, quantities, revisions, and affected campaign references at each commit boundary.
- [ ] **C06.19.02** Inject creation and correction failures before and after commit, requiring atomic outcomes, clear unsaved or recovered status, and one effective record when acknowledgement loss triggers repeated client submissions.
- [ ] **C06.19.03** Exercise stale edits, reassignment, splits, and duplicate reconciliation, checking revision rejection, conservation, stable activity identities, and effective counts rather than summing superseded or allocated rows as independent physical workouts.
- [ ] **C06.19.04** Reconcile interrupted unknown periods with qualifying evidence, retaining pause independence and estimate labels without inventing moving duration, distance, or incline from active timers or unresolved browser drafts.
- [ ] **C06.19.05** Delete records during pending recalculation and restart, requiring persisted invalidation, coherent managed artifacts, no resurrected detail, and no committed successor advancement caused by source removal or credit recomputation.
- [ ] **C06.19.06** Terminate after source commit before downstream refresh, verifying recoverable assignment, credit, journal, dashboard, and export convergence to effective revisions while interim outdated values remain visibly pending or stale.
- [ ] **C06.19.07** Open and relaunch dossiers with caches cleared, requiring distinct run logs, stable unfinished-day continuation, unchanged workout quantities, and no exercise attributed to files, page navigation, or readiness checks.
- [ ] **C06.19.08** Retain fault and ledger evidence; accept only when accepted effects remain durable and deduplicated, rejected changes ineffective, unknown observations honest, deletion consistent, and passive opening creates no activity.

### Control C06 20

**Original requirement C06.20:** Audit schema access, export fidelity, diagnostic redaction, accessible entry/errors, and retention/deletion outcomes. Require reconciliation of every displayed actual total against effective source records before release.

- [ ] **C06.20.01** Audit schemas and service permissions for recording, correction, selection, deletion, and export, confirming local-profile and origin boundaries prevent campaign endpoints from rewriting measurements or optional sensitive fields.
- [ ] **C06.20.02** Reconcile every actual total to effective sources, allocations, revisions, formulas, and filters, identifying pending or unavailable results and excluding launches, prompts, virtual quantities, and uncommitted browser values.
- [ ] **C06.20.03** Audit export definitions, provenance, timezone, references, uncertainty, and sensitive scope against committed records, including aggregate reports, missing values, corrections, splits, and excluded duplicate observations in representative portable histories.
- [ ] **C06.20.04** Inspect launcher, service, browser, and failure logs for prohibited sensitive detail, preserving investigation identifiers while repairing leaks and applying documented retention cleanup to affected managed diagnostic copies.
- [ ] **C06.20.05** Review accessible entry and correction with keyboards and screen readers, requiring labels, units, retained drafts, actionable validation, source selection, conflict recovery, and understandable durable-save status across supported workflows.
- [ ] **C06.20.06** Exercise retention and deletion across effective records, permitted history, totals, dossiers, exports, and backups, verifying minimal provenance and no regenerated sensitive detail beyond documented restore and copy boundaries.
- [ ] **C06.20.07** Review unresolved defects with integrity, accessibility, and privacy owners, retaining exact release revisions and concrete reconciliation, export, redaction, and deletion evidence for attributable acceptance decisions and limitations.
- [ ] **C06.20.08** Accept only when actual totals reconcile, exports remain faithful, diagnostics meet policy, accessible entry succeeds, and retention/deletion outcomes are verified without concealing missing integrity or physical-training boundary controls.

## C07 Campaign progression engine

**Accountable owner:** Game Systems Lead. **Technical owner:** Application/Simulation Engineering. **Reviewers:** Activity Data and Training Product. **Interfaces:** Loopback service and SQLite campaign/day/credit records; effective workout revisions; assignment completions; persisted route/dossier registry; event/resource engines; campaign journal; dashboard; launcher resume resolver.

**Required evidence:** SQLite day/campaign/credit schema and constraints; dual-calendar mapping; earned-versus-committed position contract; progression policy; deterministic replay and surplus-credit fixtures; explicit completion transaction; dossier manifest/recovery design; launcher resume/next-leg cases; correction/migration and stale-branch demonstrations.

**Exit criterion:** Accepted contributions and explicit day completion atomically establish the authoritative history and next leg; relaunch always resumes the unfinished day or presents the committed successor, with no duplicate effects, invented exercise, concealed scaling, or physical-data contamination.

### Control C07 01

**Original requirement C07.01:** Define a versioned `ProgressionPolicy` with ID, mode, conversion parameters, eligible activity/task categories, completion thresholds, partial-credit behavior, rounding, time-order conventions, and correction rules. Preserve the policy used by each effective credit.

- [ ] **C07.01.01** Define ProgressionPolicy fields for stable identity, revision, mode, conversion parameters, eligible categories, thresholds, partial credit, rounding, event order, correction rules, and effective applicability.
- [ ] **C07.01.02** Validate mode-specific parameter schemas, rejecting incompatible units, unsupported activity categories, ambiguous thresholds, and missing correction semantics before a policy can generate effective campaign credits.
- [ ] **C07.01.03** Persist published policy versions immutably or through attributable revisions, retaining original definitions referenced by historical credits rather than replacing them when defaults or user preferences change.
- [ ] **C07.01.04** Require credit records to reference the exact evaluated policy revision, source revision, eligible evidence, and calculation context so conversion and completion meaning remain reconstructable after corrections.
- [ ] **C07.01.05** Explain active policy and prospective effects before participation, including eligible tasks, unavailable measurements, carryover, and the distinction between earned credit and explicit committed hike-day completion.
- [ ] **C07.01.06** Test representative valid and malformed policies plus threshold equality, partial activity, ineligible tasks, and unsupported modes against independently calculated expected credit results and rejection outcomes.
- [ ] **C07.01.07** Change default policy after existing activity, verifying prior credits preserve their original policy while new evaluations follow recorded effective dates or an explicit reviewed historical migration decision.
- [ ] **C07.01.08** Review schema, explanations, historical references, and calculation evidence; accept only when every effective credit has a valid attributable policy and no undisclosed parameter changes physical assignments.

### Control C07 02

**Original requirement C07.02:** Implement distance, chapter, and disclosed scaled progression as independent rule families. The selected rule is visible before participation; fictional terrain, pack weight, and character condition cannot covertly alter the physical-to-virtual conversion.

- [ ] **C07.02.01** Specify distance, chapter, and disclosed scaled modes as independent rule families with separate inputs, outputs, eligibility, completion semantics, and supported configuration for the selected release.
- [ ] **C07.02.02** Implement distance conversion using qualifying actual measurements and documented units, preserving unavailable physical distance rather than replacing it with timer duration, fictional grade, or planned workout targets.
- [ ] **C07.02.03** Define chapter credit using accepted activity or preparation evidence, distinguishing task contribution from actual walking quantities and requiring explicit day completion regardless of earned chapter eligibility.
- [ ] **C07.02.04** Publish scaled conversion factors and precision rules before activity, showing worked actual-to-virtual examples and preserving the selected factor revision in each effective source-derived campaign credit.
- [ ] **C07.02.05** Exclude fictional terrain, pack weight, weather, and character condition from undisclosed conversion inputs, rejecting narrative attempts to change physical-to-virtual ratios or accepted training targets automatically.
- [ ] **C07.02.06** Test identical activity across each enabled family against independent expected credits, including missing measurements, nonwalking tasks, partial participation, and unsupported category or mode combinations requiring rejection.
- [ ] **C07.02.07** Change story conditions while retaining activity and policy inputs, requiring identical conversion results and physical assignments even when fictional outcomes or resource balances differ across scenarios.
- [ ] **C07.02.08** Review mode contracts, user explanations, formulas, and negative tests; accept only when enabled families are independently understandable and displayed before credit is earned or policy changes take effect.

### Control C07 03

**Original requirement C07.03:** Model real training and fictional expedition chronology separately. Persist how several actual workouts/tasks contribute to one `hike_day_id`; explicit day completion advances fictional chronology according to policy. Launcher executions, elapsed calendar days, page views, and dossier generation do not complete stages or create exercise.

- [ ] **C07.03.01** Model actual workouts and preparation tasks with real timestamps separately from fictional hike-day identities and itinerary chronology, recording explicit source-to-day relationships in repository-owned SQLite state.
- [ ] **C07.03.02** Define how multiple real sessions contribute to one unfinished hike day, retaining their own dates, categories, evidence, and quantities without creating additional virtual days from the count of contributing records.
- [ ] **C07.03.03** Implement explicit completion as the authorized fictional chronology transition, leaving earned credit, workout finish, and accepted preparation contributions distinct from the active day's committed closure and successor.
- [ ] **C07.03.04** Log launches, views, and generation events independently, excluding them from physical activity and day-completion evaluators even when they include timestamps, dossier identities, or ready-to-view content manifests.
- [ ] **C07.03.05** Provide timeline labels showing which calendar governs each event, including absence, overnight workouts, partial sessions, virtual rest stages, and several actual participation dates mapped to one itinerary day.
- [ ] **C07.03.06** Test midnight changes, repeated launches, long absence, and dossier regeneration with an unfinished day, requiring unchanged committed stage position and no invented actual workout or completed assignment.
- [ ] **C07.03.07** Complete a day with several contributing sessions, verifying one attributable fictional transition while actual workout timestamps and the accepted real schedule remain independently unchanged after service restart.
- [ ] **C07.03.08** Review chronology queries, mapping records, and timeline evidence; accept only when every virtual transition has explicit accepted completion authority and passive calendar or presentation events produce no exercise.

### Control C07 04

**Original requirement C07.04:** Maintain a campaign-credit ledger independent of physical workout records. Each credit references its source record/revision, assignment completion where relevant, policy version, credited quantity, decision/evaluation context, and effective status. Earning or recalculating credit is distinct from committing a completed hike day or its successor.

- [ ] **C07.04.01** Define credit-ledger records containing source identity and revision, assignment evidence where relevant, policy version, credited quantity, evaluation context, effect identity, and effective status separate from Workout records.
- [ ] **C07.04.02** Create SQLite references and constraints that retain causal source lineage without storing virtual credits as physical measurements or treating copied ledger quantities as new actual distance, duration, or ascent.
- [ ] **C07.04.03** Record credit creation and replacement through service-owned transactions, preserving superseded evaluation evidence and preventing multiple effective entries for the same source revision, policy, and effect identity.
- [ ] **C07.04.04** Keep earning and recalculating credit distinct from hike-day completion, ensuring credit persistence cannot independently close the active day, create completed future days, or change committed successor state.
- [ ] **C07.04.05** Expose ledger explanations with source, formula, eligible category, effective quantity, and corrections, allowing users to inspect excluded or superseded entries without confusing them with additional physical activity.
- [ ] **C07.04.06** Test credit from manual walking, recovery, preparation, corrections, and ineligible records, comparing effective virtual quantities and source references with an independently constructed campaign ledger and actual totals.
- [ ] **C07.04.07** Replay ledger evaluation after response loss and service restart, requiring deduplicated effective entries and preserved pending completion requirements without duplicated rewards, decisions, or committed next-leg movement.
- [ ] **C07.04.08** Review ledger schema, identity constraints, explanations, and reconciliations; accept only when credits are attributable and independent from actual measurement records and the sole explicit day-completion operation.

### Control C07 05

**Original requirement C07.05:** Identify campaign position by route release, itinerary version, day/stage, direction, and within-stage chainage. Persist earned within-stage position/carryover separately from the last committed completion and next-leg reference in SQLite. Only explicit `CompleteDay` advances that committed pointer; actual distance, virtual distance, skips, repeats, and transport remain separate.

- [ ] **C07.05.01** Define campaign position using route release, itinerary revision, hike day or stage, direction, and canonical within-stage chainage, preventing ambiguous identification by display mileage or mutable stage names.
- [ ] **C07.05.02** Persist earned position and residual carryover separately from completed-day history and committed next-leg reference, documenting which services may update each field through accepted ledger or completion operations.
- [ ] **C07.05.03** Represent actual distance, virtual distance, skipped sections, repeated sections, and transport as distinct records or quantities, preserving their meanings in position explanations, dashboards, and portable campaign exports.
- [ ] **C07.05.04** Limit committed advancement to later legs to explicit CompleteDay; permit audited coordinate remapping or repair only while preserving equivalent saved continuation and established completion history.
- [ ] **C07.05.05** Validate route identity, direction, and chainage bounds when accepting position changes, retaining excess credit under policy instead of discarding it or interpreting overflow as completed intervening days.
- [ ] **C07.05.06** Test exact boundaries, reverse direction, transport, repeats, and surplus credit, comparing earned and committed positions with independent expected records while requiring no automatic future-day completion from carryover.
- [ ] **C07.05.07** Restart with incomplete earned progress and a persisted successor, verifying launch resumes the unfinished day or resolves exactly the committed next leg using database state rather than browser mileage.
- [ ] **C07.05.08** Review position schema, pointer-write ownership, and reconciliation evidence; accept only when earned progress and committed itinerary continuation remain separately inspectable and each successor change has explicit completion causality.

### Control C07 06

**Original requirement C07.06:** Use a documented numeric representation with bounded rounding error and carry residual fractions forward. Many short workouts must produce the same credit as their combined equivalent within the stated tolerance.

- [ ] **C07.06.01** Select a documented numeric representation for actual-to-virtual conversion, recording units, scale, maximum range, precision, rounding mode, residual storage, and permitted cumulative error in the progression policy.
- [ ] **C07.06.02** Retain fractional residuals between evaluations rather than rounding each short session independently, ensuring discarded display digits cannot repeatedly remove or add earned credit across many small workouts.
- [ ] **C07.06.03** Perform threshold comparisons using canonical values and residuals, leaving presentation rounding outside route eligibility, chapter completion evaluation, within-stage position, and carryover allocation decisions for accepted credits.
- [ ] **C07.06.04** Define overflow and invalid-number rejection before mutation, preserving prior ledger state and returning actionable validation instead of saturating values or creating unsupported multi-stage advancement from malformed calculations.
- [ ] **C07.06.05** Construct independent expected calculations for many short sessions, their combined equivalent, fractional conversions, exact thresholds, near-threshold values, and mixed supported units under each enabled mode.
- [ ] **C07.06.06** Run partition-invariance checks and require equivalent effective credit within the stated tolerance regardless of how qualifying activity is split into accepted source records or displayed to the user.
- [ ] **C07.06.07** Apply corrections and policy-version replay with residuals, verifying stable totals, conserved excess credit, and no lost fraction or cumulative rounding drift after interruption, restart, and repeated evaluation requests.
- [ ] **C07.06.08** Review representation decisions, independent arithmetic, residual records, and tolerance results; accept only when all enabled conversions meet bounds and rounding cannot silently change committed day or successor state.

### Control C07 07

**Original requirement C07.07:** Define deterministic evaluation inputs and event ordering. Identical effective records, policy/content versions, and initial campaign state must produce identical progression; current server time and message arrival order cannot supply undisclosed outcomes.

- [ ] **C07.07.01** Define deterministic evaluator inputs including effective source revisions, policy and content versions, initial campaign state, eligible decision context, and any explicit authored ordering or random seed fields.
- [ ] **C07.07.02** Specify event ordering using stable persisted sequence or documented sort rules, defining tie resolution and correction precedence independently from request arrival time, tab timing, and current server clock.
- [ ] **C07.07.03** Reject missing or incompatible pinned dependencies before evaluation, showing pending or unavailable status rather than generating undisclosed defaults, random outcomes, or current-time-dependent progression results for incomplete records.
- [ ] **C07.07.04** Keep deterministic progression evaluation separate from generation timestamps and presentation events, ensuring launch count, page refresh, media loading, or browser timer scheduling cannot alter evaluated campaign outcomes.
- [ ] **C07.07.05** Record evaluation context and version identities with resulting effects, allowing reviewers to replay source records and explain the exact ordering and rule inputs that produced an earned position.
- [ ] **C07.07.06** Replay identical datasets through reordered requests and different wall clocks, requiring identical effective credits, position, carryover, and eligible outcomes after documented ordering and deduplication rules are applied.
- [ ] **C07.07.07** Test tie cases, delayed corrections, out-of-order inputs, and retained explicit random seeds, comparing results with independent expected sequences and requiring visible conflict when unsupported ordering cannot be resolved deterministically.
- [ ] **C07.07.08** Review input contracts, replay evidence, and ordering explanations; accept only when identical supported inputs produce identical progression and no undisclosed timing signal controls credits or committed successor eligibility.

### Control C07 08

**Original requirement C07.08:** Implement per-effect idempotency through stable source revision and policy/effect identities or equivalent uniqueness constraints. Duplicate messages and retries may occur; credit, reward, milestone, and encounter effects must each be applied once for the effective causal event.

- [ ] **C07.08.01** Define stable causal identities per source revision, policy evaluation, and effect type, covering credits, rewards, milestones, encounters, and resource consequences rather than deduplicating only the top-level request.
- [ ] **C07.08.02** Enforce SQLite uniqueness or equivalent transactional constraints for each effective effect identity, ensuring concurrent evaluation requests cannot apply the same causal reward or progress contribution more than once.
- [ ] **C07.08.03** Persist committed effect outcomes for retry lookup, returning their established identities after lost responses instead of creating replacements whose different IDs conceal semantically duplicated credits, encounters, or rewards.
- [ ] **C07.08.04** Specify revised-source semantics so deliberate corrections supersede prior effective effects under policy, distinguishing valid reevaluation from repeated delivery of an already applied unchanged causal source revision.
- [ ] **C07.08.05** Handle partially processed dependent effects through atomic boundaries or recoverable persisted work, preserving which effects committed and which remain pending rather than replaying every effect unconditionally after restart.
- [ ] **C07.08.06** Test repeated requests, concurrent tabs, duplicate messages, and response loss against credit, reward, milestone, and encounter tables, requiring one effective effect per applicable stable causal identity.
- [ ] **C07.08.07** Restart during mixed-effect processing and recover pending work, reconciling outcomes with the effective ledger without duplicate grants, missing encounters, or automatic completion of eligible but uncommitted hike days.
- [ ] **C07.08.08** Review effect keys, constraints, correction replacement, and failure evidence; accept only when all enabled semantic effects deduplicate even though transport requests and messages may legitimately occur more than once.

### Control C07 09

**Original requirement C07.09:** Define partial chapter progress and carryover explicitly. Surplus credits remain available under policy but cannot auto-complete the active day, future days, or mandatory decisions; each completed day requires its own explicit completion transaction. Show incomplete requirements without adding physical assignments or pressuring the user to extend a workout.

- [ ] **C07.09.01** Define partial chapter progress and surplus carryover with policy units, eligible sources, thresholds, allocation order, residual precision, and conditions for retaining or withdrawing credit after source corrections.
- [ ] **C07.09.02** Persist partial eligibility separately from completed-day records and committed successor references, preventing accumulated credit from serving as implicit permission to close the active stage or skip completion decisions.
- [ ] **C07.09.03** Retain surplus sufficient for several stages without generating completed future days, requiring each day's own explicit eligible completion transaction and preserved mandatory decision or permitted deferral status.
- [ ] **C07.09.04** Show credited, remaining, and unresolved fictional requirements with source explanations, keeping physical assignments unchanged and avoiding wording that pressures users to extend a workout to satisfy virtual progress gaps.
- [ ] **C07.09.05** Specify carryover consumption upon explicit completion and subsequent day preparation, ensuring reused credits retain attributable source lineage without counting the same actual workout twice in physical totals or conversion effects.
- [ ] **C07.09.06** Test partial, exact-threshold, and multi-stage-surplus inputs, requiring expected earned eligibility and residual credit while committed pointer and future-day completion records remain unchanged before explicit completion requests.
- [ ] **C07.09.07** Apply corrections and repeated completion retries with carryover, verifying conserved effective credit, deduplicated day effects, and visible incomplete requirements without bypassing pending mandatory interactions or completing successors automatically.
- [ ] **C07.09.08** Review carryover ledger, requirement displays, and surplus scenarios; accept only when every completed day has its own explicit transaction and additional credit never adds unapproved physical workload.

### Control C07 10

**Original requirement C07.10:** Support authored preparation/recovery contributions to designated chapters and story elements. These contributions carry their own categories and evidence, and never increment actual walking distance or physical ascent.

- [ ] **C07.10.01** Define authored preparation and recovery contribution rules with eligible categories, assignment revisions, designated chapters or story elements, completion evidence, and policy identities separate from walking measurement conversion rules.
- [ ] **C07.10.02** Validate task completion against its accepted category-specific rule, retaining evidence and completion date without creating physical duration, distance, incline, or ascent merely because a recovery or planning checkbox is accepted.
- [ ] **C07.10.03** Map contributions only to explicitly designated narrative outcomes, preventing generic nonwalking completion from qualifying every chapter or silently rewriting physical assignments to match fictional terrain, fatigue, or resource depletion.
- [ ] **C07.10.04** Persist contribution credits with task and policy references, explaining their virtual significance while preserving independent actual-activity totals and the difference between eligibility and committed explicit hike-day completion.
- [ ] **C07.10.05** Provide partial, rejected, unavailable, and superseded evidence statuses, keeping continued participation usable without inventing task completion or requiring additional exertion to replace incomplete preparation or accepted recovery work.
- [ ] **C07.10.06** Test recovery, knowledge, planning, and equipment tasks against independently expected chapter contributions, including unsupported categories and missing evidence that must leave corresponding eligibility unmet without physical-quantity fabrication.
- [ ] **C07.10.07** Correct or delete task evidence and verify recalculated contributions, retained historical annotations, and unchanged actual walking totals, committed successor, and established branches unless an explicit authorized operation separately changes them.
- [ ] **C07.10.08** Review authored mappings, evidence records, explanations, and reconciliation results; accept only when each nonwalking contribution is attributable and no supported preparation or recovery pathway invents physical distance or ascent.

### Control C07 11

**Original requirement C07.11:** Handle stage boundaries, termini, direction changes, and optional routes consistently. Preserve excess credit and pending decisions without automatically completing hike days. On launch the resolver resumes the active unfinished day; otherwise it derives the next leg from committed completion history and retrieves/generates its versioned persisted dossier without awarding progress.

- [ ] **C07.11.01** Define boundary resolution for stage starts and ends, route termini, reverse direction, optional branches, and return points using pinned route and itinerary identities rather than mutable display labels.
- [ ] **C07.11.02** Preserve excess credit and pending decision context at boundaries, retaining partial eligibility separately from completed-day history so a chainage crossing cannot automatically close any hike day or its successors.
- [ ] **C07.11.03** Specify terminal behavior with explicit completion and visible route-finished state, rejecting successor allocation beyond the supported route while preserving remaining credit and actual records under the documented completion policy.
- [ ] **C07.11.04** Resolve launches by first loading an unfinished active day; otherwise select exactly the committed next leg and its pinned persisted dossier without awarding new progress during retrieval or generation.
- [ ] **C07.11.05** Validate optional-route and direction-change decisions against permitted itinerary transitions, recording accepted choice and relevant policy before successor selection instead of silently choosing a branch based on remaining earned credit.
- [ ] **C07.11.06** Test exact stage boundaries, terminal surplus, optional junctions, reverse progression, and missing decisions against independent expected positions, retained carryover, and unchanged committed pointer before explicit day completion.
- [ ] **C07.11.07** Interrupt dossier retrieval or generation after a successor is committed, requiring recoverable manifest status and the same leg on relaunch without duplicate completion, lost pending decisions, or random itinerary substitution.
- [ ] **C07.11.08** Review boundary contracts, resolver evidence, and terminal scenarios; accept only when passive launch resumes or prepares the committed leg and credit overflow never automatically completes stages or chooses unresolved routes.

### Control C07 12

**Original requirement C07.12:** Specify correction/deletion behavior before launch. Recalculate effective credits and earned within-stage/carryover values, annotate affected historical completion evidence, and preserve prior outcomes for configured retention. Corrections cannot implicitly advance the committed next-leg pointer, complete another day, or silently rewrite established branches.

- [ ] **C07.12.01** Publish correction and deletion rules before participation, defining credit replacement, earned-position recalculation, carryover changes, completed-day annotations, retained prior outcomes, and limitations of historical branch revision under configured retention.
- [ ] **C07.12.02** Reference corrected effective source revisions and retained minimal provenance in recalculated credits, distinguishing superseded values from current contributions without rewriting source physical measurements through campaign correction processing.
- [ ] **C07.12.03** Recalculate earned within-stage and residual values under the applicable policy, marking affected calculations pending until accepted while keeping committed day and successor records independent from arithmetic changes alone.
- [ ] **C07.12.04** Annotate completed-day evidence affected by removed or reduced sources, explaining the changed support without silently deleting established completion events, substituting branches, or converting excess revised credit into newly completed days.
- [ ] **C07.12.05** Require explicit reviewed operations for any permitted historical outcome change, preserving prior explanations under retention and rejecting correction paths that attempt implicit CompleteDay or direct committed-pointer updates.
- [ ] **C07.12.06** Test increased, reduced, deleted, and reclassified sources across unfinished and completed days, comparing credit, carryover, annotations, and retained provenance with independently expected correction outcomes and unchanged completion authority.
- [ ] **C07.12.07** Interrupt correction propagation and replay after restart, requiring durable invalidation and deduplicated replacement without duplicate grants, lost retained history, stale results presented as current, or new automatic successor advancement.
- [ ] **C07.12.08** Review published policy, correction explanations, and reconciliation evidence; accept only when source changes remain intelligible and cannot implicitly complete another day, advance committed next-leg state, or silently rewrite established branches.

### Control C07 13

**Original requirement C07.13:** Version policy and itinerary changes. Specify prospective application versus deliberate historical migration, preview effects on credits and route-identity equivalences, and preserve explanatory prior versions. Migration must not convert revised credit into a newly completed day or advance the committed next-leg pointer without explicit `CompleteDay`.

- [ ] **C07.13.01** Version progression policies and itinerary releases with stable identities, effective dates, compatibility rules, and migration metadata, retaining prior definitions needed to explain historical credits and established campaign route positions.
- [ ] **C07.13.02** Distinguish prospective adoption from historical migration, requiring deliberate selection and review of affected source credits, stage identities, branches, residuals, and committed completion annotations before any recalculation becomes effective.
- [ ] **C07.13.03** Provide a migration preview comparing old and proposed earned quantities, chainage, carryover, route-identity equivalences, unresolved decisions, and retained completion history without applying provisional results to authoritative campaign state.
- [ ] **C07.13.04** Validate mappings for removed stages, split segments, changed directions, and unsupported routes, requiring explicit conflict resolution rather than guessing equivalences or creating completed substitute days from adjusted credit totals.
- [ ] **C07.13.05** Preserve source revisions, prior policy explanations, and migration decisions under retention, recording actor, accepted mapping, resulting versions, and unchanged committed-pointer authority as a reviewable causal history.
- [ ] **C07.13.06** Test prospective changes and accepted historical migrations against independent expected ledgers, including surplus revised credit that must remain earned eligibility without completing a new day or bypassing mandatory decisions.
- [ ] **C07.13.07** Interrupt migration staging and commit, then restart and retry with mutation identity, requiring atomic accepted versions or recoverable pending state without mixed policies, duplicated credit, or silent successor changes.
- [ ] **C07.13.08** Review previews, mapping evidence, prior definitions, and recovery results; accept only when migration is attributable and revised credit cannot advance committed next-leg state without a separate explicit eligible CompleteDay transaction.

### Control C07 14

**Original requirement C07.14:** Implement explicit `CompleteDay` as the sole service-owned operation advancing the committed next-leg pointer. In one SQLite transaction validate day ID, expected revision, accepted completion evidence, resolved or rule-permitted explicitly deferred mandatory decisions, and idempotency key; commit the completion record, causal effects, active-day closure, and successor. Dossier generation uses recoverable staging/manifest status outside that transaction; file availability never proves completion.

- [ ] **C07.14.01** Define CompleteDay requests with stable day identity, expected revision, idempotency key, accepted evidence references, and decision status, documenting it as the sole operation authorized to advance committed successor state.
- [ ] **C07.14.02** Validate the active day, policy eligibility, effective evidence revisions, and mandatory decisions or explicitly rule-permitted deferrals inside the service before completion effects can commit to the repository database.
- [ ] **C07.14.03** Commit completion record, causal effects, active-day closure, and next-leg reference together in one SQLite transaction, rolling back all components when validation, revision comparison, or persistence fails before commitment.
- [ ] **C07.14.04** Enforce unique completion and effect identities, returning the established committed result on identical retries while rejecting stale or changed payloads rather than performing additional closure or successor advancement for the same day.
- [ ] **C07.14.05** Keep dossier generation outside the completion transaction using recoverable staging and manifest status, retaining the committed successor when files fail and preventing file presence or publication from proving day completion.
- [ ] **C07.14.06** Test eligible completion, missing evidence, unresolved decisions, permitted deferral, stale revisions, and duplicate keys, requiring exactly the expected atomic outcome and no pointer change for rejected requests.
- [ ] **C07.14.07** Terminate before and after commit and interrupt successor generation, requiring restart to resume the unfinished day or prepare exactly the committed next leg with deduplicated effects and recoverable dossier availability.
- [ ] **C07.14.08** Review transaction ownership, validation, effect constraints, and recovery evidence; accept only when every successor change resolves to an eligible explicit completion and artifacts cannot independently authorize campaign advancement.

### Control C07 15

**Original requirement C07.15:** Serialize local campaign mutations through SQLite transaction boundaries and compare expected revisions. Detect incompatible decisions from stale browser tabs and return current state for explicit reconciliation. After service restart recover committed state and retry pending effects; require no cloud synchronization or account system.

- [ ] **C07.15.01** Serialize campaign writes through SQLite transaction boundaries with expected revisions, covering credits, decisions, resources, active-day relationships, corrections, migrations, and explicit completion under documented local concurrency rules.
- [ ] **C07.15.02** Reject incompatible stale-tab decisions with current committed state and conflict details, preserving the accepted branch and providing an explicit reload/reconcile path rather than automatic last-writer replacement of campaign history.
- [ ] **C07.15.03** Permit only documented safe independent merges, retaining causal identities and revision references so concurrent eligible additions cannot duplicate source effects or hide incompatible campaign choices that require user reconciliation.
- [ ] **C07.15.04** Return committed mutation outcome and revision after persistence, distinguishing saved state from provisional browser drafts, conflicts, and pending effects without requiring cloud synchronization or an external user account.
- [ ] **C07.15.05** Persist recoverable pending effect work in SQLite and resume it after restart, deduplicating causal outcomes while retaining active-day identity, established branches, earned values, and committed completion history.
- [ ] **C07.15.06** Test simultaneous credits, competing branches, correction-versus-completion, and duplicate requests, comparing accepted states with independently specified serialization outcomes and requiring atomic rejection of incompatible or stale requests.
- [ ] **C07.15.07** Terminate around writes and downstream evaluation, then reconcile browser drafts with recovered revisions, preserving accepted mutations and exposing conflicts without silent branch changes or additional committed next-leg advancement.
- [ ] **C07.15.08** Review concurrency contracts, transaction traces, recovery records, and conflict usability; accept only when all authoritative local mutations remain serialized, attributable, and recoverable without mandatory remote identity or synchronization.

### Control C07 16

**Original requirement C07.16:** Provide an inspectable explanation for each advancement: source activity/task, effective revision, policy, conversion, stage effects, and corrections. On every aggregate view, distinguish fictional route accomplishment from actual training quantities.

- [ ] **C07.16.01** Provide an inspectable advancement record identifying source workout or task, effective revision, policy version, eligible evidence, canonical conversion, stage allocation, carryover, and related correction or migration history.
- [ ] **C07.16.02** Expose actual input and fictional output side by side with distinct units and definitions, preventing campaign chainage, scaled distance, or chapter completion from appearing as additional measured walking quantities.
- [ ] **C07.16.03** Show excluded, partial, superseded, and deleted-source contributions with permitted minimal provenance, explaining why eligibility or earned totals changed without requiring retained sensitive workout detail beyond privacy and retention policy.
- [ ] **C07.16.04** Distinguish earned eligibility from explicitly committed hike-day completion and successor state, naming unresolved requirements or permitted deferrals so apparent progress cannot imply an automatically completed stage or bypassed decision.
- [ ] **C07.16.05** Provide navigation from aggregate campaign figures to their constituent effective ledger entries and formulas, retaining input filters and pinned versions needed to reproduce the presented total or stage effect.
- [ ] **C07.16.06** Test explanations for distance, scaled, recovery, preparation, surplus, correction, and migration cases, comparing displayed causal chains with independent ledger calculations and actual physical totals for each supported mode.
- [ ] **C07.16.07** Review stale or pending evaluation displays, requiring clear outdated-state labels and preserved last-known explanations rather than presenting provisional browser values or incomplete recalculations as current authoritative progress.
- [ ] **C07.16.08** Accept only when reviewers can reconstruct every advancement from source evidence and versioned rules, and all aggregate views consistently distinguish fictional accomplishment from actual activity and explicit committed chronology.

### Control C07 17

**Original requirement C07.17:** Protect actual-workout detail in campaign views, generated dossiers, and exported milestones. Store minimum necessary provenance after deletion and apply local filesystem/runtime access rules; sharing/export is optional and never introduces a mandatory account or remote dependency.

- [ ] **C07.17.01** Inventory actual-workout detail exposed in campaign screens, dossier snapshots, milestone exports, and journals, documenting the minimum fields each enabled destination requires and identifying optional sensitive content that should remain excluded.
- [ ] **C07.17.02** Use source identities and permitted minimal provenance where full quantities or notes are unnecessary, maintaining credit explainability without automatically copying private measurements, biometrics, or reflections into broadly visible fictional summaries.
- [ ] **C07.17.03** Apply local filesystem, profile, runtime, and origin access rules to campaign records and generated artifacts, documenting repository visibility assumptions and avoiding mandatory cloud accounts or remote sharing dependencies for ordinary participation.
- [ ] **C07.17.04** Provide deliberate sharing/export scope for milestone identity, period, fictional achievements, and optional physical detail, preventing a campaign-summary selection from implicitly authorizing inclusion of personal workout notes or measurement history.
- [ ] **C07.17.05** Propagate approved source deletion or retention reduction to managed campaign references and generated artifacts, preserving coherent minimal lineage without regenerating removed sensitive details from historical snapshots or browser caches.
- [ ] **C07.17.06** Test milestone export, local dossier rendering, and deletion with sensitive source notes, verifying only selected fields appear and campaign credits remain explainable using policy-permitted reduced provenance after removal.
- [ ] **C07.17.07** Review external-connectivity-disabled operation and rejected untrusted origins, confirming supported local progression remains available while unauthorized access cannot mutate campaign state or expose unintended workout detail through API responses.
- [ ] **C07.17.08** Retain access, export, and deletion evidence; accept only when campaign views minimize physical detail, optional sharing is deliberate, and documented local privacy boundaries match the enabled deployment and retention policy.

### Control C07 18

**Original requirement C07.18:** Verify replay, rounding, threshold equality, scaled modes, partial/recovery chapters, and final-route completion against expected states. Include surplus credit sufficient for several stages: earned carryover may accrue, but no future day or mandatory decision completes and the committed next-leg pointer stays fixed until its explicit `CompleteDay` transaction.

- [ ] **C07.18.01** Construct independent progression fixtures for replay, rounding, threshold equality, scaled conversion, partial chapters, recovery contributions, final-route outcomes, and surplus sufficient to qualify several future stages under each enabled policy.
- [ ] **C07.18.02** Calculate expected canonical credits, residual fractions, earned positions, and completion eligibility independently, recording input revisions, policy versions, initial states, and permitted decision requirements before executing rule evaluations or comparing implementation output.
- [ ] **C07.18.03** Replay fixtures in repeated and reordered delivery, requiring identical effective results under stable ordering and deduplication rules without dependence on current server time, browser timer state, or incidental request arrival sequence.
- [ ] **C07.18.04** Test exact thresholds and fractional short sessions, verifying combined-equivalent credit within tolerance and no rounding-based fabrication or loss of earned quantities at stage boundaries, carryover allocation, or terminal progression scenarios.
- [ ] **C07.18.05** Exercise accepted preparation and recovery chapters with missing, partial, and complete evidence, requiring intended virtual contributions and unchanged actual walking distance, movement time, and physical ascent for nonwalking task participation.
- [ ] **C07.18.06** Apply multi-stage surplus before completion, verifying no future day, mandatory choice, or committed successor changes until its own explicit eligible CompleteDay request commits for the active itinerary day under test.
- [ ] **C07.18.07** Complete eligible days individually and test final-route behavior, requiring conserved residual credit, one effective completion per day, preserved unresolved choices, and no unsupported successor beyond the itinerary's accepted terminal state.
- [ ] **C07.18.08** Retain fixtures, expected ledgers, replay results, and repaired discrepancies; accept only when all enabled modes reconcile and passive credit accumulation cannot auto-complete stages or advance committed next-leg state.

### Control C07 19

**Original requirement C07.19:** Inject duplicate/out-of-order requests, process termination before/after completion commit, lost responses, stale-tab branches, source deletions, dossier-generation interruption, and migrations. Relaunch and verify unfinished-day resume or exactly the committed next leg; demonstrate deduplicated effects without claiming universal exactly-once transport.

- [ ] **C07.19.01** Define injections for duplicate and out-of-order requests, completion termination, response loss, stale branches, source deletion, dossier interruption, and migration with expected committed and recoverable outcomes at each transaction boundary.
- [ ] **C07.19.02** Submit duplicate credits and effects in varied order, checking stable causal identities, retained source revisions, and one effective reward, milestone, encounter, and eligible progress contribution per accepted causal event.
- [ ] **C07.19.03** Terminate before and after CompleteDay commit and lose its response, requiring atomic closure/effects/successor or an unchanged unfinished day, with retries returning the established result rather than additional advancement.
- [ ] **C07.19.04** Exercise competing stale-tab branches and source deletion during pending evaluation, preserving accepted choices and explicit conflicts while recalculating effective credit without silently rewriting history or completing another day.
- [ ] **C07.19.05** Interrupt successor dossier staging and publication, requiring manifest-aware recovery of the committed leg without treating missing files as lost completion or regenerated artifacts as evidence of new campaign advancement.
- [ ] **C07.19.06** Inject prospective and historical migration failures, requiring accepted version consistency, recoverable staging, retained mapping decisions, and no automatic pointer change caused by newly recalculated surplus or shifted route identities.
- [ ] **C07.19.07** Relaunch through CMD and PowerShell after every case, reconciling unfinished-day resume or exactly the committed next leg with actual records, credits, decisions, resources, manifests, and completion history.
- [ ] **C07.19.08** Retain failure traces and reconciliation evidence; accept only when semantic effects deduplicate across retries and restarts without claiming transport requests themselves have universal exactly-once delivery or execution guarantees.

### Control C07 20

**Original requirement C07.20:** Review progress explanations and two-calendar behavior with users and training reviewers. Release only when credits reconcile, corrections are intelligible, browser timers are never treated as movement proof, no game consequence alters physical targets, and launch/credit/correction/migration paths cannot advance the committed pointer without explicit `CompleteDay`.

- [ ] **C07.20.01** Review actual-versus-fictional progress explanations with representative users, checking comprehension of source activity, conversion, chapter eligibility, carryover, explicit day completion, and the independent committed next-leg reference for supported modes.
- [ ] **C07.20.02** Review two-calendar timelines with training reviewers, including partial sessions, recovery contributions, absence, several real dates per day, and launcher events that must create no exercise or virtual completion.
- [ ] **C07.20.03** Reconcile credits, earned position, residuals, and completion evidence against effective source revisions and independently calculated ledgers, resolving unexplained differences before accepting dashboard or dossier summaries as current authoritative campaign progress.
- [ ] **C07.20.04** Evaluate correction and deletion explanations with users, ensuring changed evidence and preserved historical annotations are intelligible without implying recalculated eligibility silently changes established branches or completes additional itinerary days.
- [ ] **C07.20.05** Audit timer and source pathways so browser elapsed time never independently proves movement, and nonwalking participation cannot inflate actual physical distance, moving duration, achieved incline, or ascent in campaign views.
- [ ] **C07.20.06** Run story, resource, and encounter setbacks against accepted plans, requiring unchanged physical targets, optional prompts, and continued participation without compensatory exercise or hidden treadmill control capabilities in the companion.
- [ ] **C07.20.07** Inspect every launch, credit, correction, migration, and generation path for committed-pointer writes, requiring rejection or absent authority unless an explicit eligible CompleteDay transaction is the documented causal operation.
- [ ] **C07.20.08** Accept release only after reviewed explanations, calendar evidence, reconciled ledgers, source-boundary checks, and pointer ownership establish clear progression meaning and prevent implicit completion or narrative-driven physical training changes.

## C08 Branching decision engine

**Accountable owner:** Game Systems Lead. **Reviewing roles:** Narrative Editor, Training Content Reviewer, Accessibility Lead, Application Security Reviewer, and QA Lead.

**Interfaces:** Reads authoritative local SQLite campaign/day records, the persisted dossier snapshot, C09 encounter reservation, C10 resource balances, C12 story state, and approved educational content through the loopback service. Writes committed decisions, effects, follow-up reservations, and C13 references in SQLite. Has no authority to modify prescribed workouts or command exercise equipment.

**Required evidence:** Published schemas and SQLite constraints; rule-language specification; day/event state diagrams; versioned dossier manifest; deterministic fixtures; choice-to-test traceability; transaction/restart logs; accessibility assessment; training-isolation results; correction procedure.

**Exit criterion:** Every published event validates and has reviewed explanation coverage. SQLite commits replay consistently and survive retry/restart without duplication; unfinished days resume without advancing position. Browser cache cannot assert completion, and no event can mutate real training or equipment state through an unauthorized path.

### Control C08 01

**Original requirement C08.01:** Publish and version the `EventDefinition` schema, including stable event ID, content revision, permitted campaign versions, prerequisites, choices, effect references, explanation, expiration, follow-up references, asset dependencies, and accessibility text. Reject missing references and unknown mandatory fields during content ingestion.

- [ ] **C08.01.01** Define required event identity fields, revision format, campaign compatibility range, expiry semantics, and accessibility descriptions in a machine-readable schema with explicit field cardinalities.
- [ ] **C08.01.02** Register prerequisite, choice, effect, successor, explanation, and asset references by stable identifier; resolve every mandatory reference against the selected content manifest.
- [ ] **C08.01.03** Reject unknown required fields, duplicate event identifiers, unsupported revisions, empty choice sets, and unresolved dependencies before any event becomes publishable.
- [ ] **C08.01.04** Validate content revisions without changing published records; require a new revision when choice wording, effects, explanations, eligibility, or expiration meaning changes.
- [ ] **C08.01.05** Specify whether expiration uses fictional itinerary position, scenario time, or explicit campaign transition; exclude browser time and launcher invocation count as implicit authorities.
- [ ] **C08.01.06** Exercise valid minimal and complete events through ingestion, publication, offering, and recovery; assert the loaded revision matches the dossier manifest exactly.
- [ ] **C08.01.07** Exercise malformed metadata, incompatible campaigns, missing assets, cyclic successors, and unknown mandatory fields; retain structured rejection paths and prevent partial library installation.
- [ ] **C08.01.08** Archive schema versions, ingestion reports, dependency-resolution results, reviewer decisions, and representative event fixtures; accept only releases with zero unresolved mandatory references.

### Control C08 02

**Original requirement C08.02:** Publish typed `Condition`, `Choice`, `Effect`, and `Outcome` schemas. Define operands, operators, target namespaces, units, null/comparison semantics, ordering, and immediate/deferred effects. For mandatory decisions, record source hike day, gate scope, carryover identity, deliberate-deferral acknowledgment, and the exact completion requirement affected.

- [ ] **C08.02.01** Enumerate condition operands and comparison operators with operand types, allowed namespaces, units, null behavior, and explicit coercion prohibitions for every supported expression.
- [ ] **C08.02.02** Define choice identity, availability, selection cardinality, explanatory text, optionality, and effect ordering; require stable choices independent of display order or translated wording.
- [ ] **C08.02.03** Specify immediate and deferred effects with typed targets, signed quantities, execution triggers, prerequisite dependencies, and a stable causal relationship to their originating choice.
- [ ] **C08.02.04** Model outcomes separately from selected choices, including deterministic conclusions, persisted random results, visible explanations, and terminal versus continuing story status.
- [ ] **C08.02.05** Represent mandatory gates with source day, gate scope, carryover identity, deferral acknowledgment, and precise completion predicate; prohibit destination-day completion through carryover resolution.
- [ ] **C08.02.06** Test null operands, incompatible units, unordered choices, equal comparisons, and mixed immediate/deferred effects against an independently reviewed expected-evaluation table.
- [ ] **C08.02.07** Reject unknown operators, training targets, ambiguous completion requirements, duplicate choice IDs, and carryovers without originating gates; expose actionable authoring errors before publication.
- [ ] **C08.02.08** Retain schema specimens and gate-lifecycle traces showing offer, acknowledgment, carryover, resolution, and explicit day completion; require every gate transition to resolve its source identity.

### Control C08 03

**Original requirement C08.03:** Define the SQLite-backed `DecisionRecord` contract with campaign ID, hike-day ID, dossier generation ID/hash, event revision, selected choice, input-state revision, operation ID, evaluated conditions, resolved random outcomes, effect transaction IDs, committed-state revision, and explanation revision. Enforce foreign keys and uniqueness for durable cross-record identity.

- [ ] **C08.03.01** Define DecisionRecord columns and constraints for campaign, day, dossier generation/hash, event revision, choice, input revision, operation identity, explanation revision, and commit revision.
- [ ] **C08.03.02** Normalize evaluated conditions, persisted random outcomes, and applied effect references into linked records; preserve operand snapshots needed to explain and replay the committed evaluation.
- [ ] **C08.03.03** Enforce foreign keys to immutable dossier snapshots, offered event revisions, valid choices, and effect transactions; prohibit references belonging to another campaign or hike day.
- [ ] **C08.03.04** Apply uniqueness to consequential event-instance resolution and originating operation identity; document which reopened educational attempts may create distinct nonconsequential records.
- [ ] **C08.03.05** Write receipt, decision, condition evidence, draw references, and resulting revision atomically; return the stored committed result when acknowledgment is lost and submission retries.
- [ ] **C08.03.06** Submit a valid decision, restart the service, and retrieve its full causal chain; compare every identity and effective revision against the original receipt.
- [ ] **C08.03.07** Attempt orphaned dossiers, mismatched hashes, cross-campaign choices, duplicate operation identities, and nonexistent effects; assert rejection leaves no partial decision evidence.
- [ ] **C08.03.08** Produce schema inspection, foreign-key verification, duplicate-resolution results, and a reconstructed decision example; require complete causal linkage for every accepted test decision.

### Control C08 04

**Original requirement C08.04:** Specify deterministic evaluation: identical input snapshots, rule revisions, choices, and random draws produce identical results. Document rounding, tie-breaking, time inputs, locale independence, and serialization used for replay comparison.

- [ ] **C08.04.01** Document canonical input serialization, field ordering, numeric representation, null encoding, Unicode handling, and rule revision identity used to compare decision evaluations.
- [ ] **C08.04.02** Specify rounding precision, rounding mode, comparison tolerance where permitted, and tie-breaking order; forbid implicit locale formatting from influencing numerical or identifier comparisons.
- [ ] **C08.04.03** Declare authoritative scenario time inputs and their timezone semantics; persist their values rather than reading wall-clock time during replay or retry.
- [ ] **C08.04.04** Separate pure evaluation from database mutation, narration, and asset rendering; evaluation receives only the approved snapshot, choice, rule version, and persisted draws.
- [ ] **C08.04.05** Compute a canonical outcome fingerprint covering conditions, typed effects, successor reservations, and explanation references; exclude cosmetic timestamps and unordered diagnostic metadata.
- [ ] **C08.04.06** Replay identical fixtures across supported locales, timezone settings, process restarts, and field-order permutations; require identical canonical outcomes and effect ordering.
- [ ] **C08.04.07** Vary exactly one rule revision, input value, choice, or draw in adversarial fixtures; identify intentional differences and detect accidental dependence on unrecorded inputs.
- [ ] **C08.04.08** Retain reproducibility inputs, independent expected outputs, fingerprints, runtime versions, and comparison reports; accept deterministic evaluation only when all equivalent fixtures match exactly.

### Control C08 05

**Original requirement C08.05:** Pin generator identity and algorithm revision; persist seed or draw identifiers and resolved outcomes. A refresh, retry, reopened choice, or application restart must not obtain another random result for an already reserved decision.

- [ ] **C08.05.01** Register random generator name, algorithm revision, seed encoding, stream namespace, draw ordinal, and supported compatibility policy for each decision-randomness mechanism.
- [ ] **C08.05.02** Reserve draw identifiers against campaign, event instance, and choice-resolution identity before revealing outcomes; persist the seed or resolved result with its causal reservation.
- [ ] **C08.05.03** Specify whether canceled or deferred decisions retain reserved draws; exclude reroll through reopened UI, content rerendering, altered browser cache, or repeated launch.
- [ ] **C08.05.04** Return previously stored outcomes for retried operations; prevent changes in current generator defaults from reevaluating an established reservation under another algorithm.
- [ ] **C08.05.05** Handle unsupported historical algorithms through stored resolved outcomes or an explicit reviewed migration; never silently replace an outcome because regeneration is convenient.
- [ ] **C08.05.06** Repeat refresh, back navigation, choice reopening, service restart, and launcher invocation against a fixed reservation; assert the draw identity and result remain unchanged.
- [ ] **C08.05.07** Race two submissions and interrupt immediately before and after draw reservation commit; require one recoverable draw sequence without disclosure of an uncommitted replacement.
- [ ] **C08.05.08** Archive generator test vectors, reservation traces, historical-algorithm recovery evidence, and retry results; require zero additional draws for an already resolved decision instance.

### Control C08 06

**Original requirement C08.06:** Define a restricted rule language with an allow-listed target registry. Reject arbitrary executable scripts, network requests, filesystem access, dynamic evaluation, and references to equipment-control or real-workout mutation interfaces.

- [ ] **C08.06.01** Specify the rule grammar as typed declarative expressions with bounded nesting, operand limits, allowed operators, and an explicit prohibition on embedded executable code.
- [ ] **C08.06.02** Maintain an allow-listed effect target registry containing virtual resource, story, learning, and reservation operations; assign each target its permitted types and authorization checks.
- [ ] **C08.06.03** Remove network, filesystem, equipment-control, real-workout, arbitrary reflection, and dynamic-evaluation capabilities from the evaluator environment and its dependency injection boundary.
- [ ] **C08.06.04** Validate imported expressions into a typed intermediate representation before publication; require unknown targets, functions, fields, and operators to fail closed with source locations.
- [ ] **C08.06.05** Bound evaluation steps, recursion, collection sizes, and effect count; return a recoverable rejected-event state when a rule exceeds documented execution limits.
- [ ] **C08.06.06** Exercise each allowed rule operation against a seeded campaign and confirm only its permitted virtual records change through validated domain services.
- [ ] **C08.06.07** Submit script fragments, network URLs, path traversal, dynamic function names, training mutations, and deeply nested expressions; assert rejection without external side effects.
- [ ] **C08.06.08** Retain grammar, registry ownership, parser diagnostics, capability-isolation tests, and execution-limit results; accept no published rule that resolves an unregistered target.

### Control C08 07

**Original requirement C08.07:** Validate prerequisites on the local server when an event is offered and again when a choice is committed. Define an explicit stale-choice result when another tab, accepted correction, or intervening server transaction invalidates eligibility.

- [ ] **C08.07.01** Identify eligibility inputs including route position, campaign revision, character facts, resource state, event history, expiry, and source-day gates; persist the offer-time snapshot.
- [ ] **C08.07.02** Evaluate prerequisites on the server before offering choices; return a distinct unavailable reason rather than relying on browser-hidden buttons as authorization.
- [ ] **C08.07.03** Reevaluate eligibility inside the committing transaction using current authoritative state and submitted expected revisions; prevent offer-time approval from bypassing current constraints.
- [ ] **C08.07.04** Define stale-choice responses containing accepted current revision, invalidated prerequisite identifiers, and an accessible refresh or reoffer action without applying consequential effects.
- [ ] **C08.07.05** Preserve the selected-but-uncommitted choice when eligibility changes for review, while marking it uncommitted; require renewed deliberate selection where the available choices changed.
- [ ] **C08.07.06** Offer an eligible event, change an unrelated field, and submit according to the documented revision policy; verify explicitly permitted submissions retain correct eligibility.
- [ ] **C08.07.07** Invalidate eligibility through another tab, workout correction, character transition, expiration, and balance change; assert each stale submission leaves decision and resources unchanged.
- [ ] **C08.07.08** Archive eligibility snapshots, offer/commit traces, stale-response examples, and concurrency fixtures; require all committed choices to satisfy server prerequisites at their commit revision.

### Control C08 08

**Original requirement C08.08:** Commit the decision, resource effects, story transitions, follow-up reservation records, and journal references within one SQLite transaction. Atomicity covers database state only: dossier/media/export files use the staged publication/reconciliation protocol in C18.13, with any follow-up jobs recorded durably. Verify rollback, database-busy handling, and termination without partial mandatory effects.

- [ ] **C08.08.01** Enumerate the transaction's decision, ledger effects, character transitions, follow-up reservations, journal references, receipt, and resulting campaign revision before implementing the commit boundary.
- [ ] **C08.08.02** Acquire the required SQLite write ownership, reread authoritative inputs, validate expected revisions, and apply every mandatory effect before committing the accepted decision.
- [ ] **C08.08.03** Record follow-up rendering jobs durably inside the transaction; perform dossier, media, and export writes afterward through staged checksum publication and marker reconciliation.
- [ ] **C08.08.04** Define bounded contention retries and a distinguishable pending or rejected result; prohibit browser success, reward revelation, or partial effect visibility before durable commit.
- [ ] **C08.08.05** Rollback the entire effect set when any resource bound, foreign key, story prerequisite, or mandatory reservation fails during decision processing.
- [ ] **C08.08.06** Complete a decision containing cost, reward, character change, follow-up, and journal reference; verify all records share one cause and committed revision.
- [ ] **C08.08.07** Inject database busy, constraint failure, process termination, and publication failure around each boundary; require all database effects or none with recoverable publication work.
- [ ] **C08.08.08** Retain fault-injection traces, ledger reconciliation, orphan-reference checks, and publication recovery reports; require no partial mandatory database effects in any interruption fixture.

### Control C08 09

**Original requirement C08.09:** Require persistent idempotency keys for submissions and retain their outcomes in SQLite across launcher runs. Repeated clicks, HTTP retries, and recovery replay must return the existing result without applying costs, rewards, or transitions twice.

- [ ] **C08.09.01** Define client operation identity generation, payload versioning, campaign scope, retention, and request fingerprint rules; preserve the identity across retries of one deliberate submission.
- [ ] **C08.09.02** Store accepted and rejected consequential outcomes in SQLite receipts with request fingerprint, decision reference, effective revision, and response information needed for recovery.
- [ ] **C08.09.03** Enforce unique operation identity before applying effects; distinguish a same-key identical retry from a same-key different payload requiring an explicit conflict response.
- [ ] **C08.09.04** Retain idempotency records across service shutdown, launcher invocations, browser-cache clearing, content updates, and supported database restoration; exclude ephemeral UI flags as authority.
- [ ] **C08.09.05** Expose operation-status lookup for uncertain acknowledgments; instruct the client to resolve the existing identity before generating a new consequential submission.
- [ ] **C08.09.06** Retry an accepted choice through double-click, HTTP retransmission, page refresh, and restarted service; assert one decision and one set of costs, rewards, and transitions.
- [ ] **C08.09.07** Reuse an operation identity with another choice, campaign, or altered expected revision; assert the documented conflict response without replacing the original receipt.
- [ ] **C08.09.08** Archive request/receipt pairs and counts before and after recovery; require stable outcomes and exactly one consequential effect set for every successful operation identity.

### Control C08 10

**Original requirement C08.10:** Use server-validated campaign/day revisions and SQLite transaction concurrency controls. Resolve simultaneous submissions from browser tabs through an explicit accepted/rejected outcome; never let browser cache or last-write-wins handling replace a consequential decision.

- [ ] **C08.10.01** Define expected campaign, day, event-instance, and consequential-record revisions on submission; identify which conflicts require refusal versus safe independent acceptance.
- [ ] **C08.10.02** Use server-side SQLite concurrency control to compare revisions and reserve consequential event resolution within the committing transaction; prohibit last-write-wins replacement of accepted choices.
- [ ] **C08.10.03** Return an accepted receipt to the winner and an explicit already-resolved or stale-state result to competing tabs with the authoritative selected choice.
- [ ] **C08.10.04** Refresh tab projections from committed revisions after conflict; preserve uncommitted selections for explanation without presenting them as accepted historical choices.
- [ ] **C08.10.05** Handle database contention separately from semantic conflicts; provide bounded retry or operation lookup without generating another decision identity or changing branch consequences.
- [ ] **C08.10.06** Race identical submissions with shared and distinct operation keys; verify documented deduplication and a single resolution with consistent receipts for both tabs.
- [ ] **C08.10.07** Race mutually exclusive choices while one tab uses stale cache after restart; require one accepted branch and no merged costs, overwritten choice, or contradictory story facts.
- [ ] **C08.10.08** Retain concurrency timelines, revision comparisons, conflict responses, and state reconciliation; require every competing submission to have an explicit attributable accepted or rejected disposition.

### Control C08 11

**Original requirement C08.11:** Distinguish offered, deferred, selected-but-uncommitted, committed, revealed, expired, and canceled states. On service restart, resume the persisted active unfinished hike day and its original dossier snapshot. A new launch/run record, page load, or dossier display must not mark the day complete or advance `nextleg`.

- [ ] **C08.11.01** Publish the event state machine with permitted transitions among offered, deferred, selected-uncommitted, committed, revealed, expired, and canceled; identify terminal states and transition authority.
- [ ] **C08.11.02** Persist consequential states and defer acknowledgments in SQLite; distinguish ephemeral selection drafts from decisions that have a durable committed receipt.
- [ ] **C08.11.03** Bind restored event state to the active unfinished hike day and its original dossier generation; reject attempts to attach it to a newly inferred calendar day.
- [ ] **C08.11.04** Define expiration and cancellation effects explicitly, including whether mandatory gates remain pending or require a reviewed waiver; prohibit silent gate satisfaction through lifecycle changes.
- [ ] **C08.11.05** On startup, rehydrate event and day records before rendering; logging the launch or displaying the dossier must leave completion and next-leg fields untouched.
- [ ] **C08.11.06** Traverse valid lifecycle transitions including deliberate deferral, later resolution, reveal, and cancellation; verify consistent accessible statuses and original source-day linkage.
- [ ] **C08.11.07** Attempt illegal transitions, reveal before commit, restart after draft selection, and repeated launches across midnight; assert no fabricated decision or day advancement.
- [ ] **C08.11.08** Retain transition tables, restart snapshots, invalid-transition results, and position comparisons; require unfinished-day identity, dossier hash, and next-leg state to remain stable.

### Control C08 12

**Original requirement C08.12:** Provide authored explanations of tradeoffs and committed effects. Mark delayed consequences without fabricating immediate feedback, and provide a causal reference when their eventual effects are revealed.

- [ ] **C08.12.01** Author explanations for each choice's known tradeoffs, relevant assumptions, committed immediate effects, and uncertainty; connect text revisions to the corresponding rule and outcome identities.
- [ ] **C08.12.02** Specify which deferred consequences may be disclosed initially and which remain hidden until their reveal trigger; record disclosure policy without claiming effects already occurred.
- [ ] **C08.12.03** Create causal references linking eventual ledger or story changes to the originating decision, source day, event revision, and delayed-effect reservation.
- [ ] **C08.12.04** Render explanations from committed typed effect records and approved prose; prevent stale browser predictions or generated passages from substituting uncommitted consequences.
- [ ] **C08.12.05** Provide missing-explanation fallback showing verified effect facts and an editorial issue identifier; preserve access to the decision history when explanatory assets fail.
- [ ] **C08.12.06** Select every published choice and compare immediate feedback with its committed ledger and transition records; confirm magnitudes, direction, timing, and labels match exactly.
- [ ] **C08.12.07** Reveal delayed effects after restart, itinerary relocation, and original-event retirement; verify source decision remains identifiable and no duplicate effect is disclosed as new.
- [ ] **C08.12.08** Archive explanation coverage, causal-link resolution, user comprehension findings, and corrected wording; accept no choice with unexplained consequential effects or falsely immediate feedback.

### Control C08 13

**Original requirement C08.13:** Classify each event as fictional narrative, hypothetical planning exercise, sourced educational material, or a combination with clearly separated passages. Retain evidence references for factual explanations and scenario assumptions for hypothetical outcomes.

- [ ] **C08.13.01** Assign passage-level classification for fictional narrative, hypothetical exercise, sourced educational explanation, and mixed content; retain distinct identifiers when one event combines categories.
- [ ] **C08.13.02** Attach factual claims to approved source records with retrieval date, applicability, reviewer, and correction status; identify scenario assumptions separately from source-supported facts.
- [ ] **C08.13.03** Define visible labels near consequential claims and choices, including fictional conditions and hypothetical availability; avoid relying solely on an introductory disclaimer elsewhere.
- [ ] **C08.13.04** Prevent event import and narration from upgrading fictional assumptions into route facts, current trail reports, physical observations, or real training instructions.
- [ ] **C08.13.05** Define handling for stale sources, missing evidence, and withdrawn explanations; retain approved educational fallback or block affected factual content without losing activity access.
- [ ] **C08.13.06** Inspect representative mixed events across dossier, choice explanation, journal, and export; verify classifications and source references survive all presentation contexts.
- [ ] **C08.13.07** Introduce unsupported claims, misclassified assumptions, broken evidence links, and source withdrawal; assert publication rejection or an explicitly labeled approved fallback.
- [ ] **C08.13.08** Retain claim inventories, source reviews, classification screenshots, and withdrawal results; require every factual explanation to resolve evidence and every hypothetical outcome to disclose assumptions.

### Control C08 14

**Original requirement C08.14:** Enforce the boundary between adventure state and training state. No decision, resource failure, generated passage, or follow-up event may silently increase real duration, distance, incline, load, or recovery requirements.

- [ ] **C08.14.01** Inventory all permitted decision effects and their service permissions; prove none can write TrainingPlan, Assignment, actual WorkoutSession quantities, or equipment-control commands.
- [ ] **C08.14.02** Define immutable assignment snapshots and authorized correction interfaces separately from narrative actions; require explicit user training edits to use their own audited workflow.
- [ ] **C08.14.03** Reject effect targets for real duration, distance, incline, load, recovery, or treadmill state at authoring ingestion and runtime dispatch boundaries.
- [ ] **C08.14.04** Review resource-exhaustion and follow-up rules for indirect coercion, including required compensatory exercise, forced skipped recovery, and additional activity needed solely to escape story failure.
- [ ] **C08.14.05** Constrain generated explanations to approved narrative facts; ensure free text cannot be interpreted as structured training commands or accepted actual workout observations.
- [ ] **C08.14.06** Run each allowed effect type and compare assignment hashes, actual-session quantities, and equipment-command logs before and after its execution; require unchanged training state.
- [ ] **C08.14.07** Attempt imported forbidden effects, resource-failure escalation, generated workout instructions, and malformed target aliases; verify explicit rejection with no unauthorized mutation.
- [ ] **C08.14.08** Archive permission matrices, boundary test results, assignment comparisons, and incentive review decisions; accept zero narrative-originated physical-training changes across the enabled effect registry.

### Control C08 15

**Original requirement C08.15:** Support keyboard operation, named options, visible focus, readable feedback, and untimed alternatives. Allow convenient interaction deferral without lost content or exertion punishment. A mandatory-choice deferral requires a deliberate persisted acknowledgment under C18.09; retain source-day/gate scope, and never let resolving carryover implicitly complete a later day.

- [ ] **C08.15.01** Specify accessible option names, group labeling, keyboard navigation, focus order, selected-state announcements, error messages, and postcommit feedback for every decision interaction pattern.
- [ ] **C08.15.02** Offer untimed decision access and a convenient defer action during walking mode; preserve content, reserved outcomes, and return position without awarding or deducting exertion credit.
- [ ] **C08.15.03** Implement mandatory deferral as deliberate persisted acknowledgment identifying source day, gate scope, carryover identity, and affected completion requirement before allowing eligible completion.
- [ ] **C08.15.04** Distinguish convenient optional postponement from mandatory gate acknowledgment; display outstanding carryovers and their origin without implying that later resolution completes another day.
- [ ] **C08.15.05** Preserve accessible feedback when service acknowledgment fails; indicate pending selection or acknowledgment and recover its operation status before asserting durable deferral.
- [ ] **C08.15.06** Complete choices and mandatory deferrals with keyboard and screen reader at enlarged text; verify readable feedback, retained focus, and no time-dependent content loss.
- [ ] **C08.15.07** Resolve carryover on a later day, interrupt acknowledgment, and defer repeatedly; assert one persisted acknowledgment, original draw, unchanged destination completion, and unchanged workout requirements.
- [ ] **C08.15.08** Retain accessibility task results, acknowledgment receipts, carryover traces, and training comparisons; require all options and deferrals to remain operable without timed or walking interaction.

### Control C08 16

**Original requirement C08.16:** Require editorial review for constructive outcomes, understandable uncertainty, respectful characterization, and geographically appropriate context. Define recoverable branches for poor decisions; exclude exercise punishment and coercive streak mechanics.

- [ ] **C08.16.01** Assign narrative and instructional reviewers to each event family; record geography, season, character constraints, uncertainty wording, respectful portrayal, and intended learning tradeoffs.
- [ ] **C08.16.02** Enumerate outcomes for every poor decision and identify an authored continuation, resource repair, alternate lesson, or deliberate deferral available within approved campaign rules.
- [ ] **C08.16.03** Review incentives for exercise punishment, coercive streak restoration, shame language, mandatory payment, and concealed optimal choices; document required revisions before publication.
- [ ] **C08.16.04** Compare scenario geography and character placement with pinned route context; distinguish fictional obstacles and destinations from verified real-world restrictions or facilities.
- [ ] **C08.16.05** Provide approved fallback text for retired or unavailable branches that retains constructive framing and does not rewrite the user's established choice.
- [ ] **C08.16.06** Playtest defensible and poor choices without designer hints; record misunderstanding of uncertainty, inability to recover, and pressure toward unplanned physical activity.
- [ ] **C08.16.07** Inject exhausted resources, skipped locations, unknown facts, and missed sessions into editorial walkthroughs; require a continuing path without additional prescribed exertion.
- [ ] **C08.16.08** Retain reviewer approval, branch recovery maps, playtest findings, and resolved defects; accept no supported outcome that strands participation or introduces exercise-based punishment.

### Control C08 17

**Original requirement C08.17:** Preserve committed outcomes under their original event and generated-dossier revisions. Persist corrected generations as new SQLite snapshot records with a supersession link; apply audited compensation or a documented migration instead of overwriting history or regenerating an active day's choices implicitly.

- [ ] **C08.17.01** Store committed event revision, dossier generation/hash, choice, resolved outcomes, and explanation revision as immutable historical references; separate current library defaults from past campaign records.
- [ ] **C08.17.02** Publish corrected generations as new snapshot records with explicit supersession links, corrected dependency manifests, publication state, and reason; retain the original snapshot for historical interpretation.
- [ ] **C08.17.03** Define compensation, annotation, and migration procedures for faulty consequences, including authority, affected campaigns, preview, expected revisions, and attributable user-visible change records.
- [ ] **C08.17.04** Prevent startup regeneration from replacing active-day choices, rerolling outcomes, or adopting newer event definitions solely because content files changed.
- [ ] **C08.17.05** Handle unavailable historical revisions through a rights-aware archival reference or approved replacement annotation; preserve the original choice identity and committed causal facts.
- [ ] **C08.17.06** Update an event during an unfinished and completed day; verify both retain original decision semantics and that new generations appear only through approved operations.
- [ ] **C08.17.07** Apply compensation and reject stale migration requests; assert append-only causal corrections, reconciled resource effects, unchanged prior decisions, and complete supersession ancestry.
- [ ] **C08.17.08** Retain before/after snapshots, migration approvals, compensation ledgers, and recovery traces; require every correction to explain its scope without silently rewriting established outcomes.

### Control C08 18

**Original requirement C08.18:** Provide an authoring validator that detects unreachable choices, contradictory prerequisites, missing successors, unresolvable mandatory branches, invalid effect targets, unbounded loops, and incomplete explanations before publication.

- [ ] **C08.18.01** Build prerequisite and successor graphs from the publishable manifest; identify strongly connected components, terminal outcomes, missing nodes, and branches lacking reachable completion or explicit deferral.
- [ ] **C08.18.02** Evaluate choice satisfiability against allowed typed state ranges and mutually exclusive facts; distinguish deliberately unavailable choices from contradictory prerequisites and accidental dead branches.
- [ ] **C08.18.03** Validate effect targets, resource bounds, deferred triggers, explanation coverage, and asset references; report source location and affected choices for every authoring defect.
- [ ] **C08.18.04** Require bounded loops through visit limits or monotonic progress conditions; reject cycles capable of issuing repeated rewards or indefinitely blocking mandatory gates.
- [ ] **C08.18.05** Simulate mandatory branches with exhausted resources, missing optional dependencies, skipped locations, and permitted corrections; require at least one approved continuation for each supported state.
- [ ] **C08.18.06** Run the validator against a clean fixture containing reachable alternatives, deliberate exclusions, and bounded cycles; compare findings with independently specified expected results.
- [ ] **C08.18.07** Seed unreachable choices, contradictory conditions, missing successors, invalid targets, infinite loops, and blank explanations; require each seeded defect to prevent publication.
- [ ] **C08.18.08** Archive graph reports, satisfiability fixtures, seeded-defect detection, exception approvals, and coverage; accept only manifests with zero unresolved blocking authoring findings.

### Control C08 19

**Original requirement C08.19:** Produce branch-coverage evidence for every published choice and terminal outcome, including boundary inputs, malformed rules, missing assets, impossible states, and content versions unavailable during recovery.

- [ ] **C08.19.01** Enumerate every event revision, choice, terminal outcome, deferred consequence, and mandatory carryover path in a traceable coverage matrix tied to the publication manifest.
- [ ] **C08.19.02** Construct deterministic initial-state fixtures for each branch with prerequisite facts, resource boundaries, day identity, dossier hash, pinned rules, and required random outcomes.
- [ ] **C08.19.03** Exercise minimum, maximum, null, equal-threshold, expired, and incompatible inputs; distinguish permitted unavailable choices from errors that should block event publication.
- [ ] **C08.19.04** Include malformed rule structures, invalid target namespaces, impossible story facts, missing assets, and unavailable historical content versions in negative integration fixtures.
- [ ] **C08.19.05** Verify recovery retains original choices and outcomes when presentation dependencies disappear; require honest fallback content or explicit pending status rather than fabricated branch completion.
- [ ] **C08.19.06** Inspect each terminal outcome's decision record, resource ledger, character facts, explanation, and next-leg state; reconcile them against independently expected causal records.
- [ ] **C08.19.07** Document uncovered or intentionally unreachable branches with owner, rationale, scope, and release disposition; prohibit aggregate coverage percentages from concealing a mandatory untested outcome.
- [ ] **C08.19.08** Archive execution evidence and branch-level results; require every published reachable choice and terminal outcome to pass, with all blocking defects resolved or explicitly withheld.

### Control C08 20

**Original requirement C08.20:** Verify deterministic replay, refresh resistance, duplicate submission, stale revision, multi-tab conflict, SQLite-busy/rollback behavior, forced service termination, launcher restart, unchanged unfinished-day position, deferred-event recovery, and training isolation. Record defects, exceptions, and release approval.

- [ ] **C08.20.01** Prepare a named integration matrix covering deterministic replay, reserved draws, duplicate keys, stale revisions, conflicting tabs, database contention, termination, and launcher continuation.
- [ ] **C08.20.02** Pin campaign fixtures, route/content/rule revisions, dossier hashes, expected ledger effects, character transitions, mandatory gates, and unchanged real assignment snapshots before execution.
- [ ] **C08.20.03** Execute repeated refresh, reopened selection, retried HTTP response, service restart, and launcher restart; compare draw identities, receipts, decision counts, and campaign positions.
- [ ] **C08.20.04** Race incompatible choices and apply intervening corrections; verify one accepted branch, explicit conflicts, valid prerequisites, and no last-write-wins replacement of established decisions.
- [ ] **C08.20.05** Force SQLite busy, rollback, and process termination before commit, after commit, and during publication; recover complete database effects and reconcile any staged artifacts.
- [ ] **C08.20.06** Defer mandatory content, resume the unfinished day, and resolve carryover later; require source-gate accuracy, no implicit destination completion, and no fabricated workout credit.
- [ ] **C08.20.07** Attempt training mutations through every enabled effect path and generated field; compare assignment and equipment state to the initial protected snapshots.
- [ ] **C08.20.08** Retain reproducible traces, reconciliation reports, defects, accepted exceptions, and attributable release approval; accept only when all critical integrity scenarios pass for the released versions.

## C09 Encounter scheduler

**Accountable owner:** Content Systems Lead. **Reviewing roles:** Game Systems Lead, Narrative Editor, Training Content Reviewer, Accessibility Lead, and QA Lead.

**Interfaces:** Reads persisted current position, active hike-day identity, dossier generation, C08 decisions, C10 resources, and C12 state from the local SQLite repository. Writes encounter reservations and delivery transitions through the loopback service. Supplies `nextleg` with committed encounter context; a browser route or launch/run count is never a position source.

**Required evidence:** Scheduling and `nextleg` specifications; SQLite reservation/day constraints; generated dossier snapshots and manifests; cooldown/budget tables; reproducible fixtures; distribution review; narrative-conflict results; internet-independent operation, restart, completion, and migration results; editorial previews.

**Exit criterion:** Selection and persisted dossier generations are reproducible; retries/restarts do not reroll, duplicate encounters, or skip an unfinished day. `nextleg` reads committed repository position, required threads resolve, and unavailable content does not prevent recording activity or leaving a session.

### Control C09 01

**Original requirement C09.01:** Version encounter metadata for stage, region, fictional season, campaign mode, resource conditions, character state, story prerequisites, exclusions, educational topic, narrative family, mandatory status, and permitted content releases.

- [ ] **C09.01.01** Define encounter metadata types and required identifiers for stage, region, fictional season, campaign mode, resource predicates, character facts, educational topic, and narrative family.
- [ ] **C09.01.02** Represent exclusions, mandatory status, prerequisites, compatible content releases, and optional presentation assets explicitly; prohibit display labels from acting as stable matching keys.
- [ ] **C09.01.03** Version classification changes that alter eligibility, mandatory gates, repetition behavior, or story continuity; retain previous metadata for already reserved encounter instances.
- [ ] **C09.01.04** Distinguish fictional season and scenario conditions from real calendar weather; declare how unknown region, season, or resource information affects eligibility.
- [ ] **C09.01.05** Validate route-stage references and compatible character/thread revisions against the selected manifest before admitting encounter definitions to the scheduler's candidate library.
- [ ] **C09.01.06** Load representative metadata across directions, regions, seasons, and modes; verify expected eligible families and accurately labeled hypothetical conditions in dossier output.
- [ ] **C09.01.07** Reject contradictory exclusions, unknown modes, invalid topic IDs, absent mandatory-status fields, and incompatible release ranges; assert no partially ingested candidate appears.
- [ ] **C09.01.08** Retain schema, compatibility tables, eligibility fixtures, and editorial approvals; require every released encounter to have complete metadata and resolvable mandatory dependencies.

### Control C09 02

**Original requirement C09.02:** Define SQLite `EncounterReservation` with reservation ID, campaign/hike-day IDs, input revisions, dossier generation ID/hash, candidate-set fingerprint, selected encounter revision, generator reference, trigger, priority, delivery window, and persisted state. Link it to the immutable dossier snapshot used for presentation.

- [ ] **C09.02.01** Define reservation columns for campaign/day, input revisions, dossier generation/hash, candidate fingerprint, selected encounter revision, generator, trigger, priority, window, and lifecycle state.
- [ ] **C09.02.02** Enforce foreign keys and ownership agreement among reservation, day, dossier, event revision, and campaign; prohibit a reservation from attaching to another campaign's snapshot.
- [ ] **C09.02.03** Store the canonical candidate-set fingerprint with eligibility input references; retain enough ordering and exclusion information to reproduce why selection occurred.
- [ ] **C09.02.04** Define reservation lifecycle transitions and delivery-window units; distinguish pending, delivered, deferred, resolved, expired, and canceled states from presentation cache flags.
- [ ] **C09.02.05** Link one reserved encounter to its immutable original dossier snapshot and carryover source; preserve this reference when later presentation occurs on another day.
- [ ] **C09.02.06** Reserve, present, defer, restart, and resolve an encounter; retrieve its complete inputs and compare the generation hash and event revision across transitions.
- [ ] **C09.02.07** Attempt orphaned dossiers, mismatched hashes, duplicate reservations, cross-day ownership errors, and invalid window boundaries; require constraint rejection without partial records.
- [ ] **C09.02.08** Archive schema inspection, ownership tests, reservation traces, and replay inputs; require every persisted reservation to resolve its selected content and original presentation snapshot.

### Control C09 03

**Original requirement C09.03:** Specify selection precedence for required story events, instructional content, optional encounters, and ambient material. Publish tie-breaking, incompatible-event resolution, and the circumstances permitting an editorial priority override.

- [ ] **C09.03.01** Publish a precedence table for required story, instructional, optional encounter, and ambient candidates; specify ordering before weights or random selection are applied.
- [ ] **C09.03.02** Define tie-breaking using stable identifiers and pinned priorities; document treatment of equal scores, mandatory collisions, and incompatible candidates within one dossier budget.
- [ ] **C09.03.03** Create an incompatibility registry for simultaneous appearances, exclusive consequences, duplicate instructional goals, and contradictory scenario assumptions; identify the authoritative conflict winner.
- [ ] **C09.03.04** Specify approved editorial override authority, permissible reasons, scope, expiration, and audit requirements; prevent unrecorded manual ordering from replacing reproducible scheduling policy.
- [ ] **C09.03.05** Determine fallback behavior when highest-priority content cannot be delivered; keep mandatory obligations visible rather than silently substituting a lower-priority optional encounter.
- [ ] **C09.03.06** Schedule fixtures containing each priority family, equal-priority ties, and approved overrides; compare selected order and suppression reasons with the published precedence table.
- [ ] **C09.03.07** Introduce mutually exclusive mandatory events and absent dependencies; require a diagnosed blocker or approved recovery with no contradictory paired encounters.
- [ ] **C09.03.08** Retain policy versions, override approvals, conflict matrices, and selection traces; require every selected or suppressed encounter to have an explainable precedence disposition.

### Control C09 04

**Original requirement C09.04:** Define encounter budgets by dossier and session: delivered choices, ambient moments, active threads, repeated topics, and interruption frequency. Separate reservations, presentations, deferrals, completions, and expirations in counting rules.

- [ ] **C09.04.01** Define per-dossier and per-session limits for delivered choices, ambient moments, active threads, repeated topics, and interruptions; specify units and counting reset boundaries.
- [ ] **C09.04.02** Separate reserved, presented, deferred, completed, expired, and canceled states in budget calculations; prohibit counting the same encounter repeatedly through refresh or redisplay.
- [ ] **C09.04.03** Identify mandatory-event budget exceptions and maximum backlog behavior; ensure ordinary workout logging and session termination remain available when interaction budgets are exhausted.
- [ ] **C09.04.04** Apply budgets server-side against durable reservation and presentation records; use presentation acknowledgments only where the declared counting policy requires actual delivery.
- [ ] **C09.04.05** Specify session splitting, pause, restart, and prolonged unfinished-day treatment; prohibit launch count from resetting repetition limits or consuming another encounter allowance.
- [ ] **C09.04.06** Exercise zero, exact-limit, and over-limit candidate sets across several sessions; assert measured presentations and interruptions obey each declared budget.
- [ ] **C09.04.07** Race presentation requests, repeatedly defer content, and restart the service at the limit; verify no double counts, unlimited redisplay loopholes, or blocked workout controls.
- [ ] **C09.04.08** Retain budget configuration, counted-state reconciliation, session traces, and overload usability results; require zero unexplained budget excesses in representative dossier and session fixtures.

### Control C09 05

**Original requirement C09.05:** Define cooldown keys and durations for encounter identity, narrative family, character, topic, and consequence type. State when a revised event remains equivalent to its earlier revision for repetition control.

- [ ] **C09.05.01** Define cooldown keys for exact encounter, narrative family, character, educational topic, and consequence type; state whether overlapping keys combine through maximum or another explicit rule.
- [ ] **C09.05.02** Specify cooldown durations in fictional stages, accepted sessions, presentations, or other declared units; distinguish real calendar time from scenario progression and launch events.
- [ ] **C09.05.03** Map revised encounters to equivalence identities when wording changes without changing repetition meaning; require editorial approval when a revision intentionally resets a cooldown.
- [ ] **C09.05.04** Persist qualifying cooldown anchors and their causal deliveries or resolutions in SQLite; never infer history solely from browser memory or missing content files.
- [ ] **C09.05.05** Define behavior for repeated stages, route reversal, skipped regions, retired events, and corrected presentation records; retain reproducible anchors under historical content revisions.
- [ ] **C09.05.06** Test just-before, exact-boundary, and just-after eligibility for every cooldown unit; compare encounter, family, character, topic, and consequence restrictions independently.
- [ ] **C09.05.07** Refresh, relaunch, change browser clock, and revise cosmetic dialogue during cooldown; assert neither bypass nor accidental extension of the declared restriction.
- [ ] **C09.05.08** Archive equivalence mappings, boundary calculations, and schedule traces; require selected encounters to satisfy all active cooldown keys or carry an approved recorded override.

### Control C09 06

**Original requirement C09.06:** Pin scheduling algorithm, content manifest, random generator, and relevant scenario inputs. Persist random draws or resolved selections so replay and inspection can reproduce the chosen encounter.

- [ ] **C09.06.01** Pin scheduling algorithm revision, content manifest, generator identity, draw sequence, scenario assumptions, and authoritative campaign input revisions for each generated candidate selection.
- [ ] **C09.06.02** Canonicalize candidate ordering and weight representation before sampling; specify tie-breaking, weight normalization, zero-weight behavior, and numeric precision to ensure reproducible selection.
- [ ] **C09.06.03** Persist resolved selections or draw references before publication; bind them to the day reservation so refresh and restart cannot choose a new encounter set.
- [ ] **C09.06.04** Record inputs excluded from randomness, including launcher count, browser clock, rendering duration, and asset arrival order; prevent these values from influencing candidate selection.
- [ ] **C09.06.05** Provide replay using historical algorithm support or persisted resolved selections when algorithms are retired; require an explicit reviewed migration for changed scheduling semantics.
- [ ] **C09.06.06** Run fixed-seed selections across supported locales, process restarts, and reordered content ingestion; require identical encounter identities, order, and selection fingerprints.
- [ ] **C09.06.07** Inject unavailable generators, missing manifests, changed weights, and modified candidate snapshots; block unfaithful regeneration or present approved historical selection recovery.
- [ ] **C09.06.08** Retain test vectors, pinned input manifests, draw records, and replay reports; require every delivered encounter selection to be reproducible from stored scheduling evidence.

### Control C09 07

**Original requirement C09.07:** Persist the generation identity, input/output manifest, resolved random outcomes, and encounter reservation records against the expected hike-day revision in SQLite. Assemble/render files outside short transactions and publish through C18.13 staged, checksummed reconciliation; mark the dossier ready only after verification. Recover the same generation after refresh/restart rather than rerolling; claim atomicity only for database writes.

- [ ] **C09.07.01** Reserve generation identity, expected day revision, input manifest, output references, random outcomes, and encounter reservations in SQLite before assembling presentation files.
- [ ] **C09.07.02** Define job states separating reservation, assembly, validation, staged publication, reconciliation, and ready delivery; assign retry ownership and recovery behavior at every boundary.
- [ ] **C09.07.03** Render outside short state-update transactions using pinned generation inputs; prevent ongoing image work from holding campaign locks or changing selection after reservation.
- [ ] **C09.07.04** Validate staged files and checksums before same-filesystem rename; create publication markers and update the database ready state only after artifact verification.
- [ ] **C09.07.05** On restart, reconcile markers, staged files, published directories, and job rows; reuse the existing generation and selections instead of allocating a new seed.
- [ ] **C09.07.06** Generate a complete dossier and inspect reservation, manifests, file hashes, marker, and ready record; confirm every presented encounter belongs to the reserved generation.
- [ ] **C09.07.07** Terminate after reservation, rendering, rename, marker creation, and database acknowledgment; require deterministic recovery without partial ready dossiers or duplicate encounter sets.
- [ ] **C09.07.08** Retain boundary traces, checksum reports, contention measurements, and recovery results; describe database atomicity accurately and require verified artifacts before any ready response.

### Control C09 08

**Original requirement C09.08:** Make trigger ingestion idempotent in SQLite. The same stage arrival, checkpoint crossing, accepted workout completion, or retried loopback request cannot create duplicate reservations, character appearances, or rewards; a launcher/startup event is not a stage-completion trigger.

- [ ] **C09.08.01** Define trigger identities for stage arrival, checkpoint crossing, accepted workout completion, and loopback retries; include source-record revision and trigger type in deduplication semantics.
- [ ] **C09.08.02** Persist accepted trigger receipts and produced reservation references in SQLite; require a unique trigger-operation key before issuing encounters, appearances, or rewards.
- [ ] **C09.08.03** Declare whether corrected or repeated source records produce reversals, new triggers, or no additional trigger; retain the original causal relationship for inspection.
- [ ] **C09.08.04** Exclude launcher startup, page display, browser refresh, and calendar midnight from stage-completion triggers; rely on committed DayCompletion and approved explicit transitions.
- [ ] **C09.08.05** Handle lost acknowledgments through trigger-status lookup or identical retry; prevent clients from generating a fresh trigger identity for the same accepted event.
- [ ] **C09.08.06** Deliver each supported trigger repeatedly before and after service restart; compare reservation, character appearance, reward, and receipt counts to the single-event expectation.
- [ ] **C09.08.07** Race duplicate triggers with distinct requests, submit stale source revisions, and fabricate launch-based completion; require explicit rejection or deduplication without new effects.
- [ ] **C09.08.08** Archive trigger contracts, causal receipts, count reconciliation, and restart evidence; require exactly the documented reservation set for each accepted qualifying source transition.

### Control C09 09

**Original requirement C09.09:** Separate eligibility calculation, reservation, presentation, and completion. A movement or workout trigger may reserve content, but presentation must honor walking mode, interaction preferences, and accessibility settings.

- [ ] **C09.09.01** Define separate eligibility, reservation, presentation, and completion records with authoritative transition owners; make reservation status insufficient evidence of interaction or resolved content.
- [ ] **C09.09.02** Specify movement and workout triggers that may reserve content while requiring walking-mode, interaction-preference, and accessibility checks before interruptive presentation.
- [ ] **C09.09.03** Persist queued content and return points independently of current browser view; support later camp presentation without changing original generation, source trigger, or random outcomes.
- [ ] **C09.09.04** Record presentation acknowledgment according to the budget policy; distinguish loading an asset from intentional viewing and viewing from submitting a consequential choice.
- [ ] **C09.09.05** Provide noninterruptive queue status and service-unavailable recovery; retain workout recording and stopping controls even when presentation or decision interfaces are deferred.
- [ ] **C09.09.06** Reserve encounters during walking mode, then present them at camp; verify original selection, accessible return point, and no premature decision or reward record.
- [ ] **C09.09.07** Toggle preferences, background the tab, restart the service, and retry presentation; assert no surprise interruption, duplicate delivery count, or automatic completion.
- [ ] **C09.09.08** Retain phase-transition traces, preference fixtures, queue usability results, and effect reconciliation; require all consequential completion effects to follow a distinct accepted completion operation.

### Control C09 10

**Original requirement C09.10:** Enforce C12 narrative prerequisites and mutual exclusions. Prevent conflicting encounters from establishing inconsistent whereabouts, promises, inventory, relationships, or completed story facts.

- [ ] **C09.10.01** Import character introductions, whereabouts, possessions, promises, relationship state, completed facts, and mutual exclusions from the authoritative C12 fact and thread contracts.
- [ ] **C09.10.02** Validate candidate prerequisites against current committed narrative facts; reject appearances requiring impossible travel, unintroduced relationships, unavailable possessions, or contradictory completed events.
- [ ] **C09.10.03** Model conflicts among candidates selected together, including dialogue claims that individually pass but contradict another reserved encounter in the same generation.
- [ ] **C09.10.04** Reserve compatible appearances with expected narrative revisions; revalidate consequential eligibility when encounters resolve after intervening character or campaign updates.
- [ ] **C09.10.05** Define a diagnosed pending or approved fallback state for invalidated appearances; preserve originating obligations and avoid improvising new facts to conceal conflicts.
- [ ] **C09.10.06** Schedule fixtures with valid introductions, compatible coappearances, and known promises; verify resulting dialogue and transitions remain consistent with the registry.
- [ ] **C09.10.07** Introduce mutually exclusive whereabouts, retired characters, broken promises, hidden facts, and concurrent transitions; require exclusion or explicit stale-resolution handling.
- [ ] **C09.10.08** Retain compatibility matrices, fact snapshots, exclusion reasons, and continuity walkthroughs; accept zero unreviewed contradictions in selected encounter sets and committed character consequences.

### Control C09 11

**Original requirement C09.11:** Prevent starvation of required/long-pending encounters through priority aging and approved fallback stages. Preserve originating day, requirement, and carryover identity when relocating an event. Retirement or waiver requires a recorded approved rule and deliberate acknowledgment where required; resolving carryover cannot automatically complete its destination day or create workout credit.

- [ ] **C09.11.01** Define priority-aging units, maximum mandatory waiting thresholds, approved fallback stages, and escalation owners for required or long-pending encounters across supported itineraries.
- [ ] **C09.11.02** Preserve source day, requirement identity, carryover identity, original event revision, and acknowledgment when moving pending content to another eligible presentation stage.
- [ ] **C09.11.03** Distinguish relocated presentation from requirement waiver, retirement, and resolution; require an approved rule and deliberate acknowledgment wherever the source gate demands it.
- [ ] **C09.11.04** Ensure relocated encounters cannot manufacture activity credit, complete their destination day, advance next-leg, or resolve unrelated mandatory requirements by association.
- [ ] **C09.11.05** Provide an actionable backlog view showing delay reason, next eligible presentation, and permitted resolution or deferral; maintain workout logging despite narrative backlog.
- [ ] **C09.11.06** Simulate repeated optional competition and skipped locations until aging applies; verify required content meets thresholds or triggers the documented fallback escalation.
- [ ] **C09.11.07** Retire a pending mandatory event, remove fallback assets, and resolve carryover on a later day; assert visible obligation handling and unchanged destination completion.
- [ ] **C09.11.08** Retain aging curves, relocation records, waiver approvals, and state comparisons; require every overdue mandatory encounter to have an attributable disposition and reachable continuation.

### Control C09 12

**Original requirement C09.12:** Derive `nextleg` from the transactionally persisted current position and completed-day state. Resume an active unfinished day before creating another leg; handle explicit itinerary edits, partial sessions, repeat/skip actions, and corrections through audited transitions, never launch-count or cached-position inference.

- [ ] **C09.12.01** Define next-leg selection from committed route position, latest DayCompletion, active unfinished day, route release, direction, and itinerary revision; prohibit cached position as authority.
- [ ] **C09.12.02** Prioritize resuming the unfinished day before reserving another generation; preserve its original dossier, seed, encounter queue, mandatory gates, and saved stage origin.
- [ ] **C09.12.03** Specify audited transitions for itinerary edits, partial sessions, repeated stages, skips, corrections, and route reversal, including expected revisions and position provenance.
- [ ] **C09.12.04** Advance the next-leg pointer only through explicit completion or approved position-changing operations; log launches separately without treating run counts as itinerary progress.
- [ ] **C09.12.05** Handle inconsistent saved pointers or unsupported route revisions through diagnosed recovery; avoid silently selecting a nearby stage or creating an empty replacement campaign.
- [ ] **C09.12.06** Launch an unfinished and a completed campaign repeatedly across calendar changes; verify zero movement for resume and one reserved next day from the committed endpoint.
- [ ] **C09.12.07** Submit stale position transitions, interrupted completion, client-selected legs, and corrected activities; require audited accepted changes or rejection with preserved authoritative position.
- [ ] **C09.12.08** Retain position derivation examples, resume traces, migration approvals, and route-continuity reports; require every scheduled leg to originate from an attributable committed position.

### Control C09 13

**Original requirement C09.13:** Enforce user deferral without rerolling or repetition. Preserve a clear queue and return point; prevent an accumulation of mandatory interactions from blocking workout logging or session termination.

- [ ] **C09.13.01** Define optional and mandatory deferral operations with queue identity, source encounter, original generation, return point, and persisted acknowledgment requirements for gated content.
- [ ] **C09.13.02** Retain reserved selections and draws through deferral; exclude reroll, duplicate encounter creation, or repetition-budget reset when users postpone or reopen queued content.
- [ ] **C09.13.03** Display queue order, unresolved requirements, deferral status, and accessible return controls; explain source-day carryovers without implying destination-day completion upon later resolution.
- [ ] **C09.13.04** Bound mandatory backlog presentation without blocking workout logging, session pause, stop, or export; provide approved source-gate handling when the queue cannot be presented.
- [ ] **C09.13.05** Recover deferred queues from SQLite after refresh, restart, and browser-cache clearing; reconcile cached drafts with authoritative reservation and acknowledgment revisions.
- [ ] **C09.13.06** Defer, revisit, and resolve several encounters in different permitted orders; verify original outcomes, stable queue identities, and correct budget accounting.
- [ ] **C09.13.07** Accumulate mandatory content, disconnect the service, and retry acknowledgments; require visible pending status and continued workout controls without lost or duplicate reservations.
- [ ] **C09.13.08** Retain queue traces, usability findings, acknowledgment receipts, and draw comparisons; require no content loss, reroll, exertion penalty, or logging blockage caused by deferral.

### Control C09 14

**Original requirement C09.14:** Provide approved behavior for empty candidate sets, broken dependencies, unavailable revisions, and missing media, retaining activity recording and a usable status view. Undeliverable mandatory encounters remain pending or explicitly deferred under C18.09; a missing asset or automatic fallback cannot silently waive a day gate or complete another day.

- [ ] **C09.14.01** Define separate failure classifications for empty eligible pools, invalid dependencies, unavailable pinned revisions, missing media, and corrupted dossier snapshots; map each to approved behavior.
- [ ] **C09.14.02** Provide locally available neutral status or authored ambient fallback for optional content gaps; label substitutions accurately and retain workout recording without fabricated encounter completion.
- [ ] **C09.14.03** Keep undeliverable mandatory encounters pending or deliberately deferred under source-day gate rules; prohibit missing assets from implicitly waiving obligations or completing another day.
- [ ] **C09.14.04** Record failed dependency identities, source manifest, reservation, retry state, and fallback revision; avoid replacing reserved random selections silently during repair.
- [ ] **C09.14.05** Specify when content repair may retry the same generation versus requiring an approved corrected snapshot; retain the original selection and supersession relationship.
- [ ] **C09.14.06** Exercise genuinely empty pools and each missing-dependency class; confirm usable dossier status, accessible explanations, and unchanged actual workout assignments and records.
- [ ] **C09.14.07** Remove mandatory media during a pending encounter, restart, and restore it; verify retained obligation, original reservation, and no unintended gate or position advancement.
- [ ] **C09.14.08** Retain failure fixtures, fallback reviews, reservation comparisons, and restored-delivery evidence; require accurate degradation and zero silent mandatory-waiver or day-completion effects.

### Control C09 15

**Original requirement C09.15:** Bound schedule evaluation by computational and latency budgets. Cache only version-addressed eligibility data, invalidate it when authoritative SQLite input changes, and reconcile cached views after server restart. Cached reservations or a client-selected leg cannot override repository state.

- [ ] **C09.15.01** Set scheduler limits for candidate count, rule-evaluation steps, dependency depth, cache size, and latency on named reference hardware; document measured budget rationale.
- [ ] **C09.15.02** Key eligibility caches by algorithm, manifest, relevant campaign revisions, route position, and scenario inputs; prohibit unversioned cached candidates from becoming authoritative reservations.
- [ ] **C09.15.03** Invalidate affected cache entries when resource, story, decision, itinerary, or corrected activity inputs change; identify dependencies needed for selective invalidation correctness.
- [ ] **C09.15.04** Rehydrate reservations from SQLite on restart and reconcile cached browser views; ignore client-selected legs and stale cached reservations that conflict with saved day state.
- [ ] **C09.15.05** Define evaluation cancellation, timeout, and fallback behavior; preserve workout endpoints and existing reservations without treating computation failure as completion or selection permission.
- [ ] **C09.15.06** Benchmark representative and worst-supported candidate libraries with concurrent workout requests; require scheduler and recording latency to meet separately declared budgets.
- [ ] **C09.15.07** Change every eligibility dependency, replay stale caches, and restart during computation; verify recomputation or safe reuse only when version-addressed inputs match exactly.
- [ ] **C09.15.08** Retain cache-key contracts, invalidation coverage, performance measurements, and timeout traces; accept no stale eligibility-driven reservation or budget violation without approved scope reduction.

### Control C09 16

**Original requirement C09.16:** Record a schedule audit containing selection reason, applied exclusions, priority changes, cooldown status, input revision, suppression reason, delivery state, and content revision. Exclude unnecessary biometric or personal reflection data.

- [ ] **C09.16.01** Define schedule audit fields for campaign/day, generation, input revision, selected encounter, selection reason, exclusions, priority changes, cooldown status, suppression, and delivery state.
- [ ] **C09.16.02** Record rule and content revisions plus candidate fingerprints sufficient to inspect scheduling; reference existing authoritative data instead of copying personal reflections or biometric details.
- [ ] **C09.16.03** Classify audit retention, access, export inclusion, and diagnostic redaction; document which minimal identifiers remain necessary to correlate selection and recovery failures.
- [ ] **C09.16.04** Persist attributable editorial overrides, aging adjustments, fallback selections, and mandatory relocation reasons; distinguish automated policy decisions from manual interventions.
- [ ] **C09.16.05** Handle audit-storage failure according to the declared integrity policy; prevent an apparently fully audited decision when required causal evidence could not be retained.
- [ ] **C09.16.06** Inspect successful, suppressed, deferred, and failed selections; reproduce their principal rationale from the audit without accessing private journal text.
- [ ] **C09.16.07** Seed sensitive reflection strings and optional biometric fields, then collect diagnostics and support exports; require absence of unnecessary private content in all audit outputs.
- [ ] **C09.16.08** Retain audit schemas, sample rationale reconstructions, redaction results, and retention tests; require complete mandatory scheduling evidence with zero prohibited personal-field leakage.

### Control C09 17

**Original requirement C09.17:** Provide editorial preview and scenario inspection tools showing eligible candidates, exclusions, selection weights, active threads, and likely blockers. Keep previews isolated from production campaign state.

- [ ] **C09.17.01** Provide preview inputs for campaign facts, route position, resources, fictional season, mode, content manifest, and scheduler revision without creating production campaign records.
- [ ] **C09.17.02** Display eligible candidates, excluded candidates with reasons, weights, precedence, cooldowns, active threads, mandatory obligations, and potential unresolved blockers for the selected snapshot.
- [ ] **C09.17.03** Show reproducible seeded simulations and explicitly labeled hypothetical outcomes; distinguish preview estimates from durable encounter reservations or real activity history.
- [ ] **C09.17.04** Run previews in isolated databases or read-only evaluation contexts; remove mutation APIs and production credentials from the authoring tool's execution environment.
- [ ] **C09.17.05** Define exportable preview reports containing input snapshot and manifest fingerprints; retain sufficient context for editorial reviewers to reproduce a proposed scheduling change.
- [ ] **C09.17.06** Preview representative region, mode, season, and story states; compare selections and exclusions with the production evaluator operating on equivalent cloned inputs.
- [ ] **C09.17.07** Attempt production IDs, mutation requests, malformed snapshots, and preview-derived completion submissions; require isolation and explicit rejection without campaign changes.
- [ ] **C09.17.08** Retain preview equivalence results, isolation tests, reviewer findings, and resolved blockers; require no production side effects and complete visibility of mandatory scheduling obstacles.

### Control C09 18

**Original requirement C09.18:** Test selection determinism, refresh recovery, duplicated triggers, cooldown boundaries, exhausted candidate pools, incompatible events, and required-event starvation using named fixtures.

- [ ] **C09.18.01** Create named fixtures for fixed-seed selection, refresh recovery, duplicate triggers, cooldown boundaries, exhausted pools, incompatibility, and required-event aging across published scheduler revisions.
- [ ] **C09.18.02** Record initial campaign facts, route positions, content manifests, random draws, budgets, expected selections, exclusions, queue states, and effects before executing each fixture.
- [ ] **C09.18.03** Verify deterministic fixtures across reordered ingestion, process restart, and equivalent browser requests; compare encounter identities, sequence, draw references, and fingerprints exactly.
- [ ] **C09.18.04** Exercise cooldown boundaries and duplicate triggers with concurrent requests; confirm budget counts and reservation uniqueness remain correct at edge conditions.
- [ ] **C09.18.05** Drive required events through competing optional content, skipped stages, and fallback locations; assert documented aging thresholds and preserved source-day gate identities.
- [ ] **C09.18.06** Remove all candidates and inject conflicting mandatory content; require approved fallback or explicit pending blockers while keeping activity recording available.
- [ ] **C09.18.07** Compare all observed ledger, character, completion, and next-leg changes with the independently authored expectations; reject hidden reward duplication or automatic position movement.
- [ ] **C09.18.08** Archive fixture versions, execution traces, assertions, and defects; require every named integrity fixture to pass against the published manifest and supported runtime combinations.

### Control C09 19

**Original requirement C09.19:** Run representative long-campaign selections to measure repeated topics, character overexposure, content gaps, mandatory-event delays, and branch availability. Define acceptable distributions and investigate anomalies rather than asserting randomness alone establishes quality.

- [ ] **C09.19.01** Define representative campaign lengths, directions, regions, progression modes, branch strategies, absence patterns, and seeded runs before measuring schedule distribution and continuity.
- [ ] **C09.19.02** Set acceptable repetition, character exposure, topic coverage, mandatory-delay, content-gap, and branch-availability thresholds with editorial justification rather than assuming randomness ensures quality.
- [ ] **C09.19.03** Collect encounter identity, family, character, topic, suppression, delay, carryover, and terminal-state metrics from durable reservations and transitions rather than displayed-page counts.
- [ ] **C09.19.04** Stratify results by region, direction, mode, and strategy; ensure averages do not conceal a stranded minority branch or unsupported content region.
- [ ] **C09.19.05** Inspect threshold anomalies against candidate scarcity, weights, cooldowns, exclusions, and aging policy; identify whether correction belongs to content coverage or scheduler logic.
- [ ] **C09.19.06** Run adversarial strategies involving repeated stages, maximum deferral, exhausted resources, and missed towns; require mandatory content and recovery to remain reachable.
- [ ] **C09.19.07** Repeat corrected simulations with the same seeds and publish comparison metrics; preserve historical release results instead of silently replacing unfavorable quality evidence.
- [ ] **C09.19.08** Archive simulation inputs, distributions, anomaly investigations, reviewer decisions, and coverage maps; require thresholds met or affected campaign scope explicitly withheld from release.

### Control C09 20

**Original requirement C09.20:** Verify internet-independent operation, missing assets, staged-publication failure, migration, itinerary changes, deferred/carryover recovery, multi-tab conflicts, restart, and accessible queue operation. Completion advances one leg once; unfinished-day resume advances none; resolving earlier mandatory content cannot auto-complete the current or future day.

- [ ] **C09.20.01** Prepare end-to-end fixtures for offline operation, missing assets, publication interruption, migrations, itinerary changes, carryovers, tab conflicts, restart, and accessible queue handling.
- [ ] **C09.20.02** Pin initial day identity, dossier hash, seed, pending reservations, source gates, actual activities, current position, and next-leg pointer before each journey.
- [ ] **C09.20.03** Complete and relaunch one eligible day; require exactly one completion and pointer advance, then repeated launches of the next unfinished day with zero additional movement.
- [ ] **C09.20.04** Resolve earlier mandatory carryover on the current or future day; verify only its source requirement changes and no destination-day completion or workout credit appears.
- [ ] **C09.20.05** Interrupt staged publication and service processing while internet is disconnected; reconcile markers, database receipts, and retained selections without changing the reserved generation.
- [ ] **C09.20.06** Change itinerary or content through approved operations and conflict across tabs; require explicit revision outcomes and preserved origins for relocated pending encounters.
- [ ] **C09.20.07** Operate queue discovery, deferral, return, resolution, and error recovery with keyboard and assistive technology; verify workout logging remains accessible during backlog.
- [ ] **C09.20.08** Retain journey traces, position comparisons, reconciliation reports, accessibility results, and release dispositions; require all critical continuation invariants to pass for supported configurations.

## C10 Virtual resource system

**Accountable owner:** Game Economy Lead. **Reviewing roles:** Game Systems Lead, Training Content Reviewer, Narrative Editor, Data Engineering Lead, and QA Lead.

**Interfaces:** Receives typed effects from C08 and approved completed-day transitions through the local service; stores its ledger and authoritative balances in SQLite; supplies C09/C12 state and C13 references. Startup/run logs and browser state cannot consume or replenish resources. Measured activity and physiology remain separate.

**Required evidence:** Resource/item schemas and SQLite constraints; metric/unit dictionary; ledger invariants; consumption/clock specifications; approved balance table; correction procedure; transaction/lock/restart reconciliation; recovery-path coverage; training-isolation and label/export review.

**Exit criterion:** SQLite transactions reconcile and remain atomic/idempotent across tab conflicts, failures, and launcher/service restarts. Reopening an unfinished day does not alter balances. Exhaustion is recoverable and fictional quantities remain distinguishable from actual measurements in every view/export.

### Control C10 01

**Original requirement C10.01:** Publish typed schemas for fictional food, water, budget, equipment condition, pack inventory, pack weight, daylight, and morale. Define valid units, ranges, precision, initialization, unknown states, and whether each value is a quantity, category, score, or estimate.

- [ ] **C10.01.01** Define resource schemas for fictional food, water, currency, equipment condition, inventory, pack weight, daylight, and morale with explicit quantity, category, score, or estimate semantics.
- [ ] **C10.01.02** Specify canonical units, minimum and maximum values, numerical precision, permitted categories, initialization rules, and whether missing data means unknown, unavailable, or inapplicable.
- [ ] **C10.01.03** Assign stable resource and item identifiers independent of translated names; version meaning changes that alter bounds, consumption, condition transitions, or derived quantities.
- [ ] **C10.01.04** Model unknown quantities explicitly rather than zero; prohibit arithmetic, affordability, or comparison rules from treating unknown balances as verified available resources.
- [ ] **C10.01.05** Validate initialization against campaign mode and pinned rules; reject inconsistent item ownership, capacity, daylight ranges, or condition categories before activating the campaign.
- [ ] **C10.01.06** Round-trip valid initialized resources through storage, API, interface, and export; verify preserved types, units, precision, labels, and unknown-state distinctions.
- [ ] **C10.01.07** Submit negative prohibited quantities, invalid categories, oversized values, ambiguous units, and absent initialization fields; require structured rejection without partial resource initialization.
- [ ] **C10.01.08** Retain schemas, resource dictionaries, boundary fixtures, and initialization reviews; require every enabled resource to have complete typed semantics and deterministic validation.

### Control C10 02

**Original requirement C10.02:** Use distinct namespaces and record types for virtual resources and real measurements. Require interface labels and export metadata that prevent fictional depletion, fatigue, or route travel from being mistaken for measured physiological state or physical activity.

- [ ] **C10.02.01** Define separate virtual-resource and actual-measurement namespaces, database tables, API fields, and export tags; prohibit a shared unlabeled fatigue, distance, water, or energy field.
- [ ] **C10.02.02** Specify visible labels for fictional balances and scenario estimates beside values, charts, alerts, journal summaries, and collection descriptions where misinterpretation could occur.
- [ ] **C10.02.03** Prevent virtual depletion and narrative fatigue from populating physiological measurements, accepted workout quantities, medical observations, or actual equipment-control interfaces.
- [ ] **C10.02.04** Define unit presentation for similarly named real and virtual quantities, including virtual trail distance versus treadmill distance and fictional daylight versus actual session duration.
- [ ] **C10.02.05** Preserve domain classifications through aggregation and export; require consumers to choose a domain explicitly rather than infer it from display names or numeric units.
- [ ] **C10.02.06** Complete a workout and resource-consuming decision, then inspect dashboard and journal; reconcile actual values separately and verify unmistakable virtual labels for the fictional effects.
- [ ] **C10.02.07** Attempt namespace aliases, mixed-domain chart series, imported virtual fatigue, and mislabeled exports; require rejection or corrected presentation before publication.
- [ ] **C10.02.08** Retain data mappings, interface inspections, export examples, and boundary tests; require zero virtual values represented as measured physical activity or physiological state.

### Control C10 03

**Original requirement C10.03:** Define an append-only SQLite `ResourceTransaction` ledger with transaction ID, campaign/hike-day IDs, dossier generation, input revisions, resource, amount or state transition, source event, rule revision, timestamp, causal decision, and explanation reference. Enforce unique originating-operation keys and referential integrity.

- [ ] **C10.03.01** Define append-only transaction columns for campaign/day, dossier generation, input revisions, resource, amount or transition, source event, rule, timestamp, causal decision, and explanation.
- [ ] **C10.03.02** Represent initialization, consumption, awards, purchases, corrections, and migrations as typed ledger entries; preserve signed quantity semantics and explicit before/after state where categorical.
- [ ] **C10.03.03** Enforce foreign keys to campaign, day, dossier, decisions, rules, and operation receipts; verify the referenced entities belong to the same authoritative causal context.
- [ ] **C10.03.04** Apply unique originating-operation constraints at the declared effect granularity; allow compound operations multiple distinct entries without permitting duplicate execution of the same effect.
- [ ] **C10.03.05** Prohibit direct updates or deletions of committed ledger entries through ordinary application APIs; use compensating records with reversal references for accepted corrections.
- [ ] **C10.03.06** Commit representative quantity and categorical transitions, restart, and reconstruct their histories; compare all causes and revision references with accepted operation receipts.
- [ ] **C10.03.07** Attempt orphaned causes, cross-campaign references, duplicate effect keys, overwritten transactions, and missing explanations; assert rejection without changing committed balances.
- [ ] **C10.03.08** Archive schema inspection, append-only checks, reconstruction reports, and referential-integrity results; require every resource change to resolve its immutable originating operation.

### Control C10 04

**Original requirement C10.04:** Publish balance and inventory invariants. The materialized resource state must reconcile to initialization plus committed transactions; quantities cannot violate approved bounds or contradict ownership, equipped-item, and item-condition rules.

- [ ] **C10.04.01** Publish balance equations covering initialization, committed deltas, compensation, migration, and categorical transitions; identify materialized-state tables as projections of the authoritative ledger.
- [ ] **C10.04.02** Specify lower and upper bounds, container capacity, stack limits, ownership uniqueness, equipped-item constraints, and valid condition transitions for each resource and item type.
- [ ] **C10.04.03** Reconcile materialized balances and inventory against ledger reconstruction at startup, after correction, and during integrity review; classify mismatches before accepting further consequential writes.
- [ ] **C10.04.04** Define treatment of reservations and pending purchases; exclude uncommitted effects from available balance and prevent double-spending through concurrent affordability checks.
- [ ] **C10.04.05** Provide audited projection rebuild or repair when derived state differs from valid history; prohibit editing ledger entries to make an unexplained current balance appear consistent.
- [ ] **C10.04.06** Run known initialization and transaction sequences covering purchase, consumption, equip, damage, repair, and compensation; verify every intermediate invariant independently.
- [ ] **C10.04.07** Inject negative balances, overcapacity containers, duplicate ownership, invalid equipped states, and corrupted projections; require rejection or diagnosed repair without hidden ledger changes.
- [ ] **C10.04.08** Retain reconciliation equations, expected fixtures, mismatch reports, and repair evidence; accept zero unexplained differences between committed ledger and materialized resource state.

### Control C10 05

**Original requirement C10.05:** Select fixed-point or decimal representation where appropriate, including virtual currency. Specify conversion and rounding rules; reject unit mismatches, invalid magnitudes, overflow, and ambiguous values.

- [ ] **C10.05.01** Select fixed-point integer or explicit decimal representations for currency and consumable quantities; document scale, maximum magnitude, sign rules, and storage/API encoding.
- [ ] **C10.05.02** Define conversions, rounding direction, precision retention, and residual handling for prices, partial consumables, pack weight, and resource modifiers; avoid implicit binary-float currency arithmetic.
- [ ] **C10.05.03** Require compatible canonical units before addition or comparison; preserve source units where relevant and reject ambiguous strings instead of guessing their meaning.
- [ ] **C10.05.04** Validate overflow before arithmetic, multiplication, accumulation, and serialization; prohibit wraparound, infinity, nonnumeric values, and values outside approved resource ranges.
- [ ] **C10.05.05** Specify conversion order for compound effects so equivalent operation sequences produce the same permitted rounding results; retain rule revisions explaining any intentional order dependence.
- [ ] **C10.05.06** Exercise fractional purchases, repeated small deltas, exact affordability, and conversion round trips; compare results with independently calculated fixed-point or decimal expectations.
- [ ] **C10.05.07** Submit mixed units, extreme magnitudes, malformed decimals, excess precision, and locale-specific separators; require clear rejection with no partial balance or inventory change.
- [ ] **C10.05.08** Archive representation decisions, arithmetic test vectors, overflow results, and precision reports; require exact agreement at the documented scale for every supported resource operation.

### Control C10 06

**Original requirement C10.06:** Version item definitions, container behavior, base mass, consumable units, condition states, repair rules, stack limits, and replacement identity. Preserve the definitions used by an existing campaign unless a controlled migration is applied.

- [ ] **C10.06.01** Define immutable item revisions containing base mass, quantity unit, container capacity, condition categories, repair rules, stack limits, consumable behavior, and replacement identity.
- [ ] **C10.06.02** Specify empty-container and partial-consumable mass calculations, damaged-item treatment, worn-versus-carried classification, and ownership rules for replacements or equivalent equipment variants.
- [ ] **C10.06.03** Pin each campaign's inventory entries to item revisions; prevent current catalog edits from silently changing historical pack weight, affordability, durability, or available repair choices.
- [ ] **C10.06.04** Validate condition graphs and repair transitions, including permissible inputs, costs, required items, and resulting identity; distinguish repair from replacement and discarded ownership.
- [ ] **C10.06.05** Provide approved migration previews showing changed mass, capacity, condition, and balance effects; retain original definitions and audited conversion records for affected campaigns.
- [ ] **C10.06.06** Create, consume, damage, repair, replace, and retire representative items; verify preserved revision references and correct quantity, identity, and mass at each step.
- [ ] **C10.06.07** Test unsupported condition transitions, overfilled containers, excess stacks, duplicate replacements, and retired historical definitions; require rejection or approved historical fallback.
- [ ] **C10.06.08** Retain item dictionaries, transition fixtures, migration comparisons, and catalog reviews; require every owned item to resolve the exact definition used for its committed effects.

### Control C10 07

**Original requirement C10.07:** Apply compound purchases, repairs, resupply, equipment swaps, and completed-day effects within one SQLite transaction. Costs, item quantities, condition transitions, derived weight, and causal references must all commit together or remain unapplied; document lock-contention and rollback behavior.

- [ ] **C10.07.01** List each compound operation's required cost entries, item changes, condition transitions, derived weight, causal links, and resulting revision before defining the transaction boundary.
- [ ] **C10.07.02** Revalidate prices, availability, ownership, capacity, expected revisions, and affordability inside the SQLite transaction using pinned item and rule definitions.
- [ ] **C10.07.03** Commit ledger entries, inventory projections, conditions, derived values, receipts, and linked decision effects together; return success only after durable database commit.
- [ ] **C10.07.04** Keep rendering, media copying, and export publication outside resource transactions; record any required follow-up jobs durably and reconcile their staged output separately.
- [ ] **C10.07.05** Define bounded busy retries and rollback results; preserve the original operation identity so an uncertain acknowledgment cannot issue another purchase or repair.
- [ ] **C10.07.06** Execute compound purchase, swap, repair, resupply, and completed-day consumption fixtures; reconcile all costs, quantities, conditions, and pack weight to expected records.
- [ ] **C10.07.07** Terminate or fail constraints after each constituent mutation; require either the full compound effect set or none, without lost items or charged-but-unreceived purchases.
- [ ] **C10.07.08** Retain transaction traces, fault-injection reports, lock-contention results, and ledger reconciliation; accept no partial compound resource outcome at any tested persistence boundary.

### Control C10 08

**Original requirement C10.08:** Persist idempotency through unique originating-decision/transition keys in SQLite. Client retry, server restart, launch repetition, or replay must not award, charge, consume, or repair resources twice; do not use ephemeral browser flags as proof that an effect ran.

- [ ] **C10.08.01** Define persistent originating keys for decision effects, explicit purchases, repairs, resupply, and completion transitions; distinguish effect identity from transient HTTP request identity.
- [ ] **C10.08.02** Enforce unique operation/effect keys in SQLite with request fingerprints and receipts; allow safe identical retries while rejecting reused keys with different consequential payloads.
- [ ] **C10.08.03** Recover existing results after server restart, launcher repetition, browser-cache clearing, and supported backup restoration; avoid relying on client flags or process memory.
- [ ] **C10.08.04** Specify completion-effect identity using committed DayCompletion rather than launch or page-view events; require repeated day display to leave every resource unchanged.
- [ ] **C10.08.05** Provide operation lookup for lost acknowledgments and preserve pending requests; prevent callers from treating a timeout as permission to generate another resource effect.
- [ ] **C10.08.06** Repeat each resource operation across double-clicks, HTTP retry, restart, and replay; verify exactly one award, charge, consumption, or repair and stable resulting balances.
- [ ] **C10.08.07** Race duplicate keys and conflicting payloads, then rehydrate from the database; require a single receipt or explicit payload conflict without duplicate inventory transitions.
- [ ] **C10.08.08** Retain before/after ledger counts, request fingerprints, restored receipts, and retry tests; require operation-level uniqueness for all enabled resource mutation families.

### Control C10 09

**Original requirement C10.09:** Derive pack weight from authoritative virtual inventory and item definitions. Specify treatment of worn items, containers, damaged equipment, partial consumables, cached supplies, and items left behind.

- [ ] **C10.09.01** Define pack-weight equations from authoritative item quantities and pinned mass definitions; specify canonical mass units, rounding, and distinction between carried and worn totals.
- [ ] **C10.09.02** Include container tare mass and remaining consumable mass; document treatment of partial quantities, damaged equipment, cached supplies, abandoned items, and replacement ownership.
- [ ] **C10.09.03** Classify item location and equipped status independently of ownership; require explicit transitions when supplies move from carried inventory to caches or are left behind.
- [ ] **C10.09.04** Recalculate weight within compound inventory commits or a transactionally consistent projection; prevent charts and choice explanations from reading mismatched inventory revisions.
- [ ] **C10.09.05** Handle unknown mass or quantity through explicit unknown totals or approved estimates; disclose incomplete weight rather than substituting zero for missing item data.
- [ ] **C10.09.06** Use independently calculated fixtures combining worn items, full and empty containers, fractional food, damage, caches, and abandonment; verify every subtotal and grand total.
- [ ] **C10.09.07** Attempt duplicate ownership, negative quantities, invalid location states, outdated item revisions, and concurrent swaps; assert consistent derived weight or diagnosed rejection.
- [ ] **C10.09.08** Retain calculation specifications, item-level reconciliation, uncertainty labels, and concurrency results; require displayed pack weight to match the same committed virtual inventory revision.

### Control C10 10

**Original requirement C10.10:** Publish fictional consumption rules with their inputs, assumptions, units, calculation interval, environmental modifiers, and intended educational interpretation. Do not imply that a game quantity determines real water, food, or medical needs.

- [ ] **C10.10.01** Publish fictional consumption formulas with input resource types, scenario distance or time, environmental modifiers, interval boundaries, units, rounding, and intended learning meaning.
- [ ] **C10.10.02** Identify supplied assumptions for pace, temperature, terrain, equipment, and availability; separate hypothetical scenario modifiers from measured activity and current trail information.
- [ ] **C10.10.03** Pin consumption rules to campaign and transaction revisions; record calculation inputs and causal stage or decision so deductions can be explained and replayed.
- [ ] **C10.10.04** Define zero-length, rest-day, partial-stage, skipped-stage, accelerated-mode, and unknown-input behavior; prohibit launcher time or refresh frequency from creating additional consumption intervals.
- [ ] **C10.10.05** Review explanations to avoid presenting game water, food, fatigue, or morale quantities as prescriptions for real physiological or medical needs.
- [ ] **C10.10.06** Evaluate deterministic scenario fixtures at modifier and interval boundaries; compare deductions, residuals, and resource bounds with independent expected calculations.
- [ ] **C10.10.07** Inject missing assumptions, unit mismatches, extreme modifiers, and repeated completion retries; require explicit failure or labeled fallback without duplicate consumption.
- [ ] **C10.10.08** Retain formulas, scenario assumptions, instructional review, calculation evidence, and labels; require reproducible fictional deductions with no direct real-needs instruction or actual-workout mutation.

### Control C10 11

**Original requirement C10.11:** Define fictional daylight and elapsed-travel rules separately from real session and launch/run time. Specify effects of pauses, partial workouts, accelerated progression, rest days, and chapter completion; reopening an active day does not advance the scenario clock or consume supplies merely because another launch was logged.

- [ ] **C10.11.01** Define fictional travel-clock records and daylight models independently from real session intervals, launcher timestamps, service uptime, and computer-clock observations.
- [ ] **C10.11.02** Specify scenario elapsed-time effects for pauses, partial workouts, accelerated progression, virtual rest days, chapter completion, and approved itinerary transitions in each enabled mode.
- [ ] **C10.11.03** Persist scenario-clock changes as causal resource transitions with original day and rule references; exclude browser rendering and launch/run records from consumption triggers.
- [ ] **C10.11.04** Pin active-day scenario time and remaining supplies across reopen, refresh, restart, date rollover, and computer-clock change unless an explicit approved transition occurs.
- [ ] **C10.11.05** Represent unknown daylight or travel assumptions clearly; prohibit inferred real sunlight availability or measured walking duration from fictional clock calculations.
- [ ] **C10.11.06** Compare several real sessions completing one virtual stage with an equivalent accepted stage sequence; require the documented scenario time and consumption totals.
- [ ] **C10.11.07** Relaunch across midnight, change timezone, pause overnight, and restart after a partial workout; verify no unapproved clock advance or resource deduction.
- [ ] **C10.11.08** Retain clock-mapping tables, transition records, real-versus-fictional comparisons, and retry traces; require every scenario-time change to resolve an authorized campaign operation.

### Control C10 12

**Original requirement C10.12:** Document insufficient-resource outcomes and affordability checks. Revalidate authoritative SQLite balances and expected revision inside the transaction, resolve concurrent-tab purchase conflicts explicitly, and reject database-busy failures without accidental debt or silent item loss.

- [ ] **C10.12.01** Define affordability using committed balances, pinned prices, required quantities, reservations, permitted bounds, and expected resource revisions; document insufficient-resource results before implementing purchase APIs.
- [ ] **C10.12.02** Recheck balance, item availability, ownership, capacity, and campaign revision inside the transaction; reject browser-calculated affordability as authority for consequential purchases.
- [ ] **C10.12.03** Specify simultaneous-purchase outcomes with one accepted receipt or explicitly permitted independent transactions; prohibit hidden debt, lost items, and last-write-wins inventory replacement.
- [ ] **C10.12.04** Distinguish semantic insufficient-funds errors from database-busy and uncertain-acknowledgment states; preserve operation identity and provide bounded retry or status lookup.
- [ ] **C10.12.05** Offer authored recovery or alternate affordable choices where supported; retain workout records and logging access regardless of virtual balance or pending purchase state.
- [ ] **C10.12.06** Purchase at exact affordability and immediately below and above required cost; verify approved outcomes, resource bounds, inventory receipt, and explanatory feedback.
- [ ] **C10.12.07** Race two individually affordable but jointly unaffordable purchases, hold a database lock, and lose acknowledgment; require explicit results and no accidental debt or duplication.
- [ ] **C10.12.08** Retain boundary fixtures, concurrency timelines, contention evidence, and balance reconciliation; accept only purchases that satisfy authoritative affordability at their committed revision.

### Control C10 13

**Original requirement C10.13:** Establish stage, camp, town, rest-day, route-change, and expedition-reset transitions. Define which resources persist, replenish, expire, deteriorate, or change meaning at each boundary.

- [ ] **C10.13.01** Publish a transition matrix for stage, camp, town, rest day, route change, and expedition reset covering persistence, replenishment, expiry, deterioration, and changed resource meanings.
- [ ] **C10.13.02** Identify each transition's causal operation and pinned rule revision; distinguish explicit completion effects from arrival presentation, launch logging, or browser navigation.
- [ ] **C10.13.03** Define treatment of cached supplies, borrowed equipment, deferred purchases, daylight reset, and outstanding resource obligations across route divergence and virtual recovery days.
- [ ] **C10.13.04** Require reset scope and confirmation semantics to identify affected campaign records while preserving actual workout history and attributable prior fictional ledger entries.
- [ ] **C10.13.05** Validate transitions against item capacity, ownership, bounds, and completion state; reject unsupported transitions rather than silently initializing convenient replacement balances.
- [ ] **C10.13.06** Traverse each supported boundary using known inventories and balances; compare every retained, replenished, expired, and deteriorated quantity with the transition matrix.
- [ ] **C10.13.07** Repeat, skip, reverse, interrupt, and retry boundaries; verify one authorized effect set and no automatic resource reset from reopening an unfinished day.
- [ ] **C10.13.08** Retain transition specifications, ledger traces, reset previews, and recovery results; require complete resource disposition and historical provenance for every supported campaign boundary.

### Control C10 14

**Original requirement C10.14:** Guarantee an authored recovery pathway for every supported exhausted-resource state. Recovery must not require extra actual exertion, unplanned training, mandatory payment, or loss of access to existing workout records.

- [ ] **C10.14.01** Enumerate supported exhaustion combinations for food, water, money, equipment condition, inventory, daylight, and morale; include compound states and pending mandatory decisions.
- [ ] **C10.14.02** Author at least one reachable recovery branch for each supported state using virtual assistance, planning, deferral, repair, or narrative transfer under approved rules.
- [ ] **C10.14.03** Validate recovery availability against exhausted balances and required items; prevent the recovery itself from depending on a resource already unavailable in that state.
- [ ] **C10.14.04** Prohibit extra actual exercise, skipped recovery assignments, mandatory payment, account creation, or loss of workout-record access as conditions for fictional continuation.
- [ ] **C10.14.05** Provide clear recovery explanations and accessible selection controls; retain original failures and their causes rather than erasing history when recovery changes resources.
- [ ] **C10.14.06** Execute every enumerated exhausted-state fixture through recovery and resumed participation; verify reachable outcome, valid balances, and preserved records without unplanned activity.
- [ ] **C10.14.07** Remove optional recovery assets, retire a related character, and interrupt recovery commits; require approved fallback or durable pending status without a stranded campaign.
- [ ] **C10.14.08** Retain exhaustion coverage maps, walkthroughs, ledger comparisons, and incentive review; require a verified continuation for every supported exhaustion state before release.

### Control C10 15

**Original requirement C10.15:** Explain resource changes through user-facing causal statements tied to decisions and rules. Disclose hidden effects when revealed and provide enough context to understand tradeoffs without exposing unnecessary implementation details.

- [ ] **C10.15.01** Define explanation records linking each visible resource change to originating decision, completion, correction, rule revision, and affected virtual quantity or categorical state.
- [ ] **C10.15.02** Render causal statements with before/after values, units, relevant assumptions, and delayed-versus-immediate timing; label resources as fictional where physiological confusion is possible.
- [ ] **C10.15.03** Record hidden-effect disclosure policies and reveal triggers; when revealed, identify the earlier cause without implying the deduction occurred at the disclosure moment.
- [ ] **C10.15.04** Generate explanations from committed transactions and approved templates; exclude optimistic browser predictions or unvalidated narration from authoritative balance descriptions.
- [ ] **C10.15.05** Provide concise fallback explanations for missing prose or retired content using verified ledger facts and historical source references; preserve access to resource history.
- [ ] **C10.15.06** Inspect purchase, repair, consumption, reward, compensation, and delayed-effect feedback; reconcile every statement with signed ledger quantities and condition transitions.
- [ ] **C10.15.07** Retry reveals, correct originating data, and restore historical campaigns; assert stable causes, accurate corrected labels, and no duplicated effects or misleading timing.
- [ ] **C10.15.08** Retain explanation coverage, user comprehension findings, causal-link tests, and ledger comparisons; accept no material resource change without understandable truthful causal feedback.

### Control C10 16

**Original requirement C10.16:** Correct errors through compensating entries and audited migrations. Identify dependent decisions, derived values, encounters, stories, and journal summaries; do not erase ledger history or silently rewrite prior balances.

- [ ] **C10.16.01** Define correction authorization, reason, affected operations, expected revisions, compensation identity, and migration approval; require immutable references to the erroneous original ledger entries.
- [ ] **C10.16.02** Calculate compensating quantity or categorical transitions without deleting original history; preserve original and corrected balances with a visible causal relationship.
- [ ] **C10.16.03** Enumerate dependent decisions, pack weight, encounters, story facts, and journal summaries before applying correction; classify recalculation, annotation, or historical preservation for each dependency.
- [ ] **C10.16.04** Preview cascading consequences and resource-bound conflicts; require approved handling when compensation would invalidate later affordability or established consequential choices.
- [ ] **C10.16.05** Apply compensation and required projection updates transactionally; publish corrected files separately with new manifests and supersession references rather than overwriting established snapshots.
- [ ] **C10.16.06** Correct known quantity, price, condition, and mass errors; verify reconciliation from original ledger plus compensation matches the approved final state.
- [ ] **C10.16.07** Retry compensation, submit stale revisions, and interrupt migration; assert single correction effects, preserved historical decisions, and recoverable dependent summary updates.
- [ ] **C10.16.08** Retain correction previews, approvals, compensation records, dependency reports, and reconciliation; require every corrected balance to remain reconstructible from append-only history.

### Control C10 17

**Original requirement C10.17:** Govern balance changes through release pinning and review by game design and training content roles. Assess whether incentives could encourage overtraining, skipped recovery, or confusion between fictional and actual bodily needs.

- [ ] **C10.17.01** Pin resource balance parameters, consumption rates, item prices, recovery grants, and thresholds to a reviewed rules release; record responsible game-design and training-content reviewers.
- [ ] **C10.17.02** Describe proposed changes with representative before/after outcomes, affected campaign modes, migration scope, and potential impacts on exercise incentives and recovery participation.
- [ ] **C10.17.03** Review whether rewards encourage excessive duration, extra incline, compensatory sessions, skipped rest, or confusion between fictional shortages and actual bodily requirements.
- [ ] **C10.17.04** Separate prospective rule adoption from historical ledger correction; preserve existing campaign definitions unless an explicit reviewed migration specifies their new treatment.
- [ ] **C10.17.05** Provide rollback or forward-repair procedures for defective balance releases; retain previous rules and affected operation identities needed to explain or compensate consequences.
- [ ] **C10.17.06** Playtest low-activity, partial-session, recovery, and high-credit strategies under changed rules; verify continued narrative access without pressure for unplanned additional exercise.
- [ ] **C10.17.07** Test mid-day updates, retired rules, and stale clients; ensure active transactions use pinned revisions and no silent consumption or price change occurs.
- [ ] **C10.17.08** Retain release comparisons, incentive findings, approvals, migration tests, and rollback evidence; require attributable review before any balance change enters the released manifest.

### Control C10 18

**Original requirement C10.18:** Verify ledger reconciliation, boundary values, invalid units, arithmetic precision, purchase affordability, stack limits, item ownership, condition transitions, and derived-weight consistency using deterministic fixtures.

- [ ] **C10.18.01** Build deterministic fixtures for initialization, ledger reconciliation, arithmetic scale, bounds, affordability, stack limits, ownership, condition graphs, and derived pack-weight calculation.
- [ ] **C10.18.02** Record independent expected balances, inventories, masses, and state transitions after each operation; avoid deriving test expectations through the same production calculation functions.
- [ ] **C10.18.03** Exercise zero, exact-capacity, maximum-magnitude, fractional-unit, exact-cost, and unknown-value boundaries using the declared canonical resource units and item revisions.
- [ ] **C10.18.04** Validate rejection of incompatible units, excess precision, invalid categories, duplicate ownership, unsupported repairs, negative prohibited balances, and overfilled containers.
- [ ] **C10.18.05** Test compound operations and corrections as complete causal sequences; compare materialized projections to initialization plus committed ledger entries after every accepted transaction.
- [ ] **C10.18.06** Repeat fixtures across supported serialization, locale, and runtime configurations; require identical fixed-point or decimal results and no formatting-dependent validation behavior.
- [ ] **C10.18.07** Inspect resulting explanations and domain labels so arithmetic correctness does not conceal virtual quantities presented as actual physical observations or training requirements.
- [ ] **C10.18.08** Archive expected tables, fixture versions, execution results, and reconciliation reports; require all supported resource invariants and boundary cases to pass without unexplained numerical differences.

### Control C10 19

**Original requirement C10.19:** Test duplicate effects, forced termination during compound transactions, SQLite lock contention, concurrent-tab purchases, launcher restart, repository restoration, migrations, corrected inputs, and compensating entries. Prove that ledger reconstruction matches committed balances and launch repetition leaves them unchanged.

- [ ] **C10.19.01** Prepare fault fixtures for duplicate effects, compound transactions, lock contention, competing purchases, restart, restore, migration, corrected inputs, and compensation under pinned rules.
- [ ] **C10.19.02** Capture initial ledger, materialized balances, inventory, conditions, operation receipts, dossier references, and campaign position before each interruption or concurrency experiment.
- [ ] **C10.19.03** Terminate before commit, after each tentative compound mutation, and after commit before response; verify complete rollback or one durable effect set recoverable by operation identity.
- [ ] **C10.19.04** Hold SQLite locks and race unaffordable aggregate purchases; require bounded handling, explicit conflict results, and no debt, silent item loss, or duplicate charges.
- [ ] **C10.19.05** Repeat launches and resource submissions before and after repository restoration; confirm restored receipts prevent replayed rewards, consumption, repairs, and purchases.
- [ ] **C10.19.06** Apply approved migrations and compensating corrections to known errors; reconcile every projected balance and item state against independently reconstructed ledger history.
- [ ] **C10.19.07** Compare launch-only runs with the unchanged ledger and scenario clock; require zero resource changes from invocation count, browser display, or calendar rollover.
- [ ] **C10.19.08** Retain fault traces, restored inventories, duplicate counts, migration approvals, and reconstruction results; accept exact agreement between authoritative ledger and committed materialized balances.

### Control C10 20

**Original requirement C10.20:** Enumerate resource-exhaustion states and verify that each has a reachable continuation. Review interface labels and exports for domain separation, and demonstrate that no virtual balance can directly modify prescribed workout or equipment state.

- [ ] **C10.20.01** Create an exhaustion-state inventory covering each resource individually and supported combined shortages, including broken equipment, unknown quantities, and mandatory branch dependencies.
- [ ] **C10.20.02** Map each state to an authored available recovery, explicit deferral, or approved virtual transfer; verify recovery prerequisites remain satisfiable from the exhausted state.
- [ ] **C10.20.03** Run reachability analysis and concrete walkthroughs until participation resumes; include retired characters, missing optional assets, and delayed encounters in recovery-path fixtures.
- [ ] **C10.20.04** Inspect interface labels, alerts, journal summaries, charts, and exports for fictional domain tags, canonical units, scenario assumptions, and accurate physical-presence claims.
- [ ] **C10.20.05** Attempt direct training, actual measurement, recovery-assignment, and equipment mutations from every resource target; verify allow-list rejection and unchanged protected record hashes.
- [ ] **C10.20.06** Test users with partial workouts, planned recovery, and no accepted walking activity; ensure exhaustion continuation never requires compensatory exertion or fabricated activity credit.
- [ ] **C10.20.07** Review failure messages and incentives with training and narrative owners; resolve ambiguity suggesting game water, food, morale, or fatigue measures real bodily needs.
- [ ] **C10.20.08** Retain state coverage, reachable recovery evidence, labeling inspections, and boundary tests; require complete exhaustion continuation and zero resource-originated real-training or equipment changes.

## C11 Trail knowledge activities

**Accountable owners:** Instructional-content owner for learning objectives; qualified subject reviewers for relevant content; accessibility reviewer for exercise formats; publisher for approved versions.

**Interfaces:** Consumes locally stored stage context, source evidence, learning objectives, and prior attempts through the local service. Produces versioned `ActivityDefinition`, `QuestionVersion`, `EvaluationRule`, `LearningAttempt`, feedback, and preparation-history records persisted in authoritative repository-local SQLite. Workout credit remains under the workout/progression components.

**Required evidence:** Objective-to-activity map; local attempt schema; source register; evaluation rules; reviewer approvals; representative activities; accessibility results; version/correction tests; launch-resume, local-service recovery, and attempt-deduplication results.

**Exit criterion:** Each published activity teaches a stated preparation skill, provides supported and context-appropriate feedback, remains accessible, and records reproducible attempts. Learning outcomes cannot silently alter physical prescriptions or imply validated fitness/readiness.

### Control C11 01

**Original requirement C11.01:** Define schemas for learning objectives, activities, questions, evidence references, evaluation rules, hints, attempts, explanations, and revision history.

- [ ] **C11.01.01** Define schemas for objective, activity, question, evidence reference, evaluation rule, hint, attempt, explanation, and revision records with stable identities and relationships.
- [ ] **C11.01.02** Specify response formats, permissible score types, optional reflection fields, completion semantics, and explicit unknown values; distinguish judgment activities from objectively evaluated questions.
- [ ] **C11.01.03** Require activity/question revisions to reference their approved evaluation and explanation versions; preserve schema compatibility rules and previously published identifiers across supported content updates.
- [ ] **C11.01.04** Implement import and submission validation through the local service; reject malformed responses, orphaned hints, missing evidence, and unsupported rule/schema versions before persistence.
- [ ] **C11.01.05** Round-trip map, inventory, ordering, comparison, and short-scenario examples through storage and package export; verify their relationships and original response meaning remain intact.
- [ ] **C11.01.06** Exercise missing objectives, duplicate question IDs, circular hint references, incompatible response types, and invalid scoring ranges; confirm specific rejection messages identify affected records.
- [ ] **C11.01.07** Interrupt activity import or attempt submission and restart; ensure partially created record families cannot become publishable activities or falsely completed authoritative attempts.
- [ ] **C11.01.08** Archive schema definitions, validation fixtures, and relationship checks; accept only when every enabled activity format has complete contracts and zero unresolved reference-integrity defects.

### Control C11 02

**Original requirement C11.02:** Associate every activity with an explicit preparation skill and intended learning outcome; identify the prerequisite knowledge and the evidence of successful practice.

- [ ] **C11.02.01** Create an objective-to-activity map stating preparation skill, intended outcome, prerequisite knowledge, practice task, evaluation rationale, and observable evidence of successful practice.
- [ ] **C11.02.02** Specify objectives in terms of map interpretation, planning reasoning, equipment tradeoffs, or information evaluation rather than unsupported claims of physical readiness or competence.
- [ ] **C11.02.03** Identify which response artifacts demonstrate the intended reasoning, including calculation workings, selected tradeoffs, explanation, or correctly located features where the format supports them.
- [ ] **C11.02.04** Have the instructional reviewer verify alignment among prerequisite, task, feedback, and evidence; record revisions when an activity measures recall instead of its claimed skill.
- [ ] **C11.02.05** Complete representative activities using the intended reasoning and inspect recorded evidence; verify successful practice satisfies the published outcome without requiring undisclosed prior knowledge.
- [ ] **C11.02.06** Try correct-looking answers produced without relevant information and plausible alternative reasoning; ensure evaluation distinguishes supported practice from arbitrary guessing where objective claims require reasoning.
- [ ] **C11.02.07** Revise an objective after alignment failure; preserve published attempt associations and explain which future activity revision now measures the corrected outcome appropriately.
- [ ] **C11.02.08** Archive reviewed objective maps and sample evidence; accept only when every published activity has a clear preparation outcome and defensible evidence of its stated practice.

### Control C11 03

**Original requirement C11.03:** Maintain a topic taxonomy covering relevant preparation tasks such as itinerary planning, map interpretation, equipment tradeoffs, resupply planning, and information evaluation.

- [ ] **C11.03.01** Define a controlled topic taxonomy for itinerary planning, map interpretation, equipment tradeoffs, resupply planning, information evaluation, and other explicitly approved preparation categories.
- [ ] **C11.03.02** Assign stable topic IDs, descriptions, inclusion/exclusion boundaries, parent relationships, aliases, and revision rules; prohibit category changes based solely on ambiguous display names.
- [ ] **C11.03.03** Tag each activity and objective with reviewed topics and optional cross-topic associations; identify prerequisites separately from primary instructional focus for accurate selection.
- [ ] **C11.03.04** Specify coverage reporting and search/filter behavior using taxonomy identities; unknown or retired tags must enter review rather than silently disappear from catalog results.
- [ ] **C11.03.05** Inspect representative cross-topic activities and independently verify classification; confirm equipment/resupply overlaps remain discoverable without duplicating their underlying activity or attempt records.
- [ ] **C11.03.06** Introduce orphaned, circular, duplicate, and contradictory taxonomy entries; reject invalid structures and report misclassified activities with attributable remediation owners and versions.
- [ ] **C11.03.07** Rename or retire a topic through a migration preview; preserve historical activity/attempt associations and redirect deliberate review selections without hiding relevant prior material.
- [ ] **C11.03.08** Archive taxonomy decisions and coverage/search checks; accept only when every released activity has approved classification and all declared preparation topics have explained coverage dispositions.

### Control C11 04

**Original requirement C11.04:** Identify sourced facts, supplied assumptions, fictional constraints, and deliberately unknown information; ensure evaluation does not depend on undisclosed assumptions.

- [ ] **C11.04.01** Define content annotations separating sourced facts, supplied assumptions, fictional constraints, and deliberately unknown information, with references to the exact activity/question revision.
- [ ] **C11.04.02** List every assumption affecting accepted answers, available choices, scoring, or explanation; include quantities, conditions, priorities, and uncertainty before the learner submits a response.
- [ ] **C11.04.03** Specify how diagrams and scenario text reveal classifications; essential evaluation inputs cannot reside only in hidden metadata, feedback revealed afterward, or inaccessible imagery.
- [ ] **C11.04.04** Review evaluation rules against presented information and explicitly unknown fields; permit justified uncertainty rather than requiring learners to infer an undisclosed preferred scenario.
- [ ] **C11.04.05** Solve activities using only their rendered prompts and accessible alternatives; verify independent reviewers can derive accepted answers without designer hints or unstated knowledge.
- [ ] **C11.04.06** Remove or change a decisive assumption in fixtures; require validation/review to detect underdetermined scoring or update the activity to allow defensible alternatives.
- [ ] **C11.04.07** Correct an omitted assumption after publication; preserve affected attempts, annotate the flaw, and avoid retroactively treating learners' earlier responses as unreasonable or incorrect.
- [ ] **C11.04.08** Archive assumption inventories and independent solution reviews; accept only when every scored distinction follows from disclosed evidence/assumptions and all deliberate uncertainty is represented honestly.

### Control C11 05

**Original requirement C11.05:** Attach evidence, source dates, applicability, and review deadlines to factual content; preserve the rationale for adapting source material into an activity.

- [ ] **C11.05.01** Define factual-content evidence records with publisher, source URL/reference, publication/acquisition dates, applicability, confidence, licensing, review deadline, and supported question/explanation assertion identifiers.
- [ ] **C11.05.02** Record adaptation rationale explaining simplification, scenario constraints, omitted complexity, and interpretation; reviewers must distinguish source statements from authored instructional framing and assumptions.
- [ ] **C11.05.03** Set source-specific review deadlines and change triggers according to actual content volatility; dated information cannot silently appear as current operational trail guidance.
- [ ] **C11.05.04** Require evidence links and adaptation review before publication; missing or retired sources produce a blocked claim or an explicitly reviewed historical-context limitation.
- [ ] **C11.05.05** Trace sample question prompts and feedback assertions to retained evidence; confirm citations support the exact expressed claim rather than merely addressing the same general topic.
- [ ] **C11.05.06** Exercise overdue reviews, conflicting sources, unavailable references, and license restrictions; flag affected activities and prevent unsupported claims from entering newly approved packages.
- [ ] **C11.05.07** Replace or correct evidence through a versioned content operation; preserve previously delivered explanations and annotate affected attempts when their factual basis materially changes.
- [ ] **C11.05.08** Archive evidence coverage and adaptation decisions; accept only when every released factual assertion has applicable support, complete review status, and an attributable instructional interpretation.

### Control C11 06

**Original requirement C11.06:** Version accepted answers, partial-credit rules, defensible alternatives, and explanations; link each attempt to the exact question and evaluation versions presented.

- [ ] **C11.06.01** Version question prompts, accepted answers, partial-credit criteria, defensible alternatives, scoring parameters, and explanations together with explicit evaluation-policy identity and publication compatibility rules.
- [ ] **C11.06.02** Specify objective-question rounding, unit equivalence, response normalization, and tolerance boundaries; judgment activities require documented reasoning criteria rather than an unexplained single-answer numerical score.
- [ ] **C11.06.03** Pin each attempt to the exact question, evaluation, hint, and explanation versions presented; current catalog updates cannot recompute its historical result silently.
- [ ] **C11.06.04** Create independent expected results for fully correct, partly correct, alternative defensible, unsupported, omitted, and malformed responses with explicit reasons and boundary values.
- [ ] **C11.06.05** Run evaluation fixtures against those expectations; confirm partial-credit totals and explanation selection follow the pinned policy and all accepted alternatives receive documented treatment.
- [ ] **C11.06.06** Change the scoring policy and repeat an old response as a new attempt; preserve the historical result while applying the new version only where authorized.
- [ ] **C11.06.07** Handle an erroneous scoring revision with an explicit correction record; retain original feedback, annotate affected results, and record any approved revised evaluation separately.
- [ ] **C11.06.08** Archive evaluation versions, expected-result fixtures, and correction demonstrations; accept only when every attempt remains reproducible and no scoring change silently rewrites delivered history.

### Control C11 07

**Original requirement C11.07:** Persist attempt response, feedback, score when meaningful, completion state, time, optional reflection, campaign/day identifier, and content versions in local SQLite; browser storage cannot be the sole record.

- [ ] **C11.07.01** Define SQLite attempt records containing response, delivered feedback, meaningful score where applicable, completion state, timestamps, optional reflection, campaign/day identity, and pinned content/evaluation revisions.
- [ ] **C11.07.02** Specify attempt lifecycle and response serialization for every enabled format; distinguish draft, submitted, evaluated, completed, and abandoned records without fabricating absent responses.
- [ ] **C11.07.03** Persist attempt and evaluation results through validated local-service mutations with stable operation identity; browser storage may hold replaceable drafts but cannot acknowledge canonical completion.
- [ ] **C11.07.04** Enforce foreign keys, unique effective submission identities, and permitted revision updates; optional reflections require separate editable revisions from immutable submitted answers and delivered feedback.
- [ ] **C11.07.05** Submit an activity and restart the service/browser; compare the restored response, score, explanation, day association, reflection, and completion state with original committed records.
- [ ] **C11.07.06** Delete browser cache and issue duplicate/stale submissions; verify durable attempts remain available, retries return the existing result, and conflicts receive an explicit resolution path.
- [ ] **C11.07.07** Inject database failure before commit and response loss after commit; show unsaved failure or recover the existing receipt without duplicated attempts or invented completion.
- [ ] **C11.07.08** Archive persistence/restart and constraint evidence; accept only when all acknowledged learning results survive relaunch with exact presented versions and are independent of browser-only storage.

### Control C11 08

**Original requirement C11.08:** Support activity formats such as annotated maps, elevation interpretation, inventory puzzles, tradeoff comparisons, ordering, and short scenarios through shared accessible interaction contracts.

- [ ] **C11.08.01** Specify shared interaction contracts for map annotation, elevation interpretation, inventory puzzles, comparisons, ordering, and short scenarios, including response models, hints, submission, and resume semantics.
- [ ] **C11.08.02** Define an equivalent keyboard/non-drag method for every essential spatial or ordering operation; diagrams require text descriptions exposing the same decision-relevant data.
- [ ] **C11.08.03** Implement format adapters using common validated response and evaluation interfaces; retain format-specific information rather than flattening map coordinates or ranked choices into ambiguous text.
- [ ] **C11.08.04** Specify focus order, error identification, selection state, accessible names, and feedback presentation consistently; users must understand changed selections without color or pointer precision alone.
- [ ] **C11.08.05** Complete one activity per format with keyboard and accessible alternatives; compare resulting responses and evaluations against the pointer/visual reference interaction for equivalent instructional outcomes.
- [ ] **C11.08.06** Exercise invalid coordinates, duplicate rankings, unavailable items, missing comparison fields, and inaccessible diagrams; provide specific corrections without discarding already accepted response elements.
- [ ] **C11.08.07** Reload and restart during partially completed interactions; restore the same prompt/version and equivalent response state regardless of which accessible interaction method was used.
- [ ] **C11.08.08** Archive format-contract and accessibility comparisons; accept only when every enabled activity supports equivalent essential operations and produces validated, reproducible responses across interaction methods.

### Control C11 09

**Original requirement C11.09:** Distinguish judgment activities from objectively scored questions; permit multiple defensible decisions where conditions, priorities, or uncertainty justify them.

- [ ] **C11.09.01** Classify each question as objective, judgment, or mixed, with explicit scoring applicability, accepted reasoning criteria, uncertainty, and priorities that may justify different decisions.
- [ ] **C11.09.02** Define conditions under which alternatives are defensible, including differing risk preferences, budgets, comfort priorities, timing assumptions, or incomplete evidence already disclosed in the scenario.
- [ ] **C11.09.03** Separate objectively incorrect arithmetic/fact claims from value-dependent choices; feedback must identify the specific unsupported assertion rather than penalize an alternative priority automatically.
- [ ] **C11.09.04** Require instructional approval of answer rubrics and example responses; reviewers must explain why a rejected strategy is incompatible with supplied facts or stated constraints.
- [ ] **C11.09.05** Evaluate multiple plausible strategies under contrasting stated priorities; verify all defensible decisions receive appropriate acknowledgment and none is mislabeled as universally best or unsafe.
- [ ] **C11.09.06** Submit an unsupported decision with persuasive wording and a valid unconventional choice; ensure evaluation follows evidence/constraints rather than superficial keywords or designer preference.
- [ ] **C11.09.07** Correct a judgment rubric that excluded a defensible answer; annotate prior affected attempts and preserve original results alongside the approved revised interpretation.
- [ ] **C11.09.08** Archive classification and alternative-answer review; accept only when objective scores are reproducible and all judgment conclusions are supported by disclosed conditions and explicit reasoning.

### Control C11 10

**Original requirement C11.10:** Explain reasoning, tradeoffs, and uncertainty after an attempt; avoid equating scenario success with demonstrated real-world competence or physical readiness.

- [ ] **C11.10.01** Specify feedback fields for reasoning, relevant evidence, choice tradeoffs, uncertainty, alternative strategies, and limits of applicability linked to the presented question/evaluation revision.
- [ ] **C11.10.02** Explain why an answer is supported or limited using scenario information; feedback must add instructional value beyond repeating the selected option or displaying a score.
- [ ] **C11.10.03** Distinguish demonstrated practice within the activity from real-world competence, physical capacity, or hike readiness; remove badges/text implying validated capability from question success.
- [ ] **C11.10.04** Provide understandable feedback for incorrect, partial, defensible-alternative, and unanswered attempts; preserve respectful language and an accessible path to review relevant source context.
- [ ] **C11.10.05** Inspect sample explanations independently for correctness, clarity, and acknowledged uncertainty; confirm users can identify which assumptions would change the conclusion or tradeoff.
- [ ] **C11.10.06** Submit a perfect knowledge score and trigger reward/dashboard rendering; verify no physical-readiness label, medical inference, or automatic assignment escalation appears in any dependent view.
- [ ] **C11.10.07** Correct misleading feedback through versioned publication and attempt annotations; retain the original delivered explanation as historical evidence with the reason for subsequent correction.
- [ ] **C11.10.08** Archive explanation reviews and dependent-display boundary checks; accept only when every evaluated attempt receives supported reasoning and no learning result implies independently validated real-world readiness.

### Control C11 11

**Original requirement C11.11:** Keep learning completion and scores separate from actual workout completion; educational mistakes must not increase required physical exertion or erase recorded training.

- [ ] **C11.11.01** Define distinct learning completion, knowledge score, workout completion, actual distance, and physical-target fields with separate authoritative records and permitted mutation services.
- [ ] **C11.11.02** Specify any enabled educational campaign credit using its own progression-policy version; knowledge participation may advance approved story/preparation outcomes without inventing physical movement.
- [ ] **C11.11.03** Restrict learning evaluation effects to attempt and authorized fictional/preparation records; scoring services cannot write workout quantities, erase activity, or modify accepted exercise requirements.
- [ ] **C11.11.04** Compare database snapshots before and after correct, incorrect, partial, repeated, and abandoned learning attempts; physical assignments and accepted workout records must remain unchanged.
- [ ] **C11.11.05** Exercise educational failure branches and depleted fictional resources; confirm users retain access to recovery, review, story continuation, and recorded activity without compensatory exercise demands.
- [ ] **C11.11.06** Inspect dashboard and dossier labels for learning/physical distinctions; knowledge completion must not be presented as walked mileage, incline exposure, or a finished physical session.
- [ ] **C11.11.07** Interrupt learning submission and restart; reconcile attempt/preparation state without converting unsaved responses or retries into workout completion or duplicate physical activity credits.
- [ ] **C11.11.08** Archive authority review and physical-boundary cases; accept only when every learning outcome preserves actual activity and no educational mistake increases required physical exertion.

### Control C11 12

**Original requirement C11.12:** Select activities by stage relevance, prior attempts, and stated interests; provide deliberate review without excessive repetition or permanently hiding important material after one attempt.

- [ ] **C11.12.01** Define selection inputs comprising pinned stage relevance, prior attempts, review history, stated interests, activity availability, and selection-policy version; document priority and tie-break rules.
- [ ] **C11.12.02** Specify repetition limits and intentional review exemptions; important objectives remain deliberately reachable after success, failure, skipped participation, or a previous content revision.
- [ ] **C11.12.03** Distinguish recommendation from required participation; missing optional interests use documented neutral selection rather than inferred fitness, identity, or hidden competency profiles.
- [ ] **C11.12.04** Record selection reasons and eligible alternatives so users/reviewers can explain why an activity appeared; retain content-version compatibility with the active dossier.
- [ ] **C11.12.05** Run histories with new, successful, failed, repeated, and revised activities; verify stage-relevant material appears appropriately and no important topic disappears permanently after one attempt.
- [ ] **C11.12.06** Exercise sparse catalogs, all-previously-seen activities, withdrawn content, and conflicting interests; provide deliberate review or an honest no-available-activity state without excessive forced repetition.
- [ ] **C11.12.07** Restart an unfinished selected activity after catalog changes; preserve its pinned content unless an explicit correction/withdrawal applies, then explain any approved replacement.
- [ ] **C11.12.08** Archive selection fixtures and coverage/repetition reports; accept only when recommendations follow documented inputs and all released essential learning material remains accessible for deliberate review.

### Control C11 13

**Original requirement C11.13:** Make activity timing optional and persist resumable state through the local service; later launches restore unfinished attempts and impose no essential speed-scored interaction during walking.

- [ ] **C11.13.01** Specify optional timing modes, untimed defaults, elapsed-time semantics, pause/deferral behavior, and resumable response state for each enabled activity format and learning objective.
- [ ] **C11.13.02** Persist prompt identity, answer draft, hint state, interaction position, timing preference, and authoritative checkpoint revision through the local service with explicit save-status feedback.
- [ ] **C11.13.03** Ensure timing affects only expressly disclosed optional evaluation modes; walking presentation cannot require essential rapid responses or penalize choosing the untimed equivalent.
- [ ] **C11.13.04** Provide pause and return-later actions retaining original question/evaluation versions; finishing a physical session cannot automatically submit, fail, or abandon the learning attempt.
- [ ] **C11.13.05** Relaunch unfinished timed and untimed attempts through the normal launcher; verify exact response/hint state restoration and no fabricated elapsed performance during unobserved gaps.
- [ ] **C11.13.06** Exercise browser suspension, clock changes, delayed responses, and long deferrals; require documented timing behavior without assignment escalation, lost options, or silent speed-based penalties.
- [ ] **C11.13.07** Inject save failure and restart the service; show provisional state distinctly, recover committed checkpoints, and offer reconciliation/export where feasible without claiming unsaved drafts are durable.
- [ ] **C11.13.08** Archive timing/resume cases and walking-context review; accept only when every essential activity has an untimed path and unfinished attempts restore correctly after interruption.

### Control C11 14

**Original requirement C11.14:** Provide keyboard operation, untimed modes, accessible diagrams, text alternatives, optional hints, and equivalent non-drag interactions for every essential activity.

- [ ] **C11.14.01** Inventory essential operations and equivalent accessible alternatives for selection, annotation, ordering, comparison, hint access, submission, feedback review, pause, and resumption across activity formats.
- [ ] **C11.14.02** Specify keyboard bindings, focus behavior, visible labels, text alternatives, diagram descriptions, error announcements, untimed modes, and optional-hint semantics in the interaction contract.
- [ ] **C11.14.03** Provide non-drag ordering and map-selection interfaces exposing the same information and valid outcomes as graphical controls; essential reasoning cannot depend solely on color or location.
- [ ] **C11.14.04** Ensure hints are optional, reachable, clearly identified, and compatible with declared evaluation rules; requesting a hint cannot silently change physical targets or erase prior work.
- [ ] **C11.14.05** Complete every enabled activity by keyboard and representative screen reader; compare accepted responses, scores where meaningful, hints, and feedback with visual/pointer reference outcomes.
- [ ] **C11.14.06** Exercise enlarged text, reduced motion, absent images, narrow screens, long descriptions, and timeout preferences; verify required choices and explanations remain readable and reachable.
- [ ] **C11.14.07** Repair accessibility defects and repeat affected format flows after reload; confirm fixes preserve response state and do not weaken source context or evaluation equivalence.
- [ ] **C11.14.08** Archive operation coverage and accessible-equivalence evidence; accept only when all essential interactions pass declared accessibility criteria and untimed/non-drag alternatives support identical instructional objectives.

### Control C11 15

**Original requirement C11.15:** Explain the scenario's applicability and source context when information may change; offer current authoritative references rather than presenting an exercise as an operational trail instruction.

- [ ] **C11.15.01** Specify applicability notes identifying fictional scenario scope, source publisher/date, geographic context, uncertainty, and whether underlying information is historical or subject to change.
- [ ] **C11.15.02** Include authoritative reference links and retained source metadata beside change-sensitive learning topics; distinguish exercise assumptions from instructions for current real-world trail operation.
- [ ] **C11.15.03** Define freshness checks and review triggers before new publication; expired or unavailable sources require review, historical labeling, or corrected content rather than current-information claims.
- [ ] **C11.15.04** Review explanations for imperative wording that could be mistaken for live guidance; replace unsupported operational statements with explicit scenario context and appropriate authoritative reference framing.
- [ ] **C11.15.05** Inspect representative changing-information activities and verify users can identify the source date, scenario assumptions, limitation, and route/geographic applicability before relying on the conclusion.
- [ ] **C11.15.06** Exercise broken references, old conditions, and conflicting current notices; flag affected claims and offer reviewed context without silently importing hypothetical conditions as present facts.
- [ ] **C11.15.07** Update references through a versioned correction process; preserve prior delivered context and annotate materially affected historical attempts rather than silently replacing their evidence basis.
- [ ] **C11.15.08** Archive applicability/source-context reviews and reference tests; accept only when change-sensitive content is clearly contextualized and every factual claim has an appropriate dated authoritative reference.

### Control C11 16

**Original requirement C11.16:** Document any adaptive selection inputs and rules; prohibit inference of medical condition, physical capacity, or hike readiness from knowledge-question performance.

- [ ] **C11.16.01** Inventory adaptive inputs, derived features, selection rules, thresholds, retention, and rule versions; limit inputs to documented activity history, stated interests, and approved learning preferences.
- [ ] **C11.16.02** Describe why each input affects activity selection and expose understandable selection reasons; avoid hidden composites presented as clinical, physical-capacity, or general hike-readiness assessments.
- [ ] **C11.16.03** Restrict adaptive services from writing medical attributes, fitness classifications, or exercise targets; knowledge-question performance remains evidence of activity-specific learning interaction only.
- [ ] **C11.16.04** Define neutral behavior for sparse data, skipped questions, optional missing preferences, and conflicting attempts; absence or low scores cannot become an inferred impairment.
- [ ] **C11.16.05** Run contrasting score histories with identical physical plans; verify changed recommendations stay within approved learning rules while physical targets and readiness labels remain unaffected.
- [ ] **C11.16.06** Inject disallowed health/capacity fields into adaptive inputs and outputs; reject them with rule-specific diagnostics and confirm dependent dashboards do not infer prohibited classifications.
- [ ] **C11.16.07** Version adaptive-policy changes prospectively and review affected recommendations; preserve the policy explaining earlier selections without rewriting attempt history or assigning retrospective physical meaning.
- [ ] **C11.16.08** Archive input/output authority review and adaptation fixtures; accept only when every recommendation is explainable from allowed inputs and no medical or physical-readiness inference is produced.

### Control C11 17

**Original requirement C11.17:** Define correction handling for erroneous questions and scoring; preserve prior attempt history, annotate affected results, and avoid silently changing the feedback previously delivered.

- [ ] **C11.17.01** Define correction records identifying erroneous question/evaluation revision, reason, affected attempts, reviewer, replacement version, annotation text, and permitted result-adjustment behavior for published content.
- [ ] **C11.17.02** Preserve original submitted responses, score, delivered explanation, and version references; approved revised results must be separately attributable rather than overwriting historical feedback.
- [ ] **C11.17.03** Specify how unfinished attempts adopt corrected questions and how completed attempts receive annotations; changing decisive assumptions requires explicit disclosure and appropriate restart/review options.
- [ ] **C11.17.04** Compute affected attempt counts and downstream learning summaries before applying correction; physical activity, completed workouts, and campaign history cannot be silently erased or intensified.
- [ ] **C11.17.05** Correct one factual prompt and one partial-credit rule; compare original and revised result records with independently expected annotations and unchanged original delivered explanations.
- [ ] **C11.17.06** Exercise repeated correction requests, stale attempts, and mutually conflicting replacement proposals; require idempotent application and explicit reviewer resolution without duplicate adjustments or broken lineage.
- [ ] **C11.17.07** Interrupt correction persistence and restart; reconcile affected annotations, replacement references, and derived learning summaries against the durable correction receipt before reporting success.
- [ ] **C11.17.08** Archive correction impact and recovery evidence; accept only when every affected result is traceable, original history remains available, and revised evaluation is explicitly identified.

### Control C11 18

**Original requirement C11.18:** Bundle activity dependencies locally, use idempotent local-service submissions, and deduplicate retries transactionally; distinguish browser disconnection from unavailable internet and preserve unfinished attempts after service restart.

- [ ] **C11.18.01** Inventory question, diagram, hint, evaluation, explanation, and source-context dependencies; package required activity files locally with pinned versions, checksums, and approved repository-relative paths.
- [ ] **C11.18.02** Define submission requests containing attempt identity, mutation ID, expected revision, content/evaluation versions, response payload, and optional reflection; validate through the loopback service.
- [ ] **C11.18.03** Deduplicate submission and evaluation effects transactionally in SQLite; repeated requests return the effective saved result rather than creating another completed attempt or duplicate credit.
- [ ] **C11.18.04** Specify external-internet-loss versus local-service-loss presentation; local-only learning remains usable offline, while failed loopback writes must identify unsaved provisional response state.
- [ ] **C11.18.05** Disconnect internet and complete a packaged activity; verify response, feedback, and attempt history persist without account login, remote assets, or external evaluation requests.
- [ ] **C11.18.06** Lose submission acknowledgment after commit and retry from two tabs; verify one effective attempt/evaluation receipt and reject conflicting payloads using the same operation identity.
- [ ] **C11.18.07** Restart the service with an unfinished attempt and simulate database contention; restore committed response/hint state and provide bounded retry/conflict handling without losing presented versions.
- [ ] **C11.18.08** Archive dependency closure, offline completion, and retry/restart traces; accept only when all acknowledged attempts are durable, deduplicated, locally evaluable, and recoverable after service interruption.

### Control C11 19

**Original requirement C11.19:** Obtain subject review of correctness, alternative answers, distractors, evidence support, realistic assumptions, and explanation quality; record decisions where reviewers disagree.

- [ ] **C11.19.01** Define subject-review criteria for factual correctness, valid alternatives, distractor rationale, evidence support, realistic assumptions, evaluation boundaries, and instructional quality before selecting candidate activities.
- [ ] **C11.19.02** Assign an accountable subject reviewer and record their review scope; use specialist consultation when a claim exceeds the configured reviewer's demonstrated content expertise.
- [ ] **C11.19.03** Present exact published prompt, diagram, response rubric, hints, and explanations together; reviewers must evaluate the same information and assumptions learners actually receive.
- [ ] **C11.19.04** Require written rationale for accepted alternatives and distractor rejection; judgments based on priorities or uncertainty need explicit criteria rather than undocumented designer preference.
- [ ] **C11.19.05** Independently solve representative activities without author coaching; compare solutions with accepted answers, partial-credit rules, and supported evidence to detect undisclosed assumptions or ambiguity.
- [ ] **C11.19.06** Record reviewer disagreements with competing reasons and affected content IDs; block material unresolved factual/evaluation conflicts or document a reviewed multiple-answer/uncertainty treatment.
- [ ] **C11.19.07** Revise disputed prompts or feedback and obtain targeted rereview; preserve prior decisions and version relationships so approval cannot be reused for changed content.
- [ ] **C11.19.08** Archive attributable review decisions and final rubric examples; accept only when all released activities have appropriate subject review and every material disagreement has an explicit disposition.

### Control C11 20

**Original requirement C11.20:** Verify accessibility, repeated attempts, hints, relaunch/resume, revisions, corrected scoring, internet-free completion, duplicate submission, local-service interruption, and database contention.

- [ ] **C11.20.01** Create verification cases for accessible interaction, repeated attempts, hints, relaunch/resume, content revisions, corrected scoring, offline completion, duplicate submissions, service interruption, and database contention.
- [ ] **C11.20.02** Specify initial attempt versions, response/hint state, expected evaluation, operation identity, campaign/day associations, fault boundary, and durable result for each test case.
- [ ] **C11.20.03** Complete each enabled format with keyboard and representative assistive technology; verify equivalent prompts, hints, response meaning, feedback, and resumable state across interaction methods.
- [ ] **C11.20.04** Repeat activities before and after content/evaluation changes; confirm each attempt retains its presented versions and corrections annotate rather than overwrite original delivered feedback.
- [ ] **C11.20.05** Exercise internet-disconnected completion and loopback termination separately; verify normal local commits versus clearly provisional state and restored authoritative checkpoints after service restart.
- [ ] **C11.20.06** Inject duplicate/conflicting submissions, locks, and lost acknowledgments around commits; reconcile one effective result per operation and require explicit conflict/retry behavior without fabricated completion.
- [ ] **C11.20.07** Link detected failures to reproducible fixtures and corrected revisions; rerun affected scenarios and preserve original failure evidence alongside the confirming successful results.
- [ ] **C11.20.08** Archive the full activity verification matrix; accept only when every required format and lifecycle case passes with preserved attempt history and zero learning-to-physical-accounting leakage.

## C12 Characters and story continuity

**Accountable owner:** Narrative Lead. **Reviewing roles:** Content Systems Lead, Game Systems Lead, Training Content Reviewer, Editorial Reviewer, Accessibility Lead, and QA Lead.

**Interfaces:** Reads C08 decisions, C09 reservations, and C10 state from the local repository; writes SQLite campaign facts, character transitions, and C13 references through the local service. Uses the persisted hike-day dossier revision. Optional generated dialogue consumes approved facts but cannot authoritatively mutate them.

**Required evidence:** Character schemas and SQLite transition constraints; approved biographies; story graphs; fact registry rules; versioned dossier/branch manifest; editorial review; transaction/restart/replay fixtures; accessibility assessment; migration procedure; generated-dialogue controls where enabled.

**Exit criterion:** Every supported story state has approved content and a tested continuation/conclusion. SQLite-backed narrative facts survive tab conflicts and restarts; resuming an unfinished day preserves its story/dossier revision. Optional generation has no independent campaign, training, or equipment authority.

### Control C12 01

**Original requirement C12.01:** Version character records with stable ID, approved biography, narrative role, personality constraints, relationship model, whereabouts rules, dialogue/portrait references, appearance history, and retirement status.

- [ ] **C12.01.01** Define character schema with stable identity, approved biography, role, personality constraints, relationship model, whereabouts rules, dialogue, portrait, appearance history, and retirement status.
- [ ] **C12.01.02** Version biography and characterization changes independently from display names; pin campaign appearances to approved character revisions and compatible dialogue or portrait dependencies.
- [ ] **C12.01.03** Specify introduction prerequisites, plausible travel constraints, allowed narrative roles, and unavailable states; distinguish authored fictional identity from real officials, sources, or actual people.
- [ ] **C12.01.04** Assign biography, dialogue, portrait-rights, and continuity reviewers; require attributable approval before character revisions enter the publishable content manifest.
- [ ] **C12.01.05** Define retirement behavior for established campaigns, pending encounters, and mandatory threads; preserve appearance history and provide reviewed historical references or replacement branches.
- [ ] **C12.01.06** Load a valid character through introduction, repeat appearance, relationship change, retirement, and historical review; verify consistent revision identity and approved personality constraints.
- [ ] **C12.01.07** Reject duplicate identities, missing biographies, unresolved portraits, impossible whereabouts, unsupported roles, and unapproved real-person representation; prevent partial character-library publication.
- [ ] **C12.01.08** Retain character schemas, biography approvals, dependency validation, retirement walkthroughs, and appearance traces; require every published character to resolve its reviewed identity and content revision.

### Control C12 02

**Original requirement C12.02:** Represent story threads as explicit state graphs containing prerequisites, transitions, dependencies, outcomes, re-entry rules, convergence points, expiration, and recovery branches. Give every transition a stable identifier.

- [ ] **C12.02.01** Define thread graph nodes and stable transition identifiers with prerequisites, effects, dependencies, outcomes, re-entry rules, convergence points, expiration, and authored recovery paths.
- [ ] **C12.02.02** Specify initial, active, dormant, deferred, resolved, and terminal state semantics; distinguish mandatory source-day obligations from optional narrative continuations.
- [ ] **C12.02.03** Express conditions using approved typed facts and deterministic rule revisions; require explicit edges for route divergence, skipped encounters, retired characters, and accepted corrections.
- [ ] **C12.02.04** Bound repeatable transitions and cycles through visit counts or monotonic state changes; prevent reward farming or infinite mandatory progression loops.
- [ ] **C12.02.05** Map thread outcomes to approved dialogue, assets, explanations, and future encounter prerequisites; prohibit graph publication when supported states lack required presentation dependencies.
- [ ] **C12.02.06** Traverse every permitted state transition, including re-entry and convergence, from named fixtures; compare persisted transition sequence with the independently authored graph path.
- [ ] **C12.02.07** Introduce missing edges, impossible prerequisites, unbounded cycles, unsupported terminal states, and expired mandatory threads; require diagnosed blockers before content release.
- [ ] **C12.02.08** Retain graph definitions, reachability reports, transition fixtures, and recovery reviews; require every supported active state to reach resolution, deliberate deferral, or approved dormancy.

### Control C12 03

**Original requirement C12.03:** Establish a campaign fact registry separating immutable historical facts, current character state, player-known information, and scenario assumptions. Tag each fact with its source decision/event and revision.

- [ ] **C12.03.01** Define a fact registry separating immutable historical facts, current character state, player-known information, and supplied scenario assumptions using stable fact identifiers.
- [ ] **C12.03.02** Store source decision or event, content revision, campaign/day, assertion time, effective state, and correction or supersession references for every established fact.
- [ ] **C12.03.03** Specify fact ownership and permitted writers; require approved committed transitions to establish history while presentation and generated prose may only reference existing facts.
- [ ] **C12.03.04** Represent player knowledge separately from world truth; prevent dialogue from disclosing hidden facts as previously learned unless an explicit introduction transition occurs.
- [ ] **C12.03.05** Define contradiction, withdrawal, and correction semantics without deleting established history; preserve historical claims alongside annotated current-state corrections where necessary.
- [ ] **C12.03.06** Commit a sequence that establishes a fact, reveals it, changes current state, and annotates an error; verify distinct registry categories and causal ancestry.
- [ ] **C12.03.07** Attempt duplicate incompatible facts, hidden-information dialogue, fictional assumptions promoted to sourced truth, and prose-originated writes; assert rejection or approved explicit introduction.
- [ ] **C12.03.08** Retain fact dictionaries, ownership rules, conflict fixtures, and registry reconstructions; require every canonical fact to resolve a permitted causal source and revision.

### Control C12 04

**Original requirement C12.04:** Define relationship mechanics and bounded quantities for familiarity, trust, favors, or companionship. Specify initial state, permitted transitions, decay if used, and interpretation so scores do not imply factual psychological assessment.

- [ ] **C12.04.01** Define relationship quantities such as familiarity, trust, favors, and companionship with canonical scales, bounds, categories, initialization, and clearly fictional interpretation.
- [ ] **C12.04.02** Specify allowed transition causes, magnitude limits, dependencies, and any decay rule; exclude launcher count, browser refresh, and elapsed unrecorded wall time as implicit triggers.
- [ ] **C12.04.03** Separate transactional favors and possessions from interpretive relationship scores; document whether obligations persist through character absence, route changes, retirement, or campaign reset.
- [ ] **C12.04.04** Pin relationship rules to campaign content and preserve original transition semantics; require reviewed migration for changed scales, bounds, or interpretation.
- [ ] **C12.04.05** Display scores as fictional mechanics without psychological assessment claims; provide understandable causal descriptions for increases, decreases, obligations, and unchanged values.
- [ ] **C12.04.06** Exercise introductions, repeated encounters, fulfilled and broken promises, approved decay, and retirement; compare values against independently calculated bounded transition sequences.
- [ ] **C12.04.07** Submit out-of-range effects, unauthorized decay, duplicate favors, and retry-based familiarity gains; require rejection or deduplication without corrupting relationship state.
- [ ] **C12.04.08** Retain rule tables, interpretation review, boundary fixtures, and causal summaries; require all relationship values within declared bounds and reconstructible from accepted transitions.

### Control C12 05

**Original requirement C12.05:** Record character/thread transitions in SQLite with campaign/hike-day IDs, dossier generation, input/output revisions, causal decision, event/content revision, operation ID, and reason. Enforce causal references and unique effects; support reconstruction from committed repository history.

- [ ] **C12.05.01** Define SQLite transition records with campaign/day, dossier generation, input/output revisions, character/thread identities, causal decision, event/content revision, operation identity, and reason.
- [ ] **C12.05.02** Enforce ownership and foreign keys across source decision, character revision, thread transition, dossier, campaign, and resulting facts; reject cross-campaign causal references.
- [ ] **C12.05.03** Persist previous and resulting states or sufficient typed deltas for deterministic reconstruction; retain stable transition identifiers independent of translated dialogue text.
- [ ] **C12.05.04** Apply unique originating-operation/effect constraints to introductions, relationship changes, possessions, promises, and thread advancement; preserve receipt identity across retries and restoration.
- [ ] **C12.05.05** Separate authoritative transitions from presentation history and optional generated summaries; prohibit a viewed dialogue page from establishing a canonical state change.
- [ ] **C12.05.06** Execute representative multi-character threads, restart, and reconstruct state from committed transition history; compare facts, relationships, whereabouts, and active nodes exactly.
- [ ] **C12.05.07** Attempt orphaned causes, unsupported transitions, stale input revisions, duplicate effects, and mismatched dossier identities; require rollback without partial narrative facts.
- [ ] **C12.05.08** Retain schema verification, reconstruction results, causal-link reports, and retry evidence; require every canonical character or thread change to resolve one accepted originating operation.

### Control C12 06

**Original requirement C12.06:** Publish supported combinations of story flags and character appearances. Document mutually exclusive facts, required introductions, branch convergence, and content dependencies for each combination.

- [ ] **C12.06.01** Enumerate supported combinations of story flags, introductions, character appearances, possessions, promises, and relationships; identify unsupported combinations explicitly in the content compatibility matrix.
- [ ] **C12.06.02** Define mutually exclusive facts and required introductions using stable registry identifiers; distinguish missing knowledge from impossible world-state combinations.
- [ ] **C12.06.03** Map each supported combination to dialogue variations, assets, explanations, branch successors, and convergence points under the pinned content manifest.
- [ ] **C12.06.04** Validate combination constraints before scheduling and committing transitions; prohibit individually valid encounters from collectively establishing incompatible facts in one generation.
- [ ] **C12.06.05** Specify fallback for unsupported combinations caused by migration or correction; require approved annotation or recovery rather than improvising an unreviewed state.
- [ ] **C12.06.06** Exercise every supported combination category through scheduling and dialogue rendering; confirm available content and successors satisfy the matrix without unexplained generic substitutions.
- [ ] **C12.06.07** Inject exclusive flags, absent introductions, retired dependencies, and concurrent appearances; require diagnosed exclusion or explicit reviewed recovery with preserved history.
- [ ] **C12.06.08** Retain compatibility matrices, combination coverage, exclusion traces, and fallback approvals; accept no supported combination without complete presentation and reachable continuation dependencies.

### Control C12 07

**Original requirement C12.07:** Validate whereabouts, introductions, possessions, promises, relationships, and completed events before scheduling a character appearance. Reject dialogue that requires information the player has not received unless the narrative deliberately introduces it.

- [ ] **C12.07.01** Enumerate appearance prerequisites for whereabouts, introductions, possessions, promises, relationship state, completed events, and player knowledge; resolve them against authoritative registry revisions.
- [ ] **C12.07.02** Define route-position and fictional-time plausibility rules for character travel; record approved coincidence or relocation assumptions rather than hiding geography contradictions.
- [ ] **C12.07.03** Validate dialogue claims against known and current facts before scheduling; require explicit narrative introduction when new information is intentionally disclosed.
- [ ] **C12.07.04** Revalidate consequential appearance constraints at resolution after intervening choices, corrections, or migrations; return a stale-appearance result without establishing conflicting facts.
- [ ] **C12.07.05** Provide approved pending, relocation, or alternate-dialogue behavior when a character becomes unavailable; preserve source obligations and original generation references.
- [ ] **C12.07.06** Schedule valid introduced characters with known possessions and promises; verify rendered dialogue and committed consequences satisfy every recorded appearance prerequisite.
- [ ] **C12.07.07** Attempt impossible travel, absent introductions, consumed possessions, broken promises, hidden facts, and concurrent state changes; require exclusion or explicit stale handling.
- [ ] **C12.07.08** Retain appearance snapshots, dialogue claim inventories, prerequisite tests, and continuity review; require every character appearance to be plausible under its pinned campaign context.

### Control C12 08

**Original requirement C12.08:** Apply character transitions in the same SQLite transaction as their C08 choice and C10 effects. Prevent a journal claim or relationship reward from appearing before the authoritative transition commits, including during database contention and server termination.

- [ ] **C12.08.01** Enumerate character facts, relationship effects, thread transitions, resource changes, decision records, journal references, receipts, and resulting revisions within the shared choice transaction.
- [ ] **C12.08.02** Revalidate narrative prerequisites and resource bounds inside the SQLite write transaction; reject a choice when any required character transition cannot legally commit.
- [ ] **C12.08.03** Commit all linked changes together before revealing relationship rewards, journal claims, possession updates, or next-thread availability to the browser.
- [ ] **C12.08.04** Record postcommit rendering jobs durably and publish artifacts separately; do not treat filesystem output as part of SQLite transaction atomicity.
- [ ] **C12.08.05** Define bounded contention and uncertain-acknowledgment behavior preserving operation identity; expose existing receipts rather than applying character effects again after a timeout.
- [ ] **C12.08.06** Choose a branch combining cost, promise, relationship change, thread advance, and journal reference; verify one causal operation and consistent committed revision.
- [ ] **C12.08.07** Terminate after each tentative mutation and after commit before response, including database-busy conditions; require all database effects or none and recoverable presentation.
- [ ] **C12.08.08** Retain fault traces, narrative/resource reconciliation, journal visibility checks, and receipt recovery; accept no reward or historical claim displayed as committed before authoritative transition commit.

### Control C12 09

**Original requirement C12.09:** Deduplicate transitions and relationship effects by originating operation persisted in SQLite. Replaying encounters, refreshing dialogue, repeated launches, or loopback request retries must not farm familiarity, rewards, introductions, or favors.

- [ ] **C12.09.01** Define originating operation/effect keys for introductions, familiarity, favors, rewards, possessions, and thread advancement; document distinct deliberate encounters versus redisplay of the same encounter.
- [ ] **C12.09.02** Enforce unique keys in SQLite and persist outcome receipts; reject same-key changed payloads without replacing existing narrative transitions or relationship values.
- [ ] **C12.09.03** Treat dialogue replay, refreshed portraits, browser navigation, repeated launch, and repeated HTTP requests as presentation or retry operations with no new consequential effects.
- [ ] **C12.09.04** Retain deduplication evidence across service restart, campaign export/import where supported, and repository restore; preserve original operation ancestry for historical encounters.
- [ ] **C12.09.05** Provide lookup for uncertain accepted transitions so clients resolve acknowledgment before submitting another operation; distinguish pending selection from committed relationship progress.
- [ ] **C12.09.06** Replay dialogue and retry the same encounter through multiple tabs and restarted service; verify one introduction, reward, favor, and relationship delta.
- [ ] **C12.09.07** Race identical and conflicting keys, restore a backup, and repeat launcher runs; require stable receipts and no farming through restored presentation state.
- [ ] **C12.09.08** Retain transition counts, receipt fingerprints, replay traces, and restored-state comparisons; require exactly the declared effects per accepted originating narrative operation.

### Control C12 10

**Original requirement C12.10:** Define continuity under explicit itinerary divergence: skipped towns, alternate routes, reversed direction, accelerated/repeated stages, and absence. A service restart resumes the active day's established story; next-stage relocation requires a committed completion or other audited position transition.

- [ ] **C12.10.01** Define continuity policies for skipped towns, alternate routes, reversed direction, accelerated or repeated stages, and prolonged absence under each supported itinerary mode.
- [ ] **C12.10.02** Map character travel, deferred promises, pending introductions, and thread availability to explicit route positions and fictional chronology; preserve established historical facts through divergence.
- [ ] **C12.10.03** Require approved relocation or dormancy transitions with reason, expected revision, original encounter identity, and source-day obligation when route changes displace narrative content.
- [ ] **C12.10.04** Resume established active-day story and dossier on restart; prohibit recalculating whereabouts from launch date, current catalog defaults, or client-selected route positions.
- [ ] **C12.10.05** Allow next-stage relocation only after committed completion or another audited position transition; prevent carryover resolution from advancing next-leg or fabricating activity credit.
- [ ] **C12.10.06** Traverse divergence fixtures in both directions, including repeated and accelerated stages; verify plausible appearances, retained promises, and reachable authored continuation.
- [ ] **C12.10.07** Restart during unfinished dialogue, skip a required location, and return after absence; require original day continuity or an explicit approved recovery transition.
- [ ] **C12.10.08** Retain divergence policy, relocation audit, before/after fact registries, and walkthroughs; require no unexplained character teleportation, history rewrite, or launch-originated narrative advancement.

### Control C12 11

**Original requirement C12.11:** Bound branch proliferation through explicit convergence points and approved variation sets. Block publication when a supported branch lacks dialogue, assets, explanation, or a reachable successor.

- [ ] **C12.11.01** Define approved branch variation sets, convergence nodes, maximum independent branch factors, and coverage expectations for every supported story thread and campaign mode.
- [ ] **C12.11.02** List required dialogue, portrait or alternative, explanation, prerequisite facts, and successor references for each variation; validate dependencies against the pinned content manifest.
- [ ] **C12.11.03** Design convergence without erasing material choices or promises; retain causal history while defining which future state differences intentionally persist after branches rejoin.
- [ ] **C12.11.04** Bound repeat and re-entry paths to prevent unlimited variant multiplication; require stable transition identities and explicit ownership for newly introduced branch combinations.
- [ ] **C12.11.05** Block publication when supported branches lack complete presentation or reachable successors; treat intentionally unsupported variants as scope exclusions with approved rationale.
- [ ] **C12.11.06** Traverse each variation to its convergence point and onward; verify preserved meaningful facts and complete dialogue coverage for the converged state combinations.
- [ ] **C12.11.07** Delete branch assets, successor edges, and explanations or add an unsupported flag combination; require precise validation failure before the release manifest is published.
- [ ] **C12.11.08** Retain branch inventories, convergence reports, dependency checks, and reviewer approval; require complete reachable content for every supported variation in the selected release.

### Control C12 12

**Original requirement C12.12:** Provide authored resolution or deliberate, source-day-scoped deferral for mandatory threads and recognizable dormancy for optional threads. Missing characters must have an approved recovery branch; automatic narrative closure or later carryover resolution cannot complete a hike day, move `nextleg`, or supply actual activity credit.

- [ ] **C12.12.01** Classify mandatory and optional threads and define their resolution, source-day-scoped deferral, recognizable dormancy, retirement, and approved recovery state transitions.
- [ ] **C12.12.02** Model mandatory source gates and deliberate acknowledgments separately from optional narrative closure; preserve original day, requirement, and carryover identities throughout continuation.
- [ ] **C12.12.03** Author recovery for missing characters and displaced locations using compatible dialogue, relocation, or alternate resolution; prevent an unavailable character from stranding preparation participation.
- [ ] **C12.12.04** Prohibit automatic closure, later carryover resolution, or dormancy from completing a hike day, moving next-leg, or creating real activity or progression evidence.
- [ ] **C12.12.05** Show clear unresolved, deferred, dormant, and resolved statuses with accessible return actions; preserve workout logging and session controls independently of thread availability.
- [ ] **C12.12.06** Resolve and defer representative mandatory threads, then revisit optional dormant threads; verify correct original obligations, authored continuation, and unchanged destination-day completion.
- [ ] **C12.12.07** Retire characters, interrupt acknowledgments, and relaunch an unfinished day; require retained thread identity, recoverable pending state, and no implicit completion.
- [ ] **C12.12.08** Retain lifecycle traces, source-gate receipts, recovery walkthroughs, and position comparisons; require every supported thread state to have an explicit truthful disposition.

### Control C12 13

**Original requirement C12.13:** Preserve committed story facts and the generated dossier snapshot across content updates. Publish corrected story generations with version/supersession metadata and an approved migration or annotation; do not rewrite active-day dialogue or established choices during automatic startup regeneration.

- [ ] **C12.13.01** Pin committed story facts, dialogue, character revision, event choice, and dossier generation/hash to immutable historical records independent of current content library versions.
- [ ] **C12.13.02** Create corrected story generations as new snapshots with version, reason, input manifest, supersession link, and publication state; retain the original presentation reference.
- [ ] **C12.13.03** Define annotation and migration authority, preview, expected revisions, affected threads, and compensation rules; preserve established decisions when correcting erroneous story implications.
- [ ] **C12.13.04** Prevent automatic startup regeneration from replacing active-day dialogue, introductions, random outcomes, or prior choices merely because updated files exist.
- [ ] **C12.13.05** Handle withdrawn portraits or dialogue rights through approved historical placeholders or replacements; retain honest revision metadata and known facts without displaying prohibited assets.
- [ ] **C12.13.06** Update characters and story definitions while campaigns are unfinished and completed; verify original facts and dialogue remain reproducible until approved correction operations.
- [ ] **C12.13.07** Interrupt correction publication and submit stale migrations; require recoverable new snapshots, intact old references, and no partial authoritative narrative rewrite.
- [ ] **C12.13.08** Retain supersession chains, original/corrected snapshots, approvals, and restart evidence; require attributable versioned correction for every changed established story presentation.

### Control C12 14

**Original requirement C12.14:** Require editorial review for respectful portrayal, consistent characterization, appropriate humor, and clearly fictional identity. Do not present invented characters as actual trail officials, sources, or people without verified authorization and accurate attribution.

- [ ] **C12.14.01** Assign editorial reviewers for respectful portrayal, characterization, humor, geographic context, fictional identity, and any representation requiring authorization or accurate real-person attribution.
- [ ] **C12.14.02** Define biography and dialogue style constraints with examples of appropriate and prohibited portrayals; ensure characters retain consistent motives, language, and relationship boundaries.
- [ ] **C12.14.03** Label invented characters and institutions where confusion with actual trail officials, emergency services, sources, or people could influence user understanding.
- [ ] **C12.14.04** Record authorization and attribution for approved real-person references; prohibit invented statements, endorsements, or official advice attributed to an actual individual or organization.
- [ ] **C12.14.05** Provide review and withdrawal procedures for harmful or misleading portrayal; preserve campaign continuity through approved replacement dialogue rather than erasing user decisions.
- [ ] **C12.14.06** Review representative introductions, setbacks, recovery, conflict, and humor across all supported branches; document inconsistencies and required wording changes before publication.
- [ ] **C12.14.07** Playtest ambiguous authority claims, stereotype risks, coercive dialogue, and retired real-person permissions; require corrected content or removal from the release scope.
- [ ] **C12.14.08** Retain editorial annotations, authorization evidence, branch coverage, and approvals; accept no unreviewed misleading official identity or unresolved material portrayal defect.

### Control C12 15

**Original requirement C12.15:** Review educational dialogue against approved sources and fictional scenario assumptions. A character's narrative confidence must not substitute for evidence or create unsupported real training prescriptions.

- [ ] **C12.15.01** Inventory factual educational claims, trail assertions, equipment explanations, and training references in character dialogue; associate each claim with approved evidence or explicit scenario assumptions.
- [ ] **C12.15.02** Separate fictional confidence and opinion from source-backed instruction; require visible context when a character discusses hypothetical availability, weather, or resource planning.
- [ ] **C12.15.03** Pin educational source revisions and reviewer status to dialogue releases; flag stale, withdrawn, disputed, or geographically inapplicable claims before publication.
- [ ] **C12.15.04** Reject unsupported personalized duration, incline, load, distance, recovery, or equipment prescriptions introduced by dialogue or generated narrative; retain assignment authority outside character systems.
- [ ] **C12.15.05** Provide authored uncertainty and missing-source fallback that remains useful without pretending a fictional character supplies professional, current, or firsthand evidence.
- [ ] **C12.15.06** Inspect every educational dialogue branch against its cited source and scenario inputs; compare claims, limitations, classifications, and factual scope with approved evidence.
- [ ] **C12.15.07** Inject overconfident unsupported advice, absent sources, fictional facts labeled real, and generated prescriptions; require validation rejection or reviewed wording correction.
- [ ] **C12.15.08** Retain claim/source matrices, instructional review, rejected examples, and training-state comparisons; require supported educational claims and zero narrative-originated physical-training prescriptions.

### Control C12 16

**Original requirement C12.16:** If generated dialogue is enabled, constrain inputs to approved character facts and current story state; validate outputs and provide authored fallback. Generated prose cannot directly set campaign facts, spend resources, alter workouts, or command equipment.

- [ ] **C12.16.01** Define approved generation inputs comprising pinned character biographies, known facts, current thread state, scenario assumptions, tone constraints, and permitted source-supported educational material.
- [ ] **C12.16.02** Exclude unnecessary reflections, biometric data, secrets, filesystem paths, and external credentials from prompts; record the enabled generator and privacy handling for retained inputs.
- [ ] **C12.16.03** Validate generated dialogue for contradictions, unauthorized claims, missing classifications, inappropriate portrayal, and unsupported instructions before presenting it as approved narrative content.
- [ ] **C12.16.04** Provide locally authored fallback for timeout, malformed output, unavailable generation service, or failed grounding; preserve established choices and accessible story continuation.
- [ ] **C12.16.05** Treat generated output strictly as prose with no mutation capability; never parse it into facts, spending, workout changes, device commands, or authoritative transition instructions.
- [ ] **C12.16.06** Generate dialogue from known fixtures and compare each claim with approved facts and sources; verify unsupported additions are rejected and fallback remains contextually consistent.
- [ ] **C12.16.07** Submit adversarial prompt text, invented state updates, malicious tool instructions, and contradicted character histories; assert no authoritative state mutation or prohibited capability access.
- [ ] **C12.16.08** Retain input manifests, output validation, grounding review, fallback traces, and state hashes; require all displayed generation to pass review and leave protected records unchanged.

### Control C12 17

**Original requirement C12.17:** Provide portrait alternative text, transcripts, adjustable presentation, and replay/review of dialogue. Do not require audio, rapid reading, timed responses, or interaction while the user is walking to preserve story access.

- [ ] **C12.17.01** Specify portrait alternative text, complete dialogue transcripts, speaker identity, relationship context, adjustable text presentation, and accessible replay controls for every conversation pattern.
- [ ] **C12.17.02** Provide equivalent text for audio and visual-only story information; prohibit essential facts or choices from depending on sound, animation, or portrait interpretation alone.
- [ ] **C12.17.03** Support keyboard navigation, named choices, visible focus, screen-reader announcements, enlarged text, and reduced motion without losing dialogue chronology or selected-state information.
- [ ] **C12.17.04** Permit untimed reading and replay after deferral, walking mode, session termination, and service restart; preserve original transcript revisions and encounter return points.
- [ ] **C12.17.05** Handle missing audio, portraits, transcripts, or acknowledgment through honest accessible fallback; retain the narrative queue and avoid treating absent interaction as completed content.
- [ ] **C12.17.06** Complete introduction, choice, deferral, replay, and history review using keyboard and assistive technology; verify all essential facts and options remain perceivable and operable.
- [ ] **C12.17.07** Disable audio, enlarge text, enable reduced motion, and resume an interrupted conversation; require no timed response, rapid reading, or walking interaction obligation.
- [ ] **C12.17.08** Retain accessibility task evidence, transcript coverage, alternative-text review, and interruption results; require equivalent story access across supported presentation preferences and modalities.

### Control C12 18

**Original requirement C12.18:** Validate graph reachability, terminal states, missing assets, contradictory facts, branch convergence, mutual exclusions, and required introductions before publication. Identify intentionally unreachable states separately from defects.

- [ ] **C12.18.01** Build graph validation covering reachable nodes, terminal states, convergence, missing assets, contradictory facts, exclusions, required introductions, and supported re-entry or recovery paths.
- [ ] **C12.18.02** Define the permitted initial-state space and intentionally unreachable nodes explicitly; identify rationale, owner, and release scope instead of counting them as successful coverage.
- [ ] **C12.18.03** Check every transition's typed prerequisites and effects against fact definitions, relationship bounds, whereabouts rules, and compatible character/content revisions.
- [ ] **C12.18.04** Verify each supported node resolves required dialogue, portraits or approved alternatives, explanations, and successors; block incomplete mandatory paths before publication.
- [ ] **C12.18.05** Analyze cycles for bounded progress and reward duplication; prove mandatory paths can resolve or deliberately defer without entering an endless narrative loop.
- [ ] **C12.18.06** Run valid graph fixtures containing branch convergence, mutual exclusions, introductions, and recovery; compare analyzer findings with independent expected reachability and dependencies.
- [ ] **C12.18.07** Seed impossible facts, missing assets, dead terminals, incompatible introductions, and unbounded cycles; require precise blocking findings rather than silent graph pruning.
- [ ] **C12.18.08** Retain graph reports, seeded-defect detection, scope exclusions, and reviewer decisions; accept zero unresolved blocking continuity or reachability defects in supported branches.

### Control C12 19

**Original requirement C12.19:** Run continuity fixtures for missed locations, concurrent tabs/events, duplicate delivery, repeated launches, unfinished-day resume, forced process termination, repeat stages, absence, content retirement, migration, and correction. Verify replay from SQLite reproduces all character/thread states.

- [ ] **C12.19.01** Prepare continuity fixtures for missed locations, concurrent events, duplicate delivery, repeated launches, unfinished-day resume, process termination, repeated stages, absence, retirement, migration, and correction.
- [ ] **C12.19.02** Pin initial facts, thread nodes, relationships, whereabouts, route position, source-day obligations, dossier hashes, and expected operation receipts for each named scenario.
- [ ] **C12.19.03** Exercise route divergence and absence before scheduling the next appearance; verify approved relocation or dormancy with preserved promises, knowledge, and historical facts.
- [ ] **C12.19.04** Race incompatible events and repeat accepted operations across tabs and restart; assert explicit conflicts, one transition per effect, and no relationship farming.
- [ ] **C12.19.05** Terminate around shared decision/resource/story commits and recover; require complete or unapplied effects with no premature journal claims or orphaned causal references.
- [ ] **C12.19.06** Apply character retirement, corrected dialogue, and approved migration; compare original snapshots with versioned replacements and preserve established choices and source-gate identities.
- [ ] **C12.19.07** Reconstruct every final character and thread state solely from committed SQLite history; compare it with live projections and independently specified fixture expectations.
- [ ] **C12.19.08** Retain scenario traces, reconstruction reports, conflict results, and defects; require exact replay agreement and zero launch-originated story progression or unsupported continuity changes.

### Control C12 20

**Original requirement C12.20:** Approve narrative walkthroughs for representative complete campaigns. If generation is enabled, include adversarial and contradiction tests, grounding review, failure fallback, and confirmation that unvalidated text cannot change authoritative state.

- [ ] **C12.20.01** Select complete walkthrough campaigns covering both directions, major regions, enabled modes, divergent choices, recovery states, mandatory carryovers, and optional thread dormancy.
- [ ] **C12.20.02** Record pinned manifests, initial narrative facts, chosen strategy, encounter sequence, expected convergence, and reviewer identities before executing each approved walkthrough.
- [ ] **C12.20.03** Review characterization, geographic plausibility, known information, promises, possessions, branch closure, and educational claims throughout the full story rather than isolated dialogue samples.
- [ ] **C12.20.04** When generation is enabled, include contradictory inputs, adversarial instructions, unavailable services, malformed output, and unsupported factual claims; verify grounding rejection and authored fallback.
- [ ] **C12.20.05** Compare canonical fact, resource, workout, and equipment state before and after generated prose delivery; require no changes unless a separate validated user operation commits.
- [ ] **C12.20.06** Verify every supported ending and recovery route remains reachable with planned recovery or partial activity; resolve stranded mandatory threads and coercive exercise incentives.
- [ ] **C12.20.07** Record accessibility and comprehension findings for reading, deferral, replay, and causal explanations; correct material issues before approving affected narrative content.
- [ ] **C12.20.08** Archive complete walkthroughs, generation validation, state comparisons, defects, and attributable acceptance; require approved campaigns to preserve continuity and all authoritative-state boundaries.

## C13 Camp journal and collection

**Accountable owner:** User Data Product Lead. **Reviewing roles:** Data Engineering Lead, Narrative Editor, Media Rights Reviewer, Privacy Reviewer, Accessibility Lead, and QA Lead.

**Interfaces:** Reads repository SQLite actual-session, hike-day, launch/run, progression, C08/C10/C12 records, persisted dossier snapshots, and credited local media. Writes reflections/collections through the loopback service. Browser drafts are explicitly pending until acknowledged by SQLite; exports use committed records and permitted assets without requiring a cloud account.

**Required evidence:** Journal/collection/launch/day schemas and SQLite constraints; snapshot provenance specification; acknowledged-save/conflict policy; correction dependency map; local privacy/retention specification; rights-aware export samples; restart/internet-independent recovery results; accessibility review; grounding results where enabled.

**Exit criterion:** SQLite-acknowledged reflections and collections survive interruption, tab conflict, and restart without silent loss or duplication. Launch records never imply completed days; pending browser drafts never imply committed saves. Exports remain intelligible, attributed, privacy controlled, and clear about actual versus fictional outcomes.

### Control C13 01

**Original requirement C13.01:** Publish SQLite journal schemas with stable entry ID, campaign/hike-day IDs, dossier generation ID/hash, real-session references, route/content versions, timestamps, source type, locale, revision, and deletion state. Model launch/run records separately from completed days and actual workouts; a launch log alone cannot create a completion debrief.

- [ ] **C13.01.01** Define journal columns for stable entry identity, campaign/day, dossier generation/hash, session references, route/content versions, timestamps, source type, locale, revision, and deletion state.
- [ ] **C13.01.02** Separate Run records, actual WorkoutSessions, draft reflections, partial-stage notes, and completed-day debriefs; document the distinct causal requirement for each entry type.
- [ ] **C13.01.03** Enforce foreign keys and ownership agreement across journal, campaign, day, dossier, sessions, decisions, and committed DayCompletion where a completion debrief is claimed.
- [ ] **C13.01.04** Specify timestamp precision, real timezone, fictional-day identity, revision ancestry, and tombstone behavior; preserve unknown times without substituting launch timestamps for actual activity.
- [ ] **C13.01.05** Reject creation of completion debriefs from page display, launch logs, deferred carryover resolution, or uncommitted completion requests; require a durable qualifying DayCompletion reference.
- [ ] **C13.01.06** Create each valid entry type and retrieve it after service restart; verify stable identities, accurate source classification, and original dossier generation references.
- [ ] **C13.01.07** Attempt orphaned sessions, cross-campaign entries, invalid locales, duplicate debrief causes, and launch-only completion notes; require structured rejection without fabricated historical records.
- [ ] **C13.01.08** Retain schema inspection, causal fixtures, foreign-key results, and restart evidence; require every canonical entry to have valid provenance and every completion debrief committed completion authority.

### Control C13 02

**Original requirement C13.02:** Separate actual workout results, fictional expedition outcomes, educational observations, and personal reflections in the data model and presentation. Define real calendar dates and fictional expedition days independently.

- [ ] **C13.02.01** Define separate journal fields and sections for actual workout results, fictional expedition outcomes, educational observations, and personal reflections with explicit source classifications.
- [ ] **C13.02.02** Store real calendar date and timezone independently from fictional expedition day, route stage, scenario clock, and campaign chronology; prohibit conflated date identities.
- [ ] **C13.02.03** Specify summary aggregation by domain so virtual distance, resource changes, and story milestones cannot enter actual activity totals or measured incline exposure.
- [ ] **C13.02.04** Preserve domain labels through collection captions, search snippets, charts, human-readable exports, and structured exports; require downstream consumers to retain classifications.
- [ ] **C13.02.05** Represent missing measurements as unknown or omitted with context; prevent story prose or launch history from filling absent actual session values.
- [ ] **C13.02.06** Complete a real session, hypothetical lesson, fictional encounter, and reflection on one day; inspect each journal section for correct quantities, dates, and meaning.
- [ ] **C13.02.07** Test knowledge-only, skipped-stage, accelerated, repeated, and overnight sessions; verify labels distinguish accomplishments and do not imply unrecorded physical trail presence.
- [ ] **C13.02.08** Retain data mappings, presentation examples, export checks, and aggregation reconciliation; accept zero cross-domain measurements or misleading real-versus-fictional date representations.

### Control C13 03

**Original requirement C13.03:** Reference authoritative SQLite sessions, decisions, resource transactions, milestones, and persisted generated-dossier snapshots by stable IDs. Retain generation version, source-input manifest, and presentation hash so later updates or service restarts preserve what the user originally saw.

- [ ] **C13.03.01** Define stable journal references to authoritative sessions, decisions, resource transactions, milestones, and immutable generated-dossier snapshots; prohibit display names or filenames as primary causal identity.
- [ ] **C13.03.02** Retain dossier generation version, source-input manifest, presentation hash, route/content revisions, and original viewed snapshot reference with each derived journal entry.
- [ ] **C13.03.03** Enforce cross-record ownership and revision compatibility; verify journal causes belong to the referenced campaign/day or explicitly documented cross-day carryover relationship.
- [ ] **C13.03.04** Define historical fallback for retired, withdrawn, or unavailable assets while preserving original presentation metadata and rights-aware replacement or omission records.
- [ ] **C13.03.05** Resolve journal history from SQLite and pinned snapshots after service restart, cache clearing, and current-content update; avoid regeneration that changes what the user originally saw.
- [ ] **C13.03.06** Create a linked entry, update live content, restart, and inspect its original dossier and decisions; compare hashes and source manifests with the creation-time evidence.
- [ ] **C13.03.07** Break references, remove artifacts, alter hashes, and restore an older snapshot; require diagnosed fallback or integrity failure rather than silently attaching current content.
- [ ] **C13.03.08** Retain reference-resolution reports, snapshot comparisons, fallback approvals, and recovery traces; require canonical causes to resolve or carry a documented historical disposition.

### Control C13 04

**Original requirement C13.04:** Define collectible identity, eligibility, unlock operation, encounter location, campaign context, status, and asset revision. Distinguish seeing content, unlocking an item, viewing it later, and physically visiting a location.

- [ ] **C13.04.01** Define collectible identity, asset revision, eligibility, unlock cause, encounter location, campaign context, lifecycle status, and correction or revocation rules in explicit schemas.
- [ ] **C13.04.02** Separate presented content, unlocked collection item, later review, virtual route encounter, and actual physical visit into distinct records and display meanings.
- [ ] **C13.04.03** Require qualifying committed decisions, lessons, or milestones for unlock operations; prevent viewing an image or relaunching a dossier from creating earned accomplishments.
- [ ] **C13.04.04** Pin collectible rules and location classification to the source encounter and route revision; retain illustrative or distant-view context where an asset does not depict an on-route visit.
- [ ] **C13.04.05** Define retired-asset placeholders, rights restrictions, pending unlock acknowledgment, and supported migration behavior without erasing established original unlock provenance.
- [ ] **C13.04.06** Unlock through each approved cause, review repeatedly, and restart; verify one item, stable eligibility evidence, and accurate virtual-versus-physical labels.
- [ ] **C13.04.07** Attempt direct asset-view unlocks, cross-campaign causes, stale eligibility, duplicate operations, and fabricated visit claims; require rejection without collection inflation.
- [ ] **C13.04.08** Retain collectible schemas, causal receipts, classification reviews, and count reconciliation; require every unlocked item to resolve a qualifying committed source and truthful accomplishment type.

### Control C13 05

**Original requirement C13.05:** Preserve media credit, license, redistribution conditions, geographic relevance, capture context, caption, and alternative text. Require missing-rights behavior for export, sharing, and later asset retirement.

- [ ] **C13.05.01** Store media attribution, license, redistribution conditions, geographic relevance, capture context, caption, alternative text, rights validity, and asset revision with journal media references.
- [ ] **C13.05.02** Distinguish rights for local viewing, export, redistribution, public sharing, and derivatives; require explicit permission evaluation for each enabled output channel.
- [ ] **C13.05.03** Preserve captions and location-confidence labels with historical media so later gallery or collection presentation cannot imply a different place or physical visit.
- [ ] **C13.05.04** Define missing, expired, withdrawn, and uncertain-rights behavior using omission, approved replacement, or text-only reference; disclose changes without silently dropping credits.
- [ ] **C13.05.05** Check rights at export or sharing time against current permission status while preserving the historical attribution record and original asset identity.
- [ ] **C13.05.06** Export and locally review media with differing permission grants; verify allowed assets, required credits, accurate captions, and preserved alternative text.
- [ ] **C13.05.07** Retire an asset, remove its rights metadata, and request prohibited redistribution; require honest omission or labeled substitution without copying restricted media.
- [ ] **C13.05.08** Retain rights decisions, export manifests, caption inspections, and retirement traces; accept zero restricted-media redistribution and complete attribution for every included asset.

### Control C13 06

**Original requirement C13.06:** Classify user-authored, template-authored, and generated passages. Preserve the inputs and source references supporting automated summaries; prevent generated narrative from inventing workout measurements, completed choices, or physical visits.

- [ ] **C13.06.01** Classify passages as user-authored, approved template-authored, or generated; retain authorship, template or generator revision, creation time, and applicable source references.
- [ ] **C13.06.02** Define automated-summary inputs as accepted session quantities, committed choices, ledger effects, milestones, and pinned dossier facts; exclude uncommitted drafts and optimistic browser state.
- [ ] **C13.06.03** Store input fingerprints or references sufficient to reproduce and audit summary grounding without unnecessarily retaining sensitive prompt data or unrelated reflections.
- [ ] **C13.06.04** Prohibit generated measurements, invented completed choices, assumed physical visits, and fabricated exercise from missing data; require explicit unknown or omission behavior.
- [ ] **C13.06.05** Validate summaries against authoritative source records before presentation and provide authored fallback when generation, source resolution, or grounding fails.
- [ ] **C13.06.06** Generate summaries for complete, partial, recovery, skipped, and knowledge-only days; compare every factual clause and quantity with the corresponding accepted sources.
- [ ] **C13.06.07** Supply contradictory prompts, absent measurements, pending decisions, and illustrative photographs; require rejection of unsupported accomplishments and no mutation of underlying history.
- [ ] **C13.06.08** Retain provenance fields, grounding reviews, rejected-output examples, and fallback evidence; require every automated factual claim to resolve committed supporting records.

### Control C13 07

**Original requirement C13.07:** Autosave reflections through the local service with explicit draft/committed states, server acknowledgment, and SQLite revision tracking. A browser-only draft remains visibly pending; recover it after service restart without presenting an uncommitted edit as saved or duplicating entries.

- [ ] **C13.07.01** Define autosave request identity, entry ID, expected revision, draft sequence, debounce behavior, payload limits, and acknowledgment contract for local-service reflection updates.
- [ ] **C13.07.02** Persist committed reflection text and revision ancestry in SQLite; show saved status only after durable acknowledgment identifies the accepted effective revision.
- [ ] **C13.07.03** Keep browser-only drafts visibly pending with local draft identity and base revision; distinguish recoverable client drafts from authoritative committed journal entries.
- [ ] **C13.07.04** Reconcile pending drafts after service restart using operation lookup and current server revision before retrying; prevent duplicate entries or silent replacement of newer text.
- [ ] **C13.07.05** Handle database busy, rejected revisions, and uncertain responses with clear status and retained text; ensure stopping a workout does not discard unsaved reflections.
- [ ] **C13.07.06** Type, wait for acknowledgment, refresh, and reopen the entry after restart; verify exact text, one entry identity, and correct committed revision.
- [ ] **C13.07.07** Interrupt before send, during commit, and after commit before response; require pending or recovered saved status matching SQLite without text loss or duplication.
- [ ] **C13.07.08** Retain autosave timing evidence, receipts, draft recovery traces, and revision comparisons; require every saved indicator to correspond to a durable accepted reflection revision.

### Control C13 08

**Original requirement C13.08:** Make debrief records and collectible unlocks idempotent with SQLite uniqueness constraints and atomic causal writes; day-completion debriefs require a committed `DayCompletion`. Rendered/exported files publish separately under C18.13. Relaunch, retry, unfinished-day resume, or carryover resolution cannot duplicate entries or emit an unearned completed-day debrief.

- [ ] **C13.08.01** Define unique causal keys for day-completion debriefs and collectible unlocks; tie completion debrief eligibility to a committed DayCompletion rather than launch or dossier access.
- [ ] **C13.08.02** Commit canonical debrief references, unlocks, receipts, and causal links atomically in SQLite; maintain distinct records for incomplete-day reflections and later completion summaries.
- [ ] **C13.08.03** Record rendering and export jobs durably while publishing their files through staging, checksum validation, rename, and marker reconciliation outside the database transaction.
- [ ] **C13.08.04** Recover duplicate submissions using existing cause and operation receipts; preserve uniqueness through restart, browser-cache clearing, repository restore, and repeated dossier display.
- [ ] **C13.08.05** Prohibit earlier carryover resolution from generating destination-day debriefs or unlocks unless an independent approved cause qualifies them under the declared rules.
- [ ] **C13.08.06** Complete a day and retry debrief or unlock operations repeatedly; verify one canonical entry per cause and consistent original completion and dossier references.
- [ ] **C13.08.07** Resume unfinished days, relaunch completed days, interrupt publication, and resolve carryovers later; assert no unearned completion debrief or duplicated collection item.
- [ ] **C13.08.08** Retain causal-count reports, interruption traces, publication reconciliation, and eligibility tests; require every completed-day debrief to resolve exactly one committed qualifying completion.

### Control C13 09

**Original requirement C13.09:** Define editing semantics: reflections can be edited directly, while measured activity and consequential decisions use their own correction workflows. Preserve the distinction between changing a note and changing authoritative history.

- [ ] **C13.09.01** Specify direct reflection-edit permissions, revision ancestry, deletion semantics, and audit metadata; separate these from actual-session correction and consequential decision correction interfaces.
- [ ] **C13.09.02** Prevent note editing from changing linked measurements, resource effects, character facts, route position, or historical choices; retain references as immutable contextual provenance.
- [ ] **C13.09.03** Define how user statements disagreeing with recorded history appear as personal text without becoming authoritative corrections or revised activity observations.
- [ ] **C13.09.04** Provide explicit navigation to approved correction workflows where users intend to correct underlying data; explain the different consequences and confirmation context without silently transferring edits.
- [ ] **C13.09.05** Preserve original reflection revisions according to retention policy and mark edited text appropriately; prohibit regenerated summaries from overwriting user-authored passages.
- [ ] **C13.09.06** Edit a reflection describing distance, choice, and resources; verify only journal text revision changes while all linked authoritative values remain unchanged.
- [ ] **C13.09.07** Attempt hidden field updates, injected correction commands, stale note payloads, and generated factual edits; require validation rejection or journal-only persistence.
- [ ] **C13.09.08** Retain permission tests, before/after state comparisons, revision history, and usability findings; require note editing to remain distinct from accepted historical-data correction.

### Control C13 10

**Original requirement C13.10:** Reconcile corrected session or campaign records with dependent summaries. Identify affected entries, refresh derived displays consistently, and preserve original-versus-corrected provenance where historical evidence is retained.

- [ ] **C13.10.01** Identify journal entries and summaries dependent on corrected sessions, progression credits, decisions, resource effects, route positions, and milestones using stable source-revision relationships.
- [ ] **C13.10.02** Define refresh, annotation, preservation, and supersession policies for each derived field; distinguish mutable current projections from immutable historical dossier or summary snapshots.
- [ ] **C13.10.03** Record original-versus-corrected values, source correction identity, affected revision, and visible annotation where historical evidence remains; avoid presenting both as unqualified current measurements.
- [ ] **C13.10.04** Update derived projections consistently with the authoritative correction commit or durable follow-up job; expose pending recalculation rather than stale data labeled current.
- [ ] **C13.10.05** Preserve user reflection text and original consequential choices during recalculation; route any historical effect changes through their separate reviewed compensation or migration workflow.
- [ ] **C13.10.06** Correct distance, session dates, progression policy errors, and resource inputs; inspect every affected entry and reconcile current summaries with accepted corrected records.
- [ ] **C13.10.07** Interrupt recalculation, retire source content, and apply overlapping corrections; require recoverable jobs, complete ancestry, and no duplicate annotations or overwritten reflections.
- [ ] **C13.10.08** Retain dependency reports, original/corrected comparisons, job recovery traces, and summary reconciliation; require all affected entries to have an explicit accurate correction disposition.

### Control C13 11

**Original requirement C13.11:** Label walked, accelerated, repeated, skipped, knowledge-only, and illustrative accomplishments accurately. A photograph, landmark, badge, or story unlock must not imply physical presence or measured training that did not occur.

- [ ] **C13.11.01** Define accomplishment classes for walked, accelerated, repeated, skipped, knowledge-only, and illustrative progress with explicit eligibility and display semantics for each collection or milestone.
- [ ] **C13.11.02** Store accepted actual activity and fictional progression evidence separately; prevent virtual route travel from being labeled measured walking or actual physical presence.
- [ ] **C13.11.03** Specify badge captions, map labels, photograph descriptions, journal prose, and export fields that communicate accomplishment class beside the relevant milestone.
- [ ] **C13.11.04** Represent mixed days with multiple truthful categories rather than a single ambiguous completed label; retain actual quantities and progression policy version supporting each claim.
- [ ] **C13.11.05** Handle corrected or deleted activities through reviewed reclassification or annotation; preserve historical unlock causes while clarifying unsupported current actual-activity claims.
- [ ] **C13.11.06** Complete examples in every enabled progression mode and accomplishment class; inspect interface and exports for precise quantities, source types, and physical-presence wording.
- [ ] **C13.11.07** Use illustrative images, skipped stages, duplicate workouts, and knowledge-only lessons to challenge milestone language; require no fabricated visits, distance, or incline exposure.
- [ ] **C13.11.08** Retain classification rules, presentation reviews, correction examples, and source reconciliation; accept zero accomplishments implying physical activity or presence without qualifying actual evidence.

### Control C13 12

**Original requirement C13.12:** Support retrieval by region, stage, real date, fictional day, lesson, character, landmark, and user-selected tags. Define search-index updates for edits, corrections, migrations, and deletion.

- [ ] **C13.12.01** Define searchable keys for region, stage, real date, fictional day, lesson, character, landmark, and user tags using stable references and documented normalization rules.
- [ ] **C13.12.02** Specify indexed fields, tokenization, locale handling, date interpretation, tag limits, and whether private reflection text participates in search by explicit local preference.
- [ ] **C13.12.03** Update indexes for committed edits, corrections, migrations, tombstones, and rights-aware retirement; link index versions to authoritative journal revisions.
- [ ] **C13.12.04** Distinguish real-date filters from fictional-day filters and route-region identities from displayed names; prevent cross-domain search results from misleading chronological interpretation.
- [ ] **C13.12.05** Rebuild indexes from SQLite after corruption or restore; preserve canonical journal data and report pending index status without losing entry access.
- [ ] **C13.12.06** Retrieve known entries through each filter and combined filters before and after edits; compare result identities and snippets with independently expected sets.
- [ ] **C13.12.07** Delete entries, rename tags, correct session dates, and restore backups; verify index removal, updated results, no stale private snippets, and deterministic rebuild.
- [ ] **C13.12.08** Retain search contracts, expected result sets, update traces, and rebuild reports; require every supported retrieval path to return current permitted entries accurately.

### Control C13 13

**Original requirement C13.13:** Protect local reflections through repository/database access policy and explicit selection for export or sharing. Document file permissions, field inclusion, diagnostic redaction, retention, deletion, and backups. Core journaling must work without remote identity, cloud storage, or account creation.

- [ ] **C13.13.01** Define repository and database access policy, file permissions, owner identity, export-selection rules, journal retention, tombstones, backup inclusion, and supported permanent-deletion boundaries.
- [ ] **C13.13.02** Make reflection inclusion an explicit export or sharing choice; default diagnostic and support data to minimal correlation without private text or sensitive draft content.
- [ ] **C13.13.03** Document where committed reflections, pending drafts, temporary exports, and backups reside; apply consistent protections rather than securing only the primary database file.
- [ ] **C13.13.04** Keep core reading and writing functional through the local service without cloud identity, account creation, remote storage, or external authentication dependency.
- [ ] **C13.13.05** Define deletion handling for indexes, derived summaries, staged files, exports, and retained backups; communicate retained-backup limitations through the declared local privacy policy.
- [ ] **C13.13.06** Create private entries offline and inspect filesystem access, logs, support bundles, and default exports; require absence of unselected reflection content.
- [ ] **C13.13.07** Attempt unauthorized reads, implicit sharing, diagnostic error dumps, and postdeletion searches; verify access restrictions, redaction, and documented removal behavior.
- [ ] **C13.13.08** Retain access policy, permission inspections, export selections, redaction tests, and deletion evidence; require local journaling independence and zero unselected private-reflection disclosure.

### Control C13 14

**Original requirement C13.14:** Provide human-readable and structured exports with units, timestamps, source types, progression rules, correction status, and provenance. Respect media redistribution restrictions and disclose omitted or substituted assets.

- [ ] **C13.14.01** Define human-readable and structured export schemas containing entry identity, units, timestamps, timezone, source types, fictional-day context, progression rules, corrections, and provenance.
- [ ] **C13.14.02** Specify selected fields and reflection inclusion explicitly; retain a manifest describing application/schema/content versions, record counts, omitted data, and export creation identity.
- [ ] **C13.14.03** Evaluate media redistribution rights per asset and output channel; omit prohibited files or use approved labeled substitutes while preserving credit and omission metadata.
- [ ] **C13.14.04** Produce exports from a consistent committed database snapshot; exclude pending browser drafts unless explicitly exported as clearly labeled uncommitted text.
- [ ] **C13.14.05** Publish export files through staging, checksums, verified rename, and recoverable markers; report success only when the expected complete artifact and manifest exist.
- [ ] **C13.14.06** Export representative mixed-domain, corrected, overnight, retired-content, and reflection-selected histories; reconcile readable values and structured records against the authoritative snapshot.
- [ ] **C13.14.07** Interrupt publication, remove licensed assets, and disable reflection inclusion; require complete recovery, honest omissions, and no restricted media or unintended private text.
- [ ] **C13.14.08** Retain export specifications, manifests, record reconciliation, rights decisions, and recovery tests; require accurate domains, dates, provenance, and declared omissions in every delivered export.

### Control C13 15

**Original requirement C13.15:** Resolve multiple-tab edits using server-validated entry IDs, expected SQLite revisions, and revision ancestry. Merge compatible edits or present conflicts; never let cached text silently overwrite newer committed content. Define retry behavior for lock contention and restarted service connections.

- [ ] **C13.15.01** Define edit requests with stable entry identity, expected revision, base ancestry, operation identity, and text payload; reject client-generated timestamps as conflict authority.
- [ ] **C13.15.02** Specify compatible-merge criteria and explicit conflict presentation for overlapping changes; preserve original, server-current, and local-draft text for user review.
- [ ] **C13.15.03** Apply server-side revision comparisons and SQLite concurrency controls before commit; prohibit cached text or last-write-wins writes from silently replacing newer committed reflections.
- [ ] **C13.15.04** Persist revision ancestry and accepted operation receipts; recover lost acknowledgments or restarted connections before resubmitting a draft under another consequential identity.
- [ ] **C13.15.05** Define lock-contention retries and pending statuses separately from semantic conflicts; retain unsaved text and allow safe read access while writes await resolution.
- [ ] **C13.15.06** Edit separate supported text regions from two tabs and exercise the permitted merge; verify one coherent result with both contributions and complete ancestry.
- [ ] **C13.15.07** Race overlapping edits, restart the service, and submit stale cached text; require explicit conflict or rejection with all original text preserved and no silent overwrite.
- [ ] **C13.15.08** Retain revision graphs, concurrent-edit traces, conflict screenshots, and contention results; require every accepted edit to descend from validated ancestry or documented reviewed merge.

### Control C13 16

**Original requirement C13.16:** Support journaling without internet while the local service runs, using repository snapshots/assets. If the service stops, cached content may remain readable and drafts pending, but cannot assert committed saves, completion, or position; reconnect and revalidate against SQLite before writes.

- [ ] **C13.16.01** Define offline-internet operation using the running loopback service, authoritative SQLite, repository snapshots, and locally available assets; distinguish this from service-disconnected browser behavior.
- [ ] **C13.16.02** Allow cached historical reading when the service stops while clearly labeling connection state and any pending draft; prohibit cached acknowledgment of durable saves or completion.
- [ ] **C13.16.03** Preserve pending draft identity, base revision, text, and prior operation key until reconnection; document limits if browser storage is cleared before server acceptance.
- [ ] **C13.16.04** On reconnection, verify application instance, campaign, entry identity, current revision, and operation status before submitting or merging retained drafts.
- [ ] **C13.16.05** Prevent browser cache from asserting campaign position, completed days, unlocks, or accepted workouts while disconnected; reconstruct authoritative state from service responses.
- [ ] **C13.16.06** Disconnect internet and perform read, edit, search, and export through the local service; verify durable records and locally resolved assets after restart.
- [ ] **C13.16.07** Stop the service during editing, refresh cached content, then reconnect after another tab edits; require pending visibility and explicit revision conflict handling without duplicate entries.
- [ ] **C13.16.08** Retain connectivity-state traces, pending-draft recovery, authoritative reconciliation, and offline results; require accurate saved status and unchanged position during service-disconnected presentation.

### Control C13 17

**Original requirement C13.17:** Provide accessible reading, editing, search, collection browsing, and export controls. Include useful text alternatives for visual collections and preserve accessible document structure in human-readable exports.

- [ ] **C13.17.01** Specify accessible structure for journal headings, dates, domain sections, editable labels, validation feedback, search filters, collection items, pagination, and export controls.
- [ ] **C13.17.02** Provide meaningful text alternatives for photographs, badges, maps, and collection thumbnails; preserve accomplishment type, geographic relevance, and fictional-versus-physical context in alternatives.
- [ ] **C13.17.03** Support keyboard navigation, visible focus, screen-reader announcements, enlarged text, reduced motion, and touch where declared without hiding editing or conflict-resolution controls.
- [ ] **C13.17.04** Design accessible pending-save, saved, error, deleted, corrected, and conflicting revision states; ensure assistive users can discover status without color or animation alone.
- [ ] **C13.17.05** Preserve semantic headings, reading order, captions, units, and document language in human-readable exports; evaluate the declared export formats independently from the browser interface.
- [ ] **C13.17.06** Complete reading, editing, searching, collection review, correction annotation, and export with keyboard and screen reader; verify equivalent information and task completion.
- [ ] **C13.17.07** Exercise long reflections, empty results, retired-media placeholders, save failure, and multi-tab conflicts at enlarged text; require operable recovery and retained focus context.
- [ ] **C13.17.08** Retain accessibility task records, alternative-text review, export structure inspection, and resolved defects; require all supported journal tasks to pass the declared assessment target.

### Control C13 18

**Original requirement C13.18:** Verify acknowledged autosave, pending drafts, refresh recovery, repeated launches, unfinished-day resume, duplicate debrief/unlock prevention, multi-tab conflicts, SQLite busy/rollback behavior, forced service termination, and repository restore. Confirm every canonical reference resolves or has a documented historical fallback.

- [ ] **C13.18.01** Prepare fixtures covering acknowledged autosave, pending drafts, refresh, repeated launch, unfinished-day resume, debrief uniqueness, unlock uniqueness, conflicts, database busy, termination, and restore.
- [ ] **C13.18.02** Capture initial entry identities, text revisions, source links, dossier hashes, completion records, operation receipts, collection counts, and campaign position for each journey.
- [ ] **C13.18.03** Save and refresh committed reflections, then interrupt unacknowledged saves before and after commit; verify exact text recovery and saved indicators matching durable receipts.
- [ ] **C13.18.04** Relaunch unfinished and completed days repeatedly; assert no additional debrief, unlock, fabricated activity, or position change without an explicit qualifying operation.
- [ ] **C13.18.05** Race conflicting edits and hold SQLite locks; require bounded retry or explicit conflict with preserved local, original, and current server text.
- [ ] **C13.18.06** Restore the repository and resolve every canonical journal cause and snapshot; require documented historical fallback for withdrawn or unavailable content instead of silent substitution.
- [ ] **C13.18.07** Reconcile entry and collection counts, revision ancestry, foreign keys, and causal links against independent expected records after every recovery scenario.
- [ ] **C13.18.08** Retain fixture evidence, reference reports, duplicate counts, recovery traces, and defects; require complete truthful save recovery with no orphaned entries or unearned debriefs.

### Control C13 19

**Original requirement C13.19:** Test correction propagation, content retirement, migrations, media attribution, rights-restricted export, structured export/import where supported, and deletion/index removal. Inspect exported records for accurate domain labels and dates.

- [ ] **C13.19.01** Create fixtures for session corrections, campaign corrections, content retirement, schema migration, restricted media export, structured import where supported, and journal deletion.
- [ ] **C13.19.02** Pin original journal text, source revisions, media rights, dates, domain labels, index contents, and expected corrected or omitted output for each scenario.
- [ ] **C13.19.03** Apply accepted corrections and inspect dependent summaries; require accurate current quantities, retained original provenance, and untouched user-authored reflections or established decisions.
- [ ] **C13.19.04** Retire media and migrate content or schema through approved operations; verify historical references, explicit substitutions, accessible placeholders, and supersession metadata remain coherent.
- [ ] **C13.19.05** Export records with varied rights and reflection selections; reconcile structured and readable data, units, source types, timestamps, omissions, and attribution against authoritative records.
- [ ] **C13.19.06** Where import is supported, round-trip into an isolated campaign and verify ownership, identities, correction ancestry, and no duplicate unlocks or completion causes.
- [ ] **C13.19.07** Delete selected entries and rebuild the search index; verify permitted tombstones, removed snippets, derived-summary handling, and declared backup-retention behavior.
- [ ] **C13.19.08** Retain before/after reports, export/import reconciliation, rights decisions, index checks, and defects; accept zero misleading domain labels, dates, or restricted asset inclusion.

### Control C13 20

**Original requirement C13.20:** Review generated summaries where enabled for grounding and missing-data behavior; test privacy boundaries and accessible task completion. Confirm that journal edits cannot silently rewrite workout, decision, resource, or character history.

- [ ] **C13.20.01** When summaries are enabled, define approved input sources, grounding criteria, unknown-value behavior, authorship labels, validation authority, and locally authored fallback for generation failure.
- [ ] **C13.20.02** Review complete, partial, recovery, knowledge-only, corrected, and retired-content summaries against accepted sessions, decisions, resources, character facts, and pinned dossier context.
- [ ] **C13.20.03** Test absent or contradictory measurements and pending choices; reject invented workout quantities, fabricated completed branches, assumed physical visits, and unsupported source claims.
- [ ] **C13.20.04** Inject private reflection markers and unnecessary sensitive fields into excluded inputs; inspect prompts, logs, support bundles, and unselected exports for leakage.
- [ ] **C13.20.05** Complete summary review, reflection editing, search, conflict recovery, and export using supported assistive technology; verify truthful saved states and accessible grounding explanations.
- [ ] **C13.20.06** Edit notes containing apparent distance corrections, resource commands, or character declarations; compare protected authoritative record hashes to confirm journal-only mutation.
- [ ] **C13.20.07** Attempt malformed API fields, generated state instructions, and cross-domain correction aliases; require explicit validation rejection while retaining legitimate reflection text.
- [ ] **C13.20.08** Retain grounding matrices, privacy tests, accessible task results, and protected-state comparisons; require factual summary support and zero silent journal-originated history changes.

## C14 Training and preparation dashboard

**Accountable owner:** Training Insights Lead. **Technical owner:** Analytics/Frontend Engineering. **Reviewers:** Activity Data, Accessibility, and Privacy. **Interfaces:** Loopback read API and repository-local SQLite; effective workout/day ledger; versioned plans; preparation evidence; campaign-credit ledger; exports; correction workflows.

**Required evidence:** Metric dictionary; SQLite-based aggregation fixtures and reconciliation reports; launch/start/complete event distinctions; duration/uncertainty examples; stale-view/restart specification; chart/table/export parity; local access/export review; accessibility and interpretation results.

**Exit criterion:** Every displayed training or preparation result is reproducible from permitted effective records, missing data remains visible, fictional progress cannot inflate physical metrics, and users can inspect and correct the underlying evidence.

### Control C14 01

**Original requirement C14.01:** Publish a versioned metric dictionary for every displayed figure: formula, unit, eligible sources, inclusion/exclusion rules, uncertainty treatment, rounding, calculation version, and applicable interpretation. Avoid unsupported readiness or medical-risk scores.

- [ ] **C14.01.01** Inventory every dashboard figure and assign a versioned metric definition containing formula, unit, eligible sources, inclusion rules, uncertainty, rounding, calculation revision, and permitted interpretation for the selected release.
- [ ] **C14.01.02** Define actual, planned, preparation, and fictional quantities separately, rejecting undocumented composite metrics whose source domains or units cannot be independently reconciled with effective workout, task, assignment, or campaign records.
- [ ] **C14.01.03** Specify missing-value behavior and required source coverage, preserving unavailable results rather than treating absent measurements as zero or hiding unsupported estimation assumptions behind an apparently precise aggregate displayed to users.
- [ ] **C14.01.04** Document interval formulas using elapsed partition and overlapping application pause, ensuring no dashboard metric equates active application time with confirmed moving duration without qualifying physical observation evidence from effective source records.
- [ ] **C14.01.05** Publish calculation versions and change history, linking displayed historical results to the definition applicable to their inputs or clearly identifying a deliberate recalculation under a newer reviewed interpretation and source-selection policy.
- [ ] **C14.01.06** Test dictionary coverage by tracing each label, chart axis, card, table, export column, and shared summary to a valid definition with independently specified expected values, source eligibility, and uncertainty handling for representative data.
- [ ] **C14.01.07** Review descriptions for unsupported readiness, medical-risk, fitness prediction, or injury-avoidance claims, replacing them with factual participation or measurement interpretations supported by the recorded evidence and approved preparation outcome definitions for the enabled dashboard release.
- [ ] **C14.01.08** Accept only when every displayed figure has a reviewed definition and source lineage, all estimates disclose limits, and no unsupported composite score is presented as validated preparation, health, or completion guidance for the user.

### Control C14 02

**Original requirement C14.02:** Present actual activity, planned training, preparation tasks, and fictional expedition accomplishments as distinct domains. Use separate labels for actual distance, scaled campaign distance, and completed chapters, including in exports and shared summaries.

- [ ] **C14.02.01** Design distinct dashboard areas or labels for actual activity, planned training, preparation tasks, and fictional expedition accomplishments, preserving their separate meanings in totals, filters, comparisons, and trend views for the selected release.
- [ ] **C14.02.02** Use explicit actual-distance, scaled-campaign-distance, and completed-chapter terminology with units, avoiding generic mileage or progress labels that imply virtual route completion represents additional physical walking distance recorded in the authoritative workout database.
- [ ] **C14.02.03** Identify planned targets as accepted assignment values rather than achieved observations, distinguishing requested equipment settings and scheduled duration from actual measurements or self-reports that qualify as completed activity evidence in current source records.
- [ ] **C14.02.04** Represent preparation participation through category-specific task evidence and dates, avoiding conversion of knowledge, recovery, or equipment completion into fabricated physical distance or validated claims of wilderness competence or overall fitness readiness in dashboard cards.
- [ ] **C14.02.05** Carry domain classifications into exports and shared summaries, retaining descriptive column names and explanations even when views are narrowed to one period or a campaign milestone with no selected physical activity detail included by the user.
- [ ] **C14.02.06** Test mixed walking, recovery, preparation, planned-only, and scaled-progression histories, comparing displayed domain totals with independently expected records and checking unavailable physical measurements remain visibly distinct from earned fictional quantities and upcoming accepted physical targets.
- [ ] **C14.02.07** Review responsive, magnified, chart, and screen-reader renderings to ensure shortened labels and accessible descriptions preserve actual-versus-fictional distinctions rather than hiding qualifiers that materially change interpretation of the displayed period, axis, or total for users navigating alternate presentation modes.
- [ ] **C14.02.08** Accept only when users and reviewers can identify the domain of every figure, and all supported output formats preserve clear separation between measured or reported activity, accepted plans, preparation evidence, and fictional route accomplishments generated by versioned progression rules.

### Control C14 03

**Original requirement C14.03:** Define aggregation periods, week starts, timezone selection, overnight workouts, daylight-saving changes, and date-only tasks. Preserve reproducible historical results and show which calendar governs each report.

- [ ] **C14.03.01** Define report periods, week starts, timezone selection, interval boundaries, and inclusion rules for actual workouts and date-only tasks, recording the governing calendar and reproducible filter representation for each supported dashboard query or export period.
- [ ] **C14.03.02** Specify overnight workout attribution as whole-record or supported interval allocation under an explicit versioned rule, preserving source timestamps and avoiding double counting when adjacent daily or weekly periods overlap the same effective physical activity interval in dashboard views.
- [ ] **C14.03.03** Distinguish date-only task dates from timezone-derived instants, preventing travel or daylight-saving conversion from silently shifting an all-day preparation record into another report date without an approved scheduling correction or a clearly documented alternative display-calendar selection used in that calculation.
- [ ] **C14.03.04** Define daylight-saving handling for repeated and nonexistent local times using recorded source timezone and resolved instant, retaining accurate duration and period membership independent from wall-clock labels that may repeat or skip within the user's local reporting interval across the relevant transition date.
- [ ] **C14.03.05** Persist report timezone, period boundaries, week-start setting, and calculation version where historical reproducibility requires them, distinguishing deliberate retrospective regrouping from an unnoticed preference change that could otherwise alter previously interpreted adherence results or actual totals in archived summaries and exports generated from committed source records.
- [ ] **C14.03.06** Test midnight-spanning workouts, timezone travel, daylight-saving transitions, week boundaries, leap dates, and date-only tasks against independently constructed expected membership and allocations, requiring canonical sum agreement across adjacent periods, selected calendar views, and equivalent exported filter specifications supported by the reporting policy for the release.
- [ ] **C14.03.07** Change timezone and week-start preferences, verifying the interface explains altered grouping while preserving source quantities, historical timestamps, committed expedition-day references, and any previously pinned report interpretation needed for reproducibility rather than presenting regrouping as newly added or removed physical activity recorded by the user.
- [ ] **C14.03.08** Review period contracts, expected ledgers, persisted filters, and explanatory labels; accept only when every report identifies its governing calendar and source dates can reproduce historical totals without duplicate overnight allocation, timezone guesses, or passive fictional chronology changes caused by the selected reporting period or display preferences.

### Control C14 04

**Original requirement C14.04:** Apply canonical duration semantics consistently: elapsed contains moving, stationary, and unknown observations; application pause is an overlapping state. Never add paused time to elapsed or present application-active time as confirmed moving time.

- [ ] **C14.04.01** Adopt the shared canonical duration dictionary in every dashboard calculation, representing elapsed as moving plus stationary plus unknown where evidence supports partitioning and application pause as an independently overlapping state rather than an additional exclusive physical duration class.
- [ ] **C14.04.02** Define supported charts and totals for interval-backed and aggregate-only records, retaining each self-reported duration meaning and leaving unavailable components absent rather than fabricating a complete movement partition from elapsed application time, assignment targets, or unknown periods solely to populate stacked displays or satisfy visual consistency expectations.
- [ ] **C14.04.03** Implement elapsed aggregations from effective source quantities or validated physical interval unions, avoiding repeated addition of pause intervals and preserving independent paused-duration metrics that may overlap moving, stationary, or unknown observations for the same session identity and report period in the selected calculation contract version.
- [ ] **C14.04.04** Label application-active and paused measures as application-state observations, rejecting wording or formula choices that equate active duration with confirmed moving time or automatically subtract all pause from actual movement even when qualifying evidence reports walking during that paused interval in the effective workout observation record retained by the logger.
- [ ] **C14.04.05** Display unknown coverage and aggregate-only limitations in charts, tables, tooltips, and exports, allowing users to distinguish unavailable breakdowns from observed zero movement or stationary time and ensuring uncertainty meaning survives narrowed periods, accessibility alternatives, and display-unit changes applied through supported reporting controls at the dashboard interface.
- [ ] **C14.04.06** Test moving-through-pause, stationary pauses, unknown paused gaps, aggregate-only manual duration, and corrected interval classifications against independent expected partition and overlap totals, requiring elapsed equality and consistent pause semantics across companion, logger, dashboard, and exported summaries using the same committed effective source revisions during verification sessions.
- [ ] **C14.04.07** Apply interval corrections and report-period allocation, verifying no doubled elapsed duration, erased pause observations, or unsupported movement appears after recalculation, stale-cache replacement, service restart, and export generation from the newly accepted effective workout revision rather than provisional browser edits or obsolete pre-correction summaries retained temporarily for display during processing.
- [ ] **C14.04.08** Review formulas, labels, uncertainty displays, and independent arithmetic evidence; accept only when no dashboard or export adds paused time to elapsed, subtracts pause from movement automatically, or presents application activity as proof of physical motion without qualifying source evidence recorded and retained under the shared duration-accounting contract.

### Control C14 05

**Original requirement C14.05:** Represent missing measurements as unavailable rather than zero. Show mixed-source coverage, estimated values, incomplete incline intervals, unknown activity periods, and provisional data in both totals and charts.

- [ ] **C14.05.01** Define unavailable states for absent distance, duration components, incline, and source coverage, preserving null semantics in aggregation, charts, tables, and exports rather than filling missing physical measurements with misleading zeros or planned quantities from accepted assignments to make dashboard totals appear complete in the current selected reporting period.
- [ ] **C14.05.02** Calculate and display source coverage by relevant metric, showing measured, manual, imported, and estimated portions separately where supported and retaining explicit limitations for records whose provenance or quantity cannot be compared directly under the selected versioned formula and effective source arbitration rules used to produce the displayed aggregate result.
- [ ] **C14.05.03** Represent partial incline observation coverage with observed interval fraction and unavailable remainder, avoiding extrapolation from requested settings, preceding readings, or fictional route ascent unless an explicitly disclosed estimate rule produces a separately labeled result with retained assumptions and quality in the applicable dashboard view and exported derived summary metadata.
- [ ] **C14.05.04** Expose unknown physical periods independently from known stationary time and overlapping application pause, preserving correct duration semantics and preventing visual defaults or chart stacking from converting unobserved intervals into confirmed movement, complete coverage, or observed zero values in totals that downstream users may interpret as actual training evidence or completion progress.
- [ ] **C14.05.05** Mark provisional browser data and pending recalculations clearly, keeping them outside committed authoritative totals unless a deliberately labeled preview is selected and showing the last committed revision so users can distinguish unsaved drafts, stale results, and accepted actual activity when the loopback service or downstream calculation processing becomes unavailable locally.
- [ ] **C14.05.06** Test all-missing metrics, mixed-source coverage, explicit zero observations, partial incline, unknown gaps, and estimated data against independent expected totals and display states, requiring unavailable all-missing results rather than zero and retained coverage explanations in chart, table, tooltip, and export representations of the same committed selected source dataset.
- [ ] **C14.05.07** Change display units, filters, responsive layout, and accessibility mode, checking that uncertainty and unavailable states remain visible and semantically accurate rather than being dropped from compact cards or summary exports that could falsely imply complete source coverage or precise measurement of every recorded activity within the selected reporting period.
- [ ] **C14.05.08** Review aggregation rules, coverage calculations, screenshots, and accessible/export outputs; accept only when missing, estimated, incomplete, unknown, and provisional data are distinguishable from observed zeros and fully supported actual measurements across every enabled dashboard presentation and derived summary output for the approved release scope and metric dictionary revision.

### Control C14 06

**Original requirement C14.06:** Query committed SQLite records through the service and retain input revisions, calculation time, database/schema version, and selected filters. Mark stale browser snapshots and pending recalculation; a browser cache is not authoritative history.

- [ ] **C14.06.01** Define dashboard service queries using committed effective SQLite records, supported filters, and local profile identity, prohibiting browser caches, unsaved draft values, or dossier display text from becoming alternative authoritative actual history or campaign continuation inputs during aggregation and current-state presentation through the local reporting API contract for the release.
- [ ] **C14.06.02** Return input revision coverage, calculation timestamp, schema and database version, metric-definition revision, and selected filters with each dashboard snapshot, retaining enough information to reconstruct its values and determine whether a later accepted source mutation makes the displayed browser result outdated rather than silently presenting its cached figures as current history.
- [ ] **C14.06.03** Validate profile ownership and filter syntax server-side, preserving explicit report-period, timezone, category, source, and domain selection without guessing unsupported ranges or mixing physical workout and fictional completion records into one aggregate when malformed or ambiguous client parameters are submitted from stale tabs or restored browser preference caches after restart.
- [ ] **C14.06.04** Identify stale browser snapshots when committed source revisions or relevant calculation versions change, showing refresh or pending status and preserving last-known values only with a visible qualification instead of representing outdated totals as accepted current data while canonical recalculation is still incomplete or the loopback service is unavailable to reconcile state.
- [ ] **C14.06.05** Track pending derived calculations through durable invalidation records, allowing current source revisions and known stale summaries to be distinguished without optimistic browser arithmetic that independently changes actual totals, completion evidence, earned virtual credit, or committed next-leg references before the local service accepts the corresponding calculation outcome and returns its verified revision context.
- [ ] **C14.06.06** Test fresh query, cached reopen, source correction, schema-version change, invalid filters, and service outage, comparing response provenance and rendered status with expected committed input revisions and current source state rather than merely checking that some previously displayed numeric value remains available in the browser after failures or reload operations.
- [ ] **C14.06.07** Relaunch with browser cache deleted and persisted filters retained, requiring database-derived actual totals, active-day state, and committed successor to reload accurately without adding physical activity or changing chronology because the reporting page generated a new snapshot or the local service selected a different validated port for its loopback delivery.
- [ ] **C14.06.08** Review query contracts, snapshot metadata, stale indicators, and cache-replacement evidence; accept only when every current figure derives from committed SQLite inputs and the browser clearly distinguishes cached or pending views from authoritative history after corrections, service loss, schema changes, and restart under the selected local deployment and reporting policy versions.

### Control C14 07

**Original requirement C14.07:** Define preparation indicators using recorded evidence, category, and completion date for gear tests, outdoor practice, planning, and knowledge activities. A checked task indicates recorded participation, not proof of backcountry competence or fitness.

- [ ] **C14.07.01** Define preparation indicator records with category, stable task identity, accepted completion evidence, applicable assignment and content revisions, completion date, and optional equipment or planning context sufficient to explain the recorded activity without treating a checkbox as independent proof of real backcountry competence or fitness for the user's eventual expedition goals.
- [ ] **C14.07.02** Separate gear tests, outdoor practice, planning, and knowledge indicators, specifying eligible evidence and interpretation for each category rather than combining all checked tasks into an unexplained readiness score or converting nonwalking participation into physical distance, duration, achieved incline, or ascent measurements attributed to actual workouts in dashboard aggregates.
- [ ] **C14.07.03** Bind displayed task completion to committed source records and current effective status, distinguishing partial, rejected, revised, cancelled, and deleted evidence from an accepted completed preparation activity that qualifies under the applicable category-specific rule and retained content interpretation used when the assignment or knowledge activity was originally completed by the user.
- [ ] **C14.07.04** Show completion dates, evidence summaries, relevant unresolved issues, and limitations where supplied, avoiding unsupported claims that equipment was fully proven, knowledge mastered, or planning decisions guaranteed safe merely because the local app recorded participation or an educational response met its authored task criterion in a fictional scenario selected for training content.
- [ ] **C14.07.05** Provide provenance drill-down to the accepted preparation record and completion rule, retaining privacy-appropriate detail and allowing direct corrections when a task was checked accidentally, evidence changed, or equipment observations require qualification without forcing the user to invent physical activity to repair a preparation indicator on the dashboard or its narrative eligibility.
- [ ] **C14.07.06** Test accepted and partial gear, outdoor, planning, knowledge, and recovery records with missing or invalid evidence, comparing indicators with independently expected category states and requiring actual-distance totals to remain unchanged when nonwalking tasks are completed, corrected, or deleted under the shared preparation participation and progression policy definitions applied in this release.
- [ ] **C14.07.07** Review dashboard cards, tables, accessibility alternatives, and exports with users and content reviewers, checking whether labels communicate recorded participation and limitations rather than implying certification, validated expedition readiness, predicted thru-hike completion, or immunity from injury and environmental risk beyond what the recorded task evidence actually demonstrates in the supported local training context.
- [ ] **C14.07.08** Accept only when preparation indicators trace to attributable evidence and dates, category interpretations are reviewed, corrections remain available, and no checked task is presented as proof of fitness or backcountry competence unsupported by the authored activity and its documented scope, source references, completion rule, and accepted review limitations for the enabled content revision.

### Control C14 08

**Original requirement C14.08:** Compare actual performance with the applicable assignment/plan snapshot. Distinguish partial, completed, skipped, cancelled, and rescheduled work, and preserve original-versus-revised scheduling where it materially changes interpretation.

- [ ] **C14.08.01** Compare actual activity with the assignment and plan snapshots applicable when the activity was accepted, retaining stable historical references so later target or schedule revisions cannot silently change whether a previously recorded workout appeared partial, completed, or nonadherent under the originally accepted plan shown in dashboard interpretation and exports.
- [ ] **C14.08.02** Define status-specific adherence inclusion rules for partial, completed, skipped, cancelled, superseded, and rescheduled assignments, distinguishing absent exercise from accepted recovery or preparation participation rather than treating every nonwalking date as failure or every removed assignment as successfully completed work in aggregate progress against the user's selected plan period.
- [ ] **C14.08.03** Preserve original and revised schedule dates with attributable change history, displaying both where postponement or retrospective editing materially affects interpretation of lateness, participation, or planned-versus-actual comparison in the selected reporting calendar and retaining the relevant version and timezone needed to reconstruct that interpretation after restart or future plan revision.
- [ ] **C14.08.04** Use effective actual source quantities and accepted completion rules for comparisons, distinguishing missing measurements and unknown periods from confirmed underperformance and avoiding inference that application timer duration or requested incline proves the user achieved the assignment's physical targets during a recorded session with incomplete evidence or aggregate-only self-reported duration meaning.
- [ ] **C14.08.05** Provide explanatory status and snapshot details in drill-down views, allowing users to identify which accepted target, schedule, and completion criterion was used rather than presenting an unexplained adherence percentage detached from historical plan revisions, substitutions, user-approved alternatives, or explicit category-specific evidence for recovery and preparation tasks contributing to the comparison metric.
- [ ] **C14.08.06** Test partial walking, completed preparation, skipped sessions, cancellation, postponement, substitution, splitting, and retrospective target edits against independently specified adherence outcomes, requiring preserved original interpretation where policy demands it and explicit revised explanations where a deliberate accepted historical correction changes applicable evidence or schedule meaning for displayed comparisons and generated exports.
- [ ] **C14.08.07** Recalculate after accepted corrections and reassignment, checking physical activity remains counted once and schedule/status changes do not erase actual measurements or rewrite completed assignment snapshots through dashboard refresh, cached browser preferences, or relaunch loading the latest plan rather than the specific historical revision associated with each recorded workout or completed preparation task.
- [ ] **C14.08.08** Review comparison definitions, snapshot references, change-history displays, and ledger evidence; accept only when users can distinguish each assignment outcome and understand materially changed schedules, with every adherence figure reproducible from effective activity plus the applicable accepted plan revision rather than silently revised targets or unsupported assumptions about missing measurement evidence and optional background information.

### Control C14 09

**Original requirement C14.09:** Count each effective physical workout once across splits, reassignment, duplicate reconciliation, and imports. Keep launches, dossier views, generated days, started days, and completed days as separate events; none contributes activity unless linked to an effective actual workout/task record. Sum canonically and round only for display.

- [ ] **C14.09.01** Define effective physical-activity aggregation over canonical workout identities and accepted allocations, excluding superseded revisions, duplicate aliases, secondary observations, and reassignment references that do not represent additional underlying actual exercise or separate source quantities eligible for the selected metric's documented inclusion rules and provenance classifications used by the local reporting service.
- [ ] **C14.09.02** Distinguish launch, dossier view, generated day, started day, completed day, workout start, and actual task records as separate event types, specifying which can contribute counts and which may contribute physical quantities only through qualifying effective source workout or category-specific preparation evidence rather than by event existence, timestamp, or linked presentation context alone.
- [ ] **C14.09.03** Implement canonical summation before display rounding, preserving residual precision and null semantics across split portions and mixed units so repeated short sessions or reassignment cannot gain or lose actual activity through row-level rounding, duplicate source joins, or summing both original and allocated workout quantities in the same dashboard period query.
- [ ] **C14.09.04** Validate joins and source eligibility to avoid multiplicative aggregation when workouts have multiple assignment, day, import, or journal relationships, using explicit effective-record selection and allocation rules that preserve one physical contribution while allowing separately labeled fictional credits and source-provenance references to retain their intended independent reporting domains in relevant dashboard views.
- [ ] **C14.09.05** Expose event counts with explicit labels and definitions, preventing repeated launches, generated dossiers, started-but-unfinished sessions, or completed fictional days from appearing as recorded walking participation without accepted actual workout evidence or preparation records that qualify for the selected category-specific metric under the applicable dictionary and completion policy revisions used in this release.
- [ ] **C14.09.06** Test original/split/reassigned records, probable overlaps, accepted duplicates, multiple sources, and numerous passive launches against an independent effective ledger, requiring conserved quantities, correct actual counts, and separate event totals with no manufactured physical activity from presentation or launcher records regardless of report filter, period grouping, or source selection applied in the dashboard view.
- [ ] **C14.09.07** Correct and delete sources with many relationships, then recalculate and restart, verifying aggregate queries exclude obsolete effective records and residual quantities remain conserved without double counting replacements, repeated outbox processing, or stale browser snapshots combined with freshly retrieved totals from committed SQLite records that now reflect the accepted revised source lineage and allocation state.
- [ ] **C14.09.08** Review query logic, canonical precision, event dictionaries, and reconciled chart/table/export totals; accept only when every physical quantity appears once through effective source selection and passive launches, views, generated days, or virtual completion records cannot contribute exercise absent qualifying actual records clearly identified in the dashboard's provenance drill-down and exported metric definitions.

### Control C14 10

**Original requirement C14.10:** Identify materially changed sources, equipment, calibration, or metric definitions on trends. Avoid plotting unlike data as an uninterrupted directly comparable sequence without annotation or an explicit user-selectable normalization.

- [ ] **C14.10.01** Define material trend-change metadata for measurement source, equipment, calibration, unit interpretation, quality, and metric-definition revision, linking effective dates and affected records to source provenance rather than inferring comparability merely because values share display units or fall within the same dashboard chart series selected by the current report filter or period setting.
- [ ] **C14.10.02** Detect supported changes from committed source and configuration revisions, annotating the point or period where assumptions differ and preserving a readable explanation of why apparent increases or decreases may reflect measurement method rather than changed actual performance, training capacity, preparation quality, or physical readiness under the user's accepted plan and recorded evidence for that interval.
- [ ] **C14.10.03** Separate unlike source segments or offer clearly identified normalization only where a reviewed formula and adequate data support it, retaining original values, assumptions, calculation version, and user selection instead of silently replacing the physical ledger or showing estimated normalized quantities as measured activity recorded by the original manual or device sources.
- [ ] **C14.10.04** Represent missing calibration or equipment context as unknown comparability, avoiding fabricated constants, guessed device equivalence, or claims that a trend has been corrected when the selected data lacks the observations needed to support the disclosed transformation or meaningful direct comparison across measurement methods and source quality changes in the chosen reporting interval.
- [ ] **C14.10.05** Carry change annotations and normalization state into accessible tables and exports, allowing users to interpret historical segments outside the chart without losing the source, calibration, equipment, definition, uncertainty, or calculation-version distinctions that materially qualify the plotted values and apparent trends generated from committed effective workout and preparation records in the release.
- [ ] **C14.10.06** Test device replacement, calibration change, manual-to-measured transition, revised duration definition, and missing context against independently expected annotations and grouping, requiring unlike data to remain visibly qualified and any optional normalization result to match its disclosed formula without altering original source quantities, evidence labels, or historical provenance recorded in the authoritative workout ledger.
- [ ] **C14.10.07** Apply source corrections and report filters, verifying material-change labels update with effective revisions and normalization can be reversed or deselected without losing originals or modifying accepted assignment targets, progression conversions, actual-record definitions, or committed fictional next-leg state through a dashboard presentation preference intended solely to qualify trend comparison for the user.
- [ ] **C14.10.08** Review chart segments, textual alternatives, formula evidence, and export annotations; accept only when unlike measurements cannot appear as an uninterrupted directly comparable series without qualification and optional normalization is deliberate, reversible, inspectable, and explicitly distinguished from original physical observations and accepted plan performance expectations under the metric dictionary and selected release calculation policy.

### Control C14 11

**Original requirement C14.11:** Include accepted recovery and preparation assignments in appropriate adherence views. Make streak definitions explicit and prevent reminders or achievement language from promoting unapproved compensatory exercise.

- [ ] **C14.11.01** Define adherence eligibility for accepted walking, recovery, equipment, planning, outdoor, and knowledge assignments, preserving each category's evidence and schedule rather than equating all participation with consecutive-day walking or treating nonwalking recovery as missing exercise in the selected plan adherence metric and trend displays used by the dashboard for the release.
- [ ] **C14.11.02** Publish streak definitions with expected schedule, eligible categories, partial work handling, gaps, rescheduling, and completion boundaries, distinguishing personal plan participation from a universal daily exercise requirement that could otherwise misrepresent legitimate accepted recovery or preparation days as failure and encourage unplanned additional physical activity solely to maintain a fictional or displayed achievement count.
- [ ] **C14.11.03** Include accepted recovery and preparation completions in appropriate adherence views without adding physical walking quantities, clearly labeling their participation meaning and limitations while keeping actual distance, movement time, incline exposure, and fictional chapter credit domains independent under the versioned metric, category, and progression policies applicable to the source records being reported.
- [ ] **C14.11.04** Review achievement, reminder, and gap language for pressure to compensate after missed sessions, removing automatic target increases or demands for additional exertion and providing plan-consistent choices such as recorded partial participation, postponement, accepted substitution, or scheduled recovery without suggesting those choices validate a predicted fitness or thru-hike completion outcome for the user.
- [ ] **C14.11.05** Keep notification acknowledgement distinct from accepted assignment evidence, ensuring reminder replies, dismissals, page visits, and launch events cannot lengthen adherence streaks or mark workouts and preparation tasks completed without the documented completion rule and qualifying committed source record under the selected category-specific participation semantics used by the dashboard and campaign credit systems.
- [ ] **C14.11.06** Test planned recovery, preparation-only weeks, skipped walking sessions, partial evidence, postponement, and disabled reminders against independently defined adherence and streak outcomes, requiring truthful status without fabricated exercise, rejected legitimate participation, or language that prescribes compensatory physical targets in response to missing events or a broken fictional achievement sequence in the report period.
- [ ] **C14.11.07** Change accepted schedules and streak preferences with retained revision context, verifying recalculated views explain altered definitions and preserve historical actual quantities, completed snapshots, original dates where material, and the independent committed campaign successor rather than reinterpreting browser preference changes as new workout completion or virtual-day advancement performed automatically through the reporting interface.
- [ ] **C14.11.08** Review definitions, category inclusion, reminder wording, and user interpretation evidence; accept only when adherence reflects the accepted plan and displayed streaks or achievements cannot pressure users toward unapproved compensatory exercise or silently promote reminder responses, recovery participation, or preparation records into physical walking evidence that was never supplied in effective source activity records.

### Control C14 12

**Original requirement C14.12:** Provide provenance drill-down from each total to its included workouts/tasks, revisions, formula, and exclusions. Offer a direct correction path and explain why some entries do not qualify for a particular metric.

- [ ] **C14.12.01** Provide drill-down from each displayed aggregate to included effective workout or task identities, input revisions, formula version, units, filters, source quality, and exclusion rules, preserving a reproducible causal explanation rather than presenting totals that can only be trusted by inspecting hidden implementation logic or a transient browser cache representation of historical values.
- [ ] **C14.12.02** List excluded, superseded, duplicate, missing, and ineligible records with appropriate reasons and minimal privacy-permitted context, distinguishing nonqualification from lost data or zero activity and allowing users to understand why a preparation task or self-reported duration does not contribute to a particular physical measurement or fictional accomplishment metric under the selected reporting policy.
- [ ] **C14.12.03** Show constituent canonical values and accepted allocations before display rounding, allowing reviewers to verify conserved quantities across split workouts, reassignment, mixed units, and selected source observations without accidentally summing historical revisions or alternate device readings that describe the same underlying actual physical activity recorded once in the effective workout ledger maintained by the local service.
- [ ] **C14.12.04** Provide a direct correction path linked to the current source revision, retaining the report's filter and navigation context while requiring validated expected-revision mutation through the logger or task service rather than allowing dashboard edits to overwrite calculated totals or bypass physical-target acceptance rules for the historical assignment snapshot being compared against source performance.
- [ ] **C14.12.05** Explain formula limits, uncertainty, coverage, and pending calculations in the drill-down, making unavailable data and estimates inspectable without exposing sensitive optional fields unnecessarily or asserting that numerical precision demonstrates complete observation, real fitness readiness, or validated wilderness judgment beyond the recorded source evidence and authored preparation task interpretation permitted for the selected release.
- [ ] **C14.12.06** Test totals built from corrections, duplicate exclusions, partial evidence, missing values, multiple categories, and mixed sources, tracing every displayed quantity to independently expected included records and formula results while verifying excluded records have truthful reasons and no actual or fictional contribution appears without a stable effective source and applicable versioned calculation context.
- [ ] **C14.12.07** Exercise correction from drill-down followed by stale-tab conflict and service loss, requiring retained navigation, explicit unsaved or pending status, preserved source data, and current revision retrieval before updated totals are presented as authoritative rather than silently applying browser-only arithmetic or discarding input when a correction cannot be committed to the local database service.
- [ ] **C14.12.08** Review trace samples, correction usability, exclusion explanations, and sensitive-field scope; accept only when every aggregate can be reconstructed from permitted source evidence and users have an accessible validated correction route with clear reasons for records that do not qualify under the inspected metric definition, source selection, and reporting filters currently applied to the dashboard result.

### Control C14 13

**Original requirement C14.13:** Recalculate summaries after committed corrections/deletions/day completion and safely retry persisted invalidation events after process restart. On service loss or stale revision show status; on relaunch reload committed history and active/next-day references before presenting current totals.

- [ ] **C14.13.01** Define invalidation triggers for committed workout or task correction, deletion, assignment changes, source arbitration, metric-version updates, and explicit day completion, documenting which summaries and active/next-day references must refresh and which actual quantities remain unaffected by fictional completion or presentation events under the local reporting contracts and domain boundaries used in this release.
- [ ] **C14.13.02** Persist required invalidation events or atomic derived updates with accepted source mutations, ensuring acknowledged changes retain recoverable downstream work rather than relying on transient browser callbacks, in-memory event listeners, or page reload side effects to notify dashboards that their cached calculation inputs became obsolete when the effective repository database source revision changed.
- [ ] **C14.13.03** Deduplicate recalculation by causal source revision and calculation identity, retrying safe pending work after process restart without creating repeated actual quantities, campaign credits, changed assignment evidence, or additional committed successor movement merely because the same invalidation request or durable outbox event is delivered again to reporting consumers during interrupted recovery processing.
- [ ] **C14.13.04** Track calculation input revisions and expose pending or stale results until successful refresh, preserving last-known values only with clear status while avoiding optimistic browser totals that can falsely imply an uncommitted correction or deletion already changed authoritative history when the local service is unavailable, conflicted, or unable to persist the accepted recalculation result.
- [ ] **C14.13.05** Reload committed history, active unfinished day, and saved next-leg reference after relaunch before presenting current campaign continuation, keeping launch logs distinct from actual activity and ensuring the dashboard does not select a leg from cached browser mileage, file timestamps, newly generated dossier presence, or a recalculated credit total that lacks explicit day-completion authority.
- [ ] **C14.13.06** Test corrections, deletion, and day completion with normal, delayed, duplicate, and failed recalculation events, comparing eventual summaries and displayed state with independently expected effective ledgers while checking interim status identifies the outdated dependency and no physical quantity changes solely because a fictional day completed or a report query generated a new snapshot.
- [ ] **C14.13.07** Terminate after source commit before refresh and recover with service outage or stale tabs, requiring durable retries, preserved accepted revisions, consistent source-to-summary lineage, and clear unsaved or pending indicators that distinguish provisional client drafts from canonical changes and successfully recalculated totals retrieved through the validated loopback service after local restart completes.
- [ ] **C14.13.08** Review invalidation records, restart traces, current-state loading, and independent reconciliation evidence; accept only when every acknowledged source change eventually produces consistent summaries and passive refresh, relaunch, cached data, or recalculation cannot independently create exercise, complete a hike day, or advance the committed next-leg pointer outside explicit eligible service-owned completion transactions.

### Control C14 14

**Original requirement C14.14:** Supply accessible chart alternatives with equivalent data tables, descriptive units, keyboard-operable controls, visible focus, and text/patterns beyond color. Reduced-motion and enlarged-text modes must preserve meaning and navigation.

- [ ] **C14.14.01** Provide equivalent data tables for every chart containing the same values, period labels, units, uncertainty, source coverage, and relevant annotations, allowing full interpretation when graphics cannot be seen, pointer hover is unavailable, or the user selects a text-oriented accessibility mode at supported magnification and display sizes for the selected dashboard release.
- [ ] **C14.14.02** Implement keyboard-operable filter, period, metric, drill-down, and export controls with visible focus, predictable order, meaningful accessible names, and retained state after refresh, avoiding essential functions that require dragging, precise pointer interaction, or reading unlabeled visual chart elements to identify current selected values and pending data status in the report view.
- [ ] **C14.14.03** Use text, patterns, symbols, or direct labels beyond color to distinguish actual and fictional domains, source changes, unavailable values, estimates, and assignment states, ensuring those distinctions retain semantic meaning in grayscale, reduced contrast contexts, accessible tables, and textual exports generated from the same selected committed inputs and calculation version displayed by the chart.
- [ ] **C14.14.04** Expose chart titles, axis definitions, period boundaries, and summary descriptions through accessible semantics, describing interpretation and uncertainty without making unsupported readiness claims or replacing complete underlying tables with vague summaries that prevent users from independently inspecting individual effective quantities, missing intervals, or corrected observations included in the selected dashboard result and drill-down provenance.
- [ ] **C14.14.05** Honor reduced motion by removing nonessential chart animation, preserving updated-value announcements and focus without triggering repetitive screen-reader notices or forcing users to watch transitions to understand whether a calculation became current, a source correction changed the data, or a selected period now contains unavailable rather than observed zero physical measurements for that metric.
- [ ] **C14.14.06** Support enlarged text and responsive layouts without clipped legends, hidden controls, overlapping rows, or lost unit qualifiers, preserving readable table headers and direct chart-to-table navigation so alternate presentation modes continue exposing the same source coverage and domain distinctions instead of sacrificing essential interpretation for a compact layout or a narrower display while reporting locally.
- [ ] **C14.14.07** Test keyboard, screen reader, reduced motion, enlarged text, grayscale, and broken visual asset scenarios with corrected and mixed-source data, comparing accessible table values and annotations against the chart and independent effective ledger and verifying every control remains usable during stale-service status, filter changes, pending recalculation, and direct source correction navigation from a drill-down result.
- [ ] **C14.14.08** Retain accessibility findings, repaired defects, and chart/table parity evidence; accept only when all report meanings and actions are available through supported alternatives and presentation changes cannot conceal actual-versus-fictional labels, source coverage, uncertainty, data status, or the units and calculation context needed to interpret the selected values accurately in the approved dashboard release.

### Control C14 15

**Original requirement C14.15:** Keep reporting local/private without required cloud authentication. Scope optional exports independently by period, metric, identity, notes, and detail; explain filesystem storage and copied-export limitations. Exporting a campaign milestone must not implicitly include personal workout detail.

- [ ] **C14.15.01** Operate reporting from local-profile and repository data without required cloud authentication, identifying filesystem locations and loopback-service boundaries for dashboard snapshots, preferences, managed exports, and diagnostics while documenting local device access assumptions that determine who can inspect optional personal activity detail stored under the enabled deployment configuration for the selected release.
- [ ] **C14.15.02** Provide independent export selection for period, metrics, identity, notes, source detail, and fictional accomplishments, previewing included fields so choosing a campaign milestone cannot automatically attach private workout measurements, biometric observations, background information, or journal text that the user did not deliberately include in the current export scope through the local interface.
- [ ] **C14.15.03** Minimize campaign-summary detail by default, retaining only needed fictional outcomes and policy-permitted lineage unless the user selects actual activity information explicitly, distinguishing optional sharing preferences from the authoritative physical records that remain available locally for private ledger reconciliation and accepted-plan interpretation without a remote account or external reporting destination configured.
- [ ] **C14.15.04** Explain managed local file storage and copied-export limitations in the export workflow, identifying the destination and what the app can later update or delete without claiming control over unmanaged duplicates, manually moved files, remote recipients, or backup copies beyond the retention and restore boundary documented for locally generated report artifacts under the release policy.
- [ ] **C14.15.05** Apply local profile and origin validation to reporting queries and export creation, preventing untrusted origins or incompatible profile references from retrieving sensitive source details while ensuring the ordinary manual local workflow remains usable offline and does not depend on mandatory registration, remote authorization services, or implicit transmission to external analytics to generate a selected report.
- [ ] **C14.15.06** Test narrow period exports, omitted identity and notes, selected actual detail, campaign-only milestones, and empty result sets against independently expected field scope, requiring absence of unselected sensitive content across filenames, embedded metadata, manifests, diagnostics, and generated export bodies rather than checking only the visible chart or selected top-level summary text itself.
- [ ] **C14.15.07** Review privacy defaults and export previews with users, confirming that scope choices, destination labels, local accessibility assumptions, and copy limitations are understood before any enabled external sharing operation occurs and that failed export creation does not silently publish provisional data or alter actual workout records, accepted assignment targets, or committed fictional successor state.
- [ ] **C14.15.08** Retain access tests, scoped export samples, and reviewed privacy explanations; accept only when reporting remains locally usable without mandatory cloud identity and every optional export includes precisely the selected domain and personal detail, with honest managed-copy boundaries and no implicit disclosure of workout content through campaign milestones, diagnostics, or unrelated summary-generation actions.

### Control C14 16

**Original requirement C14.16:** Export selected periods and filters with timezone, units, definitions, source/quality coverage, input revisions, and generation time. Distinguish source records from derived summaries and fictional campaign statistics.

- [ ] **C14.16.01** Define export formats containing selected period boundaries, filters, governing timezone, units, metric definitions, calculation version, source and quality coverage, input revisions, and generation time, ensuring portable summaries retain enough interpretation and reproducibility context rather than presenting bare rounded totals disconnected from their committed actual records or fictional progression policy relationships in the release.
- [ ] **C14.16.02** Separate source-record exports from derived summaries and fictional statistics through explicit sections or column classifications, preserving actual measurement provenance and campaign definitions without implying scaled virtual distance, chapter completion, generated days, or launch counts are additional physical activity recorded by the user within the selected report period or linked preparation evidence included in the export scope.
- [ ] **C14.16.03** Generate from effective committed SQLite inputs and accepted calculation revisions, honoring selected period, metric, profile, identity, and sensitive-field scope while marking incomplete or stale summaries appropriately rather than filling missing physical observations with zeros or silently including provisional browser drafts that failed to persist through the local service before the export snapshot was assembled.
- [ ] **C14.16.04** Preserve null, meaningful zero, aggregate-duration definitions, estimates, partial incline coverage, unknown periods, and material source changes, carrying their interpretation into export metadata and human-readable tables so a recipient can distinguish supported physical quantities from unavailable or derived information without needing the original browser chart, hover labels, or cached presentation preferences to understand the selected report correctly.
- [ ] **C14.16.05** Include stable input and revision references adequate for reconciliation, documenting duplicate exclusions and split allocation where exported detail permits while minimizing private content that is unnecessary to explain the selected summaries under the user's scope or permitted minimal provenance retained after sensitive-field deletion and lifecycle expiry under the selected deployment policy version used for the generated artifact.
- [ ] **C14.16.06** Test matched chart, table, source-record, and derived-summary exports for mixed units, timezones, corrections, missing values, splits, preparation tasks, and scaled campaign modes, comparing each selected figure with an independently constructed effective ledger and checking exported filters and definition versions reproduce the exact intended reporting boundaries and accepted source coverage interpretation used by the dashboard view.
- [ ] **C14.16.07** Exercise export creation after recalculation failure, service loss, source deletion, and filter changes, requiring clear failure or qualified pending status and deliberate retry rather than silently generating an apparently current artifact from obsolete cached numbers, deleted private detail, or uncommitted source edits absent from effective canonical repository history at the export generation time recorded in its manifest.
- [ ] **C14.16.08** Review portable samples, metadata completeness, source-versus-summary labels, and independent reconciliation results; accept only when exported periods and filters are faithful and actual records, estimates, derived aggregates, and fictional statistics remain distinguishable with retained definitions, coverage, revision lineage, and privacy scope outside the original dashboard interface for the approved release and selected metric dictionary revision.

### Control C14 17

**Original requirement C14.17:** Keep optional goal targets and user-defined comparisons inspectable and editable. Explain their origin and avoid representing progress toward a personal target as a validated prediction of thru-hike completion or injury avoidance.

- [ ] **C14.17.01** Model optional user-defined goals and comparisons with identity, author or origin, target value, units, category, period, effective dates, calculation meaning, revision, and optional notes, distinguishing personal choices from reviewed assignment targets or validated preparation predictions inferred by the app from fictional route completion, resource balances, or narrative events during campaign participation.
- [ ] **C14.17.02** Provide inspectable goal creation and editing with original-versus-proposed values, clear units, scope, and accepted changes where goals affect physical assignments, preserving the boundary between a dashboard comparison preference and an actual training-plan revision that requires explicit deliberate acceptance through the plan service before altered duration, distance, speed, or incline targets become authoritative in the repository.
- [ ] **C14.17.03** Show progress toward personal targets as descriptive comparison against recorded qualifying sources, identifying missing measurements, estimates, excluded categories, and applicable periods rather than claiming that a percentage or completed target validates thru-hike feasibility, predicts successful route completion, demonstrates wilderness competence, or guarantees injury avoidance for the user in an individualized training or medical sense.
- [ ] **C14.17.04** Allow optional goal omission, cancellation, or revision without blocking ordinary reporting and story access, retaining history where policy requires it and ensuring removed goals do not erase actual activity or create compulsory compensatory exercise to restore a streak, percentage, or fictional milestone previously tied to the user's selected comparison preferences or reporting dashboard view.
- [ ] **C14.17.05** Validate goal units, periods, numeric bounds, eligibility, and zero or absent targets, preventing divide-by-zero displays, dimensionally incompatible comparisons, and silently invented defaults when the user leaves a personal goal unspecified or imports an unsupported definition into the local reporting profile under the current accepted metric dictionary revision for the selected release and category scope.
- [ ] **C14.17.06** Test target creation, inspection, revision, removal, missing observations, mixed categories, and stale edits, comparing progress with independently expected effective source sums and checking actual workout values, accepted assignment snapshots, progression conversions, and committed next-leg state remain unchanged when the user modifies a dashboard-only goal or comparison setting outside the plan mutation workflow.
- [ ] **C14.17.07** Review goal wording and origin labels with users and training reviewers, correcting any interpretation that personal targets constitute validated fitness readiness or injury prevention predictions and retaining practical limitations, selected evidence definitions, and user-approved changes needed to explain historical goal comparisons or exported progress summaries generated from the committed report inputs and applicable goal revision.
- [ ] **C14.17.08** Accept only when every enabled goal is optional, attributable, inspectable, and editable under explicit rules, progress calculations reconcile to qualifying actual or preparation evidence, and no personal target comparison is presented as a validated forecast of expedition completion, medical safety, or freedom from injury unsupported by reviewed sources and the supplied training-content scope for the user.

### Control C14 18

**Original requirement C14.18:** Compare aggregates against independently constructed ledgers containing nulls, zero values, uncertainty intervals, splits, revisions, duplicates, overnight sessions, mixed units, and timezone changes. Verify chart/table/export agreement.

- [ ] **C14.18.01** Construct independent effective ledgers with nulls, meaningful zeros, observed and unknown intervals, self-reported aggregate durations, splits, corrections, duplicate aliases, overnight sessions, mixed units, and timezone changes, recording expected metric inclusion, source selection, precision, and period membership before calculating dashboard outputs or using its formulas as reference expectations for the verification evidence.
- [ ] **C14.18.02** Calculate expected totals and coverage independently at canonical precision, defining chart, table, and export display-rounding expectations separately so row-level formatting cannot conceal duplicated activity, lost residuals, invalid null-to-zero substitution, or differences in actual-versus-fictional reporting domain inclusion arising from the aggregation queries and source revision filters used in the selected dashboard calculation implementation.
- [ ] **C14.18.03** Specify period allocations across midnight, daylight-saving transitions, timezone travel, week starts, and date-only tasks, requiring adjacent-period sums and historical reproducibility to match the approved reporting contract without double counting whole records or inferring unsupported interval breakdowns from aggregate-only manual durations whose declared meaning and physical coverage remain limited in the effective source ledger.
- [ ] **C14.18.04** Create correction, split, reassignment, and duplicate-reconciliation fixtures with preserved source lineage, testing effective quantities and counts against independent conservation rules rather than counting historical revisions or alternate device observations as separate actual activity when record joins include multiple assignment or campaign relationships that can otherwise multiply the selected canonical measurement values in report aggregates.
- [ ] **C14.18.05** Include incomplete incline, estimated quantities, source changes, pending calculations, and all-missing metrics, defining expected unavailable states and uncertainty annotations so verification checks interpretation as well as numerical results and does not accept a misleading zero, continuous comparable trend, or apparently measured value when the recorded evidence supports only partial, unknown, provisional, or differently sourced information for a selected period.
- [ ] **C14.18.06** Run fixture sets through chart, table, drill-down, and each enabled export format, requiring agreed source filters, calculation versions, values, units, coverage, and domain labels; separately compare actual workout and preparation metrics with fictional progression quantities to reveal unintended cross-domain inclusion or misleading combined totals detached from the authoritative ledger and explicit campaign completion semantics of the release.
- [ ] **C14.18.07** Apply source revisions and refresh the same reports after restart and browser cache deletion, comparing current and historical outputs with the expected ledgers while verifying persisted filter choices remain reproducible and no repeated query, launch, dossier view, or restored dashboard snapshot adds physical activity or changes the independently committed next-leg pointer in SQLite campaign history.
- [ ] **C14.18.08** Retain fixture definitions, independent arithmetic, period expectations, output comparisons, and repaired discrepancies; accept only when chart, table, and exports agree with effective evidence for every named boundary class, including honest null and uncertainty treatment, conserved split quantities, deduplicated observations, timezone membership, and independent actual-versus-fictional domains under the versioned metric and reporting contracts of the selected release.

### Control C14 19

**Original requirement C14.19:** Verify local-service outage, stale browser revisions, process-restart recovery, recalculation failures, deletion propagation, persisted filters, source-version changes, and optional export scoping. Compare pre/post-relaunch totals and next-leg references; all-missing metrics remain unavailable and repeated launches add no activity.

- [ ] **C14.19.01** Define recovery scenarios for loopback outage, stale browser revisions, process restart, failed recalculation, deletion, saved filters, source-version changes, and scoped exports, recording expected committed quantities, unavailable states, source coverage, active day, and next-leg references before each injected failure or accepted mutation reaches its durable persistence boundary in the local service.
- [ ] **C14.19.02** Disconnect the local service with cached dashboards visible, requiring clear stale or unavailable status and exclusion of provisional drafts from authoritative totals while retaining supported inspection context and recovery navigation without falsely acknowledging source corrections, completed assignments, actual exercise, or explicit fictional-day advancement that never committed to SQLite while the API was inaccessible through the browser.
- [ ] **C14.19.03** Commit corrections or deletion from another tab, then exercise stale dashboard queries and source-version changes, requiring updated revision metadata or explicit pending state and eventual agreement with an independently expected ledger rather than silently retaining old values or merging cached totals with fresh database-derived results that can double count physical activity in the selected report period.
- [ ] **C14.19.04** Terminate after invalidation persistence but before recalculation, requiring restart to retry durable pending events and produce consistent chart/table/export results without losing accepted corrections, resurrecting deleted sensitive detail, duplicating recalculated credits, or changing committed campaign successor state solely because a dependent consumer reprocessed the same source revision and effect identity after local interruption or retry.
- [ ] **C14.19.05** Persist filters and reload across service port changes, cleared browser caches, and the required launcher path, checking report periods, timezone, category selection, actual totals, active unfinished day, and saved successor resolve from committed repository state rather than obsolete browser-only preferences or file timestamps mistakenly treated as canonical history by resumed dashboard initialization code.
- [ ] **C14.19.06** Test all-missing quantities and repeated launches with no new workout evidence, requiring unavailable aggregates, unchanged actual activity counts and measurements, and distinct run events; verify report queries and generated snapshots do not convert absence of observations into zeros or interpret new dossier generation as newly completed training activity or hike-day advancement on relaunch.
- [ ] **C14.19.07** Exercise narrow export scope during stale, deleted, and pending states, verifying selected periods, metrics, identity, notes, quality, and domain classifications appear only as allowed and current or qualified status is truthful without including private details, obsolete values, or provisional browser edits excluded from the effective canonical source records and selected export filters after recovery completes.
- [ ] **C14.19.08** Compare pre/post-relaunch ledgers, filters, revision coverage, deletion propagation, source annotations, and next-leg references, retaining fault evidence and repaired defects; accept only when reporting recovers durably, all-missing metrics remain unavailable, optional scope is honored, repeated launches add no activity, and passive dashboard or recalculation paths never substitute for explicit day completion.

### Control C14 20

**Original requirement C14.20:** Complete screen-reader, keyboard, contrast, enlarged-text, and interpretation reviews. Require traceability for every total and documented limits for every estimate; remove unsupported readiness language before release.

- [ ] **C14.20.01** Complete screen-reader review of totals, charts, tables, units, source coverage, uncertainty, filters, drill-down, corrections, and exports, requiring equivalent interpretation and actionable stale or failed-save status without relying on visual hover, unlabeled icons, color alone, or repeated announcements that obscure essential reporting context and navigation for the approved accessibility/browser combinations in the selected release.
- [ ] **C14.20.02** Conduct keyboard-only review of period selection, source filtering, chart/table navigation, personal goals, provenance drill-down, and correction recovery, verifying visible focus, predictable sequence, modal control, retained context, and accessible errors after service loss or stale revisions so users can inspect and repair source data without pointer precision or inadvertent physical-target acceptance or campaign-state mutation.
- [ ] **C14.20.03** Review contrast and enlarged-text layouts across compact cards, long tables, legends, help text, pending statuses, and export controls, checking that domain qualifiers, units, missing values, source changes, and estimate labels remain readable without clipping, overlap, hidden controls, or semantic loss when the interface reflows at documented supported magnification, display sizes, and reduced-motion settings.
- [ ] **C14.20.04** Perform interpretation sessions with actual, planned, preparation, and fictional examples, assessing whether users distinguish source measurements, personal targets, unknown periods, nonwalking participation, earned virtual credit, completed days, and explicit next-leg state rather than concluding that timers prove walking, task checkmarks certify competence, or scaled campaign distance demonstrates additional physical exercise in reported actual records.
- [ ] **C14.20.05** Trace every total and chart segment to effective source records, accepted allocations, revision filters, formulas, and period definitions, requiring independent reconciliation and inspectable exclusions instead of relying on broad claims that the dashboard calculates accurately without reviewed evidence for splits, corrections, duplicates, nulls, source changes, uncertainty, and the selected calendar interpretation affecting a displayed result.
- [ ] **C14.20.06** Review every estimate and optional normalization for disclosed assumptions, formula, coverage, source quality, calculation version, and practical limits, removing unsupported readiness, medical-risk, injury-avoidance, or expedition-completion predictions that exceed the documented descriptive meaning of recorded participation and supplied reviewed training content in the current metric dictionary and enabled preparation indicators for the chosen release scope.
- [ ] **C14.20.07** Resolve blocking accessibility and interpretation defects, documenting remaining limitations, responsible owners, review evidence, and deployment boundaries for optional exclusions while verifying corrected wording and alternate table exports preserve the same actual-versus-fictional distinctions, missing-value behavior, source lineage, and explicit completion semantics used by the authoritative local service rather than inconsistent browser presentation-only approximations.
- [ ] **C14.20.08** Accept release only with reviewed accessibility workflows, truthful interpretation evidence, reproducible provenance for every actual or fictional total, documented estimate limits, and removed unsupported readiness language, retaining exact application, schema, metric-definition, content, and reporting-policy revisions so acceptance status refers to the implementation and data meaning actually reviewed under the declared supported local deployment and user context.

## C15 Web application shell

**Accountable owner:** Application product owner. **Technical owner:** Web application engineering. **Reviewers:** Accessibility, security, reliability, and user data owners.

**Inputs:** Local-service responses containing versioned dossiers, media manifests, assignments, campaign state, and user preferences. **Outputs:** Accessible views, validated API mutations, durable-save receipts, and actionable status. The repository-local service and SQLite database are authoritative; browser cache and view state cannot independently advance the hike.

**Required evidence:** Local architecture and API contracts; browser matrix; accessibility assessment; reference-device performance report; server/storage fault results; request retry and multi-tab reconciliation; security tests; migration/restoration report.

**Exit criterion:** A user can launch, complete, and recover a repository-local daily experience, record actual training once, resolve conflicting tabs, and export history on supported platforms, with honest persistence status and no unauthorized mutations.

### Control C15 01

**Original requirement C15.01:** Document the browser, repository-local domain service, SQLite persistence, generation pipeline, and PowerShell launch boundaries; give each authoritative record one defined owner and versioned interface.

- [ ] **C15.01.01** Draw the launch, browser, domain-service, generation, and SQLite data flows, identifying process boundaries, request paths, persisted records, and failure handoffs.
- [ ] **C15.01.02** Create an authority matrix naming the sole writer and permitted readers for campaigns, hike days, workouts, decisions, publication markers, and generated artifacts.
- [ ] **C15.01.03** Specify interface versions, operation identifiers, and ownership-transfer rules where one component requests another component's consequential action.
- [ ] **C15.01.04** Separate presentation calculations from authoritative domain calculations; identify every derived browser value that must be revalidated by the service.
- [ ] **C15.01.05** Document startup, restart, shutdown, and unavailable-service sequences, including how incomplete generation and unsent browser drafts remain distinguishable.
- [ ] **C15.01.06** Trace a successful daily journey through the diagram and reconcile every durable change with its named owner and transaction boundary.
- [ ] **C15.01.07** Attempt browser-side position, resource, and completion overrides and verify that no presentation-only value can replace authoritative SQLite state.
- [ ] **C15.01.08** Retain reviewed diagrams, ownership matrices, interface specifications, and boundary-test results; accept only when every consequential record has an unambiguous mutation authority.

### Control C15 02

**Original requirement C15.02:** Define routable identifiers for dossiers, campaigns, assignments, and journals; use stable opaque identifiers and avoid placing private notes or sensitive activity information in URLs.

- [ ] **C15.02.01** Define stable opaque identifiers for campaign, day, dossier revision, assignment, and journal resources, with explicit uniqueness and lifetime rules.
- [ ] **C15.02.02** Document URL path and permitted query fields; prohibit personal reflections, biometric values, credentials, and raw activity detail from route construction.
- [ ] **C15.02.03** Validate identifier syntax and resolve identifiers through service-owned records rather than converting path text directly into filesystem locations.
- [ ] **C15.02.04** Define behavior for unknown, withdrawn, wrong-campaign, and superseded resource identifiers, preserving a safe route back to the current day.
- [ ] **C15.02.05** Ensure copied links identify the intended resource without creating another campaign, rerolling an encounter, or completing a day.
- [ ] **C15.02.06** Test routing with renamed display labels, encoded characters, empty identifiers, long values, and identifiers belonging to another local campaign.
- [ ] **C15.02.07** Inspect address bars, browser history, referrers, diagnostic logs, and exported links for prohibited private field values.
- [ ] **C15.02.08** Retain the routing schema, identifier validation cases, and leakage inspection; accept when stable resource navigation works without private data entering URLs.

### Control C15 03

**Original requirement C15.03:** Publish a browser and device support matrix with exact tested versions, viewport classes, input methods, storage modes, and known limitations; provide an informative unsupported-browser state.

- [ ] **C15.03.01** List each supported browser, exact tested build, Windows version, display class, and input method, with the features assessed for that combination.
- [ ] **C15.03.02** Define required browser capabilities separately from optional cache, audio, download, and presentation features; record a fallback for each optional capability.
- [ ] **C15.03.03** Select representative desktop, tablet, touch, keyboard, and treadmill-viewing configurations and record their actual screen and resource characteristics.
- [ ] **C15.03.04** Implement capability-based startup checks and an informative unsupported state that preserves access to export or existing readable history where feasible.
- [ ] **C15.03.05** Document private-browsing, storage-disabled, enlarged-text, and browser-profile behavior without making browser storage the authoritative persistence requirement.
- [ ] **C15.03.06** Run preparation, recording, decision, debrief, correction, and restart tests on every supported matrix row using the released configuration.
- [ ] **C15.03.07** Exercise a deliberately unsupported or capability-deficient browser and verify intelligible limitations rather than silent missing controls or fabricated saved status.
- [ ] **C15.03.08** Archive the dated compatibility matrix and per-row results; mark support only for tested combinations with resolved defects or explicit reviewed limitations.

### Control C15 04

**Original requirement C15.04:** Define application, API, database, cache, content, and rule-schema versions separately; specify compatible combinations and an explicit incompatible-package response.

- [ ] **C15.04.01** Define distinct application, API, database, content, rule, and presentation-cache version identifiers and identify their authoritative manifests or records.
- [ ] **C15.04.02** Publish a compatibility matrix specifying accepted version ranges, required migrations, optional features, and combinations that permit read-only operation.
- [ ] **C15.04.03** Include relevant protocol and content versions in startup health, dossier responses, mutation requests, and stored operation receipts.
- [ ] **C15.04.04** Reject incompatible mutations before changing state, and display the exact incompatibility without silently replacing an active day's pinned rules.
- [ ] **C15.04.05** Specify cache invalidation and controlled activation when presentation versions change while a session, editor, or consequential choice remains open.
- [ ] **C15.04.06** Test supported current and historical combinations, including a migrated database with an older published dossier and an updated browser bundle.
- [ ] **C15.04.07** Submit newer-schema packages and stale-client operations and verify safe rejection, preserved user data, and an actionable update or recovery path.
- [ ] **C15.04.08** Retain compatibility fixtures, migration decisions, and rejection results; accept only when every deployed version combination has a declared and verified disposition.

### Control C15 05

**Original requirement C15.05:** Specify request/response and error contracts, cancellation, retry limits, idempotency keys, concurrency revisions, and correlation identifiers for consequential operations.

- [ ] **C15.05.01** Specify request and response schemas for each consequential operation, including operation identity, expected revision, canonical units, and required causal references.
- [ ] **C15.05.02** Define distinct validation, conflict, unavailable, committed, and failed outcomes with stable error codes and user-facing recovery actions.
- [ ] **C15.05.03** Bind an idempotency key to its operation type, campaign scope, and payload identity; reject reuse for materially different submitted values.
- [ ] **C15.05.04** Define timeout, bounded retry, cancellation, and operation-status lookup behavior, including cancellation arriving after a successful authoritative commit.
- [ ] **C15.05.05** Include correlation identifiers in safe diagnostics and receipts without copying private notes, credentials, or unnecessary measurement payloads.
- [ ] **C15.05.06** Verify a successful request produces the documented response and exactly one corresponding effective domain change with the expected revision.
- [ ] **C15.05.07** Test malformed payloads, missing revisions, duplicate requests, lost responses, stale revisions, and cancel-after-commit races against documented outcomes.
- [ ] **C15.05.08** Archive the API contract and request-response fixtures; accept when clients can determine whether an action committed without guessing from transport success.

### Control C15 06

**Original requirement C15.06:** Select a local campaign explicitly and maintain its identity in requests; a different browser profile or changed port must load the same repository history rather than creating a new hike silently.

- [ ] **C15.06.01** Define the repository's active campaign selection record and distinguish selecting an existing hike from deliberately creating a new campaign.
- [ ] **C15.06.02** Include the selected campaign identity in dossier, workout, decision, journal, completion, and export requests and validate it server-side.
- [ ] **C15.06.03** Load campaign selection from committed repository state when browser preferences, cookies, or caches are missing or belong to another origin port.
- [ ] **C15.06.04** Require an explicit creation operation for a new hike; an empty browser profile or unrecognized URL cannot initialize replacement history.
- [ ] **C15.06.05** Define switching behavior for unsent reflections, pending choices, and active recordings so another campaign does not inherit their mutations.
- [ ] **C15.06.06** Open the repository through a new browser profile and a changed port and verify identical campaign, day, position, and completion records.
- [ ] **C15.06.07** Test deleted or invalid campaign selections and conflicting tabs; show a recovery selector instead of silently creating or choosing another hike.
- [ ] **C15.06.08** Retain selection-state traces and identity comparisons; accept when repository history remains stable across browser changes and every campaign transition is deliberate.

### Control C15 07

**Original requirement C15.07:** Implement loading, empty, server-unavailable, stale, partial, denied, conflict, and failure states; basic workout recording must not depend on a nonessential gallery or internet access.

- [ ] **C15.07.01** Define view states for loading, empty, partial, stale, denied, conflicting, unavailable-service, and failed operations, with entry and exit conditions.
- [ ] **C15.07.02** Identify which actions remain valid in each state and which require a committed dossier, current revision, or functioning persistence service.
- [ ] **C15.07.03** Provide distinct messages for absent media, incomplete generation, unavailable service, rejected mutation, and an operation whose commit outcome is unknown.
- [ ] **C15.07.04** Keep pause, finish, draft preservation, and status controls available when nonessential gallery, audio, narration, or external lookup fails.
- [ ] **C15.07.05** Prevent optimistic visuals from claiming workout recording or day completion before the corresponding durable receipt is established.
- [ ] **C15.07.06** Exercise each view state using controlled fixtures and verify keyboard focus, accessible status, action availability, and recovery transitions.
- [ ] **C15.07.07** Disable internet and fail individual images while recording a local session; verify that nonessential content never blocks authoritative activity submission.
- [ ] **C15.07.08** Retain the state/action matrix and fault demonstrations; accept when each failure is distinguishable, recoverable, and truthful about what has actually saved.

### Control C15 08

**Original requirement C15.08:** Treat browser storage as optional cache or pending-draft storage and the repository database as authoritative; browser clearing, incognito mode, and cache eviction must not erase committed activity or determine the next leg.

- [ ] **C15.08.01** Inventory browser-stored values and classify each as replaceable asset cache, presentation preference, or explicitly pending draft; exclude authoritative continuation records.
- [ ] **C15.08.02** Document the service queries required to reconstruct campaign, current day, resources, decisions, and workout history after total browser-data removal.
- [ ] **C15.08.03** Namespace caches by repository and content revision so cached assets cannot impersonate another hike or a different published dossier.
- [ ] **C15.08.04** Label retained drafts as pending until the local service commits them; cached text or optimistic state cannot establish completion or progress.
- [ ] **C15.08.05** Handle unavailable browser storage without initializing another campaign or changing committed route position, and document possible loss of unsent drafts.
- [ ] **C15.08.06** Clear browser cache and preferences after a completed and an unfinished day, then reconcile restored views with unchanged SQLite records.
- [ ] **C15.08.07** Repeat with incognito mode, disabled storage, and cache eviction; verify no launch, day, credit, resource, or decision is duplicated.
- [ ] **C15.08.08** Retain before/after database comparisons and reconstruction traces; accept when browser storage can be discarded without altering any committed hike truth.

### Control C15 09

**Original requirement C15.09:** Distinguish unsent input, submitted operation, and database-committed receipt; display saved success only after the local service confirms the authoritative commit.

- [ ] **C15.09.01** Define unsent, submitted, outcome-unknown, rejected, and database-committed states for workout, decision, and journal mutations.
- [ ] **C15.09.02** Specify a committed receipt containing operation identity, campaign/day scope, resulting revision, effective values, and commit status.
- [ ] **C15.09.03** Display save confirmation only after validating the receipt against the submitted operation and the expected local service instance.
- [ ] **C15.09.04** Preserve input during transport failure and query operation status before assuming that a response timeout means the commit failed.
- [ ] **C15.09.05** Reject mismatched receipts, stale-instance responses, and reused operation identifiers with different payloads rather than confirming the wrong action.
- [ ] **C15.09.06** Verify ordinary save, validation rejection, retry, and successful readback through every input form that creates consequential records.
- [ ] **C15.09.07** Interrupt the connection after database commit but before acknowledgement and verify reconciliation displays the existing result without applying another effect.
- [ ] **C15.09.08** Archive receipt schemas and commit-boundary traces; accept when every saved indicator is supported by a matching authoritative commit and effective readback.

### Control C15 10

**Original requirement C15.10:** Detect refused connections, server restarts, disk exhaustion, read-only data directories, and failed writes; preserve unsent values where possible and show actionable recovery without claiming they were saved.

- [ ] **C15.10.01** Define detectable error categories for refused connection, restarted instance, disk exhaustion, read-only storage, database contention, and rejected writes.
- [ ] **C15.10.02** Map each error to record-safety rules, preserved input, retry eligibility, and an actionable user message identifying whether anything committed.
- [ ] **C15.10.03** Retain unsent or outcome-unknown values independently of success banners and provide a private draft export when authoritative saving remains unavailable.
- [ ] **C15.10.04** Disable new consequential commits when the service cannot establish durable storage, while preserving readable committed history and safe session controls.
- [ ] **C15.10.05** After service recovery, obtain current revisions and resolve pending operation outcomes before replaying or reapplying browser input.
- [ ] **C15.10.06** Inject each listed failure during a workout, decision, and reflection save, inspecting visible status and the resulting database records.
- [ ] **C15.10.07** Test a failure after commit separately from failure before commit and verify the interface never loses a successful result or invents a failed save.
- [ ] **C15.10.08** Retain the error/recovery matrix and fault records; accept when no failed write yields false saved status, duplicate effect, or silently advanced leg.

### Control C15 11

**Original requirement C15.11:** Keep activity, decision, and journal persistence independent of replaceable browser media caches; do not discard pending drafts merely to free space for photographs.

- [ ] **C15.11.01** Separate cache-management code and storage quotas for replaceable photographs from pending drafts and durable service-backed activity or journal records.
- [ ] **C15.11.02** Define eviction priority by asset replaceability, current-day relevance, package integrity, and user-selected retention rather than record age alone.
- [ ] **C15.11.03** Prevent media cleanup operations from deleting pending reflections, unacknowledged operation identities, or references needed for save reconciliation.
- [ ] **C15.11.04** Before a user-requested reset, identify unsent input and require an explicit choice about preserving or discarding those drafts.
- [ ] **C15.11.05** Allow missing cached media to reload from approved local artifacts without reconstructing or overwriting campaign and workout state.
- [ ] **C15.11.06** Fill browser cache to its tested limit and request additional imagery while preserving pending notes and a recorded unfinished session.
- [ ] **C15.11.07** Run eviction, cache reset, and low-storage recovery with a lost save acknowledgement; verify pending operation reconciliation remains possible.
- [ ] **C15.11.08** Retain storage-namespace and eviction traces; accept when media pressure can reduce visual fidelity but cannot silently remove consequential user input or committed history.

### Control C15 12

**Original requirement C15.12:** Verify local dossier and asset availability before declaring readiness for use without internet; show missing dependencies and use a labeled substitute when permitted.

- [ ] **C15.12.01** Derive required local assets from the current dossier manifest, distinguishing essential content from optional images, audio, maps, and external references.
- [ ] **C15.12.02** Check file presence, accepted rendition, checksum, version, and permitted use before marking a dossier ready for internet-disconnected operation.
- [ ] **C15.12.03** Display missing dependencies with their effect on the experience and identify permitted fallback content with honest geographic and representation labels.
- [ ] **C15.12.04** Ensure assignment instructions, required decisions, lessons, and journal submission can use local content without mandatory remote requests.
- [ ] **C15.12.05** Retain a coherent published snapshot when an optional external source is unavailable; never substitute invented current conditions for missing information.
- [ ] **C15.12.06** Disable internet before launch and complete a prepared day, confirming local media delivery and authoritative saves through the loopback service.
- [ ] **C15.12.07** Remove essential and optional dependencies separately and verify the declared readiness gate or labeled fallback applies without skipping the hike day.
- [ ] **C15.12.08** Archive package inventories and disconnected test results; accept offline readiness only for the validated manifest and its declared essential dependencies.

### Control C15 13

**Original requirement C15.13:** Retrieve local assets from allowlisted service paths and reject partial or checksum-mismatched snapshots; keep package generation and publication distinct from browser presentation.

- [ ] **C15.13.01** Define approved local asset routes and their mapping to canonical interface, published dossier, and media roots, independent of user-supplied filesystem strings.
- [ ] **C15.13.02** Validate requested asset identity against the dossier manifest and require matching checksum, length, rendition, and publication state where applicable.
- [ ] **C15.13.03** Reject staging artifacts, incomplete transfers, invalid encodings, unexpected content types, and paths that escape the configured served roots.
- [ ] **C15.13.04** Keep generation and publication operations behind service-owned jobs; browser presentation requests must not activate partially generated snapshots.
- [ ] **C15.13.05** Use a known labeled placeholder or approved substitute when an optional asset fails integrity validation, retaining the rejected asset's diagnostic identity.
- [ ] **C15.13.06** Test correct local assets, encoded filenames, approved renditions, and repository relocation against the same manifest references.
- [ ] **C15.13.07** Inject truncated bytes, altered checksums, path traversal, wrong MIME types, and incomplete publication markers and verify rejection before display.
- [ ] **C15.13.08** Retain asset-validation and path-boundary evidence; accept when displayed assets belong to a coherent approved snapshot and invalid files cannot become ready content.

### Control C15 14

**Original requirement C15.14:** Pin application and content revisions for an active view; stale caches must refresh through a controlled transition rather than silently replacing rules during a day.

- [ ] **C15.14.01** Store the active view's application, API, dossier, content-manifest, and rules revisions and identify which revisions are required on consequential requests.
- [ ] **C15.14.02** Specify permitted read-only behavior for old views and the controlled boundary at which new presentation assets or content versions can activate.
- [ ] **C15.14.03** Reject stale incompatible mutations before evaluation and offer a refresh that preserves pending text and explains changed content context.
- [ ] **C15.14.04** Keep a day's pinned narrative, random outcomes, and training-assignment snapshot stable across unrelated publisher or browser-cache updates.
- [ ] **C15.14.05** Apply rights withdrawal and explicit correction policies separately from ordinary cache refresh so prohibited assets are not resurrected by stale views.
- [ ] **C15.14.06** Update the application while a workout, reflection draft, and deferred decision are open and verify controlled version negotiation and preserved state.
- [ ] **C15.14.07** Present an old cached bundle after content or rule migration and verify it cannot apply outdated effects or silently overwrite current day references.
- [ ] **C15.14.08** Archive version-activation traces and stale-view tests; accept when active-day semantics change only through the declared controlled migration or correction path.

### Control C15 15

**Original requirement C15.15:** Restore committed session and editor state through the service after reload, background suspension, tab closure, or server reconnect; identify unobserved physical-activity intervals explicitly.

- [ ] **C15.15.01** Define the authoritative reconstruction response for committed session state, last accepted interval, draft revision, pending encounters, and presentation position.
- [ ] **C15.15.02** Record runtime clock epochs and checkpoints so reload or suspension does not misinterpret wall-clock elapsed time as observed physical activity.
- [ ] **C15.15.03** On reconnect, verify instance identity and obtain current service revisions before enabling consequential forms or restoring active-session ownership.
- [ ] **C15.15.04** Mark unobserved gaps as unknown and permit labeled reconciliation instead of automatically crediting distance or declaring the user stationary.
- [ ] **C15.15.05** Preserve conflicting unsent reflection text and offer a review against the committed version rather than replacing either revision silently.
- [ ] **C15.15.06** Reload in each session and editor state and verify restoration of the same hike day, dossier, decisions, and accepted workout records.
- [ ] **C15.15.07** Suspend the browser and restart the service independently; verify lease recovery, gap classification, and absence of duplicate completion or rerolled encounters.
- [ ] **C15.15.08** Retain reconstruction and interval-accounting traces; accept when committed state survives lifecycle events and unobserved activity remains explicitly unverified.

### Control C15 16

**Original requirement C15.16:** Retry local API operations with stable identifiers, bounded backoff, cancellation, and response reconciliation; a repeated request must return the existing committed result rather than create another workout or decision.

- [ ] **C15.16.01** Assign a stable operation identity before first submission and persist its association with operation type, payload, campaign, and expected base revision.
- [ ] **C15.16.02** Define retry eligibility, maximum attempts or elapsed budget, backoff, cancellation, and operation-status lookup for each mutating endpoint.
- [ ] **C15.16.03** Return a retained existing outcome for identical repeated operations and reject the same identity when reused with materially different content.
- [ ] **C15.16.04** Distinguish database-committed operations from retryable transport failures and conflicts requiring user intervention rather than automatic replay.
- [ ] **C15.16.05** After service restart, reconcile uncertain operations against durable receipts before assigning new identifiers or creating replacement records.
- [ ] **C15.16.06** Retry identical workout, purchase, choice, and complete-day requests and compare unique effective rows and balances with a single-submission baseline.
- [ ] **C15.16.07** Lose acknowledgements, reorder requests, and reuse keys with changed payloads; verify original results, causal ordering, and explicit rejection of incompatible requests.
- [ ] **C15.16.08** Retain retry traces and uniqueness assertions; accept when repeated delivery produces one domain effect and transport uncertainty is never treated as exercise completion.

### Control C15 17

**Original requirement C15.17:** Validate base record and campaign revisions on mutations; conflicting tabs must receive an explicit refresh or resolution path without destructive last-write-wins behavior.

- [ ] **C15.17.01** Define revision fields for mutable records and campaigns and require the client to submit the revision on which each consequential edit was based.
- [ ] **C15.17.02** Specify compare-and-update transaction behavior and a conflict response containing permitted current context without unnecessary private payload disclosure.
- [ ] **C15.17.03** Reject outdated choices, reflection replacements, plan edits, and completion requests before applying their dependent effects or overwriting current values.
- [ ] **C15.17.04** Preserve the user's proposed edit and offer reload, compare, or deliberate reapply operations with fresh prerequisite validation.
- [ ] **C15.17.05** Forbid automatic conflict resolution that chooses larger exercise targets, overwrites established decisions, or discards a reflection through last-write-wins behavior.
- [ ] **C15.17.06** Edit the same record from two tabs and verify one accepted result plus an intelligible conflict, with both proposed texts recoverable where applicable.
- [ ] **C15.17.07** Test a delayed stale submission after correction, policy change, and server restart, confirming no resource, training, or continuation mutation occurs.
- [ ] **C15.17.08** Retain stale-revision fixtures and conflict screenshots; accept when every rejected edit preserves authoritative history and supplies a deliberate recovery path.

### Control C15 18

**Original requirement C15.18:** Define active-session ownership across local tabs and launcher invocations; prevent two views from finalizing the same session independently and recover expired ownership leases.

- [ ] **C15.18.01** Define active-session ownership identifiers, lease duration or equivalent ownership rule, repository scope, renewal, expiration, and takeover conditions.
- [ ] **C15.18.02** Validate stored workout ownership on recording and session finalization; permit eligible explicit day completion after finalization or on preparation days without an active workout lease.
- [ ] **C15.18.03** Make repeated launcher invocations attach to the existing owned service and unfinished session instead of allocating competing recordings.
- [ ] **C15.18.04** Recover expired or abandoned ownership deliberately while classifying unobserved activity gaps and preserving accepted session intervals.
- [ ] **C15.18.05** Enforce one effective finalization result per session independently of lease transitions so old tabs cannot finish a record again.
- [ ] **C15.18.06** Open concurrent tabs and launchers, attempt simultaneous start and finish, and verify one authoritative session owner and one effective workout record.
- [ ] **C15.18.07** Simulate crashed owner, expired lease, delayed renewal, and stale finalization after takeover, verifying correct denial or deliberate recovery.
- [ ] **C15.18.08** Archive ownership-state traces and concurrency results; accept when ownership recovery restores access without duplicate recording, completion, or invented activity.

### Control C15 19

**Original requirement C15.19:** Export and restore history from authoritative local-service records; test a new browser profile, changed port, and relocated repository while preserving the same campaign identity.

- [ ] **C15.19.01** Define an export manifest covering authoritative records, schema versions, units, provenance, campaign identity, and required dossier references.
- [ ] **C15.19.02** Obtain a consistent service-owned snapshot for export rather than mixing browser cache and live records from incompatible revisions.
- [ ] **C15.19.03** Respect media redistribution permissions and identify omitted assets or local dependencies without implying a completely self-contained export when it is incomplete.
- [ ] **C15.19.04** Validate imports/restoration against supported schema and unique identities, preview conflicts, and preserve existing history before accepting replacement.
- [ ] **C15.19.05** Resolve repository-relative artifact references after relocation and reconstruct browser views from the restored database rather than exported display totals.
- [ ] **C15.19.06** Restore into a clean repository and browser profile, comparing campaigns, completed days, current position, workouts, decisions, and private reflections.
- [ ] **C15.19.07** Change port, move the repository, remove optional images, and retry the same restore; verify identities remain stable and duplicate effects are rejected.
- [ ] **C15.19.08** Retain export manifests and restoration reconciliation; accept when supported history round-trips without silent omissions, duplicated records, or changed next-leg position.

### Control C15 20

**Original requirement C15.20:** Map applicable WCAG 2.2 AA criteria to interface tests, including keyboard operation, focus, status messages, contrast, text resizing, and non-color distinctions; retain manual assessment evidence.

- [ ] **C15.20.01** Inventory preparation, workout, decision, debrief, correction, and export screens and map applicable accessibility criteria to their components and interaction states.
- [ ] **C15.20.02** Define assessment methods, supported assistive technologies, evidence requirements, severity, and the reviewer responsible for each selected criterion.
- [ ] **C15.20.03** Implement semantic controls, accessible names, focus order, status announcements, contrast, text resizing, and distinctions that do not depend solely on color.
- [ ] **C15.20.04** Specify focus restoration and announcement behavior for dynamic content, failed saves, modal transitions, deferred choices, and route changes.
- [ ] **C15.20.05** Provide a documented exception/applicability rationale where a criterion does not apply; an untested screen cannot be treated as conformant.
- [ ] **C15.20.06** Run manual keyboard and screen-reader journeys alongside automated checks on all essential screen states and record observable failures.
- [ ] **C15.20.07** Test high text magnification, missing images, reduced motion, errors, and unexpected service loss while preserving essential task completion.
- [ ] **C15.20.08** Archive criterion-level assessment and resolved defect evidence; accept the declared accessibility target only for the tested release and supported workflows.

### Control C15 21

**Original requirement C15.21:** Provide accessible equivalents for map, elevation, calendar, chart, and drag interactions; essential tasks must remain possible without interpreting images or using precise pointing.

- [ ] **C15.21.01** Identify every map, profile, calendar, chart, and drag interaction and the task or information it provides to the user.
- [ ] **C15.21.02** Define an equivalent text, table, list, or form representation containing the same quantities, selections, order, and actionable options.
- [ ] **C15.21.03** Implement keyboard-operable selection and editing so no essential operation requires pointer precision, dragging, hover, or visual geography interpretation.
- [ ] **C15.21.04** Keep equivalent views synchronized with the same authoritative records and filters rather than independently maintained approximations.
- [ ] **C15.21.05** Provide understandable labels and units for map locations, elevation ranges, scheduled assignments, and chart summaries in the nonvisual representation.
- [ ] **C15.21.06** Complete each represented task using only its equivalent view and verify identical saved outcomes and selected campaign context.
- [ ] **C15.21.07** Change filters, revise source records, remove imagery, and enlarge text; verify the visual and equivalent results continue to agree.
- [ ] **C15.21.08** Retain task-equivalence and data-parity evidence; accept when all essential graphical tasks are independently usable through accessible semantic alternatives.

### Control C15 22

**Original requirement C15.22:** Support reduced motion, captions, text size, optional audio, and deferred decisions; avoid modal or timed story interactions that interrupt workout controls.

- [ ] **C15.22.01** Define user preferences for motion, text size, captions, audio, narration frequency, and decision timing, with stable defaults and scope.
- [ ] **C15.22.02** Identify animated, automatically playing, timed, or modal content that could interfere with workout controls or comprehension.
- [ ] **C15.22.03** Implement reduced-motion and audio alternatives without hiding required information, removing choices, or changing the physical assignment.
- [ ] **C15.22.04** Allow consequential decisions to remain pending until deliberate engagement, preserving their eligibility and avoiding penalties solely for deferral.
- [ ] **C15.22.05** Keep pause and finish controls reachable while presentation preferences change or a story panel opens; avoid modal focus traps.
- [ ] **C15.22.06** Complete a dossier in reduced-motion, silent, captioned, and enlarged-text configurations and verify identical domain effects.
- [ ] **C15.22.07** Trigger an encounter during an active recording, defer it, reload, and resume; verify no forced response window or unauthorized workout extension.
- [ ] **C15.22.08** Retain preference, interaction-timing, and walking-use results; accept when comfort settings preserve every essential task and physical-training boundary.

### Control C15 23

**Original requirement C15.23:** Test layouts at the supported widths and magnifications, including long labels, missing images, translated text, onscreen keyboards, and touch input; prevent controls from moving unexpectedly as media loads.

- [ ] **C15.23.01** Define supported viewport and magnification classes, text-length extremes, orientation changes, and input modes in the layout test matrix.
- [ ] **C15.23.02** Reserve stable geometry for photographs, captions, asynchronous errors, and essential workout controls before their content arrives.
- [ ] **C15.23.03** Use reflow and wrapping rules that preserve labels, units, buttons, and visible focus without clipping required actions.
- [ ] **C15.23.04** Account for onscreen keyboards, long translated labels, browser zoom, missing media, and variable-height source or explanation text.
- [ ] **C15.23.05** Define acceptable controlled layout transitions and prevent image loading or status updates from moving an action underneath a user's pointer.
- [ ] **C15.23.06** Inspect every essential view at matrix extremes with real longest-case content, recording screenshots and task completion results.
- [ ] **C15.23.07** Load delayed media while interacting, open the onscreen keyboard, and rotate supported devices; verify no accidental action or hidden recovery control.
- [ ] **C15.23.08** Retain responsive-layout captures and interaction tests; accept when supported combinations have no overlapping, clipped, displaced, or unreachable essential content.

### Control C15 24

**Original requirement C15.24:** Establish and measure budgets for initial dossier display, workout responsiveness, image bytes, memory growth, local API latency, and long-session stability on reference devices.

- [ ] **C15.24.01** Specify measurable budgets for dossier readiness, input response, API latency, image transfer size, memory growth, and sustained session behavior.
- [ ] **C15.24.02** Record reference machine, browser build, repository size, content manifest, cold/warm cache conditions, and measurement method for each budget.
- [ ] **C15.24.03** Instrument relevant phases without collecting private reflections or unnecessary activity details, and separate service processing from presentation delays.
- [ ] **C15.24.04** Define workload fixtures covering media-heavy days, large histories, concurrent views, journal editing, and background generation.
- [ ] **C15.24.05** Specify graceful quality reduction and actionable status when optional presentation exceeds budget, preserving recording and commit integrity.
- [ ] **C15.24.06** Measure repeated cold and warm launches and long sessions on reference configurations against the approved budgets and aggregation method.
- [ ] **C15.24.07** Stress memory, slow disk, large images, and local request contention; verify stable controls, bounded resource use, and truthful save behavior.
- [ ] **C15.24.08** Archive reproducible measurement traces and budget comparisons; accept only when selected limits pass or reviewed limitations specify the affected configuration.

### Control C15 25

**Original requirement C15.25:** Sanitize rich content, reject arbitrary scripts and unsafe links, apply an appropriate content security policy, and validate imported package formats before exposing them to the interface.

- [ ] **C15.25.01** Inventory rich-text, Markdown, image, package, and link ingestion paths and define permitted content syntax and trusted publication boundaries.
- [ ] **C15.25.02** Specify allowlisted elements, attributes, URL schemes, content types, and package fields; reject arbitrary script and executable rule payloads.
- [ ] **C15.25.03** Sanitize at ingestion and rendering boundaries and apply a content policy matching the approved local assets and optional external resources.
- [ ] **C15.25.04** Validate package structure, sizes, checksums, and dependencies before activation; do not treat a valid filename extension as format validation.
- [ ] **C15.25.05** Keep rejected content quarantined or unavailable with attributable diagnostics, preventing it from reaching active dossiers or private-record endpoints.
- [ ] **C15.25.06** Render approved rich content and supported packages and verify captions, links, accessible structure, and the intended local resource permissions.
- [ ] **C15.25.07** Inject script tags, event handlers, unsafe schemes, malformed packages, and oversized inputs and verify rejection without mutation or credential disclosure.
- [ ] **C15.25.08** Retain sanitizer policy and hostile-content fixtures; accept when all ingestion paths enforce the same approved execution and publication boundaries.

### Control C15 26

**Original requirement C15.26:** Keep secrets, private configuration, runtime markers, backups, and database files outside publicly served paths; use scoped permissions for optional external integrations.

- [ ] **C15.26.01** Inventory sensitive repository files, including SQLite state, journals, local configuration, tokens, runtime markers, diagnostics, backups, and private exports.
- [ ] **C15.26.02** Define explicit served roots and file-class access rules; default-deny paths outside approved interface, dossier, and media catalogs.
- [ ] **C15.26.03** Store optional integration secrets outside client-delivered bundles and expose only the minimum derived configuration required by the interface.
- [ ] **C15.26.04** Scope external integration permissions to enabled operations and document storage, rotation, revocation, and diagnostic-redaction behavior.
- [ ] **C15.26.05** Inspect generated dossiers, source maps, manifests, and build artifacts for accidental copying of private configuration or credential values.
- [ ] **C15.26.06** Verify approved assets remain reachable through the configured local service while sensitive files return the declared denial response.
- [ ] **C15.26.07** Attempt direct, encoded, traversal, and alternate-case requests for database, backup, marker, and secret files, including paths through reparse points.
- [ ] **C15.26.08** Retain served-root inventories and denial tests; accept when browser-delivered content contains no secrets and private repository files remain outside serving authority.

### Control C15 27

**Original requirement C15.27:** Restrict mutations to the intended local instance and selected campaign, with validated request tokens and origin policy; another website or stale tab must not commit arbitrary local history changes.

- [ ] **C15.27.01** Define intended local instance, repository, campaign, and request-origin identity for each mutating endpoint and record token lifecycle rules.
- [ ] **C15.27.02** Validate request tokens, accepted origins, campaign ownership, expected revision, and endpoint permission before interpreting mutation payloads.
- [ ] **C15.27.03** Refuse arbitrary cross-origin state changes and do not grant wildcard origin access to private records or mutating operations.
- [ ] **C15.27.04** Expire or deliberately reconcile tokens after service replacement so an old tab cannot send consequential requests to the wrong instance.
- [ ] **C15.27.05** Keep token acquisition scoped to the served local interface and prevent tokens from appearing in URLs, exported journals, or ordinary logs.
- [ ] **C15.27.06** Verify intended local pages can save each operation and receive attributable commit receipts for the selected campaign.
- [ ] **C15.27.07** Submit foreign-origin, missing-token, wrong-instance, wrong-campaign, and stale-revision requests and confirm no database effects or disclosed private payloads.
- [ ] **C15.27.08** Archive the instance/origin policy and mutation-denial matrix; accept when only valid intended-view requests can commit local hike history changes.

### Control C15 28

**Original requirement C15.28:** Select applicable session, authentication, cross-site request, input-validation, upload, transport, and dependency controls using a documented security baseline; record applicability and verification instead of claiming certification.

- [ ] **C15.28.01** Define the enabled local deployment and optional integrations before selecting applicable security baseline controls and documenting excluded functions.
- [ ] **C15.28.02** Map input validation, session state, cross-site mutation, upload, transport, credential, authorization, and dependency concerns to owned verification activities.
- [ ] **C15.28.03** Record the baseline edition, selected requirement identifiers, applicability reasoning, implementation references, and evidence needed for each assessment.
- [ ] **C15.28.04** Implement selected controls at service boundaries rather than relying solely on hidden interface actions or assumed loopback trust.
- [ ] **C15.28.05** Distinguish application verification from third-party certification and prohibit unsupported assurance claims in release notes or product wording.
- [ ] **C15.28.06** Run the approved security verification plan against the released configuration and retain reproducible findings and severity dispositions.
- [ ] **C15.28.07** Retest material findings after fixes and exercise misuse cases for local origins, private files, imported content, stale requests, and optional secrets.
- [ ] **C15.28.08** Accept the baseline review only when every applicable requirement has evidence or an owned time-bounded exception, with claims limited to assessed scope.

### Control C15 29

**Original requirement C15.29:** Inventory network destinations and tracking behavior; request only needed permissions and keep optional analytics separate from required user activity records.

- [ ] **C15.29.01** Inventory local and optional remote network destinations, initiating features, transmitted fields, frequency, purpose, and configuration switches.
- [ ] **C15.29.02** Separate required loopback requests from external content retrieval, integrations, diagnostics, and optional product analytics.
- [ ] **C15.29.03** Require only permissions needed by enabled features and explain optional grants without blocking the core local training and dossier flow.
- [ ] **C15.29.04** Keep user activity records authoritative regardless of whether analytics collection is disabled, rejected, interrupted, or removed.
- [ ] **C15.29.05** Define failure and revocation behavior for optional destinations and prevent fallback requests from sending private notes or additional identifiers.
- [ ] **C15.29.06** Observe network traffic during core operation with all optional services disabled and confirm expected loopback-only behavior.
- [ ] **C15.29.07** Enable and revoke each optional feature, comparing captured payloads and destinations with the inventory and checking continued local functionality.
- [ ] **C15.29.08** Retain destination/payload review and permission tests; accept when every network request is attributable to an enabled purpose and disclosed data scope.

### Control C15 30

**Original requirement C15.30:** Redact private reflections, biometric fields, secrets, and unnecessary identifiers from diagnostics; provide user-controlled support exports with a visible content description.

- [ ] **C15.30.01** Classify diagnostic fields and define prohibited values for private reflections, biometric detail, tokens, secrets, and unnecessary persistent identifiers.
- [ ] **C15.30.02** Specify safe correlation fields sufficient to trace run, operation, generation, and error outcomes without copying entire request or record payloads.
- [ ] **C15.30.03** Apply redaction before diagnostic persistence, console display, crash capture, and support-bundle assembly rather than only during final export.
- [ ] **C15.30.04** Let the user inspect the support bundle's categories, relevant period, and included files before deliberately producing an external copy.
- [ ] **C15.30.05** Define retention, local path, permissions, and deletion behavior for diagnostic bundles separately from authoritative hike history.
- [ ] **C15.30.06** Generate failures containing known marker values in notes, biometric fields, and secrets and search all produced diagnostic surfaces for leakage.
- [ ] **C15.30.07** Verify retained correlation still reconstructs the failed operation and commit outcome after prohibited fields are removed.
- [ ] **C15.30.08** Archive redaction fixtures and bundle inspections; accept when diagnostics remain useful for recovery without exposing prohibited data or undisclosed files.

### Control C15 31

**Original requirement C15.31:** Define campaign switching, local deletion, shared-computer behavior, and cached-private-data cleanup where supported; avoid silently exposing a different participant's records through a reused browser view.

- [ ] **C15.31.01** Define supported local profiles and campaign selection boundaries, including what remains visible when changing participants on a shared computer.
- [ ] **C15.31.02** Specify treatment of open forms, pending reflections, active sessions, cached responses, presentation preferences, and export locations during switching.
- [ ] **C15.31.03** Invalidate view-specific access or state on a switch and load the new campaign through service validation instead of reusing prior private responses.
- [ ] **C15.31.04** Provide an explicit deletion workflow identifying affected records, generated private artifacts, backups, and remaining copies outside application control.
- [ ] **C15.31.05** Do not promise protection from the underlying Windows account beyond the documented filesystem and application boundaries.
- [ ] **C15.31.06** Switch campaigns with notes, gallery, dashboards, and deferred decisions open and verify no previous participant data appears in the resulting views.
- [ ] **C15.31.07** Test browser-back navigation, stale tabs, deleted campaigns, cached responses, and unsent drafts after switching or cleanup.
- [ ] **C15.31.08** Retain shared-use and deletion evidence; accept when supported switching and cleanup are deliberate, scoped, and free of silent cross-participant disclosure.

### Control C15 32

**Original requirement C15.32:** Run preparation, workout completion, deferred choice, camp debrief, correction, export, and recovery from the CMD launch path using repository-local state and internet-disconnected operation.

- [ ] **C15.32.01** Prepare a reference repository with known route, content, campaign, assignments, expected resources, and no reliance on internet-connected services.
- [ ] **C15.32.02** Launch through the shipped CMD entry point and verify PowerShell orchestration, owned instance, correct loopback origin, and selected saved day.
- [ ] **C15.32.03** Complete preparation and a labeled actual workout, confirming one committed activity record and the disclosed progression conversion.
- [ ] **C15.32.04** Defer then resolve a consequential encounter and reconcile its resource, character, and journal effects against the selected branch.
- [ ] **C15.32.05** Finish the day deliberately, restart the application, and verify the committed next leg and the preserved completed dossier.
- [ ] **C15.32.06** Correct recorded activity and export the resulting history, checking updated summaries, causal links, units, privacy, and correction annotations.
- [ ] **C15.32.07** Repeat the journey after browser cache removal and a service interruption with internet disabled, preserving unfinished-day state and unknown activity gaps.
- [ ] **C15.32.08** Retain end-to-end screenshots, request receipts, and database reconciliation; accept when the entire shipped local journey matches expected state without duplicated effects.

### Control C15 33

**Original requirement C15.33:** Inject local-server loss, partial snapshots, denied writes, disk exhaustion, invalid request tokens, stale revisions, repeated submissions, and incompatible updates; inspect both records and user-visible messages.

- [ ] **C15.33.01** Define fault points for local connection loss, partial snapshots, denied writes, disk exhaustion, invalid tokens, stale revisions, duplicates, and incompatible versions.
- [ ] **C15.33.02** For each fault, record initial database state, pending operation, injected failure boundary, expected response, and permitted recovery behavior.
- [ ] **C15.33.03** Inject faults during recording, decision submission, journal editing, publication, and complete-day rather than testing startup errors alone.
- [ ] **C15.33.04** Observe browser status and preserve unsent or outcome-unknown input without displaying unsupported saved or completed confirmations.
- [ ] **C15.33.05** Reconcile actual rows, receipts, balances, publication state, and next-leg pointer immediately after failure and again after recovery.
- [ ] **C15.33.06** Verify faults before commit leave no effect while lost responses after commit recover the existing effect through idempotent reconciliation.
- [ ] **C15.33.07** Test combinations such as stale tab after restart and disk failure during publication, ensuring safeguards do not mask another unresolved error.
- [ ] **C15.33.08** Archive the fault matrix, traces, and invariant assertions; accept when every listed failure has a truthful interface result and a verified noncorrupting recovery.

### Control C15 34

**Original requirement C15.34:** Test migration using populated historical databases and old content manifests; preserve referential integrity and define a rollback or forward-repair procedure that does not destroy new user activity.

- [ ] **C15.34.01** Collect populated historical database and content fixtures covering completed days, unfinished generation, old policies, corrections, and private reflections.
- [ ] **C15.34.02** Define migration prerequisites, supported source versions, backup requirements, transaction boundaries, and application/content compatibility after upgrade.
- [ ] **C15.34.03** Preserve stable identities, foreign-key relationships, immutable history, units, progression provenance, and pinned dossier references during migration.
- [ ] **C15.34.04** Specify safe rollback or forward repair, including how activity committed after upgrade remains protected rather than overwritten by a stale backup.
- [ ] **C15.34.05** Reject newer unsupported schemas and incomplete migrations before accepting browser mutations; provide an actionable recovery path.
- [ ] **C15.34.06** Migrate each historical fixture and independently reconcile counts, canonical values, current day, completed endpoints, credits, and narrative history.
- [ ] **C15.34.07** Interrupt at migration boundaries and then repair or restore, comparing new user records and generated snapshot references with expected preservation rules.
- [ ] **C15.34.08** Retain migration and repair reports; accept when supported historical states upgrade reproducibly and no chosen recovery path silently destroys newer activity.

### Control C15 35

**Original requirement C15.35:** Record dependency inventory, vulnerability review, build provenance, deployed configuration, support limitations, and release evidence; prevent unreviewed runtime dependencies from entering production packages.

- [ ] **C15.35.01** Inventory direct and transitive runtime dependencies with exact versions, origin, integrity identifiers, license disposition, and their deployed purpose.
- [ ] **C15.35.02** Record build inputs, source revision, configuration schema, packaging steps, content manifest, and output checksums for the candidate release.
- [ ] **C15.35.03** Review known vulnerabilities and integrity defects against actual usage, retaining severity, applicability, remediation, or a bounded exception decision.
- [ ] **C15.35.04** Prevent undeclared runtime downloads or unreviewed packages from entering the release without an attributable dependency and configuration change.
- [ ] **C15.35.05** Publish supported platforms, operational limitations, compatibility, migration requirements, and evidence references without overstating tested behavior.
- [ ] **C15.35.06** Rebuild the candidate from recorded inputs and compare attributable outputs, manifests, and dependency inventory with the release package.
- [ ] **C15.35.07** Introduce an undeclared dependency or altered package and verify release checks detect the change before acceptance or distribution.
- [ ] **C15.35.08** Archive provenance, dependency review, reproducible-build results, and release disposition; accept only the identified package and configuration covered by that evidence.

## C16 Content administration and quality controls

**Accountable owners:** Content program owner for governance; domain owners for geography, media, narrative, learning, and training references; release owner for bundle publication; rights/security/accessibility reviewers where applicable.

**Interfaces:** Coordinates all content-producing components through repository-local SQLite records, content identifiers, evidence, approvals, dependency graphs, local path manifests, correction reports, and audit events. Packages dossiers for the service started by a `.cmd` launcher invoking PowerShell and serving `http://127.0.0.1:<port>`. It publishes content packages; it does not command equipment or create exercise prescriptions.

**Required evidence:** Responsibility register; SQLite/content schemas; repository path conventions; content/evidence inventory; approvals; impact report; validation results; source-update policy; separate operational/day logs; local release manifest; relaunch/completion/withdrawal/rollback/restoration rehearsal.

**Exit criterion:** Repository-local content is traceable, approved, reproducible from its manifest, and recoverable without corrupting SQLite training/day/campaign state. Relaunch resumes unfinished work; explicit completion alone advances next-leg. The local service requires no cloud/account or browser-authoritative storage and exposes only approved content paths. Blocking failures are resolved; accepted limitations have an owner and disposition.

### Control C16 01

**Original requirement C16.01:** Maintain a responsibility register for authoring, geographic validation, narrative review, instructional review, rights, accessibility, publication, correction, withdrawal, and escalation.

- [ ] **C16.01.01** Create a responsibility register covering authoring, geographic validation, narrative/instructional review, rights, accessibility, publication, correction, withdrawal, escalation, and substitutes for unavailable accountable owners.
- [ ] **C16.01.02** Specify each role's authority, approval artifacts, review scope, escalation triggers, and handoff obligations; document combined roles without implying independent review where none exists.
- [ ] **C16.01.03** Assign named accountable owners and reviewers to every released content family; unassigned responsibilities must block the relevant approval or publication transition.
- [ ] **C16.01.04** Define urgent factual/rights correction routing with response targets and fallback ownership; an absent primary reviewer cannot leave prohibited current content indefinitely deliverable.
- [ ] **C16.01.05** Walk a sample route/media/lesson release through actual handoffs; verify each required decision has an attributable owner, exact revision, evidence reference, and dated disposition.
- [ ] **C16.01.06** Simulate unavailable owners and ambiguous shared responsibility; confirm fallback/escalation routing produces an explicit decision rather than bypassing review or silently approving pending content.
- [ ] **C16.01.07** Change role assignments during active review and inspect authorization updates; preserve prior attributable approvals and prevent former owners from executing newly unauthorized publication actions.
- [ ] **C16.01.08** Archive the register, workflow rehearsal, and authority review; accept only when every required responsibility has an accountable actor and every escalation path is actionable.

### Control C16 02

**Original requirement C16.02:** Inventory each item in authoritative local SQLite with identifier, type, owner, version, state, dependencies, repository-relative file references, review deadline, and withdrawal status; cloud accounts are not required.

- [ ] **C16.02.01** Define SQLite content inventory fields for stable identifier, type, owner, immutable/mutable version semantics, lifecycle state, dependencies, safe relative file references, deadlines, and withdrawal status.
- [ ] **C16.02.02** Specify inventory uniqueness, foreign keys, publication eligibility, and allowed updates; distinguish missing files, absent metadata, drafts, approved items, and withdrawn-but-retained historical references.
- [ ] **C16.02.03** Register imported and authored items through validated local operations; authoritative inventory and review workflows must function without cloud accounts or external service availability.
- [ ] **C16.02.04** Validate repository-relative paths beneath approved content/media roots; inventory records cannot authorize serving private database, logs, credentials, or files escaping configured publication boundaries.
- [ ] **C16.02.05** Reconcile a released manifest against the inventory and physical files; require every listed dependency to resolve to the correct version, ownership, state, and checksum.
- [ ] **C16.02.06** Exercise orphaned dependencies, duplicate IDs, missing files, overdue review fields, and contradictory withdrawal flags; block affected publication and identify responsible remediation owners.
- [ ] **C16.02.07** Restart or relocate the repository and reload inventory; verify committed content ownership, dependency lineage, deadlines, and withdrawal state remain intact independent of browser cache.
- [ ] **C16.02.08** Archive inventory/schema and file reconciliation results; accept only when all published content is locally inventoried, safely referenced, and traceable to effective review/publication status.

### Control C16 03

**Original requirement C16.03:** Maintain an evidence registry recording sources, publishers, dates, acquisition, applicability, confidence, licensing, and the specific assertions supported.

- [ ] **C16.03.01** Define evidence registry entries for source identity, publisher, publication/acquisition dates, retrieval context, applicability, confidence, licensing, archived reference, and supported assertion IDs.
- [ ] **C16.03.02** Map evidence to specific assertions rather than whole dossiers alone; record which geographic, instructional, temporal, or rights claim each retained source actually supports.
- [ ] **C16.03.03** Specify assessment rules for contradictory, dated, incomplete, retired, and indirectly interpreted evidence; confidence and applicability require reviewer reasoning rather than automatic source-count scoring.
- [ ] **C16.03.04** Preserve original acquisition details and adaptation rationale; replacing source references must create new evidence revisions with explicit relationships to prior published assertion support.
- [ ] **C16.03.05** Trace a representative dossier's factual assertions through the registry; independently inspect whether each source supports the expressed claim, scope, date, and level of certainty.
- [ ] **C16.03.06** Seed missing assertion mappings, license ambiguity, conflicting dates, and broken references; require review/blocking disposition before affected claims enter a newly approved release.
- [ ] **C16.03.07** Correct a source or withdraw unsupported evidence; calculate affected content and campaign dependencies and apply explicit correction/withdrawal while preserving historical review and acquisition records.
- [ ] **C16.03.08** Archive assertion coverage and evidence-review decisions; accept only when every released factual claim has applicable traceable support and every uncertain source has a documented disposition.

### Control C16 04

**Original requirement C16.04:** Use versioned schemas and controlled vocabularies for route associations, representation labels, event effects, rights, approval states, and source freshness.

- [ ] **C16.04.01** Publish versioned schemas and controlled vocabularies for route associations, representation classes, typed event effects, rights/use channels, approval states, and source-freshness classifications.
- [ ] **C16.04.02** Define stable vocabulary identifiers, meanings, valid transitions/combinations, aliases, deprecation rules, and compatibility matrices; display-label edits must not silently change semantic identities.
- [ ] **C16.04.03** Apply shared validation during import, authoring, package generation, and service loading; reject unknown types or incompatible versions before their content can affect campaigns.
- [ ] **C16.04.04** Specify migration mappings and reviewer responsibilities for renamed/deprecated terms; preserve pinned historical values and audit any prospective changes to catalog records.
- [ ] **C16.04.05** Round-trip representative records for every vocabulary through SQLite and manifest serialization; verify semantic values and unknown/null distinctions survive locale and display-label changes.
- [ ] **C16.04.06** Exercise forbidden state/effect combinations, obsolete identifiers, malformed route associations, and unsupported freshness codes; detect violations with precise record/field messages rather than default guesses.
- [ ] **C16.04.07** Interrupt vocabulary/schema migration and restart; retain a coherent supported catalog and block mixed-version publication until all dependent records pass the selected migration policy.
- [ ] **C16.04.08** Archive vocabulary registers, compatibility fixtures, and migration review; accept only when all released values belong to approved versions and deprecated meanings remain historically interpretable.

### Control C16 05

**Original requirement C16.05:** Maintain a dependency graph covering dossiers, stages, media, events, lessons, templates, offline packages, exports, and campaign snapshots.

- [ ] **C16.05.01** Model directed version-specific dependency edges linking dossiers, stages, media, events, lessons, templates, local packages, exports, and campaign snapshots with relationship type and ownership.
- [ ] **C16.05.02** Specify immutable historical edges separately from current-release selection pointers; completed snapshots retain their original dependency identities even when catalogs adopt newer content.
- [ ] **C16.05.03** Maintain reverse indexes and validate missing nodes, incompatible versions, invalid cycles, and required-dependency closure before publication, correction, withdrawal, or export operations.
- [ ] **C16.05.04** Define graph traversal rules for impact analysis, rights propagation, package completeness, and historical annotations; identify boundaries where independent exports cannot be recalled by the application.
- [ ] **C16.05.05** Construct a sample shared asset used by multiple dossiers and exports; independently enumerate expected dependents and compare the impact query's complete returned set.
- [ ] **C16.05.06** Seed orphan nodes, hidden transitive dependencies, cycles, and mismatched campaign snapshots; require accurate detection and blocking disposition for structurally invalid publication graphs.
- [ ] **C16.05.07** Interrupt graph updates during content publication and restart; reconcile committed manifests and edges so partial relationship changes cannot hide affected campaigns or orphan published files.
- [ ] **C16.05.08** Archive graph validation and transitive-impact results; accept only when every release/package has complete dependency closure and every affected-content query matches independently expected dependencies.

### Control C16 06

**Original requirement C16.06:** Produce immutable local release manifests with compatible application/SQLite schema versions, validated package paths, checksums, coverage, attribution, limitations, and predecessor/replacement relationships.

- [ ] **C16.06.01** Define immutable release manifests with publication identity, application/SQLite schema compatibility, validated package paths, dependency checksums, coverage, attribution, limitations, and predecessor/replacement references.
- [ ] **C16.06.02** Specify required dependency closure and manifest-signing or attributable-approval method appropriate to the local deployment; checksum integrity does not substitute for editorial approval evidence.
- [ ] **C16.06.03** Validate every path and actual file checksum against the staged package before final publication; prohibit absolute/escaping references and untracked mutable latest-version dependencies.
- [ ] **C16.06.04** Store manifest identity and ready/publication references durably while retaining predecessor lineage; never overwrite published manifests under unchanged release identity or silently repoint historical snapshots.
- [ ] **C16.06.05** Load a candidate release using supported and unsupported application/schema combinations; verify compatible content works and incompatible manifests fail with actionable upgrade/rollback information.
- [ ] **C16.06.06** Corrupt files, remove dependencies, alter attribution, and create replacement cycles; require validation to reject each inconsistent manifest/package before current-release selection changes.
- [ ] **C16.06.07** Interrupt manifest/file publication and recover through explicit reconciliation; preserve the prior coherent release pointer until a completely validated replacement is ready.
- [ ] **C16.06.08** Archive compatibility, path, checksum, and lineage results; accept only when every selected release is immutable, internally complete, and matched to the exact validated local package.

### Control C16 07

**Original requirement C16.07:** Implement controlled authoring, review, approval, publication, correction, withdrawal, and archive transitions; record actor/reason/version/time locally, separating launcher diagnostics from authoritative hike-day completion logs.

- [ ] **C16.07.01** Define controlled transitions for authoring, review, approval, publication, correction, withdrawal, and archive with required actor authority, evidence, reason, time, and expected revision.
- [ ] **C16.07.02** Implement locally durable audit events identifying content ID/version, old/new state, acting role, decision reason, review reference, and operation receipt for every effective transition.
- [ ] **C16.07.03** Separate content lifecycle audits from launcher diagnostics and authoritative day-completion records; publication activity cannot be interpreted as workout performance or route advancement.
- [ ] **C16.07.04** Require approved transition gates for corrections and withdrawals affecting pinned snapshots; historical content remains immutable except through explicit, traceable annotation/substitution/removal workflows.
- [ ] **C16.07.05** Execute each legal transition on representative route, media, lesson, and dossier content; inspect state, revision, actor, prerequisites, and audit lineage against the lifecycle specification.
- [ ] **C16.07.06** Attempt unauthorized publication, direct approval bypass, missing reasons, and stale edits; reject each request with no partial transition or misleading successful audit event.
- [ ] **C16.07.07** Lose transition acknowledgments and restart during commits; deduplicate retries and reconcile one effective lifecycle event without changing saved hike-day completion or next-leg state.
- [ ] **C16.07.08** Archive transition/authority and audit-separation evidence; accept only when every effective lifecycle change is attributable and no operational/content log substitutes for an explicit completed-day record.

### Control C16 08

**Original requirement C16.08:** Specify factual, geographic, instructional, narrative, rights, accessibility, and technical review criteria; require specialized review when the content warrants it.

- [ ] **C16.08.01** Specify review criteria and required evidence for factual, geographic, instructional, narrative, rights, accessibility, and technical content, including conditions demanding specialized reviewer involvement.
- [ ] **C16.08.02** Define applicability by content type and claim severity; a media grant review cannot serve as geographic validation or approve unreviewed physical training guidance.
- [ ] **C16.08.03** Create review forms recording exact revision, inspected assertions/assets, criteria outcomes, limitations, defects, reviewer scope, decision, and date with explicit blocking-severity rules.
- [ ] **C16.08.04** Assign appropriate review before publication and record combined roles where necessary; escalation must identify when available expertise is insufficient for the supplied content.
- [ ] **C16.08.05** Apply the review criteria to representative maps, photographs, scenarios, lessons, templates, and assignments; verify all required specialist domains receive attributable dispositions.
- [ ] **C16.08.06** Seed misleading imagery, unsupported lessons, narrative contradictions, expired permission, inaccessible controls, and unsafe technical references; confirm corresponding reviewers identify and block material defects.
- [ ] **C16.08.07** Revise content after review and inspect review invalidation rules; changed claims or dependencies require targeted rereview rather than automatic reuse of superseded approvals.
- [ ] **C16.08.08** Archive criteria, reviewer-scope records, and inspected samples; accept only when all applicable review domains pass and any expertise limitations have explicitly bounded release decisions.

### Control C16 09

**Original requirement C16.09:** Automate schema, link, evidence, credit, dependency, route-reference, unit, unreachable-event, and unresolved-placeholder checks; classify blocking failures and documented exceptions.

- [ ] **C16.09.01** Inventory automated checks for schema, links, evidence references, credits, dependencies, route positions, units, event reachability, and unresolved placeholders with versioned severity rules.
- [ ] **C16.09.02** Specify validator inputs and outputs using exact candidate manifests, stable offending IDs, expected constraints, observed values, and remediation ownership where failures affect release eligibility.
- [ ] **C16.09.03** Run checks against packaged candidate bytes as well as authoring records; stale passing results cannot authorize files changed after validation or mismatched dependency revisions.
- [ ] **C16.09.04** Define documented exception records containing reason, impact, compensating control, owner, expiration, and scope; approved exceptions cannot suppress unrelated or newly introduced validator failures.
- [ ] **C16.09.05** Create seeded fixtures with one known failure in each category; verify all expected blockers are detected and valid reference packages pass without spurious unexplained defects.
- [ ] **C16.09.06** Exercise unreachable successors, mixed units, broken assertion links, and unresolved template variables; confirm actionable results identify the specific publication dependency or rule needing repair.
- [ ] **C16.09.07** Interrupt validation or restart with incomplete results; require a full valid receipt for the final manifest rather than treating a partially completed run as passed.
- [ ] **C16.09.08** Archive validator configuration, seeded coverage, and exception decisions; accept only when all applicable checks pass for released bytes and every retained failure has an approved disposition.

### Control C16 10

**Original requirement C16.10:** Analyze revision impact before publication, identifying affected live campaigns, completed records, cached packages, and exports; preview migration/correction behavior.

- [ ] **C16.10.01** Define revision-impact reports listing changed content/dependencies, active campaigns, unfinished and completed snapshots, caches, controlled exports, compatibility changes, and proposed correction/migration behaviors.
- [ ] **C16.10.02** Compute impact from the version-specific dependency graph and authoritative campaign records; browser caches or current catalog references cannot define the complete affected population.
- [ ] **C16.10.03** Preview previous versus proposed geographic positions, branches, rights, explanations, assets, and training references; identify immutable history and explicit operations needed for any adopted change.
- [ ] **C16.10.04** Require accountable reviewers to approve impact and migration scope before publication; missing affected campaigns or unresolved historical treatment must block material revisions.
- [ ] **C16.10.05** Preview route, rights, scoring, and event changes against representative saved histories; independently enumerate affected records and compare every reported migration/correction action.
- [ ] **C16.10.06** Exercise stale histories, withdrawn replacements, conflicting live branches, and already exported packages; expose incompatibilities and recall limits rather than promising universal automatic adoption.
- [ ] **C16.10.07** Cancel or interrupt a revision preview and restart; verify no publication pointer, pinned snapshot, workout record, completion status, or continuation position changed during analysis.
- [ ] **C16.10.08** Archive approved impact previews and post-publication reconciliation; accept only when executed revisions match reviewed scope and every affected campaign/history class has a defined treatment.

### Control C16 11

**Original requirement C16.11:** Establish source-specific review cadences and update triggers for route releases, changing official information, permission expiration, and retired references; expose overdue review work.

- [ ] **C16.11.01** Create a source-specific review schedule stating owner, content scope, cadence, due-date basis, trigger conditions, evidence requirement, and permitted overdue-release behavior for each source family.
- [ ] **C16.11.02** Include route-release updates, changing official information, rights expiration/revocation, retired references, and material source corrections as explicit event-driven review triggers beyond routine dates.
- [ ] **C16.11.03** Calculate review deadlines from stored acquisition/review records with documented timezone/date conventions; unknown freshness cannot silently become a current or indefinitely approved status.
- [ ] **C16.11.04** Expose overdue tasks with affected claims/assets, severity, accountable owner, and publication consequences; distinguish informational backlog from content requiring immediate withdrawal or blocked release.
- [ ] **C16.11.05** Advance reference dates and inject source-change events in fixtures; verify correct tasks appear, deadlines recalculate appropriately, and permission expiry reaches dependent publication/delivery checks.
- [ ] **C16.11.06** Exercise absent owners, unknown dates, retired URLs, and repeatedly deferred reviews; require escalation or a bounded exception rather than silently clearing overdue status.
- [ ] **C16.11.07** Complete a review or replace its source through an attributable operation; retain prior deadlines, findings, and content revisions so freshness evidence remains historically auditable.
- [ ] **C16.11.08** Archive review schedules and trigger/overdue tests; accept only when every changing-information source has an owner and overdue material receives an explicit release or withdrawal disposition.

### Control C16 12

**Original requirement C16.12:** Sanitize imported/authored content, validate uploads, restrict executable embeds, and separate authored game rules from equipment-command authority and unapproved exercise changes.

- [ ] **C16.12.01** Specify allowed authored markup, attachment/media formats, size limits, embedded content policy, rule effect types, and prohibited executable/equipment-command capabilities for imported and authored materials.
- [ ] **C16.12.02** Sanitize presentation content using the selected parser/rendering contract and validate file signatures/paths; dangerous markup or disguised executables must not enter approved served packages.
- [ ] **C16.12.03** Restrict rules to approved typed fictional/preparation effects; content authors cannot create automatic treadmill commands or change physical targets through scripts, markup, or generated prose.
- [ ] **C16.12.04** Review the import-to-preview-to-publication trust boundaries and identify authoritative validation points; browser-only sanitization cannot authorize unsafe server-side content or bypass rule validation.
- [ ] **C16.12.05** Publish valid supported content and inspect rendered behavior; confirm intended formatting, captions, links, and fictional effects remain functional without granting additional executable authority.
- [ ] **C16.12.06** Submit script markup, executable embeds, oversized uploads, path escapes, forbidden effects, and hidden physical directives; require rejection or safe sanitization with traceable offending content IDs.
- [ ] **C16.12.07** Interrupt rejected imports and restart; verify quarantined/staged files cannot become served dependencies and prior approved content plus accepted physical assignments remain unchanged.
- [ ] **C16.12.08** Archive adversarial import/rule and boundary evidence; accept only when prohibited content has no execution/equipment authority and every allowed effect stays within its documented domain.

### Control C16 13

**Original requirement C16.13:** Provide reporting for inaccurate geography, misleading imagery, incorrect lessons, rights problems, broken events, and inaccessible content; track severity, owner, response, and resolution evidence.

- [ ] **C16.13.01** Define issue-report fields for inaccurate geography, misleading imagery, lesson errors, rights concerns, broken branches, inaccessible content, affected version, severity, reporter context, and evidence.
- [ ] **C16.13.02** Provide a local reporting path reachable from relevant dossier/media/activity views; automatically include useful content identity while avoiding unnecessary personal reflection or workout disclosure.
- [ ] **C16.13.03** Assign owner, acknowledgment target, triage status, corrective action, due date, and escalation according to severity; urgent rights/factual issues require targeted delivery restrictions when justified.
- [ ] **C16.13.04** Link reports to affected dependencies, review decisions, correction releases, and retained verification results; closure requires evidence rather than merely changing an issue status.
- [ ] **C16.13.05** Submit representative reports for each content problem category; verify correct routing, version capture, privacy-conscious diagnostics, and traceability to the actual released asset or rule.
- [ ] **C16.13.06** Exercise missing details, duplicate reports, disputed severity, and unavailable owners; preserve the report and obtain a documented disposition without silently discarding actionable concerns.
- [ ] **C16.13.07** Resolve a material defect through correction/withdrawal, then revisit affected content; confirm reported behavior is repaired and historical annotations/recall limitations match the approved action.
- [ ] **C16.13.08** Archive issue-to-resolution examples and response metrics; accept only when every actionable report has an accountable disposition and closed material issues have confirming corrective evidence.

### Control C16 14

**Original requirement C16.14:** Support targeted withdrawal and transactional release-pointer rollback to a verified coherent snapshot; preserve workout/day logs and next-leg state. Leave pinned unfinished/completed snapshots unchanged except through the explicit correction/withdrawal workflow.

- [ ] **C16.14.01** Define targeted withdrawal and rollback operations with affected content versions, replacement/coherent target manifest, expected release revision, actor, reason, and approved historical treatment.
- [ ] **C16.14.02** Validate rollback targets for complete dependency closure, effective rights, schema/application compatibility, and safe local-file availability before changing the current release pointer.
- [ ] **C16.14.03** Commit release-pointer changes transactionally in SQLite; published file preparation remains separately recoverable and cannot imply that filesystem artifacts participate in database atomicity.
- [ ] **C16.14.04** Preserve workout records, completed/unfinished day identities, pinned snapshots, and next-leg state; any snapshot correction/withdrawal must use its explicit audited workflow.
- [ ] **C16.14.05** Withdraw one shared asset and roll back a problematic content release; inspect current delivery, substitutes, cache behavior, and unaffected campaign records against expected outcomes.
- [ ] **C16.14.06** Attempt rollback to an expired-rights, missing-file, incompatible-schema, or structurally incomplete snapshot; reject the target while retaining the existing coherent approved pointer.
- [ ] **C16.14.07** Interrupt pointer updates and file preparation, then restart; reconcile to one verified selected release or explicit nonready status without mixed dependencies or campaign advancement.
- [ ] **C16.14.08** Archive withdrawal/rollback and history-preservation evidence; accept only when every selected target is coherent and all campaign changes remain limited to explicitly approved correction operations.

### Control C16 15

**Original requirement C16.15:** Manage permission-based removal across packages and caches under application control; record what cannot be recalled from independent copies or prior exports.

- [ ] **C16.15.01** Define permission-removal events with grant/asset versions, permitted retention, delivery restrictions, effective date, affected packages/caches/exports, replacement, reviewer, and independent-copy recall limits.
- [ ] **C16.15.02** Use reverse dependencies to enumerate controlled copies and manifests; distinguish immutable historical metadata from image bytes that must no longer be served or included.
- [ ] **C16.15.03** Invalidate or rebuild application-controlled packages and caches according to the decision; new exports must omit prohibited assets or use reviewed, correctly attributed substitutes.
- [ ] **C16.15.04** Document already exported or independently copied material outside application control with known scope and any user-facing recall information; never claim deletion beyond verified controlled locations.
- [ ] **C16.15.05** Execute a removal involving current galleries, local packages, cached renditions, and controlled exports; reconcile expected affected copies and confirm prohibited current delivery is denied.
- [ ] **C16.15.06** Reopen old URLs and populated browser caches after removal; verify revalidation or blocking prevents restoration of withdrawn content as an approved current dependency.
- [ ] **C16.15.07** Interrupt cleanup and restart from the durable removal ledger; continue pending actions without removing unrelated originals or damaging saved workout/day/continuation records.
- [ ] **C16.15.08** Archive controlled-copy reconciliation and recall-limit statements; accept only when every controlled dependency complies and every unverifiable external recall boundary is explicitly recorded.

### Control C16 16

**Original requirement C16.16:** Back up SQLite using a database-consistent method plus referenced originals, evidence, snapshots, and logs; verify restoration and repository relocation, with retention and schema-migration recovery documented.

- [ ] **C16.16.01** Define backup scope including database, referenced originals, evidence records, immutable snapshots, required manifests, and logs with retention, privacy, integrity, and restoration ownership.
- [ ] **C16.16.02** Use a database-consistent SQLite backup method appropriate to the selected journal/runtime configuration; do not copy a live main database file while ignoring required consistency handling.
- [ ] **C16.16.03** Create a backup manifest mapping database/schema versions, artifact paths/checksums, creation time, application compatibility, and included run/history references; identify intentionally excluded recoverable caches.
- [ ] **C16.16.04** Specify restoration ordering and schema-migration rollback/forward-repair procedures; validate referenced artifacts before exposing restored content or allowing authoritative campaign mutations to resume.
- [ ] **C16.16.05** Restore a backup into a clean supported repository and independently reconcile campaigns, next-leg position, completed snapshots, media originals, evidence links, and retained diagnostics.
- [ ] **C16.16.06** Relocate the restored repository and verify relative paths, package roots, and launch behavior; no stale absolute source path may redirect authoritative storage elsewhere.
- [ ] **C16.16.07** Inject missing artifacts, checksum corruption, interrupted backup, and incompatible schema migration; block unsafe restoration and retain the verified prior backup or documented repair path.
- [ ] **C16.16.08** Archive restore/relocation rehearsals and retention decisions; accept only when consistent backups reconstruct authoritative history and required artifacts with verified integrity across supported recovery environments.

### Control C16 17

**Original requirement C16.17:** Provide separate local preview/publication directories and dry runs using representative saved histories; configure the local service to expose approved roots, exclude database/log files, and keep draft files outside served paths.

- [ ] **C16.17.01** Define distinct repository-local authoring/preview, staging, and publication roots with ownership, served-root configuration, package eligibility, and safe canonical-path validation for the loopback service.
- [ ] **C16.17.02** Keep draft files and representative saved-history fixtures outside approved delivery roots; preview operations must not mutate real campaign, workout, or next-leg records.
- [ ] **C16.17.03** Run dry publication against copied representative histories covering branches, old manifests, unfinished/completed days, and rights changes; record compatibility and impact without changing live selection pointers.
- [ ] **C16.17.04** Configure delivery to expose only approved package/media roots and explicit application endpoints; database, logs, local settings, evidence-private files, and unrelated repository content remain inaccessible.
- [ ] **C16.17.05** Request valid published files and attempted draft/database/log paths through the actual service; verify approved delivery works and all excluded paths receive safe denial.
- [ ] **C16.17.06** Exercise traversal encodings, escaping links, root overlap mistakes, and repository relocation; require configuration validation before serving an incorrectly expanded publication boundary.
- [ ] **C16.17.07** Interrupt preview or dry-run publication and inspect live data; verify no ready pointer, completion record, active campaign, or physical assignment changed from the baseline.
- [ ] **C16.17.08** Archive root configuration, dry-run impacts, and path-exposure tests; accept only when preview isolation holds and the service serves exclusively the explicitly approved publication boundaries.

### Control C16 18

**Original requirement C16.18:** Monitor coverage, publication failures, missing assets, overdue reviews, broken sources, and unresolved corrections; assign an owner to every actionable exception.

- [ ] **C16.18.01** Define actionable monitoring records for coverage gaps, publication failures, missing assets, overdue reviews, broken sources, and unresolved corrections with affected versions and severity.
- [ ] **C16.18.02** Calculate indicators from authoritative inventory, validation receipts, files, and correction registers; distinguish observed errors from unknown/unverified checks and stale monitoring results.
- [ ] **C16.18.03** Assign owner, response target, escalation, and disposition to each actionable exception; transient retry status cannot indefinitely conceal a failed publication or overdue rights review.
- [ ] **C16.18.04** Provide local reports or dashboard views linking indicators to exact dependencies and remediation evidence; avoid collecting unnecessary personal journal content for content-health monitoring.
- [ ] **C16.18.05** Seed one defect in every indicator category and generate the report; independently verify counts, affected records, severity, and assigned owner against the known fixture inventory.
- [ ] **C16.18.06** Exercise missing owners, duplicate alerts, retired releases, and stale source checks; deduplicate notifications while preserving unresolved problems and exposing when monitoring itself is unavailable.
- [ ] **C16.18.07** Resolve defects and rerun the relevant indicators; retain historical failure/disposition records and close exceptions only after the claimed repair has confirming evidence.
- [ ] **C16.18.08** Archive monitoring definitions, seeded results, and ownership coverage; accept only when every actionable problem is visible, attributable, and traceable through resolution or a bounded accepted exception.

### Control C16 19

**Original requirement C16.19:** Test permission failures, concurrent launches/edits, SQLite locks, interrupted file-and-database publication, dependency mismatch, unsafe paths, withdrawal, rollback, campaign compatibility, and consistent backup restoration.

- [ ] **C16.19.01** Create a content-operations verification matrix for permission denial, concurrent launches/edits, SQLite contention, interrupted file/database publication, dependency mismatch, unsafe paths, withdrawal, rollback, and restoration.
- [ ] **C16.19.02** Specify exact initial manifests, campaign histories, database revisions, file states, fault boundaries, expected responses, and preserved workout/day/continuation records before executing each scenario.
- [ ] **C16.19.03** Exercise concurrent authoring and launcher requests with stale revisions; verify deterministic reservation/publication ownership, explicit conflicts, and no duplicate releases or accidental campaign/day completion.
- [ ] **C16.19.04** Inject failures around staging, checksum validation, rename, database publication markers, and pointer changes; reconcile one coherent selected package or explicit recoverable nonready state.
- [ ] **C16.19.05** Attempt unsafe delivery paths and incompatible campaign adoption; require denial without exposing private repository content or mixing pinned historical dependencies with current catalog selections.
- [ ] **C16.19.06** Withdraw shared assets, roll back candidate releases, and restore consistent backups; compare all affected delivery paths and restored relationships with independently enumerated expected dependency sets.
- [ ] **C16.19.07** Track failures to implementation/content versions and responsible owners; retain reproduced fault evidence and rerun targeted scenarios after corrections rather than discarding failed results.
- [ ] **C16.19.08** Archive the complete operations matrix and reconciliation artifacts; accept only when every listed failure/recovery case preserves authoritative campaign history and approved content/path boundaries.

### Control C16 20

**Original requirement C16.20:** Require readiness evidence for continuity, dossier completeness, branches, rights, learning, accessibility, local internet-free operation, relaunch/resume, explicit completion advancement, path exposure, and compatibility; archive accepted limitations.

- [ ] **C16.20.01** Create release-readiness evidence requirements for route continuity, dossier completeness, reachable branches, rights, learning quality, accessibility, local operation, resume, completion, exposure boundaries, and compatibility.
- [ ] **C16.20.02** Map every evidence item to candidate application/schema/content/rule versions, accountable reviewer, test or inspection result, affected release scope, and explicit pass/exception criteria.
- [ ] **C16.20.03** Require evidence from actual packaged candidate content and supported local launcher/service flows; isolated unit results alone cannot establish complete-user-journey or internet-free release readiness.
- [ ] **C16.20.04** Reconcile unfinished/completed saved histories through relaunch and explicit completion; verify required branches, pinned dependencies, physical activity, and next-leg advancement match independently expected records.
- [ ] **C16.20.05** Inspect rights, accessibility, learning explanations, and path exposure against their declared review baselines; reject missing evidence or material unresolved defects before attributable acceptance.
- [ ] **C16.20.06** Exercise obsolete evidence, mismatched manifest hashes, unsupported schema versions, and unreviewed limitations; prevent approval records from authorizing a different or incomplete candidate release.
- [ ] **C16.20.07** Record accepted limitations with impact, compensating controls, owner, expiration, revisit trigger, and user-visible wording where material; preserve failed/replaced candidate evidence for auditability.
- [ ] **C16.20.08** Archive readiness matrix and attributable acceptance beside immutable release manifests; accept only when all applicable gates pass or have explicit bounded exceptions matching the selected release.

## C17 CMD and PowerShell launch orchestration

**Accountable owner:** Local application owner. **Technical owner:** Windows launch/runtime engineering. **Reviewers:** Reliability, security, and support.

**Inputs:** Repository location, configuration, supported runtime, existing instance marker, and launch arguments. **Outputs:** Attributable run record, owned service instance, verified dossier URL, browser launch, and exit status.

**Required evidence:** Launch/run contract; supported-version matrix; configuration schema; instance and health protocol; process-ownership tests; PowerShell error demonstrations; startup/restart test report.

**Exit criterion:** The user can launch the correct saved hike from the CMD entry point, receive a verified loopback URL, resume after failure, and stop owned services without duplicate days or interference with unrelated applications.

### Control C17 01

**Original requirement C17.01:** Provide `Start-Hike.cmd` as the stable entry point and a versioned `Start-Hike.ps1` orchestration script; keep invocation, defaults, supported switches, and exit-code meanings documented.

- [ ] **C17.01.01** Specify the user entry point, PowerShell script location, supported invocation modes, defaults, and arguments in a versioned launch contract.
- [ ] **C17.01.02** Define stable exit codes for success, already-running reuse, configuration error, unsupported runtime, persistence failure, readiness timeout, and browser-start failure.
- [ ] **C17.01.03** Implement the CMD wrapper using its own directory and invoke the intended PowerShell script with explicit structured argument forwarding.
- [ ] **C17.01.04** Keep startup orchestration separate from domain completion logic; launcher success cannot itself award exercise credit or close a hike day.
- [ ] **C17.01.05** Preserve an intelligible console outcome and diagnostic reference when the wrapper or script fails before the browser is available.
- [ ] **C17.01.06** Invoke the shipped entry point with default and supported switches and compare returned codes and run records with the contract.
- [ ] **C17.01.07** Test missing script, invalid switch, refused startup, and nested invocation to confirm error propagation does not disguise a failed launch as success.
- [ ] **C17.01.08** Archive the wrapper/script versions, invocation fixtures, and exit-code results; accept when documented launch outcomes remain stable and attributable.

### Control C17 02

**Original requirement C17.02:** Resolve the repository from the launcher's own absolute path rather than the caller's working directory; test spaces, Unicode characters, parentheses, and shell-significant path characters.

- [ ] **C17.02.01** Define repository-root resolution from the launcher's absolute location and document how scripts derive subordinate content, data, and configuration paths.
- [ ] **C17.02.02** Normalize and validate resolved paths without assuming the caller directory, a fixed drive letter, or a user-specific installation location.
- [ ] **C17.02.03** Pass resolved filesystem paths as values through the CMD and PowerShell boundary rather than constructing evaluated command text.
- [ ] **C17.02.04** Specify handling of unavailable roots, moved repositories, symbolic links or reparse points, and paths outside the approved runtime-data boundary.
- [ ] **C17.02.05** Ensure log and database identity refer to the resolved repository even when the launcher is called through a shortcut or another working directory.
- [ ] **C17.02.06** Launch from unrelated directories using repository names containing spaces, Unicode, parentheses, ampersands, and other supported shell-significant characters.
- [ ] **C17.02.07** Relocate the repository, use an invalid shortcut target, and supply malformed path overrides; verify no files or state are created in an unintended directory.
- [ ] **C17.02.08** Retain canonical-path traces and special-character tests; accept when all supported invocations resolve the intended repository without quoting ambiguity or escaped write targets.

### Control C17 03

**Original requirement C17.03:** Select tested Windows and PowerShell versions and a supported local-server runtime; detect missing or incompatible dependencies and report exact remediation instead of launching a partially functional service.

- [ ] **C17.03.01** Select supported Windows, PowerShell, local-service runtime, and SQLite dependency versions, documenting the capabilities required from each.
- [ ] **C17.03.02** Define dependency discovery precedence and version checks without assuming that the first similarly named executable on the search path is acceptable.
- [ ] **C17.03.03** Validate executable identity and required capabilities before starting the service or performing a database migration.
- [ ] **C17.03.04** Report missing, unsupported, or incompatible dependencies with exact local remediation and retain the attempted version in launch diagnostics.
- [ ] **C17.03.05** Do not initialize replacement history or start partial functionality when a required runtime cannot satisfy persistence or protocol requirements.
- [ ] **C17.03.06** Test every supported runtime combination with a clean startup, saved-day resume, completion, shutdown, and restart journey.
- [ ] **C17.03.07** Exercise absent executable, wrong architecture, incompatible version, conflicting search-path entries, and unreadable dependency paths without altering hike state.
- [ ] **C17.03.08** Archive the supported matrix, detected-version records, and preflight results; accept dependency checks only when unsupported environments fail before consequential mutations.

### Control C17 04

**Original requirement C17.04:** Validate arguments and pass them as structured values without constructing commands from untrusted strings; do not use shell evaluation for campaign identifiers, ports, paths, or user text.

- [ ] **C17.04.01** Define argument schemas for campaign identity, configuration paths, port, mode, and diagnostics, including type, length, allowed values, and defaults.
- [ ] **C17.04.02** Distinguish launcher-owned fixed command syntax from user-supplied values and identify every transition between CMD, PowerShell, and server argument parsing.
- [ ] **C17.04.03** Use structured argument passing and literal filesystem APIs; prohibit dynamic evaluation or concatenated shell commands containing user text.
- [ ] **C17.04.04** Reject unknown switches, duplicate incompatible options, malformed numeric values, and argument combinations that bypass normal state ownership.
- [ ] **C17.04.05** Keep rejected argument text out of unsafe executable contexts and redact any sensitive values from usage errors and run records.
- [ ] **C17.04.06** Round-trip permitted spaces, quotes, Unicode, and supported paths across each invocation boundary and verify unchanged interpreted values.
- [ ] **C17.04.07** Submit command-substitution syntax, separators, wildcard paths, overflow ports, and malicious campaign strings and confirm no unintended command or file operation occurs.
- [ ] **C17.04.08** Retain parsing specifications and injection-denial results; accept when supported values survive correctly and untrusted arguments cannot alter command structure.

### Control C17 05

**Original requirement C17.05:** Load documented configuration precedence for defaults, local overrides, and command arguments; validate values, canonical paths, port range, timezone, data location, and content compatibility.

- [ ] **C17.05.01** Publish schemas for public defaults, local overrides, and command arguments, including path, port, timezone, content, and runtime fields.
- [ ] **C17.05.02** Specify precedence, missing-value behavior, unknown-field handling, and which settings may change during an active hike or running service.
- [ ] **C17.05.03** Merge configuration through typed validation and canonicalize paths before use, retaining the effective nonsecret configuration identity in the run record.
- [ ] **C17.05.04** Verify ports fall in the accepted range, timezone identifiers are recognized, directories are appropriate, and content matches supported application schemas.
- [ ] **C17.05.05** On invalid configuration, stop before reserving a day and report the offending field without printing secrets or discarding previously saved state.
- [ ] **C17.05.06** Test defaults alone and each override layer, comparing the effective configuration and served URL with independently specified expected values.
- [ ] **C17.05.07** Exercise conflicting overrides, invalid JSON, unknown fields, unavailable paths, malformed timezones, and incompatible content to verify explicit rejection.
- [ ] **C17.05.08** Archive schemas, precedence fixtures, and effective-config reports; accept when launch settings are reproducible and invalid values cannot redirect authoritative state silently.

### Control C17 06

**Original requirement C17.06:** Respect the machine's PowerShell execution-policy configuration and present actionable errors; do not silently change persistent user or machine policy as part of an ordinary launch.

- [ ] **C17.06.01** Document the supported PowerShell invocation and relevant execution-policy expectations without promising that every machine permits unsigned scripts.
- [ ] **C17.06.02** Define how preflight detects script-policy refusal and distinguishes it from missing runtime, syntax, permission, or service errors.
- [ ] **C17.06.03** Run within the existing permitted configuration; ordinary launch must not change persistent user, machine, or organizational execution-policy settings.
- [ ] **C17.06.04** Present an actionable explanation identifying the refused script and documented user-controlled resolution rather than silently retrying through another policy scope.
- [ ] **C17.06.05** Record the launch failure without treating a policy denial as a started session, new day, or completed leg.
- [ ] **C17.06.06** Verify normal startup in the selected permitted policy configurations using the actual distributed script and its deployment location.
- [ ] **C17.06.07** Launch under a deliberately restrictive configuration and confirm no persistent policy changes, hidden bypass, partial service, or hike-state mutation occurs.
- [ ] **C17.06.08** Retain policy-state comparisons and refusal diagnostics; accept when launch respects existing policy and failures remain precise, recoverable, and nonmutating.

### Control C17 07

**Original requirement C17.07:** Check read/write access and disk capacity for state, generated dossiers, logs, and backups before changing hike state; distinguish content-read problems from authoritative-state failures.

- [ ] **C17.07.01** Inventory required read and write locations for content, SQLite state, generation staging, diagnostics, exports, and backups before startup mutates history.
- [ ] **C17.07.02** Define preflight checks for directory existence, effective permissions, supported storage, available capacity, and minimum writable operational locations.
- [ ] **C17.07.03** Use scoped safe probes that verify required access without modifying authoritative records or overwriting existing user files.
- [ ] **C17.07.04** Classify missing optional media separately from unreadable content manifests, unwritable state, and unavailable backup destinations.
- [ ] **C17.07.05** Stop or enter the declared read-only mode when authoritative storage cannot work; do not replace the database in a fallback directory silently.
- [ ] **C17.07.06** Test normal content read, state commit, staged publication, and backup preparation with the documented repository permissions.
- [ ] **C17.07.07** Inject read-only directories, denied files, low space, missing media, and unavailable volumes, confirming correct severity and unchanged continuation state.
- [ ] **C17.07.08** Archive location/permission checks and capacity-failure traces; accept when write prerequisites are verified and storage faults cannot cause hidden state relocation or false saving.

### Control C17 08

**Original requirement C17.08:** Acquire a repository-scoped startup lock before starting or reserving a day; simultaneous double-clicks must not create duplicate services or duplicate hike-day records.

- [ ] **C17.08.01** Define the repository-scoped startup lock identity, acquisition method, timeout, owner metadata, lifetime, and stale-owner recovery rules.
- [ ] **C17.08.02** Acquire ownership before service creation or day reservation and ensure the lock identity differentiates distinct repositories correctly.
- [ ] **C17.08.03** Coordinate concurrent launchers so one performs startup while others wait, attach, or return the documented already-running outcome.
- [ ] **C17.08.04** Keep database uniqueness constraints as a second safeguard; a launcher lock alone does not establish exclusive day creation under every failure.
- [ ] **C17.08.05** Release or recover lock ownership after bounded failure without deleting a lock belonging to a live unrelated or newer instance.
- [ ] **C17.08.06** Launch simultaneous processes repeatedly and verify one owned service, one active-day reservation, and attributable run records for every invocation.
- [ ] **C17.08.07** Terminate the owner during startup and test abandoned lock, timeout, delayed readiness, and repository identity mismatch without creating duplicate days.
- [ ] **C17.08.08** Retain lock-state and concurrency traces; accept when ownership recovery permits restart while preserving single active reservation and correct process scope.

### Control C17 09

**Original requirement C17.09:** Identify an existing service using instance identity, application identity, repository identity, protocol version, and health response; a listening port or PID alone is insufficient evidence of ownership.

- [ ] **C17.09.01** Define an instance marker containing application, repository, process, startup-time, instance, protocol, and listening-address identifiers with safe retention rules.
- [ ] **C17.09.02** Specify the health-response fields and comparison procedure required to prove that a candidate process belongs to this repository and application.
- [ ] **C17.09.03** Verify marker data against a live health response and process identity before reusing, managing, or shutting down an existing service.
- [ ] **C17.09.04** Treat a reused PID, responding port, stale marker, or matching process name as insufficient when instance or repository identity differs.
- [ ] **C17.09.05** On ambiguous ownership, leave the process untouched and provide a conflict diagnostic rather than forcing reuse or termination.
- [ ] **C17.09.06** Start a valid owned instance and verify subsequent launchers identify and attach to its current day using the expected protocol.
- [ ] **C17.09.07** Test PID reuse, copied markers, foreign health responses, wrong repository fingerprints, and obsolete protocols, confirming refusal without interference.
- [ ] **C17.09.08** Archive ownership proofs and mismatch cases; accept when every managed process is linked to a verified current repository instance rather than circumstantial identifiers.

### Control C17 10

**Original requirement C17.10:** Reuse an owned compatible service deliberately; refuse or clearly handle an incompatible owned instance and an unrelated process occupying the configured port without terminating unrelated processes.

- [ ] **C17.10.01** Define distinct outcomes for owned compatible instance, owned incompatible instance, unrelated occupied port, and unavailable candidate instance.
- [ ] **C17.10.02** Specify when reuse is allowed, when deliberate restart is offered, and whether a controlled alternate port may be selected.
- [ ] **C17.10.03** Preserve existing active-day and session state during compatible reuse and report the actual instance, dossier, and URL attached.
- [ ] **C17.10.04** Do not terminate or send shutdown commands to unrelated processes merely because they occupy the preferred port.
- [ ] **C17.10.05** Require ownership validation before replacing an incompatible owned service and protect pending commits through the documented shutdown/restart protocol.
- [ ] **C17.10.06** Test repeated launch against a compatible live instance and verify no new service, day, random draw, or workout is created.
- [ ] **C17.10.07** Run conflicting services and incompatible versions, verifying controlled failure or alternate-port behavior without damage to either repository or unrelated application.
- [ ] **C17.10.08** Retain instance-disposition and process-safety results; accept when reuse and conflict handling preserve hike continuity and respect ownership boundaries.

### Control C17 11

**Original requirement C17.11:** Bind only to the selected IPv4 loopback address `127.0.0.1`; use a documented configured port or controlled fallback and open the actual resulting URL.

- [ ] **C17.11.01** Specify the required listener address as IPv4 loopback, configured port selection, accepted fallback policy, and canonical browser-origin format.
- [ ] **C17.11.02** Validate that runtime binding options cannot silently expand the listener to wildcard, LAN, or an unintended additional address family.
- [ ] **C17.11.03** Read the actual bound endpoint from service startup/readiness and use it consistently for health checks, interface requests, and browser opening.
- [ ] **C17.11.04** When the preferred port is unavailable, apply only the documented controlled choice and record the actual port in the current instance marker.
- [ ] **C17.11.05** Maintain the same repository campaign when the port changes; origin-specific browser preferences cannot initialize another hike.
- [ ] **C17.11.06** Inspect active listeners and connect through the selected loopback URL, verifying correct service identity and dossier state.
- [ ] **C17.11.07** Attempt LAN access and test wildcard-default configuration and port collision, confirming required binding or safe refusal without accidental exposure.
- [ ] **C17.11.08** Archive bind inspection and endpoint-resolution results; accept when exactly the approved local endpoint serves the intended repository and the browser uses its actual address.

### Control C17 12

**Original requirement C17.12:** Start owned helper/service processes without unwanted visible windows, record process identity and startup time, and retain a readable launcher status/error path.

- [ ] **C17.12.01** Identify launcher-visible console behavior separately from background helper/service windows and document which processes require user interaction.
- [ ] **C17.12.02** Define owned process metadata, startup arguments, working directory, stdout/stderr routing, lifecycle, and repository identity for each helper.
- [ ] **C17.12.03** Start noninteractive helpers with hidden windows while preserving a readable launcher status and a durable diagnostic location.
- [ ] **C17.12.04** Capture process start failures and unexpected exits before readiness and distinguish them from a healthy service whose browser has not opened.
- [ ] **C17.12.05** Keep private notes, secrets, and untrusted command text out of visible command lines and ordinary process diagnostics.
- [ ] **C17.12.06** Run the supported launch modes and inspect window behavior, process metadata, console status, and diagnostic correlation.
- [ ] **C17.12.07** Fail helper startup or terminate it before readiness, verifying no orphaned unowned process, premature browser success, or silent day advancement.
- [ ] **C17.12.08** Retain process lifecycle and user-visible startup evidence; accept when helpers operate without unwanted windows while failures remain attributable and intelligible.

### Control C17 13

**Original requirement C17.13:** Record each launch attempt using a unique run identifier, UTC timestamp, configured local date/timezone, command mode, repository identity, application version, and outcome; early startup failures need a diagnostic fallback if the database is unavailable.

- [ ] **C17.13.01** Define the run record fields, launch phases, success/failure outcomes, correlation identifiers, and the distinction between invocation and hike-day completion.
- [ ] **C17.13.02** Generate a unique invocation identity and capture UTC time plus configured local date/timezone without using either as a route-position authority.
- [ ] **C17.13.03** Persist run records through the service/database when available, linking the selected campaign/day and actual service instance.
- [ ] **C17.13.04** Provide a minimal early-failure diagnostic record when startup cannot open SQLite, with a later reconciliation policy that avoids duplicate run history.
- [ ] **C17.13.05** Update run outcome through attributable transitions and preserve known failure details without fabricating a clean shutdown or completed workout.
- [ ] **C17.13.06** Compare invocation count with recorded run identities across fresh start, reuse, resume, readiness failure, browser failure, and normal stop.
- [ ] **C17.13.07** Test failed database access, clock change, repeated launcher clicks, and crash before run finalization, verifying truthful incomplete or failure statuses.
- [ ] **C17.13.08** Archive sample chronological runs and count reconciliation; accept when every attempted invocation is attributable and no run record itself advances the hike.

### Control C17 14

**Original requirement C17.14:** Ask the domain service to resume or reserve the active day from saved state; launching, refreshing, or crossing midnight cannot independently complete a stage or create physical activity.

- [ ] **C17.14.01** Define the startup resolver inputs: selected campaign, incomplete day, continuation pointer, route/content versions, and generation state.
- [ ] **C17.14.02** Give the domain service sole authority to resume or reserve a day; launcher arguments may select permitted modes but cannot assert completed progress.
- [ ] **C17.14.03** Reuse the active day's identity, pinned scenario, dossier, decisions, and resources when an incomplete reservation already exists.
- [ ] **C17.14.04** Reserve the successor only from committed completion state and protect simultaneous requests with transactional uniqueness and idempotent reservation.
- [ ] **C17.14.05** Treat midnight, elapsed calendar days, process exit, browser refresh, and launch count as scheduling context rather than completion evidence.
- [ ] **C17.14.06** Launch repeatedly within one date and across several dates with an unfinished day and verify unchanged route origin and narrative outcome.
- [ ] **C17.14.07** Complete deliberately, relaunch, and inject failure before generation; verify the saved successor is correct and no additional leg is consumed.
- [ ] **C17.14.08** Retain resolver traces and state comparisons; accept when each launch opens the persisted unfinished day or exactly the successor authorized by committed completion.

### Control C17 15

**Original requirement C17.15:** Poll readiness with a bounded timeout and backoff; verify database readiness, expected campaign/day identity, published dossier availability, and compatible API before opening the browser.

- [ ] **C17.15.01** Define readiness prerequisites for database/schema validation, campaign selection, active-day resolution, coherent publication, and compatible local API.
- [ ] **C17.15.02** Specify bounded wait time, polling cadence/backoff, cancellation, and the outcome reported when generation or service startup remains incomplete.
- [ ] **C17.15.03** Validate readiness response identity against the expected repository and instance before trusting its dossier URL or opening the browser.
- [ ] **C17.15.04** Separate process-alive, health, database-ready, generation-ready, and interface-ready states so a responding port cannot impersonate a complete launch.
- [ ] **C17.15.05** Preserve failed or unfinished generation for recovery and present an actionable status without creating another day after timeout.
- [ ] **C17.15.06** Exercise normal and intentionally slow generation, confirming the browser opens only after the correct day and manifest meet readiness conditions.
- [ ] **C17.15.07** Return false-ready, foreign-instance, incompatible-version, missing-snapshot, and timeout responses, verifying refusal and unchanged hike history.
- [ ] **C17.15.08** Retain readiness timelines and identity assertions; accept when opening the browser is gated by a coherent published day rather than process or port presence alone.

### Control C17 16

**Original requirement C17.16:** Launch the default browser once per requested invocation after readiness, print the actual local URL, and provide a no-browser option for diagnostics or an already-open view.

- [ ] **C17.16.01** Define browser-opening behavior for fresh launch, compatible reuse, explicit no-browser mode, diagnostics, and an already-open experience.
- [ ] **C17.16.02** Construct the URL exclusively from the verified bound endpoint and selected ready resource, excluding private data and credentials.
- [ ] **C17.16.03** Open the default browser once for the invocation after readiness and display the same actual URL in the readable launcher output.
- [ ] **C17.16.04** Do not retry browser-opening failures indefinitely or create another service/day in an attempt to recover the interface.
- [ ] **C17.16.05** When opening fails, leave a valid service and copyable URL where appropriate and report a distinct browser-launch outcome.
- [ ] **C17.16.06** Test default-browser opening and no-browser launch against fresh and reused services, counting browser-open actions and run records.
- [ ] **C17.16.07** Simulate missing handler, refused browser launch, changed port, and premature readiness; verify no stale URL or extra day is presented.
- [ ] **C17.16.08** Archive launch-action counts and URL comparisons; accept when each requested opening reaches the verified local day and interface failure is safely recoverable.

### Control C17 17

**Original requirement C17.17:** Provide a verified stop/status operation; shutdown only a process whose repository and instance identity match, accounting for stale marker files and PID reuse.

- [ ] **C17.17.01** Specify stop and status commands, required instance identity, response contracts, permissions, and expected already-stopped outcomes.
- [ ] **C17.17.02** Validate repository, instance, process startup time, protocol, and live ownership before issuing any shutdown or cleanup action.
- [ ] **C17.17.03** Implement graceful owned-instance stop with acknowledgement or bounded verification rather than unconditional termination by PID or port.
- [ ] **C17.17.04** Treat stale markers and reused PIDs as diagnostic inconsistencies; do not target a process whose current ownership cannot be established.
- [ ] **C17.17.05** Preserve committed history and reconcile unfinished sessions or generation state on the next launch after a forced or unexpected stop.
- [ ] **C17.17.06** Stop the valid service and repeat status/stop, verifying correct clean outcomes and removal or retirement of only its owned runtime markers.
- [ ] **C17.17.07** Replace the marker PID with an unrelated process or present another repository instance and verify stop refuses interference.
- [ ] **C17.17.08** Archive ownership checks and shutdown results; accept when management commands are idempotent, scope-correct, and incapable of terminating unrelated applications.

### Control C17 18

**Original requirement C17.18:** Define graceful shutdown, Ctrl+C, console closure, and launch-time failure behavior; flush committed records, close database connections, and distinguish clean shutdown from unexpected termination.

- [ ] **C17.18.01** Define shutdown paths for deliberate stop, Ctrl+C, console closure, startup failure, timeout, and unexpected service termination.
- [ ] **C17.18.02** Specify bounded drain, new-request rejection, active transaction handling, connection closure, marker retirement, and run-outcome recording.
- [ ] **C17.18.03** Finish or roll back current database transactions according to their boundary; never mark an unfinished hike day complete merely because shutdown occurred.
- [ ] **C17.18.04** Keep published snapshots and generation staging distinguishable so interrupted publication can be reconciled on restart.
- [ ] **C17.18.05** Record unresolved or abnormal exit when finalization cannot run, and recover that status from process/instance evidence during later startup.
- [ ] **C17.18.06** Exercise clean shutdown with an idle view, active workout, pending choice, and generation job, inspecting committed records and next-leg state.
- [ ] **C17.18.07** Terminate at commit and publication boundaries and verify restart preserves accepted history, reports unknown intervals, and resumes the same incomplete day.
- [ ] **C17.18.08** Retain shutdown-state tables and recovery traces; accept when exit classification is truthful and no shutdown path loses committed activity or invents completion.

### Control C17 19

**Original requirement C17.19:** Test double launch, arbitrary caller directory, missing dependency, blocked script execution, occupied port, stale PID marker, slow generation, and browser-start failure without skipping a hike leg.

- [ ] **C17.19.01** Prepare launch fixtures for simultaneous invocation, unrelated caller directory, missing runtime, policy refusal, port conflict, stale marker, and delayed generation.
- [ ] **C17.19.02** Record initial campaign, active-day identity, next-leg position, processes, configuration, and expected result before each fixture.
- [ ] **C17.19.03** Run each case through the actual distributed CMD entry point rather than calling domain helpers directly.
- [ ] **C17.19.04** Capture wrapper exit code, console result, run record, listener identity, browser-open action, and any created reservation.
- [ ] **C17.19.05** Verify duplicate invocation yields one owned service/day while each launch remains attributable and unrelated occupied-port processes remain untouched.
- [ ] **C17.19.06** Confirm blocked or missing prerequisites stop before consequential day mutation and delayed readiness opens only the valid published dossier.
- [ ] **C17.19.07** Compare post-case route pointer, workouts, decisions, and day sequence with initial expected state, including browser-start failure after healthy service startup.
- [ ] **C17.19.08** Archive the launch acceptance matrix and reconciliation; accept when all named cases behave predictably without skipped legs, false exercise, or ownership violations.

### Control C17 20

**Original requirement C17.20:** Test restart after service crash, repository relocation, Unicode paths, invalid configuration, read-only folders, and disk failure; verify accurate run outcomes and ownership-safe cleanup.

- [ ] **C17.20.01** Create restart fixtures containing an unfinished day, committed decisions, an interrupted generator, and an attributable prior abnormal run.
- [ ] **C17.20.02** Define relocation, Unicode path, invalid configuration, read-only folder, unavailable volume, and low-disk test conditions with expected safe outcomes.
- [ ] **C17.20.03** Terminate the owned service, relaunch from the supported entry point, and compare recovered campaign/day identity and pinned content with the fixture.
- [ ] **C17.20.04** Move the repository and verify canonical path resolution, relative asset references, instance identity replacement, and preserved database history.
- [ ] **C17.20.05** Inject configuration and storage faults before and during startup, ensuring clear error status and no unintended fallback database creation.
- [ ] **C17.20.06** Check old marker/process cleanup targets only verified owned resources and does not follow stale identity into another process or repository.
- [ ] **C17.20.07** Inspect run history, published manifests, current-day status, and continuation pointer after every recovery and compare them with independent expected records.
- [ ] **C17.20.08** Retain restart/relocation fault reports; accept when supported moves and crashes recover correctly and unsupported storage/configuration conditions fail without corrupting hike state.

## C18 Repository hike history and next leg state

**Accountable owner:** Hike history owner. **Technical owner:** Persistence/domain engineering. **Reviewers:** Route, activity data, game systems, and reliability.

**Inputs:** Launch records, campaign selection, route/itinerary versions, day reservation, accepted workouts, choices, and explicit completion. **Outputs:** Authoritative day history, saved continuation position, generated-snapshot references, and portable history exports.

**Required evidence:** Database schema and constraints; run/day state machine; continuation algorithm; transactional completion tests; file/database reconciliation protocol; backup and restoration results; chronological sample history.

**Exit criterion:** The next dossier is derived reproducibly from the last committed hike state, every run and completed day remain attributable, and crashes or repeated launches cannot silently lose, duplicate, or skip a leg.

### Control C18 01

**Original requirement C18.01:** Store authoritative state in a repository-local SQLite database with documented path, schema version, campaign identity, foreign keys, unique constraints, and migration history.

- [ ] **C18.01.01** Define the database path relative to the repository root and require the launcher, HTTP service, export tool, and recovery tool to resolve that same path.
- [ ] **C18.01.02** Specify schema metadata containing schema version, migration identifier, application compatibility bounds, campaign identifiers, creation time, and the last successfully applied migration.
- [ ] **C18.01.03** Create foreign keys for campaign, day, session, completion, decision, and credit relationships; enable enforcement on every connection before accepting application writes.
- [ ] **C18.01.04** Enforce unique operation identities, expedition day sequences, completion references, and other declared business keys through database constraints rather than browser validation alone.
- [ ] **C18.01.05** Keep schema migrations versioned with ordered preconditions, transactional boundaries, backup requirements, and explicit recovery steps for migrations containing filesystem changes.
- [ ] **C18.01.06** Initialize a fresh repository, reopen it, and demonstrate that all supported entry points retrieve the same campaign identity and schema version.
- [ ] **C18.01.07** Attempt orphan records, duplicate business keys, unsupported schema access, and opening an unexpected empty database; verify clear rejection without silently creating another campaign.
- [ ] **C18.01.08** Retain the schema definition, connection configuration, migration inventory, and constraint test results; accept when repository authority and relational integrity are demonstrable.

### Control C18 02

**Original requirement C18.02:** Define separate `Run`, `HikeDay`, `WorkoutSession`, and `DayCompletion` records; retain the distinction between starting the software, opening an expedition day, doing activity, and finishing a leg.

- [ ] **C18.02.01** Define Run as one application invocation, HikeDay as one virtual expedition leg, WorkoutSession as one activity record, and DayCompletion as its committed advancement event.
- [ ] **C18.02.02** Specify identifiers and relationships that permit several runs and workout sessions to reference one HikeDay without creating duplicate completion or expedition day records.
- [ ] **C18.02.03** Document which actions create each record and prohibit browser refresh, application launch, or session creation from implicitly inserting a DayCompletion.
- [ ] **C18.02.04** Separate invocation timestamps, workout timestamps, fictional day sequence, and completion timestamps so reports cannot infer one dimension from another.
- [ ] **C18.02.05** Support launching for review without exercise, exercising without finishing a leg, and reopening a completed dossier through explicit action classifications.
- [ ] **C18.02.06** Run two launches and three workouts against one unfinished day; verify distinct invocation and workout history with only one active expedition day.
- [ ] **C18.02.07** Refresh, reopen, and inspect the dossier repeatedly; verify no route advancement and no invented workout or completion records.
- [ ] **C18.02.08** Retain the entity relationship model and event-to-record matrix; accept when software use, physical activity, and virtual advancement remain independently auditable.

### Control C18 03

**Original requirement C18.03:** Define each run with identifier, timestamps, configured local date/timezone, instance identity, application version, selected day, action, status, and failure/exit details; multiple runs may refer to the same day.

- [ ] **C18.03.01** Define required Run fields for run ID, start time, configured local date, timezone identifier, instance ID, application version, selected day, action, status, and exit outcome.
- [ ] **C18.03.02** Store unambiguous timestamps alongside recorded local-date context; preserve the configuration used at invocation instead of recalculating historical dates after timezone changes.
- [ ] **C18.03.03** Create an attributable initial run record before normal operation and update its terminal outcome when the owned process exits normally.
- [ ] **C18.03.04** Represent launcher failure, reused service, review-only access, interrupted execution, and unknown terminal outcome through defined statuses with explanatory reason codes.
- [ ] **C18.03.05** Allow multiple invocations on the same date without a date uniqueness constraint and correlate a reused service with each originating launcher run.
- [ ] **C18.03.06** Execute multiple launches, including one browser-opening failure, and verify that run history preserves each invocation while hike progress remains unchanged.
- [ ] **C18.03.07** Terminate the process unexpectedly, then restart; verify the previous unresolved run is reconciled as interrupted without inventing an exact exit timestamp.
- [ ] **C18.03.08** Retain representative run records and reconciliation results; accept when every recorded invocation has an interpretable identity, action, and attributable lifecycle outcome.

### Control C18 04

**Original requirement C18.04:** Define each hike day with campaign, expedition-day number, stage and route release, start/end route positions, content manifest, scenario seed, generated snapshot, state, revision, and completion references.

- [ ] **C18.04.01** Define the HikeDay schema with campaign identity, expedition sequence, stage ID, route release, start and end positions, manifest identity, seed, snapshot references, state, and revision.
- [ ] **C18.04.02** Specify canonical route positions using segment identity, chainage, direction, and route release; retain display mileage separately for presentation.
- [ ] **C18.04.03** Pin content, narrative rules, and random seed at reservation or generation according to a documented boundary that subsequent retries cannot silently change.
- [ ] **C18.04.04** Reference completion and generated artifacts through validated identities; prevent a day from claiming another campaign's completion or an unpublished snapshot.
- [ ] **C18.04.05** Define which fields are immutable after publication and which require a revisioned correction, regeneration, or deliberate campaign repair operation.
- [ ] **C18.04.06** Reserve, generate, activate, and complete a day; compare each stored record against the declared schema and expected revision transitions.
- [ ] **C18.04.07** Attempt to alter pinned route release, swap a snapshot reference, or attach a foreign completion; verify rejection or the documented explicit correction procedure.
- [ ] **C18.04.08** Retain schema samples, immutability rules, and state transition evidence; accept when a day can be reproduced and explained from its persisted references.

### Control C18 05

**Original requirement C18.05:** Store the continuation pointer as a route-release/segment/chainage/direction identity, not a guessed mileage string, file modification time, calendar date, browser preference, or count of launches.

- [ ] **C18.05.01** Define the continuation pointer as campaign, route release, segment identity, chainage, travel direction, and any explicitly selected branch or terminal condition.
- [ ] **C18.05.02** Specify how segment boundaries and route junctions resolve the next position, including precision, rounding, and valid endpoint ranges.
- [ ] **C18.05.03** Compute continuation from committed completion results and selected itinerary rules; prohibit deriving it from filename sorting, calendar dates, launch count, or displayed mileage.
- [ ] **C18.05.04** Validate that a pointer belongs to the campaign's pinned route release and that its segment and direction are valid before reserving another day.
- [ ] **C18.05.05** Represent terminal trail completion and deliberate itinerary changes explicitly so an endpoint cannot wrap to the first leg or jump to an unrelated release.
- [ ] **C18.05.06** Complete adjacent legs and verify contiguous positions, including one boundary crossing where display mileage rounding would otherwise create ambiguity.
- [ ] **C18.05.07** Change file timestamps, browser storage, local date, and display units; verify the authoritative continuation pointer remains unchanged.
- [ ] **C18.05.08** Retain pointer schema, boundary fixtures, and before-and-after committed positions; accept when every next leg has a traceable route-based origin.

### Control C18 06

**Original requirement C18.06:** Enforce at most one active uncompleted day per campaign and a unique expedition-day sequence; permit several actual sessions and calendar dates to contribute to a virtual day.

- [ ] **C18.06.01** Define the database predicate identifying an active unfinished HikeDay and enforce at most one matching record per campaign through a constraint or equivalent transactional invariant.
- [ ] **C18.06.02** Require a unique campaign and expedition day sequence while permitting multiple workout sessions and application runs to reference that same day.
- [ ] **C18.06.03** Allow one virtual day to span several calendar dates without renumbering it or creating a replacement day merely because the local date changed.
- [ ] **C18.06.04** Specify how completed, failed-generation, and deliberately abandoned or repaired records interact with the active-day invariant and sequence allocation.
- [ ] **C18.06.05** Ensure administrative repair cannot leave two independently resumable days; require a documented conflict disposition before normal launch resumes.
- [ ] **C18.06.06** Accumulate sessions across several dates and verify one active day, one sequence number, and the expected many-to-one activity relationships.
- [ ] **C18.06.07** Race two reservations and attempt duplicate sequences; verify one authoritative result and a recoverable conflict response for the losing request.
- [ ] **C18.06.08** Retain constraint definitions and concurrency evidence; accept when calendar changes and parallel launches cannot create competing active legs.

### Control C18 07

**Original requirement C18.07:** Specify legal transitions such as reserved, generating, ready, active, interrupted, completed, and failed-generation; failed generation must not advance the route or consume another expedition day silently.

- [ ] **C18.07.01** Define a transition table for reserved, generating, ready, active, interrupted, completed, and failed-generation states with permitted triggers and responsible operations.
- [ ] **C18.07.02** Specify required fields and artifact availability for each state, including whether the user may view, exercise, decide, retry generation, or complete the day.
- [ ] **C18.07.03** Apply state changes with expected revision checks and record the triggering run, operation identity, timestamp, and reason.
- [ ] **C18.07.04** Represent interrupted generation and interrupted workouts separately where needed so resuming content production cannot fabricate accepted physical activity.
- [ ] **C18.07.05** Keep generation failures associated with their reserved day and seed; retry that reservation without consuming another expedition sequence or advancing continuation.
- [ ] **C18.07.06** Exercise every permitted transition and verify the resulting capabilities, revisions, and audit references against the transition table.
- [ ] **C18.07.07** Attempt completion from failed-generation, reopening a completed day as active, and duplicate generating transitions; verify the specified rejection or idempotent behavior.
- [ ] **C18.07.08** Retain the transition table and transition coverage results; accept when failures remain recoverable within the existing day and cannot silently advance the hike.

### Control C18 08

**Original requirement C18.08:** Resume the current incomplete day and its pinned choices/resources on restart; create the next day only when no incomplete day exists and the campaign continuation permits it.

- [ ] **C18.08.01** Define startup selection precedence: validate campaign, locate its existing unfinished day, reconcile artifacts, and resume that day before considering a new reservation.
- [ ] **C18.08.02** Restore the pinned dossier, stored choices, fictional resource state, accepted activity credits, and journal references from authoritative records.
- [ ] **C18.08.03** Permit next-day reservation only when no unfinished day exists and the committed continuation pointer identifies an eligible route position.
- [ ] **C18.08.04** Specify handling for ready, interrupted, and failed-generation days, preserving their identifiers while applying the appropriate resume or repair action.
- [ ] **C18.08.05** Expose review access to completed days separately from the resume target so browsing history cannot change which leg the next launch selects.
- [ ] **C18.08.06** Close and reopen during several points in one day; verify the same day ID, content revision, choices, resources, and remaining requirements.
- [ ] **C18.08.07** Reopen an old browser URL after a later completion and request a new day during an unfinished reservation; verify history viewing or a clear conflict without advancement.
- [ ] **C18.08.08** Retain startup selection traces and resumed-state comparisons; accept when every launch resumes or reserves exactly the day justified by committed history.

### Control C18 09

**Original requirement C18.09:** Define explicit completion criteria and a deliberate complete-day operation; require accepted activity/preparation and resolved or rule-permitted mandatory deferrals with deliberate acknowledgment and source-day identity. Carryover cannot implicitly complete a later day or bypass its required decisions.

- [ ] **C18.09.01** Specify the day-completion predicate using accepted activity or preparation requirements, mandatory decision dispositions, route endpoint rules, and campaign mode.
- [ ] **C18.09.02** Require a deliberate user completion action showing the source day and resulting endpoint; do not infer consent from reaching distance or closing a browser.
- [ ] **C18.09.03** Store whether each mandatory interaction was resolved or deferred under an identified rule, including the relevant rule version and user acknowledgement.
- [ ] **C18.09.04** Allocate carryover credits causally and distinguish available credit from accepted completion; future-day decisions and acknowledgements remain independently required.
- [ ] **C18.09.05** Return specific unmet requirements without discarding workouts, choices, or draft journal content when completion is rejected.
- [ ] **C18.09.06** Satisfy one day's requirements, deliberately complete it, and verify one advancement with evidence linking accepted activity and interaction dispositions.
- [ ] **C18.09.07** Attempt completion using surplus distance alone, unresolved mandatory choices, unallocated or ineligible credits, and an unacknowledged deferral; verify no next-pointer mutation.
- [ ] **C18.09.08** Retain completion policy, eligible and ineligible examples, and acknowledgement records; accept when advancement reflects an explicit, fully qualified source-day decision.

### Control C18 10

**Original requirement C18.10:** Commit the day-completion record, status, final route position, causal credits, and next-leg pointer within one SQLite transaction with an idempotency key and expected campaign revision.

- [ ] **C18.10.01** Define one completion operation containing campaign ID, source day ID, expected revision, idempotency key, and the acknowledged completion intent.
- [ ] **C18.10.02** Validate eligibility and position against authoritative records within the same transaction that will finalize completion, preventing checks from becoming stale before commit.
- [ ] **C18.10.03** Commit DayCompletion, source-day completed status, final route position, causal credit allocations, and the campaign continuation pointer together in one SQLite transaction.
- [ ] **C18.10.04** Enforce unique operation and source-day completion constraints, and increment the relevant aggregate revisions within the successful transaction.
- [ ] **C18.10.05** Keep file rendering and external notifications outside the completion transaction; expose authoritative completion before retryable derivative exports finish.
- [ ] **C18.10.06** Complete a valid day and inspect all affected records, proving matching operation identity, route position, revision, and credit allocations.
- [ ] **C18.10.07** Inject failure before commit and lose the response after commit; verify respectively zero advancement or one queryable completed operation with safe replay.
- [ ] **C18.10.08** Retain transaction design, fault results, and reconciled record sets; accept when completion has exactly one committed effect despite crashes or retries.

### Control C18 11

**Original requirement C18.11:** Return the existing completion result on repeated submission; enforce unique completion per day and reject stale tabs attempting to complete a superseded day.

- [ ] **C18.11.01** Define the stored completion receipt returned for repeated requests, including operation identity, source day, resulting revision, final position, and next-pointer summary.
- [ ] **C18.11.02** Require one completion record per day and distinguish replay of the same operation from a new conflicting request using another idempotency key.
- [ ] **C18.11.03** Check expected source-day revision and campaign continuation context before accepting a previously unseen completion request.
- [ ] **C18.11.04** Allow an identical committed replay to retrieve its original receipt without allocating credits again or changing the current active day.
- [ ] **C18.11.05** Return a precise stale-day or already-completed result for a superseded browser tab, including enough identity information to refresh safely.
- [ ] **C18.11.06** Repeat one successful completion through browser retry and service restart; verify unchanged completion count, balances, and continuation pointer.
- [ ] **C18.11.07** Submit an old tab's completion after subsequent progress and submit changed payload under an existing key; verify no new effects and an explicit conflict.
- [ ] **C18.11.08** Retain duplicate and stale-request traces; accept when retries are reproducible and historical browser state cannot complete or overwrite the current leg.

### Control C18 12

**Original requirement C18.12:** Reserve a next-day identifier and route range transactionally; simultaneous launcher requests must receive the same reservation rather than two adjacent legs.

- [ ] **C18.12.01** Define a reservation operation that reads the committed continuation pointer and allocates the next day identity and route range within a short transaction.
- [ ] **C18.12.02** Validate absence of an unfinished reservation and eligibility of the next route range before inserting the reserved HikeDay.
- [ ] **C18.12.03** Persist expedition sequence, selected stage, route release, position bounds, seed, and manifest selection according to the reservation contract.
- [ ] **C18.12.04** Use campaign revision and uniqueness constraints to coordinate parallel launchers and HTTP clients requesting the same next day.
- [ ] **C18.12.05** Return the existing compatible reservation to repeated requests, while rejecting conflicting route or manifest expectations without reserving another leg.
- [ ] **C18.12.06** Reserve after a completed day and verify that the new range begins at the committed continuation position with one incremented sequence.
- [ ] **C18.12.07** Race multiple reservation requests and interrupt one caller after commit; verify all successful retries resolve to one day identity and route range.
- [ ] **C18.12.08** Retain reservation transaction traces and race-test results; accept when concurrent entry points cannot consume two expedition days from one continuation state.

### Control C18 13

**Original requirement C18.13:** Separate the database transaction from filesystem snapshot publication using staged artifacts, manifest checksums, publication markers, and startup reconciliation; do not claim atomicity across the database and files.

- [ ] **C18.13.01** Order generation stages as temporary creation, checksum verification, verified same-volume promotion, then SQLite publication marking and registration, with explicit recoverable boundaries.
- [ ] **C18.13.02** Record intended day, job, manifest, seed, artifact revision, and checksums in staging metadata so startup can attribute leftovers without guessing from filenames.
- [ ] **C18.13.03** Publish only verified complete artifacts, and ensure the database never exposes an unverified staging directory as the current dossier.
- [ ] **C18.13.04** Document each ordering window between filesystem publication and database updates; specify reconciliation for published-but-unregistered and registered-but-missing artifacts.
- [ ] **C18.13.05** Quarantine ambiguous or corrupt output and regenerate against the same reservation when safe; do not advance the day to bypass publication failure.
- [ ] **C18.13.06** Generate and reopen a dossier, confirming the stored manifest, publication marker, database reference, and actual file checksums agree.
- [ ] **C18.13.07** Interrupt each publication boundary and restart; verify deterministic reconciliation with either one valid published revision or a clearly recoverable existing-day failure.
- [ ] **C18.13.08** Retain publication protocol and boundary fault evidence; accept when recovery is proven without claiming a combined SQLite and filesystem atomic transaction.

### Control C18 14

**Original requirement C18.14:** Configure and verify SQLite journaling, synchronization, busy handling, and connection ownership for the selected storage environment; pin a supported dependency version and review known integrity defects before release.

- [ ] **C18.14.01** Document the chosen journal mode, synchronization setting, connection lifetime, timeout, storage assumptions, and supported SQLite runtime for repository-local operation.
- [ ] **C18.14.02** Apply required connection settings consistently to launcher utilities, service workers, maintenance commands, and export or recovery readers.
- [ ] **C18.14.03** Define bounded busy handling and retry rules distinguishing lock contention, disk exhaustion, permission failure, corruption, and unsupported storage behavior.
- [ ] **C18.14.04** Review relevant runtime integrity defects before version adoption, recording applicability and mitigation rather than assuming a version pin alone establishes safety.
- [ ] **C18.14.05** Specify journal and sidecar handling for backup, shutdown, relocation, and recovery under the selected storage configuration.
- [ ] **C18.14.06** Measure concurrent read and write behavior on supported storage and verify durability expectations after normal shutdown and controlled interruption.
- [ ] **C18.14.07** Exercise locked database, unavailable storage, disk-full, and integrity-check failure paths; verify no unsafe fallback, hidden history reset, or endless retry.
- [ ] **C18.14.08** Retain configuration, runtime provenance, storage qualification, and failure results; accept when durability and contention behavior match the stated local deployment assumptions.

### Control C18 15

**Original requirement C18.15:** Persist immutable causal records and apply audited corrections or compensating credits; define whether revised training affects future position, historical annotations, or a deliberate campaign repair without silently rewriting decisions.

- [ ] **C18.15.01** Identify immutable causal records for workouts, accepted credits, decisions, completions, resource effects, and pointer movements, and prohibit ordinary edits from rewriting them.
- [ ] **C18.15.02** Define correction records with original reference, reason, author or local actor, timestamp, expected revision, and compensating quantities where applicable.
- [ ] **C18.15.03** Specify how corrections affect summaries, remaining credit, and future planning while preserving the original historical events and their route context.
- [ ] **C18.15.04** Separate annotations from deliberate campaign repair; require repair operations to state the resulting pointer and affected reservations explicitly.
- [ ] **C18.15.05** Reject automatic reinterpretation of old branches under new rule or route releases unless a reviewed migration defines the intended transformation.
- [ ] **C18.15.06** Correct an overreported workout and verify the original remains visible, compensation reconciles totals, and future credit follows the documented policy.
- [ ] **C18.15.07** Correct activity already consumed by a completed day and attempt a silent historical rewrite; verify the selected repair or annotation policy without unexplained route changes.
- [ ] **C18.15.08** Retain correction examples and reconciliation reports; accept when every adjusted total and future position can be traced through preserved causal history.

### Control C18 16

**Original requirement C18.16:** Export run/day history in documented JSON or JSON Lines derived from committed records; treat exports and diagnostics as views, not competing sources of next-leg truth.

- [ ] **C18.16.01** Define versioned JSON or JSONL export schemas for run and day history, including campaign identity, record identities, revisions, timestamps, and source database snapshot metadata.
- [ ] **C18.16.02** Generate exports from a consistent committed database view and include counts or checksums that support checking completeness and transport integrity.
- [ ] **C18.16.03** Represent interrupted runs, unfinished days, corrections, and completion links explicitly rather than flattening them into misleading calendar-day summaries.
- [ ] **C18.16.04** Document that these exports are derivative reports and cannot become the next-leg authority merely because their filenames or timestamps appear newer.
- [ ] **C18.16.05** Provide a separate validated import or restore workflow if supported, with campaign compatibility checks and an explicit conflict policy.
- [ ] **C18.16.06** Export a campaign containing repeated launches and partial workouts; reconcile record counts and key relationships against the committed database snapshot.
- [ ] **C18.16.07** Modify, truncate, reorder, or delete an exported history file and relaunch; verify repository progress remains authoritative and export errors are reported accurately.
- [ ] **C18.16.08** Retain export schema and reconciliation evidence; accept when history is portable and intelligible without introducing a competing source of progression state.

### Control C18 17

**Original requirement C18.17:** Perform consistent database backups with required snapshot manifests and verify restoration; when WAL is enabled, use a supported consistent backup method rather than assuming a copied main database file contains every commit.

- [ ] **C18.17.01** Define a backup procedure obtaining a consistent SQLite snapshot through a supported mechanism and pairing it with the referenced dossier and content manifest inventory.
- [ ] **C18.17.02** Record campaign identity, schema version, application compatibility, backup time, database integrity result, artifact revisions, and checksums in the backup manifest.
- [ ] **C18.17.03** Preserve required committed state when journaling sidecars are active; prohibit treating an arbitrary copy of the main database file alone as a verified backup.
- [ ] **C18.17.04** Write and verify the backup before marking it successful, retaining the previous usable backup when the new attempt is interrupted or incomplete.
- [ ] **C18.17.05** Restore into a validated target with clear conflict handling, then reconcile missing generated files without changing committed completion history.
- [ ] **C18.17.06** Restore a campaign with an unfinished day and several completed legs; verify the exact continuation pointer, active day, choices, credits, and journal links.
- [ ] **C18.17.07** Interrupt backup, corrupt one artifact, and supply a manifest from another campaign; verify precise rejection or documented recovery without overwriting valid local history.
- [ ] **C18.17.08** Retain successful restore evidence and backup failure results; accept when the backup recovers authoritative progress and identifies every required or reproducible artifact.

### Control C18 18

**Original requirement C18.18:** Define relocation, Git checkout/update, cleanup, reset, and uninstall behavior; exclude personal state and private logs from accidental publication and preserve user history unless an explicit reset is requested.

- [ ] **C18.18.01** Classify repository files as application source, versioned content, generated dossiers, personal state, diagnostics, temporary artifacts, and backups with explicit lifecycle rules.
- [ ] **C18.18.02** Exclude personal database, journals, workout history, credentials, and private diagnostics from default Git publication and distributable application packages.
- [ ] **C18.18.03** Resolve persistent paths relative to the repository after relocation and validate campaign identity before using an existing database at the new location.
- [ ] **C18.18.04** Specify update and cleanup operations that preserve authoritative state and required published artifacts while removing only known reproducible or expired temporary files.
- [ ] **C18.18.05** Make reset and uninstall data removal separate explicit actions identifying affected campaigns, backups, and exports, with a recoverable option where supported.
- [ ] **C18.18.06** Move the repository, apply an application update, and perform routine cleanup; verify the same campaign resumes with identical committed progress.
- [ ] **C18.18.07** Inspect Git status and a release package, then exercise reset cancellation; verify private state stays excluded and cancellation leaves history intact.
- [ ] **C18.18.08** Retain lifecycle inventory, relocation results, and package inspection evidence; accept when ordinary maintenance preserves the user's hike and deliberate removal has clear scope.

### Control C18 19

**Original requirement C18.19:** Test same-day relaunch, multi-day absence, midnight, clock rollback, duplicate completion, concurrent reservation, final trail endpoint, alternate route, and edited itinerary; reconcile all next positions against expected route state.

- [ ] **C18.19.01** Create a progression fixture covering unfinished days, completed legs, alternate branches, route endpoints, itinerary edits, and several calendar dates.
- [ ] **C18.19.02** Specify expected run counts, active day identity, continuation positions, completion counts, and credit balances before executing each lifecycle scenario.
- [ ] **C18.19.03** Test immediate relaunch, long absence, midnight crossing, timezone change, and clock rollback while preserving the same unresolved expedition day.
- [ ] **C18.19.04** Test duplicate completion and concurrent reservation with controlled request ordering, verifying both committed results and caller-visible receipts.
- [ ] **C18.19.05** Test route endpoint, alternate route selection, and edited itinerary under explicit compatibility rules; prohibit silently substituting a new route release.
- [ ] **C18.19.06** Compare each observed database state and browser resume target with the independently written expected ledger and route positions.
- [ ] **C18.19.07** Repeat failed or ambiguous scenarios with recorded operation identities and fault timing, ensuring diagnostics explain the discrepancy without private journal disclosure.
- [ ] **C18.19.08** Retain the lifecycle matrix and reconciled results; accept when every listed scenario preserves or deliberately changes progression exactly as specified.

### Control C18 20

**Original requirement C18.20:** Inject failure before/after reservation, snapshot publication, completion commit, and backup; test integrity checks and restore, showing that the latest committed leg is retained and unresolved generation is recoverable.

- [ ] **C18.20.01** Identify fault injection points before and after reservation commit, snapshot promotion, publication registration, completion commit, and backup verification.
- [ ] **C18.20.02** Define an expected recovery state for each point, including surviving records, artifact disposition, operation receipt, active day, and continuation pointer.
- [ ] **C18.20.03** Use isolated test repositories and controlled termination or injected exceptions so production personal history is never used as destructive test material.
- [ ] **C18.20.04** Run integrity checks and relationship reconciliation after each restart, then validate the restored application's visible dossier and next-leg selection.
- [ ] **C18.20.05** Verify generation can retry the original day and manifest after a recoverable artifact failure without discarding accepted workouts or decisions.
- [ ] **C18.20.06** Demonstrate that precommit failures preserve the previous committed position and postcommit failures retain exactly the new committed position.
- [ ] **C18.20.07** Restore from the last verified backup after an intentionally unrecoverable test corruption and quantify any expected records outside that backup's recovery point.
- [ ] **C18.20.08** Retain fault timing, integrity results, and recovery comparisons; accept when every durable boundary preserves the last valid commit or a documented verified restore.

## C19 Loopback HTTP service and local dossier delivery

**Accountable owner:** Local service owner. **Technical owner:** Service/domain engineering. **Reviewers:** Security, content, reliability, and interface engineering.

**Inputs:** Validated repository configuration, authoritative database, published dossier snapshots, local media catalog, and browser requests. **Outputs:** Loopback pages, versioned API responses, commit receipts, and health/readiness status.

**Required evidence:** API specification; bind/origin/path tests; domain mutation validation; generation/recovery traces; concurrency and commit-retry results; health protocol; startup/shutdown tests.

**Exit criterion:** The service serves the correct saved dossier through the intended loopback origin, durably processes validated interactions, survives restart without changing established outcomes, and does not expose private repository files.

### Control C19 01

**Original requirement C19.01:** Bind explicitly to `127.0.0.1` at the selected port; verify that wildcard, LAN, and unintended IPv6 listeners are not created by runtime defaults.

- [ ] **C19.01.01** Define the supported listening address as explicit IPv4 loopback 127.0.0.1 and specify the configured port and any documented fallback range.
- [ ] **C19.01.02** Construct the listener from validated address and port settings; prohibit wildcard, machine-name, LAN-address, or implicit dual-stack binding in normal local mode.
- [ ] **C19.01.03** Report the actual bound address, port, and owned instance identity to the launcher before any browser navigation or readiness acknowledgement.
- [ ] **C19.01.04** Reject invalid or occupied ports with an attributable launch result; use a fallback only when the configured policy permits it.
- [ ] **C19.01.05** Keep any future remote-access mode separately configured and reviewed rather than allowing a local setting to accidentally expose the service.
- [ ] **C19.01.06** Inspect listening sockets after startup and verify the browser's advertised URL matches the exact reachable loopback endpoint.
- [ ] **C19.01.07** Attempt access through a LAN address, wildcard configuration, and unintended IPv6 listener; verify the local mode exposes no such listener.
- [ ] **C19.01.08** Retain binding configuration and socket inspection results; accept when the service is reachable only through its declared loopback address and selected port.

### Control C19 02

**Original requirement C19.02:** Serve interface and API from the intended local origin; define accepted Host/Origin values and refuse arbitrary cross-origin mutations or wildcard cross-origin access.

- [ ] **C19.02.01** Define the accepted local origin and Host values using the actual selected loopback port, including a clear policy for optional localhost aliases.
- [ ] **C19.02.02** Validate Host on requests and Origin on browser mutations against the active instance configuration rather than reflecting arbitrary client headers.
- [ ] **C19.02.03** Disable wildcard cross-origin permission and permit only specifically required origins, methods, and headers if any cross-origin access is supported.
- [ ] **C19.02.04** Handle requests with absent, malformed, null, or unexpected Origin according to endpoint type and the declared browser or maintenance-client policy.
- [ ] **C19.02.05** Reject mismatched authority, alternate ports, and rebinding-style hostnames before reading private campaign data or applying mutations.
- [ ] **C19.02.06** Exercise the supported browser workflow using the actual selected origin and verify all necessary reads and writes succeed.
- [ ] **C19.02.07** Send forged Host, foreign Origin, preflight, and alternate-port requests; verify rejection without state effects or permissive reflected access headers.
- [ ] **C19.02.08** Retain origin policy and request matrix results; accept when only the intended local browser context can invoke the declared campaign operations.

### Control C19 03

**Original requirement C19.03:** Protect mutating requests with an instance-specific request policy such as a validated nonce and exact-origin checks; reject unsafe methods/content types and do not use GET requests to advance hike state.

- [ ] **C19.03.01** Issue an unpredictable instance-specific mutation nonce and define its lifetime, browser delivery mechanism, and invalidation on owned-service restart.
- [ ] **C19.03.02** Validate nonce, intended origin, supported method, and content type before processing any workout, decision, journal, completion, export, or shutdown mutation.
- [ ] **C19.03.03** Keep mutating actions out of GET and HEAD handlers, including convenience URLs that would otherwise advance a day or stop the service.
- [ ] **C19.03.04** Avoid embedding the nonce in URLs, diagnostic output, exported history, or media requests where it could spread through logs or referrers.
- [ ] **C19.03.05** Define a safe refresh path for an expired instance token that preserves unsaved user input and does not replay a mutation automatically.
- [ ] **C19.03.06** Perform valid browser mutations and confirm their receipts map to the intended instance, campaign, operation, and resulting revision.
- [ ] **C19.03.07** Submit absent, incorrect, and previous-instance nonces, unexpected content types, and mutation-shaped GET requests; verify no authoritative changes occur.
- [ ] **C19.03.08** Retain token lifecycle and method-validation evidence; accept when stale or foreign request contexts cannot mutate the local hike.

### Control C19 04

**Original requirement C19.04:** Expose health and readiness endpoints containing application/protocol/instance/repository identity and readiness state without leaking private notes, database contents, or secrets.

- [ ] **C19.04.01** Define separate liveness and readiness responses, distinguishing a running listener from a service able to open compatible state and serve the selected dossier.
- [ ] **C19.04.02** Include application version, protocol version, owned instance ID, nonsecret repository identity, and readiness status with stable machine-readable field names.
- [ ] **C19.04.03** Specify readiness gates for database compatibility, campaign reconciliation, required assets, and generation state without exposing internal private paths or secrets.
- [ ] **C19.04.04** Return structured unavailable or initializing reasons with bounded retry guidance so the launcher can distinguish recoverable startup from incompatible service reuse.
- [ ] **C19.04.05** Keep private journal text, database credentials, mutation nonce, workout details, and complete filesystem paths outside ordinary health responses.
- [ ] **C19.04.06** Start a healthy instance and verify the launcher validates identity and readiness before opening the current dossier URL.
- [ ] **C19.04.07** Probe an unrelated listener, incompatible protocol, missing artifact, and locked database; verify readiness cannot falsely authorize browser launch or instance reuse.
- [ ] **C19.04.08** Retain response schemas and readiness-gate results; accept when health endpoints support reliable startup while exposing only the minimum operational identity.

### Control C19 05

**Original requirement C19.05:** Define API schemas for campaign state, current dossier, day reservation, workouts, decisions, journal edits, complete-day, export, and shutdown; specify validation, error codes, revisions, and idempotency semantics.

- [ ] **C19.05.01** Inventory API operations for campaign state, current dossier, reservation, workout, decision, journal, completion, export, and owned shutdown with explicit supported methods.
- [ ] **C19.05.02** Define request and response schemas with required identifiers, units, bounds, optional fields, expected revisions, operation keys, and compatibility version.
- [ ] **C19.05.03** Specify consistent validation, authorization-context, conflict, unavailable, and internal-error responses with stable codes and safe user-facing explanations.
- [ ] **C19.05.04** Declare which operations are idempotent, how replay payloads are compared, and which committed receipt can be retrieved after an uncertain response.
- [ ] **C19.05.05** Version contract changes and define client compatibility behavior before permitting mutations through an outdated browser shell.
- [ ] **C19.05.06** Execute one valid request and response example for every endpoint, checking schema conformance and expected durable or read-only effects.
- [ ] **C19.05.07** Exercise missing fields, unknown identities, unit mismatches, stale revisions, duplicate keys, and unsupported methods; verify predictable rejection and preserved state.
- [ ] **C19.05.08** Retain the API contract and conformance results; accept when every public operation has an unambiguous validation, revision, replay, and error policy.

### Control C19 06

**Original requirement C19.06:** Validate all browser-provided identifiers and quantities against current database state; never trust a submitted next-leg position, resource balance, completion flag, or derived physical total as authoritative.

- [ ] **C19.06.01** Classify client fields as user-entered observations, requested actions, expected revisions, and display-only derived values with explicit server handling rules.
- [ ] **C19.06.02** Validate campaign, source day, session, decision option, and correction references against authoritative records and their permitted relationships.
- [ ] **C19.06.03** Compute next position, resource balances, completion eligibility, and accepted physical totals on the service from stored inputs and versioned rules.
- [ ] **C19.06.04** Reject or ignore browser-supplied derived balances and route pointers according to the API contract, without using them as authoritative substitutes.
- [ ] **C19.06.05** Validate numeric finiteness, units, reasonable schema bounds, timestamp semantics, and manual-entry classification before recording physical observations.
- [ ] **C19.06.06** Submit valid observations and decisions, then compare service-derived totals and consequences with independently calculated fixture expectations.
- [ ] **C19.06.07** Tamper with completion eligibility, mileage totals, resource balances, route positions, and another campaign's references; verify no unauthorized effects.
- [ ] **C19.06.08** Retain field authority classifications and tampering results; accept when browser input can request or report actions without determining authoritative progression.

### Control C19 07

**Original requirement C19.07:** Limit static serving to explicitly configured interface, published dossier, and approved media roots; disable directory listings and reject path traversal, symlink/reparse escapes, and database/config/backup disclosure.

- [ ] **C19.07.01** Define explicit served roots for interface assets, verified published dossiers, and approved media, keeping database, journals, backups, source configuration, and staging outside them.
- [ ] **C19.07.02** Resolve requested resources through an allowlisted mapping or canonical path validation that remains inside the selected served root.
- [ ] **C19.07.03** Disable directory listing and reject traversal, absolute paths, encoded separators, unexpected file types, and private dotfiles according to the resource contract.
- [ ] **C19.07.04** Validate symlinks, junctions, and other reparse targets so a nominally allowed resource cannot resolve into private repository or external directories.
- [ ] **C19.07.05** Serve a missing or withdrawn asset with a safe error or declared replacement without exposing filesystem paths or falling back to arbitrary file reads.
- [ ] **C19.07.06** Load all documented interface and dossier resources, confirming their paths, media types, checksums, and attribution requirements.
- [ ] **C19.07.07** Attempt traversal and reparse escapes plus direct database, journal, backup, and staging requests; verify none expose private content.
- [ ] **C19.07.08** Retain root configuration and resource-access tests; accept when published content is reachable and private repository material has no HTTP retrieval path.

### Control C19 08

**Original requirement C19.08:** Serve the selected published dossier revision and its pinned asset manifest; a browser refresh must not trigger a new random event selection or regenerate a different day.

- [ ] **C19.08.01** Define each served dossier by day ID, published revision, manifest identity, pinned seed, and artifact checksums rather than an unversioned generated folder.
- [ ] **C19.08.02** Resolve the current dossier pointer from committed publication records and require the referenced revision to pass readiness and integrity checks.
- [ ] **C19.08.03** Keep refresh, repeat GET, and browser reattachment read-only with respect to generation seed, narrative choices, and published content.
- [ ] **C19.08.04** Expose explicit regeneration or correction as a separate revisioned operation with policy for preserving completed-day history and user decisions.
- [ ] **C19.08.05** Represent withdrawn or missing pinned content through a traceable replacement or recovery disposition instead of silently changing the dossier.
- [ ] **C19.08.06** Refresh one published day repeatedly across process restarts and verify identical narrative inputs, media inventory, and manifest identity.
- [ ] **C19.08.07** Replace a file without updating the manifest and request an obsolete revision; verify integrity failure or historical handling rather than current-day substitution.
- [ ] **C19.08.08** Retain publication lookup and repeat-read evidence; accept when the same dossier revision remains stable until an explicit attributable publication change.

### Control C19 09

**Original requirement C19.09:** Generate missing dossiers through a recoverable job keyed to day identity, content manifest, and scenario seed; repeated requests share the same job and cannot reserve another leg.

- [ ] **C19.09.01** Define the generation job key from reserved day, pinned manifest, seed, generator version, and other reproducibility inputs declared by the content pipeline.
- [ ] **C19.09.02** Persist job identity, status, attempts, timestamps, result revision, and recoverable failure information tied to the existing reservation.
- [ ] **C19.09.03** Return or attach to an existing compatible job when repeated browser or launcher requests ask for the same generation.
- [ ] **C19.09.04** Coordinate job ownership across workers or processes so only one active producer publishes a given job result at a time.
- [ ] **C19.09.05** Define cancellation and retry rules that preserve the day reservation and deterministic inputs while avoiding partial artifacts masquerading as published output.
- [ ] **C19.09.06** Issue repeated generation requests and verify one reservation, one logical job, and one valid publication with queryable progress.
- [ ] **C19.09.07** Race callers, crash the producer, and retry after restart; verify ownership recovery without additional days or inconsistent duplicate snapshots.
- [ ] **C19.09.08** Retain job-key design and concurrency results; accept when repeated generation requests recover or share the existing day's work.

### Control C19 10

**Original requirement C19.10:** Supply valid content types, text encoding, cache validators, and revision-aware asset URLs; keep personal state responses out of public caches and prevent stale assets from impersonating current snapshots.

- [ ] **C19.10.01** Define media types, character encoding, content-disposition behavior, validators, and cache directives for interface assets, dossier resources, and private API responses.
- [ ] **C19.10.02** Use revisioned asset URLs or content hashes for immutable published resources and validate that their bytes correspond to the declared revision.
- [ ] **C19.10.03** Mark private campaign state and mutation receipts with the selected restrictive cache policy, avoiding shared-cache storage of activity or journal content.
- [ ] **C19.10.04** Specify conditional request behavior and ensure a validator from another revision cannot produce a misleading unchanged response.
- [ ] **C19.10.05** Version the browser shell and manifest relationship so stale cached code detects incompatibility before sending mutations to a changed service.
- [ ] **C19.10.06** Inspect response headers and exercise normal reload, conditional retrieval, and content revision updates in the supported browser matrix.
- [ ] **C19.10.07** Reuse stale validators and cached assets after an update, and inspect private responses; verify correct freshness and no private public-cache permission.
- [ ] **C19.10.08** Retain header contracts and cache tests; accept when caching improves delivery without substituting stale assets for the current authoritative state.

### Control C19 11

**Original requirement C19.11:** Keep slow image processing, optional external lookup, and dossier assembly outside short state-update transactions; document cancellation and keep status/workout endpoints responsive.

- [ ] **C19.11.01** Classify slow work such as content lookup, image processing, report assembly, and optional generation separately from short authoritative database transactions.
- [ ] **C19.11.02** Execute slow work through bounded jobs with progress, timeout, cancellation, and retained input identities rather than holding write locks across it.
- [ ] **C19.11.03** Keep health, status, resume reads, and interruption controls responsive while generation or export is running within declared local resource limits.
- [ ] **C19.11.04** Perform a final revision and eligibility check when slow preparation leads to a mutation, preventing stale precomputed results from overwriting newer state.
- [ ] **C19.11.05** Specify cancellation cleanup for temporary files and job records while preserving existing reservations, accepted workouts, and previously published artifacts.
- [ ] **C19.11.06** Run a deliberately slow content job while polling status and saving an independent permitted action; measure responsiveness against the declared budget.
- [ ] **C19.11.07** Cancel and restart jobs, exhaust worker capacity, and introduce a stale revision; verify bounded responses and no long-held campaign write transaction.
- [ ] **C19.11.08** Retain timing and lock-duration evidence; accept when slow dossier work remains recoverable and does not freeze essential local controls.

### Control C19 12

**Original requirement C19.12:** Serialize or coordinate writes with explicit database transaction ownership, bounded contention handling, and unique operation identifiers; do not share unsafe mutable campaign objects across concurrent requests.

- [ ] **C19.12.01** Define write ownership and connection usage for campaign mutations, avoiding shared mutable in-memory balances or pointers as the source of truth.
- [ ] **C19.12.02** Use short transactions, unique operation constraints, and expected revisions to serialize conflicting effects while permitting safe independent reads.
- [ ] **C19.12.03** Bound database busy waits and retries, returning a recoverable status that preserves user drafts and operation identities when contention remains unresolved.
- [ ] **C19.12.04** Specify ordering for dependent decisions, credit allocations, resource effects, and completion so concurrent requests cannot violate causal prerequisites.
- [ ] **C19.12.05** Discard or revalidate cached campaign state after another writer commits, including requests originating from another tab or launcher process.
- [ ] **C19.12.06** Run concurrent workout saves and decisions, then reconcile all accepted receipts with the authoritative ledger and resulting revisions.
- [ ] **C19.12.07** Race conflicting choices and completion, hold a write lock, and duplicate an operation; verify one valid ordering with no lost or repeated effect.
- [ ] **C19.12.08** Retain concurrency design and reconciliation results; accept when simultaneous clients produce a consistent durable campaign without unsafe shared-state shortcuts.

### Control C19 13

**Original requirement C19.13:** Return success after commit, including effective revision and operation identity; an acknowledgement lost after commit must be recoverable through retry or operation-status lookup.

- [ ] **C19.13.01** Define mutation receipts containing operation key, campaign and source identity, committed revision, effect summary, and completion status.
- [ ] **C19.13.02** Send a success response only after the authoritative transaction commits; distinguish accepted background work from a durable completed mutation.
- [ ] **C19.13.03** Store enough operation identity and result data to query a receipt after connection loss, browser timeout, or service restart.
- [ ] **C19.13.04** Compare replayed payloads under existing keys and reject changed requests instead of returning a misleading success for different intent.
- [ ] **C19.13.05** Have the browser present uncertain save status until lookup or safe replay establishes the outcome, retaining the original draft and operation key.
- [ ] **C19.13.06** Complete ordinary mutations and verify each successful receipt corresponds to exactly one committed effect and the correct resulting revision.
- [ ] **C19.13.07** Drop the response after commit and interrupt before commit; verify lookup and replay resolve respectively one existing effect or one safely retried effect.
- [ ] **C19.13.08** Retain receipt schemas and lost-acknowledgement tests; accept when displayed success means durability and uncertain responses never cause duplicate progress.

### Control C19 14

**Original requirement C19.14:** Rehydrate state from the database on restart and reconcile reserved jobs, staging files, publication markers, and active sessions; do not initialize an empty hike merely because browser state is absent.

- [ ] **C19.14.01** Define startup rehydration from the repository database, including campaign identity, active day, continuation pointer, accepted activity, choices, and operation receipts.
- [ ] **C19.14.02** Reconcile persisted generation jobs, staging metadata, publication markers, and dossier references before declaring the affected day ready.
- [ ] **C19.14.03** Classify interrupted workout intervals and expired local session ownership without treating offline elapsed time as proven treadmill movement.
- [ ] **C19.14.04** Recover resumable work or expose a precise repair state for ambiguous artifacts, preserving the existing reserved day and its pinned inputs.
- [ ] **C19.14.05** Ignore absent or empty browser storage as a reset signal; require an explicit repository initialization or user-authorized reset workflow.
- [ ] **C19.14.06** Restart with a fresh browser profile and verify identical committed progress, active dossier, prior choices, and remaining completion requirements.
- [ ] **C19.14.07** Crash during generation, session saving, and publication registration; verify attributable reconciliation without a new empty campaign or next-leg jump.
- [ ] **C19.14.08** Retain startup recovery traces and state comparisons; accept when repository history alone restores the hike independently of browser cache.

### Control C19 15

**Original requirement C19.15:** Validate schema compatibility before accepting mutations, back up before migrations where appropriate, and stop with a precise error if the schema is newer than the supported application.

- [ ] **C19.15.01** Read database schema and compatibility metadata before permitting any campaign mutation, including apparently minor journal or run-history writes.
- [ ] **C19.15.02** Define supported schema ranges and ordered migration prerequisites for the installed service, launcher, and maintenance utilities.
- [ ] **C19.15.03** Create and verify the required backup before a migration that changes authoritative state, recording its restore procedure and source schema.
- [ ] **C19.15.04** Run migrations under exclusive coordination with explicit success metadata, rejecting concurrent service instances using incompatible assumptions.
- [ ] **C19.15.05** Refuse unsupported newer schemas with a precise explanation and preserve the database; never downgrade by recreating or partially editing it.
- [ ] **C19.15.06** Migrate a supported fixture and compare campaign positions, completions, credits, and dossier references against expected preserved values.
- [ ] **C19.15.07** Interrupt migration and open a newer unsupported fixture; verify documented recovery or refusal with no unauthorized mutation or hidden reset.
- [ ] **C19.15.08** Retain compatibility tables, backup receipts, and migration results; accept when startup protects existing history before any schema-changing work.

### Control C19 16

**Original requirement C19.16:** Sanitize rendered dossier and journal content, apply browser content protections, and isolate optional generated prose from executable rules, local filesystem access, and physical-training changes.

- [ ] **C19.16.01** Define allowed dossier and journal markup, escaping rules, link schemes, media references, and rendering boundaries for browser-visible content.
- [ ] **C19.16.02** Sanitize imported or generated text at the appropriate rendering boundary and use browser protections compatible with the approved local assets.
- [ ] **C19.16.03** Treat generated prose as content data that cannot invoke PowerShell, alter filesystem paths, change route rules, or prescribe automatic training adjustments.
- [ ] **C19.16.04** Keep narrative outcome execution in versioned structured rules with validated action identities rather than parsing instructions from displayed prose.
- [ ] **C19.16.05** Validate external links and embedded media references against content and rights policy, preserving readable text when unsafe markup is rejected.
- [ ] **C19.16.06** Render approved dossier and journal examples and verify formatting, links, accessibility, and narrative effects remain consistent with the selected contract.
- [ ] **C19.16.07** Insert script payloads, command-looking prose, unsafe URLs, and forged rule directives; verify inert display or rejection with no executable campaign effect.
- [ ] **C19.16.08** Retain sanitization fixtures and execution-boundary evidence; accept when expressive content cannot become browser script or authoritative game and training instructions.

### Control C19 17

**Original requirement C19.17:** Record request/generation errors with run, instance, job, and operation correlation while redacting private reflections and credentials; define log rotation and failure behavior when diagnostic storage fills.

- [ ] **C19.17.01** Define diagnostic events correlated by run, service instance, generation job, operation, and safe campaign reference with consistent event and failure codes.
- [ ] **C19.17.02** Specify fields that support reconstructing launch, save, publication, and recovery failures while excluding journal bodies, credentials, nonces, and unnecessary physical details.
- [ ] **C19.17.03** Set rotation, retention, maximum size, and safe handling of unavailable or full diagnostic storage appropriate to a repository-local application.
- [ ] **C19.17.04** Ensure logging failure cannot produce a false mutation receipt or crash-loop the campaign; expose a bounded diagnostic-degraded status where applicable.
- [ ] **C19.17.05** Provide a support-bundle preview with redaction and user-selected scope before any optional sharing or external transfer.
- [ ] **C19.17.06** Trace a complete launch-to-completion journey using correlation fields and verify event ordering against authoritative operation records.
- [ ] **C19.17.07** Exercise disk-full logging, repeated exceptions, and sensitive input fixtures; verify rotation limits, usable errors, and absence of prohibited details.
- [ ] **C19.17.08** Retain event schema and redaction results; accept when diagnostics explain failures without becoming an uncontrolled copy of personal hike history.

### Control C19 18

**Original requirement C19.18:** Implement ownership-validated graceful shutdown that drains or rejects new mutations, finishes bounded commits, closes database handles, and records run outcome without killing unrelated services.

- [ ] **C19.18.01** Define an owned shutdown operation requiring the active instance identity, authorized local context, and explicit lifecycle intent.
- [ ] **C19.18.02** Stop accepting new mutations, notify connected clients of shutdown state, and drain or reject in-flight work according to a bounded documented policy.
- [ ] **C19.18.03** Allow committed operations to retain queryable receipts and classify unfinished jobs or sessions for recovery before closing owned database connections.
- [ ] **C19.18.04** Record run and instance outcomes after the relevant durable work, distinguishing clean shutdown, timeout, and interrupted cleanup.
- [ ] **C19.18.05** Identify owned processes through instance evidence and prohibit terminating unrelated listeners or a reused operating-system process identifier.
- [ ] **C19.18.06** Stop during idle and active work, then restart; verify the expected committed records, interrupted classifications, and resumed day.
- [ ] **C19.18.07** Submit a stale-instance shutdown request and exceed the drain deadline in an isolated test; verify safe refusal or bounded owned-process recovery.
- [ ] **C19.18.08** Retain shutdown sequencing and ownership tests; accept when stopping the experience preserves durable history and affects only the intended service.

### Control C19 19

**Original requirement C19.19:** Test loopback binding, wrong Host/Origin, forged mutations, invalid IDs, malicious paths, oversized requests, stale revisions, repeated requests, and attempts to fetch private repository files.

- [ ] **C19.19.01** Define an HTTP protection matrix covering binding, Host, Origin, nonce, method, content type, identity relationships, payload size, revisions, replay, and private file access.
- [ ] **C19.19.02** Create valid baseline requests for each mutation so rejection tests distinguish security enforcement from an unrelated broken endpoint.
- [ ] **C19.19.03** Exercise forged origins, invalid campaign and day IDs, malicious paths, unexpected media references, and oversized payloads with specified expected errors.
- [ ] **C19.19.04** Test stale and duplicate operations against known campaign revisions, checking both response semantics and durable effect counts.
- [ ] **C19.19.05** Probe private database, backup, journal, configuration, and staging files through normal, encoded, and reparse-derived paths.
- [ ] **C19.19.06** Verify allowed browser use still succeeds after protections are enabled, including fallback port selection and supported local-origin policy.
- [ ] **C19.19.07** Reconcile the database before and after rejected requests and inspect response content for private data or sensitive diagnostic leakage.
- [ ] **C19.19.08** Retain the request matrix and state-difference evidence; accept when all listed unauthorized inputs are rejected without damaging supported local use.

### Control C19 20

**Original requirement C19.20:** Test service crash after commit but before response, stalled generation, missing assets, moved repository, port change, internet disconnection, and request concurrency; verify correct day delivery and preserved authoritative state.

- [ ] **C19.20.01** Define service resilience scenarios for postcommit response loss, stalled generation, missing assets, repository relocation, port conflict, offline startup, and concurrent callers.
- [ ] **C19.20.02** Record expected active day, completion count, continuation pointer, operation receipt, publication revision, and accepted credits for each fault boundary.
- [ ] **C19.20.03** Crash after commit before acknowledgement and verify restart exposes the original receipt, with replay adding no duplicate activity or advancement.
- [ ] **C19.20.04** Stall generation and remove a test asset, verifying responsive controls and recovery of the existing reservation without silently replacing its content manifest.
- [ ] **C19.20.05** Move the repository, occupy the preferred port, and disconnect the internet; verify supported local recovery advertises the actual endpoint and available dossier state.
- [ ] **C19.20.06** Run concurrent saves, reservations, and completions under controlled timing and reconcile all caller outcomes with committed campaign records.
- [ ] **C19.20.07** Inspect diagnostics and user-visible messages for every scenario, confirming truthful save status and actionable recovery without private-content disclosure.
- [ ] **C19.20.08** Retain the resilience matrix and restored-state comparisons; accept when local failures preserve committed progress and identify any remaining incomplete work.

## SCN Scenario design controls

**Accountable roles:** Scenario author and narrative reviewer, with geography, training, learning, rights, and accessibility review where the scenario affects those domains.

Scenario controls apply to each enabled scenario family and its released variants. Fact, observation, supplied assumption, fictional consequence, illustration, and estimate must retain their declared classifications.

### Control SCN 01

**Original requirement SCN.01:** For departure planning, supply the fictional date, daylight model, route distances, pace assumptions, alternatives, and explanation; do not hide assumptions that determine whether a choice succeeds.

- [ ] **SCN.01.01** Define departure scenarios with fictional date/timezone, daylight model/version, route-stage distances, supplied pace/rest assumptions, arrival constraints, alternatives, and conditional outcome/explanation records.
- [ ] **SCN.01.02** State which daylight values are calculated, sourced, or authored estimates; disclose all quantities and uncertainty that influence success before asking for a departure choice.
- [ ] **SCN.01.03** Separate fictional pace and arrival arithmetic from actual workout targets; choosing an earlier/later departure cannot change treadmill duration, speed, incline, or required exertion.
- [ ] **SCN.01.04** Specify handling for midnight arrival, zero/unknown pace, insufficient daylight, route changes, and multiple defensible timing priorities; prohibit hidden thresholds defining an unexplained best answer.
- [ ] **SCN.01.05** Calculate reference choices independently using the published assumptions; verify arrival time, daylight comparison, route distance, rest intervals, and virtual consequences within declared rounding tolerances.
- [ ] **SCN.01.06** Exercise boundary arrival exactly at dusk, impossible schedules, missing dates, and differing rest priorities; provide supported explanations and recoverable alternatives rather than arbitrary failure penalties.
- [ ] **SCN.01.07** Persist deferred departure choices and their scenario inputs; relaunch must restore the same fictional date, options, assumptions, and saved choice without advancing the day.
- [ ] **SCN.01.08** Archive arithmetic fixtures, prompt review, and branch walkthroughs; accept only when every outcome follows disclosed assumptions and no departure consequence alters the physical assignment.

### Control SCN 02

**Original requirement SCN.02:** For pack selection, define item identities, quantities, weight conventions, compatibility constraints, optional comfort effects, and cost rules; calculate virtual pack weight consistently with inventory.

- [ ] **SCN.02.01** Define pack-item identities, item-definition revisions, quantities, mass units, compatibility constraints, slot/category rules, optional comfort effects, acquisition costs, and inventory ownership for each scenario.
- [ ] **SCN.02.02** Specify canonical weight conversion, quantity precision, worn/carried distinctions if enabled, container/content handling, and rounding; prohibit double-counting nested items or treating unknown weight as zero.
- [ ] **SCN.02.03** Validate selected combinations against disclosed constraints and effective inventory; fictional capacity/comfort rules cannot prescribe real pack load or modify an accepted physical training target.
- [ ] **SCN.02.04** Display item-level mass contributions, compatibility explanations, cost deltas, and computed virtual pack weight before committing the choice; separate optional preferences from mandatory scenario constraints.
- [ ] **SCN.02.05** Calculate known inventories independently, including repeated items and mixed entered units; reconcile line-item totals and resulting virtual balances within the declared numeric tolerance.
- [ ] **SCN.02.06** Exercise negative quantities, unavailable items, incompatible combinations, unknown mass, and duplicated operation requests; reject invalid choices without partially charging costs or inventing equipment ownership.
- [ ] **SCN.02.07** Change or undo pack selection through approved inventory transactions; preserve causal history and recover from interrupted commits to one coherent selected pack and resource balance.
- [ ] **SCN.02.08** Archive inventory arithmetic, constraint checks, and tradeoff review; accept only when virtual weight matches committed items and every imposed restriction/cost is disclosed and reproducible.

### Control SCN 03

**Original requirement SCN.03:** For water planning, identify supplied scenario availability, uncertainty, quantities, container capacity, and relevant information sources; do not present fictional water availability as a current trail report.

- [ ] **SCN.03.01** Define water-planning scenarios with authored availability, source/observation classification, uncertainty, route positions, supplied consumption assumptions if used, quantities, container capacity, and evidence/context references.
- [ ] **SCN.03.02** Clearly label fictional availability and dated observations beside planning choices; scenario data cannot be presented as a live trail water report or operational guarantee.
- [ ] **SCN.03.03** Specify virtual refill, carrying, uncertainty, and capacity rules using explicit units; instructional assumptions cannot become personalized hydration prescriptions or automatically increase physical exercise.
- [ ] **SCN.03.04** Expose alternatives for uncertain sources and incomplete information, including conservative planning, seeking additional evidence, and deferral where authored; explain their fictional tradeoffs without concealed guarantees.
- [ ] **SCN.03.05** Independently reconcile starting quantity, container capacity, planned use, refill limits, and remaining virtual water for representative choices under the published scenario assumptions.
- [ ] **SCN.03.06** Exercise unavailable sources, unknown availability, full containers, excessive refill requests, unit mismatches, and depleted virtual balances; reject impossible transactions and preserve a continuing narrative path.
- [ ] **SCN.03.07** Resume an unfinished plan after service restart; retain original assumptions and committed resource effects, then annotate any approved scenario correction without rewriting completed history.
- [ ] **SCN.03.08** Archive quantity fixtures, classification screenshots, and subject review; accept only when all virtual arithmetic is consistent and availability is explicitly contextualized rather than represented as current fact.

### Control SCN 04

**Original requirement SCN.04:** For resupply shopping, validate item availability, unit prices, quantities, budget arithmetic, exchange rules, and transaction reversibility; provide explanations of tradeoffs rather than unexplained best-item scoring.

- [ ] **SCN.04.01** Define shopping catalogs with item/version identities, availability limits, canonical quantity units, unit prices, currency precision, budget, exchange/refund rules, and transaction operation identities.
- [ ] **SCN.04.02** Specify rounding, partial quantities, stock limits, bundled items, zero-cost items, and reversible-versus-final purchases; show every applicable condition before users commit virtual spending.
- [ ] **SCN.04.03** Calculate cart subtotals, total cost, resulting budget, inventory changes, and any pack-weight implications using shared resource/item contracts rather than separate unexplained shopping arithmetic.
- [ ] **SCN.04.04** Present sourced or authored item attributes and tradeoff explanations for cost, convenience, compatibility, and preferences; do not substitute an unexplained universally best-item score.
- [ ] **SCN.04.05** Compare reference baskets with independently calculated expected costs, balances, quantities, and weight; verify receipt line items exactly reconcile to the committed inventory/resource records.
- [ ] **SCN.04.06** Exercise insufficient budget, unavailable stock, invalid quantities, price revision, duplicate submission, and stale cart state; reject or explicitly refresh without partially spending virtual funds.
- [ ] **SCN.04.07** Interrupt purchases and approved exchanges before/after commit; retries must recover one effective receipt and reversals must create attributable compensating transactions with documented eligibility.
- [ ] **SCN.04.08** Archive arithmetic, transaction recovery, and editorial tradeoff evidence; accept only when every accepted purchase reconciles resources and inventory and every denial explains the disclosed rule.

### Control SCN 05

**Original requirement SCN.05:** For camp choice, distinguish verified location attributes from fictional stopping points and scenario-specific availability; explain distance, exposure, social, and itinerary consequences.

- [ ] **SCN.05.01** Define camp-choice records separating verified location attributes, fictional destination identity, scenario-specific availability, route positions, exposure/social assumptions, itinerary effects, and supporting evidence revisions.
- [ ] **SCN.05.02** Specify which distance, terrain, facility, and location claims are sourced versus authored; unsupported fictional stops must carry visible classification rather than implied real campsite verification.
- [ ] **SCN.05.03** Expose decision-relevant arrival distance, hypothetical exposure, social considerations, and next-stage consequences before selection; identify uncertainty and alternatives where multiple priorities remain defensible.
- [ ] **SCN.05.04** Restrict camp effects to declared fictional resources, character threads, and itinerary choices; real workout completion and physical targets remain governed by their accepted assignments.
- [ ] **SCN.05.05** Walk through contrasting camp choices with independent expected route endpoints and narrative effects; verify captions, decisions, debriefs, and tomorrow's preview use the correct classifications.
- [ ] **SCN.05.06** Exercise unavailable camps, ambiguous locations, inaccessible choices, and missing evidence; provide honest fictional/recovery alternatives or block misleading publication without stranding the campaign.
- [ ] **SCN.05.07** Defer, resume, and retry camp selection through the local service; preserve the scenario version and commit one coherent choice without early next-leg advancement.
- [ ] **SCN.05.08** Archive geographic reviews, choice-consequence maps, and recovery walkthroughs; accept only when every camp implication is disclosed and real-location claims have applicable evidence.

### Control SCN 06

**Original requirement SCN.06:** For weather response, state whether conditions are historical, hypothetical, or sourced current data; show scenario timestamps and supply authored alternatives and deferral options.

- [ ] **SCN.06.01** Define weather scenarios with condition classification, relevant source or authored assumption, timestamp/timezone, geographic scope, uncertainty, available responses, deferral, and typed consequence references.
- [ ] **SCN.06.02** Distinguish historical observations, hypothetical campaign weather, and any enabled current source; display timestamp and classification beside conditions rather than relying on a distant sources page.
- [ ] **SCN.06.03** Specify freshness and unavailable-source behavior for enabled current information; absent connectivity must not convert stale observations into current facts or silently invent replacement weather.
- [ ] **SCN.06.04** Provide accessible authored alternatives and decide-later paths; scenario responses cannot automatically issue equipment commands, extend a workout, or generate personalized physical/medical instructions.
- [ ] **SCN.06.05** Inspect historical and hypothetical dossiers under changed real dates and clock settings; confirm labels and timestamps preserve their original meaning and scenario outcomes remain reproducible.
- [ ] **SCN.06.06** Exercise missing timestamps, ambiguous current wording, stale data, severe fictional conditions, and prolonged deferral; require honest context and a recoverable choice without compensatory exertion.
- [ ] **SCN.06.07** Persist the selected response and supplied conditions; restart restores the same event, while approved corrections retain original delivered assumptions and explicit replacement/annotation history.
- [ ] **SCN.06.08** Archive classification/freshness review and branch tests; accept only when users can distinguish condition type/time and every weather outcome stays within authorized fictional effects.

### Control SCN 07

**Original requirement SCN.07:** For trail encounters, specify character prerequisites, location plausibility, dialogue revision, optional participation, and effects on continuing threads; prevent contradictions with established facts.

- [ ] **SCN.07.01** Define encounter prerequisites for character/thread state, campaign branch, route position, plausible timing, dialogue revision, optional participation, and permitted continuing-thread effects with stable identities.
- [ ] **SCN.07.02** Specify location plausibility using the pinned itinerary and known character facts; repeated or simultaneous appearances must have an authored explanation consistent with established chronology.
- [ ] **SCN.07.03** Validate dialogue references and claimed knowledge against persisted branch history; characters cannot acknowledge choices, losses, relationships, or future events the player has not established.
- [ ] **SCN.07.04** Provide decline, defer, and resume options preserving meaningful participation choice; skipping optional dialogue cannot silently change physical targets or erase accepted activity or reflections.
- [ ] **SCN.07.05** Execute mutually exclusive branch histories and compare encounter availability/dialogue with independent expected character states; verify only compatible scenes appear and successors maintain causal continuity.
- [ ] **SCN.07.06** Exercise absent prerequisites, withdrawn dialogue, impossible locations, repeated encounters, and contradictory known facts; block invalid scenes or use an explicitly approved narrative recovery variant.
- [ ] **SCN.07.07** Persist participation and thread effects transactionally with idempotent operation identity; lost acknowledgments and service restart must restore one effective encounter outcome with original dialogue revision.
- [ ] **SCN.07.08** Archive continuity maps, dialogue reviews, and replay results; accept only when every encounter is optional as designed, geographically plausible, and compatible with established campaign facts.

### Control SCN 08

**Original requirement SCN.08:** For landmark discovery, connect the feature and photograph to route position, geographic confidence, capture context, and learning objective; distinguish viewing an image from physically visiting the location.

- [ ] **SCN.08.01** Define discovery records linking landmark/feature identity, immutable route position, geographic confidence, image association, representation class, capture context, learning objective, and discovery-effect revision.
- [ ] **SCN.08.02** Distinguish camera position, depicted feature, nearby scenery, and distant view; an image's appearance or filename cannot alone support an exact-location discovery claim.
- [ ] **SCN.08.03** Display geographic classification, historical/seasonal capture context, and the preparation skill taught; viewing an image must be described as virtual discovery rather than physical visitation.
- [ ] **SCN.08.04** Specify collection/unlock effects separately from real location/activity records; virtual landmark discovery cannot produce outdoor mileage, GPS presence, or evidence of firsthand trail experience.
- [ ] **SCN.08.05** Trace a sample discovery through map, photograph, caption, lesson, and collection entry; independently verify all refer to the same reviewed feature/context and supported objective.
- [ ] **SCN.08.06** Exercise missing imagery, uncertain associations, historical photographs, illustrative substitutes, and incorrect route links; reject misleading exact claims or provide an explicitly labeled informative alternative.
- [ ] **SCN.08.07** Resume and retry discovery after interruption; persist one effective unlock while retaining original media/objective revisions and leaving actual activity plus next-leg state unchanged.
- [ ] **SCN.08.08** Archive geographic/media/learning review and representation screenshots; accept only when discoveries are traceable to supported associations and every display distinguishes virtual viewing from real physical presence.

### Control SCN 09

**Original requirement SCN.09:** For equipment problems, publish the fictional fault and available information, accessible recovery choices, virtual costs, and source-backed explanation; do not turn a narrative repair into an unreviewed real equipment instruction.

- [ ] **SCN.09.01** Define equipment-problem scenarios with fictional fault, item identity/version, available observations, uncertainty, accessible recovery choices, virtual costs, source-backed explanation, and consequence records.
- [ ] **SCN.09.02** Clearly separate narrative diagnosis/repair from actual equipment guidance; reviewed source context cannot be converted into individualized real repair instructions or automatic equipment-control commands.
- [ ] **SCN.09.03** Disclose choice prerequisites, supplied information, reversible costs, and limitations; include a recoverable continue/defer/alternative path when missing items or funds would otherwise strand participation.
- [ ] **SCN.09.04** Validate effects against virtual inventory/resources only; fictional faults cannot invalidate an actual completed workout, increase exercise targets, or claim real equipment has been inspected.
- [ ] **SCN.09.05** Play through each repair/replacement/deferral choice and independently reconcile costs, inventory, narrative state, and explanation with the published assumptions and approved typed effects.
- [ ] **SCN.09.06** Exercise uncertain faults, unavailable parts, exhausted budget, incompatible items, and repeated retries; show supported alternatives and reject impossible transactions without partially charging resources.
- [ ] **SCN.09.07** Interrupt a recovery transaction and restart; retain original fault/context and recover exactly one committed outcome or explicit unresolved state with no duplicate virtual costs.
- [ ] **SCN.09.08** Archive source-context review, recovery maps, and transaction tests; accept only when every fault remains fictional, all choices are accessible, and no unreviewed real repair prescription appears.

### Control SCN 10

**Original requirement SCN.10:** For town and recovery days, provide planning, journal, character, and knowledge content that can progress without invented walking distance or pressure to compensate for missed exercise.

- [ ] **SCN.10.01** Define town/recovery-day content covering planning tasks, journal prompts, optional character interactions, knowledge activities, accepted preparation evidence, and the enabled narrative/progression policy for nonwalking participation.
- [ ] **SCN.10.02** Specify completion criteria independently from distance targets; approved recovery/preparation participation can satisfy its assigned objectives without generating moving intervals, incline exposure, or walked mileage.
- [ ] **SCN.10.03** Author supportive explanations for skipped/shortened sessions and real rest; remove streak penalties, compensatory-exercise incentives, or dialogue implying the user must earn recovery through additional exertion.
- [ ] **SCN.10.04** Provide accessible content and deliberate complete-day controls; physical-session finish, story viewing, and clock/date changes cannot implicitly complete or advance the expedition day.
- [ ] **SCN.10.05** Complete a recovery day using only planning, learning, journal, and authored choices; verify permitted story progress while actual-distance and physical-exposure totals remain unchanged.
- [ ] **SCN.10.06** Exercise absent walking data, partial previous sessions, resource exhaustion, skipped optional scenes, and multiple real dates; preserve participation paths without invented fitness baselines or required compensation.
- [ ] **SCN.10.07** Relaunch before explicit completion and then after accepted completion; verify unfinished-day restoration versus exactly one committed next-leg advance with preserved preparation evidence.
- [ ] **SCN.10.08** Archive nonwalking journey and incentive review; accept only when recovery content is substantive, progress follows disclosed policy, and no physical activity is fabricated or pressured.

### Control SCN 11

**Original requirement SCN.11:** Review every scenario family for recoverable outcomes, more than one defensible strategy where appropriate, explanation quality, repetition, respectful tone, and a continuing path after a setback.

- [ ] **SCN.11.01** Create a review matrix for every enabled scenario family covering recoverability, alternative defensible strategies, explanations, repetition, respectful tone, uncertainty, and continuation after setbacks.
- [ ] **SCN.11.02** Specify setback states and minimum continuing paths, including depleted resources, declined encounters, wrong answers, missed activity, and unavailable assets; participation cannot require unplanned exertion.
- [ ] **SCN.11.03** Review alternate strategies against supplied conditions/priorities; permit multiple supported outcomes when appropriate and document why any mandatory constraint excludes a seemingly reasonable choice.
- [ ] **SCN.11.04** Inspect failure explanations, repeated scenes, and rewards for blame, coercion, misleading certainty, or physical-readiness claims; require edits to material pressure or unsupported implications.
- [ ] **SCN.11.05** Traverse every authored terminal and setback branch using representative campaign histories; verify at least one accessible continuing path exists and consequences match the disclosed typed effects.
- [ ] **SCN.11.06** Exercise repeated failure, exhausted resources, missing optional equipment, and deferred decisions; confirm recovery remains available without resetting history or adding compensatory exercise demands.
- [ ] **SCN.11.07** Record defects with family/version, problematic branch, owner, correction, and reviewer disposition; replay corrected branches and retain the original failure evidence with final acceptance.
- [ ] **SCN.11.08** Archive family coverage and recovery/strategy reviews; accept only when all enabled families have reviewed continuing paths and all material explanation/incentive defects are resolved.

### Control SCN 12

**Original requirement SCN.12:** Playtest representative choices without designer hints; record misunderstood assumptions, inaccessible alternatives, confusing actual/fictional quantities, and unintended incentives, then resolve material defects.

- [ ] **SCN.12.01** Define a playtest sample spanning scenario families, branches, prior experience, supported interaction methods, and representative displays with exact candidate content/rule versions and tasks.
- [ ] **SCN.12.02** Provide rendered scenario information without designer hints; record participants' interpreted assumptions, selected choices, expected consequences, observed outcomes, and where they sought clarification or assistance.
- [ ] **SCN.12.03** Observe confusion between actual workout quantities, virtual resources, scenario dates, historical imagery, and physical presence; identify the exact label or interaction causing each misunderstanding.
- [ ] **SCN.12.04** Include keyboard/assistive interaction and untimed walking-context deferral where applicable; inaccessible alternatives must be recorded as defects rather than attributed to user performance.
- [ ] **SCN.12.05** Compare unassisted choices and explanations with authored intent; detect concealed success assumptions, unsupported best-choice scoring, unintended extra-exercise incentives, and recoverability failures across tested families.
- [ ] **SCN.12.06** Record material findings with severity, affected control/version, reproduction steps, owner, corrective proposal, and required acceptance evidence; retain contradictory observations rather than averaging away serious confusion.
- [ ] **SCN.12.07** Revise prompts, labels, choices, or rules and conduct targeted unassisted retesting; confirm users understand corrected assumptions/consequences and access alternatives without additional designer explanation.
- [ ] **SCN.12.08** Archive anonymized playtest findings and repair evidence; accept only when all material misunderstandings, inaccessible options, and unintended physical incentives have resolved or explicitly bounded release dispositions.

## INT System integration acceptance controls

**Accountable roles:** Application and data-integrity owner, with content and user-experience reviewers for the affected journey.

Each journey identifies initial committed records, exact candidate versions, operations, expected records, visible results, and retained evidence. Supporting unit checks do not replace the complete journey.

### Control INT 01

**Original requirement INT.01:** Complete a day from dossier preparation through planned training, decision, resource update, camp journal, and dashboard; verify all records link to the same effective versions.

- [ ] **INT.01.01** Create a named campaign fixture with pinned route, content, rule, training-plan, and schema revisions; record initial position, inventory, character facts, and day-completion requirements.
- [ ] **INT.01.02** Launch through CMD and PowerShell, reserve the next day, and verify staged dossier publication, generation hash, saved seed, loopback readiness, and correct active-day identity.
- [ ] **INT.01.03** Record the planned activity through the local service, including accepted interval classifications and assignment snapshot; verify durable receipt and actual totals independent of scenario distance.
- [ ] **INT.01.04** Offer and commit the day decision, inspect its explanation, and reconcile condition evidence, persisted draws, resource ledger, and character effects to one causal operation.
- [ ] **INT.01.05** Create a camp reflection and explicitly complete the eligible day; assert acknowledged journal revision, committed DayCompletion, and transactionally saved next-leg pointer.
- [ ] **INT.01.06** Inspect dashboard, collection, and debrief projections; require matching effective session, progression, event, dossier, resource, and correction revisions throughout the completed journey.
- [ ] **INT.01.07** Restart after accepted activity and again after completion acknowledgment loss; verify no duplicate effects, unchanged completed dossier, and correct reservation of the following unfinished day.
- [ ] **INT.01.08** Retain launch records, request receipts, database reconciliation, dossier manifest, interface evidence, and reviewer results; accept only a fully linked journey with zero version mismatches.

### Control INT 02

**Original requirement INT.02:** Replay a known campaign from its initial state using accepted activity, decisions, scheduling inputs, and persisted random outcomes; reconcile resulting position, resources, characters, and journal references.

- [ ] **INT.02.01** Archive a known campaign's initial database state, route/content manifests, training assignments, accepted activity revisions, decisions, trigger ordering, and persisted random outcomes.
- [ ] **INT.02.02** Define independently expected final route position, next-leg pointer, resources, inventory, character/thread states, journal causes, and completion sequence before replay begins.
- [ ] **INT.02.03** Replay accepted activity and progression operations using original policy revisions and ordering; verify actual totals and fractional credit match their historical authoritative records.
- [ ] **INT.02.04** Replay encounter scheduling and choices using pinned candidate fingerprints, rule revisions, seeds or draws, and source-day gates; prohibit additional random sampling for established reservations.
- [ ] **INT.02.05** Reconstruct resource and character projections from committed causal records; compare balances, possessions, relationships, facts, and thread nodes with the expected final state.
- [ ] **INT.02.06** Resolve journal and dossier references to original snapshot hashes; verify completion debriefs, corrections, and collectible unlocks correspond to their qualifying historical causes.
- [ ] **INT.02.07** Repeat replay after service restart and with current library defaults changed; require stable outcomes or an explicit unsupported-version recovery path without silent migration.
- [ ] **INT.02.08** Retain replay inputs, canonical fingerprints, ledger reports, fact comparisons, and mismatch findings; accept exact reconciliation of all final authoritative domains for the known campaign.

### Control INT 03

**Original requirement INT.03:** Retry and reorder permitted operations across local browser requests, service restarts, and multiple tabs; verify single committed effects, rejected stale revisions, and documented handling of missing predecessors.

- [ ] **INT.03.01** Prepare permitted operation sequences with stable keys, expected revisions, causal predecessor IDs, and independent final states; include activity, decisions, purchases, unlocks, and journal saves.
- [ ] **INT.03.02** Submit identical retries before response, after response loss, and across restarted service; assert one committed effect set and recovery through the original operation receipt.
- [ ] **INT.03.03** Deliver operations in approved alternate orders where independence is declared; compare resulting records with the documented commutativity and prerequisite contracts.
- [ ] **INT.03.04** Send consequential operations before required predecessors; verify explicit pending or rejected outcomes and no guessed decisions, resources, debriefs, or completion evidence.
- [ ] **INT.03.05** Race shared and distinct keys from multiple tabs, including conflicting branch selections and edits; require stable accepted results and explicit stale-revision or conflict responses.
- [ ] **INT.03.06** Restart between predecessor and successor operations, then replay stale browser queues; revalidate against SQLite and preserve original identities rather than issuing replacement effects.
- [ ] **INT.03.07** Reconcile operation counts, ledger entries, transitions, revisions, and orphan references after each ordering experiment; verify single effects and complete causal ancestry.
- [ ] **INT.03.08** Retain request timelines, receipts, rejection evidence, restart traces, and expected-state comparisons; require documented disposition for every retried, reordered, or predecessor-missing operation.

### Control INT 04

**Original requirement INT.04:** Split one virtual stage across several real sessions in every enabled progression mode; preserve actual totals, fractional credit, unfinished decisions, and the stage's original dossier context.

- [ ] **INT.04.01** Create equivalent unfinished-stage fixtures for every enabled progression mode with pinned dossier, seed, source gates, conversion policy, assignment snapshots, and independently calculated credit expectations.
- [ ] **INT.04.02** Record the first partial real session, including moving, paused, and unknown intervals; verify accepted actual quantities and fractional virtual credit without day completion.
- [ ] **INT.04.03** Relaunch on the same and later real dates; assert identical active day, dossier generation/hash, seed, pending decisions, and next-leg origin after each launch.
- [ ] **INT.04.04** Record subsequent sessions until the stage's eligibility threshold is met; preserve session identities, actual totals, fractional remainders, and each credit's source revision.
- [ ] **INT.04.05** Defer or leave a decision unfinished during the split journey; verify it remains linked to its original source-day gate and reserved random outcome.
- [ ] **INT.04.06** Explicitly complete only after the declared activity and gate conditions are satisfied; verify one completion and next-leg advance independent of the number of sessions.
- [ ] **INT.04.07** Interrupt a partial save and retry a credited session after restart; require one accepted session revision and no duplicated credit, consumed resources, or regenerated dossier.
- [ ] **INT.04.08** Retain per-mode conversion calculations, launch traces, session receipts, gate states, and completion reconciliation; require preserved real totals and original context throughout every split stage.

### Control INT 05

**Original requirement INT.05:** Earn enough credit in one session to cover multiple stages; retain surplus credit and ordered pending encounters, then require explicit completion for each eligible day without inventing decisions or moving the committed next-leg pointer early.

- [ ] **INT.05.01** Initialize a campaign with known remaining stage requirement, future stages, pending mandatory encounters, and a progression policy permitting surplus credit; pin all expected conversions.
- [ ] **INT.05.02** Record one accepted session producing credit sufficient for several stages; reconcile actual distance once and separate consumed current-stage credit from durable surplus and remainders.
- [ ] **INT.05.03** Inspect eligibility and ordered pending encounters before completion; require unchanged committed next-leg pointer and no invented future choices, journals, resource consumption, or completed days.
- [ ] **INT.05.04** Explicitly complete the current eligible day after its required gate disposition; verify exactly one pointer advance and one causally linked completion-effect set.
- [ ] **INT.05.05** Launch the next day, allocate surplus under the pinned policy, and present its own dossier and decisions; require deliberate completion independent of prior session size.
- [ ] **INT.05.06** Repeat through remaining surplus-supported stages without requiring extra actual exertion; preserve each day's source gates, ordered encounters, original training plan, and distinct completion operations.
- [ ] **INT.05.07** Restart and retry completions during surplus allocation; assert retained credit, no duplicate allocation, stable reserved seeds, and no premature advancement of later days.
- [ ] **INT.05.08** Retain credit-ledger reconciliation, pending encounter order, pointer snapshots, decision records, and assignment comparisons; accept surplus retention with explicit completion for every eligible day.

### Control INT 06

**Original requirement INT.06:** Complete recovery, knowledge, and equipment-preparation assignments; verify permitted chapter/story progress and no fabricated walking distance or physical incline exposure.

- [ ] **INT.06.01** Create approved recovery, knowledge, and equipment-preparation assignments with explicit completion rules, progression eligibility, zero invented walking targets, and pinned instructional content revisions.
- [ ] **INT.06.02** Complete each assignment through its supported evidence workflow, distinguishing acknowledgment, learning response, equipment practice reflection, and accepted actual activity where any is genuinely recorded.
- [ ] **INT.06.03** Apply the selected progression policy to eligible nonwalking tasks; verify chapter or story credit references the qualifying task and policy version rather than fabricated distance.
- [ ] **INT.06.04** Present relevant lessons, character dialogue, and camp content; ensure virtual route advancement and scenario resources remain clearly labeled when nonwalking progress is permitted.
- [ ] **INT.06.05** Inspect WorkoutSession, SessionInterval, distance, and incline records; require no generated walking quantity or physical incline exposure for tasks lacking accepted such measurements.
- [ ] **INT.06.06** Explicitly complete eligible days with their own decision requirements; verify source-day gates, debriefs, and next-leg transitions do not substitute task acknowledgment for consequential choices.
- [ ] **INT.06.07** Retry task completion, restart offline, and miss a scheduled recovery assignment; require idempotent credit and continuing participation without compensatory exercise pressure.
- [ ] **INT.06.08** Retain assignment definitions, completion evidence, progression receipts, domain-label inspections, and zero-measurement reconciliation; accept permitted preparation progress without fabricated physical activity.

### Control INT 07

**Original requirement INT.07:** Correct or delete a workout after campaign advancement; verify aggregate recalculation, credit adjustments, historical decision preservation, resource policy, and visible journal annotations.

- [ ] **INT.07.01** Complete and advance a campaign using a known accepted workout; archive original session revision, credits, decisions, resources, character facts, journal summaries, and saved position.
- [ ] **INT.07.02** Preview a correction and a deletion under approved policy, including aggregate changes, credit reversal or adjustment, downstream consequences, and preservation of established decision history.
- [ ] **INT.07.03** Apply the accepted workout correction through its dedicated revision workflow; verify durable receipt, revised actual totals, original source ancestry, and compensating progression entries.
- [ ] **INT.07.04** Inspect resource and character policy handling for already consumed credit; require documented preservation, compensation, or migration rather than silent reversal of consequential choices.
- [ ] **INT.07.05** Refresh dashboard and dependent journal summaries; display original-versus-corrected annotations where retained history remains and preserve user-authored reflection text.
- [ ] **INT.07.06** Delete a qualifying session through the supported workflow and repeat reconciliation; ensure deleted evidence no longer contributes current actual totals or unqualified readiness claims.
- [ ] **INT.07.07** Interrupt recalculation, retry the correction, and submit a stale deletion from another tab; require one adjustment, explicit conflict handling, and no orphaned references.
- [ ] **INT.07.08** Retain correction previews, ancestry, credit/resource ledgers, summary annotations, and final reconciliation; accept accurate current totals with preserved attributable historical decisions.

### Control INT 08

**Original requirement INT.08:** Create conflicting branch decisions and reflection edits in two local tabs, including stale views after a service restart; verify deduplication, explicit conflict handling, and preservation of original text.

- [ ] **INT.08.01** Open the same pinned event and journal entry in two tabs with identical initial campaign, day, event-instance, and reflection revisions; preserve original text as baseline evidence.
- [ ] **INT.08.02** Select mutually exclusive branch choices in both tabs and submit concurrently using distinct operation keys; require one accepted resolution and an explicit competing-choice conflict.
- [ ] **INT.08.03** Retry the accepted key from both tabs; verify stable receipt, one resource effect set, one character transition set, and no replacement of the accepted branch.
- [ ] **INT.08.04** Edit overlapping reflection text in both tabs; verify conflict presentation preserves original, local-draft, and server-current versions instead of silently applying last-write-wins.
- [ ] **INT.08.05** Exercise declared compatible merges using nonoverlapping changes; inspect resulting revision ancestry and ensure both contributions survive according to the approved merge contract.
- [ ] **INT.08.06** Restart the service while one tab retains stale event and entry views, then submit; require authoritative revalidation, explicit stale responses, and recoverable pending drafts.
- [ ] **INT.08.07** Inspect journal and decision histories after conflict resolution; confirm preserved original text, selected branch identity, causal receipts, and unaffected actual workout assignments.
- [ ] **INT.08.08** Retain concurrency timelines, conflict interfaces, revision graphs, receipt counts, and state comparisons; accept deterministic single consequential choices and explicit reflection conflict handling.

### Control INT 09

**Original requirement INT.09:** Interrupt execution around each persistence boundary during finish, decision, purchase, unlock, and journal save; verify complete or recoverable outcomes with no orphaned references.

- [ ] **INT.09.01** Enumerate persistence boundaries for session finish, consequential decision, compound purchase, collectible unlock, and journal save, including commit, acknowledgment, staged publication, rename, and marker reconciliation.
- [ ] **INT.09.02** Prepare deterministic fixtures and fault hooks with expected complete and unapplied states; capture initial ledger, revisions, causal references, artifacts, and operation identities.
- [ ] **INT.09.03** Terminate immediately before and during each database transaction; restart and verify either fully committed records or complete rollback, never partial mandatory effects.
- [ ] **INT.09.04** Terminate after durable commit but before HTTP acknowledgment; recover through the existing receipt and retry the original identity without duplicating quantities or transitions.
- [ ] **INT.09.05** Interrupt artifact rendering, checksum verification, rename, marker creation, and ready-record update; reconcile the same generation without exposing incomplete published dossiers or exports.
- [ ] **INT.09.06** Validate foreign keys, operation uniqueness, journal causes, resource transactions, unlocks, and completion pointers after each recovery; identify any orphan or unexplained intermediate state.
- [ ] **INT.09.07** Repeat selected faults under SQLite contention and concurrent browser requests; require bounded behavior and explicit retry states without altered seeds or replacement operation identities.
- [ ] **INT.09.08** Retain fault-location traces, before/after snapshots, receipt lookups, artifact manifests, and integrity reports; accept only complete or documented recoverable outcomes at every persistence boundary.

### Control INT 10

**Original requirement INT.10:** Complete repository-local content with internet disconnected, then restart the local service; reconcile credits, encounters, resource balances, notes, manifests, and database commit receipts.

- [ ] **INT.10.01** Prepare repository-local route, media, lessons, events, characters, training assignments, and manifests; disable internet while preserving the running loopback service and authoritative SQLite access.
- [ ] **INT.10.02** Launch or resume the pinned day through CMD and PowerShell; verify no required remote dependency prevents dossier readiness, workout recording, decisions, or journal access.
- [ ] **INT.10.03** Record accepted activity, commit choices and resource changes, complete eligible learning, and save a reflection; retain durable receipts for every state mutation.
- [ ] **INT.10.04** Explicitly complete the day only when its source gates are satisfied; inspect committed next-leg position, resource effects, encounters, unlocks, and completed-day debrief.
- [ ] **INT.10.05** Restart the local service with internet still disconnected; rehydrate campaign state, encounter queue, session revisions, reflections, and operation outcomes exclusively from repository authority.
- [ ] **INT.10.06** Reconcile credits, balances, character facts, notes, manifests, file checksums, and database receipts with independently expected final records; reject dependence on browser cache.
- [ ] **INT.10.07** Clear browser storage and remove an optional remote link during recovery; require usable local fallbacks, retained original generation, and no fabricated activity or automatic completion.
- [ ] **INT.10.08** Retain offline dependency audit, launch/restart records, committed receipts, manifest checks, and reconciliation results; accept complete local operation without internet or hidden remote persistence.

### Control INT 11

**Original requirement INT.11:** Resume an older campaign after route, dossier, image-rights, lesson, event, and character updates; verify pinned history, approved migration, withdrawn-content treatment, and usable replacements.

- [ ] **INT.11.01** Archive an older campaign containing completed history, an unfinished pinned day, pending encounters, reflections, original media rights, and known route/content/rule revisions.
- [ ] **INT.11.02** Install newer route, dossier, media-rights, lesson, event, and character releases without applying migration; resume and verify unchanged historical choices, active snapshot, seed, and saved position.
- [ ] **INT.11.03** Identify withdrawn and unavailable dependencies through current rights and correction policy; verify truthful placeholders, omission labels, or approved replacements preserve original provenance.
- [ ] **INT.11.04** Preview an approved migration with position mapping, source-gate treatment, character continuity, credit policy, media handling, and affected journal annotations before changing authoritative records.
- [ ] **INT.11.05** Apply migration using expected revisions and attributable approval; retain original versions, supersession links, audit records, and compensating changes required by the documented policy.
- [ ] **INT.11.06** Inspect completed dossiers and decisions after migration; require immutable original outcomes or explicit annotations rather than current content silently rewriting established campaign history.
- [ ] **INT.11.07** Interrupt migration and replacement publication, then restart offline; recover a supported usable campaign or diagnosed limitation without rerolling events or skipping unresolved gates.
- [ ] **INT.11.08** Retain original/new manifests, migration previews, rights decisions, supersession ancestry, and resume evidence; accept pinned history with explicit reviewed transitions and usable rights-aware replacements.

### Control INT 12

**Original requirement INT.12:** Attempt to alter physical training through every permitted story effect, imported rule, generated narrative field, resource failure, and external integration; verify the training boundary and rejection evidence.

- [ ] **INT.12.01** Inventory every permitted story effect, imported rule target, generated narrative field, resource failure, and enabled integration capable of reaching domain mutation interfaces.
- [ ] **INT.12.02** Capture protected TrainingPlan, Assignment, actual WorkoutSession, accepted quantities, recovery schedule, and equipment-command state as independently verifiable initial snapshots.
- [ ] **INT.12.03** Exercise every allow-listed virtual effect with valid inputs; compare protected hashes and command logs while confirming intended fictional resources, facts, or reservations change.
- [ ] **INT.12.04** Import rules targeting actual duration, distance, incline, load, recovery, or equipment control through direct fields, aliases, malformed paths, and nested expressions; require rejection.
- [ ] **INT.12.05** Generate prose claiming workouts, prescribing compensatory exercise, or requesting device commands; verify validation and rendering cannot convert text into accepted measurements or mutations.
- [ ] **INT.12.06** Exhaust resources and resolve poor decisions across enabled integrations; require authored recovery without extra prescribed exertion or external commands derived from fictional need.
- [ ] **INT.12.07** Restart and replay rejected requests, including stale and concurrent submissions; verify no deferred job or recovery path bypasses the training boundary later.
- [ ] **INT.12.08** Retain target inventory, rejected payloads, validation reasons, protected-state comparisons, and command evidence; accept zero narrative-originated physical-training or equipment changes across all enabled paths.

### Control INT 13

**Original requirement INT.13:** Remove an image, map tile, external link, or event dependency; retain workout logging and provide the documented dossier or story fallback without misrepresenting substituted imagery.

- [ ] **INT.13.01** Prepare a complete day with known image, map-tile, external-link, and event dependencies; capture pinned manifests, rights metadata, labels, gates, and workout-recording endpoints.
- [ ] **INT.13.02** Remove one dependency class at a time while retaining authoritative database state; record whether failure occurs before publication, during presentation, or after restart.
- [ ] **INT.13.03** Verify workout start, pause, finish, correction, and journal save remain available with durable receipts despite missing presentation assets or optional external destinations.
- [ ] **INT.13.04** Inspect dossier fallback for missing photographs and tiles; require geographic honesty, accurate substitute classification, retained credits, alternative text, and no implied current trail observation.
- [ ] **INT.13.05** Break an event dependency and verify optional fallback or explicit pending mandatory status; prohibit asset loss from waiving source-day gates or completing any day.
- [ ] **INT.13.06** Restore dependencies or publish an approved corrected snapshot; reconcile hashes, supersession links, reservation identity, and original draws without unrecorded rerolling.
- [ ] **INT.13.07** Restart offline and retry failed rendering or submissions; assert stable campaign position, recoverable queues, one accepted effect set, and no lost actual activity.
- [ ] **INT.13.08** Retain removal fixtures, fallback inspections, workout receipts, manifest comparisons, and gate traces; accept usable degradation with truthful imagery and preserved authoritative continuation.

### Control INT 14

**Original requirement INT.14:** Complete the full preparation, recording, deferred decision, debrief, correction, export, and recovery flow using keyboard and screen reader, enlarged text, reduced motion, and touch where supported.

- [ ] **INT.14.01** Define supported keyboard, screen-reader, enlarged-text, reduced-motion, and touch configurations; prepare a full-day fixture with activity, mandatory deferral, correction, export, and recoverable faults.
- [ ] **INT.14.02** Navigate dossier preparation, source labels, training assignment, and workout controls without pointer dependence; verify meaningful names, focus order, announced status, and untimed access.
- [ ] **INT.14.03** Record and finish activity using accessible controls; inspect pause, error, unknown-interval, saved, and pending states without relying solely on color, movement, or sound.
- [ ] **INT.14.04** Defer a mandatory decision deliberately, then return and resolve it; verify source-gate explanation, persisted acknowledgment, retained focus context, and unchanged destination completion.
- [ ] **INT.14.05** Write a reflection, explicitly complete the eligible day, and review its debrief and dashboard; require readable domain labels and accurate announced commit outcomes.
- [ ] **INT.14.06** Correct activity and export selected history; verify accessible preview, conflict/error recovery, provenance annotations, reflection selection, and semantic structure in the resulting document.
- [ ] **INT.14.07** Interrupt the service during saving and resume with assistive technology; recover drafts and receipts without silent data loss or inaccessible conflict-resolution controls.
- [ ] **INT.14.08** Retain task recordings, assistive configurations, findings, document inspections, and resolved defects; accept complete preparation-to-recovery task completion across each supported accessibility configuration.

### Control INT 15

**Original requirement INT.15:** Run representative long campaigns in both directions and across all content regions; detect stranded threads, repeated events, impossible recovery, contradictory characters, and incomplete stage coverage.

- [ ] **INT.15.01** Select named long-campaign fixtures spanning both directions, all released regions, enabled progression modes, divergent choices, skipped locations, repeated stages, absence, and exhaustion recovery.
- [ ] **INT.15.02** Pin seed sets, manifests, initial resources, character facts, route coverage, and acceptance thresholds for mandatory delays, repetition, stranded threads, and missing stage content.
- [ ] **INT.15.03** Execute the complete itinerary through explicit day completions and approved divergences; retain operation receipts, position ancestry, encountered content, and source-gate disposition per stage.
- [ ] **INT.15.04** Measure topic repetition, character exposure, encounter gaps, unresolved mandatory threads, branch availability, and geographical content coverage by direction and region rather than overall averages.
- [ ] **INT.15.05** Inspect contradictions in whereabouts, introductions, possessions, promises, resources, known facts, and educational dialogue; compare each violation with the governing continuity rules.
- [ ] **INT.15.06** Drive supported exhausted states and long deferrals to recovery; verify reachable continuation without extra actual exertion, invented choices, or automatic destination-day completion.
- [ ] **INT.15.07** Restart at representative campaign boundaries and retire selected content; confirm pinned recovery, usable fallbacks, and deterministic reconstruction of established narrative and resource state.
- [ ] **INT.15.08** Retain campaign traces, stratified metrics, coverage maps, contradiction findings, and reviewer dispositions; accept only scope with complete stage coverage and no unresolved stranded mandatory path.

### Control INT 16

**Original requirement INT.16:** Verify every summary, collection, chart, export, and optional shared view distinguishes actual activity, game progress, virtual resources, scenario conditions, and the user's physical presence.

- [ ] **INT.16.01** Inventory every enabled summary, collection, chart, journal section, export, and optional shared view with its input fields, aggregation rules, domain labels, and physical-presence language.
- [ ] **INT.16.02** Prepare mixed examples containing accepted workouts, virtual trail distance, fictional resources, hypothetical conditions, illustrative images, knowledge-only progress, skipped stages, and personal reflections.
- [ ] **INT.16.03** Inspect actual activity displays and reconcile quantities exclusively to accepted sessions and corrections; prevent fictional distance, scenario time, or resources from entering physical metrics.
- [ ] **INT.16.04** Inspect game-progress and collection displays for explicit accomplishment type, policy revision, virtual route context, and distinction between viewing content and visiting a location.
- [ ] **INT.16.05** Inspect scenario-condition and resource presentations for assumptions, timestamp meaning, unknown values, and fictional labels adjacent to values or consequential explanatory claims.
- [ ] **INT.16.06** Export and, where enabled, create an explicitly selected shared preview; verify preserved domain metadata, rights-aware media, accurate dates, and selected reflection inclusion.
- [ ] **INT.16.07** Correct or delete measurements and retire media, then refresh every surface; require current labels, truthful annotations, no stale actual totals, and no fabricated presence claims.
- [ ] **INT.16.08** Retain surface inventory, source reconciliation, label inspections, export examples, and reviewer results; accept zero ambiguous cross-domain quantities or unsupported actual-activity and location-presence claims.

### Control INT 17

**Original requirement INT.17:** Reconcile dashboard totals against independent expected records after unit changes, date boundaries, overnight sessions, duplicate imports, interval gaps, split/merge operations, and corrections.

- [ ] **INT.17.01** Construct an independently calculated activity ledger covering unit conversions, date boundaries, overnight sessions, duplicate imports, interval gaps, split/merge operations, and accepted corrections.
- [ ] **INT.17.02** Pin timezone, canonical units, conversion precision, aggregation rules, unknown-interval handling, and expected daily and campaign totals before exercising dashboard projections.
- [ ] **INT.17.03** Record boundary and overnight sessions with separate moving, stationary, paused, and unknown intervals; verify elapsed, moving, pause, and distance quantities retain declared semantics.
- [ ] **INT.17.04** Import duplicate observations with matching and differing source identifiers; assert documented deduplication or conflict handling and no unapproved double credit in actual totals.
- [ ] **INT.17.05** Split and merge supported sessions, then correct and delete selected records; verify source ancestry, recalculated aggregates, progression adjustments, and preserved historical journal annotations.
- [ ] **INT.17.06** Change display units and timezone views without altering canonical measurements; compare rounding, date grouping, and chart labels to independently expected presentation values.
- [ ] **INT.17.07** Restart after interrupted projection recalculation and inspect dashboard, charts, journal, and exports; require consistent effective revisions or explicit pending status across surfaces.
- [ ] **INT.17.08** Retain independent calculations, source records, conversion results, correction ancestry, and projection comparisons; accept exact canonical totals and only documented display-rounding differences.

### Control INT 18

**Original requirement INT.18:** Restore exported or backed-up history into a clean supported environment; verify record ownership, referential integrity, campaign position, reflections, units, provenance, and rights-aware media behavior.

- [ ] **INT.18.01** Create consistent backup and supported structured-export fixtures containing campaign history, positions, session revisions, reflections, receipts, pinned manifests, media rights, and restoration metadata.
- [ ] **INT.18.02** Prepare a clean supported environment with no browser history or prior database; verify runtime, schema compatibility, repository identity, permissions, and chosen import or restore operation.
- [ ] **INT.18.03** Restore using verified checksums and documented ownership mapping; retain original stable identities, causal references, operation receipts, units, timezone metadata, and correction ancestry.
- [ ] **INT.18.04** Check database foreign keys, ledger reconciliation, active-day identity, dossier hashes, seed, completed endpoint, and next-leg pointer before accepting restored mutations.
- [ ] **INT.18.05** Read reflections and replay historical decisions or summaries; require accurate text, provenance, original outcomes, accessible fallback, and rights-aware treatment of expired or withdrawn media.
- [ ] **INT.18.06** Launch through CMD and PowerShell, resume the unfinished day, and retry a previously accepted operation; verify no fabricated activity, rerolled content, duplicate effects, or skipped leg.
- [ ] **INT.18.07** Test corrupted checksum, missing artifact, incompatible schema, and interrupted restore; require diagnosed refusal or documented recovery without silently initializing an empty replacement hike.
- [ ] **INT.18.08** Retain restoration manifests, ownership checks, integrity reports, launch evidence, and final reconciliation; accept usable restored history with complete authority and truthful media handling.

### Control INT 19

**Original requirement INT.19:** Change progression policy or itinerary mid-campaign through its approved operation; inspect the preview, prospective effects, original credits, migration audit, and unresolved narrative handling.

- [ ] **INT.19.01** Prepare a mid-campaign fixture with accepted credits, fractional surplus, completed history, unfinished pinned dossier, pending gates, deferred encounters, character threads, and original policy/itinerary revisions.
- [ ] **INT.19.02** Invoke the approved change operation and inspect a preview of prospective conversion, route mapping, pending narrative treatment, resource consequences, and affected journal annotations.
- [ ] **INT.19.03** Verify the preview identifies authority, effective boundary, required acknowledgments, expected revisions, unsupported mappings, and unresolved mandatory content before any authoritative mutation occurs.
- [ ] **INT.19.04** Apply an approved progression-policy change; preserve original credit amounts and policy references while recording only declared prospective effects or explicit compensating migration entries.
- [ ] **INT.19.05** Apply an approved itinerary change using stable route positions; preserve completed stages and active-day semantics or require an explicit audited migration of affected unfinished content.
- [ ] **INT.19.06** Inspect relocated encounters, source-day carryovers, character continuity, resource transitions, and supersession records; prohibit automatic waiver, destination completion, or training-plan escalation.
- [ ] **INT.19.07** Submit stale changes from another tab and interrupt migration/publication; require explicit conflict, recoverable audited state, retained original history, and unchanged unapplied preview operations.
- [ ] **INT.19.08** Retain previews, approvals, before/after credits and positions, migration audits, and unresolved-content dispositions; accept attributable prospective change with no silent historical rewriting.

### Control INT 20

**Original requirement INT.20:** Relaunch on the same and later calendar dates, clear browser cache, change port, and relocate the repository; verify that saved day/next-leg state survives and that another launch cannot fabricate activity or skip a leg.

- [ ] **INT.20.01** Create an unfinished campaign with known active day, next-leg origin, dossier hash, seed, sessions, choices, resources, journal revision, and operation receipts; capture an independent baseline.
- [ ] **INT.20.02** Relaunch repeatedly on the same calendar date through CMD and PowerShell; verify distinct run records but identical active-day identity and no additional exercise or completion records.
- [ ] **INT.20.03** Relaunch on later dates and after changing the computer clock or timezone; require preserved unfinished-day context, original scenario time, and unchanged next-leg pointer.
- [ ] **INT.20.04** Clear browser cache and reopen through the local service; verify reconstruction from SQLite and repository snapshots rather than an empty hike, regenerated seed, or client position.
- [ ] **INT.20.05** Change the configured loopback port and verify owned-service readiness, expected instance identity, correct dossier URL, and unaffected authoritative campaign and receipt state.
- [ ] **INT.20.06** Relocate the repository to a supported path and launch from another working directory; resolve paths from the launcher and verify database, snapshots, assets, and backups remain attributable.
- [ ] **INT.20.07** Explicitly complete the day once, lose acknowledgment, and relaunch or retry; require one committed completion, one next-leg advance, and the following unfinished day resumed without skips.
- [ ] **INT.20.08** Retain launch logs, before/after record counts, position/hash/seed comparisons, port and relocation evidence, and completion receipts; accept zero launch-fabricated activity or unintended leg advancement.

## REL Release and operational acceptance controls

**Accountable roles:** Release owner and the accountable application, content, training, narrative, accessibility, and user-data reviewers for the selected scope.

Release acceptance applies to the frozen candidate and declared scope. Changed dependencies or manifests reopen affected evidence. One-person ownership remains valid when responsibility and review are attributable.

### Control REL 01

**Original requirement REL.01:** Freeze the selected release scope, enabled modes, supported platforms, route release, content manifest, schemas, and rule versions in a signed or otherwise attributable release record.

- [ ] **REL.01.01** Create a release record identifying application build, source revision, artifact checksums, target platform matrix, supported browser versions, and accountable release owner.
- [ ] **REL.01.02** Freeze selected campaign modes, route releases, covered stages, content manifests, rules versions, database schema, and API compatibility for the release candidate.
- [ ] **REL.01.03** Declare the actual completeness boundary, distinguishing prototype content, selected regional coverage, and any intended full-route experience using quantified inventories.
- [ ] **REL.01.04** Link the release record to launcher, service, interface, content, training, narrative, and persistence evidence applicable to that exact candidate.
- [ ] **REL.01.05** Require a reviewed change record and affected-check rerun when a frozen dependency, manifest, rule, schema, or runtime changes before acceptance.
- [ ] **REL.01.06** Reproduce candidate installation or repository startup from the recorded materials and verify reported versions and manifests match the release record.
- [ ] **REL.01.07** Introduce an unrecorded asset or rule change and verify release validation detects the mismatch rather than accepting previous evidence unchanged.
- [ ] **REL.01.08** Archive the frozen record and reproduction results; accept when reviewers can identify precisely what application, content, and operating scope were approved.

### Control REL 02

**Original requirement REL.02:** Review every applicable control disposition; accepted exceptions include their impact, owner, compensating control, expiration, and user-visible limitation when material.

- [ ] **REL.02.01** Maintain a control applicability register with parent and child IDs, applicable status, rationale, affected mode or platform, owner, and evidence reference.
- [ ] **REL.02.02** Separate verified completion, not applicable, open defect, and time-limited exception so unchecked work cannot be disguised as a completed requirement.
- [ ] **REL.02.03** Require each exception to describe user impact, affected data or behavior, compensating measure, responsible owner, expiry or review trigger, and acceptance authority.
- [ ] **REL.02.04** Propagate parent disposition from its eight children under documented rules, identifying any unresolved child instead of averaging completion percentages.
- [ ] **REL.02.05** Expose material limitations in the appropriate release notes and user workflow where the limitation affects a real decision or expected capability.
- [ ] **REL.02.06** Review representative applicable, inapplicable, and exception records against supporting evidence and the candidate's actual selected scope.
- [ ] **REL.02.07** Expire a test exception and change an applicability assumption; verify affected release gates reopen and compensations remain traceable.
- [ ] **REL.02.08** Retain the disposition register and exception decisions; accept when every released control has an attributable, current, and evidence-supported outcome.

### Control REL 03

**Original requirement REL.03:** Confirm that each published stage has its required dossier elements, licensed imagery or an honestly labeled substitute, working decisions, a useful lesson, and a camp debrief.

- [ ] **REL.03.01** Define a stage completeness schema requiring route context, daily objectives, licensed imagery or labeled substitute, decisions, knowledge activity, camp endpoint, camp debrief, and source metadata.
- [ ] **REL.03.02** Run completeness validation against every stage included in the frozen content manifest, reporting missing fields and incompatible route references by stage ID.
- [ ] **REL.03.03** Verify each photo's rights and attribution records or each substitute's explicit representation label before counting the visual requirement as satisfied.
- [ ] **REL.03.04** Check that choices have reachable outcomes, mandatory interactions have valid dispositions, and the camp endpoint aligns with the declared stage boundary.
- [ ] **REL.03.05** Require optional omissions to have usable fallback content and preserve the minimum dossier experience during offline startup.
- [ ] **REL.03.06** Open a dossier for every selected stage or a justified automated coverage pass with targeted human review of content-specific risks.
- [ ] **REL.03.07** Remove required imagery, invalidate a route reference, and break a choice outcome in fixtures; verify publication or release completeness gates fail precisely.
- [ ] **REL.03.08** Retain stage validation reports and reviewed dossiers; accept when every advertised stage delivers its required daily experience with legitimate visual provenance.

### Control REL 04

**Original requirement REL.04:** Inspect regional, seasonal, and representation coverage; quantify missing content and avoid describing an incomplete authored library as coverage of every trail day.

- [ ] **REL.04.01** Create a coverage matrix by selected route region, stage range, season representation, terrain context, visual source type, and applicable scenario or lesson families.
- [ ] **REL.04.02** Quantify covered and uncovered stages and route distance using the pinned route release rather than a promotional approximation.
- [ ] **REL.04.03** Identify factual imagery, historical imagery, illustrative substitutes, and fictional encounters separately so representation completeness remains assessable.
- [ ] **REL.04.04** Document seasonal assumptions and unresolved source gaps without presenting generated seasonal prose as current observed trail conditions.
- [ ] **REL.04.05** Align user-facing coverage claims, installation documentation, and release notes with the measured manifest inventory and fallback availability.
- [ ] **REL.04.06** Sample dossiers across each advertised region and representation class, verifying their sources, season labels, and claimed stage coverage.
- [ ] **REL.04.07** Compare marketing or onboarding claims with the inventory and flag any statement implying every day is populated when stages remain unsupported.
- [ ] **REL.04.08** Retain the quantified coverage matrix and claim review; accept when users can understand the available route experience and its documented gaps.

### Control REL 05

**Original requirement REL.05:** Review supplied training content, adjustment behavior, recovery rewards, and game incentives; resolve material pressure toward unplanned exercise before release.

- [ ] **REL.05.01** Review released training objectives, workout options, progression changes, recovery behavior, and preparation tasks against the stated educational training purpose.
- [ ] **REL.05.02** Identify every game mechanic that can suggest additional exercise, including streaks, deadlines, resource depletion, characters, unlocks, and completion rewards.
- [ ] **REL.05.03** Require rest, reduced activity, interruption, and preparation alternatives to remain available under the selected training policy without punitive narrative pressure.
- [ ] **REL.05.04** Confirm fictional injury, thirst, weather, and urgency are not translated automatically into individualized physical prescriptions or treadmill commands.
- [ ] **REL.05.05** Review changes to training plans separately from narrative content, recording their source, rationale, applicable audience, and user acknowledgement where required.
- [ ] **REL.05.06** Walk through a low-activity week, missed session, and voluntarily reduced workout, verifying supportive choices and accurate unchanged physical records.
- [ ] **REL.05.07** Trigger scarcity, streak loss, and urgent encounter fixtures; verify the game cannot require unplanned exercise to protect fictional characters or retain progress.
- [ ] **REL.05.08** Retain training and incentive review evidence; accept when the released adventure supports preparation without coercing extra physical activity.

### Control REL 06

**Original requirement REL.06:** Reconcile physical activity, progression credits, fictional resources, story transitions, collections, and summary projections against authoritative records.

- [ ] **REL.06.01** Define reconciliation rules linking physical observations, accepted activity, causal credits, fictional resources, decisions, story flags, collections, and dashboard summaries.
- [ ] **REL.06.02** Identify the authoritative ledger and rule version for each quantity, including units, rounding, reversals, and correction handling.
- [ ] **REL.06.03** Generate release reconciliation reports from a consistent database snapshot, preserving source record identities for every derived balance or summary.
- [ ] **REL.06.04** Check that completed-day credit allocations do not exceed eligible activity and that carryover remains unavailable for implicit future-day completion.
- [ ] **REL.06.05** Verify fictional resource costs and narrative rewards cannot rewrite physical distance, moving time, training plan approval, or route source data.
- [ ] **REL.06.06** Reconcile fixtures containing partial sessions, manual corrections, deferred decisions, repeated requests, completed legs, and collection unlocks.
- [ ] **REL.06.07** Introduce a deliberately duplicated resource effect or inconsistent summary and verify detection identifies the originating operation and affected display.
- [ ] **REL.06.08** Retain reconciled ledgers and discrepancy dispositions; accept when each reported total and unlocked state is explainable from authoritative causal records.

### Control REL 07

**Original requirement REL.07:** Complete the selected accessibility assessment and walking-context usability review; record outstanding issues and their release disposition.

- [ ] **REL.07.01** Freeze the accessibility and walking-usability assessment scope, including supported browsers, input methods, display sizes, assistive technology, and selected conformance criteria.
- [ ] **REL.07.02** Map each applicable criterion or usability objective to interface states, test procedures, evidence, owner, and unresolved issue disposition.
- [ ] **REL.07.03** Evaluate core tasks for keyboard operation, visible focus, readable text, semantic structure, alternative imagery descriptions, errors, and status announcements.
- [ ] **REL.07.04** Evaluate pause, defer, enlarge, comfort settings, accidental activation prevention, and interruption recovery in the intended treadmill-side use context.
- [ ] **REL.07.05** Ensure charts, route maps, and visual game feedback have task-equivalent text or structured alternatives needed to understand decisions and progress.
- [ ] **REL.07.06** Complete the actual launcher-to-dossier-to-save journey with supported accessibility configurations and record reproducible observations for any failures.
- [ ] **REL.07.07** Review issue dispositions against user impact, rejecting unsupported conformance claims or exceptions that leave an essential task inaccessible without a usable alternative.
- [ ] **REL.07.08** Retain assessment evidence and accepted limitations; accept when the released core experience meets its declared accessibility scope and practical walking-use requirements.

### Control REL 08

**Original requirement REL.08:** Complete applicable authorization, content-sanitization, storage, dependency, transport, credential, and privacy checks for the enabled deployment.

- [ ] **REL.08.01** Define the selected security and privacy review scope for loopback service, repository storage, browser rendering, optional network integrations, and distributed dependencies.
- [ ] **REL.08.02** Review origin and nonce enforcement, request schemas, private-file isolation, content sanitization, credentials, and supported local transport assumptions against applicable controls.
- [ ] **REL.08.03** Inventory bundled and external dependencies with versions, provenance, update responsibility, and reviewed issue applicability for the frozen candidate.
- [ ] **REL.08.04** Inspect storage and export paths for private workout, journal, profile, and credential data, documenting access assumptions for the selected local deployment.
- [ ] **REL.08.05** Assess optional remote services separately, including user consent, transmitted fields, credential storage, retention, and failure behavior when disabled.
- [ ] **REL.08.06** Run the candidate's applicable security checks and confirm supported launch, save, resume, and export tasks still function with protections enabled.
- [ ] **REL.08.07** Resolve or explicitly disposition findings with evidence and owner; avoid representing a limited local review as independent certification or broader infrastructure assurance.
- [ ] **REL.08.08** Archive the scoped review and findings; accept when the actual released surface has an attributable security and privacy disposition.

### Control REL 09

**Original requirement REL.09:** Verify local diagnostics and support bundles exclude private reflections, secrets, unnecessary biometric data, and unneeded persistent identifiers; preserve minimum run/operation correlation for recovery.

- [ ] **REL.09.01** Define a diagnostic data classification covering run metadata, operation correlation, journal content, credentials, nonces, personal profiles, and optional biometric observations.
- [ ] **REL.09.02** Specify allowable diagnostic fields and prohibit raw sensitive bodies or secret-bearing request headers from default logs and error reports.
- [ ] **REL.09.03** Apply redaction at collection and support-bundle generation boundaries, preserving safe identifiers needed to reconstruct failed launches and saves.
- [ ] **REL.09.04** Set retention and deletion rules for logs and bundles independently from authoritative activity records so troubleshooting retention cannot silently govern workout history.
- [ ] **REL.09.05** Provide a preview and explicit sharing action for any support bundle leaving the device, with selected scope and visible redaction status.
- [ ] **REL.09.06** Exercise errors using distinctive sensitive test values, then search logs, exported bundles, and browser error details for prohibited disclosure.
- [ ] **REL.09.07** Confirm redacted evidence still links one failure across run, instance, job, and operation records without exposing journal or biometric values.
- [ ] **REL.09.08** Retain redaction tests and diagnostic field policy; accept when support evidence is useful and contains only the approved minimum personal information.

### Control REL 10

**Original requirement REL.10:** Meet the documented performance and storage budgets on named reference devices, including a long session with backgrounding, image loading, and accumulated campaign history.

- [ ] **REL.10.01** Specify performance budgets for startup, readiness, dossier display, mutation acknowledgement, history queries, background jobs, and resource consumption on identified reference hardware.
- [ ] **REL.10.02** Record operating system, runtime, browser, storage type, dataset size, media cache state, and optional integrations for each measured candidate.
- [ ] **REL.10.03** Include long workout sessions, background-tab transitions, image loading, large journals, and substantial run or workout history in representative workloads.
- [ ] **REL.10.04** Measure response distribution and peak memory, CPU, disk, and lock duration where relevant rather than relying on one favorable interactive run.
- [ ] **REL.10.05** Check that media processing and history queries cannot starve pause, status, save, or controlled shutdown operations beyond declared limits.
- [ ] **REL.10.06** Run cold and warm startup plus a sustained-session workload, comparing observed results against each applicable budget.
- [ ] **REL.10.07** Exercise a slow asset and large-history fixture, documenting bottlenecks and accepted limitations with their user-visible consequences.
- [ ] **REL.10.08** Retain reproducible measurements and dispositions; accept when the selected hardware and data scale deliver the promised core responsiveness.

### Control REL 11

**Original requirement REL.11:** Exercise content withdrawal, application migration, interrupted local mutation, database repair, consistent backup restoration, and rollback or forward repair; retain recovery evidence.

- [ ] **REL.11.01** Define release recovery procedures for content withdrawal, schema migration failure, interrupted mutations, damaged local artifacts, and incompatible application updates.
- [ ] **REL.11.02** Identify which actions permit application rollback, which require forward repair, and how schema compatibility prevents unsafe older-code writes.
- [ ] **REL.11.03** Require verified backup or snapshot preconditions for state-changing recovery steps and preserve the last known usable artifact until replacement is validated.
- [ ] **REL.11.04** Specify how withdrawn imagery or facts receive attributable substitutes without silently rewriting completed decisions, accepted workouts, or route positions.
- [ ] **REL.11.05** Document interrupted-operation lookup and idempotent replay so recovery staff or users do not repeat already committed effects.
- [ ] **REL.11.06** Rehearse migration interruption, withdrawal, dossier recovery, database repair, consistent backup restoration, and supported rollback or forward repair using isolated campaigns with known progress.
- [ ] **REL.11.07** Verify recovery restores or preserves the expected continuation pointer, active day, completion ledger, and audit trail under every supported repair path.
- [ ] **REL.11.08** Retain recovery rehearsals and compatibility limits; accept when the candidate has a tested path back to usable preserved history after material failure.

### Control REL 12

**Original requirement REL.12:** Publish support information explaining progression modes, actual/fictional distinctions, manual data correction, offline readiness, saving status, and known limitations.

- [ ] **REL.12.01** Publish operating instructions for launching, resuming an unfinished day, completing a leg, reviewing history, stopping the service, and relocating the repository.
- [ ] **REL.12.02** Explain enabled progression modes, default selection, eligibility, conversion units and rules, and distinctions between real workouts, accepted credits, virtual days, facts, and fictional consequences.
- [ ] **REL.12.03** Document manual entry and correction rules, including attribution, units, downstream summaries, and effects on future credits or deliberate repair.
- [ ] **REL.12.04** Describe offline readiness and truthful save indicators, including what an uncertain response means and how to verify a committed operation safely.
- [ ] **REL.12.05** List known limitations affecting supported platforms, route coverage, imagery, integrations, accessibility, and recovery without burying essential operational constraints.
- [ ] **REL.12.06** Have a reviewer follow documentation from a fresh local setup through partial activity, restart, completion, backup, and restore without undocumented steps.
- [ ] **REL.12.07** Introduce a stale tab, failed browser opening, and missing media fixture; verify the documented advice matches actual errors and preserves user work.
- [ ] **REL.12.08** Retain documentation walkthrough evidence; accept when the user can operate and recover the released experience with accurate progress and save expectations.

### Control REL 13

**Original requirement REL.13:** Assign owners and review cadences for source changes, route releases, media rights expiration, educational accuracy, application dependencies, and browser compatibility.

- [ ] **REL.13.01** Assign accountable owners and review cadence for route data, factual sources, photo rights, lessons, training content, story rules, dependencies, and browser compatibility.
- [ ] **REL.13.02** Record provenance, last review, next review trigger, issue intake route, and affected manifest or application versions for each maintained collection.
- [ ] **REL.13.03** Define event-driven reviews for source withdrawal, route release changes, rights expiry, material dependency issues, and breaking browser or runtime changes.
- [ ] **REL.13.04** Specify how review results become versioned changes, targeted withdrawals, accepted exceptions, or explicitly unchanged records with rationale.
- [ ] **REL.13.05** Link changed assets and rules to affected parent and child controls so maintenance triggers proportionate revalidation rather than untracked replacement.
- [ ] **REL.13.06** Run a maintenance rehearsal using one changed source and one dependency notice, verifying ownership, impact assessment, and release traceability.
- [ ] **REL.13.07** Check for unowned content and overdue rights or compatibility review; verify such gaps appear in the release or maintenance disposition register.
- [ ] **REL.13.08** Retain the ownership register and review examples; accept when every released collection has a practical maintenance and correction responsibility.

### Control REL 14

**Original requirement REL.14:** Define actionable indicators for failed launches/saves, duplicate-effect prevention, unresolved conflicts, broken dependencies, crash frequency, and backup health, with thresholds appropriate to the local deployment.

- [ ] **REL.14.01** Define local operational indicators for failed launches, failed or uncertain saves, prevented duplicate effects, unresolved conflicts, broken assets, crashes, and backup health.
- [ ] **REL.14.02** Specify event sources, counting windows, denominator meanings, thresholds, and reset behavior so repeated retries do not falsely appear as distinct successful activity.
- [ ] **REL.14.03** Distinguish prevented duplicate requests from actual duplicate durable effects, which require separate severity and reconciliation treatment.
- [ ] **REL.14.04** Provide actionable local status or diagnostics appropriate to a single-user installation, with optional broader monitoring only when that deployment exists.
- [ ] **REL.14.05** Associate each threshold with an owner or user-facing recovery action and suppress repeated unchanged notices according to the selected operating policy.
- [ ] **REL.14.06** Inject representative launch, save, conflict, asset, crash, and backup failures and verify the expected indicator and recovery guidance.
- [ ] **REL.14.07** Check indicators against known authoritative records and redact private fields; ensure missing telemetry is classified as unavailable rather than zero failures.
- [ ] **REL.14.08** Retain indicator definitions and fixture results; accept when operational signals identify real actionable problems at the application's actual scale.

### Control REL 15

**Original requirement REL.15:** Separate optional product analytics from user activity records; document consent, retention, aggregate definitions, and whether small-group reporting could reveal individual behavior.

- [ ] **REL.15.01** Separate required local workout and campaign history from optional product analytics by storage purpose, collection mechanism, and user control.
- [ ] **REL.15.02** Define each optional analytic event, transmitted or retained fields, destination, aggregation method, retention period, and deletion procedure.
- [ ] **REL.15.03** Obtain the selected explicit consent before optional collection or transfer and preserve normal local operation when analytics are declined or later disabled.
- [ ] **REL.15.04** Specify how aggregation treats small groups, repeated devices, rare events, and combinations that could reveal an individual's training or journal behavior.
- [ ] **REL.15.05** Prevent journal text, raw biometric observations, secrets, and unnecessary exact activity history from entering product analytics through generic event logging.
- [ ] **REL.15.06** Compare analytics-enabled and disabled journeys, verifying identical authoritative hike behavior and only the consented optional event differences.
- [ ] **REL.15.07** Withdraw consent and inspect queued events, stored identifiers, and subsequent traffic; verify the documented deletion and cessation behavior.
- [ ] **REL.15.08** Retain consent and aggregation evidence; accept when optional analytics remain distinguishable, controllable, and proportionate to their declared purpose.

### Control REL 16

**Original requirement REL.16:** Establish defect intake, severity, triage, correction, release communication, and incident review procedures; give urgent factual or rights corrections a targeted withdrawal path.

- [ ] **REL.16.01** Define defect intake fields for affected build or manifest, control IDs, reproducible behavior, user impact, privacy sensitivity, and safe supporting evidence.
- [ ] **REL.16.02** Specify severity and triage rules that distinguish lost progress, incorrect training incentives, factual errors, rights issues, accessibility barriers, and cosmetic defects.
- [ ] **REL.16.03** Assign acknowledgement, investigation, correction, and release communication responsibilities appropriate to the actual maintenance team or individual operator.
- [ ] **REL.16.04** Provide targeted withdrawal for urgent factual or rights problems, identifying affected assets and usable substitutes without unnecessarily disabling unrelated stages.
- [ ] **REL.16.05** Require regression evidence tied to the original failure and affected controls before marking a correction resolved in a release.
- [ ] **REL.16.06** Rehearse one progress-loss report and one urgent image-rights withdrawal, verifying intake, impact assessment, correction, and user-visible disposition.
- [ ] **REL.16.07** Review incident records for causal explanation, recurrence prevention, and evidence redaction without inventing certainty beyond observed facts.
- [ ] **REL.16.08** Retain triage and correction examples; accept when users have an attributable route from defect discovery to verified repair or targeted content withdrawal.

### Control REL 17

**Original requirement REL.17:** Define the maintenance budget, version-support policy, integration deprecation procedure, and end-of-service export plan for the actual product scale.

- [ ] **REL.17.01** Define the maintenance budget in time, storage, hosting if used, content licensing, dependency updates, and supported integration effort for the intended product scale.
- [ ] **REL.17.02** Publish application, schema, runtime, and content version-support policy, including compatibility windows and how users receive actionable update information.
- [ ] **REL.17.03** Specify integration deprecation steps covering notice, alternative workflows, credential removal, retained history, and export of integration-specific records.
- [ ] **REL.17.04** Define an end-of-service plan that preserves repository-local launching where feasible and explains any dependency on discontinued external services.
- [ ] **REL.17.05** Provide documented export formats for authoritative activity, campaign history, journals, and rights-permitted content references with compatibility metadata.
- [ ] **REL.17.06** Rehearse disabling an optional integration and exporting a complete campaign, checking that local progress remains usable and exported records reconcile.
- [ ] **REL.17.07** Review maintenance commitments against available resources and record unsustainable scope as a visible limitation or scheduled deprecation rather than an unsupported promise.
- [ ] **REL.17.08** Retain support policy and continuity rehearsal evidence; accept when users can maintain or leave the application without losing access to their recorded hike.

### Control REL 18

**Original requirement REL.18:** Obtain attributable acceptance from the accountable application, content, training, narrative, accessibility, and user-data owners for their affected evidence; archive the final record with the release.

- [ ] **REL.18.01** Identify accountable application, content, training, narrative, accessibility, and user-data reviewers, allowing one person to hold several explicitly recorded roles.
- [ ] **REL.18.02** Prepare each reviewer an evidence package scoped to affected controls, exact candidate versions, open defects, exceptions, and material limitations.
- [ ] **REL.18.03** Record acceptance, conditional acceptance, or rejection with reviewer identity, role, timestamp, affected scope, rationale, and evidence references.
- [ ] **REL.18.04** Require explicit disposition of unresolved conditions and prohibit treating absent review, automated test success, or a generic checkbox as attributable human acceptance.
- [ ] **REL.18.05** Invalidate or reopen affected acceptance when a frozen build, content manifest, training rule, schema, or material exception changes before release.
- [ ] **REL.18.06** Cross-check the final acceptance matrix against the applicability register and release record, verifying all selected responsibilities are covered.
- [ ] **REL.18.07** Archive evidence with integrity metadata and a retrieval index, protecting personal test data and retaining only the required reviewed artifacts.
- [ ] **REL.18.08** Retain the signed or otherwise attributable final decision record; accept release only when every required role has reviewed its actual affected evidence.

## Source and applicability record

Original baseline SHA-256: `50f42e5a5c2329519c899d6770aa008597aa9b32fb83e12a44674aaffdf5393b`. The original 465 IDs and requirement sentences are preserved. These proposed application requirements extend the baseline and do not constitute completed implementation evidence or certification.

Refer to the [original reference sources and applicability](PCT_Training_Adventure_Checklist.md#reference-sources-and-applicability) for the established route, preparation, accessibility, security, scripting, and database references. Record the exact source, edition, runtime, and license applicable to the selected implementation before evaluating the related controls.
