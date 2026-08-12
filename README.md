# Lab 03 - Snake Game Trio Studio

## What are you building?

Your trio will turn four small Python contracts into a playable grid-based Snake Game. The Pygame window, keyboard adapter, drawing code, restart key, and deterministic food placement are supplied. Your job is deliberately smaller:

1. move the head exactly one grid cell;
2. detect when the head reaches the food;
3. detect four wall boundaries;
4. create the next body with or without growth;
5. design at least three additional tests;
6. preserve one real red-to-green debugging story; and
7. use GitHub branches, reviews, and commits to show how three people collaborated.

The core mission is complete when the public tests and trio tests are green, the Pygame game launches, one round can be played and restarted, evidence files are complete, and every member can explain one contract and one test.

## Why this Lab exists

Snake makes changing state visible. Each step has a current head, direction, body, food cell, and next state. The game is small enough to finish, but it still requires professional habits: contract before code, test before confidence, inspect before repair, and review before merge.

## Trio roles

- **Driver:** types only what the trio has agreed.
- **Navigator:** reads the contract, predicts the next behavior, and keeps the edit small.
- **Tester / Recorder:** writes expected observations, runs commands, updates evidence, and records L1 AI use.

Rotate after every completed TODO. Complete `GROUP_CONTRACT.md` before editing Python. The student pack also includes `Snake_Trio_Working_Contract.html` for phones and `Snake_Trio_Working_Contract.pdf` as a one-page landscape print sheet.

## L1 AI policy

L1 is allowed for the entire studio. AI may explain a Python concept, ask a guiding question, suggest a counterexample or test idea, and help read a traceback. AI may not provide the final four function bodies, silently write the submitted tests, impersonate a member, or invent command output. Record every use in `AI_USE.md`.

## GitHub collaboration contract

One member creates a **private** GitHub repository and invites the other two. Every member clones the same repository. Work through short branches and Pull Requests:

```bash
git pull --ff-only
git switch -c todo-1-next-head
# edit, run one focused test, then:
git add src/snake_trio/logic.py evidence/TRIO_LOG.md
git diff --staged
git commit -m "Implement one-cell head movement"
git push -u origin todo-1-next-head
```

Open a Pull Request. A different member reviews the contract, diff, and test result before merge. Each member must author at least one Pull Request and review at least one Pull Request. Pull `main` before starting the next branch. Do not share passwords or personal access tokens.

## Setup and expected-red baseline

From the extracted `lab03-snake-trio/` root:

```bash
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\Activate.ps1      # Windows PowerShell
python -m pip install -e '.[test,display]'
python -m pytest tests_public -q
```

Before implementation, one infrastructure test passes and the four function-contract tests fail with `NotImplementedError`. Import or collection errors are not expected. The student test scaffold is intentionally incomplete; replace it rather than treating it as a product defect.

## Step-by-step core route

### Step 1 - Write the working contract

Complete `GROUP_CONTRACT.md`. Confirm the private repository, roles, response rule, AI boundary, review rule, and help threshold.

### Step 2 - Write four function contracts

Complete `evidence/FUNCTION_CONTRACTS.md`. For every function, state accepted input, returned result, invariant, and at least one boundary example.

### Step 3 - TODO 1: move one cell

Implement `next_head`. Run only its focused public test first. Open and review the first Pull Request, then rotate roles.

### Step 4 - TODO 2: recognize food

Implement `ate_food` as an exact cell comparison. Test both equal and unequal cells. Open and review the second Pull Request, then rotate roles.

### Step 5 - TODO 3: stop at a wall

Implement `hit_wall`. Test the four legal/illegal boundary pairs. Open and review the third Pull Request, then rotate roles.

### Step 6 - TODO 4: move or grow the body

Implement `advance_body` without mutating the supplied list. Test normal movement, growth, and input preservation. Open and review the fourth Pull Request.

### Step 7 - Design trio tests

Replace the scaffold in `tests/test_snake_student.py` with at least three meaningful tests. Each member authors or explains at least one. Do not copy the public tests word for word.

### Step 8 - Debug one real failure

Choose one genuine failing test. Fill `evidence/DEBUG_LOG.md` while it is still red: observed fact, contract expectation, smallest hypothesis, smallest change, focused rerun, then full regression.

### Step 9 - Play the game

```bash
python -m pytest tests_public tests -q
python -m snake_trio --check
python -m snake_trio
```

Use arrow keys or WASD. Press `R` after game over. Do not add features until the core round is playable and tests are green.

### Step 10 - Final GitHub gate

Confirm that every member authored and reviewed work, Actions is green, the evidence files are committed, and the tree is clean:

```bash
git status --short
git log --oneline --decorate -8
```

Submit the private repository URL, final commit hash, three Pull Request URLs, and the four evidence files through Moodle.

## Stop and ask for help when

- Python is not 3.11-3.13 or installation fails;
- GitHub access or invitation fails;
- tests cannot be collected;
- the failure is outside the function currently being edited;
- your trio has spent 15 focused minutes without a new observed fact; or
- AI suggests a complete function body or a change your trio cannot explain.

## Further learning

- Python functions: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Python lists: https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
- pytest getting started: https://docs.pytest.org/en/stable/getting-started.html
- GitHub branch workflow: https://docs.github.com/en/get-started/using-github/github-flow
- GitHub Pull Request reviews: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests
- Pygame beginner tutorials: https://pyga.me/docs/tutorials/en/index.html
