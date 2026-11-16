import streamlit as st

st.set_page_config(page_title="Battleship 8x8")

st.title("🚢 Battleship Classic 8x8")

left_board, right_board = st.columns(2)

with left_board:
    st.subheader("Your Fleet")

    for row in range(8):
        cols = st.columns(8)

        for col in range(8):
            cols[col].button("🌊", key=f"player_{row}_{col}")

with right_board:
    st.subheader("Enemy Waters")

    for row in range(8):
        cols = st.columns(8)

        for col in range(8):
            cols[col].button("🌊", key=f"enemy_{row}_{col}")