import random
from enum import Enum
from typing import List
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from words import WORDS, EMOJIS

BASE_DIR = Path(__file__).parent.resolve()
USED_WORDS_PATH = BASE_DIR / "used_words.txt"


class Color(Enum):
    WHITE = (1, 1, 1)
    YELLOW = (1, 1, 0)
    BLUE = (0.53, 0.81, 0.98)
    RED = (1, 0.4, 0.4)
    BLACK = (0, 0, 0)


def plot_grid(
    colors: List[List[Color]],
    words: List[str],
) -> plt.Figure:
    if words is None:
        raise ValueError("Words must be provided")
    if len(words) != 25:
        raise ValueError("Words must have 25 elements")
    if len(colors) != 5 or any(len(row) != 5 for row in colors):
        raise ValueError("Colors must be a 5x5 matrix")

    fig, ax = plt.subplots()
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)

    for i in range(5):
        for j in range(5):
            create_rectangle(
                ax=ax,
                row=i,
                col=j,
                color=colors[i][j],
                text=words[i * 5 + j],
            )

    ax.set_xticks(np.arange(0, 6, 1))
    ax.set_yticks(np.arange(0, 6, 1))
    ax.grid(True)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.gca().invert_yaxis()
    return fig


def create_rectangle(
    ax: plt.Axes,
    row: int,
    col: int,
    color: Color,
    text: str = "",
) -> None:
    rectangle_size = 0.8
    offset = (1 - rectangle_size) / 2
    square = plt.Rectangle(
        (row + offset, col + offset),
        rectangle_size,
        rectangle_size,
        edgecolor="black",
        facecolor=color.value,
    )
    text_color = "white" if color == Color.BLACK else "black"
    ax.text(
        row + 0.5,
        col + 0.5,
        text,
        color=text_color,
        horizontalalignment="center",
        verticalalignment="center",
    )
    ax.add_patch(square)


def generate_custom_colors() -> List[List[Color]]:
    colors = [[Color.YELLOW for _ in range(5)] for _ in range(5)]
    positions = [(i, j) for i in range(5) for j in range(5)]

    blue_positions = random.sample(positions, 8)
    for pos in blue_positions:
        colors[pos[0]][pos[1]] = Color.BLUE

    positions = [pos for pos in positions if pos not in blue_positions]
    red_positions = random.sample(positions, 8)
    for pos in red_positions:
        colors[pos[0]][pos[1]] = Color.RED

    positions = [pos for pos in positions if pos not in red_positions]
    extra_color_position = random.choice(positions)
    colors[extra_color_position[0]][extra_color_position[1]] = random.choice(
        [Color.RED, Color.BLUE]
    )

    positions = [pos for pos in positions if pos != extra_color_position]
    black_position = random.choice(positions)
    colors[black_position[0]][black_position[1]] = Color.BLACK

    return colors


def generate_white_colors() -> List[List[Color]]:
    return [[Color.WHITE for _ in range(5)] for _ in range(5)]


def choose_words(available_words: List[str] = WORDS, n: int = 25) -> List[str]:
    used_words = read_used_words()
    words = random.sample(list(set(available_words) - set(used_words)), n)
    write_used_words(words)
    return words


def read_used_words() -> List[str]:
    if not USED_WORDS_PATH.exists():
        return []
    with USED_WORDS_PATH.open("r") as f:
        return f.read().splitlines()


def write_used_words(words: List[str]) -> None:
    with USED_WORDS_PATH.open("a") as f:
        for word in words:
            f.write(word + "\n")


def generate_boards() -> List[List[str]]:
    words: list[str] = choose_words(available_words=EMOJIS)
    colors: list[list[Color]] = generate_custom_colors()
    whites: list[list[Color]] = generate_white_colors()

    capitan_board = plot_grid(colors=colors, words=words)
    player_board = plot_grid(colors=whites, words=words)

    return capitan_board, player_board


if __name__ == "__main__":
    capitan_board, player_board = generate_boards()

    capitan_board.savefig("capitan_board.png")
    player_board.savefig("player_board.png")
