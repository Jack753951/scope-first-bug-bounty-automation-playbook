> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video Source Candidate Pre-Scoring Pattern

Use this when a Shorts/video automation project can technically render drafts but source selection is strategically off-target.

## Trigger

- Draft generation works, render QA passes, but the selected story/topic does not match the channel's latest learning signal.
- The channel pulls from a live source pool (Reddit, RSS, trend APIs, competitor-inspired topics, etc.) and currently chooses by raw popularity/randomness.
- The user wants a systematic, extensible optimization layer rather than one-off prompt tweaks.

## Implementation pattern

1. Define transparent labels from the latest learning summary.
   - Example target labels for Reddit story channels: `family-betrayal`, `parent-control`, `public-humiliation`, `inheritance-money`, `secret-exposure`, `forbidden-food/allergy/religion`.
   - Define negative labels too, e.g. low-stakes comedy, niche hobby/event, resolved past trauma.
   - Add tone-risk negative labels when private-output QA reveals a technically valid but strategically risky draft. Example: `gross-out-sustained-retaliation` for repeated spitting/contamination revenge that may be high-hook but advertiser-unsafe.
   - Prefer contamination/action phrases over neutral object terms. For example, use `spit in his drink`, `spit on her toothbrush`, `tampered with food`; avoid standalone neutral objects like `toothbrush`, `lotion`, `hairbrush`, or `aftershave` unless tests prove they are safe.
2. Score candidates before script generation.
   - Keep source popularity as a tie-breaker, not the primary selector.
   - Preserve source URL, source subreddit/feed, fit score, matched labels, penalties, and reasons in downstream metadata.
3. Use phrase/word-boundary matching for rubric terms.
   - Avoid naive substring matches: `mom` must not match `moment`; generic `will` should not trigger inheritance logic.
   - Prefer phrase-level terms for ambiguous keywords (`the will`, `changed the will`) or require multiple complementary signals.
4. Rank a larger candidate pool, then choose from the top fit band to avoid always picking the exact same item.
5. If no high-fit candidate exists, fall back safely and attach a warning such as `no_high_fit_candidate_found` so the draft is not mistaken for a strong canary.
6. Add tests for:
   - high-fit candidate beating high-source-score off-target candidate;
   - risky high-hook candidate being demoted by tone-risk penalties (for example, gross-out retaliation losing to cleaner interpersonal unfairness);
   - direct penalty detection for the risky pattern;
   - fallback warning when no high-fit candidate exists;
   - false-positive keyword boundaries, including negative-label terms (`spitfire` should not match `spit`; neutral object mentions should not trigger contamination penalties unless paired with an action phrase);
   - metadata propagation of source fit fields;
   - empty/malformed candidate robustness where practical.
7. Run one upload-free draft or review the next private scheduled output after implementation and inspect:
   - selected source labels/reasons;
   - metadata fit fields;
   - SRT text, not only visual QA;
   - render QA and contact sheet;
   - first-4-seconds visual distinctness for Shorts: if the opening contact sheet repeats one background through the hook, record it as a non-blocking opening-energy issue and consider requiring at least two distinct visual beats before 4s for future canaries;
   - canary/no-canary decision gate.

## Review checklist for Codex/Claude reviewers

- Does source selection now reflect the learning signal, not just raw platform popularity?
- Do negative labels capture strategic tone risk without turning into hard blocks for the whole niche?
- For tone-risk labels, are triggers phrased as actions/contamination patterns rather than neutral props or setting words?
- Are scoring reasons transparent enough for future handoff/research review?
- Are ambiguous keywords protected from substring false positives?
- Are source fit fields persisted to metadata/reports, not only console logs?
- Are safety boundaries preserved: no upload/publication, scheduler, OAuth/token, privacy-default, or runtime data deletion changes unless explicitly requested?
- Did the implementation add regression tests and run local validation directly, not only worker/sandbox validation?
