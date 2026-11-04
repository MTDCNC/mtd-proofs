r"""Build a customer proof page from a Mailwizz campaign (read-only) for proofs.mtdcnc.com.

Usage:  python build_proof.py <campaign_id> <client-slug> [topic-slug]
Writes: proofs/YYYY-MM-DD-<client>[-<topic>].html and staging/<id>-raw.html

Rules: the stored template never contains e-targetit.com (Mailwizz adds tracking at send time);
Mailwizz merge tags are replaced; ONLY plain HTML comments are removed, every Outlook conditional
token (<!--[if ...]>, <!-->, <!--<![endif]-->, <![endif]-->) is preserved byte for byte
(2026-11-04: a naive stripper swallowed the non-Outlook buttons, Jof caught it); robots noindex.
The script refuses to write if any e-targetit.com reference or merge tag survives, or if the
conditional-token counts differ from the raw template.
"""
import os, re, sys, datetime
sys.path.insert(0, r"Y:\MTD-Client-Files\Mailwizz-DB-Connection")
import mwq

HERE = os.path.dirname(os.path.abspath(__file__))
COND = re.compile(r"<!--\s*\[if[^\]]*\]>(?:<!-->)?|<!-->|<!--<!\[endif\]-->|<!\[endif\]-->")

def strip_plain_comments(h):
    keep = {}
    def hold(m):
        k = f"\x00{len(keep)}\x00"; keep[k] = m.group(0); return k
    h = COND.sub(hold, h)
    h = re.sub(r"<!--[\s\S]*?-->", "", h)
    for k, v in keep.items(): h = h.replace(k, v)
    return h

def build(cid, client, topic=None, campaign_name=None):
    cols, rows = mwq.query("SELECT t.content, c.name FROM mw_campaign_template t JOIN mw_campaign c ON c.campaign_id=t.campaign_id WHERE t.campaign_id=%s", (cid,))
    if not rows: sys.exit(f"campaign {cid} not found")
    raw, name = rows[0]
    os.makedirs(os.path.join(HERE, "staging"), exist_ok=True)
    open(os.path.join(HERE, "staging", f"{cid}-raw.html"), "w", encoding="utf-8").write(raw)
    h = raw
    h = h.replace("[UNSUBSCRIBE_URL]", "#").replace("[EMAIL]", "").replace("[SUBSCRIBER_UID]", "proof")
    h = h.replace("[CAMPAIGN_NAME]", campaign_name or name).replace("[CURRENT_DATE]", datetime.date.today().strftime("%d/%m/%Y"))
    h = strip_plain_comments(h)
    meta = '<meta name="robots" content="noindex,nofollow">'
    h = re.sub(r"(<head[^>]*>)", lambda m: m.group(1) + meta, h, count=1, flags=re.I) if re.search(r"<head[^>]*>", h, re.I) else meta + h
    # guards
    assert "e-targetit" not in h.lower(), "e-targetit.com reference present"
    left = re.findall(r"\[[A-Z_]+\]", h); assert not left, f"merge tags left: {left}"
    assert COND.findall(h) == COND.findall(raw), "Outlook conditional tokens changed"
    for tag in ("v:roundrect", "v:textbox", "v:rect", "table", "td", "a"):
        assert h.count(f"<{tag}") == raw.count(f"<{tag}"), f"<{tag}> count changed"
    slug = f"{datetime.date.today():%Y-%m-%d}-{client}" + (f"-{topic}" if topic else "")
    out = os.path.join(HERE, "proofs", slug + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(h)
    print(f"written {out} ({len(h)} chars) from campaign {cid} '{name}'")
    print(f"https://proofs.mtdcnc.com/proofs/{slug}.html")
    return out

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    build(int(sys.argv[1]), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
