---
name: Streamlit publishing in artifact workspaces
description: Published monorepos serve declared artifacts, not a root-level Streamlit app.
---

In a pnpm workspace with artifact manifests, publishing only serves services declared under `artifacts/**/.replit-artifact/artifact.toml`; a root `app.py` alone produces a deployment with no previewable artifacts.

**Why:** The publisher switches to artifact mode when manifests are present and ignores the legacy root workflow for production serving.

**How to apply:** Put the Streamlit command, port, health path, and production dependency setup in a dedicated web artifact manifest, then republish after changing it.