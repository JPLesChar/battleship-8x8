import random
import streamlit as st

st.set_page_config(page_title="Battleship 8x8", layout="wide")

SHIP_NAMES = ["Battleship", "Cruiser", "Submarine", "Destroyer"]
SHIP_LENGTHS = [4, 3, 3, 2]
SHIP_ICONS = ["🛳️", "🚢", "⚓", "🚤"]
SHIP_COLORS = [
    ("#1e3a8a", "#93c5fd"),
    ("#0f766e", "#5eead4"),
    ("#7e22ce", "#d8b4fe"),
    ("#c2410c", "#fdba74"),
]
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]


def ship_index_at(coord, occupied):
    offset = 0
    for index, length in enumerate(SHIP_LENGTHS):
        if coord in occupied[offset : offset + length]:
            return index
        offset += length
    return None


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

ship_cell_styles = []
for coord in st.session_state.player_ships:
    ship_index = ship_index_at(coord, st.session_state.player_ships)
    row, col = coord
    fill, border = SHIP_COLORS[ship_index]
    ship_cell_styles.append(
        f"""
        .st-key-player_{row}_{col} button {{
            background: {fill} !important;
            border: 2px solid {border} !important;
            color: white !important;
        }}
        .st-key-player_{row}_{col} button:hover {{
            background: {fill} !important;
            border-color: white !important;
        }}
        """
    )

legend_items = "".join(
    f'<span><i style="background:{fill};border-color:{border}"></i>'
    f"{icon} {name}</span>"
    for name, icon, (fill, border) in zip(SHIP_NAMES, SHIP_ICONS, SHIP_COLORS)
)
st.markdown(
    f"""
    <style>
    div[class*="st-key-player_"] button,
    div[class*="st-key-enemy_"] button {{
        min-height: 3.6rem;
        padding: 0;
        font-size: 2rem;
        line-height: 1;
    }}
    .grid-label {{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 3.6rem;
        font-weight: 700;
    }}
    .fleet-legend {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin-bottom: 0.75rem;
    }}
    .fleet-legend span {{
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        font-weight: 600;
    }}
    .fleet-legend i {{
        width: 0.8rem;
        height: 0.8rem;
        border: 2px solid;
        border-radius: 0.2rem;
    }}
    @media (max-width: 640px) {{
        .stMainBlockContainer > [data-testid="stVerticalBlock"] {{
            gap: 0.5rem !important;
        }}
        .stTabs [data-testid="stTabPanel"] > [data-testid="stVerticalBlock"] {{
            gap: 0.1rem !important;
        }}
        .stTabs [data-testid="stTabPanel"] {{
            padding-top: 0.25rem !important;
        }}
        .stTabs [data-testid="stHorizontalBlock"] {{
            flex-wrap: nowrap !important;
            gap: 0.1rem !important;
        }}
        .stTabs [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
            flex: 1 1 0% !important;
            width: auto !important;
            min-width: 0 !important;
            max-width: none !important;
        }}
        .fleet-legend {{
            display: none;
        }}
        h1 {{
            font-size: 1.25rem !important;
            line-height: 1.2 !important;
            white-space: nowrap;
        }}
        div[class*="st-key-player_"] button,
        div[class*="st-key-enemy_"] button {{
            min-height: 1.25rem;
            font-size: 0.75rem;
        }}
        .grid-label {{
            height: 1.25rem;
        }}
    }}
    {"".join(ship_cell_styles)}
    </style>
    """,
    unsafe_allow_html=True,
)

if st.button("🔄 New Game"):
    reset_game()
    st.rerun()

st.title("🚢 Battleship Classic 8x8")
orientation = st.radio(
    "Orientation",
    ["Horizontal", "Vertical"],
    key="orientation",
    horizontal=True,
)

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

player_tab, enemy_tab = st.tabs(["🚢 Your Fleet", "🎯 Enemy Waters"])

with player_tab:
    st.markdown(
        f'<div class="fleet-legend">{legend_items}</div>',
        unsafe_allow_html=True,
    )
    header = st.columns(9)
    header[0].markdown('<div class="grid-label"></div>', unsafe_allow_html=True)
    for i, letter in enumerate(LETTERS):
        header[i + 1].markdown(
            f'<div class="grid-label">{letter}</div>',
            unsafe_allow_html=True,
        )

    for row in range(8):
        cols = st.columns(9)
        cols[0].markdown(
            f'<div class="grid-label">{row + 1}</div>',
            unsafe_allow_html=True,
        )

        for col in range(8):
            coord = (row, col)
            ship_index = ship_index_at(coord, st.session_state.player_ships)

            if coord in st.session_state.computer_shots:
                if coord in st.session_state.player_ships:
                    symbol = (
                        "💥"
                        if st.session_state.computer_shots[coord] == "hit"
                        else SHIP_ICONS[ship_index]
                    )
                else:
                    symbol = "❌"
            elif ship_index is not None:
                symbol = SHIP_ICONS[ship_index]
            else:
                symbol = "⬜"

            if cols[col + 1].button(
                symbol,
                key=f"player_{row}_{col}",
                disabled=(st.session_state.ship_index >= len(SHIP_NAMES) or st.session_state.game_over),
                use_container_width=True,
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

with enemy_tab:
    header = st.columns(9)
    header[0].markdown('<div class="grid-label"></div>', unsafe_allow_html=True)
    for i, letter in enumerate(LETTERS):
        header[i + 1].markdown(
            f'<div class="grid-label">{letter}</div>',
            unsafe_allow_html=True,
        )

    for row in range(8):
        cols = st.columns(9)
        cols[0].markdown(
            f'<div class="grid-label">{row + 1}</div>',
            unsafe_allow_html=True,
        )

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
                use_container_width=True,
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
