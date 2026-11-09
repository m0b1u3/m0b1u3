"""Create one continuous profile SVG while leaving assets/terminal.svg untouched."""
from pathlib import Path
import hashlib
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
H = 1236


def tag(name, **attrs):
    return ET.Element(f'{{{NS}}}{name}', {k: str(v) for k, v in attrs.items()})


def render(original, animation):
    # Change the accent only in the generated copy, preserving the source SVG.
    root = ET.fromstring(original.replace('#FFB347', '#FF79C6'))
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
    # The original trailing prompt is replaced by the next command in this
    # generated copy. The source artwork on disk is never changed.
    removed = 0
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag == f'{{{NS}}}g' and any(
                n.tag == f'{{{NS}}}text' and n.get('y') == '736'
                for n in child
            ):
                parent.remove(child)
                removed += 1
    assert removed == 1, 'Expected exactly one original trailing prompt'
    lower = tag('g', id='profile-links')
    lower.set('class', 'flick')
    defs = next(n for n in root if n.tag == f'{{{NS}}}defs')
    extra_style = tag('style')
    extra_style.text = """
.profile-graph-reveal{transform:scaleY(0);transform-origin:0 0;animation:profile-graph-in .7s steps(7,end) 12.45s forwards,profile-graph-open .01s linear 13.20s forwards}
@keyframes profile-graph-in{to{transform:scaleY(1)}}
@keyframes profile-graph-open{from,to{transform:scaleY(1)}}
#profile-snake *{animation-delay:12.45s!important}
@media(prefers-reduced-motion:reduce){.profile-graph-reveal{animation:none!important;transform:scaleY(1)!important}#profile-snake *{animation:none!important}}
"""
    defs.append(extra_style)
    reveal = tag('clipPath', id='profile-graph-clip', clipPathUnits='userSpaceOnUse')
    reveal_rect = tag('rect', x=0, y=0, width=1056, height=230.4)
    reveal_rect.set('class', 'profile-graph-reveal')
    reveal.append(reveal_rect)
    defs.append(reveal)

    def stage(parent, delay):
        node = tag('g', style=f'animation-delay:{delay:.2f}s')
        node.set('class', 'in')
        parent.append(node)
        return node

    def text(parent, x, y, value, fill='#B6F5CF', size=16):
        node = tag('text', x=x, y=y, fill=fill, filter='url(#glow)', style=f'font-size:{size}px')
        node.text = value
        parent.append(node)
        return node

    def typing(parent, x, y, command, start, duration):
        width = len(command) * 9.6
        cover = tag('rect', x=x, y=y-17, width=f'{width+12:.1f}', height=24, fill='#040806')
        cover.set('class', 'cov')
        cover.set('style', f'--d:{duration:.2f}s;--n:{len(command)};--w:{width:.1f}px;--t:{start:.2f}s')
        parent.append(cover)

    def prompt(y, command, parent, delay=None, duration=None):
        node = stage(parent, delay) if delay is not None else parent
        text(node, 72, y, 'm0b1u3@lab', '#3DFF8F')
        text(node, 169, y, ':', '#5F7F6C')
        text(node, 179, y, '~', '#7FD4FF')
        text(node, 189, y, '$', '#5F7F6C')
        text(node, 211, y, command)
        if duration is not None:
            typing(node, 211, y, command, delay + .12, duration)
        return node

    prompt(736, 'ls ~/links', lower, delay=7.42, duration=.45)
    link = tag('a', href='https://pwned.icu', target='_top')
    website = stage(link, 8.12)
    text(website, 72, 778, '$ open pwned.icu', '#3DFF8F')
    typing(website, 72, 778, '$ open pwned.icu', 8.24, .65)
    text(stage(link, 9.00), 1000, 778, '[ OPEN SITE ]', '#3DFF8F')
    lower.append(link)
    prompt(834, './redteam --interactive', lower, delay=9.08, duration=1.05)
    text(stage(lower, 10.48), 72, 868, '3 scenarios  //  defense OFF / ON  //  capture the flag', '#8FBFA2', 14)
    prompt(922, './contributions --snake --last-year', lower, delay=10.86, duration=1.25)
    graph_stage = stage(lower, 12.45)
    translated = tag('g', transform='translate(72,934)')
    clipped = tag('g')
    clipped.set('clip-path', 'url(#profile-graph-clip)')
    snake = ET.fromstring(animation)
    snake.set('id', 'profile-snake')
    snake.set('x', '0')
    snake.set('y', '0')
    snake.set('width', '1056')
    snake.set('height', '230.4')
    clipped.append(snake)
    translated.append(clipped)
    graph_stage.append(translated)
    final_prompt = prompt(1206, '', lower, delay=13.45)
    cursor = tag('rect', x=211, y=1191, width=10, height=18, fill='#3DFF8F', filter='url(#glow)')
    cursor.set('class', 'cur')
    final_prompt.append(cursor)
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
    combined = render(original.decode('utf-8'), animation)
    output.write_text(combined, encoding='utf-8')
    output.with_name('profile-sequence.svg').write_text(combined, encoding='utf-8')
    output.with_name('profile-sequence-pink.svg').write_text(combined, encoding='utf-8')
    assert hashlib.sha256(source.read_bytes()).digest() == digest
    print(f'Generated {output}; original terminal.svg unchanged')


if __name__ == '__main__':
    main()
