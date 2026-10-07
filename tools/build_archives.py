"""Render the recording and writing archives as dependency-free HTML."""
import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content" / "archive.json").read_text(encoding="utf-8"))
NAV = [("index.html", "Main"), ("work.html", "Work"), ("podcast.html", "Podcast"),
       ("talks.html", "Talks"), ("interviews.html", "Interviews"), ("writing.html", "Writing")]


def link(url, label):
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def human_date(value):
    try:
        parsed = date.fromisoformat(value)
        return f"{parsed.day} {parsed.strftime('%B %Y')}"
    except ValueError:
        if len(value) == 7:
            return date.fromisoformat(value + "-01").strftime("%B %Y")
        return value


def page(filename, title, description, body):
    nav = '<span aria-hidden="true"> || </span>'.join(
        f'<a href="{url}"' + (' aria-current="page"' if url == filename else '') + f'>{label}</a>'
        for url, label in NAV
    )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} — Ádám Ficsór</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="canonical" href="https://adamficsor.com/{filename}">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header>
    <h1><a href="./">Ádám Ficsór</a></h1>
    <nav aria-label="Main navigation">{nav}</nav>
  </header>
  <main id="main">
{body}
  </main>
  <footer><p><a href="./">Main</a> · <a href="work.html">Work</a> · <a href="https://github.com/nopara73">GitHub</a> · <a href="https://nopara73.medium.com/">Medium</a></p></footer>
</body>
</html>
'''


def entries(items):
    return '<dl class="entries archive">\n' + '\n'.join(items) + '\n</dl>'


def entry(title, text, links="", element_id=""):
    ident = f' id="{escape(element_id)}"' if element_id else ''
    return f'<div{ident}><dt>{title}</dt><dd>{text}' + (f'<br>{links}' if links else '') + '</dd></div>'


def grouped(items, render):
    sections = []
    for year in sorted({item['date'][:4] for item in items}, reverse=True):
        rows = [render(item) for item in reversed(items) if item['date'].startswith(year)]
        sections.append(f'<section aria-labelledby="year-{year}"><h2 id="year-{year}">{year}</h2>{entries(rows)}</section>')
    return '\n'.join(sections)


def talk(item):
    title = escape(item['title'])
    label = human_date(item['date'])
    if item['date_basis'].startswith('Upload'):
        label = 'Published ' + label
    elif item['date_basis'].startswith('Conference year'):
        label += ' conference'
    elif item['date_basis'] == 'Event range':
        label = item['date_label']
    note = item.get('display_note', '')
    details = f'<span class="record-meta">{escape(label)}</span>'
    if note:
        details += '<br>' + escape(note)
    links = []
    if item.get('recording'):
        links.append(link(item['recording'], 'Excerpt' if item.get('excerpt') else 'Recording'))
    if item.get('slides'):
        links.append(link(item['slides'], 'Slides'))
    for source in item.get('evidence', []):
        links.append(link(source['url'], source['label']))
    return entry(title, details, ' · '.join(links))


def interview(item):
    label = human_date(item['date'])
    if item['date_basis'].startswith('Video publication'):
        label = 'Published ' + label
    elif item['date_basis'].startswith('Live broadcast'):
        label = 'Broadcast ' + label
    else:
        label = 'Released ' + label
    text = f'<span class="record-meta">{escape(item["publisher"])} · {escape(label)}</span>'
    if item.get('display_note'):
        text += '<br>' + escape(item['display_note'])
    links = []
    if item.get('source') and item['source'] != item['url']:
        label = 'Excerpt' if item['source'].startswith('https://www.youtube.com/') else 'Episode source'
        links.append(link(item['source'], label))
    return entry(link(item['url'], item['title']), text, ' · '.join(links))


talk_body = '''    <section aria-labelledby="talks">
      <h2 id="talks">Talks, panels, and demonstrations</h2>
      <p class="section-content">Recordings and material from my public presentations. Dates identify the event where known; otherwise they identify the recording’s publication.</p>
    </section>
''' + grouped(DATA['talks'], talk)

interview_body = '''    <section aria-labelledby="interviews">
      <h2 id="interviews">Interviews</h2>
      <p class="section-content">Conversations where I was the guest. For conversations I host, see <a href="podcast.html">Immortal Combat</a>.</p>
    </section>
''' + grouped(DATA['guest_interviews'], interview)

episodes = []
for item in reversed(DATA['selected_hosted_episodes']):
    episodes.append(entry(link(item['url'], item['guest']),
                          f'<span class="record-meta">Published {human_date(item["date"])}</span><br>{escape(item["title"])}'))
podcast_body = '''    <section aria-labelledby="podcast">
      <h2 id="podcast">Immortal Combat</h2>
      <div class="section-content">
        <p>I host Immortal Combat, a podcast about longevity. Since 2024, I’ve been talking with researchers, physicians, founders, and people working to extend healthy life.</p>
        <p><a href="https://www.youtube.com/playlist?list=PL4nqc85w185sO4i7eR3oUO_lMmlJ2K1cL">Browse the official episode playlist</a> or <a href="https://www.youtube.com/@nopara73">visit my YouTube channel</a>.</p>
      </div>
    </section>
    <section aria-labelledby="episodes">
      <h2 id="episodes">Selected conversations</h2>
''' + entries(episodes) + '\n    </section>'

writing_rows = []
for item in DATA['writings']:
    description = escape(item.get('description', ''))
    text = f'<span class="record-meta">{escape(item["date_label"])}</span>'
    if description:
        text += '<br>' + description
    writing_rows.append(entry(link(item['url'], item['title']), text))
writing_body = '''    <section aria-labelledby="writing">
      <h2 id="writing">Writing</h2>
      <p class="section-content">Essays, proposals, and technical explanations. My full article archive is on <a href="https://nopara73.medium.com/">Medium</a>.</p>
''' + entries(writing_rows) + '\n    </section>'

pages = {
    'talks.html': ('Talks', 'Public talks, panels, and demonstrations by Ádám Ficsór, with recordings and slides.', talk_body),
    'interviews.html': ('Interviews', 'Guest interviews with Ádám Ficsór on Bitcoin privacy and longevity.', interview_body),
    'podcast.html': ('Immortal Combat', 'Immortal Combat: a longevity podcast hosted by Ádám Ficsór. Selected conversations and the episode playlist.', podcast_body),
    'writing.html': ('Writing', 'Writing by Ádám Ficsór on Bitcoin privacy, longevity, games, and his past software work.', writing_body),
}
for filename, args in pages.items():
    (ROOT / 'site' / filename).write_text(page(filename, *args), encoding='utf-8', newline='\n')
print(f'Rendered {len(pages)} archives: {len(DATA["talks"])} talks, {len(DATA["guest_interviews"])} interviews, '
      f'{len(DATA["selected_hosted_episodes"])} hosted conversations, {len(DATA["writings"])} writings.')
