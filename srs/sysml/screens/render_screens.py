"""Структурные диаграммы экранов CarKeeper (SysML v2 Pilot Implementation, %viz).

Модель carkeeper-screens.sysml загружается в ядро SysML (Jupyter), для каждого
пакета выполняется %viz --view=tree; полученный PlantUML-код ядра переводится
в SVG тем же PlantUML из ядра, затем SVG сохраняется в PNG (srs/img/screen-*.png).
Запуск: python3 render_screens.py
"""
import glob, json, os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.normpath(os.path.join(HERE, '..', '..', 'img'))
ENV = os.path.expanduser('~/sysml-env')
JAR = glob.glob(os.path.join(ENV, 'share/jupyter/kernels/sysml/*.jar'))[0]
JAVA = os.path.join(ENV, 'lib/jvm/bin/java')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
MEASURE_FONT, DISPLAY_FONT, SCALE = 'DejaVu Sans', 'Arial', 3

PACKAGES = {
    'screen-dashboard': 'CarKeeper_Dashboard',
    'screen-plan': 'CarKeeper_Plan',
    'screen-record': 'CarKeeper_Record',
    'screen-expenses': 'CarKeeper_Expenses',
    'screen-regulations': 'CarKeeper_Regulations',
}

model = open(os.path.join(HERE, 'carkeeper-screens.sysml'), encoding='utf-8').read()
cells = [model] + [f'%viz --view=tree --style=ORTHOLINE --style=PUMLCODE {p}' for p in PACKAGES.values()]
nb = {'nbformat': 4, 'nbformat_minor': 5,
      'metadata': {'kernelspec': {'name': 'sysml', 'display_name': 'SysML', 'language': 'sysml'}},
      'cells': [{'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [],
                 'source': c, 'id': f'c{i}'} for i, c in enumerate(cells)]}
nb_path = os.path.join(HERE, 'carkeeper-screens.ipynb')
json.dump(nb, open(nb_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
env = dict(os.environ, PATH=os.path.join(ENV, 'bin') + ':' + os.environ['PATH'])
subprocess.run([os.path.join(ENV, 'bin/jupyter'), 'nbconvert', '--to', 'notebook', '--execute', '--inplace',
                '--ExecutePreprocessor.timeout=300', nb_path], check=True, env=env)
nb = json.load(open(nb_path, encoding='utf-8'))


def text_of(cell):
    out = []
    for o in cell['outputs']:
        out.append(''.join(o.get('text', '')) + ''.join(o.get('data', {}).get('text/plain', '')))
    return ''.join(out)


print('model:', text_of(nb['cells'][0]).strip()[:300])
for (name, pkg), cell in zip(PACKAGES.items(), nb['cells'][1:]):
    txt = text_of(cell)
    m = re.search(r'@startuml.*?@enduml', txt, re.S)
    assert m, f'{pkg}: нет PlantUML\n{txt[:500]}'
    puml = m.group(0).replace('skin sysmlbw', f'skin sysmlbw\n<style>\nroot {{\n  FontName {MEASURE_FONT}\n}}\n</style>', 1)
    pp = os.path.join(HERE, name + '.puml')
    open(pp, 'w', encoding='utf-8').write(puml)
    subprocess.run([JAVA, '-Djava.awt.headless=true', '-cp', JAR, 'net.sourceforge.plantuml.Run',
                    '-tsvg', '-charset', 'UTF-8', pp], check=True,
                   env=dict(env, GRAPHVIZ_DOT=os.path.join(ENV, 'bin/dot')))
    svg = open(os.path.join(HERE, name + '.svg'), encoding='utf-8').read()
    w = int(float(re.search(r'width:(\d+(?:\.\d+)?)px', svg).group(1)))
    h = int(float(re.search(r'height:(\d+(?:\.\d+)?)px', svg).group(1)))
    with tempfile.TemporaryDirectory() as td:
        html = os.path.join(td, 'd.html')
        open(html, 'w', encoding='utf-8').write(
            '<html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}'
            f'text{{font-family:"{DISPLAY_FONT}",sans-serif !important}}</style></head><body>{svg[svg.index("<svg"):]}</body></html>')
        png = os.path.join(IMG, name + '.png')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        f'--force-device-scale-factor={SCALE}', f'--window-size={w},{h}',
                        f'--user-data-dir={td}/prof', f'--screenshot={png}', 'file://' + html],
                       check=True, capture_output=True)
    print(name, w * SCALE, 'x', h * SCALE)
