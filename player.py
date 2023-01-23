

import sys

class Player:
    team: int
    remaining_time: float

    empty_timer: bool
    empty_words: bool

    def __init__ (self, team: int) -> None:
        self.team = team
        self.remaining_time = 60 if len(sys.argv) == 1 else int(sys.argv[1])

    def reset_turn (self) -> None:
        self.empty_timer = False
        self.empty_words = False

    def end_turn (self) -> None:
        self.empty_timer = True
        self.empty_words = True

    @property
    def oposing_team (self) -> int:
        return (self.team + 1) % 2
