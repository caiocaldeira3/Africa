import glob
import time
import threading
import dataclasses as dc

import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from player import Player
import config

@dc.dataclass(init=False)
class Africa:
    words: list[str]
    round_score: np.ndarray[int]
    teams_score: np.ndarray[int]

    window: tk.Tk
    text_widget: tk.Label
    timer_widget: tk.Label

    yes_button: tk.Button
    no_button: tk.Button
    back_button: tk.Button

    game_on: bool

    def __init__ (self) -> None:
        words_set = set()

        for file_name in glob.glob("palavras/*.txt"):
            with open(file_name, "r") as fr:
                file_words = { word for word in fr.read().split("\n") if word != "" }

                words_set |= file_words

        self.words = list(words_set)
        self.teams_score = np.array([ 0, 0 ])
        self.round_score = np.array([ 0, 0 ])

        self.window = tk.Tk()
        self.game_on = False

        self.__post_init__()

    def __post_init__ (self) -> None:
        self.window.title("Africa")
        self.window.geometry("650x250")
        self.window.configure(bg=config.BG_COLOR)

        text_frame = ttk.Frame(self.window)

        self.text_widget = tk.Label(
            text_frame, bg=config.BG_COLOR, fg=config.TEXT_COLOR, font=config.FONT,
            width=20, height=5, text=""
        )
        self.text_widget.grid(row=0, column=0)

        self.timer_widget = tk.Label(
            text_frame, bg=config.BG_GRAY, font=config.FONT, text="00",
            width=20, height=5
        )
        self.timer_widget.grid(row=0, column=1)

        text_frame.pack(side=tk.TOP, pady=15, padx=15)
        button_frame = ttk.Frame(self.window)

        self.yes_button = tk.Button(
            button_frame, text="Acertaram", command=(lambda: config.next_word("s")),
            relief="solid"
        )
        self.yes_button.grid(row=0, column=0)

        self.no_button = tk.Button(
            button_frame, text="Não Conta", command=(lambda: config.next_word("n")),
            relief="solid"
        )
        self.no_button.grid(row=0, column=1)

        self.back_button = tk.Button(
            button_frame, text="Voltar", command=config.backtrack, relief="solid")
        self.back_button.grid(row=0, column=2)

        button_frame.pack(side=tk.TOP, pady=15)

    async def run (self) -> None:
        threading.Thread(target=self.start_game).start()

        self.window.mainloop()

    def start_game (self) -> None:
        time.sleep(1)
        self.game_on = True

        curr_player = Player(0)
        for _ in [ 1, 2, 3]:
            curr_player = self.start_round(curr_player)

            self.update_score()

        str_score = " x ".join(map(str, self.teams_score))
        messagebox.showinfo("Placar da Rodada", str_score)

        self.game_on = False
        self.window.destroy()

    def start_round (self, curr_player: Player) -> Player:
        config.build_words(self.words)

        while config.has_words():
            if np.isclose(curr_player.remaining_time, 0):
                curr_player = Player(curr_player.oposing_team)

            self.wait_ready()
            self.round_score[curr_player.team] += self.play(curr_player)

            config.reset_response()

        return curr_player

    def play (self, player: Player) -> int:
        score: int = 0
        last_score: bool = False

        player.reset_turn()

        timer_thread = threading.Thread(target=self.timer, args=(player, ))
        timer_thread.start()

        self.print_word_info()

        while not player.empty_timer and config.has_words():
            if config.CURR_RESPONSE is None:
                continue

            if config.CURR_RESPONSE == "s":
                score += 1
                last_score = True

            elif config.CURR_RESPONSE == "v" and last_score:
                score -= 1
                last_score = False

            else:
                last_score = False

            self.print_word_info()
            config.reset_response()

        if config.CURR_RESPONSE == "s":
            score += 1

        config.reset_response()

        player.end_turn()
        return score

    def timer (self, player: Player) -> None:
        self.timer_widget.config(text=f"{player.remaining_time:02}")
        time.sleep(1)

        while config.has_words():
            player.remaining_time -= 1
            self.timer_widget.config(text=f"{player.remaining_time:02}")

            if player.remaining_time == 0:
                break

            time.sleep(1)

        player.end_turn()

    def print_word_info (self) -> None:
        self.text_widget.config(text=f"{config.get_curr_word()}\n")

    def wait_ready (self) -> None:
        self.reset_round()

        messagebox.showinfo("Novo Turno", "Aperte Ok para começar")

    def reset_round (self) -> None:
        self.text_widget.config(text="")
        self.timer_widget.config(text="00")

    def update_score (self) -> None:
        str_score = " x ".join(map(str, self.round_score))

        messagebox.showinfo("Placar da Rodada", str_score)

        self.teams_score += self.round_score
        self.round_score = np.array([ 0, 0 ])
