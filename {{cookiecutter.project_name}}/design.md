# UI Design Decisions & System Tokens

## Core Aesthetic: Shadcn/UI (Zinc)

This project follows a clean, modern aesthetic inspired by [Shadcn/UI](https://ui.shadcn.com/). It uses a minimal grayscale palette (Zinc) with high-contrast primary elements and precise, consistent geometry.

## UI Tokens (Tailwind v4 `@theme`)

The following semantic tokens are defined in `frontend/shared/css/main.css` using Oklch values for optimal color precision and accessibility.

### Colors (Light Mode)

- **Base Colors**:
    - `base-100`: `oklch(1 0 0)` (Pure White) — Primary background.
    - `base-200`: `oklch(0.97 0 0)` (Zinc-100) — Secondary background.
    - `base-300`: `oklch(0.922 0 0)` (Zinc-200) — Borders/Inputs.
    - `base-content`: `oklch(0.145 0 0)` (Zinc-950) — Default text color.

- **Brand Colors**:
    - `primary`: `oklch(0.62 0.21 45)` (Vibrant Orange) — Main actions.
    - `primary-content`: `oklch(0.985 0 0)` (Zinc-50) — Text on primary. Passes AA for large/UI text.
    - `secondary`: `oklch(0.97 0 0)` (Zinc-100).
    - `secondary-content`: `oklch(0.205 0 0)`.
    - `accent`: `oklch(0.97 0 0)`.
    - `accent-content`: `oklch(0.205 0 0)`.
    - `neutral`: `oklch(0.205 0 0)`.
    - `neutral-content`: `oklch(0.985 0 0)`.

- **Semantic States**:
    - `success`, `warning`, `info`, `destructive` with corresponding `-content` tokens.

- **Utility**:
    - `muted`: `oklch(0.97 0 0)`.
    - `muted-content`: `oklch(0.556 0 0)` (Zinc-500) — Secondary text.
    - `ring`: `oklch(0.62 0.21 45)` (Orange) — Focus states.

### Geometry

- **Radius**: `0.5rem` (standard `md` rounding). All interactive elements (Buttons, Inputs) and containers (Cards) must use this consistent rounding.

## Component Standards

### Icons (Lucide)

- Use Lucide icons in templates/components with: `<i data-lucide="iconname"></i>`.
- Do not rely on auto-importing the full icon set in page scripts.
- Import every icon explicitly in `@frontend/shared/js/icons.ts` and register it in `createIcons({ icons: { ... } })`.
- Keep `@frontend/shared/js/icons.ts` as the single source of truth for available Lucide icons.

### Buttons (`.btn`)

- **Height**: `2.5rem` (10 units).
- **Variants**: `.btn-primary`, `.btn-secondary`, `.btn-outline`, `.btn-ghost`, `.btn-link`.
- **States**: Subtle hover effects (`bg-primary/90`), focus-visible rings with offsets.

### Inputs (`.input`)

- **Styling**: Standard `h-10` with `border-base-300`.
- **Focus**: Uses `ring-2 ring-ring` with a white offset to maintain separation.

### Cards (`.card`)

- **Structure**: Header (Title/Description), Content, and Footer sections.
- **Shadow**: `shadow-sm` for a lift that doesn't feel heavy.
- **Background**: Uses `bg-base-100` and `border-base-300`.
