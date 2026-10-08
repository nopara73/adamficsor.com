"""Render the recording and writing archives as dependency-free HTML."""
import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content" / "archive.json").read_text(encoding="utf-8"))
WORK = json.loads((ROOT / "content" / "work.json").read_text(encoding="utf-8"))
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
    display_title = item.get('display_title', item['title'])
    title = link(item['recording'], display_title) if item.get('recording') else escape(display_title)
    label = human_date(item['date'])
    if item['date_basis'].startswith('Upload'):
        label = 'Published ' + label
    elif item['date_basis'].startswith('Conference year'):
        label += ' conference'
    elif item['date_basis'] == 'Event range':
        label = item['date_label']
    note = item.get('display_note', '')
    if item.get('event'):
        label = item['event'] + ' · ' + label
    details = f'<span class="record-meta">{escape(label)}</span>'
    if note:
        details += '<br>' + escape(note)
    links = []
    if item.get('slides'):
        links.append(link(item['slides'], 'Slides'))
    for source in item.get('evidence', []):
        links.append(link(source['url'], source['label']))
    return entry(title, details, ' · '.join(links))


def interview(item):
    label = human_date(item['date'])
    if item['date_basis'].startswith('Video publication'):
        label = 'Published ' + label
    elif item['date_basis'] == 'Original interview article':
        label = 'Published ' + label
    elif item['date_basis'].startswith('Live broadcast'):
        label = 'Broadcast ' + label
    else:
        label = 'Released ' + label
    publisher = item.get('display_publisher', item['publisher'])
    text = f'<span class="record-meta">{escape(publisher)} · {escape(label)}</span>'
    if item.get('display_note'):
        text += '<br>' + escape(item['display_note'])
    links = []
    if item.get('source') and item['source'] != item['url']:
        label = item.get('source_label', 'Excerpt' if item['source'].startswith('https://www.youtube.com/') else 'Episode page')
        links.append(link(item['source'], label))
    return entry(link(item['url'], item.get('display_title', item['title'])), text, ' · '.join(links))


talk_body = '''    <section aria-labelledby="talks">
      <h2 id="talks">Talks, panels, and demonstrations</h2>
    </section>
''' + grouped(DATA['talks'], talk)

interview_body = '''    <section aria-labelledby="interviews">
      <h2 id="interviews">Interviews</h2>
      <p class="section-content">Conversations where I’m the guest. See also the <a href="podcast.html">podcasts I host</a>.</p>
    </section>
''' + grouped(DATA['guest_interviews'], interview)

episodes = []
for item in DATA['selected_hosted_episodes']:
    episodes.append(entry(link(item['url'], item['guest']),
                          f'<span class="record-meta">Published {human_date(item["date"])}</span><br>{escape(item.get("description", item["title"]))}'))
podcast_body = '''    <section aria-labelledby="podcast">
      <h2 id="podcast">Immortal Combat</h2>
      <div class="section-content">
        <p>I’ve hosted this podcast about longevity since 2024.</p>
        <p><a href="https://www.youtube.com/playlist?list=PL4nqc85w185sO4i7eR3oUO_lMmlJ2K1cL">All episodes</a> · <a href="https://www.youtube.com/@nopara73">My YouTube channel</a></p>
      </div>
    </section>
    <section aria-labelledby="episodes">
      <h2 id="episodes">Three conversations to start with</h2>
''' + entries(episodes[:3]) + '''
    </section>
    <section aria-labelledby="more-episodes">
      <h2 id="more-episodes">More episodes</h2>
''' + entries(episodes[3:]) + '\n    </section>'

value_rows = [entry(link(item['url'], item['guest']),
                    f'<span class="record-meta">Published {human_date(item["date"])}</span>' +
                    ('<br>' + escape(item['description']) if item['description'] else ''))
              for item in DATA['value_series']]
podcast_body += '''
    <section aria-labelledby="pursuit-of-value">
      <h2 id="pursuit-of-value">Pursuit of Value with Derek Mazzone</h2>
      <div class="section-content">
        <p>In 2023, I recorded eight conversations with Derek Mazzone about his book <i>The Pursuit of Value: A Philosophy of Loss and Equanimity</i>.</p>
        <p><a href="https://www.youtube.com/playlist?list=PL4nqc85w185uz_WBVDXMyZBCGbe8BUgdJ">Full series</a></p>
      </div>
''' + entries(value_rows) + '\n    </section>'

other_rows = [entry(link(item['url'], item.get('display_guest', item['guest'])),
                    f'<span class="record-meta">Published {human_date(item["date"])}</span><br>{escape(item["description"])}')
              for item in DATA['other_conversations']]
block_rows = [entry(link(item['url'], item['guest']), escape(item['description']),
                    link(item['example_recording'], 'Example episode (2019)'), item.get('id', ''))
              for item in DATA['cohosted_podcasts']]
podcast_body += '<section aria-labelledby="other-conversations"><h2 id="other-conversations">Other podcasts and conversations</h2>' + entries(other_rows + block_rows) + '</section>'

early_rows = [entry(link(item['url'], item['title']),
                   f'<span class="record-meta">Published {human_date(item["date"])} · {escape(item["language"])}</span><br>' +
                   escape(item['description']), element_id=item['id'])
              for item in DATA['early_videos']]

def writing(item):
    description = escape(item.get('description', ''))
    text = f'<span class="record-meta">{escape(item["date_label"])}</span>'
    if description:
        text += '<br>' + description
    links = ' · '.join(link(source['url'], source['label']) for source in item.get('extra_links', []))
    return entry(link(item['url'], item['title']), text, links, item.get('id', ''))


writing_body = '''    <section aria-labelledby="writing">
      <h2 id="writing">Writing</h2>
      <p class="section-content">More of my writing is on <a href="https://nopara73.medium.com/">Medium</a>.</p>
    </section>
'''
for category, title in [('longevity', 'Longevity'), ('bitcoin', 'Bitcoin privacy'),
                        ('value', 'Value'), ('software', 'Software')]:
    rows = [writing(item) for item in DATA['writings'] if item['category'] == category]
    writing_body += f'<section aria-labelledby="{category}"><h2 id="{category}">{title}</h2>' + entries(rows) + '</section>\n'

work_sections = []
for section in WORK['sections']:
    rows = [entry(link(item['url'], item['title']) if item.get('url') else escape(item['title']),
                  escape(item['description']),
                  ' · '.join(link(source['url'], source['label']) for source in item.get('links', [])),
                  item.get('id', '')) for item in section['entries']]
    body = ('<p class="section-content">' + escape(section['description']) + '</p>' if section.get('description') else '') + entries(rows)
    if section.get('after'):
        after = section['after']
        body += '<p class="section-content">' + escape(after.get('prefix', '')) + link(after['url'], after['label']) + escape(after.get('suffix', '')) + '</p>'
    work_sections.append(f'<section aria-labelledby="{section["id"]}"><h2 id="{section["id"]}">{escape(section["title"])}</h2>{body}</section>')
work_body = '\n'.join(work_sections)
work_body += '\n<section aria-labelledby="early-videos"><h2 id="early-videos">My first video</h2>' + entries(early_rows) + '</section>'

pages = {
    'work.html': ('Work and research', 'Work and research by Ádám Ficsór: Longevity World Cup, Immortal Combat, zkSNACKs, Wasabi Wallet, ZeroLink, WabiSabi, and TumbleBit.', work_body),
    'talks.html': ('Talks', 'Public talks, panels, and demonstrations by Ádám Ficsór, with recordings and slides.', talk_body),
    'interviews.html': ('Interviews', 'Guest interviews with Ádám Ficsór on Bitcoin privacy and longevity.', interview_body),
    'podcast.html': ('Podcasts and conversations', 'Podcasts and conversations with Ádám Ficsór: Immortal Combat, Pursuit of Value, Bitcoin privacy conversations, and Block Digest.', podcast_body),
    'writing.html': ('Writing', 'Writing by Ádám Ficsór on Bitcoin privacy, longevity, games, and his past software work.', writing_body),
}
for filename, args in pages.items():
    (ROOT / 'site' / filename).write_text(page(filename, *args), encoding='utf-8', newline='\n')
print(f'Rendered {len(pages)} archives: {len(DATA["talks"])} talks, {len(DATA["guest_interviews"])} interviews, '
      f'{len(DATA["selected_hosted_episodes"])} hosted conversations, {len(DATA["writings"])} writings.')
