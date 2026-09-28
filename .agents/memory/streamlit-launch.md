---
name: Streamlit launch prompt
description: Streamlit may pause for its first-run usage-statistics prompt in managed workflows.
---

Set `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false` in the workflow command when running Streamlit non-interactively.

**Why:** In this environment, the first-run prompt can block the process before it opens the configured web port.

**How to apply:** Include the variable alongside `streamlit run` for any future Streamlit workflow.