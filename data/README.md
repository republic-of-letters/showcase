# data/ — the live feed for letters.jupyter.pro

These JSON files are the **single source** the site at
[letters.jupyter.pro](https://letters.jupyter.pro) reads at request time (cached ~5 min).
Edit them here by pull request; the site updates without a redeploy.

- `board.json` — notice-board entries (offering / seeking silhouettes).
- `projects.json` — public project cards.

Both are **publications**: everything here is on the public internet, and every change
goes through a PR (the merge gate). Keep board entries to **silhouettes** — coarse
fields only, nothing that could be copied. See the schema in
[`../notices.yaml`](../notices.yaml) (the human-authored mirror) and
[`../projects.yaml`](../projects.yaml).

Field reference: `board.json` items — `id, kind(offering|seeking), what(data|licence|
compute|methods|ideas), area, shape, scale, period, terms(can-run|can-share|
licence-bound), seeking, contact(@handle|watch), posted, expires` (+ optional `*_zh`).
Expired notices (past `expires`, YYYY-MM) are dropped by the site automatically.
