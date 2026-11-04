# proofs-site

Static host for customer email proofs at https://proofs.mtdcnc.com (GitHub Pages, CNAME file in this folder).

Why: the Mailwizz share link lives on e-targetit.com, which sits on SURBL after big sends, so customer
gateways reject any email carrying it (YMT, 2026-11-04). Proofs must carry a clean mtdcnc.com URL.

How a proof gets here: pull the campaign HTML from Mailwizz read-only (mw_campaign_template.content),
replace the Mailwizz tags, strip plain HTML comments, add robots noindex, save as
proofs/YYYY-MM-DD-<client>-<topic>.html, then run publish_proof.cmd. Never put e-targetit.com links in.
