"""Отрисовка диаграмм модели CarKeeper средствами SysML v2 Pilot Implementation.

Скрипт собирает Jupyter-блокнот: в первых ячейках загружаются файлы модели
(*.sysml), далее — команды %viz для нужных элементов. Блокнот выполняется
ядром SysML (jupyter nbconvert --execute), SVG из результатов %viz
сохраняются в srs/sysml/viz/, а затем переводятся в PNG (srs/img/) через
headless Chrome.

Нужно: окружение с пакетом jupyter-sysml-kernel (conda-forge) и Graphviz.
Запуск:  ~/sysml-env/bin/python render_viz.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SYSML = os.path.dirname(HERE)
IMG = os.path.join(os.path.dirname(SYSML), 'img')
ENV = os.path.expanduser('~/sysml-env/bin')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

MODEL_FILES = ['carkeeper.sysml', 'carkeeper-domain.sysml', 'carkeeper-ui.sysml']

# имя PNG -> команда %viz
DIAGRAMS = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'diagrams.json'), encoding='utf-8'))
IMG = sys.argv[2] if len(sys.argv) > 2 else IMG


def build_notebook(path):
    cells = []
    for f in MODEL_FILES:
        src = open(os.path.join(SYSML, f), encoding='utf-8').read()
        cells.append(src)
    for name, cmd in DIAGRAMS.items():
        cells.append(cmd)
    nb = {
        'nbformat': 4, 'nbformat_minor': 5,
        'metadata': {'kernelspec': {'name': 'sysml', 'display_name': 'SysML', 'language': 'sysml'}},
        'cells': [{'cell_type': 'code', 'metadata': {}, 'execution_count': None,
                   'outputs': [], 'source': c, 'id': f'c{i}'} for i, c in enumerate(cells)],
    }
    json.dump(nb, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def main():
    nb_path = os.path.join(HERE, 'carkeeper-viz.ipynb')
    build_notebook(nb_path)
    subprocess.run([os.path.join(ENV, 'jupyter'), 'nbconvert', '--to', 'notebook', '--execute',
                    '--inplace', '--ExecutePreprocessor.timeout=300', nb_path], check=True)
    nb = json.load(open(nb_path, encoding='utf-8'))
    n_model = len(MODEL_FILES)
    for i, f in enumerate(MODEL_FILES):
        for out in nb['cells'][i]['outputs']:
            text = out.get('text') or ''.join(out.get('data', {}).get('text/plain', ''))
            print(f, '->', ''.join(text)[:300].strip())
    for (name, cmd), cell in zip(DIAGRAMS.items(), nb['cells'][n_model:]):
        svg = None
        for out in cell['outputs']:
            data = out.get('data', {})
            if 'image/svg+xml' in data:
                svg = ''.join(data['image/svg+xml'])
            elif out.get('output_type') in ('stream', 'error'):
                print(name, 'сообщение:', ''.join(out.get('text', '')) or out.get('evalue'))
        if not svg:
            print(name, ': SVG не получен'); continue
        svg_path = os.path.join(HERE, name + '.svg')
        open(svg_path, 'w', encoding='utf-8').write(svg)
        to_png(svg_path, os.path.join(IMG, name + '.png'))
        print(name, ': ok')


def to_png(svg_path, png_path, scale=2):
    import re
    svg = open(svg_path, encoding='utf-8').read()
    m = re.search(r'width="(\d+)(?:px)?"\s+[^>]*?height="(\d+)(?:px)?"', svg) or \
        re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', svg)
    w, h = int(float(m.group(1))), int(float(m.group(2)))
    html_path = svg_path[:-4] + '.html'
    open(html_path, 'w', encoding='utf-8').write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;background:#fff}}</style></head>'
        f'<body>{svg}</body></html>')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                    f'--force-device-scale-factor={scale}', f'--window-size={w},{h}',
                    f'--screenshot={png_path}', 'file://' + html_path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.remove(html_path)


if __name__ == '__main__':
    main()
