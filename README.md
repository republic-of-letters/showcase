# showcase

The public face of the **Republic of Letters** — a research collaboration space
where faculty, students, and their AI agents do empirical work together under
[one protocol](https://github.com/republic-of-letters/protocol).

Live site: **<https://republic-of-letters.github.io/showcase/>**

## How this repo works

- [`projects.yaml`](projects.yaml) is the registry: one card per project. The site
  is rebuilt from it on every push to `main` (see `.github/workflows/pages.yml`).
- **A card is a publication.** Research projects live in their own private repos;
  what appears here is only what each project approved for public display. Cards
  are added and changed **by pull request**, reviewed by the project's lead — the
  same merge-gate logic the protocol uses everywhere else.
- Issues on this repo are the front door: propose a project or apply to join one
  via the [issue forms](../../issues/new/choose).

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
