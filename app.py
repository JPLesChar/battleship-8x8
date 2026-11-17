import streamlit as st

st.set_page_config(
    page_title="Battleship 2.0",
    layout="wide"
)

st.title("⚓ Battleship 2.0")

board = [
    ["🌊","🌊","🌊","🌊","🌊","🌊","🌊","🌊"],
    ["🌊","🛳️","🛳️","🛳️","🛳️","🌊","🌊","🌊"],
    ["🌊","🌊","🌊","🌊","🌊","🌊","🌊","🌊"],
    ["🌊","⛴️","⛴️","⛴️","🌊","🌊","🌊","🌊"],
    ["🌊","🌊","🌊","🌊","🌊","🌊","🌊","🌊"],
    ["🌊","🚤","🚤","🚤","🌊","🌊","🌊","🌊"],
    ["🌊","🌊","🌊","🌊","🌊","🌊","🌊","🌊"],
    ["🌊","🛶","🛶","🌊","🌊","🌊","🌊","🌊"]
]

st.markdown("""
<style>

.board {
    display:grid;
    grid-template-columns: repeat(8, 60px);
    gap:2px;
    background:#0b3b60;
    padding:10px;
    border-radius:12px;
    width:max-content;
}

.cell {
    width:60px;
    height:60px;
    background:#1e88e5;
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:32px;
    border-radius:6px;
}

.titlebox {
    background:#0b3b60;
    color:white;
    padding:10px;
    border-radius:10px;
    margin-bottom:10px;
    text-align:center;
    font-weight:bold;
    font-size:22px;
}

</style>
""", unsafe_allow_html=True)

left, right = st.columns(2)

with left:

    st.markdown(
        '<div class="titlebox">🚢 Your Fleet</div>',
        unsafe_allow_html=True
    )

    html = '<div class="board">'

    for row in board:
        for cell in row:
            html += (
                f'<div class="cell">{cell}</div>'
            )

    html += '</div>'

    st.markdown(
        html,
        unsafe_allow_html=True
    )

with right:

    st.markdown(
        '<div class="titlebox">🎯 Enemy Waters</div>',
        unsafe_allow_html=True
    )

    html = '<div class="board">'

    for row in range(8):
        for col in range(8):
            html += (
                '<div class="cell">🌊</div>'
            )

    html += '</div>'

    st.markdown(
        html,
        unsafe_allow_html=True
    )

st.info(
    "Prototype UI for Battleship 2.0"
)