# Solving a Simplified Two-Player Poker Game using Counterfactual Regret Minimization (CFR)

This project consists in solving a simplified two-player poker game using the **Counterfactual Regret Minimization (CFR)** algorithm.

The goal of the solver is to learn optimal strategies for both players by simulating millions of poker games and minimizing regret over time.
At the end of the training process, the learned strategies are visualized using **heatmaps exported to a PDF file**.

---

# Project Overview

Poker is an **imperfect information game**, meaning that players do not know the opponent's private cards. Solving such games requires specialized algorithms.

This project uses **Counterfactual Regret Minimization (CFR)**, a widely used algorithm in poker AI research that approximates **Nash equilibrium strategies**.

After training, the solver outputs:

- the expected value of the game
- optimized strategies
- heatmap visualizations of the strategies
- a PDF file containing all strategy maps

---

# Game Description

This project models a **simplified heads-up poker game**.

## Players

- 2 players
- Each player receives **two private cards**
- No community cards

## Deck

A standard **52-card deck** is used.

Each player receives two cards randomly.

---

# Hand Representation

Hands are represented using standard poker notation:

```
AA
AKs
KQo
72o
```

Where:

- `s` = suited
- `o` = offsuit
- no suffix = pair

Examples:

| Hand | Meaning |
|-----|------|
| AA | pocket aces |
| AKs | ace-king suited |
| KQo | king-queen offsuit |
| 72o | seven-two offsuit |

---

# Betting Structure

Each player starts by posting an ante.

```
ante = 1
```

Players then go through a simplified betting round.

## Available Actions

Players may choose between:

```
check
bet
call
raise
fold
```

## Bet Sizes

Two betting sizes are implemented:

```
bet1 = 2
bet2 = 8
```

These values determine the size of the pot and the payoff at the end of the hand.

---

# Algorithm

The solver uses **Counterfactual Regret Minimization (CFR)**.

CFR works by repeatedly simulating games and updating **regret values** for each decision point.

At each iteration:

1. Two hands are randomly dealt
2. The game tree is traversed
3. Counterfactual utilities are computed
4. Regret values are updated
5. The average strategy is updated

Over time, the algorithm converges toward a **Nash equilibrium strategy**.

---

# Training

Training consists of running a large number of CFR iterations.

Example:

```
iterations = 4_000_000
```

Typical output after training:

```
Training result after 4000000 iterations: -0.07155684070156848
Heatmaps saved in results/strategies.pdf
```

The displayed value corresponds to the **expected value for Player 1 per hand**.

If the algorithm converges toward equilibrium, this value should approach:

```
EV ≈ 0
```

---

# Strategy Visualization

After training, the solver generates **heatmaps representing strategies**.

Each heatmap shows the probability of choosing a specific action for every possible starting hand.

# Running the Solver

To run the solver:

```
pip install -r requirements.txt
python main.py
```
---

# Possible Improvements

This project can be extended in several ways.

## Algorithm Improvements

- implement **CFR+**
- implement **Monte Carlo CFR**
- compute **exploitability**
- add **convergence tracking**

## Game Improvements

- add **community cards**
- implement **multiple betting rounds**
- allow **multiple bet sizes**

## Visualization Improvements

- strategy comparison
- convergence graphs
- interactive visualization tools
