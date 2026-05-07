"""
PIED PIPER — State Bridge
Writes game state to ~/.pied_piper_state.json after every action.
The map window polls this file every 300ms and redraws.
"""
import json
import time
from pathlib import Path

STATE_FILE = Path.home() / ".pied_piper_state.json"

_missile_counter = 0

def push(game_state, scenario=None, missiles=None, extra_events=None):
    """
    Write current GameState to the shared state file.
    Call this after EVERY action in war_game.py.

    Args:
        game_state:    engine.probability.GameState instance
        scenario:      current scenario dict (optional)
        missiles:      list of {src, dst, label, retaliation} dicts to animate
        extra_events:  additional event strings to surface in the ticker
    """
    global _missile_counter

                                                               
                                
    stamped_missiles = []
    for m in (missiles or []):
        _missile_counter += 1
        stamped_missiles.append({
            "src":         m.get("src",""),
            "dst":         m.get("dst",""),
            "label":       m.get("label","ICBM"),
            "retaliation": m.get("retaliation", False),
            "t":           _missile_counter,
        })

    scenario_name = ""
    scenario_actors = []
    if scenario:
        fp = scenario.get("flashpoint", {})
        scenario_name = fp.get("name", "")
        scenario_actors = scenario.get("actors", [])

    state_dict = {
        "player":               game_state.player,
        "defcon":               game_state.defcon,
        "tension":              round(game_state.tension_level, 4),
        "world_opinion":        round(game_state.world_opinion, 4),
        "third_party_risk":     round(game_state.third_party_risk, 4),
        "strikes_launched":     game_state.strikes_launched,
        "strikes_received":     game_state.strikes_received,
        "casualties_inflicted": game_state.casualties_inflicted,
        "casualties_suffered":  game_state.casualties_suffered,
        "black_swans":          len(game_state.black_swans),
        "nations_struck":       list(set(game_state.nations_struck)),
        "active_missiles":      stamped_missiles,
        "events":               game_state.event_log[-30:],
        "scenario_name":        scenario_name,
        "scenario_actors":      scenario_actors,
        "turn":                 game_state.turn,
        "timestamp":            time.time(),
    }

    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state_dict, f)
    except Exception as e:
        pass                                                  


def clear_state():
    """Reset the state file to standby (call on game exit)."""
    try:
        blank = {
            "player": None, "defcon": 5, "tension": 0.0,
            "world_opinion": 0.5, "third_party_risk": 0.10,
            "strikes_launched": 0, "strikes_received": 0,
            "casualties_inflicted": 0, "casualties_suffered": 0,
            "black_swans": 0, "nations_struck": [],
            "active_missiles": [], "events": ["SYSTEM STANDBY."],
            "scenario_name": "STANDBY", "scenario_actors": [],
            "turn": 0, "timestamp": time.time(),
        }
        with open(STATE_FILE, "w") as f:
            json.dump(blank, f)
    except:
        pass
