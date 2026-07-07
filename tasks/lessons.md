## 2026-07-07 — brand skill packaging
**What happened:** The uploaded brand skill referenced `references/design-tokens.md`, but the packaged skill did not include that file, and the frontmatter description exceeded the validator limit.
**Better approach:** When updating skills, run `quick_validate.py` and include any referenced `references/` files in the same skill folder before treating the package as ready.
