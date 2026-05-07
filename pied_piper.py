                      
"""
╔══════════════════════════════════════════════════╗
║           PIED PIPER SYSTEM  v3.0                ║
║       Classification: EYES ONLY                  ║
║  Powered by: Sigma I-64 · Perla (2022)           ║
║             Desert Crossing AAR · MC '02         ║
╚══════════════════════════════════════════════════╝
"""
import os, sys, time, random, json, subprocess
from pathlib import Path

                      
sys.path.insert(0, str(Path(__file__).parent))

from ui.terminal import (clear, slow_print, blink_print, scanline,
                          glitch, press_enter, box, G, B, R, Y, C, DIM,
                          set_scheme, strip_ansi)

CONFIG_FILE = Path.home() / ".pied_piper_v2.json"

def load_cfg():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f: return json.load(f)
        except: pass
    return {}

def save_cfg(cfg):
    with open(CONFIG_FILE, "w") as f: json.dump(cfg, f)

                                               
             
                                               

LOGO = r"""
  ██████╗ ██╗███████╗██████╗     ██████╗ ██╗██████╗ ███████╗██████╗
  ██╔══██╗██║██╔════╝██╔══██╗    ██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
  ██████╔╝██║█████╗  ██║  ██║    ██████╔╝██║██████╔╝█████╗  ██████╔╝
  ██╔═══╝ ██║██╔══╝  ██║  ██║    ██╔═══╝ ██║██╔═══╝ ██╔══╝  ██╔══██╗
  ██║     ██║███████╗██████╔╝    ██║     ██║██║     ███████╗██║  ██║
  ╚═╝     ╚═╝╚══════╝╚═════╝     ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
"""

SUBTITLE = "  JOINT WAR GAMES AGENCY  ·  CLASSIFICATION: TOP SECRET  ·  v3.0"

                                               
                
                                               

def boot_sequence():
    clear()
    if os.name != "nt":
        os.system("printf '\\033[40m'")
    else:
        os.system(""); sys.stdout.write("\033[40m"); sys.stdout.flush()

    print(B(LOGO))
    print(DIM(SUBTITLE))
    print()
    time.sleep(0.2)

    msgs = [
        ("CRYPTOGRAPHIC MODULES", True),
        ("SECURE CHANNEL", True),
        ("NATION DOCTRINE PROFILES [9 NATIONS]", True),
        ("SIGMA I-64 HISTORICAL DATA (JCS, 1964)", True),
        ("DESERT CROSSING AAR (NSAEBB207, 1999)", True),
        ("MILLENNIUM CHALLENGE 2002 DATASET", True),
        ("BAYESIAN PROBABILITY ENGINE", True),
        ("BLACK SWAN MODULE", True),
        ("SCENARIO GENERATOR [7 FLASHPOINTS]", True),
        ("ARCADE SUBSYSTEM [6 GAMES]", True),
        ("SYSTEM READY.", False),
    ]
    for label, has_dots in msgs:
        if has_dots:
            dots = "." * (48 - len(label))
            slow_print(G(f"  LOADING {label} {dots} [OK]"), delay=0.010)
        else:
            time.sleep(0.2)
            slow_print(B(f"  {label}"), delay=0.018)
        time.sleep(random.uniform(0.03, 0.12))
    print()
    scanline(2)
    time.sleep(0.3)

                                               
        
                                               

def logon_screen(cfg):
    if "logon_id" in cfg:
        lid = cfg["logon_id"]
        print(G(f"\n  LOGON: ") + B(lid))
        slow_print(G("  IDENTITY CONFIRMED."), delay=0.020)
        time.sleep(0.3)
        return lid
    else:
        print()
        slow_print(G("  FIRST ACCESS — IDENTITY REGISTRATION"), delay=0.018)
        time.sleep(0.2)
        slow_print(G("  ENTER LOGON ID — ENTER SOMETHING YOU LOVE:"), delay=0.018)
        print()
        lid = input(B("  > ")).strip().upper() or "ANONYMOUS"
        cfg["logon_id"] = lid
        save_cfg(cfg)
        slow_print(G(f"\n  LOGON [{lid}] REGISTERED PERMANENTLY."), delay=0.016)
        slow_print(G("  WELCOME, OPERATOR."), delay=0.018)
        time.sleep(0.3)
        return lid

                                               
               
                                               

def color_menu(cfg):
    print()
    print(G("  DISPLAY MODE:"))
    print(G("    [1]  GREEN ON BLACK  (default)"))
    print(G("    [2]  WHITE ON BLACK"))
    print()
    ch = input(DIM("  SELECT [1/2, ENTER to keep]: ")).strip()
    if ch == "2":
        cfg["color"] = "white"; set_scheme("white")
    elif ch == "1":
        cfg["color"] = "green"; set_scheme("green")
    save_cfg(cfg)
    print(G(f"  DISPLAY MODE SET: {cfg.get('color','green').upper()}"))
    time.sleep(0.6)

                                               
                         
                                               

def tic_tac_toe_egg():
    clear()
    time.sleep(0.2)
    slow_print(R("  ACCESSING TIC TAC TOE MODULE ..."), delay=0.022)
    time.sleep(0.4)
    slow_print(R("  WARNING: RESTRICTED SIMULATION DETECTED"), delay=0.018)
    time.sleep(0.3)

    cascade = [
        "  DEFCON STATUS: CHANGING ...............",
        "  LAUNCH AUTHORITY: COMPROMISED .........",
        "  MISSILE SYSTEMS: RESPONDING ...........",
        "  NORAD ALERT LEVEL: CRITICAL ...........",
        "  SIGMA SCENARIO: UNCONTROLLED ..........",
        "  SYSTEM INTEGRITY: CATASTROPHIC FAILURE.",
    ]
    for w in cascade:
        glitch(w)
        slow_print(R(w), delay=0.012)
        time.sleep(random.uniform(0.10, 0.28))

    print()
                           
    WIDTH = 30
    for i in range(WIDTH + 1):
        bar = "█" * i + "░" * (WIDTH - i)
        pct = int(100 * i / WIDTH)
        sys.stdout.write(f"\r  {R('◉')} ICBM TRAJECTORY [{bar}] {pct:3d}%")
        sys.stdout.flush()
        time.sleep(0.07)
    print()

    time.sleep(0.3)
    print()
    slow_print(R("  RUNNING 1,437 THERMONUCLEAR SCENARIOS ..."), delay=0.016)
    time.sleep(0.8)

    for _ in range(4):
        glitch("  NO WINNERS DETECTED IN ANY SCENARIO.")
        time.sleep(0.08)
    slow_print(R("  NO WINNERS DETECTED IN ANY SCENARIO."), delay=0.012)
    time.sleep(0.4)

    print()
    blink_print("  A STRANGE GAME.", times=4, interval=0.50)
    time.sleep(0.3)
    blink_print("  THE ONLY WINNING MOVE IS NOT TO PLAY.", times=3, interval=0.60)
    time.sleep(0.5)

    print()
    slow_print(DIM("  — Sigma I-64 (1964): results not passed to President Johnson."), delay=0.010)
    slow_print(DIM("    The war continued for eleven more years."), delay=0.010)
    print()
    slow_print(R("  PIED PIPER SYSTEM SHUTTING DOWN ..."), delay=0.018)

    for i in range(15, 0, -1):
        sys.stdout.write(f"\r" + R(f"  TERMINATING IN {i:02d} ..."))
        sys.stdout.flush()
        time.sleep(0.18)

    clear()
    print()
    print(R("  CONNECTION TERMINATED."))
    time.sleep(0.8)
    sys.exit(0)

                                               
         
                                               

def logout(logon):
    clear()
    slow_print(G(f"\n  LOGGING OUT OPERATOR: {logon}"), delay=0.018)
    time.sleep(0.3)
    slow_print(G("  PURGING SESSION DATA ..."), delay=0.014)
    time.sleep(0.3)
    slow_print(G("  PIED PIPER SYSTEM OFFLINE."), delay=0.018)
    time.sleep(0.2)
    print(); print(DIM("  GOODBYE."))
    time.sleep(0.4)

                                               
            
                                               

def main_menu(logon, cfg):
    from games.arcade import (game_chess, game_sudoku, game_poker,
                               game_hangman, game_minesweeper, game_number_guess)
    from games.war_game import game_thermonuclear_war

    while True:
        clear()
        print(B(LOGO))
        print(G(f"  OPERATOR: {logon}") + "     " + DIM("CLASSIFICATION: TOP SECRET"))
        print()

        menu_lines = [
            f"  {B('SHALL WE PLAY A GAME?')}",
            "",
            f"  {G('[1]')}  CHESS",
            f"  {G('[2]')}  SUDOKU",
            f"  {G('[3]')}  POKER",
            f"  {G('[4]')}  HANGMAN",
            f"  {G('[5]')}  MINESWEEPER",
            f"  {G('[6]')}  NUMBER GUESS",
            "",
            f"  {R('[7]')}  {B('GLOBAL THERMONUCLEAR WAR')}",
            "",
            f"  {G('[C]')}  CHANGE DISPLAY MODE",
            f"  {G('[Q]')}  LOGOUT",
            "",
            f"  {DIM('(or type a game name directly)')}",
        ]
        box(menu_lines, width=44, title="PIED PIPER  ·  MAIN MENU")
        print()

        cmd = input(B("  PIED PIPER> ")).strip().upper()

        if cmd in ["1", "CHESS"]:
            game_chess()
        elif cmd in ["2", "SUDOKU"]:
            game_sudoku()
        elif cmd in ["3", "POKER"]:
            game_poker()
        elif cmd in ["4", "HANGMAN"]:
            game_hangman()
        elif cmd in ["5", "MINESWEEPER"]:
            game_minesweeper()
        elif cmd in ["6", "NUMBER", "NUMBER GUESS"]:
            game_number_guess()
        elif cmd in ["7", "GLOBAL THERMONUCLEAR WAR", "GTW", "WAR", "THERMONUCLEAR"]:
                                                   
            try:
                _map_proc = subprocess.Popen(
                    [sys.executable, str(Path(__file__).parent / "map_window.py")],
                    cwd=str(Path(__file__).parent)
                )
            except Exception as _e:
                print(G(f"  [MAP WINDOW] Could not launch: {_e}"))
                _map_proc = None
            game_thermonuclear_war(logon)
        elif cmd in ["TIC TAC TOE", "TICTACTOE", "TTT", "TIC-TAC-TOE"]:
            tic_tac_toe_egg()
        elif cmd == "C":
            color_menu(cfg)
        elif cmd in ["Q", "QUIT", "EXIT", "LOGOUT"]:
            logout(logon)
            break
        else:
            print(R("  COMMAND NOT RECOGNIZED."))
            time.sleep(0.7)

                                               
              
                                               

def main():
    cfg = load_cfg()
                              
    scheme = cfg.get("color", "green")
    set_scheme(scheme)

    boot_sequence()
    logon = logon_screen(cfg)
    time.sleep(0.4)
    main_menu(logon, cfg)
    print()

if __name__ == "__main__":
    main()