# Quality Checklist

Before delivering results, verify all items:

## Research Design

- [ ] Research Questions (RQs) defined and confirmed with user
- [ ] Inclusion/exclusion criteria defined before search
- [ ] Keyword set with synonyms/variants constructed from RQs

## Search & Collection

- [ ] All three temporal tiers are represented
- [ ] Preprints included to counter publication bias
- [ ] Search Review Checkpoint (Phase 2.5) completed — user approved the paper list before analysis
- [ ] Inclusion/exclusion criteria applied at checkpoint with reasons noted
- [ ] Duplicates removed and count recorded in search log
- [ ] Search Log records every search action: source, exact query/URL, result count, and notes
- [ ] Source summary lists all information sources used and query counts

## Paper-Level Analysis

- [ ] Each paper has: title, authors, year, venue/source, publisher DOI (or arXiv ID if unpublished), and thesis/core/diff/limit
- [ ] limit fields contain only author-stated limitations (no LLM speculation)
- [ ] Phase 3a/3b split: OA papers processed first, paywall papers batched by publisher

## DOI & Verification

- [ ] DOI Resolution phase completed — arXiv-only papers checked against DBLP/Semantic Scholar/Crossref for publisher DOIs
- [ ] Hallucination check completed — all papers verified via DOI/URL

## Report Structure

- [ ] Abstract follows 4-sentence structure (state/contribute/findings/method)
- [ ] Terminology section maps term variants
- [ ] Comparison table covers key papers cross-cuttingly
- [ ] Quantitative trends tabulated (year count, method distribution, experiment settings)
- [ ] Concept matrix maps concepts to papers
- [ ] Papers are organized by category, not just listed chronologically
- [ ] The overview section gives a reader unfamiliar with the topic a clear starting point
- [ ] Survey Findings section contains thesis, foundation, progress, and gap
- [ ] If user requested research proposals: seed section included (see `references/seed_format.md`)
- [ ] Survey-level claims are traceable to specific paper-level annotations
- [ ] Foundational works table includes #, paper, year, venue, and significance
- [ ] Threats to Validity section discusses search scope, publication bias, selection bias, and analysis limitations
- [ ] Conclusion answers each Research Question
- [ ] Output language is consistent throughout — no mixing of languages
