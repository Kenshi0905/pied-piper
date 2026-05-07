"""
PIED PIPER — Terminal UI Layer
Cross-platform, color-scheme-aware output utilities.
"""
import os, sys, time, random, re

COLOR_SCHEME = "green"

def set_scheme(scheme):
    global COLOR_SCHEME
    COLOR_SCHEME = scheme

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def G(t):
    return f"\033[0;32m{t}\033[0m" if COLOR_SCHEME == "green" else f"\033[0;37m{t}\033[0m"

def B(t):
    return f"\033[1;32m{t}\033[0m" if COLOR_SCHEME == "green" else f"\033[1;37m{t}\033[0m"

def R(t):   return f"\033[1;31m{t}\033[0m"
def Y(t):   return f"\033[1;33m{t}\033[0m"
def C(t):   return f"\033[0;36m{t}\033[0m"
def M(t):   return f"\033[0;35m{t}\033[0m"
def DIM(t): return f"\033[2;32m{t}\033[0m" if COLOR_SCHEME == "green" else f"\033[2;37m{t}\033[0m"

def strip_ansi(s):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', s)

def slow_print(text, delay=0.022, newline=True):
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    if newline: print()

def blink_print(text, times=3, interval=0.45):
    for _ in range(times):
        sys.stdout.write("\r" + B(text)); sys.stdout.flush(); time.sleep(interval)
        sys.stdout.write("\r" + " " * len(strip_ansi(text))); sys.stdout.flush(); time.sleep(interval * 0.4)
    sys.stdout.write("\r" + B(text) + "\n"); sys.stdout.flush()

def scanline(rows=2):
    for _ in range(rows):
        print(DIM("░" * 74)); time.sleep(0.04)
    for _ in range(rows):
        sys.stdout.write("\033[F"); sys.stdout.write(" " * 74 + "\n")

def glitch(text, iters=8):
    chars = "!@#$%^&*<>?|[]{}~`░▒▓█╬╫"
    orig = list(text)
    for _ in range(iters):
        c = ["" + (random.choice(chars) if random.random() < 0.3 else ch) for ch in orig]
        sys.stdout.write("\r" + R("".join(c))); sys.stdout.flush(); time.sleep(0.06)
    sys.stdout.write("\r" + " " * len(text) + "\r"); sys.stdout.flush()

def progress_bar(value, width=22, color_fn=None):
    filled = int(width * value / 100)
    bar = "█" * filled + "░" * (width - filled)
    label = f"[{bar}] {value:5.1f}%"
    if color_fn:
        return color_fn(label)
    if value >= 70: return R(label)
    if value >= 40: return Y(label)
    return G(label)

def box(lines, width=70, title="", title_color=None):
    tc = title_color or B
    border = G("═" * width)
    print(G("╔") + border + G("╗"))
    if title:
        plain_t = strip_ansi(title)
        pad = width - len(plain_t)
        lp = pad // 2; rp = pad - lp
        print(G("║") + " " * lp + tc(plain_t) + " " * rp + G("║"))
        print(G("╠") + border + G("╣"))
    for line in lines:
        plain = strip_ansi(line)
        pad = max(0, width - len(plain))
        print(G("║") + line + " " * pad + G("║"))
    print(G("╚") + border + G("╝"))

def section(title, width=70):
    print(G("╠") + G("═" * width) + G("╣"))
    plain = strip_ansi(title)
    pad = width - len(plain) - 2
    lp = pad // 2; rp = pad - lp
    print(G("║ ") + B(plain) + " " * rp + G(" ║"))
    print(G("╠") + G("═" * width) + G("╣"))

def press_enter(msg="PRESS ENTER TO CONTINUE"):
    input(DIM(f"\n  [{msg}] "))

def typing_effect(lines, delay=0.016):
    for line in lines:
        slow_print(line, delay=delay)
        time.sleep(0.04)

def missile_bar(src, tgt, label="ICBM", width=32):
    print()
    for i in range(width + 1):
        pct = int(100 * i / width)
        bar = "█" * i + "░" * (width - i)
        sys.stdout.write(f"\r  {R('◉')} [{src}→{tgt}] {R(label)} [{bar}] {pct:3d}%")
        sys.stdout.flush()
        time.sleep(0.07)
    print()

def defcon_banner(level):
    labels = {5:"PEACETIME",4:"INCREASED READINESS",3:"ROUND THE CLOCK OPS",2:"ARMED FORCES READY",1:"MAXIMUM FORCE — IMMINENT"}
    colors = {5:G, 4:Y, 3:Y, 2:R, 1:R}
    fn = colors.get(level, G)
    label = labels.get(level, "UNKNOWN")
    print(fn(f"  ▲ DEFCON {level}  ──  {label}"))
