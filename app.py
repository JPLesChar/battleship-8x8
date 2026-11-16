import streamlit as st

st.set_page_config(page_title="Battleship 8x8")

st.title("🚢 Battleship Classic 8x8")

for row in range(8):
    cols = st.columns(8)

    for col in range(8):
        cols[col].button("🌊", key=f"{row}_{col}")
