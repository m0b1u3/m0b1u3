"""Create one continuous profile SVG while leaving assets/terminal.svg untouched."""
from pathlib import Path
import hashlib
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
H = 1288


def tag(name, **attrs):
    return ET.Element(f'{{{NS}}}{name}', {k: str(v) for k, v in attrs.items()})


def render(original, animation):
    root = ET.fromstring(original)
    root.set('height', str(H))
    root.set('viewBox', f'0 0 1200 {H}')
    root.set('aria-label', 'm0b1u3 security researcher profile, website, lab and contribution animation')
    frame = next(n for n in root if n.tag == f'{{{NS}}}g' and n.get('clip-path') == 'url(#win)')
    clip = next(n for n in root.iter() if n.get('id') == 'win')
    for node in clip:
        if node.tag == f'{{{NS}}}rect':
            node.set('height', str(H))
    # Extend only the generated canvas, shared overlays and border.
    for node in frame:
        if node.tag == f'{{{NS}}}rect' and node.get('height') == '780':
            node.set('height', str(H))
    for node in root:
        if node.tag == f'{{{NS}}}rect' and node.get('height') == '779':
            node.set('height', str(H - 1))
    lower = tag('g', id='profile-links')

    def text(parent, x, y, value, fill='#B6F5CF', size=16):
        node = tag('text', x=x, y=y, fill=fill, filter='url(#glow)', style=f'font-size:{size}px')
        node.text = value
        parent.append(node)
        return node

    def prompt(y, command, parent=lower):
        text(parent, 72, y, 'm0b1u3@lab', '#3DFF8F')
        text(parent, 169, y, ':', '#5F7F6C')
        text(parent, 179, y, '~', '#7FD4FF')
        text(parent, 189, y, '$', '#5F7F6C')
        text(parent, 211, y, command)

    prompt(788, 'ls ~/links')
    link = tag('a', href='https://pwned.icu', target='_top')
    text(link, 72, 830, '$ open pwned.icu', '#3DFF8F')
    text(link, 1000, 830, '[ OPEN SITE ]', '#3DFF8F')
    lower.append(link)
    prompt(886, './redteam --interactive')
    text(lower, 72, 920, '3 scenarios  //  defense OFF / ON  //  capture the flag', '#8FBFA2', 14)
    prompt(974, './contributions --snake --last-year')
    snake = ET.fromstring(animation)
    snake.set('x', '72')
    snake.set('y', '986')
    snake.set('width', '1056')
    snake.set('height', '230.4')
    lower.append(snake)
    prompt(1258, '')
    cursor = tag('rect', x=211, y=1243, width=10, height=18, fill='#3DFF8F', filter='url(#glow)')
    cursor.set('class', 'cur')
    lower.append(cursor)
    # Reuse the original full-window scanlines and vignette over both parts.
    overlay_index = next(i for i, n in enumerate(frame) if n.get('fill') == 'url(#scan)')
    frame.insert(overlay_index, lower)
    return ET.tostring(root, encoding='unicode') + '\n'


def main():
    source = Path('assets/terminal.svg')
    original = source.read_bytes()
    digest = hashlib.sha256(original).digest()
    animation = Path('dist/github-contribution-grid-snake-dark.svg').read_text(encoding='utf-8')
    output = Path('dist/profile-combined.svg')
    output.write_text(render(original.decode('utf-8'), animation), encoding='utf-8')
    assert hashlib.sha256(source.read_bytes()).digest() == digest
    print(f'Generated {output}; original terminal.svg unchanged')


if __name__ == '__main__':
    main()
