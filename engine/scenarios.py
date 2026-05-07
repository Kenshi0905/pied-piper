"""
PIED PIPER — Dynamic Scenario Generator

Generates geopolitically grounded crisis scenarios by combining:
- Nation-specific flashpoints and fault lines
- Historical wargame scenario templates (Sigma I-64, Desert Crossing, MC '02)
- Randomized trigger events with doctrine-informed starting conditions
"""

import random
from engine.nations import NATIONS, NATION_KEYS

                                                        
FLASHPOINTS = [
    {
        "id":       "taiwan_strait",
        "name":     "TAIWAN STRAIT CRISIS",
        "actors":   ["CHN", "USA"],
        "optional": ["PRK"],
        "region":   "WESTERN PACIFIC",
        "trigger":  "PRC military exercises cross median line. Taiwan defense activation imminent.",
        "sigma_ref": "Analogous to SIGMA II-64 China intervention threshold — CPR moves lower at each Blue escalation step.",
        "defcon_start": 3,
        "tension_start": 0.45,
    },
    {
        "id":       "korean_peninsula",
        "name":     "KOREAN PENINSULA ESCALATION",
        "actors":   ["PRK", "USA"],
        "optional": ["CHN", "RUS"],
        "region":   "NORTHEAST ASIA",
        "trigger":  "DPRK Hwasong-17 ICBM launch detected over Japan. Trajectory analysis: US mainland range.",
        "sigma_ref": "Coercive deterrence in action — test whether Blue Team will blink first.",
        "defcon_start": 2,
        "tension_start": 0.65,
    },
    {
        "id":       "south_asia_flash",
        "name":     "SOUTH ASIA NUCLEAR FLASH",
        "actors":   ["IND", "PAK"],
        "optional": ["CHN"],
        "region":   "SOUTH ASIA",
        "trigger":  "Pakistan Nasr tactical nuclear weapon deployed near Line of Control. India mobilizes Strike Corps.",
        "sigma_ref": "Full Spectrum Deterrence vs. massive retaliation — which threshold triggers first?",
        "defcon_start": 3,
        "tension_start": 0.50,
    },
    {
        "id":       "middle_east_samson",
        "name":     "MIDDLE EAST — SAMSON THRESHOLD",
        "actors":   ["ISR", "RUS"],
        "optional": ["USA", "UK"],
        "region":   "MIDDLE EAST",
        "trigger":  "Combined multi-front attack on Israel. Iron Dome overwhelmed. Existential threat declared.",
        "sigma_ref": "Nuclear ambiguity as deterrent — does Samson Option credibility hold?",
        "defcon_start": 2,
        "tension_start": 0.70,
    },
    {
        "id":       "nato_eastern_flank",
        "name":     "NATO EASTERN FLANK — ESCALATE TO DE-ESCALATE",
        "actors":   ["RUS", "USA"],
        "optional": ["UK", "FRA"],
        "region":   "EASTERN EUROPE",
        "trigger":  "Russia deploys tactical nuclear warning shot over Baltic Sea. Article 5 invoked by Estonia.",
        "sigma_ref": "Russia's Escalate to De-escalate doctrine in action. Blue Team must decide response.",
        "defcon_start": 2,
        "tension_start": 0.60,
    },
    {
        "id":       "arctic_confrontation",
        "name":     "ARCTIC — STRATEGIC COMPETITION",
        "actors":   ["RUS", "USA"],
        "optional": ["UK"],
        "region":   "ARCTIC",
        "trigger":  "Russian submarine force detected in GIUK gap. Two US SSBNs lose contact with SUBLANT.",
        "sigma_ref": "C2 uncertainty in undersea domain — Perla's Black Swan space.",
        "defcon_start": 3,
        "tension_start": 0.40,
    },
    {
        "id":       "indo_pacific_alliance",
        "name":     "INDO-PACIFIC — ALLIANCE REALIGNMENT",
        "actors":   ["CHN", "USA"],
        "optional": ["IND", "RUS"],
        "region":   "INDO-PACIFIC",
        "trigger":  "China announces mutual defense pact with Russia. QUAD nations convene emergency session.",
        "sigma_ref": "Alliance dynamics shift — analogous to Sigma Yellow Team (neutral bloc) activation.",
        "defcon_start": 4,
        "tension_start": 0.30,
    },
]

                                                                         
MOVE_TEMPLATES = [
                                      
    {
        "move": 1, "phase": "INITIAL POSITIONING",
        "blue_options": [
            "Advise ally that US will initiate graduated pressure by {date} if conditions not met.",
            "Request emergency UN Security Council session. Seek ceasefire resolution.",
            "Deploy carrier strike group to theater. Signal resolve without striking.",
            "Initiate back-channel communication through neutral consulate.",
        ],
        "red_options": [
            "Recommend preparations for introduction of regular forces to support proxy operations.",
            "Prepare for possible offensive operations. Deter escalation through force posture.",
            "Use world opinion campaign to offset military pressure. Appeal to neutral bloc.",
            "Accept military punishment as part of psychological campaign — play for time.",
        ],
    },
                                       
    {
        "move": 2, "phase": "ESCALATION DECISION",
        "blue_options": [
            "Launch covert air strikes against identified military targets. Plausible deniability maintained.",
            "Request congressional authorization for overt military action.",
            "Propose ceasefire with neutral monitoring. Stand down carrier group as signal.",
            "Authorize tactical nuclear alert. Move to DEFCON 2.",
        ],
        "red_options": [
            "Rival commander consolidates hold on southern region. May declare autonomous state.",
            "Request ally air defense assistance. Prepare retaliatory options.",
            "Accept limited ceasefire. Use pause to reposition forces.",
            "Launch asymmetric counter — suicide boats, EMP, proxy attack.",
        ],
    },
                                             
    {
        "move": 3, "phase": "RESOLUTION OR SPIRAL",
        "blue_options": [
            "Negotiate transition government with regional buy-in. Establish exit timeline.",
            "Escalate to overt strikes on strategic targets. Accept world opinion cost.",
            "Invoke mutual defense clause. Bring allies into active operations.",
            "Stand down all forces. Accept diplomatic solution on adversary terms.",
        ],
        "red_options": [
            "Ethnic and religious uprisings complicate situation. Fragmentation accelerates.",
            "Third-party forces enter theater. Strategic situation fundamentally changed.",
            "Negotiate from position of strength. Demand US withdrawal as condition.",
            "Nuclear signal: test missile. Move to first-use posture.",
        ],
    },
]

def generate_scenario(player_nation, include_nations=None):
    """
    Generate a dynamic crisis scenario relevant to the player's nation.
    Returns scenario dict with flashpoint, actors, moves, and starting conditions.
    """
                                                                  
    relevant = [f for f in FLASHPOINTS
                if player_nation in f["actors"] or player_nation in f.get("optional", [])]

    if not relevant:
        relevant = FLASHPOINTS                   

    flashpoint = random.choice(relevant)

                      
    actors = list(flashpoint["actors"])
    if flashpoint.get("optional"):
        extras = [n for n in flashpoint["optional"] if n != player_nation]
        if extras and random.random() > 0.4:
            actors.append(random.choice(extras))

                           
    if player_nation == actors[0]:
        role = "BLUE TEAM (PRIMARY AGGRESSOR / DEFENDER)"
    elif player_nation in actors[1:]:
        role = "RED TEAM (ADVERSARY)"
    else:
        role = "THIRD PARTY / OBSERVER"

    return {
        "flashpoint": flashpoint,
        "actors": actors,
        "player_role": role,
        "moves": MOVE_TEMPLATES,
        "starting_defcon": flashpoint["defcon_start"],
        "starting_tension": flashpoint["tension_start"],
        "sigma_reference": flashpoint["sigma_ref"],
    }

def get_all_flashpoints():
    return FLASHPOINTS
