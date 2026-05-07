"""
PIED PIPER — ASCII Map Renderer
Hand-crafted ASCII world map with proper geographic shapes.
96 cols x 27 rows — optimized for terminal display.
"""
import sys, time, os
from ui.terminal import R, G, B, Y, C, DIM, M, strip_ansi

try:
    from PIL import Image
    import numpy as np
    HAS_PIL = True
except Exception:
    HAS_PIL = False

                                                                               
                               
                                                               
                                                                               
ASCII_MAP = [
    r"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"~~,-.~~~~~~~~~~~~~~~~~~,-----------,~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~,-----------,~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"~/ AK\~~~~~~~~~~~~~~~~/ GREENLAND  |~~~~~~~~~~~~~~~~~~~~~~~~~,-/ SCANDINAVIA \-,~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"|      `--,___________`            |~~~~~,----,~~~~~~~~~~~~~~~/  SWEDEN FINLAND  |~SIBERIA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"| CANADA           LABRADOR        |~~~~| ICEL |~~~~~~~~~~~~~~~~\ UK   BALTICS  /~~~~~~~~~~,-,~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"|         GREAT    HUDSON    ,-----'~~~~`----'~~~~~~~~~,---------\ FRA  POLAND /  RUSSIA   | |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"|         LAKES    BAY      /~~~ATLANTIC~~~~,----------\  UKRAINE  `----------'             | |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"| USA              ,-------'~~~~OCEAN~~~~~~|   TURKEY  GEORGIA  KAZAKH  MONGOLIA    SIBERIA | |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"|                 /~~~~~~~~~~~~~~~~~~,----.|   SYRIA   ARMENIA  UZBEK   XINJIANG    GOBI    `-'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"|     USA        /~~~~~~~~~~~~~~~~~~~|     `---,  IRAQ  IRAN  AFGHANI  TIBET  NEPAL  CHINA  ,--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"|               /~~~~~~~~~~~~~~~~~~~~|  ISR  EGYPT  KUWAIT    PAKISTAN       BHUTAN  ,-CHN-'  |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r" \             / GULF OF~~~~~~~~~~~~~`--------\  SAUDI         INDIA   ,------'  MYANMAR  VIET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"  \   USA     /  MEXICO~~~~~~~~~~~~~~~~~~,----`  ARABIA       /      BANGLADESH  THAILAND  ,--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"   \          |  CARIBBEAN~~~~~~~~~~~~~~/ HORN                /  INDIA  CALCUTTA  ,---,   /   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"    `--,      |  SEA~~~~~~~~~~~~~~~~~~/ OF     INDIAN        /          BAY    S.CHINA  /  PHI~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"        `--,  `--,~~~~~~~~~~~~~~~~~~~/ AFRICA  OCEAN        /         OF BENGAL  SEA  ,-'     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"PACIFIC      `----`-----------------'~~~~~~~~~~~~~~~~~~~~~~~~~~\      ,----------'   /  BORNEO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"OCEAN     VENEZUELA  ,~~~~ATLANTIC~~~~~~,----------,~~~~~~~~~~~~`----'  MALAYSIA  ,-'    JAVA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"        COLOMBIA     |~~~~OCEAN~~~~~~~~/ S.AFRICA  |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  SULAWESI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"          BRAZIL     |~~~~~~~~~~~~~~~`'~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~,--- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"                     |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~,-------,~~~~~~~~~~~~~~~~~~~~~AUSTRALIA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"        S.AMERICA    |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|       |~~~~~~~~~~~~~~~~~~~~~            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"          BRAZIL     |~~~~~~~~~~~~~~S.ATLANTIC~~~~~~~~~~|       `--,~~AUSTRALIA~~,-'            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"                     |~~~~~~~~~~~~~~OCEAN~~~~~~~~~~~~~~~~`---------'~~~~~~~~~~~~~|               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"         ARGENTINA   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"           CHILE    /~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SOUTHERN OCEAN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    r"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
]

MAP_ROWS = len(ASCII_MAP)
MAP_COLS = max(len(r) for r in ASCII_MAP)

                                                                               
                                                                            
                                                                               
NATION_POS = {
    "USA": ( 9, 21),          
    "RUS": ( 5, 179),             
    "CHN": ( 9, 162),                          
    "UK" : ( 4, 100),       
    "FRA": ( 5, 147),          
    "IND": (12, 132),               
    "PAK": (10, 132),               
    "ISR": (10, 85),          
    "PRK": ( 7, 187),                                       
}

NATION_META = {
    "USA": {"lon": -95.71, "lat": 37.09},
    "RUS": {"lon": 105.32, "lat": 61.52},
    "CHN": {"lon": 104.20, "lat": 35.86},
    "UK":  {"lon":  -3.44, "lat": 55.38},
    "FRA": {"lon":   2.21, "lat": 46.23},
    "IND": {"lon":  78.96, "lat": 20.59},
    "PAK": {"lon":  69.35, "lat": 30.38},
    "ISR": {"lon":  34.85, "lat": 31.05},
    "PRK": {"lon": 127.51, "lat": 40.34},
}


                                                                               
          
                                                                               

def _color(ch):
    """Colorize a single terrain character."""
    if ch == '~':               return C(ch)                        
    if ch in r",.-'`/\|_\\":   return G(ch)                                
    if ch == ' ':               return ch                            
    if ch.isupper():            return DIM(ch)                      
    return G(ch)

def _bresenham(a, b):
    r0,c0 = a; r1,c1 = b
    dr,dc = abs(r1-r0), abs(c1-c0)
    sr = 1 if r0<r1 else -1
    sc = 1 if c0<c1 else -1
    err = dr - dc; pts = []
    r,c = r0,c0
    while True:
        pts.append((r,c))
        if r==r1 and c==c1: break
        e2 = 2*err
        if e2 > -dc: err -= dc; r += sr
        if e2 <  dr: err += dr; c += sc
    return pts

def _overlay(rows, r, c, ch):
    if 0<=r<len(rows) and 0<=c<len(rows[r]):
        lst = list(rows[r]); lst[c] = ch; rows[r] = ''.join(lst)
    return rows

def _safe(row, enc):
    try:
        row.encode(enc or 'utf-8'); return row
    except Exception:
        return row.replace('◉','@').replace('◎','O').replace('·','.').replace('◆','*')

def _render_row(line, enc):
    safe = _safe(line, enc)
    out = ""
    for ch in safe:
        if   ch == 'X':      out += R(ch)
        elif ch == '◉':      out += M(ch)
        elif ch == '◎':      out += Y(ch)
        elif ch == '#':      out += R(ch)
        elif ch == '@':      out += Y(ch)
        elif ch in '·*.◆':  out += G(ch)
        else:                out += _color(ch)
    return out

def _border(width):
    return G("+" + "-" * width + "+")

def _legend():
    return (f"  {M('◉')} YOU   {Y('◎')} TARGET   "
            f"{R('X')} STRUCK   {C('~')} OCEAN   {G('-')} COAST")


                                                                               
            
                                                                               

def print_map(nations_data, player=None, highlights=None, strikes=None):
    highlights = highlights or []
    strikes    = strikes    or []
    enc        = (sys.stdout.encoding or '').lower()

    rows = [r.ljust(MAP_COLS) for r in ASCII_MAP]

    for code in strikes:
        pos = NATION_POS.get(code)
        if pos: rows = _overlay(rows, pos[0], pos[1], 'X')
    for code in highlights:
        pos = NATION_POS.get(code)
        if pos: rows = _overlay(rows, pos[0], pos[1], '◎')
    if player:
        pos = NATION_POS.get(player)
        if pos: rows = _overlay(rows, pos[0], pos[1], '◉')

    print(_border(MAP_COLS))
    for line in rows:
        print(G("|") + _render_row(line, enc) + G("|"))
    print(_border(MAP_COLS))
    print(_legend())


                                                                               
                          
                                                                               

def animate_strike(src, tgt, label='SIGNAL', speed=0.04):
    a = NATION_POS.get(src); b = NATION_POS.get(tgt)
    if not a or not b: return
    from engine.nations import NATIONS

    path = _bresenham(a, b); trail = []
    enc  = (sys.stdout.encoding or '').lower()
                                                                    
    TOTAL = MAP_ROWS + 4

    print_map(NATIONS, player=src, highlights=[tgt])
    print(C(f"  LAUNCH: {src} >>> {tgt}  [{label}]  0%"))
    time.sleep(0.2)

    for i, (pr, pc) in enumerate(path):
        rows = [r.ljust(MAP_COLS) for r in ASCII_MAP]
        for tr,tc in trail[-10:]:
            rows = _overlay(rows, tr, tc, '.')
        rows = _overlay(rows, pr, pc, '#')
        if a: rows = _overlay(rows, a[0], a[1], '@')
        if b: rows = _overlay(rows, b[0], b[1], '@')

        sys.stdout.write(f"\033[{TOTAL}A")
        print(_border(MAP_COLS))
        for line in rows:
            print(G("|") + _render_row(line, enc) + G("|"))
        print(_border(MAP_COLS))
        print(_legend())

        pct = int(100 * i / max(1, len(path)-1))
        filled = int(pct/5); bar = '█'*filled + '░'*(20-filled)
        print(f"  {R('◆')} {src} >>> {tgt}  [{label}]  |{bar}| {pct:3d}%")
        sys.stdout.flush()
        trail.append((pr, pc))
        time.sleep(speed)


                                                                               
                         
                                                                               

def animate_strikes(strikes, speed=0.04):
    from engine.nations import NATIONS

    sdata = []
    for s in strikes:
        src,tgt = s[0],s[1]; lbl = s[2] if len(s)>2 else 'STRIKE'
        a = NATION_POS.get(src); b = NATION_POS.get(tgt)
        if a and b:
            sdata.append({'src':src,'tgt':tgt,'label':lbl,'a':a,'b':b,
                          'path':_bresenham(a,b),'trail':[]})
    if not sdata: return

    enc   = (sys.stdout.encoding or '').lower()
                                                           
    TOTAL = MAP_ROWS + 4 + len(sdata)

    targets = [s['tgt'] for s in sdata]
    print_map(NATIONS, player=sdata[0]['src'], highlights=targets)
    print()
    for s in sdata:
        bar = '░'*20
        print(C(f"  {s['src']} >>> {s['tgt']:3}  [{s['label'][:20]:20}]  |{bar}|   0%"))
    time.sleep(0.4)

    maxlen = max(len(s['path']) for s in sdata)

    for frame in range(maxlen):
        rows = [r.ljust(MAP_COLS) for r in ASCII_MAP]
        for s in sdata:
            for i,(tr,tc) in enumerate(s['trail'][-12:]):
                rows = _overlay(rows, tr, tc, '·' if i<6 else '.')
            if frame < len(s['path']):
                pr,pc = s['path'][frame]
                rows = _overlay(rows, pr, pc, '#' if frame%2==0 else '◆')
                s['trail'].append((pr, pc))
            tp = NATION_POS.get(s['tgt']); pp = NATION_POS.get(s['src'])
            if tp: rows = _overlay(rows, tp[0], tp[1], '@')
            if pp: rows = _overlay(rows, pp[0], pp[1], '◉')

        sys.stdout.write(f"\033[{TOTAL}A")
        print(_border(MAP_COLS))
        for line in rows:
            print(G("|") + _render_row(line, enc) + G("|"))
        print(_border(MAP_COLS))
        print(_legend())
        print()
        for s in sdata:
            plen = len(s['path'])
            pct  = int(100*frame/max(1,plen-1)) if plen>1 else 100
            filled = int(pct/5); bar = '█'*filled + '░'*(20-filled)
            print(C(f"  {s['src']} >>> {s['tgt']:3}  [{s['label'][:20]:20}]  |{bar}| {pct:3d}%"))

        sys.stdout.flush()
        time.sleep(speed)


                                                                               
                         
                                                                               

def getAverageL(image):
    im = np.array(image); w,h = im.shape
    return np.average(im.reshape(w*h))

def covertImageToAscii(fileName, cols, scale, moreLevels):
    gs = "$B%8&WM*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    image = Image.open(fileName).convert('L'); W,H = image.size
    w = W/cols; h = w/scale; nrows = int(H/h); aimg = []
    for j in range(nrows):
        y1=int(j*h); y2=int((j+1)*h) if j<nrows-1 else H; aimg.append("")
        for i in range(cols):
            x1=int(i*w); x2=int((i+1)*w) if i<cols-1 else W
            avg = getAverageL(image.crop((x1,y1,x2,y2)))
            aimg[j] += gs[int((avg/255)*(len(gs)-1))]
    return aimg
