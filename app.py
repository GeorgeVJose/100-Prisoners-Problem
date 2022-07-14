import streamlit as st

from network_graph import Graph
from plots import grid_boxes, nodes_histogram

st.set_page_config(
    layout="wide"
)

# Sidebar tools
st.sidebar.title("100 Prisoners Problem")
st.sidebar.markdown("---")
st.sidebar.button("Shuffle numbers")


st.markdown("<h1 style='text-align: center'>100 Prisoners Problem</h1>",unsafe_allow_html=True)

st.write("The 100 prisoners problem is a mathematical problem in probability theory and combinatorics. \
         At first glance, the situation appears hopeless, but a clever strategy offers the prisoners a realistic chance of survival.")
st.markdown("---")


st.markdown("<h2 style='text-align: center'>The Problem</h2>",unsafe_allow_html=True)


desc_img, desc_text = st.columns(2)
with desc_img:
    st.markdown('''
    * The director of a prison offers 100 death row prisoners, who are numbered from 1 to 100, a last chance. A room contains a cupboard with 100 drawers.
    * The director randomly puts one prisoner's number in each closed drawer. The prisoners enter the room, one after another.
    * Each prisoner may open and look into 50 drawers in any order. The drawers are closed again afterwards.
    * If, during this search, every prisoner finds his number in one of the drawers, all prisoners are pardoned.
    * If just one prisoner does not find his number, all prisoners die.
    * Before the first prisoner enters the room, the prisoners may discuss strategy — but may not communicate once the first prisoner enters to look in the drawers.
    ''')

with desc_text:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/100_prisoners_problem_qtl1.svg/330px-100_prisoners_problem_qtl1.svg.png", width=450)

st.markdown("<br></br>", unsafe_allow_html=True)
st.markdown(
    "If every prisoner selects 50 drawers at random, the probability that a single prisoner finds his number is **50%.**\n \
     Therefore the probability that all prisoners are pardoned is :",
)
st.latex(
    r"P(survival) = (\frac{1}{2})^{100} ≈ 0.0000000000000000000000000000008")

st.markdown("<br></br>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center'>Drawers</h3>",unsafe_allow_html=True)
st.write("Hover over the drawers to see the numbers.")
prisoner_numbers, grid_box = grid_boxes()
st.plotly_chart(grid_box, config={"displayModeBar": False}, use_container_width=True)

st.markdown("---")
st.markdown("<h2 style='text-align: center'>The Solution</h2>",unsafe_allow_html=True)

st.markdown('''
    * Each prisoner first opens the drawer labeled with his own number.
    * If this drawer contains his number, he is done and was successful.
    * Otherwise, the drawer contains the number of another prisoner, and he next opens the drawer labeled with this number.
    * The prisoner repeats steps 2 and 3 until he finds his own number or has opened fifty drawers.
    By starting with his own number, the prisoner guarantees he is on a sequence of drawers containing his number.
    The only question is whether this sequence is longer than fifty drawers.
'''
            )

graph = Graph(prisoner_numbers)
graph_plot, bar_plot = graph.draw_graph()

if "subgraph_nodes_num" not in st.session_state:
    st.session_state["subgraph_nodes_num"] = graph.subgraph_nodes_num
else:
    st.session_state["subgraph_nodes_num"] += graph.subgraph_nodes_num

network_col, barplot_col = st.columns([2, 1])
with network_col:
    st.markdown("<h3 style='text-align: center'>Network Graph</h3>",unsafe_allow_html=True)
    st.plotly_chart(graph_plot, config={
                    "displayModeBar": False}, use_container_width=True)
with barplot_col:
    st.markdown("<h3 style='text-align: center'>Component node count</h3>",unsafe_allow_html=True)
    st.plotly_chart(bar_plot, config={
                    "displayModeBar": False}, use_container_width=True)

st.markdown("---")
st.markdown("<h2 style='text-align: center'>Overall Statistics</h2>",unsafe_allow_html=True)

st.plotly_chart(
    nodes_histogram(st.session_state["subgraph_nodes_num"]),
    config={"displayModeBar": False},
    use_container_width=True
)
