# Engine AI Brand Tokens

Use this reference after `brand/SKILL.md` when writing styled code or producing a visual deliverable. It is the detailed artifact-facing reference for the packaged `brand` skill in `engineai-nz/engineai-skills`.

For local Engine AI builds, the live design-system files supersede this summary on conflicts:

- `/home/duchats/projects/engineai/design-system/DESIGN.md`
- `/home/duchats/projects/engineai/design-system/colors_and_type.css`

## Identity

Near-black canvas, warm off-white text, restrained gold, light-weight Inter headlines, uppercase JetBrains Mono labels, and quiet operator confidence. The work should feel precise, premium, and built by people who live close to the tools.

## Core Colours

| Token | Value | Use |
|---|---:|---|
| `--color-bg-primary` | `#0A0A0A` | Default dark canvas |
| `--color-bg-surface` | `#111111` | Alternating dark section or panel |
| `--color-bg-card` | `rgba(12, 12, 12, 0.84)` | Transparent card fill |
| `--color-bg-card-opaque` | `rgba(12, 12, 12, 0.90)` | Dense dashboard card fill |
| `--color-gold` | `#C4A35A` | CTAs, top bars, active states, one highlighted line |
| `--color-gold-ink` | `#8A6C2A` | Gold text/icons on light backgrounds |
| `--color-text-primary` | `#FFFFFF` | Headlines and high-emphasis text |
| `--color-text-body` | `#E8E6E1` | Body text on dark |
| `--color-text-secondary` | `#ACA69B` | Labels and mono captions |
| `--color-text-muted` | `#918B80` | Body-size de-emphasis only |
| `--color-border` | `rgba(255, 255, 255, 0.07)` | Default border |
| `--color-border-strong` | `rgba(255, 255, 255, 0.12)` | Strong border, glass edge |
| `--color-border-gold` | `rgba(196, 163, 90, 0.24)` | Gold border or focus ring |

Do not hand-pick greys. Avoid raw `#888`, `#555`, and similar shortcuts in production UI. Use the named tokens or their closest artifact equivalent.

## Product Accents

Use product accents only when the whole surface is scoped to that product. Do not use them as general dashboard accents.

| Product | Accent |
|---|---:|
| OpenClaw | `#2B8C8C` |
| Copilot | `#0078D4` |
| Bespoke Builds | `#4CAF50` |

## Theme Variants

Dark is the default for dashboards, tools, HTML artifacts, and marketing pages.

Light surfaces are allowed for Word documents, PDFs, print, and deliberate paper-style deliverables:

| Surface | Canvas | Text | Gold text |
|---|---:|---:|---:|
| Paper | `#FAF8F3` | `#2E2A24` | `#8A6C2A` |
| Pure | `#FFFFFF` | `#2E2A24` | `#8A6C2A` |
| Mist | `#F1EDE5` | `#2E2A24` | `#8A6C2A` |

For light output, keep the same restraint: one gold accent, neutral structure, no colourful decoration.

## Typography

| Role | Family | Notes |
|---|---|---|
| Headlines | Inter | Weight 300 light, tight leading, negative tracking |
| Body | Inter | Generous leading, warm off-white on dark |
| Labels | JetBrains Mono | Uppercase, tracked `0.2em` to `0.34em` |
| Data | JetBrains Mono | KPI values, metrics, badges, compact dashboard numbers |

Use semantic sizes. Do not invent tiny text.

| Context | Floor |
|---|---:|
| Web body | `16px` |
| Web small text | `14px` |
| Mono labels | `11px` |
| Deck body | `24px` |
| Print body | `12pt` |

Headline pattern:

```css
font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
font-weight: 300;
letter-spacing: -0.04em;
line-height: 1.1;
```

Mono label pattern:

```css
font-family: "JetBrains Mono", "SF Mono", "Fira Code", monospace;
font-size: 11px;
text-transform: uppercase;
letter-spacing: 0.24em;
color: #ACA69B;
```

## Component Patterns

### Primary Button

```css
display: inline-flex;
align-items: center;
gap: 0.5rem;
padding: 0.875rem 2rem;
background: #C4A35A;
color: #000;
font-family: "Inter", sans-serif;
font-size: 0.875rem;
font-weight: 600;
border: 0;
border-radius: 9999px;
transition: transform 300ms ease-out, filter 300ms ease-out;
```

Hover: translate up by 1-2px and brighten slightly.

### Ghost Button

```css
background: rgba(255, 255, 255, 0.04);
border: 1px solid rgba(255, 255, 255, 0.07);
border-radius: 9999px;
backdrop-filter: blur(24px) saturate(140%);
color: #E8E6E1;
font-family: "JetBrains Mono", monospace;
font-size: 11px;
letter-spacing: 0.2em;
text-transform: uppercase;
```

Hover: text to white, border to `rgba(196, 163, 90, 0.24)`.

### Card

Dense dashboard card:

```css
background: rgba(12, 12, 12, 0.90);
border: 1px solid rgba(255, 255, 255, 0.07);
border-radius: 8px;
```

Accent card:

```css
border-top: 3px solid rgba(196, 163, 90, 0.60);
```

Feature or marketing card:

```css
border-radius: 1.75rem;
box-shadow: 0 24px 80px rgba(0, 0, 0, 0.32);
backdrop-filter: blur(24px) saturate(140%);
```

Glass is for chrome and showcase surfaces. Dense tables, lists, and operational data stay flatter.

### Inputs

Prefer underline inputs for polished Engine AI forms:

```css
background: transparent;
border: 0;
border-bottom: 1px solid rgba(255, 255, 255, 0.12);
border-radius: 0;
padding: 0.625rem 0;
color: #FFFFFF;
font-family: "Inter", sans-serif;
font-size: 15px;
```

Focus: bottom border to `#C4A35A`.

## Layout

- Max content width: `1100px` to `1200px` for dashboards and artifacts.
- Marketing page container: `max-w-6xl`, centred, `px-6`.
- Dashboard padding: `24px` to `32px`.
- Marketing section padding: `py-24` mobile, `py-32` to `py-44` desktop.
- Dense dashboard gaps: `10px` to `12px`.
- Marketing grid gaps: `gap-6` to `gap-12`.
- Footer on artifacts: mono, centred, subtle grey, document name and date.

## Charts

- Gold for the primary or highlighted series only.
- Greys for secondary series and baselines.
- Red only for warning, negative, or conservative scenarios.
- Do not introduce rainbow palettes.
- Put labels and small chart metadata in JetBrains Mono.
- Use short, specific chart titles in Inter.

## Motion

- No load animations in dashboards or data interfaces.
- Marketing pages may use scroll reveal: opacity `0` to `1`, translateY `24px` to `0`, 800ms ease-out, stagger 100-150ms.
- Cards may lift slightly on hover and brighten border to gold at low opacity.
- Buttons may lift 1-2px and brighten.
- No spring, bounce, playful loops, or decorative motion.

## Document Variant

For `.docx`, PDFs, print, and client leave-behinds:

- Use light Paper or Pure backgrounds, not a full dark page unless explicitly requested.
- Use Inter for headings and body.
- Use JetBrains Mono for labels, metadata, captions, and small tags.
- Use `#8A6C2A` for gold text on light backgrounds.
- Keep gold to headings, rules, section markers, and one or two emphasis points.
- Avoid dark-on-dark screenshots or panels that lose contrast in print.
- Keep margins generous and hierarchy calm.

## Voice

- Direct, grounded, and low-pressure.
- NZ English: organisation, programme, colour, optimise, realise.
- No jargon or corporate padding.
- No emoji or exclamation marks.
- Prefer short sentences and specific outcomes.
- Use "we" for Engine AI and "you" or "your team" for the reader.
