from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# Hint bug: the messages were swapped, so a high guess said "Go HIGHER!"
def test_too_high_guess_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_guess_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

# Hint bug: the secret was turned into a string on even attempts, so
# "9" > "50" compared alphabetically and 9 was reported as too high.
def test_single_digit_guess_below_two_digit_secret_is_too_low():
    outcome, message = check_guess(9, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_two_digit_guess_above_single_digit_secret_is_too_high():
    outcome, message = check_guess(10, 9)
    assert outcome == "Too High"
    assert "LOWER" in message

# Difficulty bug: Normal and Hard ranges were swapped, so Hard (1-50)
# was easier than Normal (1-100).
from logic_utils import get_range_for_difficulty

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)

def test_harder_difficulty_has_larger_range():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high

# New Game bug: the button never reset status, so after a win or loss the
# app hit st.stop() forever. It also always drew the secret from 1-100.
from logic_utils import new_game_state

def test_new_game_resets_status_after_finished_game():
    for finished in ("won", "lost"):
        state = {"status": finished, "attempts": 5, "score": 40, "history": [3, 7]}
        state.update(new_game_state(1, 20))
        assert state["status"] == "playing"
        assert state["attempts"] == 0
        assert state["score"] == 0
        assert state["history"] == []

def test_new_game_secret_respects_difficulty_range():
    low, high = get_range_for_difficulty("Easy")
    for _ in range(200):
        secret = new_game_state(low, high)["secret"]
        assert low <= secret <= high
