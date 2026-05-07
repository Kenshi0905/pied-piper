"""
PIED PIPER — Nation Profiles
All nine nuclear-armed states with doctrine, arsenal, readiness,
alliance data, and historical wargame-derived modifiers.
"""

NATIONS = {
    "USA": {
        "full": "UNITED STATES OF AMERICA",
        "capital": "WASHINGTON D.C.",
        "warheads": 5550, "icbm": 400, "slbm": 280, "bomber": 60,
        "defense": 0.72, "first_strike": 0.68, "second_strike": 0.91,
        "allies": ["UK", "FRA"],
        "rivals": ["RUS", "CHN", "PRK"],
        "doctrine": "FLEXIBLE RESPONSE / NUCLEAR TRIAD",
        "doctrine_detail": (
            "The US maintains a nuclear triad of ICBMs, SLBMs, and strategic bombers. "
            "Doctrine emphasizes flexible response across the escalation ladder. "
            "Extended deterrence covers NATO allies. No-first-use is NOT policy."
        ),
        "readiness": 85,
        "intel_score": 92,
        "economy": 98,
        "conventional_strength": 95,
        "c2_resilience": 88,                                  
        "sigma_modifier": 1.0,                                    
        "color": "B",
    },
    "RUS": {
        "full": "RUSSIAN FEDERATION",
        "capital": "MOSCOW",
        "warheads": 6257, "icbm": 306, "slbm": 176, "bomber": 55,
        "defense": 0.69, "first_strike": 0.71, "second_strike": 0.88,
        "allies": [],
        "rivals": ["USA", "UK", "FRA"],
        "doctrine": "ESCALATE TO DE-ESCALATE",
        "doctrine_detail": (
            "Russia's doctrine permits first use of nuclear weapons if the state faces "
            "existential threat — including from conventional attack. 'Escalate to "
            "de-escalate' envisions limited nuclear use to terminate a losing conventional war."
        ),
        "readiness": 88,
        "intel_score": 88,
        "economy": 55,
        "conventional_strength": 82,
        "c2_resilience": 80,
        "sigma_modifier": 0.95,                                                       
        "color": "R",
    },
    "CHN": {
        "full": "PEOPLE'S REPUBLIC OF CHINA",
        "capital": "BEIJING",
        "warheads": 350, "icbm": 100, "slbm": 48, "bomber": 20,
        "defense": 0.55, "first_strike": 0.45, "second_strike": 0.62,
        "allies": [],
        "rivals": ["USA", "IND"],
        "doctrine": "MINIMUM DETERRENCE / NO FIRST USE",
        "doctrine_detail": (
            "China maintains a No First Use pledge and a minimum credible deterrent. "
            "Arsenal is expanding rapidly toward 1,000+ warheads by 2030. "
            "Underground 'Underground Great Wall' tunnel system protects second-strike capability."
        ),
        "readiness": 70,
        "intel_score": 80,
        "economy": 88,
        "conventional_strength": 80,
        "c2_resilience": 72,
        "sigma_modifier": 0.90,                                                           
        "color": "Y",
    },
    "UK": {
        "full": "UNITED KINGDOM",
        "capital": "LONDON",
        "warheads": 225, "icbm": 0, "slbm": 48, "bomber": 0,
        "defense": 0.60, "first_strike": 0.50, "second_strike": 0.72,
        "allies": ["USA", "FRA"],
        "rivals": ["RUS"],
        "doctrine": "MINIMUM CREDIBLE DETERRENCE",
        "doctrine_detail": (
            "UK relies solely on Trident SLBM submarines. A single Vanguard-class SSBN "
            "is on continuous at-sea deterrent patrol at all times. "
            "Decision to use is sovereign but coordinated with NATO."
        ),
        "readiness": 65,
        "intel_score": 85,
        "economy": 72,
        "conventional_strength": 62,
        "c2_resilience": 68,
        "sigma_modifier": 1.0,
        "color": "C",
    },
    "FRA": {
        "full": "FRENCH REPUBLIC",
        "capital": "PARIS",
        "warheads": 290, "icbm": 0, "slbm": 48, "bomber": 54,
        "defense": 0.58, "first_strike": 0.48, "second_strike": 0.70,
        "allies": ["USA", "UK"],
        "rivals": ["RUS"],
        "doctrine": "STRICT SUFFICIENCY",
        "doctrine_detail": (
            "France maintains a doctrine of 'strict sufficiency' — enough to deter "
            "any adversary from concluding that the gain from attacking France would "
            "outweigh the risk of unacceptable damage. Arsenal is entirely "
            "submarine-based and air-launched. Independence from NATO command is key."
        ),
        "readiness": 62,
        "intel_score": 78,
        "economy": 74,
        "conventional_strength": 60,
        "c2_resilience": 65,
        "sigma_modifier": 1.0,
        "color": "C",
    },
    "IND": {
        "full": "REPUBLIC OF INDIA",
        "capital": "NEW DELHI",
        "warheads": 160, "icbm": 0, "slbm": 0, "bomber": 0,
        "defense": 0.40, "first_strike": 0.38, "second_strike": 0.55,
        "allies": [],
        "rivals": ["PAK", "CHN"],
        "doctrine": "NO FIRST USE / MASSIVE RETALIATION",
        "doctrine_detail": (
            "India pledges No First Use but promises massive retaliation if nuclear "
            "weapons are used against India or its forces. "
            "Developing sea-based Arihant-class SSBN for survivable second strike. "
            "Agni-V ICBM brings all of China in range."
        ),
        "readiness": 55,
        "intel_score": 68,
        "economy": 70,
        "conventional_strength": 65,
        "c2_resilience": 58,
        "sigma_modifier": 0.88,
        "color": "G",
    },
    "PAK": {
        "full": "ISLAMIC REPUBLIC OF PAKISTAN",
        "capital": "ISLAMABAD",
        "warheads": 165, "icbm": 0, "slbm": 0, "bomber": 0,
        "defense": 0.38, "first_strike": 0.42, "second_strike": 0.50,
        "allies": [],
        "rivals": ["IND"],
        "doctrine": "FULL SPECTRUM DETERRENCE",
        "doctrine_detail": (
            "Pakistan explicitly rejects No First Use. Full Spectrum Deterrence "
            "includes tactical nuclear weapons (Nasr / HATF-9) designed for "
            "battlefield use against Indian armored advances. "
            "Decentralized command increases first-use risk in crisis."
        ),
        "readiness": 58,
        "intel_score": 60,
        "economy": 38,
        "conventional_strength": 52,
        "c2_resilience": 48,
        "sigma_modifier": 0.85,
        "color": "G",
    },
    "ISR": {
        "full": "STATE OF ISRAEL",
        "capital": "JERUSALEM",
        "warheads": 90, "icbm": 0, "slbm": 0, "bomber": 0,
        "defense": 0.65, "first_strike": 0.55, "second_strike": 0.60,
        "allies": [],
        "rivals": ["IRN"],
        "doctrine": "NUCLEAR AMBIGUITY (SAMSON OPTION)",
        "doctrine_detail": (
            "Israel maintains deliberate nuclear ambiguity — neither confirming nor "
            "denying its arsenal. The 'Samson Option' describes last-resort use "
            "against existential threats. Arrow/Iron Dome/David's Sling provide "
            "layered missile defense. Likely has submarine-launched cruise missiles."
        ),
        "readiness": 72,
        "intel_score": 90,
        "economy": 76,
        "conventional_strength": 68,
        "c2_resilience": 70,
        "sigma_modifier": 0.92,
        "color": "Y",
    },
    "PRK": {
        "full": "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA",
        "capital": "PYONGYANG",
        "warheads": 50, "icbm": 10, "slbm": 0, "bomber": 0,
        "defense": 0.25, "first_strike": 0.35, "second_strike": 0.40,
        "allies": [],
        "rivals": ["USA", "KOR"],
        "doctrine": "COERCIVE DETERRENCE",
        "doctrine_detail": (
            "North Korea uses nuclear threats for coercive bargaining, regime survival, "
            "and to deter US intervention. Hwasong-17 ICBM can reach the continental US. "
            "Doctrine emphasizes pre-emptive nuclear use if regime faces existential threat. "
            "C2 is opaque and centralized on Supreme Leader."
        ),
        "readiness": 60,
        "intel_score": 35,
        "economy": 12,
        "conventional_strength": 45,
        "c2_resilience": 38,
        "sigma_modifier": 0.80,
        "color": "R",
    },
}

NATION_KEYS = list(NATIONS.keys())

def get_nation(code):
    return NATIONS.get(code.upper())

def list_nations():
    return [(k, v["full"]) for k, v in NATIONS.items()]
