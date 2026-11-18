import random

import streamlit as st

st.set_page_config(page_title="Battleship | 8×8", page_icon="⚓", layout="wide")

BOARD_SIZE = 8
SHIP_NAMES = ["Battleship", "Cruiser", "Submarine", "Destroyer"]
SHIP_LENGTHS = [4, 3, 3, 2]
SHIP_ICONS = {
    "Battleship": "🛳️",
    "Cruiser": "🚢",
    "Submarine": "🐬",
    "Destroyer": "🚤",
}
SHIP_COLORS = {
    "Battleship": "#8ec5ff",
    "Cruiser": "#66d9c2",
    "Submarine": "#c2a5ff",
    "Destroyer": "#ffd166",
}
LETTERS = list("ABCDEFGH")

st.markdown(
    """
    <style>
      :root { color-scheme: dark; }
      .stApp {
        background: radial-gradient(ellipse at 50% -20%, #164b70 0%, #0a2740 42%, #061727 100%);
        color: #e8f4ff;
      }
      [data-testid="stHeader"] { background: transparent; }
      .block-container { max-width: 1500px; padding-top: 2rem; padding-bottom: 3rem; }
      h1, h2, h3 { color: #f3f9ff !important; letter-spacing: -0.02em; }
      .hero-kicker { color: #65d9df; font-size: .78rem; font-weight: 800; letter-spacing: .2em; text-transform: uppercase; }
      .hero-copy { color: #a9c5d9; margin-top: -.5rem; }
      [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(133, 195, 228, .2);
        border-radius: 18px;
        background: rgba(8, 31, 51, .72);
        box-shadow: 0 16px 40px rgba(0, 0, 0, .18);
      }
      [data-testid="stMetric"] { background: rgba(22, 61, 89, .58); padding: 12px 16px; border-radius: 14px; }
      [data-testid="stMetricLabel"] { color: #a9c5d9 !important; }
      [data-testid="stMetricValue"] { color: #f3f9ff !important; }
      [data-testid="stRadio"] label { color: #d7e9f6; }
      .stButton button {
        min-height: 3.15rem;
        width: 100%;
        border: 1px solid rgba(120, 194, 232, .24);
        border-radius: 9px;
        background: linear-gradient(145deg, #12436a, #0b3153);
        color: #b7e5ff;
        font-size: 1.18rem;
        font-weight: 700;
        transition: .15s ease;
      }
      .stButton button:hover:not(:disabled) {
        border-color: #57dce5;
        background: linear-gradient(145deg, #17618a, #10476e);
        color: white;
        transform: translateY(-1px);
      }
      .stButton button:disabled { opacity: .9; color: #b7e5ff; }
      [data-testid^="st-key-player_"] button,
      [data-testid^="st-key-enemy_"] button { padding: 0; }
      [data-testid="stMarkdownContainer"] p { color: #c4d9e8; }
      @media (max-width: 800px) {
        .block-container { padding: 1rem .7rem 2rem; }
        .stButton button { min-height: 2.45rem; font-size: .95rem; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def can_place_ship(ship, occupied):
    """Keep a one-cell buffer between ships, including diagonally."""
    for row, col in ship:
        for r in range(max(0, row - 1), min(BOARD_SIZE, row + 2)):
            for c in range(max(0, col - 1), min(BOARD_SIZE, col + 2)):
                if (r, c) in occupied:
                    return False
    return True


def generate_fleet():
    fleet = []
    for ship_length in SHIP_LENGTHS:
        while True:
            orientation = random.choice(["Horizontal", "Vertical"])
            row, col = random.randrange(BOARD_SIZE), random.randrange(BOARD_SIZE)
            if orientation == "Horizontal":
                if col + ship_length > BOARD_SIZE:
                    continue
                ship = [(row, col + i) for i in range(ship_length)]
            else:
                if row + ship_length > BOARD_SIZE:
                    continue
                ship = [(row + i, col) for i in range(ship_length)]
            if can_place_ship(ship, fleet):
                fleet.extend(ship)
                break
    return fleet


def reset_game():
    st.session_state.player_ships = []
    st.session_state.player_ship_types = {}
    st.session_state.enemy_ships = generate_fleet()
    st.session_state.player_shots = {}
    st.session_state.computer_shots = {}
    st.session_state.ship_index = 0
    st.session_state.available_shots = [
        (row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)
    ]
    st.session_state.game_over = False


def initialize_game():
    if "player_ships" not in st.session_state:
        reset_game()
    else:
        defaults = {
            "player_ship_types": {},
            "enemy_ships": generate_fleet(),
            "player_shots": {},
            "computer_shots": {},
            "ship_index": 0,
            "available_shots": [
                (r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)
            ],
            "game_over": False,
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value


def ship_cells(row, col, length, orientation):
    if orientation == "Horizontal":
        return [(row, col + i) for i in range(length)]
    return [(row + i, col) for i in range(length)]


def add_cell_styles():
    rules = []
    for coord, ship_name in st.session_state.player_ship_types.items():
        row, col = coord
        rules.append(
            f'[data-testid="st-key-player_{row}_{col}"] button '
            f'{{ background: linear-gradient(145deg, #174b70, #102f4b); '
            f'border-color: {SHIP_COLORS[ship_name]}; color: {SHIP_COLORS[ship_name]}; }}'
        )
    for (row, col), result in st.session_state.computer_shots.items():
        color = "#ff796f" if result == "hit" else "#7093a9"
        rules.append(
            f'[data-testid="st-key-player_{row}_{col}"] button '
            f'{{ background: #10283d; border-color: {color}; color: {color}; }}'
        )
    for (row, col), result in st.session_state.player_shots.items():
        color = "#ff796f" if result == "hit" else "#7093a9"
        rules.append(
            f'[data-testid="st-key-enemy_{row}_{col}"] button '
            f'{{ background: #10283d; border-color: {color}; color: {color}; }}'
        )
    if rules:
        st.markdown("<style>" + "\n".join(rules) + "</style>", unsafe_allow_html=True)


def render_board_header():
    header = st.columns([0.55] + [1] * BOARD_SIZE, gap="small")
    for index, letter in enumerate(LETTERS):
        header[index + 1].markdown(
            f'<div style="text-align:center;color:#82b4d2;font-weight:800;padding:.25rem 0">{letter}</div>',
            unsafe_allow_html=True,
        )


def place_player_ship(row, col, orientation):
    ship_index = st.session_state.ship_index
    name = SHIP_NAMES[ship_index]
    length = SHIP_LENGTHS[ship_index]
    if (orientation == "Horizontal" and col + length > BOARD_SIZE) or (
        orientation == "Vertical" and row + length > BOARD_SIZE
    ):
        st.warning(f"That {name.lower()} does not fit {orientation.lower()} here.")
        return

    ship = ship_cells(row, col, length, orientation)
    if not can_place_ship(ship, st.session_state.player_ships):
        st.warning("Ships can’t overlap or touch—even diagonally. Choose another spot.")
        return

    st.session_state.player_ships.extend(ship)
    for coord in ship:
        st.session_state.player_ship_types[coord] = name
    st.session_state.ship_index += 1
    st.rerun()


def fire_at_enemy(coord):
    if coord in st.session_state.player_shots:
        return
    st.session_state.player_shots[coord] = (
        "hit" if coord in st.session_state.enemy_ships else "miss"
    )

    if st.session_state.available_shots:
        target = random.choice(st.session_state.available_shots)
        st.session_state.available_shots.remove(target)
        st.session_state.computer_shots[target] = (
            "hit" if target in st.session_state.player_ships else "miss"
        )
    st.rerun()


def render_player_board(orientation):
    render_board_header()
    for row in range(BOARD_SIZE):
        cells = st.columns([0.55] + [1] * BOARD_SIZE, gap="small")
        cells[0].markdown(
            f'<div style="text-align:center;color:#82b4d2;font-weight:800;padding:.85rem 0">{row + 1}</div>',
            unsafe_allow_html=True,
        )
        for col in range(BOARD_SIZE):
            coord = (row, col)
            ship_name = st.session_state.player_ship_types.get(coord)
            if coord in st.session_state.computer_shots:
                label = "💥" if st.session_state.computer_shots[coord] == "hit" else "·"
            elif ship_name:
                label = SHIP_ICONS[ship_name]
            else:
                label = "〰"

            if cells[col + 1].button(
                label,
                key=f"player_{row}_{col}",
                disabled=(st.session_state.ship_index >= len(SHIP_NAMES) or st.session_state.game_over),
                help=(f"{ship_name} at {LETTERS[col]}{row + 1}" if ship_name else None),
            ):
                if st.session_state.ship_index < len(SHIP_NAMES):
                    place_player_ship(row, col, orientation)


def render_enemy_board():
    render_board_header()
    for row in range(BOARD_SIZE):
        cells = st.columns([0.55] + [1] * BOARD_SIZE, gap="small")
        cells[0].markdown(
            f'<div style="text-align:center;color:#82b4d2;font-weight:800;padding:.85rem 0">{row + 1}</div>',
            unsafe_allow_html=True,
        )
        for col in range(BOARD_SIZE):
            coord = (row, col)
            result = st.session_state.player_shots.get(coord)
            label = "💥" if result == "hit" else ("·" if result == "miss" else "〰")
            if cells[col + 1].button(
                label,
                key=f"enemy_{row}_{col}",
                disabled=(st.session_state.ship_index < len(SHIP_NAMES) or st.session_state.game_over),
                help=f"Fire at {LETTERS[col]}{row + 1}" if result is None else f"Already fired at {LETTERS[col]}{row + 1}",
            ):
                fire_at_enemy(coord)


initialize_game()
if st.button("↻  New game", type="secondary"):
    reset_game()
    st.rerun()

st.markdown('<div class="hero-kicker">NORTH ATLANTIC · COMMAND DECK</div>', unsafe_allow_html=True)
st.title("⚓ Battleship")
st.markdown('<p class="hero-copy">A classic fleet duel. Deploy your ships, then find the enemy before they find you.</p>', unsafe_allow_html=True)

placement_phase = st.session_state.ship_index < len(SHIP_NAMES)
if placement_phase:
    next_name = SHIP_NAMES[st.session_state.ship_index]
    next_length = SHIP_LENGTHS[st.session_state.ship_index]
    st.info(f"📍 Deploy your **{next_name}** ({next_length} cells). Select a direction, then choose its starting square on your board.")
else:
    st.success("✅ Fleet deployed — choose a square in Enemy Waters to fire.")

enemy_hits = sum(result == "hit" for result in st.session_state.player_shots.values())
player_hits = sum(result == "hit" for result in st.session_state.computer_shots.values())
st.session_state.game_over = enemy_hits >= sum(SHIP_LENGTHS) or player_hits >= sum(SHIP_LENGTHS)

stats = st.columns(3)
st.title if False else None
stats[0].metric("Enemy fleet hits", f"{enemy_hits} / {sum(SHIP_LENGTHS)}")
stats[1].metric("Hits on your fleet", f"{player_hits} / {sum(SHIP_LENGTHS)}")
stats[2].metric("Ships deployed", f"{st.session_state.ship_index} / {len(SHIP_NAMES)}")

if enemy_hits >= sum(SHIP_LENGTHS):
    st.balloons()
    st.success("🏆 Victory! You sank the enemy fleet!")
elif player_hits >= sum(SHIP_LENGTHS):
    st.error("💀 Defeat — the computer sank your fleet.")

orientation = st.radio(
    "Ship direction",
    ["Horizontal", "Vertical"],
    horizontal=True,
    key="orientation",
    disabled=not placement_phase,
)

add_cell_styles()
left_board, right_board = st.columns(2, gap="large")
with left_board:
    with st.container(border=True):
        st.subheader("🚢 Your fleet")
        st.caption("Your ships are shown in distinct colors and icons.")
        render_player_board(orientation)
with right_board:
    with st.container(border=True):
        st.subheader("🎯 Enemy waters")
        st.caption("Dark blue squares are unexplored water · 💥 hit · · miss")
        render_enemy_board()

with st.container(border=True):
    st.markdown("**Fleet roster**")
    roster = st.columns(len(SHIP_NAMES))
    for index, (name, length) in enumerate(zip(SHIP_NAMES, SHIP_LENGTHS)):
        deployed = index < st.session_state.ship_index
        roster[index].markdown(
            f"{SHIP_ICONS[name]} **{name}**  \n{'Deployed' if deployed else f'{length} cells'}"
        )
