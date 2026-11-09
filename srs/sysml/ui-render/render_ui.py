"""Генерация мокапов экранов CarKeeper из модели SysML v2 (carkeeper-ui.sysml).

Скрипт разбирает текстовую нотацию SysML v2 (part def / part / attribute),
находит определения экранов (part def ...Screen :> Screen) и рисует для каждого
цветной макет экрана. Порядок частей в модели задаёт
компоновку: Row — по горизонтали, Card — группа с заголовком, остальное — элементы.

Запуск:  python3 render_ui.py ../carkeeper-ui.sysml ../../img ../../mockups
(PNG — в srs/img, HTML-исходники макетов — в srs/mockups)
Нужен Google Chrome (рендер HTML в PNG в режиме headless).
"""
import html
import os
import re
import subprocess
import sys

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
OUTPUT = {  # имя part def -> файл PNG
    'DashboardScreen': 'mock-dashboard.png',
    'PlanScreen': 'mock-plan.png',
    'RecordScreen': 'mock-record.png',
    'ExpensesScreen': 'mock-expenses.png',
    'AdminRegulationsScreen': 'mock-admin.png',
}


# ---------------- Разбор SysML v2 ----------------
TOKEN = re.compile(r'''\s+|//[^\n]*|/\*.*?\*/|"(?:[^"\\]|\\.)*"|:>>|:>|::|[{};:=]|[^\s{};:="]+''', re.S)


def tokenize(text):
    out = []
    for m in TOKEN.finditer(text):
        t = m.group(0)
        if t.isspace() or t.startswith('//') or t.startswith('/*'):
            continue
        out.append(t)
    return out


class Element:
    def __init__(self, kind, name, type_=None):
        self.kind, self.name, self.type = kind, name, type_
        self.attrs = {}
        self.parts = []

    def get(self, key, default=''):
        return self.attrs.get(key, default)


def parse_body(tok, i, owner):
    """Разбирает содержимое { ... } до закрывающей скобки, возвращает индекс после неё."""
    while i < len(tok) and tok[i] != '}':
        t = tok[i]
        if t == 'part' and tok[i + 1] == 'def':
            el = Element('def', tok[i + 2])
            i += 3
            if tok[i] == ':>':
                el.type = tok[i + 1]; i += 2
            i = parse_tail(tok, i, el)
            owner.parts.append(el)
        elif t == 'part':
            el = Element('part', tok[i + 1])
            i += 2
            if tok[i] in (':', ':>'):
                el.type = tok[i + 1]; i += 2
            i = parse_tail(tok, i, el)
            owner.parts.append(el)
        elif t == 'attribute':
            i += 1
            if tok[i] == ':>>':
                i += 1
            name = tok[i]; i += 1
            if tok[i] == ':':
                i += 2
            value = None
            if tok[i] == '=':
                raw = tok[i + 1]; i += 2
                value = raw[1:-1] if raw.startswith('"') else raw
            if tok[i] == ';':
                i += 1
            if value is not None:
                owner.attrs[name] = value
        else:  # прочие конструкции (import, doc, satisfy, first ... then ...) пропускаются
            depth = 0
            while i < len(tok):
                if tok[i] == '{':
                    depth += 1
                elif tok[i] == '}':
                    if depth == 0:
                        break
                    depth -= 1
                    if depth == 0:
                        i += 1; break
                elif tok[i] == ';' and depth == 0:
                    i += 1; break
                i += 1
    return i + 1


def parse_tail(tok, i, el):
    if tok[i] == ';':
        return i + 1
    if tok[i] == '{':
        return parse_body(tok, i + 1, el)
    raise SyntaxError(f'ожидалось ; или {{ после {el.name}: {tok[i]}')


def parse_model(path):
    tok = tokenize(open(path, encoding='utf-8').read())
    assert tok[0] == 'package'
    root = Element('package', tok[1])
    parse_body(tok, tok.index('{') + 1, root)
    return root


# ---------------- Отрисовка ----------------
E = html.escape
STATUS = {'Просрочено': 'red', 'Скоро': 'yel', 'В норме': 'grn'}


def width(el):
    return int(el.get('width', '1') or 1)


def cell(text):
    m = re.fullmatch(r'\[(.+)\]', text.strip())
    if m:
        return f'<span class="badge {STATUS.get(m.group(1), "")}">{E(m.group(1))}</span>'
    if text.startswith('+ '):
        return f'<span class="muted">{E(text)}</span>'
    return E(text)


def render(el):
    t = el.type
    if t == 'Row':
        inner = ''.join(f'<div style="flex:{width(c)}">{render(c)}</div>' for c in el.parts)
        return f'<div class="row">{inner}</div>'
    if t == 'Card':
        inner = ''.join(render(c) for c in el.parts)
        return f'<div class="card"><div class="card-h">{E(el.get("label"))}</div>{inner}</div>'
    if t == 'Field':
        return (f'<div class="field"><div class="lbl">{E(el.get("label"))}</div>'
                f'<div class="inp">{E(el.get("value"))}</div></div>')
    if t == 'Button':
        cls = 'btn primary' if el.get('primary') == 'true' else 'btn'
        return f'<div class="{cls}">{E(el.get("label"))}</div>'
    if t == 'Note':
        return f'<div class="note">{E(el.get("label"))}</div>'
    if t == 'Kpi':
        tone = {'просрочено': ' red-t', 'скоро': ' yel-t'}.get(el.get('label'), '')
        return f'<div class="kpi{tone}"><div class="kv">{E(el.get("value"))}</div><div class="muted">{E(el.get("label"))}</div></div>'
    if t == 'Tabs':
        act = el.get('active')
        return '<div class="tabs">' + ''.join(
            f'<span class="{"on" if x == act else ""}">{E(x)}</span>' for x in el.get('items').split('|')) + '</div>'
    if t == 'CheckList':
        checked = set(el.get('checked').split('|'))
        rows = ''
        for n, item in enumerate(el.get('items').split('|'), 1):
            mark = 'on' if str(n) in checked else ''
            rows += f'<div class="chk-row"><span class="chk {mark}"></span>{E(item)}</div>'
        return f'<div class="checklist">{rows}</div>'
    if t == 'Table':
        cols = el.get('columns').split('|')
        head = ''.join(f'<th>{E(c)}</th>' for c in cols)
        body = ''
        for r in el.get('rows').split(';'):
            cells = (r.split('|') + [''] * len(cols))[:len(cols)]
            body += '<tr>' + ''.join(f'<td>{cell(c)}</td>' for c in cells) + '</tr>'
        return f'<table><tr>{head}</tr>{body}</table>'
    if t == 'BarChart':
        vals = [float(v) for v in el.get('values').split('|')]
        caps = el.get('captions').split('|')
        top = max(vals) or 1
        bars = ''
        for v, c in zip(vals, caps):
            h = 150 * v / top
            bars += (f'<div class="bar"><div class="bv">{int(v) if v else ""}</div>'
                     f'<div class="bb" style="height:{h:.0f}px"></div><div class="bc">{E(c)}</div></div>')
        return f'<div class="chart">{bars}</div>'
    return f'<div class="note">«part» {E(el.name)} : {E(t or "")}</div>'


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1100px;height:640px;background:#f3f4f6;font-family:"Helvetica Neue",Arial,sans-serif;color:#1f2937;font-size:12.5px;display:flex;overflow:hidden}
.side{width:186px;background:#1e293b;color:#cbd5e1;display:flex;flex-direction:column}
.logo{display:flex;align-items:center;gap:9px;font-weight:700;font-size:17px;color:#fff;padding:18px 16px;border-bottom:1px solid #334155}
.logo i{display:inline-block;width:26px;height:26px;border-radius:7px;background:#f59e0b;position:relative}
.logo i::after{content:"";position:absolute;left:6px;top:11px;width:14px;height:6px;border-radius:3px 3px 1px 1px;background:#1e293b}
.logo span{color:#f59e0b}
.mi{padding:10px 16px;font-size:13px}
.mi.on{background:#0f172a;color:#fff;border-left:3px solid #f59e0b;padding-left:13px;font-weight:600}
.user{margin-top:auto;padding:14px 16px;font-size:11px;color:#94a3b8;line-height:1.5}
.main{flex:1;padding:20px 24px;overflow:hidden}
.head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px}
h1{font-size:21px;color:#0f172a}.sub{color:#6b7280;font-size:12px;margin-top:3px}
.btns{display:flex;gap:8px}
.btn{border:1px solid #d1d5db;border-radius:7px;padding:8px 14px;background:#fff;font-weight:600;white-space:nowrap;text-align:center;color:#374151}
.btn.primary{background:#d97706;color:#fff;border-color:#d97706}
.row{display:flex;gap:12px;margin-bottom:12px;align-items:stretch}
.row>div>.card{height:100%}
.card{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:12px 14px;margin-bottom:12px;box-shadow:0 1px 2px rgba(15,23,42,.05)}
.row .card{margin-bottom:0}
.card-h{font-weight:700;font-size:13.5px;margin-bottom:9px;color:#0f172a}
.field{margin-bottom:8px}.lbl{font-size:11px;color:#6b7280;margin-bottom:3px}
.inp{border:1px solid #d1d5db;border-radius:6px;padding:6px 10px;min-height:30px;background:#fff;font-size:13px}
.row .field{margin-bottom:0}.row .btn{margin-top:17px}
.note{font-size:11.5px;color:#6b7280;margin:4px 0}
table{width:100%;border-collapse:collapse}
th{text-align:left;font-size:11px;color:#6b7280;font-weight:600;padding:6px 8px;border-bottom:1px solid #e5e7eb}
td{padding:6px 8px;border-bottom:1px solid #f1f5f9;font-size:12px}
.badge{display:inline-block;padding:2px 9px;border-radius:10px;font-size:11px;font-weight:700}
.red{background:#fee2e2;color:#b91c1c}.yel{background:#fef3c7;color:#92400e}.grn{background:#dcfce7;color:#166534}
.muted{color:#6b7280;font-size:11.5px}
.kpi{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:9px 12px;text-align:center;margin-bottom:8px}
.row .kpi{margin-bottom:0;text-align:left;padding:12px 16px}
.kv{font-size:22px;font-weight:700;color:#0f172a}
.red-t .kv{color:#b91c1c}.yel-t .kv{color:#b45309}
.red-t{background:#fef2f2;border-color:#fecaca}.yel-t{background:#fffbeb;border-color:#fde68a}
.checklist{line-height:2}.chk{display:inline-block;width:14px;height:14px;border:1.5px solid #9ca3af;border-radius:3px;margin-right:8px;vertical-align:-2px}
.chk.on{background:#d97706;border-color:#d97706}
.tabs{margin-bottom:12px}.tabs span{display:inline-block;border:1px solid #d1d5db;padding:6px 14px;margin-right:6px;border-radius:7px;background:#fff}
.tabs span.on{background:#1e293b;color:#fff;border-color:#1e293b}
.chart{display:flex;align-items:flex-end;gap:9px;height:215px;padding:4px 6px}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.bb{width:72%;background:#f59e0b;border-radius:3px 3px 0 0}.bv{font-size:10px;color:#6b7280;margin-bottom:2px}
.bc{font-size:10.5px;color:#6b7280;padding-top:4px;border-top:1px solid #d1d5db;width:100%;text-align:center}
"""


def page(screen, menu):
    buttons = [p for p in screen.parts if p.type == 'Button']
    content = [p for p in screen.parts if p.type != 'Button']
    items = ''.join(f'<div class="mi {"on" if m == screen.get("activeMenu") else ""}">{E(m)}</div>'
                    for m in menu.get('items').split('|'))
    btns = ''.join(render(b) for b in buttons)
    body = ''.join(render(c) for c in content)
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{E(screen.get("title"))}</title><style>{CSS}</style></head><body>
<div class="side"><div class="logo"><i></i><b>Car<span>Keeper</span></b></div>{items}<div class="user">{E(screen.get("userInfo"))}</div></div>
<div class="main"><div class="head"><div><h1>{E(screen.get("title"))}</h1><div class="sub">{E(screen.get("subtitle"))}</div></div>
<div class="btns">{btns}</div></div>{body}</div></body></html>"""


def main():
    model_path = sys.argv[1] if len(sys.argv) > 1 else '../carkeeper-ui.sysml'
    out_dir = sys.argv[2] if len(sys.argv) > 2 else '../../img'
    model = parse_model(model_path)
    menu = next(p for p in model.parts if p.type == 'SideMenu')
    screens = [p for p in model.parts if p.kind == 'def' and p.type == 'Screen']
    src_dir = os.path.abspath(sys.argv[3] if len(sys.argv) > 3 else '../../mockups')
    os.makedirs(src_dir, exist_ok=True)
    if screens:
        for s in screens:
            html_path = os.path.join(src_dir, OUTPUT.get(s.name, s.name + '.png')[:-4] + '.html')
            open(html_path, 'w', encoding='utf-8').write(page(s, menu))
            png = os.path.abspath(os.path.join(out_dir, OUTPUT.get(s.name, s.name + '.png')))
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=2', '--window-size=1100,640',
                            f'--screenshot={png}', 'file://' + html_path],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f'{s.name}: {len(s.parts)} частей -> {png}')


if __name__ == '__main__':
    main()
