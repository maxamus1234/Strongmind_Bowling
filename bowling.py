class BowlingScorecard:
    def __init__(self) -> None:
        self.player_name = ""
        self.get_player_name()

        self.frames = 10
        self.player_roll_scores = []
        self.pins_knocked_during_frame = 0
        self.roll_count = 0

        self.update_player_frame_scores()

    def get_player_name(self):
        self.player_name = input(f'Please enter your name: ')

    # -------------------------------------------------------------
    # update_player_frame_scores loops through each frame and drives
    # score updates per frame
    # -------------------------------------------------------------
    def update_player_frame_scores(self):
        for frame in range(self.frames):
            if frame > 0:
                continue_playing = still_playing(self.player_name)
                if continue_playing == False:
                    self.unfinished_game_handler(frame)
                    break
            self.roll_count = 0
            if frame < 9:
                self.first_and_bonus_roll_handler(frame)
                if self.pins_knocked_during_frame < 10:
                    self.second_roll_handler(frame)
            elif frame == 9:
                self.tenth_frame_handler(frame)

    # -------------------------------------------------------------
    # unfinished_game_handler scores zero's for the remaining frames
    # when a player does not finish the game
    # -------------------------------------------------------------
    def unfinished_game_handler(self, frame):
        while frame < self.frames:
            self.player_roll_scores.append(0)
            self.player_roll_scores.append(0)
            frame += 1

    # -------------------------------------------------------------
    # tenth_frame_handler ensures that players get the extra rolls
    # received when scoring a strike or spare in the 10th round
    # -------------------------------------------------------------
    def tenth_frame_handler(self, frame):
        self.first_and_bonus_roll_handler(frame)
        if self.pins_knocked_during_frame == 10:
            self.bonus_two_rolls(frame)
        if self.pins_knocked_during_frame < 10:
            self.second_roll_handler(frame)
            if self.pins_knocked_during_frame == 10:
                self.first_and_bonus_roll_handler(frame)

    # -------------------------------------------------------------
    # first_and_bonus_roll_handler gets pins knocked for roll and
    # checks whether or not a strike was made
    # -------------------------------------------------------------
    def first_and_bonus_roll_handler(self, frame):
        self.roll_count += 1
        print(f'{self.player_name}, For frame {frame + 1}, Roll {self.roll_count}')
        self.pins_knocked_during_frame = get_pins_knocked()
        if self.pins_knocked_during_frame == 10:
            self.player_roll_scores.append('x')
        elif self.pins_knocked_during_frame < 10:
            self.player_roll_scores.append(
                self.pins_knocked_during_frame)

    # -------------------------------------------------------------
    # second_roll_handler gets pins knocked for roll and
    # checks whether or not a spare was made
    # -------------------------------------------------------------
    def second_roll_handler(self, frame):
        self.roll_count += 1
        print(f'{self.player_name}, For frame {frame + 1}, Roll {self.roll_count}')
        pins_knocked_second_roll = get_pins_knocked(
            self.pins_knocked_during_frame)
        self.pins_knocked_during_frame += pins_knocked_second_roll
        if self.pins_knocked_during_frame == 10:
            self.player_roll_scores.append('/')
        else:
            self.player_roll_scores.append(pins_knocked_second_roll)

    # -------------------------------------------------------------
    # bonus_two_rolls gives two bonus rolls for a strike in the 10th
    # frame, and checks for strikes or spares
    # -------------------------------------------------------------
    def bonus_two_rolls(self, frame):
        self.roll_count += 1
        print(f'{self.player_name}, For frame {frame + 1}, roll {self.roll_count}')
        self.pins_knocked_during_frame = get_pins_knocked()
        if self.pins_knocked_during_frame == 10:
            self.player_roll_scores.append('x')
            self.first_and_bonus_roll_handler(frame)
        elif self.pins_knocked_during_frame < 10:
            self.player_roll_scores.append(
                self.pins_knocked_during_frame)
            self.second_roll_handler(frame)


# -------------------------------------------------------------
# get_pins_knocked is a helper function that gets the pins
# knocked and verifies proper user input
# -------------------------------------------------------------
def get_pins_knocked(firstRoll=0):
    while True:
        try:
            pins_knocked = int(input("How many pins were knocked? "))
        except ValueError:
            print(
                "Sorry, I didn't understand that. make sure to enter a integer value between 0 and 10.")
            continue
        else:
            if (pins_knocked + firstRoll) > 10 or pins_knocked < 0:
                print(
                    f"Sorry, I didn't understand that. make sure to enter a integer value between 0 and {10 - firstRoll}.")
                continue
            else:
                break

    return pins_knocked

# -------------------------------------------------------------
# still_playing is a function that ascertains whether the user
# wants to continue
# -------------------------------------------------------------
def still_playing(name):
    while True:
        answer = input(
            f"{name}, you have completed a Frame! Do you want to continue playing?: ")

        if answer.lower() != 'yes' and answer.lower() != 'no':
            print("please enter either 'yes' or 'no'.")
        elif answer.lower() == 'yes':
            return True
        else:
            return False

# -------------------------------------------------------------
# tally_score is a function that calculates the players final
# score based upon there rolls
# -------------------------------------------------------------
def tally_score(roll_scores: list):
    total_score = 0
    rolls = 0
    for index, roll_score in enumerate(roll_scores):
        if rolls >= 20:
            break
        if roll_score == '/':
            total_score += spare_score(roll_scores, index)
        elif roll_score == 'x':
            rolls += 1
            total_score += strike_score(roll_scores, index)
        else:
            total_score += roll_score
        rolls += 1
    return total_score


def spare_score(roll_scores, index):
    return (10 - roll_scores[index - 1]) + frame_value(roll_scores[index + 1])


def strike_score(roll_scores, index):
    if roll_scores[index + 2] == '/':
        return 20
    strike_score = 10 + \
        frame_value(roll_scores[index + 1]) + \
        frame_value(roll_scores[index + 2])
    return strike_score


def frame_value(roll_score):
    if roll_score == 'x':
        return 10
    else:
        return roll_score

# -------------------------------------------------------------
# these are test cases I used to develop my tally_score function.
# I could not properly set up unit testing on my home computer so
# I relied on old fashion testing.
# -------------------------------------------------------------
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 0
# [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] 20
# [1,'/',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] 29
# [1,'/',1,'/',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] 38
# ['x',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] 30
# [1,'/','x',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] 48
# ['x','x','x',1,1,1,1,1,1,1,1,1,1,1,1,1,1] 77
# [1,'/',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 10
# ['x','x','x','x','x','x','x','x','x','x','x','x'] 300
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'/',5] 15
# ['x','x','x','x','x','x','x','x','x','x',9,'/'] 289
# ['x','x','x','x','x','x',0,0,0,0,0,0,0,0] 150


def main():
    scorecard = BowlingScorecard()
    scores = scorecard.player_roll_scores
    finalscore = tally_score(scores)
    print(f"Your final score was: {finalscore}")


if __name__ == "__main__":
    main()