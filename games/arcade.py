"""
PIED PIPER — Arcade Games Module
Chess, Sudoku, Poker, Hangman, Minesweeper, Number Guess
"""
import random, time, sys
import chess
from ui.terminal import (clear, slow_print, press_enter, box,
                          G, B, R, Y, C, DIM, progress_bar)

                                               
        
                                               

def game_chess():
    clear()
    print(B("\n  ♟  CHESS — TEXT TERMINAL MODE\n"))
    slow_print(G("  You play WHITE. Moves: e2e4 or SAN (e4, Nf3, O-O)."), delay=0.014)
    slow_print(G("  Commands: 'moves' = legal moves  'resign' = quit  'quit' = exit\n"), delay=0.014)

    board = chess.Board()

    def draw(b):
        print()
        print(G("     a   b   c   d   e   f   g   h"))
        print(G("   ┌───┬───┬───┬───┬───┬───┬───┬───┐"))
        for rank in range(7, -1, -1):
            row = G(f"  {rank+1}│")
            for file in range(8):
                sq  = chess.square(file, rank)
                pc  = b.piece_at(sq)
                dark = (rank + file) % 2 == 0
                if pc:
                    sym = pc.symbol()
                    row += (B(f" {sym} ") if pc.color == chess.WHITE else R(f" {sym} "))
                else:
                    row += (DIM(" · ") if dark else G("   "))
                row += G("│")
            row += G(f" {rank+1}")
            print(row)
            if rank > 0:
                print(G("   ├───┼───┼───┼───┼───┼───┼───┼───┤"))
        print(G("   └───┴───┴───┴───┴───┴───┴───┴───┘"))
        print(G("     a   b   c   d   e   f   g   h\n"))

    def cpu(b):
        captures = [m for m in b.legal_moves if b.is_capture(m)]
        if captures:
            return max(captures, key=lambda m: (b.piece_at(m.to_square).piece_type if b.piece_at(m.to_square) else 0))
        checks = [m for m in b.legal_moves if b.gives_check(m)]
        if checks: return random.choice(checks)
        center = {chess.E4,chess.E5,chess.D4,chess.D5,chess.C3,chess.F3,chess.C6,chess.F6}
        c_moves = [m for m in b.legal_moves if m.to_square in center]
        return random.choice(c_moves) if c_moves else random.choice(list(b.legal_moves))

    while not board.is_game_over():
        draw(board)
        if board.turn == chess.WHITE:
            chk = " CHECK!" if board.is_check() else ""
            print(G("  YOUR TURN (WHITE)" + chk))
            cmd = input(B("  Move> ")).strip().lower()
            if cmd == "quit": return
            if cmd == "resign":
                print(R("  YOU RESIGNED.")); press_enter(); return
            if cmd == "moves":
                print(G("  Legal: ") + ", ".join(board.san(m) for m in board.legal_moves))
                continue
            try:
                m = chess.Move.from_uci(cmd)
                if m not in board.legal_moves: raise ValueError
                board.push(m)
            except:
                try: board.push(board.parse_san(cmd))
                except: print(R("  INVALID MOVE."))
        else:
            print(G("  CPU COMPUTING...")); time.sleep(random.uniform(0.4, 1.0))
            m = cpu(board)
            print(G(f"  CPU: {board.san(m)}")); board.push(m); time.sleep(0.3)

    draw(board)
    r = board.result()
    if r == "1-0": print(B("  ★ YOU WIN — CHECKMATE!"))
    elif r == "0-1": print(R("  CPU WINS — CHECKMATE."))
    else: print(Y("  DRAW."))
    press_enter()


                                               
         
                                               

def game_sudoku():
    def make():
        base = 3; side = 9
        def pat(r,c): return (base*(r%base)+r//base+c)%side
        def shuf(s): return random.sample(s,len(s))
        rBase=range(base)
        rows=[g*base+r for g in shuf(rBase) for r in shuf(rBase)]
        cols=[g*base+c for g in shuf(rBase) for c in shuf(rBase)]
        nums=shuf(range(1,side+1))
        board=[[nums[pat(r,c)] for c in cols] for r in rows]
        for p in random.sample(range(81), 45):
            board[p//9][p%9]=0
        return board

    def draw(b, orig):
        print()
        print(G("     1   2   3   4   5   6   7   8   9"))
        print(G("   ┌───────────┬───────────┬───────────┐"))
        for i,row in enumerate(b):
            r=G(f"  {i+1}│")
            for j,v in enumerate(row):
                if v==0: r+=DIM(" · ")
                elif orig[i][j]==0: r+=Y(f" {v} ")
                else: r+=G(f" {v} ")
                if j in [2,5]: r+=G("│")
                elif j<8: r+=DIM("·")
            r+=G("│"); print(r)
            if i in [2,5]: print(G("   ├───────────┼───────────┼───────────┤"))
            elif i<8: print(DIM("   ·"+" "*33+"·"))
        print(G("   └───────────┴───────────┴───────────┘\n"))

    def valid(b,r,c,n):
        if n in b[r]: return False
        if n in [b[x][c] for x in range(9)]: return False
        br,bc=3*(r//3),3*(c//3)
        return not any(b[br+dr][bc+dc]==n for dr in range(3) for dc in range(3))

    clear(); print(B("\n  ■ SUDOKU\n"))
    slow_print(G("  ROW COL VALUE to place (e.g. '5 3 7'). 'quit' to exit.\n"), delay=0.014)
    board=make(); orig=[r[:] for r in board]

    while True:
        draw(board,orig)
        if all(board[r][c]!=0 for r in range(9) for c in range(9)):
            print(B("  ★ PUZZLE SOLVED!")); press_enter(); return
        cmd=input(B("  Input> ")).strip().lower()
        if cmd=="quit": return
        try:
            p=cmd.split(); r,c,v=int(p[0])-1,int(p[1])-1,int(p[2])
            if orig[r][c]!=0: print(R("  ORIGINAL CELL."))
            elif not 1<=v<=9: print(R("  VALUE 1-9 ONLY."))
            elif not valid(board,r,c,v): print(R("  INVALID PLACEMENT."))
            else: board[r][c]=v
        except: print(R("  FORMAT: ROW COL VALUE"))
        time.sleep(0.2)


                                               
                      
                                               

def game_poker():
    SUITS=["♠","♥","♦","♣"]
    RANKS=["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    RV={r:i for i,r in enumerate(RANKS)}

    def deck(): return [(r,s) for s in SUITS for r in RANKS]

    def card_s(c):
        r,s=c
        return (R(f"{r}{s}") if s in["♥","♦"] else G(f"{r}{s}"))

    def hand_s(h): return "  "+"  ".join(card_s(c) for c in h)

    def rank_hand(h):
        from collections import Counter
        rv=[RV[c[0]] for c in h]; suits=[c[1] for c in h]
        flush=len(set(suits))==1
        sr=sorted(rv,reverse=True)
        straight=(max(sr)-min(sr)==4 and len(set(sr))==5)
        if rv==[12,3,2,1,0]: straight=True; sr=[3,2,1,0,-1]
        cnt=Counter(rv); vals=sorted(cnt.values(),reverse=True)
        grp=sorted(cnt.keys(),key=lambda x:(cnt[x],x),reverse=True)
        if straight and flush: return (8,sr)
        if vals[0]==4: return (7,grp)
        if vals[:2]==[3,2]: return (6,grp)
        if flush: return (5,sr)
        if straight: return (4,sr)
        if vals[0]==3: return (3,grp)
        if vals[:2]==[2,2]: return (2,grp)
        if vals[0]==2: return (1,grp)
        return (0,sr)

    NAMES={8:"STRAIGHT FLUSH",7:"FOUR OF A KIND",6:"FULL HOUSE",
           5:"FLUSH",4:"STRAIGHT",3:"THREE OF A KIND",
           2:"TWO PAIR",1:"ONE PAIR",0:"HIGH CARD"}

    def cpu_disc(h):
        from collections import Counter
        rv=[RV[c[0]] for c in h]; cnt=Counter(rv)
        keep={r for r,c in cnt.items() if c>=2}
        if not keep:
            keep={sorted(rv,reverse=True)[0]}
        return [i for i,c in enumerate(h) if RV[c[0]] not in keep]

    clear(); print(B("\n  ♠ FIVE-CARD DRAW POKER\n"))
    slow_print(G("  100 chips. Ante 5/round. Discard by position (e.g. '1 3') or 'keep'.\n"), delay=0.014)

    you=100; cpu=100; rnd=0
    while you>0 and cpu>0:
        rnd+=1
        if you<5 or cpu<5: break
        print(G(f"\n  ── ROUND {rnd} ──  You: {Y(str(you))}  CPU: {Y(str(cpu))}"))
        you-=5; cpu-=5; pot=10
        d=deck(); random.shuffle(d)
        yh=d[:5]; ch=d[5:10]; d=d[10:]

        print(G("\n  YOUR HAND:")); print(hand_s(yh)); print()
        print(G("  Discard positions (e.g. '1 3 5') or 'keep':"))
        di=input(B("  > ")).strip().lower()
        if di not in["keep",""]:
            try:
                idx=[int(x)-1 for x in di.split() if 0<=int(x)-1<5]
                for i in sorted(set(idx),reverse=True): yh[i]=d.pop(0)
            except: pass

        ci=cpu_disc(ch)
        for i in sorted(set(ci),reverse=True): ch[i]=d.pop(0)
        print(G(f"\n  CPU DISCARDED {len(ci)}."))

        print(G("\n  YOUR FINAL HAND:")); print(hand_s(yh)); print()
        print(G("  BET (0 to check):"))
        try: bet=max(0,min(int(input(B("  > ")).strip()),you))
        except: bet=0
        you-=bet; pot+=bet

        yr=rank_hand(yh)[0]
        if yr>=2 or bet==0:
            cb=min(bet,cpu); cpu-=cb; pot+=cb; print(G(f"  CPU CALLS {cb}."))
        else:
            print(G("  CPU FOLDS.")); you+=pot
            print(B(f"  YOU WIN POT: {pot}!")); press_enter("NEXT ROUND"); continue

        print(G("\n  ── SHOWDOWN ──"))
        print(G("  YOUR HAND: ")+hand_s(yh)+G(f"  [{NAMES[rank_hand(yh)[0]]}]"))
        print(G("  CPU HAND:  ")+hand_s(ch) +G(f"  [{NAMES[rank_hand(ch)[0]]}]"))
        pr=rank_hand(yh); cr=rank_hand(ch)
        if pr>cr: you+=pot; print(B(f"  ★ YOU WIN: {pot}!"))
        elif cr>pr: cpu+=pot; print(R(f"  CPU WINS: {pot}."))
        else:
            you+=pot//2; cpu+=pot//2; print(Y("  SPLIT POT."))

        press_enter("NEXT ROUND")
        if you<=0: print(R("\n  OUT OF CHIPS.")); break
        if cpu<=0: print(B("\n  ★ CPU IS BROKE. YOU WIN!")); break
        if input(G("  Continue? [Y/N]: ")).strip().upper()!="Y": break

    print(G(f"\n  FINAL — You: {you}  CPU: {cpu}")); press_enter()


                                               
          
                                               

HANGMAN_WORDS = [
    "NUCLEAR","DETERRENCE","ESCALATION","MISSILE","SUBMARINE","CLASSIFIED",
    "PROTOCOL","WARHEAD","SATELLITE","CRYPTOGRAPHY","INFILTRATE","TRAJECTORY",
    "INTERCEPT","DEFCON","BUNKER","INTELLIGENCE","PERIMETER","OVERRIDE",
    "FREQUENCY","DETONATOR","PROLIFERATION","PREEMPTION","COUNTERFORCE",
    "SUFFICIENCY","TRIDENT","MINUTEMAN","POSEIDON","RETALIATION","DOCTRINE",
]

GALLOWS = [
    ["       ","       ","       ","       ","       ","       "],
    ["  ┌────","  │    ","  │    ","  │    ","  │    ","──┘────"],
    ["  ┌────","  │   │","  │    ","  │    ","  │    ","──┘────"],
    ["  ┌────","  │   │","  │   ○","  │    ","  │    ","──┘────"],
    ["  ┌────","  │   │","  │   ○","  │   │","  │    ","──┘────"],
    ["  ┌────","  │   │","  │   ○","  │  /│","  │    ","──┘────"],
    ["  ┌────","  │   │","  │   ○","  │  /│\\","  │    ","──┘────"],
    ["  ┌────","  │   │","  │   ○","  │  /│\\","  │  / ","──┘────"],
    ["  ┌────","  │   │","  │   ○","  │  /│\\","  │  / \\","──┘────"],
]

def game_hangman():
    clear(); print(B("\n  ☠  HANGMAN — CLASSIFIED LEXICON\n"))
    word=random.choice(HANGMAN_WORDS); guessed=set(); wrong=0; MAX=8

    while wrong<MAX:
        clear(); print(B("\n  ☠  HANGMAN\n"))
        for line in GALLOWS[wrong]: print(R(f"  {line}"))
        print()
        display=" ".join(c if c in guessed else "_" for c in word)
        print(G(f"  WORD: {B(display)}\n"))
        bad=sorted(guessed-set(word))
        if bad: print(R(f"  WRONG [{wrong}/{MAX}]: {' '.join(bad)}"))
        print()
        if all(c in guessed for c in word):
            print(B(f"  ★ CORRECT! THE WORD: {word}")); press_enter(); return
        g=input(B("  Letter (or 'quit'): ")).strip().upper()
        if g=="QUIT": return
        if len(g)!=1 or not g.isalpha(): print(R("  SINGLE LETTER.")); time.sleep(0.4); continue
        if g in guessed: print(Y("  ALREADY GUESSED.")); time.sleep(0.4); continue
        guessed.add(g)
        if g not in word: wrong+=1; print(R(f"  '{g}' NOT IN WORD.")); time.sleep(0.4)

    clear()
    for line in GALLOWS[MAX]: print(R(f"  {line}"))
    print(R(f"\n  ☠  EXECUTED. WORD WAS: {B(word)}")); press_enter()


                                               
              
                                               

def game_minesweeper():
    R_S,C_S,M_S=9,9,10

    def make():
        b=[[0]*C_S for _ in range(R_S)]; mines=set()
        while len(mines)<M_S:
            mines.add((random.randint(0,R_S-1),random.randint(0,C_S-1)))
        for (r,c) in mines:
            b[r][c]=-1
            for dr in[-1,0,1]:
                for dc in[-1,0,1]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<R_S and 0<=nc<C_S and b[nr][nc]!=-1: b[nr][nc]+=1
        return b,mines

    def draw(b,rev,flag,mines=None,gg=False):
        print()
        print(G("     "+"  ".join(str(i+1) for i in range(C_S))))
        print(G("   ┌"+"───"*C_S+"┐"))
        for r in range(R_S):
            row=G(f"  {chr(65+r)}│")
            for c in range(C_S):
                if gg and (r,c) in (mines or set()): row+=R(" * ")
                elif (r,c) in flag: row+=Y(" F ")
                elif (r,c) not in rev: row+=DIM(" ░ ")
                else:
                    v=b[r][c]
                    if v==0: row+=G("   ")
                    elif v==-1: row+=R(" * ")
                    else:
                        fn=[None,G,Y,R,R,R,C,C,C][min(v,8)]
                        row+=(fn or G)(f" {v} ")
                row+=G("│")
            print(row)
        print(G("   └"+"───"*C_S+"┘\n"))

    def reveal(b,rev,r,c):
        if (r,c) in rev or not(0<=r<R_S and 0<=c<C_S): return
        rev.add((r,c))
        if b[r][c]==0:
            for dr in[-1,0,1]:
                for dc in[-1,0,1]: reveal(b,rev,r+dr,c+dc)

    clear(); print(B("\n  ✦ MINESWEEPER\n"))
    slow_print(G("  A1 = reveal  FA1 = flag/unflag  quit = exit\n"), delay=0.014)
    b,mines=make(); rev=set(); flag=set(); safe=R_S*C_S-M_S

    while True:
        draw(b,rev,flag)
        print(G(f"  Mines: {Y(str(M_S-len(flag)))}  Safe revealed: {len(rev)}/{safe}"))
        if len(rev)==safe: print(B("  ★ FIELD CLEARED!")); press_enter(); return
        cmd=input(B("  > ")).strip().upper()
        if cmd=="QUIT": return
        fl=cmd.startswith("F"); coord=cmd[1:] if fl else cmd
        if len(coord)<2: print(R("  Format: A1")); time.sleep(0.4); continue
        try:
            r=ord(coord[0])-ord('A'); c=int(coord[1:])-1
            assert 0<=r<R_S and 0<=c<C_S
        except: print(R("  OUT OF BOUNDS.")); time.sleep(0.4); continue
        if fl:
            if (r,c) in flag: flag.remove((r,c))
            else: flag.add((r,c))
        else:
            if (r,c) in rev: continue
            if b[r][c]==-1:
                draw(b,rev,flag,mines,gg=True)
                print(R("  ☠  MINE DETONATED.")); press_enter(); return
            reveal(b,rev,r,c)


                                               
               
                                               

def game_number_guess():
    clear(); print(B("\n  ? NUMBER GUESS\n"))
    slow_print(G("  I am thinking of a number 1-100. You have 7 attempts.\n"), delay=0.014)
    n=random.randint(1,100)
    for att in range(1,8):
        try: g=int(input(B(f"  Attempt {att}/7 > ")))
        except: print(R("  NUMBERS ONLY.")); continue
        if g==n: print(B(f"\n  ★ CORRECT! Solved in {att} attempt(s).")); press_enter(); return
        print(Y("  TOO LOW.") if g<n else Y("  TOO HIGH."))
    print(R(f"\n  OUT OF ATTEMPTS. Number was {n}.")); press_enter()
