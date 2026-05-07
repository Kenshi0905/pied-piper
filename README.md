```
  ██████╗ ██╗███████╗██████╗     ██████╗ ██╗██████╗ ███████╗██████╗
  ██╔══██╗██║██╔════╝██╔══██╗    ██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
  ██████╔╝██║█████╗  ██║  ██║    ██████╔╝██║██████╔╝█████╗  ██████╔╝
  ██╔═══╝ ██║██╔══╝  ██║  ██║    ██╔═══╝ ██║██╔═══╝ ██╔══╝  ██╔══██╗
  ██║     ██║███████╗██████╔╝    ██║     ██║██║     ███████╗██║  ██║
  ╚═╝     ╚═╝╚══════╝╚═════╝     ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝

  JOINT WAR GAMES AGENCY  ·  CLASSIFICATION: TOP SECRET  ·  v2.0
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-32cd32?style=flat-square&labelColor=0d0d0d&color=32cd32)
![License](https://img.shields.io/badge/License-MIT-32cd32?style=flat-square&labelColor=0d0d0d)
![Terminal](https://img.shields.io/badge/Interface-Terminal%20%2F%20CLI-32cd32?style=flat-square&labelColor=0d0d0d)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-32cd32?style=flat-square&labelColor=0d0d0d)
![Status](https://img.shields.io/badge/Status-Active%20Development-32cd32?style=flat-square&labelColor=0d0d0d)

**A terminal-based nuclear war simulation system — inspired by the 1983 film *WarGames* —**  
**powered by a Bayesian probability engine built on real declassified US military wargame documents.**

*SHALL WE PLAY A GAME?*

</div>

---

## ◈ What Is This

**Pied Piper** is a command-line war game system that lets you play as any of the nine nuclear-armed states in the world and navigate a geopolitical crisis — making strike decisions, deploying diplomacy, running covert operations, and watching probabilities cascade in real time.

It is also a collection of classic arcade games (Chess, Sudoku, Poker, Hangman, Minesweeper, Number Guess) — all wrapped in a cinematic WarGames-style CRT terminal interface with typewriter animations, ASCII maps, missile trajectory renders, and a hidden easter egg that ends the session the way the movie does.

The war game is not a typical strategy game. Every decision you make is evaluated by a **probability engine trained on real declassified US military wargame documents**: Sigma I-64 (1964), the Desert Crossing After-Action Report (1999), and analyses of Millennium Challenge 2002. The probabilities you see are not invented — they are the historically observed outcomes from real wargames, encoded as Bayesian priors and applied to your decisions.

---

## ◈ Source Documents

The probability engine is grounded in the following primary sources:

| Document | Year | Classification | Source |
|---|---|---|---|
| **SIGMA I-64 Final Report** (CM-1325-64) | 1964 | Declassified | LBJ Presidential Library |
| **Desert Crossing After-Action Report** | 1999 | Declassified | NSA Electronic Briefing Book #207 |
| **Millennium Challenge 2002** analysis | 2002 | Open Source | Micah Zenko / FOIA materials |
| **Perla — Wargaming and the Cycle of Research** | 2022 | Open Source | Scandinavian Journal of Military Studies |
| **Caffrey — On Wargaming** | 2019 | Open Source | Naval War College Press |
| **CNA wargaming research** (CNA) | ongoing | Open Source | Center for Naval Analyses |

### What the documents teach the engine

**SIGMA I-64 (1964):**  
A Top Secret war game run by the Joint Chiefs of Staff in April 1964, sponsored by the Chairman of the JCS. Gamed a graduated air pressure campaign against North Vietnam. Key encoded finding: bombing stiffened adversary will to resist (71% historical rate). Each escalatory move by Blue (US) lowered the CPR (China) intervention threshold by ~12%. The game's results were never passed beyond Secretary McNamara's desk to President Johnson. The war continued for eleven more years. Pied Piper applies a **0.62× success multiplier** to air strike campaigns in direct reference to this finding.

**Desert Crossing AAR (1999):**  
Gamed post-Saddam regime change. Scenario: "Saddam assassinated by son Uday, June 21st." Move 2: rival commanders declared autonomous regions. Move 3: Shia and Kurd uprisings complicated stabilization. Found that regime change causes sectarian fragmentation (74%), neighbor interference (61%), and insurgency emergence (69%). Results were not applied when the Iraq War was launched in 2003. Pied Piper applies a **post-strike stability penalty** sourced directly from this game's outcome data.

**Millennium Challenge 2002:**  
Rehearsal for the Iraq War. Red Team (Gen. Van Riper) used low-tech asymmetric tactics — motorcycle messengers, light signals, suicide boat swarms — to sink 16 Blue Team ships in minutes. The exercise was then re-run with scripted results to validate predetermined conclusions. Pied Piper applies a **0.42× technology superiority discount** when conventional assault faces a motivated adversary, sourced from Van Riper's findings.

---

## ◈ Features

### Global Thermonuclear War — the main event

- **9 playable nations**: USA, Russia, China, UK, France, India, Pakistan, Israel, North Korea — each with full doctrine profiles, arsenal data, readiness scores, C2 resilience, economic power, and historical wargame-derived modifiers
- **7 crisis flashpoints**: Taiwan Strait, Korean Peninsula, South Asia Nuclear Flash, Middle East Samson Threshold, NATO Eastern Flank, Arctic Confrontation, Indo-Pacific Alliance Realignment
- **Bayesian probability engine**: priors update every turn based on your escalation history, diplomatic actions, covert ops, and intel degradation
- **6 probability bars per strike**: Success, Retaliation Risk, Survival, Third-Party Intervention, Black Swan, Post-Strike Stability
- **Doctrine warnings**: Before every strike, the engine surfaces relevant historical lessons from your source documents
- **Black Swan events**: 10 Perla/Nimitz-class surprise events (decapitation strikes, EMP blackouts, unauthorized launches, ally defections, coup attempts)
- **Full action suite**: Nuclear strike, Air strike, SLBM launch, Conventional assault, Covert operation, Diplomatic signal, Intelligence operation, DEFCON management, Stand down
- **Animated ASCII map**: missile trajectory animation across a world map with all 9 nations marked
- **Historical Doctrine Browser**: in-game — read all six source scenarios, their key findings, observed outcome distributions, and exact probability modifiers being applied to your decisions
- **Full after-action report**: generated at the end of every session with doctrine assessment

### Arcade games

| Game | Notes |
|---|---|
| ♟ Chess | Full legal move validation, capture-preferring + check-seeking CPU, algebraic notation |
| ■ Sudoku | Procedurally generated, valid puzzles, yellow highlights for your placements |
| ♠ Poker | 5-card draw vs CPU with hand evaluation, betting, split pots |
| ☠ Hangman | Military and nuclear lexicon (DETERRENCE, PROLIFERATION, MINUTEMAN...) |
| ✦ Minesweeper | 9×9 grid, flag mode, auto-reveal on empty cells |
| ? Number Guess | 1–100, 7 attempts, hot/cold feedback |

### Terminal UI
- Green-on-black or white-on-black — toggled in-menu, saved permanently
- CRT-style boot sequence with realistic delay timing
- Typewriter slow-print for all scenario text and doctrine warnings
- Glitch cascade effect (on the easter egg and on escalation events)
- Persistent logon ID — enter something you love, it's remembered forever
- Fully cross-platform: bash, zsh, fish, PowerShell, Windows CMD

### The Easter Egg
Type `TIC TAC TOE` at the main menu. Don't say we didn't warn you.

---

## ◈ Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/pied-piper.git
cd pied-piper

# Install dependencies
pip install chess

# Run
python pied_piper.py
```

**Requirements:** Python 3.9+ · `chess` library · A terminal that supports ANSI escape codes (any modern terminal does)

**Tested on:** macOS Terminal, iTerm2, Windows Terminal (PowerShell), VS Code integrated terminal, Ubuntu bash

---

## ◈ Project Structure

```
pied-piper/
│
├── pied_piper.py           ← Entry point: boot, logon, menu, easter egg
│
├── engine/
│   ├── nations.py          ← All 9 nuclear nations: doctrine, arsenal, readiness
│   ├── probability.py      ← Bayesian engine + Sigma/Perla/Desert Crossing data
│   └── scenarios.py        ← Dynamic scenario generator: 7 global flashpoints
│
├── ui/
│   ├── terminal.py         ← Colors, animations, cross-platform clear, box drawing
│   └── map_renderer.py     ← ASCII world map + missile trajectory animation
│
├── games/
│   ├── arcade.py           ← Chess, Sudoku, Poker, Hangman, Minesweeper, Number Guess
│   └── war_game.py         ← Full Global Thermonuclear War game loop
│
└── README.md
```

---

## ◈ How the Probability Engine Works

Every decision you make passes through three layers:

**Layer 1 — Nation capabilities**
Base success probability is calculated from the attacker's doctrine profile (first-strike vs. second-strike rate), defender's missile defense score, arsenal ratio, alliance bonus, readiness, intel score, and C2 resilience.

**Layer 2 — Historical doctrine modifiers**
Scenario-specific multipliers sourced directly from the wargame documents are applied:

```
Air strike against adversary?
  → Sigma I-64 modifier: ×0.62 (bombing stiffens will to resist)
  → Will-to-resist bonus applied to defender: ×1.45
  → World opinion penalty: −8% per strike

Conventional assault?
  → MC '02 modifier: ×0.42 (tech superiority discounted by asymmetric tactics)
  → Asymmetric counter-attack probability surfaced

Post-strike stability?
  → Desert Crossing: sectarian fragmentation 74%, insurgency 69%
  → Stability multiplier: ×0.48

Escalation history?
  → Each prior escalation: +12% third-party intervention risk
  → Retaliation probability scaled by escalation count
```

**Layer 3 — Bayesian updating**
After every action, priors shift. Tension accumulates. Third-party risk rises. World opinion moves. Intel degrades after Black Swan events. DEFCON updates automatically from the cumulative tension level. The game gets harder to control the deeper you go — which is the point.

---

## ◈ Nation Profiles

| Code | Nation | Warheads | Doctrine | Readiness |
|---|---|---|---|---|
| `USA` | United States | 5,550 | Flexible Response / Nuclear Triad | 85% |
| `RUS` | Russian Federation | 6,257 | Escalate to De-Escalate | 88% |
| `CHN` | People's Republic of China | 350 | Minimum Deterrence / No First Use | 70% |
| `UK`  | United Kingdom | 225 | Minimum Credible Deterrence | 65% |
| `FRA` | French Republic | 290 | Strict Sufficiency | 62% |
| `IND` | Republic of India | 160 | No First Use / Massive Retaliation | 55% |
| `PAK` | Islamic Republic of Pakistan | 165 | Full Spectrum Deterrence | 58% |
| `ISR` | State of Israel | 90 | Nuclear Ambiguity (Samson Option) | 72% |
| `PRK` | DPRK | 50 | Coercive Deterrence | 60% |

---

## ◈ Crisis Flashpoints

| Scenario | Primary Actors | Starting DEFCON |
|---|---|---|
| Taiwan Strait Crisis | CHN vs USA | 3 |
| Korean Peninsula Escalation | PRK vs USA | 2 |
| South Asia Nuclear Flash | IND vs PAK | 3 |
| Middle East — Samson Threshold | ISR vs RUS | 2 |
| NATO Eastern Flank | RUS vs USA | 2 |
| Arctic Confrontation | RUS vs USA | 3 |
| Indo-Pacific Alliance Realignment | CHN vs USA | 4 |

Each scenario is structured in three moves — analogous to the Sigma I-64 game format — with Blue options, Red options, and a Control Team projection encoded in the scenario engine.

---

## ◈ Inspiration

This project draws from:

- **WarGames (1983)** — WOPR, Joshua, the logon sequence, the DEFCON display, "the only winning move is not to play"
- **SIGMA I-64 / SIGMA II-64 (1964)** — the JCS wargames that predicted US failure in Vietnam, whose results were never passed to the President
- **Desert Crossing (1999)** — the wargame that predicted every major failure of the Iraq War, whose results were ignored
- **Millennium Challenge 2002** — the exercise that predicted asymmetric vulnerability, then was scripted to hide it
- **Peter Perla, *The Art of Wargaming*** — "Nothing that happened in the Pacific was strange or unexpected — except the Kamikaze tactics." — Nimitz
- **Matthew Caffrey, *On Wargaming*** — Prussian Kriegsspiel and the decisive advantage of integrated staff wargaming
- **Johnny Harris / CNA** — "The most enduring puzzle of these games is how little impact they made."

---

## ◈ The Lesson

Every game ends with an after-action report. If you escalated more than you negotiated, the system tells you. If you suffered more than you inflicted, the system tells you. If Black Swan events exceeded baseline, the system quotes Perla.

Sigma I-64 ran in 1964. The findings — that bombing stiffens resistance, that escalation invites counter-escalation, that air pressure alone cannot force capitulation — were clear. They were not passed to President Johnson. The war in Vietnam continued for eleven more years.

Desert Crossing ran in 1999. It found that regime change triggers fragmentation, insurgency, and regional destabilization. It was not applied in 2003.

The purpose of a wargame is not to win. It is to understand what happens when you do.

---

## ◈ Future Roadmap

- [ ] Integrate more scenarios
- [ ] Integrate Sounds
- [ ] More detailed maps
- [ ] More targets to strike
- [ ] Historical Wargames

---

## ◈ Contributing

Pull requests welcome. If you have access to additional declassified wargame documents that can be encoded as probability distributions, open an issue — that is exactly what this project is built to absorb.

---

## ◈ License

MIT. Do whatever you want with it. Just don't script the results.

---

<div align="center">

```
  A STRANGE GAME.
  THE ONLY WINNING MOVE IS NOT TO PLAY.
```

*— WOPR / Joshua, 1983*  
*— Sigma I-64, 1964, encoded*

</div>