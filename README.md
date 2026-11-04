# proofs-site

Static host for customer email proofs at https://proofs.mtdcnc.com (GitHub Pages, CNAME file in this folder).

Why: the Mailwizz share link lives on e-targetit.com, which sits on SURBL after big sends, so customer
gateways reject any email carrying it (YMT, 2026-11-04). Proofs must carry a clean mtdcnc.com URL.

How a proof gets here: `python build_proof.py <campaign_id> <client> [topic]` pulls the campaign
HTML from Mailwizz read-only (mw_campaign_template.content), replaces the Mailwizz tags, removes
plain HTML comments while preserving every Outlook conditional token, adds robots noindex, refuses
to write if anything e-targetit.com or any merge tag survives, and saves
proofs/YYYY-MM-DD-<client>-<topic>.html. Then run publish_proof.cmd (commit + push).
Lesson 2026-11-04: a naive comment stripper ate the `<!--[if !mso]><!-->` fallback buttons; the
script now checks that conditional tokens and tag counts match the raw template.
