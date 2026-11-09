# Генератор SVG-диаграмм SysML v2 для CarKeeper; рендер в PNG — headless Chrome
import subprocess, os, html
BW='font-weight="bold"'
F='font-family="DejaVu Sans, Verdana, Arial, sans-serif"'
NEW='#fcd9a8'; NEWS='#d97706'; GREY='#ececec'
def esc(s): return html.escape(s)
def box(x,y,w,h,lines,fill='#fff',stroke='#000',sw=1.3):
    o=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
    n=len(lines); lh=17; y0=y+h/2-(n-1)*lh/2+5
    for i,(t,sz,b) in enumerate(lines):
        o.append(f'<text x="{x+w/2}" y="{y0+i*lh}" text-anchor="middle" font-size="{sz}" {BW if b else ""} {F}>{esc(t)}</text>')
    return ''.join(o)
def line(x1,y1,x2,y2,dash=False,arrow=False,diamond=False):
    a=f' stroke-dasharray="6,4"' if dash else ''
    m=' marker-end="url(#arr)"' if arrow else ''
    m+=' marker-start="url(#dia)"' if diamond else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="1.2"{a}{m}/>'
def txt(x,y,t,sz=13,anchor='middle',bold=False):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{sz}" {BW if bold else ""} {F}>{esc(t)}</text>'
DEFS='''<defs><marker id="arr" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto"><path d="M0,0 L11,5 L0,10" fill="none" stroke="#000"/></marker>
<marker id="dia" markerWidth="16" markerHeight="10" refX="1" refY="5" orient="auto"><path d="M1,5 L8,1 L15,5 L8,9 Z" fill="#000"/></marker></defs>'''
def save(name,w,h,body):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#fff"/>{DEFS}{body}</svg>'
    open(name+'.svg','w').write(svg)
    open(name+'.html','w').write(f'<!doctype html><html><head><meta charset=utf-8><style>body{{margin:0}}</style></head><body>{svg}</body></html>')
    out=os.path.abspath(f'../../img/{name}.png')
    subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=2',f'--window-size={w},{h}',f'--screenshot={out}','file://'+os.path.abspath(name+'.html')],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)

# ---------- Диаграмма вариантов использования ----------
b=[]
b.append('<rect x="165" y="15" width="590" height="640" fill="none" stroke="#000" stroke-width="1.8"/>')
b.append(txt(180,42,'«part» carKeeper : CarKeeper',14,'start'))
def uc(x,y,t1,t2,new=False):
    return box(x,y,160,60,[('«use case»',11,False),(t1,13,False),(t2,13,False)],fill=NEW if new else '#fff',stroke=NEWS if new else '#000')
L=[(60,'Добавить','автомобиль'),(135,'Ввести','пробег'),(210,'Просмотреть','план ТО'),(300,'Добавить запись','в журнал'),(390,'Просмотреть','расходы'),(480,'Вести шины','и документы'),(570,'Получать','напоминания')]
for y,a,c in L: b.append(uc(180,y,a,c,new=(a=='Вести шины')))
# include/extend
b.append(uc(410,135,'Рассчитать','сроки и статусы'))
b.append(line(340,165,410,165,True,True)); b.append(txt(375,157,'«include»',11))
b.append(line(340,240,410,175,True,True)); b.append(txt(370,222,'«include»',11))
b.append(uc(410,300,'Отметить','выполненные'))
b.append(line(340,330,410,330,True,True)); b.append(txt(375,322,'«include»',11))
b.append(uc(410,390,'Экспортировать','историю в PDF'))
b.append(line(410,420,340,420,True,True)); b.append(txt(375,412,'«extend»',11))
b.append(uc(580,225,'Вести регламенты','ТО'))
b.append(uc(580,480,'Управлять','пользователями'))
# actors
b.append(box(15,290,120,60,[('«actor»',11,False),('Owner',14,True),('(владелец)',12,False)],fill=GREY))
for y,_,_ in L: b.append(line(135,320,180,y+30))
b.append(box(790,320,125,55,[('«actor»',11,False),('Administrator',14,True)],fill=GREY))
b.append(line(740,255,790,347)); b.append(line(740,510,790,347))
b.append(box(790,570,125,55,[('«actor»',11,False),('MailServer',14,True)],fill=GREY))
b.append(line(340,600,790,598))
# заменено диаграммой SysML v2 Pilot (sysml/viz): save('use-cases',930,670,''.join(b))

# ---------- Иерархии требований ----------
def tree(name,root,groups,W=760):
    b=[]; y=15; gy=[]
    for g in groups:
        n=len(g[2]); h=n*27; top=y; gy.append((top,h))
        y+=max(h,58)+22
    H=y; rx,ry=5,H/2-38
    b.append(box(rx,ry,122,76,[('«requirement»',11,False),(root[0],14,True),(root[1],11,False),(root[2],11,False)],fill=GREY))
    trunk=145; b.append(line(127,H/2,trunk,H/2,diamond=True))
    first=last=None
    for (gname,gtitle,leaves),(top,h) in zip(groups,gy):
        cy=top+max(h,58)/2; first=first or cy; last=cy
        b.append(line(trunk,cy,160,cy))
        b.append(box(160,cy-29,175,58,[('«requirement»',11,False),(gname,14,True),(gtitle,11,False)],fill=GREY))
        lx=355; b.append(line(335,cy,lx,cy,diamond=True))
        ly0=cy-h/2+12
        b.append(line(lx,ly0,lx,ly0+(len(leaves)-1)*27))
        for i,(rid,t,new) in enumerate(leaves):
            yy=ly0+i*27
            b.append(line(lx,yy,370,yy))
            b.append(f'<rect x="370" y="{yy-11}" width="{W-375}" height="22" fill="{NEW if new else "#fff"}" stroke="{NEWS if new else "#000"}" stroke-width="1.2"/>')
            b.append(f'<text x="378" y="{yy+5}" font-size="13" {F}><tspan font-weight="bold">{rid}</tspan> · {esc(t)}</text>')
    b.append(line(trunk,first,trunk,last))
    save(name,W,H,''.join(b))
N=False;Y=True
tree('func-requirements',('carKeeperSpec','Функциональные','требования'),[
 ('accessAndRoles','Доступ и роли',[('REQ-FUNC-001','Регистрация и вход',N),('REQ-FUNC-002','Роли и права доступа',N)]),
 ('garageGroup','Автомобили и пробег',[('REQ-FUNC-003','Управление автомобилями',N),('REQ-FUNC-004','Ввод показаний пробега',N),('REQ-FUNC-019','Сезонная смена шин',Y),('REQ-FUNC-020','Сроки документов',Y)]),
 ('planGroup','План ТО',[('REQ-FUNC-005','Справочник регламентов',N),('REQ-FUNC-006','План ТО автомобиля',N),('REQ-FUNC-007','Расчёт срока обслуживания',N),('REQ-FUNC-008','Статусы позиций плана',N)]),
 ('journalGroup','Журнал обслуживания',[('REQ-FUNC-009','Запись в журнал (+артикул)',Y),('REQ-FUNC-010','Закрытие позиций плана',N),('REQ-FUNC-013','Вложения к записи',N)]),
 ('reminderGroup','Напоминания',[('REQ-FUNC-011','Напоминания по e-mail',N),('REQ-FUNC-012','Уведомления в приложении',N),('REQ-FUNC-016','Календарь работ',N)]),
 ('reportGroup','Расходы и отчёты',[('REQ-FUNC-014','Отчёт о расходах',N),('REQ-FUNC-015','Экспорт истории в PDF',N),('REQ-FUNC-017','Импорт/экспорт CSV',N),('REQ-FUNC-018','Прогноз расходов',N)]),
])
tree('nonfunc-requirements',('qualitySpec','Нефункциональные','требования'),[
 ('performance','Производительность',[('REQ-PERF-001','Страницы ≤ 1,5 с',N),('REQ-PERF-002','Пересчёт плана ≤ 1 с',N),('REQ-PERF-003','PDF ≤ 5 с',N),('REQ-PERF-004','Проверка напоминаний ≤ 10 мин',N)]),
 ('security','Безопасность',[('REQ-SEC-001','bcrypt ≥ 10',N),('REQ-SEC-002','Только HTTPS',N),('REQ-SEC-003','Доступ только к своим данным',N),('REQ-SEC-004','Сеанс и блокировка входа',N),('REQ-SEC-005','CSRF, параметризация',N),('REQ-SEC-006','Проверка вложений',N)]),
 ('reliability','Надёжность и доступность',[('REQ-REL-001','Без дублей напоминаний',N),('REQ-REL-002','Повторы SMTP',N),('REQ-REL-003','Резервные копии',N),('REQ-AVAIL-001','Доступность ≥ 99 %',N),('REQ-AVAIL-002','Окно работ 02:00–05:00',N)]),
 ('operations','Наблюдение и нормы',[('REQ-OBS-001','JSON-логи без ПДн',N),('REQ-OBS-002','Метрики Actuator',N),('REQ-COMP-001','Согласие и удаление ПДн',N),('REQ-COMP-002','Форматы дат и валют',N),('REQ-COMP-003','Рекомендательный характер',N)]),
 ('implementation','Реализация',[('REQ-INST-001','docker compose',N),('REQ-BUILD-001','Maven + GitHub Actions',N),('REQ-MAINT-001','Покрытие ядра ≥ 90 %',N),('REQ-MAINT-002','Слоистая архитектура',N),('REQ-PORT-001','Браузеры, от 360 px',N),('REQ-COST-001','Хостинг ≤ 10 USD/мес',N),('REQ-DEAD-001','Сроки итераций',N)]),
])

# ---------- Модель предметной области ----------
def cls(x,y,w,name,attrs,new=False):
    h=58+len(attrs)*17+10
    o=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{NEWS if new else "#000"}" stroke-width="1.3"/>',
       f'<rect x="{x}" y="{y}" width="{w}" height="40" fill="{NEW if new else GREY}" stroke="{NEWS if new else "#000"}" stroke-width="1.3"/>',
       txt(x+w/2,y+16,'«part def»',11),txt(x+w/2,y+33,name,14,bold=True),txt(x+8,y+56,'attributes',11,'start')]
    for i,a in enumerate(attrs): o.append(txt(x+16,y+74+i*17,a,12,'start'))
    return ''.join(o),h
b=[]
def put(*a,**k):
    s,h=cls(*a,**k); b.append(s); return h
put(20,20,170,'User',['id','email','passwordHash','role','remindByEmail','warnKm, warnDays'])
put(250,20,180,'MileageReading',['id','date','mileage'])
put(490,20,170,'CarDocument',['id','type','expiresAt'],new=True)
put(720,20,170,'Regulation',['id','engineType','name'])
put(20,250,170,'TyreSet',['id','season','brand','mileage','installed'],new=True)
put(250,250,180,'Car',['id','make, model, year','engineType','vin, plate','annualMileage','archived'])
put(490,250,170,'PlanItem',['id','title, category','intervalKm','intervalMonths','lastDate, lastMileage','enabled'])
put(720,250,170,'RegulationItem',['id','title, category','intervalKm','intervalMonths'])
put(20,480,170,'Attachment',['id','fileName','contentType','size'])
put(250,480,180,'ServiceRecord',['id','date, mileage','place','labourCost','comment','total'])
put(490,480,170,'RecordPart',['id','name','manufacturer','partNumber','quantity, price'],new=True)
put(720,480,170,'Notification',['id','status','createdAt','read'])
def a(x1,y1,x2,y2,m1,p1,m2,p2,comp=True,label=None,lp=None):
    b.append(line(x1,y1,x2,y2,diamond=comp))
    b.append(txt(p1[0],p1[1],m1,12,'start')); b.append(txt(p2[0],p2[1],m2,12,'start'))
    if label: b.append(txt(lp[0],lp[1],label,11,'start'))
# owner end first (diamond)
a(250,270,105,190,'0..*',(212,255),'1',(116,206))           # User–Car (Car owned by User)
b.pop(-3); b.insert(len(b)-2,line(105,190,250,270,diamond=True))
a(340,250,340,139,'1',(346,244),'0..*',(346,157))           # Car–MileageReading
a(430,262,560,139,'1',(446,276),'0..*',(568,157))           # Car–CarDocument
a(250,335,190,335,'1',(232,328),'0..*',(196,328))           # Car–TyreSet
a(430,300,490,300,'1',(436,293),'1..*',(458,293))           # Car–PlanItem
a(340,420,340,480,'1',(346,436),'0..*',(346,474))           # Car–ServiceRecord
a(805,139,805,250,'1',(811,157),'1..*',(811,244))           # Regulation–RegulationItem
a(720,300,660,300,'0..1',(690,318),'0..*',(664,293),comp=False)  # PlanItem–RegulationItem
a(250,560,190,560,'1',(232,553),'0..*',(196,553))           # SR–Attachment
a(430,560,490,560,'1',(436,553),'0..*',(458,553))           # SR–RecordPart
a(430,490,540,420,'0..*',(438,505),'0..*',(548,438),comp=False,label='«closes»',lp=(436,462))  # SR–PlanItem
a(640,420,780,480,'1',(648,438),'0..*',(786,474),comp=False)   # PlanItem–Notification
# заменено диаграммой SysML v2 Pilot (sysml/viz): save('domain-model',910,670,''.join(b))
