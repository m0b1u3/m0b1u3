"""Wrap the generated contribution animation in the bottom of the shared terminal."""
from pathlib import Path
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)


def render(animation):
    snake = ET.fromstring(animation)
    snake.set('x', '72')
    snake.set('y', '0')
    snake.set('width', '1056')
    snake.set('height', '230.4')
    nested = ET.tostring(snake, encoding='unicode')
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="280" viewBox="0 0 1200 280" role="img" aria-label="GitHub contribution snake animation">
<defs><pattern id="terminal-scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" fill-opacity=".28"/></pattern><filter id="terminal-glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><clipPath id="terminal-window"><path d="M0 0H1200V266Q1200 280 1186 280H14Q0 280 0 266Z"/></clipPath></defs>
<style>.terminal-cursor{animation:terminal-blink 1s steps(1) infinite}@keyframes terminal-blink{50%{opacity:0}}@media(prefers-reduced-motion:reduce){.terminal-cursor{animation:none}}</style>
<g clip-path="url(#terminal-window)"><rect width="1200" height="280" fill="#040806"/>
''' + nested + '''
<g font-family="'SF Mono','JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace" font-size="16" filter="url(#terminal-glow)"><text x="72" y="258" fill="#3DFF8F">m0b1u3@lab</text><text x="169" y="258" fill="#5F7F6C">:</text><text x="179" y="258" fill="#7FD4FF">~</text><text x="189" y="258" fill="#5F7F6C">$</text><rect class="terminal-cursor" x="211" y="243" width="10" height="18" fill="#3DFF8F"/></g>
<rect width="1200" height="280" fill="url(#terminal-scan)"/></g>
<path d="M.5 0V266Q.5 279.5 14 279.5H1186Q1199.5 279.5 1199.5 266V0" fill="none" stroke="#3DFF8F" stroke-opacity=".18"/>
</svg>'''


def main():
    output = Path('dist/terminal-footer.svg')
    source = Path('dist/github-contribution-grid-snake-dark.svg')
    output.write_text(render(source.read_text(encoding='utf-8')), encoding='utf-8')
    print(f'Generated {output}')


if __name__ == '__main__':
    main()
