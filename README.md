# Adam Ficsor's personal website

Plain HTML and CSS, published with GitHub Pages at https://adamficsor.com/.

## Editing

- `site/index.html`: concise biography and selected work.
- `site/work.html`: company building, projects, publications, and research contributions.
- `content/archive.json`: curated talks, guest interviews, hosted conversations, and writing.
- `tools/build_archives.py`: renders the four archive pages using Python's standard library.
- `site/podcast.html`, `site/talks.html`, `site/interviews.html`, `site/writing.html`: generated archives.
- `site/style.css`: layout and typography.
- `site/CNAME`: the canonical domain.

After changing the archive data, run `python tools/build_archives.py` and include
the generated pages in the commit. Push to `master` to publish. The Pages workflow
also renders the archives before uploading. No third-party build or runtime
dependencies are required.
For a local preview, run `python -m http.server 8271 --bind 127.0.0.1 --directory site`.

## Hosting and domains

This project uses its own repository and custom domain. The account-level
`nopara73.github.io` repository retains no custom domain, so existing project
sites such as `/NomadicMethod/` retain their existing URLs and browser storage.

The two alternative domains, `nopara73.com` and `ficsoradam.com`, redirect to
`adamficsor.com`. Cloudflare handles DNS and those redirects on the Free plan.
The apex uses GitHub Pages directly with HTTPS enforced. Cloudflare redirects
`www.adamficsor.com` to the apex, preserving the path and query string.

## Content references

The design is inspired by the simplicity of https://www.ethanheilman.com/.
All copy is original; no biography or article content was copied from that site.

- https://github.com/nopara73
- https://github.com/nopara73/LongevityWorldCup
- https://github.com/nopara73/ZeroLink
- https://eprint.iacr.org/2021/206
- https://nopara73.medium.com/
- https://nopara73.medium.com/goodbye-wasabi-c8116c88fb8c
- https://github.com/nopara73/ScamouraiWallet/blob/master/POST_MORTEM.md
- https://github.com/ProgrammingBlockchain/ProgrammingBlockchain/blob/master/cover.md
- https://github.com/nopara73/LongevityWorldCup/blob/master/LongevityWorldCup.Documentation/About.md

Ádám created Wasabi Wallet and ZeroLink. Preserve that distinction when editing
the biography; a historical contributor list is not a list of co-creators.
He no longer identifies as a software developer. Nomadic Method is a minor side
project, not a main project alongside Wasabi and Longevity World Cup.

There are no analytics, cookies, remote fonts, or third-party scripts.

The October 2026 update applies the completed primary-source research inventory.
Archive dates distinguish event dates from release or upload dates. Preserve
the Advancing Bitcoin excerpt label and do not invent missing slides or dates.
The fuller work page links the evidence for each contribution.

Keep Longevity World Cup and Immortal Combat prominent as current work. The
introduction ends with “Thanks for coming to my TED talk.” Forbes recognition
is the Hungary 2020 list. WabiSabi's preprint and journal article are one work.
TumbleBit and ShareLock acknowledgments do not imply paper co-authorship.
P2EP followed group discussion; BIP78 is Nicolas Dorier's proposal. Do not
present the biological-age clock experiments as validated clinical results.
