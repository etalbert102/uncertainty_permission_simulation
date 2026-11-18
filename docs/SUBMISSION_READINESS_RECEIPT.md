# Submission Readiness Receipt

Date: 2026-11-16

Status: local submission package complete; public-repository activation intentionally deferred

## Scope

This receipt covers the integrated article, APA Word review copy, optional online technical appendix, evidence packet, frozen simulation artifacts, and repository verification controls. It certifies the local package, not acceptance by a publisher or activation of an external repository.

## Article and appendix

- The article contains the complete five-step process-red-team procedure and the worked Robodebt application conclusion. Its claims and interpretation do not depend on supplementary material.
- `ARTICLE_SUPPLEMENTARY_MATERIAL.md` is an optional online technical appendix containing implementation-level status codes, receipt fields, worksheets, and worked-trace detail. It may be withheld if a venue does not accept supplementary material.
- The conservative Markdown-source count is 9,558 whitespace-delimited words before the bibliography, 442 below the 10,000-word ceiling. A document-order count of the rendered Word content is 9,536 pre-reference word tokens. The conservative source count controls the release decision.
- The manuscript uses no endnotes to evade the word ceiling.

## APA Word review copy

- `ARTICLE_MANUSCRIPT_APA.docx` contains 48 rendered pages, two tables with repeating header rows, three figures with alternative-text descriptions, 33 hyperlinks, and three correctly oriented sections.
- Every rendered page was visually inspected. A long-reference wrapping collision found on page 44 was corrected in the reporting-only exporter and the affected reference pages were regenerated and reinspected.
- The final archive passes ZIP integrity checks. The accessibility audit reports zero high-, medium-, or low-severity findings; the image and section audits report the expected three figures and three sections.
- Author and last-modified-by metadata are blank, revision-session identifiers were scrubbed, and the export utility remains outside the frozen `scripts/*.py` inventory.

## Call-fit editorial pass

- On 2026-11-16, the abstract and introduction were revised to foreground AI-enabled organizational workflows and the call's emerging-technology theme.
- The manuscript now states its bounded original contribution affirmatively, adds a plain-language bridge into the formal model, uses descriptive policy names alongside internal IDs, and presents a compact owner–intervention–tradeoff implementation map.
- These are reader-facing editorial changes only. No formal definition, source mapping, parameter, policy, seed, metric, stored result, quantitative interpretation, or claim boundary changed, and no usability or field-transfer claim was added.

## Scientific and repository controls

- The immutable 77-file scientific manifest remains unchanged at SHA-256 `35f360d81e7eebe1effeae813f4144991b0fa043001df6d920d3f8592bfee65c`.
- The final source audit and literature update are complete. They found no substantive contradiction in the historical, formal, trace, or numerical claims and did not change the frozen study.
- Plan, Slice 0, and Slice 3 validators pass; all 178 tests pass; and the technical release gate passes with the frozen core and sensitivity artifacts.
- Per-attempt outputs remain intentionally ignored because they are large reproducible intermediates. The repository retains the frozen inputs, exact environment and seed inventories, compact indexes, reconciliations, analyses, figures, and receipts needed to regenerate and verify them.

## Remaining external activation

The sole remaining pre-submission activation is to make the project repository public and confirm that the manuscript's data-and-code link resolves. That action remains under project-lead control and was not performed by this local readiness pass. No external-reader return, formal comprehensibility review, usability study, or supplement-eligibility assumption is a release condition.

This receipt does not claim historical causal identification, empirical calibration to Robodebt, field efficacy, practitioner usability, inter-rater reliability, or legal judgment.
