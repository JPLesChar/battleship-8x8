import streamlit as st
import random

st.set_page_config(
    page_title="Battleship 8x8",
    layout="wide"
)

# =====================================
# FUNCTIONS
# =====================================

def can_place_ship(ship, occupied):
    for row, col in ship:
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r, c) in occupied:
                    return False
    return True


def generate_enemy_fleet():
    ship_lengths = [4, 3, 3, 2]
    fleet = []

    for length in ship_lengths:

        placed = False

        while not placed:

            orientation = random.choice(
                ["Horizontal", "Vertical"]
            )

            row = random.randint(0, 7)
            col = random.randint(0, 7)

            if orientation == "Horizontal":

                if col + length > 8:
                    continue

                ship = [
                    (row, col + i)
                    for i in range(length)
                ]

            else:

                if row + length > 8:
                    continue

                ship = [
                    (row + i, col)
                    for i in range(length)
                ]

            if can_place_ship(ship, fleet):
                fleet.extend(ship)
                placed = True

    return fleet


# =====================================
# SESSION STATE
# =====================================

if "player_ships" not in st.session_state:
    st.session_state.player_ships = []

if "enemy_ships" not in st.session_state:
    st.session_state.enemy_ships = generate_enemy_fleet()

if "player_shots" not in st.session_state:
    st.session_state.player_shots = {}

if "ship_index" not in st.session_state:
    st.session_state.ship_index = 0

ships_to_place = [
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2)
]

letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

# =====================================
# NEW GAME
# =====================================

if st.button("🔄 New Game"):

    st.session_state.player_ships = []
    st.session_state.enemy_ships = generate_enemy_fleet()
    st.session_state.player_shots = {}
    st.session_state.ship_index = 0

    st.rerun()

# =====================================
# TITLE
# =====================================

st.title("🚢 Battleship Classic 8x8")

orientation = st.radio(
    "Orientation",
    ["Horizontal", "Vertical"]
)

# =====================================
# STATUS
# =====================================

if st.session_state.ship_index < len(ships_to_place):

    ship_name, ship_length = ships_to_place[
        st.session_state.ship_index
    ]

    st.info(
        f"Place your {ship_name} ({ship_length} cells)"
    )

else:

    st.success(
        "✅ Fleet deployed. Fire at will!"
    )

enemy_hits = sum(
    1
    for result in st.session_state.player_shots.values()
    if result == "hit"
)

st.write(
    f"Enemy ship cells destroyed: {enemy_hits}/12"
)

# =====================================
# BOARDS
# =====================================

left_board, right_board = st.columns(2)

# =====================================
# PLAYER BOARD
# =====================================

with left_board:

    st.subheader("🚢 Your Fleet")

    header = st.columns(9)

    header[0].write("")

    for i in range(8):
        header[i + 1].write(
            f"**{letters[i]}**"
        )

    for row in range(8):

        cols = st.columns(9)

        cols[0].write(f"**{row + 1}**")

        for col in range(8):

            coord = (row, col)

            if coord in st.session_state.player_ships:
                symbol = "🚢"
            else:
                symbol = "⬜"

            if cols[col + 1].button(
                symbol,
                key=f"player_{row}_{col}"
            ):

                if (
                    st.session_state.ship_index
                    < len(ships_to_place)
                ):

                    _, ship_length = ships_to_place[
                        st.session_state.ship_index
                    ]

                    if orientation == "Horizontal":

                        if col + ship_length > 8:
                            continue

                        new_ship = [
                            (row, col + i)
                            for i in range(ship_length)
                        ]

                    else:

                        if row + ship_length > 8:
                            continue

                        new_ship = [
                            (row + i, col)
                            for i in range(ship_length)
                        ]

                    if can_place_ship(
                        new_ship,
                        st.session_state.player_ships
                    ):

                        st.session_state.player_ships.extend(
                            new_ship
                        )

                        st.session_state.ship_index += 1

                        st.rerun()

# =====================================
# ENEMY BOARD
# =====================================

with right_board:

    st.subheader("🎯 Enemy Waters")

    header = st.columns(9)

    header[0].write("")

    for i in range(8):
        header[i + 1].write(
            f"**{letters[i]}**"
        )

    for row in range(8):

        cols = st.columns(9)

        cols[0].write(f"**{row + 1}**")

        for col in range(8):

            coord = (row, col)

            if coord in st.session_state.player_shots:

                if (
                    st.session_state.player_shots[coord]
                    == "hit"
                ):
                    symbol = "💥"
                else:
                    symbol = "❌"

            else:

                symbol = "⬜"

            if cols[col + 1].button(
                symbol,
                key=f"enemy_{row}_{col}"
            ):

                if (
                    st.session_state.ship_index
                    == len(ships_to_place)
                ):

                    if (
                        coord
                        not in st.session_state.player_shots
                    ):

                        if (
                            coord
                            in st.session_state.enemy_ships
                        ):

                            st.session_state.player_shots[
                                coord
                            ] = "hit"

                        else:

                            st.session_state.player_shots[
                                coord
                            ] = "miss"

                        st.rerun()

# =====================================
# VICTORY
# =====================================

enemy_hits = sum(
    1
    for result in st.session_state.player_shots.values()
    if result == "hit"
)

if enemy_hits == 12:

    st.balloons()

    st.success(
        "🏆 Congratulations! You sank the enemy fleet!"
    )