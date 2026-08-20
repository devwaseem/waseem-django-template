# Template Maintainer Guide

This repository is a Cruft-first Cookiecutter foundation for Django projects.
It may generate API, SSR (HyperDjango), or hybrid projects, each with Celery
enabled or disabled. These instructions apply to humans and AI agents making
changes to the template itself.

## Scope and boundaries

- Keep the template generic. It may preserve reusable engineering patterns from
  SmoothPay, but must never contain SmoothPay terminology, product behavior,
  data, workflows, branding, or integrations.
- The root template owns generator behavior, framework/runtime platform code,
  shared UI primitives, extension points, and documentation. Generated
  projects own `identity/`, `domains/`, product routes, view
  models, settings composition, and product ADRs.
- The platform is provider-neutral: it must not own a user model, Allauth,
  JWT endpoints, authentication routes, or product authorization policy. The
  default local identity implementation belongs in the generated project's
  top-level `identity/` package.
- Change reusable platform behavior in this template repository, then release it
  through Cruft. Do not treat a generated project's inherited `platform/` as
  the normal place to make template improvements.
- Keep the generated-project `AGENTS.md` focused on application development;
  do not copy template-maintenance rules into it.

## Generation contract

- Preserve all six supported shapes: `api`, `ssr`, and `hybrid`, each with
  Celery `yes` and `no`.
- When adding conditional files or dependencies, make every affected shape
  render and work. Keep `pre_gen_project.py`, `post_gen_project.py`, tests,
  documentation, and the selected lockfile behavior aligned.
- Use Cookiecutter-compatible Jinja only. A generated project must not retain
  template internals such as `.template_locks`.
- Preserve the Cruft extension boundary: updates may change template-owned
  files without overwriting product-owned domain extensions, identity code,
  project settings composition, or product routes. Configure those paths in
  the generated project's Cruft skip list.
- Generate local identity by default. It is a complete, project-owned starting
  point rather than a permanent product decision: a project may remove or
  replace it before its first migration, or later through a deliberate data
  migration and ADR.
- Keep production security enforcement after project settings composition.
  Projects may choose their applications and settings, but must not weaken
  essential production safeguards through an ordinary settings override.

## Dependencies and lockfiles

- Every generated project receives one committed `uv.lock` matching its chosen
  shape and project slug. The six parameterized files under `.template_locks/`
  are template internals.
- Do not change dependencies or lockfiles incidentally, and never edit a
  lockfile manually.
- For an intentional dependency update, run `just refresh-template-locks`.
  It regenerates all six locks and validates the template contracts.

## Quality and handoff

- Run `just quality` before handing off template changes. It checks formatting,
  linting, rendering, generated management commands, and Cruft-update safety.
- Keep root tests focused on generator contracts. Test generated-project
  behavior in the rendered project, not by duplicating its tests here.
- Do not weaken generated-project security defaults, configuration contracts,
  or the 100% coverage requirement merely to make a template change pass.
- Exercise the product-owned settings and identity seams in rendered-project
  tests. In particular, confirm that a project can remove local identity before
  its first migration without editing template-owned platform files.

## Updates

- Before modifying a generated project that uses this template, use `cruft
  check`, commit or stash product work, then review `cruft update` conflicts
  deliberately.
- Record template-wide architectural decisions in the root documentation;
  record product decisions in the generated project's `docs/adr/` directory.
