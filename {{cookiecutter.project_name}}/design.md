# UI Design Decisions & System Tokens

## Core Aesthetic: Carbon-Inspired Default

This template defaults to a Carbon-inspired visual system focused on clarity,
efficiency, and high-contrast structure.

## UI Tokens (Tailwind v4 `@theme`)

The semantic tokens live in `frontend/shared/css/main.css`.

### Typography

- Primary font: `IBM Plex Sans`, sans-serif.
- Weights: 400, 500, 600.

### Colors (Gray 10 style)

- Base:
    - `base-100`: `oklch(1 0 0)`
    - `base-200`: `oklch(0.97 0 0)`
    - `base-300`: `oklch(0.91 0 0)`
    - `base-content`: `oklch(0.18 0 0)`
- Brand:
    - `primary`: `oklch(0.51 0.18 260)`
    - `secondary`: `oklch(0.32 0 0)`
- States:
    - `success`, `warning`, `info`, `destructive` with paired `-content` tokens.

### Geometry

- Radius token defaults to `0px` for square corners.

## Component Standards

### Icons

- Use Lucide icons in templates/components with: `<i data-lucide="iconname"></i>`.
- Register icons in `frontend/shared/js/icons.ts`.

### Buttons

- Default height: `48px` (`.btn`), small `32px` (`.btn-sm`).
- Variants: `primary`, `secondary`, `outline`, `ghost`, `danger`, `link`.

### Inputs

- Square borders with strong bottom-border focus treatment.

### Cards

- Flat, bordered, and square by default.
