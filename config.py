import glob
import os

import numpy as np

CURR_WORDS: list[str] = None

CURR_RESPONSE: str | None = None
LAST_WORD: str | None = None
CURR_WORD: str | None = None
NEXT_WORD: str | None = None

TEXT_COLOR: str = "#EAECEE"
BG_COLOR: str = "#18181B"
BG_GRAY: str = "#4B4B4F"
FONT: str = "Helvetica 20"

def build_words (all_words: list[str]) -> None:
    global CURR_WORDS

    CURR_WORDS = all_words.copy()

def has_words () -> bool:
    global CURR_WORDS
    global CURR_WORD

    return len(CURR_WORDS) > 0 or CURR_WORD is not None

def reset_response () -> None:
    global CURR_RESPONSE

    CURR_RESPONSE = None

def backtrack () -> None:
    global CURR_RESPONSE
    global CURR_WORDS
    global LAST_WORD
    global CURR_WORD
    global NEXT_WORD

    if LAST_WORD is not None:
        CURR_RESPONSE = "v"
        NEXT_WORD = CURR_WORD
        CURR_WORD = LAST_WORD
        LAST_WORD = None

        CURR_WORDS.append(CURR_WORD)

    else:
        CURR_RESPONSE = "x"

def get_curr_word () -> None:
    global CURR_WORDS
    global CURR_WORD
    if CURR_WORD is None:
        next_word(None)

    return CURR_WORD

def next_word (action: str) -> None:
    global CURR_RESPONSE
    global CURR_WORDS
    global LAST_WORD
    global CURR_WORD
    global NEXT_WORD
    LAST_WORD = CURR_WORD
    if LAST_WORD is not None:
        CURR_WORDS.remove(LAST_WORD)

    CURR_RESPONSE = action
    if NEXT_WORD is not None:
        CURR_WORD = NEXT_WORD
        NEXT_WORD = None

    elif len(CURR_WORDS) > 0:
        CURR_WORD = np.random.choice(CURR_WORDS)

    else:
        CURR_WORD = None

if __name__ == "__main__":
    for f in glob.glob("palavras/*.txt"):
        os.remove(f)

    n_players = int(input("Número de Jogadores: "))
    n_words = int(input("Nº de Palavras por Jogador: "))

    for _ in range(n_players):
        player = input("Nome: ")

        with open(f"palavras/{player}.txt", "w") as player_file:
            player_file.write("\n".join(
                input(f"{indx}ª Palavra: ") for indx in range(1, n_words + 1)
            ))

        os.system("cls" if os.name == "nt" else "clear")
