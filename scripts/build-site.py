#!/usr/bin/env python3
"""Build the showcase site from projects.yaml + notices.yaml.

Outputs:
  _site/index.html            EN main page
  _site/zh/index.html         ZH main page
  _site/letter/index.html     EN "read one letter"
  _site/zh/letter/index.html  ZH "read one letter"
  _site/assets/               static assets (figures)

Templates live in scripts/templates/. No framework; light/dark aware.
Run locally to preview:  python scripts/build-site.py && open _site/index.html
"""

import datetime
import html
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "scripts" / "templates"
OUT = ROOT / "_site"

STATUS = {
    "incubating": {"color": "#b45309", "en": "incubating", "zh": "孵化中"},
    "active":     {"color": "#15803d", "en": "active",     "zh": "进行中"},
    "writing":    {"color": "#1d4ed8", "en": "writing",    "zh": "写作中"},
    "published":  {"color": "#7e22ce", "en": "published",  "zh": "已发表"},
    "archived":   {"color": "#6b7280", "en": "archived",   "zh": "已归档"},
}
TIER = {
    "display-only":  {"en": "display only",         "zh": "仅展示"},
    "apply-to-join": {"en": "open to applications", "zh": "开放申请"},
    "open":          {"en": "open",                 "zh": "完全开放"},
}
KIND = {
    "offering": {"color": "#15803d", "en": "offering", "zh": "提供"},
    "seeking":  {"color": "#1d4ed8", "en": "seeking",  "zh": "征求"},
}
WHAT = {
    "data":    {"en": "data",    "zh": "数据"},
    "licence": {"en": "licence", "zh": "数据授权"},
    "compute": {"en": "compute", "zh": "算力"},
    "methods": {"en": "methods", "zh": "方法"},
    "ideas":   {"en": "ideas",   "zh": "想法"},
}
TERMS = {
    "can-run":       {"en": "code comes to it",                    "zh": "代码上门跑"},
    "can-share":     {"en": "can be shared into a project",        "zh": "可入圈共享"},
    "licence-bound": {"en": "licence-bound; joins on derived tables", "zh": "受授权约束，衍生表连接"},
}


def esc(v):
    return html.escape(str(v), quote=True)


def pick(entry, field, lang):
    """Language-aware field: prefer <field>_zh on the zh page, fall back to <field>."""
    if lang == "zh" and entry.get(f"{field}_zh"):
        return entry[f"{field}_zh"]
    return entry.get(field, "")


def project_card(p, lang):
    status = p.get("status", "incubating")
    s = STATUS.get(status, {"color": "#6b7280", "en": status, "zh": status})
    tier_key = p.get("tier", "display-only")
    tier = TIER.get(tier_key, {"en": tier_key, "zh": tier_key})[lang]

    pills = (
        f'<span class="pill" style="--pc:{s["color"]}">{esc(s[lang])}</span>'
        f'<span class="pill tier">{esc(tier)}</span>'
    )
    meta = []
    if p.get("since"):
        meta.append(f"since {esc(p['since'])}" if lang == "en" else f"始于 {esc(p['since'])}")
    if p.get("people"):
        meta.append(f"{esc(p['people'])} members" if lang == "en" else f"{esc(p['people'])} 名成员")
    if p.get("contact") and tier_key == "apply-to-join":
        meta.append(f"contact {esc(p['contact'])}" if lang == "en" else f"联系 {esc(p['contact'])}")
    meta_html = f'<p class="meta">{" · ".join(meta)}</p>' if meta else ""

    outputs = ""
    if p.get("outputs"):
        links = " · ".join(
            f'<a href="{esc(o["url"])}">{esc(o["label"])}</a>' for o in p["outputs"]
        )
        outputs = f'<p class="outputs">{links}</p>'

    title = esc(pick(p, "title", lang) or p.get("id", "untitled"))
    if tier_key == "open" and p.get("repo"):
        title = f'<a href="{esc(p["repo"])}">{title}</a>'
    blurb = esc(pick(p, "blurb", lang))

    return f"""      <article class="card">
        <div class="pills">{pills}</div>
        <h3>{title}</h3>
        <p>{blurb}</p>
        {meta_html}{outputs}
      </article>"""


def notice_card(n, lang):
    kind_key = n.get("kind", "offering")
    k = KIND.get(kind_key, {"color": "#6b7280", "en": kind_key, "zh": kind_key})
    what_key = n.get("what", "")
    what = WHAT.get(what_key, {"en": what_key, "zh": what_key})[lang]

    pills = (
        f'<span class="pill" style="--pc:{k["color"]}">{esc(k[lang])}</span>'
        f'<span class="pill tier">{esc(what)}</span>'
    )
    facts = []
    for field in ("shape", "scale", "period"):
        v = pick(n, field, lang)
        if v:
            facts.append(f"<span>{esc(v)}</span>")
    terms_key = n.get("terms")
    if terms_key in TERMS:
        facts.append(f"<span>{esc(TERMS[terms_key][lang])}</span>")
    facts_html = f'<p class="facts">{" · ".join(facts)}</p>' if facts else ""

    seeking = pick(n, "seeking", lang)
    seeking_html = ""
    if seeking:
        label = "In return:" if lang == "en" else "所求："
        seeking_html = f'<p><strong>{label}</strong> {esc(seeking)}</p>'

    contact = n.get("contact", "watch")
    if contact == "watch":
        contact_str = ("anonymous — reply via an issue naming this id"
                       if lang == "en" else "匿名——开 issue 写明本布告编号即可应答")
    else:
        contact_str = f"contact {esc(contact)}" if lang == "en" else f"联系 {esc(contact)}"
    meta = [f'<span>{esc(n.get("id", ""))}</span>', f"<span>{contact_str}</span>"]
    if n.get("expires"):
        meta.append(f"<span>{'until' if lang == 'en' else '有效至'} {esc(n['expires'])}</span>")

    return f"""      <article class="card notice">
        <div class="pills">{pills}</div>
        <h3>{esc(pick(n, "area", lang))}</h3>
        {facts_html}
        {seeking_html}
        <p class="meta">{" · ".join(meta)}</p>
      </article>"""


EMPTY_PROJECTS = {
    "en": """      <p class="empty">The first projects are being onboarded — check back soon,
      or <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">propose one</a>.</p>""",
    "zh": """      <p class="empty">首批项目正在入驻——过几天再来看看，或者
      <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">现在就提议一个</a>。</p>""",
}
EMPTY_NOTICES = {
    "en": """      <p class="empty">The board is empty — be the first to
      <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">post a notice</a>.</p>""",
    "zh": """      <p class="empty">布告栏还空着——来
      <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">登第一张布告</a>。</p>""",
}


def load_notices():
    data = yaml.safe_load((ROOT / "notices.yaml").read_text()) or {}
    notices = data.get("notices") or []
    this_month = datetime.date.today().strftime("%Y-%m")
    live, dropped = [], 0
    for n in notices:
        exp = str(n.get("expires", ""))
        if exp and exp < this_month:
            dropped += 1
        else:
            live.append(n)
    if dropped:
        print(f"dropped {dropped} expired notice(s)")
    return live


def main():
    projects = (yaml.safe_load((ROOT / "projects.yaml").read_text()) or {}).get("projects") or []
    notices = load_notices()
    css = (TPL / "style.css").read_text()

    OUT.mkdir(exist_ok=True)
    for sub in ("zh", "letter", "zh/letter"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    if (ROOT / "assets").is_dir():
        shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)

    for lang in ("en", "zh"):
        cards = ("\n".join(project_card(p, lang) for p in projects)
                 if projects else EMPTY_PROJECTS[lang])
        boards = ("\n".join(notice_card(n, lang) for n in notices)
                  if notices else EMPTY_NOTICES[lang])
        page = (TPL / f"index_{lang}.html").read_text()
        page = page.replace("{{CSS}}", css).replace("{{CARDS}}", cards).replace("{{NOTICES}}", boards)
        dest = OUT / "index.html" if lang == "en" else OUT / "zh" / "index.html"
        dest.write_text(page)

        letter = (TPL / f"letter_{lang}.html").read_text().replace("{{CSS}}", css)
        ldest = OUT / "letter" / "index.html" if lang == "en" else OUT / "zh" / "letter" / "index.html"
        ldest.write_text(letter)

    print(f"built en+zh main pages ({len(projects)} project(s), {len(notices)} notice(s)) + letter pages")


if __name__ == "__main__":
    main()
