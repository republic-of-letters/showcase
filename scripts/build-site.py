#!/usr/bin/env python3
"""Build the showcase site: projects.yaml -> _site/index.html.

No framework — one self-contained HTML file, styled inline, light/dark aware.
Run locally to preview:  python scripts/build-site.py && open _site/index.html
"""

import html
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

STATUS_LABELS = {
    "incubating": ("incubating", "#b45309"),
    "active": ("active", "#15803d"),
    "writing": ("writing", "#1d4ed8"),
    "published": ("published", "#7e22ce"),
    "archived": ("archived", "#6b7280"),
}
TIER_LABELS = {
    "display-only": "display only",
    "apply-to-join": "open to applications",
    "open": "open",
}


def esc(v):
    return html.escape(str(v), quote=True)


def card(p):
    status = p.get("status", "incubating")
    label, color = STATUS_LABELS.get(status, (status, "#6b7280"))
    tier = TIER_LABELS.get(p.get("tier", "display-only"), esc(p.get("tier", "")))

    pills = (
        f'<span class="pill" style="--pc:{color}">{esc(label)}</span>'
        f'<span class="pill tier">{esc(tier)}</span>'
    )
    meta = []
    if p.get("since"):
        meta.append(f"since {esc(p['since'])}")
    if p.get("people"):
        meta.append(f"{esc(p['people'])} members")
    if p.get("contact") and p.get("tier") == "apply-to-join":
        meta.append(f"contact {esc(p['contact'])}")
    meta_html = f'<p class="meta">{" · ".join(meta)}</p>' if meta else ""

    outputs = ""
    if p.get("outputs"):
        links = " · ".join(
            f'<a href="{esc(o["url"])}">{esc(o["label"])}</a>' for o in p["outputs"]
        )
        outputs = f'<p class="outputs">{links}</p>'

    title = esc(p.get("title", p.get("id", "untitled")))
    if p.get("tier") == "open" and p.get("repo"):
        title = f'<a href="{esc(p["repo"])}">{title}</a>'

    return f"""      <article class="card">
        <div class="pills">{pills}</div>
        <h3>{title}</h3>
        <p>{esc(p.get("blurb", ""))}</p>
        {meta_html}{outputs}
      </article>"""


EMPTY_STATE = """      <p class="empty">The first projects are being onboarded — check back soon,
      or <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">propose one</a>.</p>"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Republic of Letters</title>
<meta name="description" content="A research collaboration space where humans and their AI agents do empirical work by correspondence — under one protocol, behind three human gates.">
<style>
  :root {
    --bg: #faf7f1; --ink: #2b2620; --muted: #6f675c; --line: #e4ddd0;
    --card: #ffffff; --accent: #9f1239; --link: #1d4ed8;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #171419; --ink: #e8e2d9; --muted: #a39a8d; --line: #322d38;
      --card: #201c25; --accent: #fb7185; --link: #93b4f8;
    }
  }
  * { box-sizing: border-box; margin: 0; }
  body {
    background: var(--bg); color: var(--ink);
    font: 17px/1.65 Georgia, 'Times New Roman', serif;
    padding: 0 1.25rem;
  }
  main { max-width: 880px; margin: 0 auto; }
  a { color: var(--link); text-decoration-thickness: 1px; text-underline-offset: 3px; }
  header { padding: 4.5rem 0 2.5rem; border-bottom: 1px solid var(--line); }
  .seal { color: var(--accent); font-size: 0.85rem; letter-spacing: 0.22em;
          text-transform: uppercase; font-family: ui-sans-serif, system-ui, sans-serif; }
  h1 { font-size: 2.6rem; font-weight: 500; line-height: 1.15; margin: 0.5rem 0 1rem; }
  header p.lead { font-size: 1.15rem; max-width: 620px; color: var(--muted); }
  section { padding: 2.75rem 0; border-bottom: 1px solid var(--line); }
  section:last-of-type { border-bottom: none; }
  h2 { font-size: 1.5rem; font-weight: 500; margin-bottom: 1.2rem; }
  h3 { font-size: 1.15rem; font-weight: 600; margin: 0.4rem 0; }
  .cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 1.5rem; }
  .cols h3 { font-size: 1rem; }
  .cols .n { color: var(--accent); font-family: ui-sans-serif, system-ui, sans-serif;
             font-size: 0.8rem; letter-spacing: 0.12em; }
  .cols p { font-size: 0.95rem; color: var(--muted); }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 1.25rem; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 10px;
          padding: 1.25rem 1.35rem; }
  .card p { font-size: 0.95rem; }
  .pills { margin-bottom: 0.35rem; }
  .pill { display: inline-block; font: 600 0.7rem/1 ui-sans-serif, system-ui, sans-serif;
          letter-spacing: 0.06em; text-transform: uppercase; color: var(--pc, var(--muted));
          border: 1px solid currentColor; border-radius: 999px;
          padding: 0.25rem 0.6rem; margin-right: 0.4rem; }
  .pill.tier { color: var(--muted); }
  .meta, .outputs { margin-top: 0.6rem; font-size: 0.85rem !important; color: var(--muted); }
  .empty { color: var(--muted); font-style: italic; }
  table { border-collapse: collapse; width: 100%; font-size: 0.95rem; }
  th, td { text-align: left; padding: 0.55rem 0.9rem 0.55rem 0; border-bottom: 1px solid var(--line);
           vertical-align: top; }
  th { font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.75rem;
       letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
  .scroll { overflow-x: auto; }
  footer { padding: 2.5rem 0 3.5rem; color: var(--muted); font-size: 0.9rem; }
  code { font-family: ui-monospace, 'SF Mono', Menlo, monospace; font-size: 0.85em;
         background: var(--card); border: 1px solid var(--line); border-radius: 4px;
         padding: 0.1em 0.35em; }
</style>
</head>
<body>
<main>
  <header>
    <div class="seal">Respublica Literaria · est. 2026</div>
    <h1>Republic of Letters</h1>
    <p class="lead">A research collaboration space where faculty, students, and their
    AI agents do empirical work by correspondence — questions and code travel out,
    results travel back, and every step is a reviewable letter in the record.</p>
  </header>

  <section>
    <h2>How it works</h2>
    <div class="cols">
      <div><span class="n">I — TOPICS</span>
        <h3>One candidate paper, one topic</h3>
        <p>Hypotheses, the falsifier, authorship, and a decision log live in one
        file. Killing a topic is a first-class outcome with a post-mortem — the
        archive keeps everything tried, and why it stopped.</p></div>
      <div><span class="n">II — ROUNDS</span>
        <h3>One question, one pull request</h3>
        <p>A proposer writes the question and runnable code; the data side
        safety-reviews it, runs it on the real data, and returns aggregates —
        figures, tables, a written result — into the same thread.</p></div>
      <div><span class="n">III — GATES</span>
        <h3>Three doors only humans open</h3>
        <p>Topic GO/kill and authorship; any code touching real data; and the merge
        into the permanent record. Agents draft, code, and analyse — people decide.
        Anyone can halt any round with one label.</p></div>
    </div>
  </section>

  <section>
    <h2>Projects</h2>
    <div class="grid">
{{CARDS}}
    </div>
  </section>

  <section>
    <h2>What you can trust</h2>
    <p>Data never enters a repository — projects exchange questions and
    aggregate results, with CI tripwires that make the boundary hard to cross by
    accident. Every published artifact carries its provenance:</p>
    <div class="scroll"><table>
      <tr><th>Level</th><th>Meaning</th></tr>
      <tr><td><code>ran-on-real-data</code></td><td>Produced by the data side on the
        real dataset, through the safety gate, merged by humans on both sides.</td></tr>
      <tr><td><code>replicated</code></td><td>The above, plus independently re-run by
        a second member before publication.</td></tr>
      <tr><td><code>SYNTHETIC</code></td><td>Smoke-test output on made-up data. Labelled
        loudly, never citable, never shown here.</td></tr>
    </table></div>
  </section>

  <section>
    <h2>Participate</h2>
    <p><strong>Join a project</strong> — cards marked <em>open to applications</em>
    take a short application:
    <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">open an issue</a>
    saying who you are, whether you work with an agent, and what you bring (an idea,
    data, compute, or a licence).</p>
    <p><strong>Propose a project</strong> — same place, different form. A faculty
    member or student with a question and at least one committed collaborator can
    start one.</p>
    <p><strong>Start your own</strong> — the whole machinery is a
    <a href="https://github.com/republic-of-letters/protocol">template repository</a>:
    one command creates a new project with the protocol, the safety tooling, and the
    onboarding drill included.</p>
  </section>

  <footer>
    Named for the 17th-century scholars' network that did science by mail.
    The protocol is open — <a href="https://github.com/republic-of-letters/protocol">read
    it, reuse it, improve it</a>.
  </footer>
</main>
</body>
</html>
"""


def main():
    data = yaml.safe_load((ROOT / "projects.yaml").read_text()) or {}
    projects = data.get("projects") or []
    cards = "\n".join(card(p) for p in projects) if projects else EMPTY_STATE
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(PAGE.replace("{{CARDS}}", cards))
    print(f"built _site/index.html with {len(projects)} project card(s)")


if __name__ == "__main__":
    main()
