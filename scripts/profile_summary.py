"""Build the profile's SVG summary from public GitHub data (Python stdlib only)."""
import html
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request

OWNER = os.environ.get('PROFILE_OWNER', 'm0b1u3')
API = 'https://api.github.com'


def api(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-summary'}
    token = os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    request = urllib.request.Request(API + path, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def starred_count(owner):
    total = 0
    page = 1
    while True:
        batch = api(f'/users/{owner}/starred?per_page=100&page={page}')
        total += len(batch)
        if len(batch) < 100:
            return total
        page += 1


def render(user, starred, languages):
    def text(x, y, value, size=16, color='#B6F5CF'):
        return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">'
                f'{html.escape(str(value))}</text>')
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="204" '
             'viewBox="0 0 1200 204" role="img" aria-label="GitHub profile summary and selected repository languages">',
             '<style>text{font-family:Menlo,Consolas,monospace}</style>']
    for x, width in [(1, 583), (609, 590)]:
        parts.append(f'<rect x="{x}" y="1" width="{width}" height="202" rx="12" fill="#040806" stroke="#143322"/>')
    parts += [text(28, 38, '$ gh profile --summary', 17, '#3DFF8F'),
              text(636, 38, '$ ls pinned/ --languages', 17, '#3DFF8F')]
    for x, y, value, label in [(28, 95, user['public_repos'], 'repositories'),
                                (298, 95, user['followers'], 'followers'),
                                (28, 162, user['following'], 'following'),
                                (298, 162, starred, 'starred')]:
        parts += [text(x, y, value, 24), text(x + 75, y, label, 13, '#8BB39A')]
    colors = {'TypeScript': '#3178c6', 'JavaScript': '#f1e05a', 'Python': '#3572a5', 'Java': '#b07219'}
    for i, language in enumerate(languages[:4]):
        x, y = 636 + (i % 2) * 287, 95 + (i // 2) * 67
        parts += [f'<circle cx="{x+5}" cy="{y-5}" r="5" fill="{colors.get(language, "#8BB39A")}"/>',
                  text(x + 22, y, language, 15)]
    parts.append('</svg>\n')
    return ''.join(parts)


def main():
    owner = urllib.parse.quote(OWNER, safe='')
    user = api(f'/users/{owner}')
    starred = starred_count(owner)
    languages = []
    for repository in ['NotitleCode', 'AssetProbe', 'Gophish-mcp', 'JavaMemHunter']:
        language = api(f'/repos/{owner}/{repository}').get('language')
        if language and language not in languages:
            languages.append(language)
    output = Path('dist/profile-summary.svg')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(user, starred, languages), encoding='utf-8')
    print(f'Generated {output}')


if __name__ == '__main__':
    main()
