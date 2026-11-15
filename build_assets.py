#!/usr/bin/env python3
"""Generate the profile's SVG assets in light and dark variants.

Run from the repo root:  python3 scripts/build_assets.py
Every SVG is self-contained (no external fonts or images), so GitHub's image
proxy renders it reliably. Edit the text in the CONTENT section and re-run.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(bg1="#0b1018", bg2="#111c28", panel="#151f2c", line="#2a3a4c",
                 text="#e6edf3", muted="#9aa7b4", faint="#6e7d8c", accent="#2dd4bf",
                 accent_bg="#0f2a2a", gold="#f2c14e", gold_bg="#2a2412", violet="#a78bfa",
                 violet_bg="#1e1734", red="#f87171", red_bg="#2b1517", grid="#2dd4bf"),
    "light": dict(bg1="#ffffff", bg2="#f3f6f9", panel="#ffffff", line="#d0d7de",
                  text="#1f2328", muted="#57606a", faint="#8c959f", accent="#0f8f80",
                  accent_bg="#e6f6f3", gold="#9a6700", gold_bg="#fff4d6", violet="#6d4fd6",
                  violet_bg="#f1edff", red="#cf222e", red_bg="#ffebe9", grid="#0f8f80"),
}


def t(x, y, s, size, fill, weight=400, family=SANS, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def frame(w, h, c, title, desc, body, radius=14):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c['grid']}" stroke-opacity=".06"/></pattern>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c['faint']}"/></marker>
<marker id="arrA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c['accent']}"/></marker>
<marker id="arrR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c['red']}"/></marker>
</defs>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{radius}" fill="url(#bg)" stroke="{c['line']}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{radius}" fill="url(#grid)"/>
{body}
</svg>'''


def chip(x, y, label, c, fg=None, bg=None, size=13, family=SANS, pad=12):
    w = int(len(label) * size * 0.58) + pad * 2
    fg = fg or c["muted"]
    bg = bg or c["panel"]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{size+15}" rx="{(size+15)//2}" fill="{bg}" stroke="{c["line"]}"/>'
            + t(x + pad, y + size + 3, label, size, fg, 500, family)), w


def node(x, y, w, h, title, sub, c, tone="plain"):
    stroke = {"plain": c["line"], "accent": c["accent"], "violet": c["violet"],
              "red": c["red"], "gold": c["gold"]}[tone]
    fill = {"plain": c["panel"], "accent": c["accent_bg"], "violet": c["violet_bg"],
            "red": c["red_bg"], "gold": c["gold_bg"]}[tone]
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}"/>'
    cy = y + h / 2
    if sub:
        out += t(x + w / 2, cy - 5, title, 19, c["text"], 600, anchor="middle")
        out += t(x + w / 2, cy + 19, sub, 14.5, c["muted"], 400, MONO, "middle")
    else:
        out += t(x + w / 2, cy + 7, title, 19, c["text"], 600, anchor="middle")
    return out


def arrow(x1, y1, x2, y2, c, kind="plain", dashed=False, path=None):
    col = {"plain": c["faint"], "accent": c["accent"], "red": c["red"]}[kind]
    mk = {"plain": "arr", "accent": "arrA", "red": "arrR"}[kind]
    d = path or f"M{x1} {y1}L{x2} {y2}"
    dash = ' stroke-dasharray="5 5"' if dashed else ""
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6"{dash} marker-end="url(#{mk})"/>'


def row(nodes, y, h, c, x0=48, gap=34, total=1184):
    """Lay out (title, sub, tone) nodes evenly in one row; return svg and box centres."""
    n = len(nodes)
    w = (total - gap * (n - 1)) / n
    out, boxes = "", []
    for i, (title, sub, tone) in enumerate(nodes):
        x = x0 + i * (w + gap)
        out += node(x, y, w, h, title, sub, c, tone)
        boxes.append((x, w))
        if i:
            px, pw = boxes[i - 1]
            out += arrow(px + pw + 3, y + h / 2, x - 3, y + h / 2, c)
    return out, boxes


# ---------------------------------------------------------------- CONTENT

def hero(c):
    b = ""
    b += t(64, 78, "ayush@github:~$ whoami", 18, c["accent"], 500, MONO)
    b += t(60, 154, "Ayush Bansal", 74, c["text"], 700)
    b += t(64, 204, "Software engineer · backend, cloud & applied AI", 30, c["muted"], 500)
    b += t(64, 246, "I build the parts of software you only notice when they break.", 21, c["faint"], 400,
           extra='font-style="italic"')
    x = 64
    for label in ["Ex-SWE Intern @ Finn", "Ex-AI/ML Research @ UNSW Sydney", "LNMIIT '28"]:
        s, w = chip(x, 274, label, c, size=16)
        b += s
        x += w + 10
    cx, cy, cw, ch = 846, 44, 390, 272
    b += f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" fill="{c["panel"]}" stroke="{c["line"]}"/>'
    b += f'<rect x="{cx}" y="{cy}" width="{cw}" height="4" rx="2" fill="{c["gold"]}"/>'
    b += t(cx + 26, cy + 42, "HACKATHON PRIZES", 14, c["faint"], 600, extra='letter-spacing="2"')
    for i, (rank, event, track, col, bgk) in enumerate([
            ("2nd", "ETHGlobal Mumbai 2026", "0G Private Computer · $1,500", "gold", "gold_bg"),
            ("1st", "LNMHacks 8.0", "Viral Consumer Apps · $600", "accent", "accent_bg")]):
        y = cy + 98 + i * 82
        b += f'<circle cx="{cx+54}" cy="{y}" r="28" fill="{c[bgk]}" stroke="{c[col]}" stroke-width="1.5"/>'
        b += t(cx + 54, y + 7, rank, 19, c[col], 700, anchor="middle")
        b += t(cx + 98, y - 4, event, 20, c["text"], 600)
        b += t(cx + 98, y + 21, track, 16, c["muted"])
    b += t(cx + 26, cy + 252, "Sponsor- and partner-track prizes", 14, c["faint"])
    return frame(1280, 360, c, "Ayush Bansal: software engineer, backend, cloud and applied AI",
                 "SWE intern at Finn, AI/ML research intern at UNSW Sydney, LNMIIT 2028. "
                 "2nd place, 0G Private Computer track, ETHGlobal Mumbai 2026; 1st place, Viral Consumer Apps track, LNMHacks 8.0.", b)


def saka_header(c):
    b = ""
    b += f'<rect x="48" y="40" width="5" height="118" rx="2" fill="{c["violet"]}"/>'
    b += t(74, 64, "FEATURED PROJECT · TEAM BUILD", 15, c["violet"], 600, extra='letter-spacing="2"')
    b += t(72, 118, "SAKA", 56, c["text"], 700)
    b += t(242, 116, "an AI agent that has to prove every move", 28, c["muted"], 500)
    b += t(74, 150, "Plans on 0G · trades on Uniswap · refuses what it can't justify", 17, c["faint"], 400, MONO)
    cx = 902
    b += f'<rect x="{cx}" y="40" width="330" height="118" rx="12" fill="{c["gold_bg"]}" stroke="{c["gold"]}"/>'
    b += t(cx + 24, 80, "2nd place · $1,500", 27, c["gold"], 700)
    b += t(cx + 24, 110, "0G Private Computer track", 18, c["text"], 600)
    b += t(cx + 24, 138, "ETHGlobal Mumbai 2026", 16, c["muted"])
    return frame(1280, 198, c, "SAKA: 2nd place, 0G Private Computer track, ETHGlobal Mumbai 2026",
                 "Featured team project: an AI DeFi agent that plans on 0G, trades on Uniswap and refuses actions it cannot justify.", b)


def saka_pipeline(c):
    b = t(48, 46, "Every money-moving request takes the same path", 18, c["muted"], 600)
    nodes = [("Intent", "plain English", "plain"), ("Plan", "MCP · unsigned", "plain"),
             ("Score", "trade + hook", "plain"), ("Simulate", "eth_call", "plain"),
             ("AI guard", "fails closed", "violet"), ("Policy", "pure decide()", "violet")]
    s, boxes = row(nodes, 70, 72, c, x0=48, total=1184 - 236)
    b += s
    px, pw = boxes[-1]
    ox = px + pw + 40
    outs = [("Auto-run", "3 s to cancel", "accent", 50), ("Ask the user", "over your limits", "gold", 116),
            ("Refuse", "with a reason", "red", 182)]
    for title, sub, tone, y in outs:
        b += node(ox, y - 29, 196, 58, title, sub, c, tone)
        b += arrow(px + pw + 3, 106, ox - 3, y, c,
                   path=f"M{px+pw+3} 106C{px+pw+22} 106 {ox-22} {y} {ox-3} {y}")
    b += node(48, 196, 760, 64, "Every outcome, including refusals, is logged to 0G Storage",
              "request IDs · checks · policy result · tx hashes", c, "plain")
    return frame(1280, 290, c, "SAKA decision pipeline",
                 "Intent, plan via an unsigned-only MCP server, trade and hook scoring, simulation, an AI guard that fails closed, "
                 "and a policy function that auto-runs, asks the user or refuses. Every outcome is logged to 0G Storage.", b)


def helios(c):
    b = t(48, 44, "Ship: GitOps with canaries that judge themselves", 18, c["muted"], 600)
    s, bx = row([("git push", "", "plain"), ("GitHub Actions", "build image", "plain"),
                 ("ArgoCD", "sync from Git", "plain"), ("Argo Rollouts", "canary steps", "accent"),
                 ("Prometheus", "analysis mid-rollout", "accent")], 62, 68, c)
    b += s
    (x3, w3), (x4, w4) = bx[3], bx[4]
    b += arrow(0, 0, 0, 0, c, "red", True,
               path=f"M{x4+w4/2} 134C{x4+w4/2} 158 {x3+w3/2} 158 {x3+w3/2} 135")
    b += t((x3 + w3 / 2 + x4 + w4 / 2) / 2, 178, "degraded? roll back automatically", 16, c["red"], 500, anchor="middle")
    b += t(48, 220, "Preview: a Go operator I wrote", 18, c["muted"], 600)
    s, _ = row([("PR opened", "", "plain"), ("PreviewEnvironment", "custom resource (CRD)", "violet"),
                ("Go operator", "Kubebuilder reconcile", "violet"), ("Isolated namespace", "least-privilege RBAC", "plain"),
                ("PR closed", "finalizer cleanup", "plain")], 238, 68, c)
    b += s
    return frame(1280, 334, c, "Helios architecture",
                 "GitOps delivery from git push through GitHub Actions and ArgoCD to Argo Rollouts canaries analysed by Prometheus, "
                 "with automatic rollback; and a custom Go operator that turns a pull request into an isolated preview namespace.", b)


def dockhealer(c):
    b = t(48, 44, "The model proposes. Deterministic code decides.", 18, c["muted"], 600)
    s, bx = row([("Local LLM", "Ollama · proposes", "violet"), ("Validator", "16 rules", "plain"),
                 ("docker build", "real build", "plain"), ("Smoke test", "hardened container", "plain"),
                 ("Accepted", "evidence attached", "accent")], 62, 68, c)
    b += s
    (x0, w0), (x3, w3) = bx[0], bx[3]
    b += arrow(0, 0, 0, 0, c, "red", True,
               path=f"M{x3+w3/2} 134C{x3+w3/2} 172 {x0+w0/2} 172 {x0+w0/2} 135")
    b += t((x0 + w0 / 2 + x3 + w3 / 2) / 2, 194, "failed? classify (22 classes) · redact logs · fingerprint · bounded retry", 16, c["red"], 500, anchor="middle")
    b += node(48, 216, 560, 50, "Project-level fault → stop and hand off to a human", "", c, "gold")
    b += t(632, 247, "186 tests · injected fakes · Wilson 95% CIs · Terraform", 15, c["faint"], 400, MONO)
    return frame(1280, 292, c, "DockHealer architecture",
                 "A local LLM proposes a Dockerfile; a 16-rule validator, a real docker build and a hardened smoke test decide. "
                 "Failures are classified, redacted and fingerprinted for a bounded repair; project faults go to a human.", b)


def pollforge(c):
    b = t(48, 44, "Five services, three languages, one cluster", 18, c["muted"], 600)
    s, bx = row([("Browser", "vote", "plain"), ("Flask API", "Python", "plain"), ("Redis", "queue", "accent"),
                 ("Worker", ".NET / C#", "plain"), ("PostgreSQL", "StatefulSet", "plain"),
                 ("Results", "Node.js", "plain")], 62, 68, c)
    b += s
    (x0, w0), (x5, w5) = bx[0], bx[5]
    b += arrow(0, 0, 0, 0, c, "accent", True,
               path=f"M{x5+w5/2} 134C{x5+w5/2} 158 {x0+w0/2} 158 {x0+w0/2} 135")
    b += t((x0 + w0 / 2 + x5 + w5 / 2) / 2, 182, "Socket.IO pushes live results to every browser", 16, c["accent"], 500, anchor="middle")
    x = 48
    for label in ["Azure AKS", "ACR", "GitHub Actions + OIDC (no stored secrets)", "NGINX Ingress",
                  "cert-manager TLS", "Prometheus ServiceMonitor"]:
        sc, w = chip(x, 204, label, c, size=14, family=MONO)
        b += sc
        x += w + 10
    return frame(1280, 258, c, "PollForge architecture",
                 "Browser to Flask API to Redis queue to .NET worker to PostgreSQL, with a Node.js Socket.IO service pushing live "
                 "results; deployed to Azure AKS with ACR, OIDC GitHub Actions, NGINX ingress, cert-manager and Prometheus.", b)


def research(c):
    b = t(48, 44, "Recall on the target geological unit, before and after one training-bug fix", 18, c["muted"], 600)
    base, top, maxw = 270, 72, 860
    for i, (label, val, tone) in enumerate([("Before fix", 0.0, "red"), ("After fix", 76.6, "accent")]):
        y = top + i * 58
        b += t(48, y + 28, label, 19, c["text"], 600)
        b += f'<rect x="{base}" y="{y+6}" width="{maxw}" height="30" rx="6" fill="{c["panel"]}" stroke="{c["line"]}"/>'
        w = max(maxw * val / 100, 3)
        b += f'<rect x="{base}" y="{y+6}" width="{w:.0f}" height="30" rx="6" fill="{c[tone]}" fill-opacity=".85"/>'
        b += t(base + w + 12 if val < 80 else base + w - 12, y + 27, f"{val:g}%", 19, c[tone] if val < 80 else c["bg1"], 700,
               anchor="start" if val < 80 else "end")
    b += t(48, 220, "Then: 8 more pipeline bugs fixed · ground truth rebuilt from a public WFS · McNemar tests",
           15, c["faint"], 400, MONO)
    return frame(1280, 250, c, "UNSW research result: recall from 0% to 76.6%",
                 "Bar chart: recall on the target geological unit was 0% before a training-bug fix and 76.6% after.", b)


def portfolio(c):
    b = ""
    b += f'<rect x="48" y="36" width="1184" height="38" rx="8" fill="{c["panel"]}" stroke="{c["line"]}"/>'
    for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        b += f'<circle cx="{72+i*22}" cy="55" r="7" fill="{col}"/>'
    b += t(640, 61, "byte-kappa.vercel.app", 17, c["muted"], 500, MONO, "middle")
    b += t(64, 124, "ayush@portfolio:~$ ls ./work", 22, c["accent"], 500, MONO)
    x = 64
    for label in ["saka/", "helios/", "dockhealer/", "pollforge/", "som-gold/"]:
        sc, w = chip(x, 146, label, c, fg=c["text"], size=18, family=MONO)
        b += sc
        x += w + 12
    b += t(1216, 124, "Case studies, demos and résumé →", 24, c["text"], 600, anchor="end")
    b += t(1216, 170, "Open the portfolio", 18, c["muted"], 500, anchor="end")
    return frame(1280, 212, c, "Portfolio: byte-kappa.vercel.app",
                 "Link to Ayush's portfolio with case studies for SAKA, Helios, DockHealer, PollForge and SOM-Gold.", b)


ASSETS = {"hero": hero, "saka-header": saka_header, "saka-pipeline": saka_pipeline, "helios": helios,
          "dockhealer": dockhealer, "pollforge": pollforge, "research": research, "portfolio": portfolio}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in ASSETS.items():
        for theme, colors in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(colors), encoding="utf-8")
    print(f"wrote {len(ASSETS) * len(THEMES)} SVGs to {OUT}")
