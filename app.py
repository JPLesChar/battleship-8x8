import streamlit as st

st.set_page_config(page_title="Battleship 8x8")

st.title("🚢 Battleship Classic 8x8")

# Hidden ship
ship = [(2, 3), (2, 4), (2, 5)]

if "shots" not in st.session_state:
    st.session_state.shots = {}

for row in range(8):
    cols = st.columns(8)

    for col in range(8):

        coord = (row, col)

        if coord in st.session_state.shots:

            if st.session_state.shots[coord] == "hit":
                label = "💥"
            else:
                label = "❌"

        else:
            label = "🌊"

        if cols[col].button(label, key=f"{row}_{col}"):

            if coord not in st.session_state.shots:

                if coord in ship:
                    st.session_state.shots[coord] = "hit"
                else:
                    st.session_state.shots[coord] = "miss"

                st.rerun()
hits = sum(
    1 for pos in ship
    if st.session_state.shots.get(pos) == "hit"
)

if hits == len(ship):
    st.success("🎉 You sunk the ship!")