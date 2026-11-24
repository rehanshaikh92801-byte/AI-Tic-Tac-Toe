
import streamlit as st

st.set_page_config(
    page_title="AI Tic-Tac-Toe",
    page_icon="🎮",
    layout="centered"
)

st.title("🎮 AI-Based Tic-Tac-Toe")
st.write("Challenge an intelligent AI powered by the Minimax Algorithm.")

# Winning combinations
WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

# Check winner
def check_winner(board):
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return None

# Minimax algorithm
def minimax(board, is_maximizing):
    winner = check_winner(board)

    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if "" not in board:
        return 0

    if is_maximizing:
        best_score = -float("inf")

        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best_score = max(score, best_score)

        return best_score

    else:
        best_score = float("inf")

        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ""
                best_score = min(score, best_score)

        return best_score

# AI move
def ai_move(board):
    best_score = -float("inf")
    best_move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                best_move = i

    if best_move is not None:
        board[best_move] = "O"

# Initialize game data
if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "result_recorded" not in st.session_state:
    st.session_state.result_recorded = False

# Record game result only once
def finish_game():
    board = st.session_state.board
    winner = check_winner(board)

    if winner == "X":
        result = "Player Won"
    elif winner == "O":
        result = "AI Won"
    elif "" not in board:
        result = "Draw"
    else:
        return

    if not st.session_state.result_recorded:
        if result == "Player Won":
            st.session_state.player_score += 1
        elif result == "AI Won":
            st.session_state.ai_score += 1
        else:
            st.session_state.draw_score += 1

        st.session_state.history.append(result)
        st.session_state.result_recorded = True

    st.session_state.game_over = True

# Scoreboard
st.divider()
st.subheader("🏆 Scoreboard")

col1, col2, col3 = st.columns(3)

col1.metric("You (X)", st.session_state.player_score)
col2.metric("AI (O)", st.session_state.ai_score)
col3.metric("Draws", st.session_state.draw_score)

st.divider()

# Current game status
board = st.session_state.board
winner = check_winner(board)

if winner == "X":
    st.success("🎉 Congratulations! You won!")
elif winner == "O":
    st.error("🤖 AI wins! Better luck next time.")
elif "" not in board:
    st.info("🤝 Match Draw!")
else:
    st.info("Your turn! You are X.")

# Game board
st.subheader("🎮 Game Board")

for row in range(3):
    cols = st.columns(3)

    for col in range(3):
        index = row * 3 + col

        with cols[col]:
            if st.button(
                board[index] if board[index] else " ",
                key=f"cell_{index}",
                use_container_width=True,
                disabled=st.session_state.game_over or board[index] != ""
            ):
                board[index] = "X"

                if check_winner(board) is None and "" in board:
                    ai_move(board)

                finish_game()
                st.rerun()

# Restart current match
if st.button("🔄 New Game", use_container_width=True):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.result_recorded = False
    st.rerun()

# Game history
st.divider()
st.subheader("📜 Game History")

if st.session_state.history:
    for number, result in enumerate(
        reversed(st.session_state.history), start=1
    ):
        st.write(f"**Match {len(st.session_state.history) - number + 1}:** {result}")
else:
    st.write("No completed matches yet. Play your first game!")

# Reset all scores and history
if st.button("🗑️ Reset Scoreboard & History"):
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.draw_score = 0
    st.session_state.history = []
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.result_recorded = False
    st.rerun()

st.divider()
st.caption("AI Engine: Minimax Algorithm | Player: X | Computer: O")