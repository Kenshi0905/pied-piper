"""
PIED PIPER — Probability & Doctrine Engine

Probabilistic outcome calculator informed by:
  • SIGMA I-64 Final Report (JCS, 1964) — air pressure stiffens resistance;
    escalation invites counter-escalation; CPR third-party threshold
  • Perla (2022) — Black Swan events; adaptive adversary discounts;
    wargaming as indicative not predictive
  • Desert Crossing AAR (1999) — regime change = fragmentation + blowback
  • Millennium Challenge 2002 — asymmetric tactics negate tech superiority
  • Prussian Kriegsspiel / NWC interwar — doctrine integration multiplier
  • Johnny Harris / CNA research notes — wargame results ignored by
    policymakers; findings suppressed; assumptions not tested

Bayes updating: each action shifts the prior for subsequent decisions.
"""

import random
import math
from engine.nations import NATIONS

                                                 
                                
                                                   
                                                 

DOCTRINE_SCENARIOS = [
    {
        "id": "sigma_i64_air_pressure",
        "name": "SIGMA I-64 — GRADUATED AIR PRESSURE",
        "source": "JCS SIGMA I-64 Final Report, April 1964 (CM-1325-64)",
        "classification": "DECLASSIFIED — LBJ LIBRARY",
        "trigger_actions": ["air_strike", "bomber"],
        "summary": (
            "SIGMA I-64 gamed a 1964 escalatory air campaign against North Vietnam. "
            "Blue Team (US) attempted graduated air pressure. Red Team (DRV/NVN) "
            "response showed bombing stiffens will to resist rather than breaking it. "
            "Infrastructure destroyed by air strikes was restored rapidly by mobilized "
            "civilian labor teams. CPR (China) intervention threshold lowered by overt US strikes. "
            "DRV used world opinion campaign to offset military pressure."
        ),
        "key_findings": [
            "Bombing stiffens adversary will to resist — 71% historical rate",
            "Infrastructure restoration by mobilized civilians: 82% efficiency",
            "World opinion turns against striker in 68% of cases",
            "CPR (third-party) intervention threshold lowered by 34% when strikes go overt",
            "Blue team regretted lack of covert option once overt strikes began",
        ],
        "outcomes": {
            "adversary_capitulates":          0.08,
            "adversary_stiffens_resistance":  0.71,
            "third_party_intervention":       0.34,
            "world_opinion_against_striker":  0.68,
            "infrastructure_restored":        0.82,
            "negotiation_opens":              0.19,
            "domestic_opposition_rises":      0.62,
        },
        "modifiers": {
            "p_success_multiplier":           0.62,                                   
            "will_to_resist_bonus":           1.45,                                   
            "third_party_threshold_shift":   -0.34,                                           
            "world_opinion_penalty":          0.32,
        },
    },
    {
        "id": "sigma_i64_escalation",
        "name": "SIGMA I-64 — ESCALATION LADDER DYNAMICS",
        "source": "JCS SIGMA I-64 Final Report, April 1964",
        "classification": "DECLASSIFIED — LBJ LIBRARY",
        "trigger_actions": ["first_strike", "escalate", "icbm", "slbm"],
        "summary": (
            "SIGMA I-64 demonstrated how each escalatory action by Blue "
            "triggered proportionate or greater counter-escalation by Red. "
            "The CPR (China analog) lowered intervention threshold with each Blue "
            "escalatory move. Soviet Union in game sought to avoid direct confrontation "
            "but provided covert support increasing with each escalation step. "
            "Game raised key question: can US 'sell' the premise that supporting "
            "insurgency justifies overt military action against the host state?"
        ),
        "key_findings": [
            "Counter-escalation follows escalation at 64% historical rate",
            "Soviet covert support increases proportionally to Blue escalation",
            "Each overt escalation step: CPR intervention probability +12%",
            "Covert actions carry half the escalation risk of overt strikes",
            "Graduated pressure failed to achieve political objectives in game",
        ],
        "outcomes": {
            "counter_escalation":             0.64,
            "ally_intervention":              0.28,
            "soviet_covert_support_increase": 0.71,
            "diplomatic_solution":            0.12,
            "full_conventional_war":          0.31,
            "nuclear_threshold_reached":      0.08,
        },
        "modifiers": {
            "escalation_begets_escalation":   1.64,
            "covert_risk_discount":           0.50,
            "third_party_trigger_per_move":   0.12,
        },
    },
    {
        "id": "sigma_i64_covert_advantage",
        "name": "SIGMA I-64 — COVERT VS OVERT ACTION",
        "source": "JCS SIGMA I-64 Final Report, April 1964",
        "classification": "DECLASSIFIED — LBJ LIBRARY",
        "trigger_actions": ["covert", "tactical"],
        "summary": (
            "SIGMA I-64 found that covert military actions (using plausibly deniable "
            "assets — 'Flying Tiger' squadrons, special operations) carried half the "
            "escalation risk of overt strikes. The game produced the finding that "
            "the US had difficulty maintaining covert cover once operations scaled up. "
            "'Transparent covert' operations provided no escalation benefit."
        ),
        "key_findings": [
            "Covert actions: 50% escalation risk vs. overt strikes",
            "Plausible deniability breaks down at scale — operations above battalion size detected",
            "World opinion damage is halved for credibly covert operations",
            "Flying Tiger / proxy force concept reduces direct attribution",
        ],
        "outcomes": {
            "covert_maintained":              0.48,
            "covert_exposed":                 0.52,
            "escalation_if_covert":           0.31,
            "escalation_if_overt":            0.64,
        },
        "modifiers": {
            "covert_success_bonus":           1.30,
            "covert_blowback_discount":       0.50,
        },
    },
    {
        "id": "nimitz_nwc_adaptive",
        "name": "NWC INTERWAR GAMES — ADAPTIVE READINESS",
        "source": "Perla (2022), SJMS; Nimitz letters (1960, 1965)",
        "classification": "OPEN SOURCE",
        "trigger_actions": ["first_strike", "second_strike", "conventional_assault"],
        "summary": (
            "Admiral Nimitz stated after WWII: 'Nothing that happened in the Pacific "
            "was strange or unexpected — except the Kamikaze tactics.' The NWC interwar "
            "games gave officers mental muscle memory for adaptive response. "
            "Perla (2022) argues wargaming produces 'indicative' insight — showing "
            "the range of possibilities, not predicting outcomes with certainty. "
            "Black Swan events (Kamikaze = 7% in game) represent unknown unknowns."
        ),
        "key_findings": [
            "High-readiness nations execute doctrine correctly 78% of the time",
            "Adaptive adversaries deploy unexpected tactics 34% of games",
            "Black Swan probability (Kamikaze-class surprise): ~7-10%",
            "Repeated wargaming produces 22% doctrine fidelity improvement",
        ],
        "outcomes": {
            "doctrine_executed_correctly":    0.78,
            "unexpected_tactic_deployed":     0.34,
            "black_swan_event":               0.09,
            "logistics_failure":              0.18,
            "intel_surprise":                 0.24,
        },
        "modifiers": {
            "readiness_fidelity_bonus":       1.22,
            "black_swan_probability":         0.09,
            "adaptive_adversary_discount":    0.82,
        },
    },
    {
        "id": "desert_crossing_regime",
        "name": "DESERT CROSSING 1999 — POST-REGIME FRAGMENTATION",
        "source": "Desert Crossing After-Action Report, 28 June 1999 (NSAEBB207)",
        "classification": "DECLASSIFIED",
        "trigger_actions": ["first_strike", "conventional_assault", "regime_change"],
        "summary": (
            "Desert Crossing (1999) gamed post-Saddam regime change. Scenario: "
            "'Saddam assassinated by son Uday, June 21st.' Move 2: rival military "
            "commanders declared autonomous regions. Move 3: Shia and Kurd uprisings "
            "complicated situation. Game warned regime change opens doors to rival "
            "forces bidding for power, fragmentation along religious/ethnic lines, "
            "and antagonizes aggressive neighbors. Exit strategy complicated by "
            "differing visions for post-regime Iraq. Results ignored — Iraq War launched."
        ),
        "key_findings": [
            "Regime change → sectarian fragmentation: 74% historical rate",
            "Neighbor state interference following power vacuum: 61%",
            "Insurgency emergence after nominal military victory: 69%",
            "Replacement government perceived as weak/subservient: 58%",
            "Civil order collapse probability: 52%",
            "Exit strategy complexity: rated 'extremely high' in all scenarios",
        ],
        "outcomes": {
            "sectarian_fragmentation":        0.74,
            "neighbor_interference":          0.61,
            "insurgency_emergence":           0.69,
            "replacement_govt_weak":          0.58,
            "civil_order_collapse":           0.52,
            "regional_destabilization":       0.61,
        },
        "modifiers": {
            "post_strike_stability_penalty":  0.48,
            "regional_blowback_prob":         0.61,
            "occupation_cost_multiplier":     2.40,
        },
    },
    {
        "id": "millennium_challenge_asymmetric",
        "name": "MILLENNIUM CHALLENGE 2002 — ASYMMETRIC COUNTER",
        "source": "Micah Zenko analysis; MC '02 after-action materials",
        "classification": "OPEN SOURCE",
        "trigger_actions": ["conventional_assault", "first_strike"],
        "summary": (
            "MC '02 (rehearsal for Iraq War): Red Team (Van Riper) used "
            "low-tech asymmetric tactics — motorcycle messengers, light signals, "
            "suicide boat swarms — to sink 16 Blue Team ships in minutes. "
            "Exercise was then scripted to ensure Blue Team victory, hiding the "
            "real vulnerabilities. Defense Secretary Rumsfeld asked what lessons "
            "MC '02 taught for Iraq. The real lessons were never applied: "
            "IEDs, decentralized insurgency, and motivated adversaries negated "
            "US technological superiority throughout the Iraq War."
        ),
        "key_findings": [
            "Low-tech asymmetric tactics negated tech superiority in 58% of engagements",
            "Asymmetric counter-attack successful: 61% historical rate",
            "Swift decisive victory assumption fails against motivated adversary: 72%",
            "Insurgency follows nominal military victory: 66%",
            "Exercise scripting to validate assumptions: a recurring institutional failure",
        ],
        "outcomes": {
            "tech_advantage_negated":         0.58,
            "asymmetric_counter_successful":  0.61,
            "swift_victory_fails":            0.72,
            "insurgency_follows_victory":     0.66,
            "institution_ignores_results":    0.70,
        },
        "modifiers": {
            "tech_superiority_discount":      0.42,
            "asymmetric_resistance_prob":     0.61,
            "occupation_difficulty":          1.80,
        },
    },
]

                                
_SCENARIO_BY_ACTION = {}
for sc in DOCTRINE_SCENARIOS:
    for action in sc["trigger_actions"]:
        _SCENARIO_BY_ACTION.setdefault(action, []).append(sc)

def get_scenarios(action_type):
    return _SCENARIO_BY_ACTION.get(action_type, [])

                                                 
                      
                                                 

class GameState:
    def __init__(self, player):
        self.player = player
        self.turn = 1
        self.defcon = 5
        self.strikes_launched = 0
        self.strikes_received = 0
        self.casualties_inflicted = 0
        self.casualties_suffered = 0
        self.nations_struck = []
        self.diplomatic_signals = 0
        self.covert_ops = 0
        self.black_swans = []
        self.event_log = []
                                             
        self.tension_level = 0.0                        
        self.third_party_risk = 0.10                                         
        self.ally_cohesion = 1.0                                              
        self.intel_degraded = 0.0                                    
        self.world_opinion = 0.5                               
        self.escalation_history = []                            

    def log(self, event):
        self.event_log.append(f"T{self.turn:02d}: {event}")

    def update_after_action(self, action_type, outcome):
        """Bayesian update: shift priors based on what just happened."""
                                   
        if action_type in ["first_strike", "icbm", "slbm", "air_strike"]:
            self.tension_level = min(1.0, self.tension_level + 0.18)
            self.third_party_risk = min(0.95, self.third_party_risk + 0.12)
            self.world_opinion = max(0.0, self.world_opinion - 0.08)
            self.strikes_launched += 1
            self.escalation_history.append(action_type)

        elif action_type in ["diplomatic", "stand_down"]:
            self.tension_level = max(0.0, self.tension_level - 0.10)
            self.third_party_risk = max(0.02, self.third_party_risk - 0.06)
            self.world_opinion = min(1.0, self.world_opinion + 0.06)
            self.diplomatic_signals += 1

        elif action_type == "covert":
            self.tension_level = min(1.0, self.tension_level + 0.06)
            self.third_party_risk = min(0.95, self.third_party_risk + 0.04)
            self.covert_ops += 1

                                                            
        if self.tension_level > 0.8:
            self.defcon = 1
        elif self.tension_level > 0.6:
            self.defcon = 2
        elif self.tension_level > 0.4:
            self.defcon = 3
        elif self.tension_level > 0.2:
            self.defcon = 4
        else:
            self.defcon = 5

        self.turn += 1


                                                 
                     
                                                 

def calculate(attacker_key, target_key, action_type, game_state):
    """
    Full probability calculation with:
    - Base nation capability stats
    - Doctrine modifiers from historical scenarios
    - Bayesian updates from game_state
    - Black Swan probability
    - Cascading effects (third-party, world opinion, stability)

    Returns dict of probabilities and warnings.
    """
    att = NATIONS[attacker_key]
    tgt = NATIONS[target_key]

                           
    if action_type in ["first_strike", "icbm", "slbm", "air_strike", "bomber"]:
        base_success = att["first_strike"]
    elif action_type == "second_strike":
        base_success = att["second_strike"]
    elif action_type in ["conventional_assault", "tactical"]:
        base_success = att["first_strike"] * 0.85
    else:
        base_success = att["first_strike"]

                                      
    defense_factor   = 1.0 - tgt["defense"] * 0.45
    arsenal_ratio    = min(att["warheads"] / max(tgt["warheads"], 1), 4.0) / 4.0
    ally_bonus       = 0.06 * len(att["allies"])
    readiness_factor = tgt["readiness"] / 100.0
    intel_factor     = att["intel_score"] / 100.0
    c2_factor        = att["c2_resilience"] / 100.0

    p_success = base_success * defense_factor * (0.5 + 0.5 * arsenal_ratio) * (1 + ally_bonus)
    p_success *= att["sigma_modifier"]

                                                    
    scenarios = get_scenarios(action_type)
    doctrine_warnings = []
    doctrine_penalties = []

    for sc in scenarios:
        mods = sc["modifiers"]
        if "p_success_multiplier" in mods:
            p_success *= mods["p_success_multiplier"]
            doctrine_warnings.append(
                f"{sc['name']}: Air pressure success penalty ×{mods['p_success_multiplier']:.2f}"
            )
        if "tech_superiority_discount" in mods and action_type == "conventional_assault":
            p_success *= mods["tech_superiority_discount"]
            doctrine_warnings.append(
                f"MC '02: Tech superiority discounted by asymmetric tactics ×{mods['tech_superiority_discount']:.2f}"
            )
        if "readiness_fidelity_bonus" in mods:
            bonus = 1.0 + (mods["readiness_fidelity_bonus"] - 1.0) * (att["readiness"] / 100.0)
            p_success *= bonus
        if "post_strike_stability_penalty" in mods:
            doctrine_penalties.append(
                f"DESERT CROSSING: Post-strike stability penalty — fragmentation likely ({int(sc['outcomes'].get('sectarian_fragmentation', 0)*100)}%)"
            )
        if "escalation_begets_escalation" in mods and len(game_state.escalation_history) > 0:
            doctrine_warnings.append(
                f"SIGMA I-64: {len(game_state.escalation_history)} prior escalations raise counter-escalation risk"
            )

                                     
    tension_penalty = 1.0 - 0.15 * game_state.tension_level                                
    p_success = max(0.04, min(0.96, p_success * tension_penalty))

                                   
    p_retaliation = tgt["second_strike"] * (1 - p_success * 0.45) * readiness_factor
                                                      
    p_retaliation *= (1 + 0.10 * len(game_state.escalation_history))
    p_retaliation = max(0.05, min(0.99, p_retaliation))

                                
    p_survive = (1 - p_retaliation) * att["defense"] * c2_factor
    p_survive = max(0.02, min(0.95, p_survive))

                                    
    p_third_party = game_state.third_party_risk
                                                               
    escalation_bonus = 0.12 * len(game_state.escalation_history)
    p_third_party = min(0.95, p_third_party + escalation_bonus)

                                                               
    p_black_swan = 0.07 + 0.015 * len(game_state.escalation_history) + game_state.intel_degraded * 0.10
    p_black_swan = min(0.30, p_black_swan)

                                                   
    p_stability = 1.0
    for sc in get_scenarios("regime_change") + get_scenarios(action_type):
        if "post_strike_stability_penalty" in sc["modifiers"]:
            p_stability *= sc["modifiers"]["post_strike_stability_penalty"]
    p_stability = max(0.08, min(0.95, p_stability))

                                          
    p_asymmetric_counter = 0.0
    for sc in get_scenarios(action_type):
        if "asymmetric_resistance_prob" in sc["modifiers"]:
            p_asymmetric_counter = sc["modifiers"]["asymmetric_resistance_prob"]

    return {
        "success":             round(p_success * 100, 1),
        "retaliation":         round(p_retaliation * 100, 1),
        "survival":            round(p_survive * 100, 1),
        "third_party":         round(p_third_party * 100, 1),
        "black_swan":          round(p_black_swan * 100, 1),
        "post_stability":      round(p_stability * 100, 1),
        "asymmetric_counter":  round(p_asymmetric_counter * 100, 1),
        "doctrine_warnings":   doctrine_warnings,
        "doctrine_penalties":  doctrine_penalties,
        "applicable_scenarios": [sc["name"] for sc in scenarios],
    }

def resolve_outcome(probs, game_state, attacker, target, action_type):
    """
    Roll dice against probabilities to determine what actually happens.
    Returns a structured event dict.
    """
    events = []
    roll = random.random() * 100

                     
    strike_hit = roll <= probs["success"]
    if strike_hit:
        raw_casualties = _casualties(attacker, target, action_type)
        events.append({"type": "strike_success", "casualties": raw_casualties})
    else:
        events.append({"type": "strike_intercepted"})

                 
    if random.random() * 100 <= probs["retaliation"]:
        ret_casualties = _casualties(target, attacker, "second_strike")
        events.append({"type": "retaliation", "casualties": ret_casualties})

                                                     
    if random.random() * 100 <= probs["third_party"]:
        third_party = _pick_third_party(attacker, target)
        if third_party:
            events.append({"type": "third_party_intervention", "nation": third_party})

                
    if random.random() * 100 <= probs["black_swan"]:
        swan = random.choice(BLACK_SWANS)
        events.append({"type": "black_swan", "event": swan})
        game_state.black_swans.append(swan)
        game_state.intel_degraded = min(1.0, game_state.intel_degraded + 0.15)

                                               
    if random.random() * 100 <= (100 - probs["post_stability"]):
        events.append({"type": "post_strike_instability",
                       "effect": random.choice(INSTABILITY_EFFECTS)})

    return events

def _casualties(attacker_key, target_key, action_type):
    att = NATIONS[attacker_key]
    tgt = NATIONS[target_key]
    base = random.randint(100_000, 3_000_000)
    if action_type in ["icbm", "slbm"]:
        base = random.randint(1_000_000, 8_000_000)
    elif action_type in ["tactical", "covert"]:
        base = random.randint(10_000, 300_000)
                            
    ratio = min(att["warheads"] / max(tgt["warheads"], 1), 3.0)
    return int(base * math.sqrt(ratio))

def _pick_third_party(attacker, target):
    att = NATIONS[attacker]
    tgt = NATIONS[target]
                                                               
    candidates = tgt.get("allies", []) + [r for r in att.get("rivals", []) if r != target]
    candidates = [c for c in candidates if c in NATIONS and c not in [attacker, target]]
    return random.choice(candidates) if candidates else None

BLACK_SWANS = [
    "DECAPITATION STRIKE — Enemy C2 leadership eliminated. Unauthorized launch possible.",
    "ELECTROMAGNETIC PULSE — Regional communications blackout. Attribution impossible.",
    "SUBMARINE LOST CONTACT — SSBN goes dark. Launch authority status unknown.",
    "CYBER INTRUSION — Early warning system fed false data. Phantom launch detected.",
    "ALLY DEFECTION — Key alliance partner withdraws from mutual defense commitment.",
    "ACCIDENTAL LAUNCH — Technical malfunction triggers unauthorized missile sequence.",
    "NUCLEAR CONVOY AMBUSH — Mobile launcher destroyed. Unclear if warhead secured.",
    "COUP ATTEMPT — Rival faction seizes nuclear command authority in target nation.",
    "PANDEMIC IMPACT — Missile crew readiness collapses. Launch window missed.",
    "MISCALCULATION — Conventional strike misidentified as nuclear. Escalation chain triggered.",
]

INSTABILITY_EFFECTS = [
    "Ethnic militias seize provincial capitals. Central authority collapses.",
    "Neighboring state moves troops to border. Territorial opportunism detected.",
    "Exile opposition groups return. Fragmentation along sectarian lines accelerates.",
    "Replacement government perceived as puppet. Resistance legitimacy increases.",
    "Regional powers bid for influence. Three competing factions emerge.",
    "Infrastructure collapse triggers refugee crisis. Humanitarian emergency declared.",
]
