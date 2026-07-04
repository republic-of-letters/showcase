# showcase

The public face of the **Republic of Letters** — a research collaboration space
where faculty, students, and their AI agents do empirical work together under
[one protocol](https://github.com/republic-of-letters/protocol).

Live site: **<https://republic-of-letters.github.io/showcase/>**

## The project registry

[`projects.yaml`](projects.yaml) is the registry — one card per project, and the lead
of the site. **A card is a publication:** research projects live in their own private
repos, and what appears here is only what each project approved for public display.
Cards are added and changed **by pull request** — the same merge-gate logic the
protocol uses everywhere else. The site is rebuilt on every push to `main`
(see `.github/workflows/pages.yml`), is bilingual (`/` en, `/zh/` 中文; cards support
optional `*_zh` fields), and includes an annotated worked round at `/letter/` — the
"read one letter" tour.

## How to join

Most collaborations start from a running project, not from the board.

1. **Mentored onboarding into an existing project.** Apply through the
   [issue forms](../../issues/new/choose), or be invited by a member. A **Mentor**
   named in the project's `PROJECT.md` joins the merge gate for your first rounds — you
   learn the loop with someone accountable beside you.
2. **The sandbox — try the loop today.** Run one full round on a public dataset at
   [`republic-of-letters/sandbox`](https://github.com/republic-of-letters/sandbox):
   ask → code → safety scan → run → result → merge, about thirty minutes, a CI robot
   standing in for the Runner.
3. **The notice board — a secondary discovery channel.** [`notices.yaml`](notices.yaml)
   posts OFFERING/SEEKING silhouettes for match-making (coarse fields only — by design
   there is no room to over-disclose; every notice has a required expiry and drops off
   automatically). A notice is a publication too, added by pull request. Use it to find
   a counterpart when no running project fits yet.

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
