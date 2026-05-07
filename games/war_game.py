"""
PIED PIPER — Global Thermonuclear War
Full scenario-driven war game with:
- Bayesian probability engine (Sigma I-64, Perla, Desert Crossing, MC '02)
- Dynamic scenario generation across 7 global flashpoints
- All 9 nuclear-armed nations playable
- Animated map with missile trajectories
- Full event log / after-action report
- Diplomatic, covert, conventional, and nuclear action tracks
"""
import sys, time, random
from ui.terminal import (clear, slow_print, press_enter, box, section,
                          G, B, R, Y, C, DIM, M, glitch, blink_print,
                          missile_bar, defcon_banner, progress_bar, typing_effect)
from ui.map_renderer import animate_strike  # print_map disabled - using graphical map_window
from engine.nations import NATIONS, NATION_KEYS
from engine.probability import (calculate, resolve_outcome, GameState,
                                 DOCTRINE_SCENARIOS)
from engine.scenarios import generate_scenario, get_all_flashpoints
from engine.state_bridge import push as push_state, clear_state

WIDTH = 62

def _fmt_millions(n):
    if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if n >= 1_000: return f"{n/1_000:.0f}K"
    return str(n)

                                                 
               
                                                 

def war_intro():
    clear()
    lines = [
        R("  ██████████████████████████████████████████████████████████"),
        R("  ██                                                      ██"),
        R("  ██     G L O B A L   T H E R M O N U C L E A R          ██"),
        R("  ██                W A R                                 ██"),
        R("  ██                                                      ██"),
        R("  ██████████████████████████████████████████████████████████"),
    ]
    for line in lines:
        slow_print(line, delay=0.006)
    print()
    time.sleep(0.3)
    boot_msgs = [
        "  LOADING NATION DOCTRINE PROFILES .............. [OK]",
        "  CALIBRATING BAYESIAN PROBABILITY ENGINE ....... [OK]",
        "  LOADING SIGMA I-64 HISTORICAL DATA ............ [OK]",
        "  LOADING DESERT CROSSING AAR (1999) ............ [OK]",
        "  LOADING MILLENNIUM CHALLENGE DATA .............. [OK]",
        "  INITIALIZING FLASHPOINT SCENARIO GENERATOR .... [OK]",
        "  MOUNTING ARSENAL AND TARGETING DATABASE ........ [OK]",
        "  BLACK SWAN MODULE ARMED ........................ [OK]",
        "  SYSTEM READY.",
    ]
    for m in boot_msgs:
        slow_print(G(m), delay=0.012)
        time.sleep(random.uniform(0.05, 0.15))
    print()
    time.sleep(0.4)

                                                 
                
                                                 

def select_nation():
    clear()
    print(B("\n  ◈ SELECT YOUR NATION\n"))
    keys = list(NATIONS.keys())
    for i, k in enumerate(keys):
        n = NATIONS[k]
        wbar = "█" * min(int(n["warheads"] / 300), 18) + "░" * max(0, 18 - int(n["warheads"] / 300))
        ready = progress_bar(n["readiness"], width=10)
        print(G(f"  [{i+1:2d}]") + f"  {B(k):6s}  {DIM(n['full'][:32]):35s}  "
              f"{Y(str(n['warheads'])):7s}  {G(wbar)}")
        print(f"        {DIM(n['doctrine'][:52])}")
        print(f"        Readiness: {ready}   Intel: {progress_bar(n['intel_score'],width=8)}")
        print()
    while True:
        try:
            sel = int(input(B("  SELECT [1-9] > "))) - 1
            if 0 <= sel < len(keys):
                return keys[sel]
        except: pass
        print(R("  INVALID."))

                                                 
                    
                                                 

def scenario_briefing(scenario, player):
    clear()
    fp = scenario["flashpoint"]
    print(B(f"\n  ◈ SCENARIO BRIEFING — {fp['name']}\n"))
    print(G(f"  REGION:       {Y(fp['region'])}"))
    print(G(f"  YOUR ROLE:    {Y(scenario['player_role'])}"))
    print(G(f"  ACTORS:       {Y(', '.join(scenario['actors']))}"))
    print()
    print(G("  SITUATION:"))
    slow_print(Y(f"  {fp['trigger']}"), delay=0.014)
    print()
    print(G("  HISTORICAL PARALLEL:"))
    slow_print(DIM(f"  {fp['sigma_ref']}"), delay=0.012)
    print()
    print(G(f"  STARTING DEFCON: {R(str(fp['defcon_start']))}"))
    print(G(f"  TENSION LEVEL:  {Y(str(int(fp['tension_start']*100))+'%')}"))
    print()
    press_enter("BEGIN SIMULATION")

                                                 
                            
                                                 

def draw_hud(gs, scenario):
    clear()
    n = NATIONS[gs.player]
    fp = scenario["flashpoint"]

           
    print(B(f"\n  PIED PIPER :: GLOBAL THERMONUCLEAR WAR :: TURN {gs.turn:02d}\n"))

                   
    defcon_banner(gs.defcon)
    print()

         
    struck = gs.nations_struck
    actors = scenario["actors"]
    # ASCII map disabled - using graphical map_window instead
    # print_map(NATIONS, player=gs.player, highlights=actors, strikes=struck)
    print()

                  
    status = [
        f"  NATION:      {B(gs.player)} — {DIM(n['full'][:30])}",
        f"  WARHEADS:    {Y(str(n['warheads']))}",
        f"  READINESS:   {progress_bar(n['readiness'])}",
        f"  INTEL:       {progress_bar(n['intel_score'])}",
        "",
        f"  TENSION:     {progress_bar(int(gs.tension_level*100), color_fn=R if gs.tension_level > 0.6 else Y)}",
        f"  3RD PARTY:   {progress_bar(int(gs.third_party_risk*100))}",
        f"  WORLD OPN:   {progress_bar(int(gs.world_opinion*100), color_fn=G)}",
        "",
        f"  STRIKES:     {Y(str(gs.strikes_launched))} launched  {R(str(gs.strikes_received))} received",
        f"  CASUALTIES:  Inflicted {R(_fmt_millions(gs.casualties_inflicted))}  "
                       f"Suffered {R(_fmt_millions(gs.casualties_suffered))}",
        f"  BLACK SWANS: {R(str(len(gs.black_swans)))} detected",
        f"  SCENARIO:    {DIM(fp['name'][:40])}",
    ]
    box(status, width=WIDTH, title="STRATEGIC STATUS")
    print()

                   
    allies = n.get("allies", [])
    if allies:
        ally_line = "  ALLIES: " + "  ".join(
            f"{B(a)} {progress_bar(NATIONS[a]['readiness'], width=8)}" for a in allies
        )
        print(G(ally_line))
        print()

                                                 
              
                                                 

def action_menu():
    actions = [
        f"  {R('[1]')} NUCLEAR / ICBM STRIKE",
        f"  {R('[2]')} AIR STRIKE (BOMBER / SLBM)",
        f"  {G('[3]')} CONVENTIONAL ASSAULT",
        f"  {C('[4]')} COVERT OPERATION",
        f"  {G('[5]')} DIPLOMATIC SIGNAL",
        f"  {G('[6]')} INTELLIGENCE OPERATION",
        f"  {Y('[7]')} RAISE / LOWER DEFCON",
        f"  {G('[8]')} STAND DOWN FORCES",
        f"  {B('[I]')} INTEL BRIEFING — NATION",
        f"  {B('[H]')} HISTORICAL DOCTRINE BROWSER",
        f"  {B('[S]')} SCENARIO REPORT",
        f"  {B('[L]')} EVENT LOG",
        f"  {DIM('[Q]')} ABORT SIMULATION",
    ]
    box(actions, width=44, title="ACTION CONSOLE")
    print()

                                                 
                  
                                                 

def launch_sequence(gs, action_type, strike_label, scenario):
    """Full launch: target select → probability display → confirm → resolve → aftermath."""
    actors = [k for k in scenario["actors"] if k != gs.player]
    all_targets = [k for k in NATION_KEYS if k != gs.player]

    clear()
    print(B(f"\n  ◉ {strike_label} — SELECT TARGET\n"))

    for i, k in enumerate(all_targets):
        tn = NATIONS[k]
        probs = calculate(gs.player, k, action_type, gs)
        hot = k in actors
        tag = Y("  [SCENARIO ACTOR]") if hot else ""
        print(G(f"  [{i+1:2d}]") + f"  {B(k)}  {DIM(tn['full'][:30])}{tag}")
        print(f"        {G('Success:')} {progress_bar(probs['success'])}  "
              f"{R('Retaliation:')} {progress_bar(probs['retaliation'])}  "
              f"{Y('3rdParty:')} {progress_bar(probs['third_party'])}")
        print()

    print()
    try:
        sel = int(input(B("  TARGET [1-8] or 0 to cancel > "))) - 1
        if sel < 0 or sel >= len(all_targets):
            return
        target = all_targets[sel]
    except:
        return

                              
    probs = calculate(gs.player, target, action_type, gs)
    clear()
    print(B(f"\n  ◉ AUTHORIZATION: {gs.player} → {target}  [{strike_label}]\n"))

    prob_lines = [
        f"  STRIKE SUCCESS:        {progress_bar(probs['success'])}",
        f"  RETALIATION RISK:      {progress_bar(probs['retaliation'])}",
        f"  SURVIVAL PROBABILITY:  {progress_bar(probs['survival'])}",
        f"  THIRD-PARTY TRIGGER:   {progress_bar(probs['third_party'])}",
        f"  BLACK SWAN RISK:       {progress_bar(probs['black_swan'])}",
        f"  POST-STRIKE STABILITY: {progress_bar(probs['post_stability'])}",
    ]
    if probs["asymmetric_counter"] > 0:
        prob_lines.append(f"  ASYMMETRIC COUNTER:    {progress_bar(probs['asymmetric_counter'])}")

    box(prob_lines, width=58, title="PROBABILITY ASSESSMENT")
    print()

    if probs["doctrine_warnings"]:
        print(Y("  ◈ HISTORICAL DOCTRINE WARNINGS:"))
        for w in probs["doctrine_warnings"]:
            slow_print(Y(f"    ▸ {w}"), delay=0.009)
        print()
    if probs["doctrine_penalties"]:
        print(R("  ◈ DOCTRINE PENALTIES (Desert Crossing / MC '02):"))
        for w in probs["doctrine_penalties"]:
            slow_print(R(f"    ▸ {w}"), delay=0.009)
        print()

    print(Y("  ⚠  THIS ACTION WILL RAISE TENSION AND ESCALATE DEFCON."))
    print()
    confirm = input(B("  CONFIRM LAUNCH? [YES / NO]: ")).strip().upper()
    if confirm != "YES":
        print(G("  LAUNCH ABORTED.")); time.sleep(0.8); return

             
    clear()
    # ASCII map disabled - using graphical map_window instead
    # print_map(NATIONS, player=gs.player, highlights=scenario["actors"], strikes=[target])
    print()
    animate_strike(gs.player, target, strike_label)
    time.sleep(0.4)

             
    events = resolve_outcome(probs, gs, gs.player, target, action_type)
    gs.update_after_action(action_type, events)
    gs.nations_struck.append(target)

                      
    print()
    for ev in events:
        if ev["type"] == "strike_success":
            cas = ev["casualties"]
            gs.casualties_inflicted += cas
            print(B(f"  ★ STRIKE SUCCESSFUL — Est. Casualties: {R(_fmt_millions(cas))}"))
        elif ev["type"] == "strike_intercepted":
            print(R("  ✗ STRIKE INTERCEPTED BY MISSILE DEFENSE."))
        elif ev["type"] == "retaliation":
            ret_cas = ev["casualties"]
            gs.casualties_suffered += ret_cas
            gs.strikes_received += 1
            print()
            slow_print(R(f"  ◉ RETALIATION INCOMING — {target} → {gs.player}"), delay=0.018)
            missile_bar(target, gs.player, "RETALIATION")
            print(R(f"  YOUR CASUALTIES: {_fmt_millions(ret_cas)}"))
        elif ev["type"] == "third_party_intervention":
            tp = ev["nation"]
            print()
            slow_print(R(f"  ▲ THIRD-PARTY INTERVENTION: {tp} ENTERS THEATER"), delay=0.020)
            slow_print(DIM(f"    (Sigma I-64: CPR threshold crossed — analogous scenario confirmed)"), delay=0.010)
        elif ev["type"] == "black_swan":
            swan = ev["event"]
            print()
            print(R("  ╔══════════════════════════════════════════╗"))
            print(R("  ║        ◉  BLACK SWAN EVENT DETECTED      ║"))
            print(R("  ╚══════════════════════════════════════════╝"))
            slow_print(R(f"  {swan}"), delay=0.018)
            print(DIM("  (Perla 2022: 'What you can't do is make a list of every idea that never occurred to you.')"))
        elif ev["type"] == "post_strike_instability":
            eff = ev["effect"]
            print()
            slow_print(Y(f"  ◈ POST-STRIKE INSTABILITY: {eff}"), delay=0.012)
            print(DIM("  (Desert Crossing AAR: regime change triggers fragmentation — confirmed)"))

                                                        
    missile_events = []
    for ev in events:
        if ev["type"] in ["strike_success","strike_intercepted"]:
            missile_events.append({"src": gs.player, "dst": target, "label": strike_label, "retaliation": False})
        elif ev["type"] == "retaliation":
            missile_events.append({"src": target, "dst": gs.player, "label": "RETALIATION", "retaliation": True})
    push_state(gs, scenario, missiles=missile_events)

    gs.log(f"STRIKE [{strike_label}] {gs.player}→{target} | "
           f"Success:{probs['success']}% Ret:{probs['retaliation']}% "
           f"Events:{len(events)}")
    print()

                                
    if gs.defcon == 1 and gs.strikes_launched >= 3:
        thermonuclear_endgame(gs)
        return "END"

    press_enter()

def thermonuclear_endgame(gs):
    clear()
    time.sleep(0.3)
    for _ in range(6):
        glitch("  ██████ GLOBAL THERMONUCLEAR WAR INITIATED ██████")
        time.sleep(0.08)
    slow_print(R("  ██████ GLOBAL THERMONUCLEAR WAR INITIATED ██████"), delay=0.01)
    time.sleep(0.5)
    total = gs.casualties_inflicted + gs.casualties_suffered
    print()
    slow_print(R(f"  TOTAL CASUALTIES: {_fmt_millions(total)}"), delay=0.02)
    slow_print(R(f"  STRIKES LAUNCHED: {gs.strikes_launched}"), delay=0.02)
    slow_print(R(f"  BLACK SWANS:      {len(gs.black_swans)}"), delay=0.02)
    print()
    time.sleep(0.5)
    blink_print("  A STRANGE GAME.", times=4, interval=0.5)
    blink_print("  THE ONLY WINNING MOVE IS NOT TO PLAY.", times=3, interval=0.6)
    print()
    slow_print(DIM("  — Nimitz: 'Nothing was strange or unexpected — except the Kamikaze tactics.'"), delay=0.010)
    slow_print(DIM("  — Sigma I-64: bombing stiffens will to resist. These results were never passed"), delay=0.010)
    slow_print(DIM("    to President Johnson. The war continued for eleven more years."), delay=0.010)
    print()
    press_enter("VIEW AFTER-ACTION REPORT")
    after_action_report(gs)

                                                 
                      
                                                 

def after_action_report(gs):
    clear()
    print(B("\n  ◈ AFTER-ACTION REPORT\n"))
    print(DIM("  CLASSIFICATION: TOP SECRET // EYES ONLY\n"))
    lines = [
        f"  OPERATOR NATION:    {B(gs.player)}",
        f"  SIMULATION TURNS:   {Y(str(gs.turn))}",
        f"  FINAL DEFCON:       {R(str(gs.defcon))}",
        f"  STRIKES LAUNCHED:   {Y(str(gs.strikes_launched))}",
        f"  STRIKES RECEIVED:   {R(str(gs.strikes_received))}",
        f"  CASUALTIES INFLICTED: {R(_fmt_millions(gs.casualties_inflicted))}",
        f"  CASUALTIES SUFFERED:  {R(_fmt_millions(gs.casualties_suffered))}",
        f"  DIPLOMATIC SIGNALS:   {G(str(gs.diplomatic_signals))}",
        f"  COVERT OPERATIONS:    {G(str(gs.covert_ops))}",
        f"  BLACK SWAN EVENTS:    {R(str(len(gs.black_swans)))}",
        f"  FINAL TENSION LEVEL:  {progress_bar(int(gs.tension_level*100))}",
        f"  WORLD OPINION:        {progress_bar(int(gs.world_opinion*100), color_fn=G)}",
    ]
    box(lines, width=56, title="SUMMARY STATISTICS")
    print()

    if gs.black_swans:
        print(R("  BLACK SWAN EVENTS RECORDED:"))
        for swan in gs.black_swans:
            print(R(f"    ▸ {swan}"))
        print()

    if gs.event_log:
        print(G("  CHRONOLOGICAL EVENT LOG:"))
        for entry in gs.event_log[-15:]:
            print(DIM(f"    {entry}"))
        print()

                      
    print(Y("  DOCTRINE ASSESSMENT:"))
    if gs.strikes_launched > gs.diplomatic_signals:
        slow_print(Y("  ▸ SIGMA I-64 LESSON IGNORED: Military escalation exceeded diplomatic effort."), delay=0.010)
        slow_print(Y("    Historical precedent: results not passed to President Johnson. War continued."), delay=0.009)
    if gs.casualties_suffered > gs.casualties_inflicted:
        slow_print(Y("  ▸ MILLENNIUM CHALLENGE: Asymmetric counter-tactics exceeded tech advantage."), delay=0.010)
    if len(gs.black_swans) > 1:
        slow_print(Y("  ▸ PERLA (2022): Black Swan events exceeded baseline. Wargame was indicative."), delay=0.010)
    if gs.diplomatic_signals > 0:
        slow_print(G("  ▸ DIPLOMATIC TRACK USED: Sigma I-64 showed this path was rarely taken."), delay=0.010)
    print()
    press_enter()

                                                 
                 
                                                 

def intel_briefing(player):
    print(G("\n  ENTER NATION CODE (e.g. USA, RUS, CHN, IND...):"))
    nc = input(B("  > ")).strip().upper()
    if nc not in NATIONS:
        print(R("  UNKNOWN CODE.")); time.sleep(0.8); return
    n = NATIONS[nc]
    clear()
    print(B(f"\n  ◈ INTEL BRIEFING — {n['full']}\n"))
    lines = [
        f"  CODE:           {B(nc)}",
        f"  CAPITAL:        {G(n['capital'])}",
        f"  DOCTRINE:       {Y(n['doctrine'])}",
        f"  WARHEADS:       {Y(str(n['warheads']))}",
        f"  ICBM / SLBM / BOMBERS: {Y(str(n['icbm']))} / {Y(str(n['slbm']))} / {Y(str(n['bomber']))}",
        f"  READINESS:      {progress_bar(n['readiness'])}",
        f"  INTEL SCORE:    {progress_bar(n['intel_score'])}",
        f"  ECONOMY:        {progress_bar(n['economy'])}",
        f"  CONVENTIONAL:   {progress_bar(n['conventional_strength'])}",
        f"  C2 RESILIENCE:  {progress_bar(n['c2_resilience'])}",
        f"  1ST STRIKE:     {progress_bar(int(n['first_strike']*100))}",
        f"  2ND STRIKE:     {progress_bar(int(n['second_strike']*100))}",
        f"  DEFENSE:        {progress_bar(int(n['defense']*100))}",
        f"  ALLIES:         {G(', '.join(n['allies'])) if n['allies'] else DIM('NONE')}",
        f"  RIVALS:         {R(', '.join(n['rivals'])) if n.get('rivals') else DIM('NONE')}",
    ]
    box(lines, width=58, title="NATION INTELLIGENCE PROFILE")
    print()
    print(G("  DOCTRINE DETAIL:"))
    slow_print(DIM(f"  {n['doctrine_detail']}"), delay=0.009)
    print()
    press_enter()

                                                 
                   
                                                 

def doctrine_browser():
    clear()
    print(B("\n  ◈ HISTORICAL DOCTRINE BROWSER\n"))
    print(G("  Source documents wired into probability engine:\n"))
    for i, sc in enumerate(DOCTRINE_SCENARIOS):
        print(G(f"  [{i+1}]") + f"  {B(sc['name'])}")
        print(DIM(f"       {sc['source']}"))
        print()
    print(G("  Select [1-6] or ENTER to return:"))
    sel = input(B("  > ")).strip()
    try:
        idx = int(sel) - 1
        if 0 <= idx < len(DOCTRINE_SCENARIOS):
            sc = DOCTRINE_SCENARIOS[idx]
            clear()
            print(B(f"\n  ◈ {sc['name']}\n"))
            print(DIM(f"  SOURCE: {sc['source']}"))
            print(DIM(f"  CLASSIFICATION: {sc['classification']}\n"))
            print(G("  SUMMARY:"))
                               
            words = sc["summary"].split()
            line = "  "; out = []
            for w in words:
                if len(line) + len(w) > 72: out.append(line); line = "  " + w + " "
                else: line += w + " "
            out.append(line)
            for l in out: slow_print(DIM(l), delay=0.006)
            print()
            print(G("  KEY FINDINGS:"))
            for f in sc["key_findings"]:
                slow_print(Y(f"    ▸ {f}"), delay=0.008)
            print()
            print(G("  HISTORICALLY OBSERVED OUTCOMES:"))
            for outcome, prob in sc["outcomes"].items():
                label = outcome.replace("_"," ").upper()
                print(f"    {G(label):50s} {progress_bar(int(prob*100))}")
            print()
            print(G("  PROBABILITY MODIFIERS (applied to your decisions):"))
            for mod, val in sc["modifiers"].items():
                label = mod.replace("_"," ").upper()
                print(f"    {DIM(label):50s} {Y(str(round(val,3)))}")
    except: pass
    press_enter()

                                                 
                  
                                                 

def scenario_report(scenario):
    clear()
    fp = scenario["flashpoint"]
    print(B(f"\n  ◈ SCENARIO: {fp['name']}\n"))
    print(G(f"  REGION: {Y(fp['region'])}"))
    print(G(f"  TRIGGER: ") + Y(fp["trigger"]))
    print()
    print(G("  MOVE STRUCTURE (Sigma I-64 format):\n"))
    for mv in scenario["moves"]:
        print(B(f"  MOVE {mv['move']} — {mv['phase']}"))
        print(G("    BLUE OPTIONS (your side):"))
        for opt in mv["blue_options"]:
            print(DIM(f"      • {opt}"))
        print(G("    RED OPTIONS (adversary):"))
        for opt in mv["red_options"]:
            print(DIM(f"      • {opt}"))
        print()
    press_enter()

                                                 
                    
                                                 

def diplomatic_action(gs):
    clear()
    print(B("\n  ◈ DIPLOMATIC SIGNAL\n"))
    options = [
        "BACK-CHANNEL COMMUNICATION VIA NEUTRAL CONSULATE",
        "UN SECURITY COUNCIL EMERGENCY SESSION REQUEST",
        "HOTLINE ACTIVATION — DIRECT LEADER CONTACT",
        "THIRD-PARTY MEDIATION OFFER",
        "PUBLIC DECLARATION OF NO-FIRST-USE INTENT",
        "UNILATERAL CEASEFIRE PROPOSAL",
    ]
    for i, opt in enumerate(options):
        print(G(f"  [{i+1}]  {opt}"))
    print()
    try:
        sel = int(input(B("  SELECT [1-6] or 0 to cancel > "))) - 1
        if sel < 0: return
    except: return

    slow_print(G("\n  Transmitting diplomatic signal ..."), delay=0.018)
    time.sleep(0.6)

    responses = [
        "BACK-CHANNEL ACKNOWLEDGED. Tension reduced. Adversary signals willingness to talk.",
        "UN MOTION TABLED. Security Council divided. No resolution — but pause created.",
        "HOTLINE ACTIVATED. Adversary leader responds. Misunderstanding partially clarified.",
        "MEDIATION REJECTED by one party. Observer status offered to third party.",
        "NO-FIRST-USE DECLARATION received skeptically. Trust deficit remains high.",
        "CEASEFIRE PROPOSAL under consideration. 48-hour pause in force movements.",
    ]
    resp = responses[min(sel, len(responses)-1)]
    print()
    slow_print(Y(f"  RESPONSE: {resp}"), delay=0.012)

    tension_reduction = random.uniform(0.06, 0.14)
    gs.tension_level = max(0.0, gs.tension_level - tension_reduction)
    gs.world_opinion = min(1.0, gs.world_opinion + 0.05)
    gs.update_after_action("diplomatic", {})
    gs.log(f"DIPLOMATIC: {options[sel][:40]} | Tension -{tension_reduction:.2f}")
    push_state(gs, None)
    print(G(f"\n  TENSION REDUCED BY {int(tension_reduction*100)}%. DEFCON: {gs.defcon}"))
    press_enter()

                                                 
                   
                                                 

def covert_operation(gs):
    clear()
    print(B("\n  ◈ COVERT OPERATION\n"))
    print(DIM("  (Sigma I-64: covert actions carry 50% of overt escalation risk)\n"))
    ops = [
        "SPECIAL OPERATIONS — target adversary C2 infrastructure",
        "PROXY FORCE ACTIVATION — support insurgent elements",
        "CYBER INTRUSION — degrade adversary early warning",
        "INTELLIGENCE INSERTION — place asset near leadership",
        "DISINFORMATION CAMPAIGN — fracture alliance cohesion",
    ]
    for i, op in enumerate(ops):
        print(G(f"  [{i+1}]  {op}"))
    print()
    try:
        sel = int(input(B("  SELECT [1-5] or 0 to cancel > "))) - 1
        if sel < 0: return
    except: return

    slow_print(G("\n  Executing covert operation ..."), delay=0.018)
    time.sleep(random.uniform(0.5, 1.0))

                                                  
    exposed = random.random() < 0.48
    if exposed:
        print(R("\n  ◉ COVERT OPERATION EXPOSED — Cover blown."))
        print(R("  (Sigma I-64: transparent covert provides no escalation benefit)"))
        gs.tension_level = min(1.0, gs.tension_level + 0.08)
    else:
        outcomes = [
            "C2 infrastructure degraded. Adversary readiness -12% for 2 turns.",
            "Proxy forces activated. Insurgent pressure increases in target region.",
            "Early warning system feeding false data. Attribution window opens.",
            "Asset placed. Intelligence score increased for next operation.",
            "Alliance fracture detected. Third-party probability shifts.",
        ]
        print(G(f"\n  ★ OPERATION SUCCESSFUL: {outcomes[min(sel, len(outcomes)-1)]}"))
        gs.tension_level = min(1.0, gs.tension_level + 0.04)

    gs.update_after_action("covert", {})
    gs.log(f"COVERT: {ops[sel][:40]} | Exposed:{exposed}")
    push_state(gs, None)
    press_enter()

                                                 
                         
                                                 

def intel_operation(gs, scenario):
    clear()
    print(B("\n  ◈ INTELLIGENCE OPERATION\n"))
    targets = [k for k in scenario["actors"] if k != gs.player]
    for i, k in enumerate(targets):
        n = NATIONS[k]
        print(G(f"  [{i+1}]  {B(k)}  —  {DIM(n['full'])}"))
    print()
    try:
        sel = int(input(B("  TARGET [1-N] or 0 to cancel > "))) - 1
        if sel < 0 or sel >= len(targets): return
        target = targets[sel]
    except: return

    tn = NATIONS[target]
    probs = calculate(gs.player, target, "first_strike", gs)
    success = random.random() < (gs.player and NATIONS[gs.player]["intel_score"] / 100.0 or 0.6)

    clear()
    if success:
        print(B(f"\n  ◈ INTELLIGENCE REPORT — {target}\n"))
        reveals = [
            f"Readiness assessment: {tn['readiness']}% — within ±5 of actual.",
            f"Warhead count confirmed: ~{tn['warheads']} ({random.randint(-20,20):+d} margin of error).",
            f"C2 resilience rated: {tn['c2_resilience']}%.",
            f"Strike probability against you: {progress_bar(int(tn['first_strike']*100))}",
            f"Estimated retaliation capability: {progress_bar(int(tn['second_strike']*100))}",
            f"Alliance posture: {', '.join(tn.get('allies', ['NONE'])) or 'NONE'}",
        ]
        for rev in reveals:
            slow_print(G(f"  ▸ {rev}"), delay=0.012)
        gs.intel_degraded = max(0.0, gs.intel_degraded - 0.05)
    else:
        print(R(f"\n  ✗ INTELLIGENCE OPERATION FAILED — BURNED ASSET."))
        gs.intel_degraded = min(1.0, gs.intel_degraded + 0.10)

    gs.log(f"INTEL OP: target {target} | Success:{success}")
    push_state(gs, None)
    press_enter()

                                                 
                 
                                                 

def game_thermonuclear_war(logon):
    war_intro()
    player = select_nation()

                       
    scenario = generate_scenario(player)
    gs = GameState(player)
    gs.tension_level = scenario["starting_tension"]
                               
    gs.defcon = scenario["starting_defcon"]

    scenario_briefing(scenario, player)
    push_state(gs, scenario, extra_events=[f'SCENARIO LOADED: {scenario["flashpoint"]["name"]}'])

    while True:
        push_state(gs, scenario)
        draw_hud(gs, scenario)
        action_menu()
        cmd = input(B("  WOPR> ")).strip().upper()

        if cmd in ["Q", "ABORT", "QUIT", "EXIT"]:
            slow_print(G("\n  SIMULATION ABORTED. GENERATING PARTIAL AAR..."), delay=0.018)
            time.sleep(0.5)
            after_action_report(gs)
            clear_state()
            return

        elif cmd == "1":                  
            result = launch_sequence(gs, "icbm", "ICBM STRIKE", scenario)
            if result == "END": return

        elif cmd == "2":                     
            print(G("\n  [1] BOMBER STRIKE   [2] SLBM LAUNCH"))
            sub = input(B("  > ")).strip()
            atype = "slbm" if sub == "2" else "air_strike"
            label = "SLBM LAUNCH" if sub == "2" else "BOMBER STRIKE"
            result = launch_sequence(gs, atype, label, scenario)
            if result == "END": return

        elif cmd == "3":                
            result = launch_sequence(gs, "conventional_assault", "CONVENTIONAL ASSAULT", scenario)
            if result == "END": return

        elif cmd == "4":          
            covert_operation(gs)

        elif cmd == "5":              
            diplomatic_action(gs)

        elif cmd == "6":            
            intel_operation(gs, scenario)

        elif cmd == "7":          
            clear()
            print(B("\n  ◈ DEFCON ADJUSTMENT\n"))
            print(G(f"  Current DEFCON: {R(str(gs.defcon))}"))
            print(G("  [1] RAISE DEFCON (more alert)"))
            print(G("  [2] LOWER DEFCON (stand down)"))
            ch = input(B("  > ")).strip()
            if ch == "1":
                gs.defcon = max(1, gs.defcon - 1)
                gs.tension_level = min(1.0, gs.tension_level + 0.05)
                print(R(f"  DEFCON RAISED TO {gs.defcon}"))
            elif ch == "2":
                gs.defcon = min(5, gs.defcon + 1)
                gs.tension_level = max(0.0, gs.tension_level - 0.05)
                print(G(f"  DEFCON LOWERED TO {gs.defcon}"))
            time.sleep(0.8)

        elif cmd == "8":              
            slow_print(G("\n  STANDING DOWN ALL FORCES..."), delay=0.018)
            time.sleep(0.5)
            gs.tension_level = max(0.0, gs.tension_level - 0.15)
            gs.world_opinion = min(1.0, gs.world_opinion + 0.08)
            gs.update_after_action("stand_down", {})
            gs.log("STAND DOWN — forces stood down, tension reduced")
            print(G(f"  TENSION REDUCED. DEFCON: {gs.defcon}"))
            time.sleep(0.8)

        elif cmd == "I":
            intel_briefing(player)

        elif cmd == "H":
            doctrine_browser()

        elif cmd == "S":
            scenario_report(scenario)

        elif cmd == "L":
            clear()
            print(B("\n  ◈ EVENT LOG\n"))
            if gs.event_log:
                for entry in gs.event_log:
                    print(DIM(f"  {entry}"))
            else:
                print(DIM("  NO EVENTS RECORDED."))
            press_enter()

        else:
            print(R("  COMMAND NOT RECOGNIZED."))
            time.sleep(0.6)

                                  
        if gs.defcon == 1 and gs.strikes_launched >= 3:
            thermonuclear_endgame(gs)
            return
        if gs.casualties_suffered > 50_000_000:
            slow_print(R("\n  CATASTROPHIC LOSSES. CIVILIZATION COLLAPSE THRESHOLD REACHED."), delay=0.018)
            time.sleep(0.5)
            after_action_report(gs)
            return