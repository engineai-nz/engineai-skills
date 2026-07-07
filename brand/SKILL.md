---
name: engine-ai-brand
description: >
  Applies The Agent Maestros / Engine AI brand identity, design system, and visual language to any
  React artifact, HTML page, dashboard, landing page, or interactive tool. Use this skill
  whenever building ANYTHING visual for The Agent Maestros, Engine AI, Ben du Chateau, Joe Ward,
  or any project that should carry the Agent Maestros or Engine AI look and feel. Trigger on:
  "Agent Maestros", "Engine AI", "maestros brand", "maestros style", "engine ai brand",
  "use the dark theme", "use our brand", "make it match the financial model", "same look as
  the lean canvas", or any artifact that is part of the Agent Maestros / Engine AI business,
  pitch materials, client deliverables, dashboards, or internal tools. Also trigger when the
  user says "brand guidelines", "design system", or "our style" in the context of Agent Maestros
  or Engine AI work. Also trigger for tone-of-voice tasks — copywriting, landing page copy,
  proposal language — for Engine AI. Always apply this skill to Agent Maestros / Engine AI
  artifacts even if the user doesn't explicitly ask for it — visual consistency is the default,
  not the exception.
---

# The Agent Maestros / Engine AI — Brand & Design System

> **Source of truth:** [engineai-nz/engineai-skills](https://github.com/engineai-nz/engineai-skills), `brand/SKILL.md` — extracted from the live site at engineai.co.nz. This file is the Cowork/artifact-adapted version of that spec: same tokens, palette, and voice, translated for inline-styled React/HTML artifacts (dashboards, financial models, decks) rather than the Tailwind/Next.js website build. When the canonical repo changes, pull the update through here too.
>
> If working locally in Claude Code with repo access, the live site's own design system docs (`DESIGN.md` and `colors_and_type.css` in the `engineai` project) supersede this summary on any conflict. This file remains the quick-reference and tone-of-voice guide for artifact work.

## When to Use

Apply this design system to **every** visual artifact built for The Agent Maestros or Engine AI. This includes dashboards, financial models, lean canvases, project trackers, client-facing tools, landing pages, pitch decks (React/HTML), and internal operator tools.

If you're building a React `.jsx` artifact or an `.html` page — use this system. No exceptions.

For Word documents (`.docx`) and PDFs, use the colour palette but follow standard document conventions (white background, dark text, Navy/Gold/Grey accents) — see the Word Document Variant in `references/design-tokens.md`.

## Design Philosophy

Dark-mode first. Data-rich but not cluttered. The aesthetic says: *"we live in the terminal but we make it beautiful."* Think Bloomberg Terminal meets premium editorial design — information density with clear visual hierarchy. Monochromatic blacks, whites, and greys form the base. A restrained touch of gold is the only general accent colour. Every element earns its place.

**Key principles:**
- Monospace for data, sans-serif for prose
- Gold is the single general accent colour — use it sparingly and with intent
- No teal or green as general accents (product sub-page exception below)
- Cards and surfaces use transparency and subtle borders — never solid blocks
- Charts use brand colours consistently — predominantly grey scale with gold highlight
- No animations on load — motion is reserved for hover/interaction and scroll-reveal only
- Headlines are light weight, never bold — confidence through restraint, not weight

---

## Full Design Reference

For the complete design system including all colour values, typography scale, component JSX snippets, chart configuration, and layout rules, read:

**`references/design-tokens.md`** — This is the comprehensive reference for artifact/component work. Load it before writing any styled code.

---

## Quick Reference (Key Tokens)

### Colours — Primary

| Name | Hex | Role |
|------|-----|------|
| Near-Black | `#0A0A0A` | Page background base |
| Surface Dark | `#111111` | Card / panel background |
| Gold | `#C4A35A` | Single general accent — KPI values, highlights, primary CTA, used sparingly |
| White | `#FFFFFF` | Primary headings, high-emphasis text |
| Off-White | `#E8E6E1` | Body text, secondary display on dark |

### Colours — Greyscale & Semantic

| Name | Hex | Role |
|------|-----|------|
| Mid Grey | `#888888` | Section titles, secondary accent, chart secondary lines |
| Grey | `#555555` | Borders, dividers, tertiary text |
| Faint Grey | `#2A2A2A` | Subtle borders, barely-visible structure |
| Red | `#e53935` | Negative / warning / conservative scenario |

### Colours — Product Accents (sub-pages only)

These exist on engineai.co.nz for specific product pages only. Never use them as general accents in dashboards, decks, or client artifacts — those stay gold-only.

| Product | Accent |
|---------|--------|
| OpenClaw | Teal `#2B8C8C` |
| Copilot | Blue `#0078D4` |
| Bespoke Builds | Green `#4CAF50` |

### Background

```css
background: linear-gradient(145deg, #080808 0%, #0f0f0f 40%, #0a0a0a 100%);
```

### Fonts

```css
/* Headings & body */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* Data, labels, monospace */
font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
```

### Card Surface

```css
background: rgba(12, 12, 12, 0.90);
border: 1px solid rgba(255, 255, 255, 0.07);
border-top: 3px solid #C4A35A;
border-radius: 8px;
```

---

## Typography Scale

| Element | Size | Weight | Tracking |
|---------|------|--------|----------|
| Hero / page title | `clamp(2rem, 4.6vw, 4.15rem)` on full pages, 24–28px in dashboards | Light (Semibold for gold emphasis line) | `-0.05em` |
| Section title | JetBrains Mono, 11px | Bold | uppercase, `1.5px`/`0.34em` |
| Card title | JetBrains Mono, 11px (or Inter 2xl on marketing pages) | Bold / Medium | uppercase |
| KPI / stat value | JetBrains Mono, 20–22px (up to 6xl–7xl on hero stats) | 800 / Light | tight |
| Body | Inter, 12–13px (dashboards) / base–lg (marketing) | Regular | `line-height: 1.55–1.8` |

**Rule:** headlines are light weight, large size, tight/negative tracking. Never bold a headline — gold emphasis lines can go semibold, everything else stays light. This is the single biggest tell of an on-brand vs off-brand build.

---

## Spacing & Layout

- **Max content width:** 1100–1200px for dashboards/artifacts, `max-w-6xl` for marketing pages, centred.
- **Section padding:** dashboards 24–32px; full marketing pages `py-24` mobile / `py-32` desktop.
- **Card gap:** 10–12px in dense dashboards, `gap-6`–`gap-12` in marketing grids.
- **Border radius:** 6–8px for dashboard cards, 1.75rem+ ("pill"-adjacent) for marketing cards, full pill for buttons.
- **Grid:** CSS Grid for card layouts, flexbox for stat rows and inline elements. Favour showing data over hiding it behind tabs/modals.

---

## Animation & Motion

- **No load animations.** Dashboards and data interfaces render instantly.
- **Scroll reveal (marketing pages only):** fade + slide up from `opacity-0 translate-y-6` to visible, ~800ms ease-out, staggered 100–340ms between siblings.
- **Hover:** cards lift `-translate-y-1`, border brightens to gold ~20% opacity, subtle gold-tinted shadow. Buttons lift `-translate-y-0.5` and brighten.
- **Transitions:** `all 0.25s ease` on interactive elements generally; `duration-500` on card hover.
- Nothing bouncy or playful. Motion is restrained, same as the palette.

---

## Tone of Voice

- **Direct.** No jargon, no buzzwords. Avoid "leverage" (as a verb), "synergy", "digital transformation", "delve", "navigate the complexities".
- **Grounded.** Practical, outcome-focused language over abstraction.
- **Calm authority.** Confident, not pushy. Low-pressure CTAs: "Book a Discovery Call", "See how we work", "No pitch. No obligation."
- **Operator language,** not consultant language: "Two operators. Not two consultants."
- Lead with the problem, then the outcome. Short sentences. Break long paragraphs into punchy lines.
- **NZ English throughout** — organisation, programme, colour, optimise, realise.
- **Zero em dashes** in any Engine AI copy — full stops, commas, or brackets instead.

Sample lines for calibration:
> "The biggest technology shift in a generation is happening right now. Most businesses are watching it happen to them."
> "We are not a consultancy that discovered AI. We are AI practitioners."
> "Start with a conversation. No pitch. No obligation."

---

## Rules

1. **Never use** generic fonts: Arial, Roboto, system-ui, or default sans-serif in artifacts.
2. **Never use** light/white backgrounds for artifacts (unless explicitly for print/docx).
3. **Never use** teal, green, or warm secondary colours as general accents. Palette is blacks, whites, greys, and a restrained gold — except the product sub-page accents above, which stay scoped to their own product page only.
4. **Always use** JetBrains Mono for numeric data, metrics, labels, and badges.
5. **Always use** Inter for body text and headings.
6. **Section titles** follow the pattern: uppercase JetBrains Mono + mid-grey `#888888` + bottom border.
7. **KPI values** are always JetBrains Mono, weight 800, sized 20–22px, coloured Gold `#C4A35A` or white `#FFFFFF`.
8. **Gold is the single general accent.** Use it for one or two key elements per view — not decoration.
9. **Charts** use: Gold for primary/highlighted data, `#888888` for secondary, `#555555` for tertiary, grey dashed for baselines.
10. **Headlines are light weight**, never bold. Tight/negative letter-spacing on large type.
11. **Buttons are pill-shaped.** Primary = gold fill + black text. Secondary = glass/transparent + mono uppercase label.
12. **Team or people photography** renders in greyscale, never colour.
13. **Max content width** is 1100–1200px, centred (dashboards); `max-w-6xl` (marketing).
14. **Footer** on every artifact: monospace, 10px, colour `#333`, centred, includes document name and date.
15. **Copy follows the tone-of-voice section above** — direct, NZ English, zero em dashes, no corporate padding.

---

## Assets Reference (marketing site only — guidance, not accessible in Cowork sandbox)

- **Logo:** three horizontal bars with descending opacity, default colour `#d7d5d1`.
- **Team photography:** always greyscale.
- **Hero background:** looping muted video on the marketing site; use a static gradient/blur-blob background instead for artifacts.

## Responsive Breakpoints (marketing pages)

| Breakpoint | Width | Key changes |
|------------|-------|-------------|
| base | 0px | Single column, mobile nav |
| `md` | 768px | 2-col layouts, larger type |
| `lg` | 1024px | 3–4 col layouts, desktop nav |
| `xl` | 1280px | Extended layouts |

Artifacts built in Cowork are generally single-viewport; treat this as guidance for anything destined for the live site rather than a hard requirement for dashboards.
