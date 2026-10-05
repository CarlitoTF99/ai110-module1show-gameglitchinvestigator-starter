# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |Suspected Code location
|-------|-------------------|-----------------|------------------------|-------
|Guess of 1 (secret 21); also guess of 100 (secret lower) | "Go HIGHER!" when guess is too low, "Go LOWER!" when too high  | Hints are reversed in both cases |none| app.py, check_guess() | |
|Won (or lost) a game on Easy, then clicked "New Game" |A fresh game starts: status back to playing, history and score cleared, secret picked from the current difficulty's range (1-20 on Easy) |Still shows "You already won. Start a new game to play again." and guesses are blocked. Only attempts and the secret reset, and the new secret could be anything from 1-100 even on Easy |none |app.py lines 134-136, the `if new_game:` block never resets `status` (so `st.stop()` runs every time) and uses `random.randint(1, 100)` instead of the difficulty range
|select "Hard" difficulty|ranger is larger than normal|range is 1-50 smaller than normal | none|app.py get_range_for_difficulty,
|Secret 50, guessed 9 on the 2nd attempt |"Go HIGHER!" because 9 < 50 |Said the guess was too high. On even attempts the secret was turned into a string, so "9" > "50" was compared alphabetically |none |app.py lines 158-161, `if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)`

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude
  - I used Claude Code inside VS Code for pretty much the whole project. I mostly used it to look through app.py with me, explain why something was acting weird, and help me write the pytest tests. I'd still run the game myself to check if what it said actually matched what I was seeing.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - When I told Claude the hints were backwards, it pointed out that in check_guess() the messages were just swapped, so a guess that was too high was returning "Go HIGHER!" and a guess that was too low was returning "Go LOWER!". It suggested flipping the two messages and moving check_guess() into logic_utils.py so it could be tested. I checked it by running the game again with the debug info open: the secret was 21, I guessed 1 and this time it told me to go higher, which is right. I also ran pytest and the tests for too high and too low passed.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  - The starter code was written by an AI, and one of the "fixes" it had in check_guess() was a try/except TypeError that turned the guess into a string whenever comparing it to the secret failed. I didn't keep that, because it just hid the real problem. On every even attempt the app was turning the secret into a string, and then "9" > "50" comes out as true since strings get compared letter by letter, so a guess of 9 was called too high. So instead I removed the line that turned the secret into a string and got rid of the try/except, so now it's always comparing numbers. To check my version I added tests like check_guess(9, 50) should be "Too Low" and check_guess(10, 9) should be "Too High", and they all passed.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
