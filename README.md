# showcase

The public face of the **Republic of Letters** — a research collaboration space
where faculty, students, and their AI agents do empirical work together under
[one protocol](https://github.com/republic-of-letters/protocol).

Live site: **<https://republic-of-letters.github.io/showcase/>**

## How this repo works

- [`projects.yaml`](projects.yaml) is the project registry: one card per project.
  [`notices.yaml`](notices.yaml) is the **notice board**: OFFERING/SEEKING
  silhouettes for match-making (coarse fields only — by design there is no room to
  over-disclose; every notice has a required expiry and drops off automatically).
  The site is rebuilt from both on every push to `main`
  (see `.github/workflows/pages.yml`).
- **A card or notice is a publication.** Research projects live in their own
  private repos; what appears here is only what each project or member approved
  for public display. Entries are added and changed **by pull request** — the
  same merge-gate logic the protocol uses everywhere else.
- Issues on this repo are the front door: propose a project, apply to join one,
  or post a notice via the [issue forms](../../issues/new/choose).
- The site is bilingual (`/` en, `/zh/` 中文) and includes an annotated worked
  round at `/letter/` — the "read one letter" tour. Cards and notices support
  optional `*_zh` fields.

## Project visibility tiers

| Tier | What's public | How to participate |
| ---- | ------------- | ------------------ |
| `display-only`  | title, blurb, published outputs | not open |
| `apply-to-join` | the above + a contact | open an issue with the join form |
| `open`          | the project repo itself | open a topic or round directly |

## Editing the site

`scripts/build-site.py` turns `projects.yaml` into `_site/index.html`. Run it
locally (`python scripts/build-site.py`, needs `pyyaml`) and open
`_site/index.html` to preview.
