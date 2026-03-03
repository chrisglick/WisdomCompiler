---
prd: true
id: PRD-20260302-fix-mobile-layout-truncation
status: COMPLETE
mode: interactive
effort_level: Extended
created: 2026-03-02
updated: 2026-03-02
iteration: 0
maxIterations: 128
loopStatus: null
last_phase: VERIFY
failing_criteria: []
verification_summary: "10/10"
parent: null
children: []
---

# Fix Mobile Layout Truncation and Horizontal Scrollbar

> Fix the WisdomCompiler mobile view where text is truncated on the right side and a horizontal scrollbar appears at 375px viewport width.

## STATUS

| What | State |
|------|-------|
| Progress | 10/10 criteria passing |
| Phase | COMPLETE |
| Next action | Deploy to Cloudflare |
| Blocked by | nothing |

## CONTEXT

### Problem Space
The WisdomCompiler site at 375px viewport shows all text truncated on the right edge and a horizontal scrollbar. The current custom.scss uses `overflow-x: hidden` as a band-aid, masking content that's genuinely wider than the viewport instead of fixing the root cause.

### Root Cause
`html { width: 100vw }` in Quartz's `base.scss` line 11. `100vw` includes vertical scrollbar width, making the document wider than the visible viewport. Combined with no global `box-sizing: border-box`, padding on elements adds to computed widths.

### Key Files
- `quartz/styles/custom.scss` — our override file (primary edit target)
- `quartz/styles/base.scss` — Quartz upstream, contains `html { width: 100vw }`
- `quartz/styles/variables.scss` — breakpoints: mobile=800px, desktop=1200px
- `quartz/components/Head.tsx` — viewport meta tag (confirmed present)

### Constraints
- Prefer custom.scss overrides over editing base.scss (upstream maintainability)
- Must not break desktop layout (1200px+)
- Quartz build must succeed

## PLAN

1. Override `html { width: 100% }` outside mobile media query (fixes 100vw bug)
2. Add `*, *::before, *::after { box-sizing: border-box }` globally
3. Remove all `overflow-x: hidden` band-aids from mobile section
4. Replace `max-width: 100vw` with `max-width: 100%` in mobile section
5. Increase `p, li, td` font-size from 0.95rem to 1rem (16px) for readability
6. Build with `npx quartz build`
7. Verify with Browser skill at 375px and 1920px

## IDEAL STATE CRITERIA (Verification Criteria)

- [x] ISC-C1: No horizontal scrollbar present at 375px viewport width [E] | Verify: Browser: scrollWidth === clientWidth at 375px
- [x] ISC-C2: All body text fully visible without right-side truncation [E] | Verify: Browser: screenshot at 375px
- [x] ISC-C3: Body text renders at readable size on mobile devices [E] | Verify: Browser: computed font-size >= 16px
- [x] ISC-C4: Content containers wrap within 375px viewport without overflow [E] | Verify: Browser: no element offsetWidth > 375
- [x] ISC-C5: Root cause identified in Quartz layout CSS not just masked [I] | Verify: Read: custom.scss fixes width not overflow
- [x] ISC-C6: Quartz build succeeds with all CSS changes applied [I] | Verify: CLI: npx quartz build
- [x] ISC-C7: Viewport meta tag includes width=device-width in HTML output [I] | Verify: Grep: viewport meta in Head.tsx
- [x] ISC-C8: Desktop layout at 1920px renders identically to current state [E] | Verify: Browser: screenshot at 1920px
- [x] ISC-A1: No overflow-x hidden used as primary mobile fix strategy [R] | Verify: Read: custom.scss overflow-x usage
- [x] ISC-A2: No hardcoded pixel widths added that break other viewports [R] | Verify: Read: check for px widths

## DECISIONS

- 2026-03-02: Override html width in custom.scss instead of editing base.scss — preserves upstream Quartz compatibility
- 2026-03-02: Use minmax(0, 1fr) instead of 1fr for mobile grid column — minmax(0, ...) overrides min-width:auto default that can cause overflow

## LOG

### Iteration 1 — 2026-03-02
- Phase reached: VERIFY (COMPLETE)
- Criteria progress: 10/10
- Work done: Identified 3 root causes (100vw, no box-sizing, grid auto column), rewrote custom.scss, verified via Browser skill
- Failing: none
- Context: Ready to deploy to Cloudflare
