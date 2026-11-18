import random
import streamlit as st

st.set_page_config(page_title="Battleship 8x8", layout="wide")

SHIP_NAMES = ["Battleship", "Cruiser", "Submarine", "Destroyer"]
SHIP_LENGTHS = [4, 3, 3, 2]
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]


def can_place_ship(ship, occupied):
    for row, col in ship:
        for r in range(max(0, row - 1), min(8, row + 2)):
            for c in range(max(0, col - 1), min(8, col + 2)):
                if (r, c) in occupied:
                    return False
    return True


def generate_fleet():
    fleet = []

    for ship_length in SHIP_LENGTHS:
        placed = False

        while not placed:
            orientation = random.choice(["Horizontal", "Vertical"])
            row = random.randint(0, 7)
            col = random.randint(0, 7)

            if orientation == "Horizontal":
                if col + ship_length > 8:
                    continue
                ship = [(row, col + i) for i in range(ship_length)]
            else:
                if row + ship_length > 8:
                    continue
                ship = [(row + i, col) for i in range(ship_length)]

            if can_place_ship(ship, fleet):
                fleet.extend(ship)
                placed = True

    return fleet


def reset_game():
    st.session_state.player_ships = []
    st.session_state.enemy_ships = generate_fleet()
    st.session_state.player_shots = {}
    st.session_state.computer_shots = {}
    st.session_state.ship_index = 0
    st.session_state.available_shots = [
        (row, col) for row in range(8) for col in range(8)
    ]
    st.session_state.game_over = False


if "player_ships" not in st.session_state:
    reset_game()

if "enemy_ships" not in st.session_state:
    st.session_state.enemy_ships = generate_fleet()

if "player_shots" not in st.session_state:
    st.session_state.player_shots = {}

if "computer_shots" not in st.session_state:
    st.session_state.computer_shots = {}

if "ship_index" not in st.session_state:
    st.session_state.ship_index = 0

if "available_shots" not in st.session_state:
    st.session_state.available_shots = [
        (row, col) for row in range(8) for col in range(8)
    ]

if "game_over" not in st.session_state:
    st.session_state.game_over = False


if st.button("🔄 New Game"):
    reset_game()
    st.rerun()

st.title("🚢 Battleship Classic 8x8")
orientation = st.radio("Orientation", ["Horizontal", "Vertical"], key="orientation")

if st.session_state.ship_index < len(SHIP_NAMES):
    ship_name = SHIP_NAMES[st.session_state.ship_index]
    ship_length = SHIP_LENGTHS[st.session_state.ship_index]
    st.info(f"Place your {ship_name} ({ship_length} cells)")
else:
    st.success("✅ Fleet deployed. Battle started!")


enemy_hits = sum(
    1 for result in st.session_state.player_shots.values() if result == "hit"
)
player_hits = sum(
    1 for result in st.session_state.computer_shots.values() if result == "hit"
)

st.session_state.game_over = enemy_hits >= 12 or player_hits >= 12
st.write(f"Your hits: {enemy_hits}/12 | Computer hits: {player_hits}/12")

if enemy_hits == 12:
    st.balloons()
    st.success("🏆 Victory! You sank the enemy fleet!")

if player_hits == 12:
    st.error("💀 Defeat! The computer sank your fleet!")

left_board, right_board = st.columns(2)

with left_board:
    st.subheader("🚢 Your Fleet")

    header = st.columns(9)
    header[0].write("")
    for i, letter in enumerate(LETTERS):
        header[i + 1].write(f"**{letter}**")

    for row in range(8):
        cols = st.columns(9)
        cols[0].write(f"**{row + 1}**")

        for col in range(8):
            coord = (row, col)

            if coord in st.session_state.computer_shots:
                if coord in st.session_state.player_ships:
                    symbol = "💥" if st.session_state.computer_shots[coord] == "hit" else "🚢"
                else:
                    symbol = "❌"
            elif coord in st.session_state.player_ships:
                symbol = "🚢"
            else:
                symbol = "⬜"

            if cols[col + 1].button(
                symbol,
                key=f"player_{row}_{col}",
                disabled=(st.session_state.ship_index >= len(SHIP_NAMES) or st.session_state.game_over),
            ):
                if st.session_state.ship_index < len(SHIP_NAMES):
                    ship_length = SHIP_LENGTHS[st.session_state.ship_index]
                    if orientation == "Horizontal":
                        if col + ship_length > 8:
                            st.warning("This ship does not fit horizontally.")
                        else:
                            new_ship = [(row, col + i) for i in range(ship_length)]
                            if can_place_ship(new_ship, st.session_state.player_ships):
                                st.session_state.player_ships.extend(new_ship)
                                st.session_state.ship_index += 1
                                st.rerun()
                            else:
                                st.warning("Ship placement overlaps or touches another ship.")
                    else:
                        if row + ship_length > 8:
                            st.warning("This ship does not fit vertically.")
                        else:
                            new_ship = [(row + i, col) for i in range(ship_length)]
                            if can_place_ship(new_ship, st.session_state.player_ships):
                                st.session_state.player_ships.extend(new_ship)
                                st.session_state.ship_index += 1
                                st.rerun()
                            else:
                                st.warning("Ship placement overlaps or touches another ship.")

with right_board:
    st.subheader("🎯 Enemy Waters")

    header = st.columns(9)
    header[0].write("")
    for i, letter in enumerate(LETTERS):
        header[i + 1].write(f"**{letter}**")

    for row in range(8):
        cols = st.columns(9)
        cols[0].write(f"**{row + 1}**")

        for col in range(8):
            coord = (row, col)

            if coord in st.session_state.player_shots:
                symbol = "💥" if st.session_state.player_shots[coord] == "hit" else "❌"
            else:
                symbol = "⬜"

            if cols[col + 1].button(
                symbol,
                key=f"enemy_{row}_{col}",
                disabled=(st.session_state.ship_index < len(SHIP_NAMES) or st.session_state.game_over),
            ):
                if coord not in st.session_state.player_shots:
                    if coord in st.session_state.enemy_ships:
                        st.session_state.player_shots[coord] = "hit"
                    else:
                        st.session_state.player_shots[coord] = "miss"

                    if st.session_state.available_shots:
                        computer_target = random.choice(st.session_state.available_shots)
                        st.session_state.available_shots.remove(computer_target)
                        if computer_target in st.session_state.player_ships:
                            st.session_state.computer_shots[computer_target] = "hit"
                        else:
                            st.session_state.computer_shots[computer_target] = "miss"

                    st.rerun()
