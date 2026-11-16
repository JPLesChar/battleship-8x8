import streamlit as st

st.set_page_config(page_title="Battleship 8x8")

st.title("🚢 Battleship Classic 8x8")

if "player_ships" not in st.session_state:
    st.session_state.player_ships = []

left_board, right_board = st.columns(2)

with left_board:
    st.subheader("Your Fleet")

    st.write(f"Ships placed: {len(st.session_state.player_ships)}/12")

    for row in range(8):
        cols = st.columns(8)

        for col in range(8):

            coord = (row, col)

            if coord in st.session_state.player_ships:
                symbol = "🚢"
            else:
                symbol = "🌊"

            if cols[col].button(symbol, key=f"player_{row}_{col}"):

                if (
                    coord not in st.session_state.player_ships
                    and len(st.session_state.player_ships) < 12
                ):
                    st.session_state.player_ships.append(coord)
                    st.rerun()

with right_board:
    st.subheader("Enemy Waters")

    for row in range(8):
        cols = st.columns(8)

        for col in range(8):
            cols[col].button("🌊", key=f"enemy_{row}_{col}")

if len(st.session_state.player_ships) == 12:
    st.success("✅ Fleet deployment complete!")
