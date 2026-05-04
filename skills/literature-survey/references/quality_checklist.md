# Quality Checklist

Before delivering results, verify all items.

## Frame (Phase 1)

- [ ] Research Questions (RQs) defined and confirmed with user
- [ ] Inclusion / exclusion criteria defined before search
- [ ] Depth (focused / broad) determined; target paper count agreed
- [ ] User-known abbreviations collected, if any
- [ ] `survey_slug` confirmed with user

## Map (Phase 2)

- [ ] All three temporal tiers represented in the mapped set
- [ ] Snowballing executed: 5–10 seeds + 1–2 hop expansion
- [ ] Preprints included to counter publication bias
- [ ] Every paper has at least one of: publisher DOI, arXiv ID, or URL
- [ ] DOIs resolved inline where possible (arXiv → publisher DOI)
- [ ] Duplicates removed
- [ ] I/E criteria applied at Map Checkpoint with reasons noted
- [ ] Map Checkpoint completed — user approved the paper list before
      proceeding to hub selection
- [ ] Per-paper extraction limited to: 1-line contribution + 3-5 concept tags
      (no premature thesis/core/diff/limit annotation for non-hubs)

## Hubs (Phase 3)

- [ ] Hub selection criteria applied: B (cluster bridging + top-tertile
      citations) AND/OR C (synthesis centrality)
- [ ] Hub count within 5–10 range
- [ ] Hub list confirmed with user before deep read
- [ ] PDFs acquired for all approved hubs (or user-confirmed exceptions)
- [ ] PDFs placed at `./literature/papers/{citekey}/main.pdf` with
      correct citekey per `/paper-summary` regulation
- [ ] `/paper-summary` invoked on each hub; resulting note paths recorded

## Synthesize (Phase 4)

- [ ] thesis derived from hub deep reads + concept matrix patterns
- [ ] foundation aggregated from hub deep reads' approach-and-core-elements
      sections + training/optimization sections (shared losses, datasets)
- [ ] progress traces a chronological trajectory using hub novelty sections
- [ ] gap grounded in (a) converging hub discussions, (b) matrix sparsity,
      (c) frontier diffs
- [ ] If user requested research proposals: seed section included per
      `references/seed_format.md`
- [ ] Survey-level claims cite hub papers via wikilink
- [ ] Concept matrix populated for all mapped papers (rows × concepts)
- [ ] Quantitative trends tabulated (year count, concept distribution,
      experiment settings, top venues)

## Verify & Output (Phase 5)

- [ ] reference-verify completed — all papers checked for hallucinations
- [ ] Excluded unverifiable papers reported
- [ ] Output file at `./literature/surveys/{survey_slug}.md`
- [ ] Hub papers linked via Obsidian wikilink to deep-read notes
- [ ] Non-hub papers represented in concept matrix and 1-line catalogue entry
- [ ] `literature/surveys/README.md` table updated
- [ ] `notes/LOGS/literature-survey.md` appended with this run

## Report Structure

- [ ] Abstract follows 4-sentence structure (state / contribute / findings / method)
- [ ] Terminology section maps term variants
- [ ] Concept matrix is the primary at-a-glance artifact
- [ ] Hub Papers section lists all hubs with links to deep notes
- [ ] Paper Catalogue groups non-hub papers by category
- [ ] Survey Methodology covers Frame / Map / Hub Selection / Verify in
      a single block (not 4 separate logs)
- [ ] Conclusion answers each Research Question
- [ ] Output language consistent throughout — no language mixing
- [ ] Abbreviation Glossary included (Abbreviation | Full name | First occurrence)
