#!/usr/bin/env python3
"""Build the showcase site: projects.yaml -> _site/index.html (EN) + _site/zh/index.html (中文).

No framework — self-contained HTML, styled inline, light/dark aware.
Run locally to preview:  python scripts/build-site.py && open _site/index.html
"""

import html
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
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


def esc(v):
    return html.escape(str(v), quote=True)


def card(p, lang):
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

    title = p.get("title", p.get("id", "untitled"))
    blurb = p.get("blurb", "")
    if lang == "zh":
        title = p.get("title_zh", title)
        blurb = p.get("blurb_zh", blurb)
    title = esc(title)
    if tier_key == "open" and p.get("repo"):
        title = f'<a href="{esc(p["repo"])}">{title}</a>'

    return f"""      <article class="card">
        <div class="pills">{pills}</div>
        <h3>{title}</h3>
        <p>{esc(blurb)}</p>
        {meta_html}{outputs}
      </article>"""


EMPTY = {
    "en": """      <p class="empty">The first projects are being onboarded — check back soon,
      or <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">propose one</a>.</p>""",
    "zh": """      <p class="empty">首批项目正在入驻——过几天再来看看，或者
      <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">现在就提议一个</a>。</p>""",
}

CSS = """
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
    font: 17px/1.7 Georgia, 'Times New Roman', 'Songti SC', 'Noto Serif CJK SC', serif;
    padding: 0 1.25rem;
  }
  main { max-width: 920px; margin: 0 auto; }
  a { color: var(--link); text-decoration-thickness: 1px; text-underline-offset: 3px; }
  nav { display: flex; flex-wrap: wrap; gap: 1.1rem; padding: 1.1rem 0;
        border-bottom: 1px solid var(--line);
        font: 500 0.85rem/1 ui-sans-serif, system-ui, sans-serif; }
  nav a { color: var(--muted); text-decoration: none; }
  nav a:hover { color: var(--ink); }
  nav .lang { margin-left: auto; color: var(--accent); }
  header { padding: 3.5rem 0 2.5rem; border-bottom: 1px solid var(--line); }
  .seal { color: var(--accent); font-size: 0.85rem; letter-spacing: 0.22em;
          text-transform: uppercase; font-family: ui-sans-serif, system-ui, sans-serif; }
  h1 { font-size: 2.6rem; font-weight: 500; line-height: 1.15; margin: 0.5rem 0 1rem; }
  header p.lead { font-size: 1.15rem; max-width: 680px; color: var(--muted); }
  section { padding: 2.75rem 0; border-bottom: 1px solid var(--line); }
  section:last-of-type { border-bottom: none; }
  h2 { font-size: 1.5rem; font-weight: 500; margin-bottom: 0.6rem; }
  .kicker { color: var(--muted); max-width: 680px; margin-bottom: 1.4rem; }
  h3 { font-size: 1.12rem; font-weight: 600; margin: 0.4rem 0; }
  .cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; }
  .cols h3 { font-size: 1rem; }
  .cols .n { color: var(--accent); font-family: ui-sans-serif, system-ui, sans-serif;
             font-size: 0.8rem; letter-spacing: 0.12em; }
  .cols p { font-size: 0.95rem; color: var(--muted); }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 1.25rem; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 10px;
          padding: 1.25rem 1.35rem; }
  .card p { font-size: 0.95rem; }
  .card.mode h3 { margin-top: 0; }
  .card .who { margin-top: 0.6rem; font-size: 0.85rem; color: var(--muted); }
  .pills { margin-bottom: 0.35rem; }
  .pill { display: inline-block; font: 600 0.7rem/1 ui-sans-serif, system-ui, sans-serif;
          letter-spacing: 0.06em; text-transform: uppercase; color: var(--pc, var(--muted));
          border: 1px solid currentColor; border-radius: 999px;
          padding: 0.25rem 0.6rem; margin-right: 0.4rem; }
  .pill.tier { color: var(--muted); }
  .meta, .outputs { margin-top: 0.6rem; font-size: 0.85rem !important; color: var(--muted); }
  .empty { color: var(--muted); font-style: italic; }
  ol.journey { counter-reset: step; list-style: none; padding: 0; max-width: 720px; }
  ol.journey li { counter-increment: step; position: relative; padding: 0 0 1.4rem 3.2rem; }
  ol.journey li::before { content: counter(step); position: absolute; left: 0; top: 0.1rem;
    width: 2.1rem; height: 2.1rem; border: 1px solid var(--accent); color: var(--accent);
    border-radius: 999px; display: flex; align-items: center; justify-content: center;
    font: 600 0.95rem/1 ui-sans-serif, system-ui, sans-serif; }
  ol.journey h3 { margin: 0 0 0.2rem; font-size: 1.05rem; }
  ol.journey p { font-size: 0.95rem; color: var(--muted); }
  table { border-collapse: collapse; width: 100%; font-size: 0.95rem; }
  th, td { text-align: left; padding: 0.55rem 0.9rem 0.55rem 0; border-bottom: 1px solid var(--line);
           vertical-align: top; }
  th { font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.75rem;
       letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
  .scroll { overflow-x: auto; }
  details { border-bottom: 1px solid var(--line); padding: 0.9rem 0; }
  details:last-of-type { border-bottom: none; }
  summary { cursor: pointer; font-weight: 600; font-size: 1rem; }
  details p { padding: 0.6rem 0 0.2rem; color: var(--muted); font-size: 0.95rem; max-width: 720px; }
  footer { padding: 2.5rem 0 3.5rem; color: var(--muted); font-size: 0.9rem; }
  code { font-family: ui-monospace, 'SF Mono', Menlo, monospace; font-size: 0.85em;
         background: var(--card); border: 1px solid var(--line); border-radius: 4px;
         padding: 0.1em 0.35em; }
  .cta { display: inline-block; margin-top: 0.4rem;
         font: 600 0.9rem/1 ui-sans-serif, system-ui, sans-serif;
         color: var(--accent); border: 1px solid var(--accent); border-radius: 8px;
         padding: 0.6rem 1rem; text-decoration: none; }
"""

PAGE_EN = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Republic of Letters</title>
<meta name="description" content="A research collaboration space where humans and their AI agents do empirical work by correspondence — under one protocol, behind three human gates.">
<style>{{CSS}}</style>
</head>
<body>
<main>
  <nav>
    <a href="#why">Why</a><a href="#modes">Modes</a><a href="#how">How it works</a>
    <a href="#projects">Projects</a><a href="#join">Participate</a><a href="#faq">FAQ</a>
    <a class="lang" href="zh/">中文</a>
  </nav>

  <header>
    <div class="seal">Respublica Literaria · est. 2026</div>
    <h1>Republic of Letters</h1>
    <p class="lead">A research collaboration space where faculty, students, and their
    AI agents do empirical work by correspondence. Questions and code travel out,
    results travel back — and every step is a reviewable letter in a permanent
    archive. Named for the 17th-century scholars' network that did science by mail.</p>
  </header>

  <section id="why">
    <h2>Why work this way</h2>
    <p class="kicker">Cross-institution empirical research usually stalls on the same
    four things: moving data, trusting code, losing context, and settling credit.
    This space removes all four by construction.</p>
    <div class="cols">
      <div><span class="n">DATA</span>
        <h3>Your data never leaves your machine</h3>
        <p>Collaborators send code; you run it after a safety review; only aggregates
        — figures, tables, write-ups — come back. No transfer agreements, no copies
        floating around. CI physically rejects raw data from every repository.</p></div>
      <div><span class="n">AGENTS</span>
        <h3>Built for the agent era</h3>
        <p>Every member works with an AI agent. The protocol is written to be
        <em>executed</em> by agents — exact commands, file contracts, hard
        boundaries — so agents do the legwork at machine speed while humans keep
        every decision that matters.</p></div>
      <div><span class="n">MEMORY</span>
        <h3>Everything on the record</h3>
        <p>Every question, run, decision, and dead end is a diffable file under
        version control. A new collaborator — or a fresh agent session — can
        reconstruct the whole history. Killed ideas get post-mortems, not silence.</p></div>
      <div><span class="n">TRUST</span>
        <h3>Trust is structural, not personal</h3>
        <p>No code touches real data until it passes an automated scan <em>and</em> a
        human read. Nothing enters the record until humans on both sides agree.
        Every published number carries its provenance level.</p></div>
      <div><span class="n">CREDIT</span>
        <h3>Authorship settled early, in writing</h3>
        <p>Name order — or the rule that decides it — is fixed no later than the
        moment a topic gets its GO, with data and compute contributions counted.
        Deferring it is a protocol violation, not an oversight.</p></div>
      <div><span class="n">COST</span>
        <h3>Zero infrastructure, zero lock-in</h3>
        <p>It's plain GitHub: free, familiar, durable. One command starts a project;
        if you ever leave, you take the complete archive with you. Nothing
        proprietary anywhere in the loop.</p></div>
    </div>
  </section>

  <section id="modes">
    <h2>What you can run here</h2>
    <p class="kicker">One protocol, several shapes. Each mode below is the same
    machinery — topics, rounds, human gates — arranged for a different kind of
    collaboration.</p>
    <div class="grid">
      <article class="card mode">
        <h3>Co-authored paper</h3>
        <p>The classic unit. One topic = one candidate paper: probe rounds test
        feasibility, GO fixes authorship, analysis rounds build the results, and the
        merged archive becomes the paper's audit trail.</p>
        <p class="who">For: 2–5 researchers with a shared question.</p>
      </article>
      <article class="card mode">
        <h3>Data–idea partnership</h3>
        <p>One side holds data and compute, the other brings hypotheses and code —
        the founding pattern of this space. Restricted-licence data (WRDS, Compustat…)
        stays on the licence-holder's machine and joins on derived tables.</p>
        <p class="who">For: data owners + methodologists who couldn't otherwise work together.</p>
      </article>
      <article class="card mode">
        <h3>Research programme</h3>
        <p>A funded project or long-running agenda as one repository with several
        topics under it. Decision logs give the programme institutional memory;
        milestones are merged rounds anyone can verify.</p>
        <p class="who">For: grant projects, lab agendas, multi-paper collaborations.</p>
      </article>
      <article class="card mode">
        <h3>Thesis &amp; student training</h3>
        <p>Students propose rounds; the mentor holds a co-review gate on every merge.
        The student learns by doing real research inside guardrails, and the merged
        archive is the cleanest possible record of their work.</p>
        <p class="who">For: supervisors and their graduate or undergraduate students.</p>
      </article>
      <article class="card mode">
        <h3>Replication &amp; robustness</h3>
        <p>Re-run an existing analysis as rounds — same question, independent
        execution. Successful re-runs earn results the <code>replicated</code>
        provenance level. An ideal first contribution for a new member.</p>
        <p class="who">For: students entering a project; teams hardening a result before submission.</p>
      </article>
    </div>
  </section>

  <section id="how">
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

  <section id="projects">
    <h2>Projects</h2>
    <p class="kicker">Research lives in private repositories; what appears here is
    what each project approved for public display. <em>Display only</em> means look
    but don't join; <em>open to applications</em> means there's a door — knock.</p>
    <div class="grid">
{{CARDS}}
    </div>
  </section>

  <section id="join">
    <h2>How to participate</h2>
    <ol class="journey">
      <li><h3>Look around</h3>
        <p>Browse the projects above and skim the
        <a href="https://github.com/republic-of-letters/protocol">protocol</a> —
        it's short, and it is the whole rulebook.</p></li>
      <li><h3>Pick your door</h3>
        <p><a href="https://github.com/republic-of-letters/showcase/issues/new/choose">Apply
        to join</a> a project marked <em>open to applications</em>, telling its lead who
        you are and what you bring — an idea, code skills, data, compute, or a licence.
        Or <a href="https://github.com/republic-of-letters/showcase/issues/new/choose">propose
        a new project</a>: a question, a falsifier, a data plan, and at least one
        committed collaborator.</p></li>
      <li><h3>Onboard — you and your agent</h3>
        <p>The onboarding guide takes you from zero (no GitHub account) to a working
        setup, and is written for your AI agent to execute. It ends with a
        <em>drill</em>: one practice round, end to end, so the loop is proven before
        real work depends on it.</p></li>
      <li><h3>Work in rounds</h3>
        <p>Propose questions with runnable code; the data side runs them and returns
        results into the same thread. Iterate, disagree, converge — everything in
        writing, everything reviewable.</p></li>
      <li><h3>Decide at the gates, publish through the record</h3>
        <p>Humans call GO/kill, approve runs, and merge. What survives all three
        gates becomes the permanent archive — and, if the project chooses, a card
        and its outputs on this page.</p></li>
    </ol>
    <p><strong>Running your own?</strong> The whole machinery is a template — one
    command creates a new project with the protocol, safety tooling, and onboarding
    included:</p>
    <p><code>gh repo create &lt;owner&gt;/&lt;name&gt; --template republic-of-letters/protocol --private</code></p>
  </section>

  <section id="trust">
    <h2>What you can trust</h2>
    <p class="kicker">Trust here is a property of the pipeline, not a promise.
    Every published artifact carries its provenance:</p>
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

  <section id="faq">
    <h2>Questions people ask</h2>
    <details><summary>Do I need to know git or GitHub?</summary>
      <p>Barely. The onboarding guide is written for your AI agent to execute; the
      human steps are creating an account and clicking a few buttons. If you can
      answer email, you can work here.</p></details>
    <details><summary>Is my data safe?</summary>
      <p>Your data never leaves your machine. You (or your side) run every analysis
      yourself, after an automated scan and a human read of the code — sandboxed,
      read-only, no network. Repositories carry only aggregate results, and CI
      rejects anything that looks like raw data.</p></details>
    <details><summary>What AI agent do I need?</summary>
      <p>Any capable coding agent — Claude Code, Codex, or similar. The protocol is
      agent-agnostic: it's a set of files and commands any competent agent can
      follow. You can even work without one, though you'd be doing the legwork
      yourself.</p></details>
    <details><summary>Who owns the results? Who gets authorship?</summary>
      <p>The humans. Authorship — name order or the rule that decides it — is agreed
      in writing no later than the moment a topic gets its GO, and data/compute
      contributions count. Agents are pens, not authors.</p></details>
    <details><summary>Who can see my project?</summary>
      <p>You choose: <em>display only</em> (a title and approved outputs on this
      page), <em>open to applications</em> (the above plus a way in), or fully
      <em>open</em>. The research repository itself stays private to invited members
      unless you decide otherwise.</p></details>
    <details><summary>What does it cost?</summary>
      <p>Nothing. The space runs on plain GitHub — free for private research
      repositories — and the protocol is open source (MIT).</p></details>
  </section>

  <footer>
    Named for the 17th-century scholars' network that did science by mail.
    The protocol is open — <a href="https://github.com/republic-of-letters/protocol">read
    it, reuse it, improve it</a>. · <a href="zh/">中文</a>
  </footer>
</main>
</body>
</html>
"""

PAGE_ZH = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>文人共和国 · Republic of Letters</title>
<meta name="description" content="一个人与 AI 代理以通信方式合作做实证研究的空间——同一套协议，三道由人把守的闸门。">
<style>{{CSS}}</style>
</head>
<body>
<main>
  <nav>
    <a href="#why">优势</a><a href="#modes">合作模式</a><a href="#how">运作方式</a>
    <a href="#projects">项目</a><a href="#join">如何参与</a><a href="#faq">常见问题</a>
    <a class="lang" href="../">English</a>
  </nav>

  <header>
    <div class="seal">Respublica Literaria · est. 2026</div>
    <h1>文人共和国</h1>
    <p class="lead">一个教师、学生和他们的 AI 代理以「通信」方式合作做实证研究的空间。
    问题与代码寄出，结果寄回——每一步都是档案里一封可审阅的信。名字取自十七世纪
    靠书信往来做科学的学者网络（Republic of Letters）。</p>
  </header>

  <section id="why">
    <h2>为什么用这种方式做研究</h2>
    <p class="kicker">跨机构的实证合作通常卡在四件事上：数据传不出去、别人的代码不敢跑、
    合作过程没有记录、署名谈不拢。这个空间从结构上把四件事都解决掉。</p>
    <div class="cols">
      <div><span class="n">数据</span>
        <h3>数据从不离开你的机器</h3>
        <p>合作者把代码寄给你；你审查之后自己运行；寄回去的只有聚合结果——图、表、
        文字结论。不需要数据传输协议，不会有数据副本流散在外。CI 会物理拦截任何
        试图进入仓库的原始数据。</p></div>
      <div><span class="n">代理</span>
        <h3>为智能体时代而设计</h3>
        <p>每位成员都带着自己的 AI 代理工作。协议就是写给代理「执行」的——精确的命令、
        文件契约、硬边界——代理以机器速度承担跑腿的部分，而每一个要紧的决定都留在人手里。</p></div>
      <div><span class="n">记录</span>
        <h3>全程留痕，包括失败</h3>
        <p>每个问题、每次运行、每个决定、每条死路，都是版本库里可以逐行对比的文件。
        新加入的合作者——或者新开的代理会话——都能完整重建历史。被否掉的方向有
        「尸检报告」，不会无声消失。</p></div>
      <div><span class="n">信任</span>
        <h3>信任来自结构，不靠人品</h3>
        <p>任何代码在触碰真实数据之前，都要先通过自动扫描「加上」人工阅读；任何结果
        在进入档案之前，都要双方的人都点头。每个公开发表的数字都带着自己的来源等级。</p></div>
      <div><span class="n">署名</span>
        <h3>署名先小人后君子</h3>
        <p>作者排序——或者决定排序的规则——最迟在课题立项（GO）那一刻白纸黑字写下，
        数据和算力的贡献都计入。拖着不谈在这里是违反协议，而不是常态。</p></div>
      <div><span class="n">成本</span>
        <h3>零基础设施，零锁定</h3>
        <p>就是普通的 GitHub：免费、熟悉、耐用。一条命令创建一个项目；哪天要走，
        完整档案随身带走。整个流程里没有任何私有依赖。</p></div>
    </div>
  </section>

  <section id="modes">
    <h2>支持哪些合作模式</h2>
    <p class="kicker">一套协议，多种形态。下面每种模式用的都是同一套机制——课题、
    round、人闸——只是为不同的合作组合方式排布。</p>
    <div class="grid">
      <article class="card mode">
        <h3>合著论文</h3>
        <p>最经典的单元。一个课题（topic）就是一篇候选论文：试探性 round 验证可行性，
        GO 的同时定署名，主体分析 round 产出结果，合并档案就是这篇论文完整的审计线索。</p>
        <p class="who">适合：2–5 位有共同问题的研究者。</p>
      </article>
      <article class="card mode">
        <h3>数据方 × 想法方</h3>
        <p>一方有数据和算力，另一方有假设和代码——这是本空间的创始形态。受限授权数据
        （WRDS、Compustat 等）也留在持照人自己的机器上，只在衍生表层面做连接。</p>
        <p class="who">适合：原本没办法坐到一起的数据持有者与方法研究者。</p>
      </article>
      <article class="card mode">
        <h3>课题 / 研究计划</h3>
        <p>一个立项课题或长期研究议程 = 一个仓库，下辖多个 topic。决策日志让课题有
        制度性记忆；里程碑就是一个个已合并、任何人都能核查的 round。</p>
        <p class="who">适合：基金课题、实验室议程、多篇论文的长期合作。</p>
      </article>
      <article class="card mode">
        <h3>学位论文与学生培养</h3>
        <p>学生提出 round，导师在每次合并时共同把关。学生在护栏之内做真实研究，
        而合并档案就是这段工作最干净的成长记录。</p>
        <p class="who">适合：导师与他们的研究生、本科生。</p>
      </article>
      <article class="card mode">
        <h3>复现与稳健性检验</h3>
        <p>把已有分析作为 round 重新独立执行——同样的问题，独立的运行。复现成功的
        结果获得 <code>replicated</code> 来源等级。这也是新成员最理想的第一份贡献。</p>
        <p class="who">适合：刚加入项目的学生；投稿前想把结果焊牢的团队。</p>
      </article>
    </div>
  </section>

  <section id="how">
    <h2>运作方式</h2>
    <div class="cols">
      <div><span class="n">一 · 课题</span>
        <h3>一篇候选论文，一个课题</h3>
        <p>假设、证伪条件、署名约定和决策日志都在一个文件里。杀掉一个课题是正式的
        产出，附带尸检报告——档案会记住试过的一切，以及为什么停下。</p></div>
      <div><span class="n">二 · ROUND</span>
        <h3>一个问题，一个 Pull Request</h3>
        <p>提议方写下问题和可运行的代码；数据方做安全审查后在真实数据上运行，把聚合
        结果——图、表、文字结论——寄回同一个线程。</p></div>
      <div><span class="n">三 · 人闸</span>
        <h3>三扇只有人能开的门</h3>
        <p>课题的 GO/终止与署名；任何触碰真实数据的代码；以及合并进永久档案。代理起草、
        写码、分析——人做决定。任何人都能用一个标签叫停任何 round。</p></div>
    </div>
  </section>

  <section id="projects">
    <h2>项目</h2>
    <p class="kicker">研究本身在私有仓库里进行；这里展示的是各项目批准公开的部分。
    「仅展示」意味着只看不进；「开放申请」意味着有一扇门——去敲。</p>
    <div class="grid">
{{CARDS}}
    </div>
  </section>

  <section id="join">
    <h2>如何参与</h2>
    <ol class="journey">
      <li><h3>先逛逛</h3>
        <p>看看上面的项目，翻一翻<a href="https://github.com/republic-of-letters/protocol">协议</a>——
        不长，但它就是全部规则。</p></li>
      <li><h3>选一扇门</h3>
        <p>对标着「开放申请」的项目，<a href="https://github.com/republic-of-letters/showcase/issues/new/choose">提交加入申请</a>，
        告诉项目负责人你是谁、带来什么——想法、代码能力、数据、算力或者数据授权。
        或者<a href="https://github.com/republic-of-letters/showcase/issues/new/choose">提议一个新项目</a>：
        一个问题、一个证伪条件、一份数据计划，和至少一位已经确定加入的合作者。</p></li>
      <li><h3>入职——你和你的代理一起</h3>
        <p>入职指南把你从零（连 GitHub 账号都没有）带到可以工作的状态，而且是写给你的
        AI 代理执行的。最后一步是一次「演练」：完整走一遍练习 round，在真实工作开始前
        把整个流程验证一遍。</p></li>
      <li><h3>以 round 的方式工作</h3>
        <p>带着可运行的代码提出问题；数据方运行后把结果寄回同一线程。迭代、争论、收敛——
        一切都落在文字上，一切都可审阅。</p></li>
      <li><h3>在闸口决策，经档案发表</h3>
        <p>人来判 GO/终止、批准运行、决定合并。通过全部三道闸的成果进入永久档案——
        如果项目愿意，也会成为这个页面上的一张卡片和它的公开成果。</p></li>
    </ol>
    <p><strong>想自己开一个？</strong>整套机制就是一个模板——一条命令创建新项目，
    协议、安全工具、入职流程全部内置：</p>
    <p><code>gh repo create &lt;owner&gt;/&lt;name&gt; --template republic-of-letters/protocol --private</code></p>
  </section>

  <section id="trust">
    <h2>可以相信什么</h2>
    <p class="kicker">这里的信任是流水线的属性，不是口头承诺。每个公开发表的产物都
    带有来源等级：</p>
    <div class="scroll"><table>
      <tr><th>等级</th><th>含义</th></tr>
      <tr><td><code>ran-on-real-data</code></td><td>由数据方在真实数据上跑出，经过安全闸，
        双方的人共同合并进档案。</td></tr>
      <tr><td><code>replicated</code></td><td>在上一条基础上，发表前由第二位成员独立
        复跑确认。</td></tr>
      <tr><td><code>SYNTHETIC</code></td><td>合成数据上的冒烟测试输出。醒目标注，
        不可引用，永远不会出现在本页。</td></tr>
    </table></div>
  </section>

  <section id="faq">
    <h2>常见问题</h2>
    <details><summary>我需要会 git 或 GitHub 吗？</summary>
      <p>基本不用。入职指南是写给你的 AI 代理执行的；人需要做的只是注册账号、点几个
      按钮。会收发邮件，就能在这里工作。</p></details>
    <details><summary>我的数据安全吗？</summary>
      <p>数据从不离开你的机器。每次分析都由你（或你这一侧）亲自运行，且在运行前经过
      自动扫描和人工读码——沙箱、只读、无网络。仓库只承载聚合结果，CI 会拒绝任何
      看起来像原始数据的东西。</p></details>
    <details><summary>需要什么样的 AI 代理？</summary>
      <p>任何有编码能力的代理——Claude Code、Codex 或同类产品。协议与具体代理无关：
      它只是一组任何称职的代理都能照做的文件和命令。没有代理也能参与，只是跑腿的活
      得自己干。</p></details>
    <details><summary>成果归谁？署名怎么算？</summary>
      <p>归人。署名——排序或决定排序的规则——最迟在课题 GO 时书面约定，数据和算力
      贡献都计入。代理是笔，不是作者。</p></details>
    <details><summary>谁能看到我的项目？</summary>
      <p>你自己选：「仅展示」（本页只出现标题和批准公开的成果）、「开放申请」（在此
      基础上多一扇门）、或者「完全开放」。研究仓库本身始终只对受邀成员可见，除非你
      主动决定公开。</p></details>
    <details><summary>要花钱吗？</summary>
      <p>不用。整个空间跑在普通的 GitHub 上——私有研究仓库免费——协议本身开源（MIT）。</p></details>
  </section>

  <footer>
    名字取自十七世纪靠书信做科学的学者网络。协议是开放的——
    <a href="https://github.com/republic-of-letters/protocol">欢迎阅读、复用、改进</a>。
    · <a href="../">English</a>
  </footer>
</main>
</body>
</html>
"""


def main():
    data = yaml.safe_load((ROOT / "projects.yaml").read_text()) or {}
    projects = data.get("projects") or []
    OUT.mkdir(exist_ok=True)
    (OUT / "zh").mkdir(exist_ok=True)
    for lang, page, path in (("en", PAGE_EN, OUT / "index.html"),
                             ("zh", PAGE_ZH, OUT / "zh" / "index.html")):
        cards = "\n".join(card(p, lang) for p in projects) if projects else EMPTY[lang]
        path.write_text(page.replace("{{CSS}}", CSS).replace("{{CARDS}}", cards))
    print(f"built en + zh with {len(projects)} project card(s)")


if __name__ == "__main__":
    main()
