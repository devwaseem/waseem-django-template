# Optional release provenance

No provenance workflow runs in normal CI, `just verify`, or local development.
Adopt this layer only when a project has a release process and a registry or
enterprise audit requirement.

## 1. Attach an SBOM to a GitHub Release

Create the GitHub Release first, then call the reusable workflow from a
project-owned release workflow. It produces an SPDX SBOM from the tagged source
and uploads it as a release asset.

```yaml
name: Release provenance

on:
  workflow_dispatch:
    inputs:
      release_tag:
        description: Existing GitHub Release tag
        required: true
        type: string

permissions:
  contents: write

jobs:
  source-sbom:
    uses: ./.github/workflows/release-provenance.yml
    with:
      release_tag: ${{ '{{' }} inputs.release_tag {{ '}}' }}
```

The generated `release-provenance.yml` deliberately has no push, pull-request,
or scheduled trigger. Removing the caller removes the feature with no effect on
development or CI.

## 2. Add container provenance when images become a release artifact

If and when releases publish a container, call the existing
`publish-image.yml` after selecting a registry and immutable image tag. It
pushes the hardened image, generates an SPDX image SBOM, and attaches GitHub
build and SBOM attestations to the image digest.

```yaml
jobs:
  publish-image:
    uses: ./.github/workflows/publish-image.yml
    with:
      registry: ghcr.io
      image_name: ghcr.io/example-org/example-service
      image_tag: ${{ '{{' }} inputs.release_tag {{ '}}' }}
    secrets: inherit
```

## 3. Future signing decision

Keep signing separate from source and image attestation. When a registry,
identity provider, and verification policy are selected, add a dedicated
reusable workflow that signs the immutable image digest with keyless OIDC and
publishes verification instructions. Do not introduce keys, signing tools, or
mandatory local steps until that decision is made.
