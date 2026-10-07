# Adam Ficsor's personal website

Plain HTML and CSS, published with GitHub Pages at https://adamficsor.com/.

## Editing

- `site/index.html`: biography, projects, publications, selected writing.
- `site/writing.html`: links to writing hosted elsewhere.
- `site/style.css`: layout and typography.
- `site/CNAME`: the canonical domain.

Push to `master` to publish. No build tools or runtime dependencies are required.
For a local preview, run `python -m http.server 8271 --bind 127.0.0.1 --directory site`.

## Hosting and domains

This project uses its own repository and custom domain. The account-level
`nopara73.github.io` repository retains no custom domain, so existing project
sites such as `/NomadicMethod/` retain their existing URLs and browser storage.

The two alternative domains, `nopara73.com` and `ficsoradam.com`, redirect to
`adamficsor.com`. Cloudflare handles DNS and those redirects on the Free plan.

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
