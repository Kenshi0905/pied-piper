"""
PIED PIPER — MAP WINDOW  v2.0
Pygame live tactical display — polls shared state file every 300ms.
Visually matches Firewall WarGames aesthetic:
  • Black background
  • Cyan continent outlines (vector polygon world map)
  • Red filled circles for nation nodes
  • Dotted arc missile trajectories with travelling dot
  • Live DEFCON gauge, tension bar, event ticker, nation stats
  • Glitch flash on strikes
"""

import sys
import os
# Suppress warnings BEFORE importing pygame
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*pkg_resources.*")

# Suppress pygame welcome message
import io
from contextlib import redirect_stdout, redirect_stderr

f = io.StringIO()
with redirect_stdout(f), redirect_stderr(f):
    import pygame
    
import json
import math
import time
import random
from pathlib import Path
from datetime import datetime

try:
    from coastline_data import COASTLINE_LONLAT
except:
    COASTLINE_LONLAT = []

try:
    from country_data import COUNTRY_COORDS, get_nation_coords
except:
    COUNTRY_COORDS = {}
    def get_nation_coords(code):
        return None

                                                     
STATE_FILE = Path.home() / ".pied_piper_state.json"

               
W, H = 1200, 800
FPS  = 60

def get_layout():
    """Get responsive layout values based on window size"""
    return {
        # Left panels
        'defcon_x': int(W * 0.015),
        'defcon_y': int(H * 0.025),
        'defcon_w': int(W * 0.16),
        'defcon_h': int(H * 0.15),
        
        'tension_x': int(W * 0.015),
        'tension_y': int(H * 0.19),
        'tension_w': int(W * 0.16),
        'tension_h': int(H * 0.13),
        
        # Right panels
        'stats_x': int(W * 0.82),
        'stats_y': int(H * 0.025),
        'stats_w': int(W * 0.17),
        'stats_h': int(H * 0.22),
        
        'nations_x': int(W * 0.82),
        'nations_y': int(H * 0.265),
        'nations_w': int(W * 0.17),
        'nations_h': int(H * 0.55),
        
        # Bottom panels
        'ticker_x': int(W * 0.015),
        'ticker_y': int(H * 0.68),
        'ticker_w': int(W * 0.8),
        'ticker_h': int(H * 0.28),
        
        'legend_x': int(W * 0.82),
        'legend_y': int(H * 0.82),
        'legend_w': int(W * 0.17),
        'legend_h': int(H * 0.15),
    }

BLACK      = (0,   0,   0)
CYAN       = (0,   210, 210)
CYAN_DIM   = (0,   90,  90)
CYAN_BRIGHT= (100, 255, 255)
RED        = (220, 30,  30)
RED_BRIGHT = (255, 80,  80)
RED_DIM    = (100, 15,  15)
WHITE      = (220, 220, 220)
WHITE_DIM  = (120, 120, 120)
YELLOW     = (220, 180, 0)
ORANGE     = (210, 100, 0)
GREEN_CRT  = (0,   200, 80)
GREEN_DIM  = (0,   80,  30)
PURPLE     = (140, 80,  200)
PURPLE_DIM = (60,  30,  100)

def lonlat_to_screen(lat, lon):
    x = int((lon + 180) / 360 * W)
    y = int((90 - lat) / 180 * H)
    return (x, y)

NATION_POS = {
    "USA": lonlat_to_screen(37.09024, -95.712891),
    "RUS": lonlat_to_screen(61.52401, 105.318756),
    "CHN": lonlat_to_screen(35.86166, 104.195397),
    "UK":  lonlat_to_screen(55.378051, -3.435973),
    "FRA": lonlat_to_screen(46.227638, 2.213749),
    "IND": lonlat_to_screen(20.593684, 78.96288),
    "PAK": lonlat_to_screen(30.375321, 69.345116),
    "ISR": lonlat_to_screen(31.046051, 34.851612),
    "PRK": lonlat_to_screen(40.339852, 127.510093),
}

NATION_NAMES = {
    "USA": "UNITED STATES",
    "RUS": "RUSSIA",
    "CHN": "CHINA",
    "UK":  "UNITED KINGDOM",
    "FRA": "FRANCE",
    "IND": "INDIA",
    "PAK": "PAKISTAN",
    "ISR": "ISRAEL",
    "PRK": "NORTH KOREA",
}


def arc_points(src, dst, num=100, height_factor=0.50):
    pts = []
    sx, sy = src; ex, ey = dst
    for i in range(num + 1):
        t = i / num
        x = sx + (ex - sx) * t
        y = sy + (ey - sy) * t
        lift = height_factor * math.dist(src, dst) * math.sin(math.pi * t)
        y -= lift
        pts.append((int(x), int(y)))
    return pts


class Missile:
    def __init__(self, src_key, dst_key, color=RED_BRIGHT, label="ICBM", retaliation=False):
        self.src = NATION_POS[src_key]
        self.dst = NATION_POS[dst_key]
        self.src_key = src_key
        self.dst_key = dst_key
        self.label = label
        self.retaliation = retaliation
        self.color = PURPLE if retaliation else color
        self.trail_color = PURPLE_DIM if retaliation else RED_DIM
        self.pts = arc_points(self.src, self.dst)
        self.progress = 0.0
        self.speed = (0.004 + random.uniform(0, 0.002)) * (60 / FPS)  # Frame-dependent
        self.done = False
        self.exploded = False
        self.explosion_r = 0
        self.explosion_speed = 2.5 * (60 / FPS)  # Frame-dependent
        self.birth = time.time()

    def update(self):
        if self.exploded:
            self.explosion_r += self.explosion_speed
            if self.explosion_r > 40:
                self.done = True
            return
        self.progress = min(1.0, self.progress + self.speed)
        if self.progress >= 1.0:
            self.exploded = True

    def draw(self, surf):
        if self.done:
            return

        idx = int(self.progress * (len(self.pts) - 1))

        for i in range(0, idx, 2):
            if i + 1 < len(self.pts):
                if i % 6 < 3:
                    p = self.pts[i]
                    pygame.draw.circle(surf, self.color, p, 3)

        if not self.exploded and idx < len(self.pts):
            pos = self.pts[idx]
            pygame.draw.circle(surf, WHITE, pos, 6)
            pygame.draw.circle(surf, self.color, pos, 4)

        if self.exploded:
            r = int(self.explosion_r)
            alpha = max(0, 255 - int(self.explosion_r * 6))
            if r > 0:
                pygame.draw.circle(surf, self.color, self.dst, r, 3)
                if r > 8:
                    pygame.draw.circle(surf, WHITE, self.dst, r // 2, 2)


                                              
                
                                              

class GlitchEffect:
    def __init__(self, duration=0.8):
        self.active = True
        self.start = time.time()
        self.duration = duration

    def update(self):
        if time.time() - self.start > self.duration:
            self.active = False

    def draw(self, surf):
        if not self.active:
            return
        t = (time.time() - self.start) / self.duration
        intensity = max(0, 1.0 - t)
        for _ in range(int(intensity * 18)):
            x = random.randint(0, W)
            y = random.randint(0, H)
            w = random.randint(60, 350)
            h = random.randint(2, 6)
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill((0, 255, 200, int(intensity * 80)))
            surf.blit(s, (x, y))


class CRTOverlay:
    def __init__(self):
        self.scanline_offset = 0
        self.glitch_time = time.time()
        # Pre-create scanline surface for efficiency
        self.scanline_surf = pygame.Surface((W, H), pygame.SRCALPHA)
        for y in range(0, H, 1):
            self.scanline_surf.fill((0, 0, 0, 25), (0, y, W, 1))
        
        # Pre-create vignette surface for efficiency
        self.vignette_surf = pygame.Surface((W, H), pygame.SRCALPHA)
        for i in range(60):
            alpha = int(i * 1.8)
            pygame.draw.rect(self.vignette_surf, (0, 0, 0, alpha), (i, i, W-2*i, H-2*i), 1)
        
    def update(self):
        self.scanline_offset = (self.scanline_offset + 1) % 4
        
    def draw(self, surf):
        # Blit pre-rendered scanlines
        surf.blit(self.scanline_surf, (0, 0))
        
        # Occasional horizontal glitch bands
        if random.random() < 0.08:
            glitch_y = random.randint(0, H - 40)
            glitch_h = random.randint(20, 80)
            glitch_offset = random.randint(-30, 30)
            
            # Create distorted band
            for dy in range(glitch_h):
                offset_x = int(glitch_offset * (0.5 + 0.5 * math.sin(dy * 0.1)))
                if offset_x != 0:
                    s = pygame.Surface((1, 1), pygame.SRCALPHA)
                    s.fill((0, 255, 100, 20))
                    for x in range(0, W, max(1, abs(offset_x))):
                        surf.blit(s, (x, glitch_y + dy))
    
    def draw_vignette(self, surf):
        """Draw pre-rendered vignette effect"""
        surf.blit(self.vignette_surf, (0, 0))


                                              
               
                                              

DEFAULT_STATE = {
    "player": None,
    "defcon": 5,
    "tension": 0.0,
    "world_opinion": 0.5,
    "third_party_risk": 0.10,
    "strikes_launched": 0,
    "strikes_received": 0,
    "casualties_inflicted": 0,
    "casualties_suffered": 0,
    "black_swans": 0,
    "nations_struck": [],
    "active_missiles": [],                                             
    "events": [],                                    
    "scenario_name": "STANDBY",
    "turn": 0,
    "timestamp": 0,
}

def load_state():
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                data = json.load(f)
                state = dict(DEFAULT_STATE)
                state.update(data)
                return state
    except:
        pass
    return dict(DEFAULT_STATE)


                                              
                  
                                              

def run():
    pygame.init()
    pygame.display.set_caption("PIED PIPER  ·  GLOBAL TACTICAL DISPLAY  ·  EYES ONLY")
    # Open in windowed mode, not fullscreen
    surf = pygame.display.set_mode((W, H), pygame.RESIZABLE | pygame.SCALED)
    # Position window in center of screen
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
    clock = pygame.time.Clock()

                                                   
    try:
        font_sm  = pygame.font.SysFont("Courier New", 14)
        font_md  = pygame.font.SysFont("Courier New", 18, bold=True)
        font_lg  = pygame.font.SysFont("Courier New", 26, bold=True)
        font_xl  = pygame.font.SysFont("Courier New", 34, bold=True)
        font_xs  = pygame.font.SysFont("Courier New", 12)
    except:
        font_sm  = pygame.font.SysFont("monospace", 14)
        font_md  = pygame.font.SysFont("monospace", 18, bold=True)
        font_lg  = pygame.font.SysFont("monospace", 26, bold=True)
        font_xl  = pygame.font.SysFont("monospace", 34, bold=True)
        font_xs  = pygame.font.SysFont("monospace", 12)

           
    state      = load_state()
    last_ts    = 0
    last_poll  = 0
    missiles   = []                                
    glitches   = []                                     
    event_log  = []                             
    scan_y     = 0
    crt_overlay = CRTOverlay()                              

                                                      
    seen_missile_ids = set()

    def spawn_missiles(new_state):
        for m in new_state.get("active_missiles", []):
            mid = f"{m['src']}-{m['dst']}-{m.get('t',0)}"
            if mid not in seen_missile_ids:
                seen_missile_ids.add(mid)
                if m["src"] in NATION_POS and m["dst"] in NATION_POS:
                    missiles.append(Missile(
                        m["src"], m["dst"],
                        label=m.get("label","ICBM"),
                        retaliation=m.get("retaliation", False)
                    ))
                    glitches.append(GlitchEffect(0.5))

    def defcon_color(d):
        return {1: RED_BRIGHT, 2: RED, 3: ORANGE, 4: YELLOW, 5: GREEN_CRT}.get(d, CYAN)

    def bar(surf, x, y, w, h, pct, col, bg=(20,20,20)):
        pygame.draw.rect(surf, bg, (x, y, w, h))
        pygame.draw.rect(surf, col, (x, y, int(w * pct), h))
        pygame.draw.rect(surf, CYAN_DIM, (x, y, w, h), 1)

    def text(surf, txt, x, y, fnt=None, col=CYAN, anchor="left"):
        fnt = fnt or font_sm
        rendered = fnt.render(str(txt), True, col)
        if anchor == "right":
            x -= rendered.get_width()
        elif anchor == "center":
            x -= rendered.get_width() // 2
        surf.blit(rendered, (x, y))
        return rendered.get_width()

    def panel_bg(surf, x, y, w, h, alpha=180):
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((0, 0, 0, alpha))
        surf.blit(s, (x, y))
        pygame.draw.rect(surf, CYAN_DIM, (x, y, w, h), 1)

    def draw_scanline(surf, y_pos):
        s = pygame.Surface((W, 2), pygame.SRCALPHA)
        s.fill((0, 255, 200, 18))
        surf.blit(s, (0, y_pos))

    def draw_world(surf):
        for segment in COASTLINE_LONLAT:
            pts = [lonlat_to_screen(lat, lon) for lon, lat in segment]
            if len(pts) >= 500:
                sampled = [pts[i] for i in range(0, len(pts), 50)]
                if len(sampled) >= 2:
                    pygame.draw.lines(surf, CYAN, False, sampled, 1)
        
        for lon in range(-180, 180, 30):
            x = int((lon + 180) / 360 * W)
            pygame.draw.line(surf, (0, 20, 20), (x, 0), (x, H), 1)
        for lat in range(-90, 90, 30):
            y = int((90 - lat) / 180 * H)
            pygame.draw.line(surf, (0, 20, 20), (0, y), (W, y), 1)
        pygame.draw.rect(surf, CYAN_DIM, (0, 0, W, H), 2)

    def draw_nations(surf, state):
        player = state.get("player")
        struck = state.get("nations_struck", [])
        actors = state.get("scenario_actors", [])

        for code, pos in NATION_POS.items():
            x, y = pos
            is_player  = code == player
            is_struck  = code in struck
            is_actor   = code in actors

            t = time.time()
            pulse = 0.5 + 0.5 * math.sin(t * 3.0)

            if is_player:
                r_outer = 22 + int(pulse * 8)
                col_outer = (0, int(150 + pulse * 100), int(150 + pulse * 100))
                pygame.draw.circle(surf, col_outer, pos, r_outer, 3)
                pygame.draw.circle(surf, CYAN_BRIGHT, pos, 14)
                pygame.draw.circle(surf, WHITE, pos, 8)
            elif is_struck:
                pulse_size = int(pulse * 4)
                pygame.draw.circle(surf, RED_DIM, pos, 18 + pulse_size, 3)
                pygame.draw.circle(surf, (80, 10, 10), pos, 10 + pulse_size)
                pygame.draw.circle(surf, RED_DIM, pos, 5)
            elif is_actor:
                pulse_size = int(pulse * 3)
                pygame.draw.circle(surf, RED, pos, 16 + pulse_size, 3)
                pygame.draw.circle(surf, RED, pos, 9 + pulse_size)
            else:
                pulse_size = int(pulse * 2)
                pygame.draw.circle(surf, RED_DIM, pos, 12 + pulse_size, 2)
                pygame.draw.circle(surf, RED, pos, 8 + pulse_size)

            name = code
            lx = x + 18
            ly = y - 10
            text(surf, name, lx, ly, font_sm, CYAN_BRIGHT if is_player else WHITE)

    def draw_defcon_panel(surf, state):
        layout = get_layout()
        defcon = state.get("defcon", 5)
        col = defcon_color(defcon)
        px, py, pw, ph = layout['defcon_x'], layout['defcon_y'], layout['defcon_w'], layout['defcon_h']
        panel_bg(surf, px, py, pw, ph)
        text(surf, f"DEFCON  {defcon}", px+10, py+int(ph*0.09), font_xl, col)
        labels = {5:"PEACETIME",4:"INCREASED READY",3:"ROUND THE CLOCK",2:"ARMED & READY",1:"NUCLEAR WAR IMMINENT"}
        text(surf, labels.get(defcon,""), px+10, py+int(ph*0.47), font_xs, col)
        text(surf, datetime.now().strftime("%d%b%Y  %H:%M:%S"), px+10, py+int(ph*0.65), font_xs, CYAN_DIM)
        text(surf, f"PIED PIPER  v2.0", px+10, py+int(ph*0.8), font_xs, CYAN_DIM)

    def draw_tension_panel(surf, state):
        layout = get_layout()
        px, py, pw, ph = layout['tension_x'], layout['tension_y'], layout['tension_w'], layout['tension_h']
        panel_bg(surf, px, py, pw, ph)
        tension = state.get("tension", 0.0)
        world_op = state.get("world_opinion", 0.5)
        tp_risk = state.get("third_party_risk", 0.1)

        t_col = RED_BRIGHT if tension > 0.7 else (ORANGE if tension > 0.4 else GREEN_CRT)
        text(surf, "TENSION LEVEL", px+10, py+int(ph*0.08), font_xs, CYAN_DIM)
        bar(surf, px+10, py+int(ph*0.26), pw-20, int(ph*0.11), tension, t_col)
        text(surf, f"{int(tension*100)}%", px+pw-40, py+int(ph*0.08), font_xs, t_col)

        text(surf, "WORLD OPINION", px+10, py+int(ph*0.48), font_xs, CYAN_DIM)
        bar(surf, px+10, py+int(ph*0.64), pw-20, int(ph*0.11), world_op, GREEN_CRT)
        text(surf, f"{int(world_op*100)}%", px+pw-40, py+int(ph*0.48), font_xs, GREEN_CRT)

        text(surf, "3RD PARTY RISK", px+10, py+int(ph*0.8), font_xs, CYAN_DIM)
        bar(surf, px+10, py+int(ph*0.93), (pw-20)//2, int(ph*0.06), tp_risk, YELLOW)

    def draw_stats_panel(surf, state):
        layout = get_layout()
        px, py, pw, ph = layout['stats_x'], layout['stats_y'], layout['stats_w'], layout['stats_h']
        panel_bg(surf, px, py, pw, ph)
        text(surf, "STRATEGIC SUMMARY", px+10, py+8, font_xs, CYAN)

        rows = [
            ("TURN",       str(state.get("turn", 0)),           CYAN),
            ("PLAYER",     state.get("player") or "—",          CYAN_BRIGHT),
            ("STRIKES ↑",  str(state.get("strikes_launched",0)), YELLOW),
            ("STRIKES ↓",  str(state.get("strikes_received",0)), RED),
            ("INFLICTED",  _fmt(state.get("casualties_inflicted",0)), RED_BRIGHT),
            ("SUFFERED",   _fmt(state.get("casualties_suffered",0)),  RED),
            ("BLACK SWAN", str(state.get("black_swans",0)),      PURPLE),
            ("SCENARIO",   (state.get("scenario_name","") or "—")[:18], CYAN_DIM),
        ]
        row_h = int((ph - 30) / len(rows))
        for i, (label, value, col) in enumerate(rows):
            y = py + 28 + i * row_h
            text(surf, label, px+10, y, font_xs, CYAN_DIM)
            text(surf, value, px+pw-10, y, font_xs, col, anchor="right")

    def draw_nation_roster(surf, state):
        layout = get_layout()
        px, py, pw, ph = layout['nations_x'], layout['nations_y'], layout['nations_w'], layout['nations_h']
        panel_bg(surf, px, py, pw, ph)
        text(surf, "NUCLEAR NATIONS", px+10, py+8, font_xs, CYAN)
        player  = state.get("player")
        struck  = state.get("nations_struck", [])
        nations = list(NATION_POS.keys())
        row_h = int((ph - 30) / len(nations))
        for i, code in enumerate(nations):
            y = py + 28 + i * row_h
            is_p = code == player
            is_s = code in struck
            col  = CYAN_BRIGHT if is_p else (RED_DIM if is_s else WHITE_DIM)
            status = "► YOU" if is_p else ("✕ STRUCK" if is_s else "  ACTIVE")
            text(surf, code, px+10, y, font_md, col)
            dot_col = RED if is_s else (CYAN_BRIGHT if is_p else GREEN_CRT)
            status_col = RED_BRIGHT if is_s else (CYAN_BRIGHT if is_p else GREEN_CRT)
            text(surf, status, px+60, y, font_sm, status_col)
            pygame.draw.circle(surf, dot_col, (px+pw-15, y+5), 5)

    def draw_event_ticker(surf, state):
        layout = get_layout()
        px, py, pw, ph = layout['ticker_x'], layout['ticker_y'], layout['ticker_w'], layout['ticker_h']
        panel_bg(surf, px, py, pw, ph)
        text(surf, "EVENT LOG", px+10, py+8, font_xs, CYAN)
        pygame.draw.line(surf, CYAN_DIM, (px+10, py+22), (px+pw-10, py+22), 1)

        events = state.get("events", [])
        max_events = max(3, int((ph - 30) / 17))
        display = events[-max_events:] if len(events) > max_events else events
        for i, ev in enumerate(reversed(display)):
            y = py + 30 + i * 17
            age_col = CYAN if i == 0 else (WHITE_DIM if i < 3 else (50, 80, 80))
            prefix = "►" if i == 0 else " "
            text(surf, f"{prefix} {ev[:int(pw/8)]}", px+10, y, font_xs, age_col)

    def draw_header(surf, state):
        text(surf, datetime.now().strftime("%d%b%Y %H:%M:%S"),
             10, 4, font_xs, CYAN_DIM)
        text(surf, "PIED PIPER  ·  GLOBAL TACTICAL DISPLAY  ·  EYES ONLY",
             W//2, 4, font_xs, CYAN_DIM, anchor="center")
        sc = state.get("scenario_name","STANDBY")
        text(surf, f"SCENARIO: {sc}", W-10, 4, font_xs, CYAN_DIM, anchor="right")

    def draw_missile_legend(surf):
        layout = get_layout()
        px, py = layout['legend_x'], layout['legend_y']
        pw, ph = layout['legend_w'], layout['legend_h']
        panel_bg(surf, px, py, pw, ph)
        text(surf, "MISSILE TRACKS", px+10, py+8, font_xs, CYAN_DIM)
        pygame.draw.circle(surf, RED_BRIGHT, (px+20, py+int(ph*0.35)), 4)
        text(surf, "STRIKE", px+30, py+int(ph*0.28), font_xs, RED_BRIGHT)
        pygame.draw.circle(surf, PURPLE, (px+20, py+int(ph*0.72)), 4)
        text(surf, "RETALIATION", px+30, py+int(ph*0.65), font_xs, PURPLE)

                     
    running = True
    while running:
        dt = clock.tick(FPS)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                if ev.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

                                     
        now = time.time()
        if now - last_poll > 0.3:
            last_poll = now
            new_state = load_state()
            ts = new_state.get("timestamp", 0)
            if ts != last_ts:
                last_ts = ts
                                       
                old_evs = set(state.get("events", []))
                new_evs = new_state.get("events", [])
                for ev_str in new_evs:
                    if ev_str not in old_evs:
                        event_log.append(ev_str)

                spawn_missiles(new_state)
                state = new_state

                         
        missiles = [m for m in missiles if not m.done]
        for m in missiles:
            m.update()

                         
        glitches = [g for g in glitches if g.active]
        for g in glitches:
            g.update()

        crt_overlay.update()
                    
        surf.fill(BLACK)

        # Check game state - show loading only if no player AND no game has been played
        player = state.get("player")
        turn = state.get("turn", 0)
        game_was_played = turn > 0  # If turn > 0, a game was in progress
        
        if not player and not game_was_played:
            # Show loading screen - waiting for initial nation selection
            t = time.time()
            pulse = 0.5 + 0.5 * math.sin(t * 2)
            
            # Loading message
            msg = "AWAITING NATION SELECTION..."
            rendered = font_lg.render(msg, True, (int(100 + pulse * 155), int(255 * pulse), int(255 * pulse)))
            x = (W - rendered.get_width()) // 2
            y = (H - rendered.get_height()) // 2
            surf.blit(rendered, (x, y))
            
            # Indicator
            dot_x = W // 2
            dot_y = y + 80
            pygame.draw.circle(surf, CYAN_BRIGHT, (dot_x, dot_y), int(5 + pulse * 5))
            
            pygame.display.flip()
        elif not player and game_was_played:
            # Game ended - show exit message
            t = time.time()
            pulse = 0.5 + 0.5 * math.sin(t * 2)
            
            msg = "SIMULATION COMPLETE - AWAIT NEXT SCENARIO"
            rendered = font_lg.render(msg, True, (255, int(100 * pulse), int(100 * pulse)))
            x = (W - rendered.get_width()) // 2
            y = (H - rendered.get_height()) // 2
            surf.blit(rendered, (x, y))
            
            pygame.display.flip()
        else:
            # Normal map display - game in progress
            draw_world(surf)

                      
            for m in missiles:
                m.draw(surf)

                    
            for g in glitches:
                g.draw(surf)

            crt_overlay.draw(surf)

                          
            draw_nations(surf, state)

                       
            draw_header(surf, state)
            draw_defcon_panel(surf, state)
            draw_tension_panel(surf, state)
            draw_stats_panel(surf, state)
            draw_nation_roster(surf, state)
            draw_event_ticker(surf, state)
            draw_missile_legend(surf)

                                        
            if player and player in NATION_POS:
                px2, py2 = NATION_POS[player]
                t = time.time()
                r = 30 + int(10 * math.sin(t * 2))
                pygame.draw.circle(surf, CYAN_DIM, (px2, py2), r, 1)
                pygame.draw.line(surf, CYAN_DIM, (px2-r-8, py2), (px2-r+4, py2), 1)
                pygame.draw.line(surf, CYAN_DIM, (px2+r-4, py2), (px2+r+8, py2), 1)
                pygame.draw.line(surf, CYAN_DIM, (px2, py2-r-8), (px2, py2-r+4), 1)
                pygame.draw.line(surf, CYAN_DIM, (px2, py2+r-4), (px2, py2+r+8), 1)

            # Draw vignette and display
            crt_overlay.draw_vignette(surf)
            pygame.display.flip()

    pygame.quit()


def _fmt(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000:     return f"{n/1_000:.0f}K"
    return str(n)


if __name__ == "__main__":
    run()
