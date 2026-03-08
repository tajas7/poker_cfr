import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from CFR import CFR
from Game import Game

hands = [
    ["AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s"],
    ["AKo", "KK", "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s"],
    ["AQo", "KQo", "QQ", "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s"],
    ["AJo", "KJo", "QJo", "JJ", "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s"],
    ["ATo", "KTo", "QTo", "JTo", "TT", "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s"],
    ["A9o", "K9o", "Q9o", "J9o", "T9o", "99", "98s", "97s", "96s", "95s", "94s", "93s", "92s"],
    ["A8o", "K8o", "Q8o", "J8o", "T8o", "98o", "88", "87s", "86s", "85s", "84s", "83s", "82s"],
    ["A7o", "K7o", "Q7o", "J7o", "T7o", "97o", "87o", "77", "76s", "75s", "74s", "73s", "72s"],
    ["A6o", "K6o", "Q6o", "J6o", "T6o", "96o", "86o", "76o", "66", "65s", "64s", "63s", "62s"],
    ["A5o", "K5o", "Q5o", "J5o", "T5o", "95o", "85o", "75o", "65o", "55", "54s", "53s", "52s"],
    ["A4o", "K4o", "Q4o", "J4o", "T4o", "94o", "84o", "74o", "64o", "54o", "44", "43s", "42s"],
    ["A3o", "K3o", "Q3o", "J3o", "T3o", "93o", "83o", "73o", "63o", "53o", "43o", "33", "32s"],
    ["A2o", "K2o", "Q2o", "J2o", "T2o", "92o", "82o", "72o", "62o", "52o", "42o", "32o", "22"]
]

def color(strategy):
    if strategy >= 0.90:
        return "green"
    elif strategy >= 0.75:
        return "greenyellow"
    elif strategy >= 0.50:
        return "yellow"
    elif strategy >= 0.25:
        return "orange"
    elif strategy >= 0.05:
        return "tomato"
    else:
        return "red"

if __name__ == "__main__":
    game = Game()
    cfr = CFR(game)
    iterations = 4000000
    result = cfr.train(iterations)
    print(f"Training result after {iterations} iterations: {result}")

    strategy = cfr.get_strategy()
    print("Optimized strategy:")

    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "strategies.pdf")

    with PdfPages(pdf_path) as pdf:
        for key, value in strategy.items():
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.set_xlim(0, 13)
            ax.set_ylim(0, 13)
            ax.set_xticks([])
            ax.set_yticks([])

            for i in range(13):
                for j in range(13):
                    text = hands[i][j] if i < len(hands) and j < len(hands[i]) else ""
                    ax.add_patch(
                        plt.Rectangle(
                            (j, 12-i), 1, 1,
                            edgecolor='black',
                            facecolor=color(value.get(text, 0))
                        )
                    )
                    ax.text(j + 0.5, 12-i + 0.5, text, ha='center', va='center', fontsize=12, color='black')

            grad = list("AKQJT98765432")
            ax.set_xticks(np.arange(13) + 0.5)
            ax.set_yticks(np.arange(13) + 0.5)
            ax.set_xticklabels(grad, fontsize=12)
            ax.set_yticklabels(grad[::-1], fontsize=12)

            plt.title(key)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

    print(f"Heatmaps saved in {pdf_path}")
