# Visual language

The default interface is a calm systems desk: precise, professional, and
quietly confident. It is deliberately an internal-tool starting point, not a
product brand.

- Use editorial hierarchy, warm-tinted neutral surfaces, and one restrained
  accent. Prefer flat structural surfaces over gradients, glass effects, neon,
  or consumer-app ornament.
- Use the semantic Tailwind v4 tokens in `hyper/shared/css/main.css`; extend
  tokens and shared primitives before adding page-local CSS.
- Support light and dark color schemes, visible keyboard focus, WCAG 2.2 AA
  contrast, and `prefers-reduced-motion`.
- Keep interactions progressive: SSR first, Alpine only for narrow local
  behavior, and event listeners in `entry.ts` rather than inline handlers.
- Rebrand through tokens, logo/identity assets, and navigation labels—not by
  forking component markup.
