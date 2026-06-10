---
name: brand
description: >
  Engine AI visual identity and brand system. Use this skill whenever building
  UI, pages, components, proposals, or any visual output for Engine AI. Covers
  colours, typography, spacing, component patterns, animation, tone of voice,
  and asset references. Source of truth extracted from the live website at
  engineai.co.nz.
---

# Engine AI Brand System

You are applying the Engine AI brand. This is a dark, premium, gold-accented identity
built for a New Zealand AI consultancy. Every UI decision should feel precise,
confident, and minimal. No corporate fluff. No generic SaaS aesthetic.

> **Canonical design system (read first):** `~/projects/engineai/design-system/`
> `DESIGN.md` is the authoritative handoff; `colors_and_type.css` holds all 120
> tokens + component classes with exact values. For any real build, read those
> first — they supersede the summary below on conflict (light theme + surfaces,
> `gold-ink` for gold-on-light, product sub-page accents, type/motion floors).
> This SKILL.md remains the quick reference and tone-of-voice guide.

Reference site: engineai.co.nz
Source repo: `~/projects/engineai_website_copy/`

---

## Colour Palette

### Core

| Token | Hex | Usage |
|---|---|---|
| `background` | `#0A0A0A` | Page background, scrollbar track |
| `surface` | `#111111` | Elevated surfaces |
| `card-bg` | `rgba(12, 12, 12, 0.84)` | Card backgrounds (semi-transparent) |
| `gold` | `#C4A35A` | Primary accent, CTAs, highlights, section borders |
| `text-primary` | `#E8E6E1` | Body text (warm off-white) |
| `text-highlight` | `#F2EFE8` | Emphasis text |
| `text-secondary` | `#888888` | Labels, mono captions |
| `text-muted` | `#555555` | Minimal prominence |
| `white` | `#ffffff` | Headlines, hover states |

### Borders

| Token | Value |
|---|---|
| `border-default` | `rgba(255, 255, 255, 0.07)` |
| `border-subtle` | `rgba(255, 255, 255, 0.04)` |
| `border-gold` | `rgba(196, 163, 90, 0.24)` |

### Product Accents (sub-pages only)

| Product | Accent |
|---|---|
| OpenClaw | Teal `#2B8C8C` |
| Copilot | Blue `#0078D4` |
| Bespoke Builds | Green `#4CAF50` |

### Selection & Scrollbar

- Text selection: `rgba(196, 163, 90, 0.25)`
- Scrollbar thumb: `#2A2A2A` (hover `#444`), width 5px

---

## Typography

### Font Stack

| Role | Family | Variable |
|---|---|---|
| Body / Headlines | Inter | `--font-sans` |
| Labels / Mono | JetBrains Mono | `--font-mono` |

Both loaded from Google Fonts with `display: swap`.

### Scale

| Element | Size | Weight | Tracking | Leading |
|---|---|---|---|---|
| Hero headline | `clamp(2rem, 4.6vw, 4.15rem)` | Light / Semibold (gold line) | `-0.05em` | `0.96` |
| Section title | `text-4xl` / `md:text-6xl` | Light | `-0.04em` | `1.15` |
| Card title | `text-2xl` | Medium | default | default |
| Body | `text-base` to `text-lg` | Regular | default | `1.8` |
| Mono label | `text-[11px]` uppercase | Regular | `0.34em` | default |
| Stat number | `text-6xl` to `text-7xl` | Light | default | tight |

### Rules

- Headlines use **light weight** for premium feel. Gold accent on the emphasis line uses semibold.
- Mono labels (`JetBrains Mono`) are always uppercase with wide tracking.
- Body text uses generous `leading-7` / `leading-8` for readability.
- Never use bold for headlines. Light + large is the pattern.

---

## Spacing & Layout

### Container

- Max width: `max-w-6xl` (consistent across all sections)
- Horizontal padding: `px-6`
- Content columns: `max-w-4xl`, `max-w-3xl`, `max-w-2xl` for narrower reads

### Section Padding

- Mobile: `py-24` (6rem)
- Desktop: `py-32` (8rem)
- Hero: `pt-24 md:pt-28 pb-10`

### Grid Patterns

| Layout | Pattern |
|---|---|
| 2-col asymmetric | `grid gap-10 lg:grid-cols-[0.95fr_1.05fr]` |
| 2-col even | `md:grid-cols-2` |
| 3-col | `lg:grid-cols-3` |
| 4-col | `xl:grid-cols-4` |

Gap values: `gap-3`, `gap-5`, `gap-6`, `gap-10`, `gap-12`

### Border Radius

| Element | Radius |
|---|---|
| Buttons | `rounded-full` (pill) |
| Cards | `rounded-[1.75rem]` to `rounded-[1.9rem]` |
| Form inputs | `rounded-[1.1rem]` |
| Images | `rounded-xl` or `rounded-lg` |

---

## Component Patterns

### Navigation

- Fixed top, `z-50`
- Height: `h-20` mobile, `h-24` desktop
- Scroll state: `bg-[#0A0A0A]/78 backdrop-blur-2xl border-b border-white/[0.07]`
- Nav items: `rounded-full px-4 py-2`, active `bg-white/[0.08]`
- Mobile: hamburger with slide-down panel

### Cards

**Standard card:**
```
rounded-[1.75rem] border border-white/[0.07] bg-[rgba(12,12,12,0.84)] p-6
shadow-[0_24px_80px_rgba(0,0,0,0.32)]
hover:-translate-y-1 hover:border-gold/20 duration-500
```

**Liquid glass effect (premium):**
```
border: 1px solid rgba(255, 255, 255, 0.12)
backdrop-filter: blur(24px) saturate(140%)
```
Multiple shadow layers for inner glow. Gold variant adds `rgba(196, 163, 90, 0.24)` border.

**Service card:**
- Top accent bar: `h-[3px] bg-gold`
- Number: `font-mono text-[11px] uppercase`
- Divider: `h-px bg-gradient-to-r from-gold/35 via-white/[0.08] to-transparent`

### Buttons

**Primary CTA:**
```
rounded-full border border-gold/30 bg-gold px-6 py-3
text-sm font-semibold tracking-[0.08em] text-black
hover:-translate-y-0.5 hover:brightness-110 duration-300
```

**Secondary/Ghost:**
```
liquid-glass rounded-full px-6 py-3
font-mono text-[11px] uppercase tracking-[0.2em]
hover:border-gold/25 hover:text-white
```

### Form Inputs

```
rounded-[1.1rem] border border-white/[0.08] bg-white/[0.02] px-4 py-3.5
text-[15px] text-white placeholder:text-text-secondary
focus:border-gold/40 focus:ring-1 focus:ring-gold/20 outline-none
```

Labels: `font-mono text-[11px] uppercase tracking-[0.24em] text-text-secondary`

---

## Animation & Motion

### Scroll Animations

- **Trigger:** Intersection Observer at `threshold: 0.08`, `rootMargin: 0px 0px -40px 0px`
- **Effect:** Fade + slide up from `opacity-0 translate-y-6` to `opacity-100 translate-y-0`
- **Duration:** `800ms ease-out`
- **Stagger:** 100ms to 340ms increments between siblings

### Keyframes

| Name | Effect | Duration |
|---|---|---|
| `heroFadeUp` | Fade in + slide up 24px | 0.9s ease-out |
| `heroFadeIn` | Pure fade | 0.8s ease-out |
| `float` | Vertical bounce +/-6px | 4s ease-in-out infinite |

Hero delay classes: `.hero-delay-1` (0.1s) through `.hero-delay-4` (0.7s)

### CountUp Numbers

- Trigger: Intersection Observer at `threshold: 0.25`
- Duration: ~900ms with cubic ease-out: `1 - Math.pow(1 - progress, 3)`

### Hover

- Cards: `hover:-translate-y-1 duration-500`
- Borders: brighten to `gold/20` or `gold/25`
- Text: `hover:text-white`
- Buttons: `hover:-translate-y-0.5 hover:brightness-110`

---

## Background & Atmosphere

### Page Background

```css
background: linear-gradient(145deg, #080808 0%, #0f0f0f 48%, #0a0a0a 100%);
```

### Ambient Grid

- White grid lines at `rgba(255,255,255,0.04)`, 96px spacing
- Masked with radial gradient (visible center, fades at edges)
- Opacity: `0.4`

### Noise Texture

- Multiple layered radial gradients at 18/24/20px
- `mix-blend-mode: soft-light`, opacity `0.2`

### Blur Blobs (decorative)

- Gold blob: `bg-gold/[0.10] blur-[140px]` (top-left)
- White blob: `bg-white/[0.04] blur-[160px]` (top-right)
- Gold blob: `bg-gold/[0.08] blur-[180px]` (bottom-center)

### Image Overlays

Sections with background images use layered gradients:
```
radial-gradient(circle at center, rgba(196,163,90,0.06) 0%, transparent 24%),
linear-gradient(180deg, rgba(10,10,10,0.78) 0%, ...)
```

### Team Photos

Always rendered with `grayscale` CSS filter.

---

## Tone of Voice

### Principles

- **Direct.** No jargon. No buzzwords. No "leverage", "synergy", or "digital transformation".
- **Grounded.** Practical, outcome-focused language.
- **Calm authority.** Confident but not pushy.
- **Honest.** "No pitch. No obligation."
- **Operator language.** "Two operators. Not two consultants."

### Patterns

- Lead with the problem, then the outcome
- Use contrast to create tension (tools vs. outcomes, potential vs. reality)
- Short sentences. Break long paragraphs into punchy lines.
- CTAs are clear and low-pressure: "Book a Discovery Call", "See how we work"
- NZ English throughout (organisation, programme, colour, optimise)

### Copy Samples

> "The biggest technology shift in a generation is happening right now. Most businesses are watching it happen to them."

> "There is a massive gap between what AI can do and what businesses are actually doing with it."

> "We are not a consultancy that discovered AI. We are AI practitioners."

> "Start with a conversation. No pitch. No obligation."

---

## Assets Reference

### Logo

SVG component at `/app/components/Logo.tsx`. Three horizontal bars with descending opacity.
Default colour: `#d7d5d1`. Accepts `color` and `size` props.

### Key Images (in `/public/images/`)

| File | Purpose |
|---|---|
| `hero.webp` | Hero section |
| `how-we-work.webp` | Process section |
| `the-problem.webp` | Problem statement |
| `the-gap-background.png` | Gap section parallax |
| `claude-icon-v2.webp` | Claude product card |
| `copilot-icon.webp` | Copilot product card |
| `openclaw-icon.webp` | OpenClaw product card |
| `joe-ward.webp` | Team (grayscale) |
| `ben-du-chateau.webp` | Team (grayscale) |

### Video

- Hero background: `/videos/engine-ai-hero.webm` (1.2MB, autoplay loop muted)
- Fallback: `/videos/engine-ai-hero.mp4`

---

## Responsive Breakpoints

| Breakpoint | Width | Key Changes |
|---|---|---|
| base | 0px | Single column, `px-6`, mobile nav |
| `md` | 768px | 2-col layouts, larger type |
| `lg` | 1024px | 3-4 col layouts, desktop nav |
| `xl` | 1280px | Extended layouts |

Typography scales with `clamp()` for fluid sizing. Mobile-first throughout.

---

## Checklist: Applying the Brand

When building Engine AI UI:

1. Background is always `#0A0A0A` or the 145-degree gradient
2. Gold `#C4A35A` for CTAs, accents, emphasis only. Never overuse.
3. Inter for body, JetBrains Mono for labels/tags (uppercase, wide tracking)
4. Headlines: light weight, tight leading, negative tracking
5. Cards: large radius (1.75rem+), subtle borders, glass effects
6. Buttons: pill-shaped. Primary = gold bg + black text. Secondary = glass + mono text.
7. Animations: subtle. Fade-up on scroll, slight lift on hover. No bouncy/playful motion.
8. Copy: direct, outcome-focused, NZ English. No corporate padding.
9. Team photos in grayscale
10. Ambient atmosphere: grid, noise, blur blobs in background
