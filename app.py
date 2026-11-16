import streamlit as st

st.set_page_config(
    page_title="Battleship 8x8",
    layout="wide"
)

st.title("🚢 Battleship Classic 8x8")

# Initialize session state
if "player_ships" not in st.session_state:
    st.session_state.player_ships = []

# Reset button
if st.button("🔄 New Deployment"):
    st.session_state.player_ships = []
    st.rerun()

st.write(f"Ships placed: {len(st.session_state.player_ships)}/12")

left_board, right_board = st.columns(2)

# -------------------------
# PLAYER BOARD
# -------------------------
with left_board:

    st.subheader("🚢 Your Fleet")

    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    header = st.columns(9)
    header[0].write("")

    for i in range(8):
        header[i + 1].write(f"**{letters[i]}**")

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
                    coord not in st.session_state.player_ships
                    and len(st.session_state.player_ships) < 12
                ):
                    st.session_state.player_ships.append(coord)
                    st.rerun()

# -------------------------
# ENEMY BOARD
# -------------------------
with right_board:

    st.subheader("🎯 Enemy Waters")

    header = st.columns(9)
    header[0].write("")

    for i in range(8):
        header[i + 1].write(f"**{letters[i]}**")

    for row in range(8):

        cols = st.columns(9)

        cols[0].write(f"**{row + 1}**")

        for col in range(8):

            cols[col + 1].button(
                "⬜",
                key=f"enemy_{row}_{col}"
            )

if len(st.session_state.player_ships) == 12:
    st.success("✅ Fleet deployment complete!")