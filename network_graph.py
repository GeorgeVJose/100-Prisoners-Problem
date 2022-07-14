from math import ceil

import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

class Graph:
    def __init__(self, prisoner_numbers) -> list:
        self.G = nx.Graph()
        # self.G = nx.random_geometric_graph(100, 0.125)

        graph_dict = dict(
            zip(range(1, len(prisoner_numbers)+1), prisoner_numbers)
        )

        self.G.add_edges_from(graph_dict.items())

        self.connected_components = list(
            sorted(nx.connected_components(self.G), key=len, reverse=True))
        self.num_components = len(self.connected_components)
        
        self.subgraph_nodes_num = [len(c) for c in self.connected_components]


    def draw_graph(self):
        """
        Returns a list of plotly figures. Each figure is a graph of the connected components.
        """

        bar_plot = go.Figure()
        bar_plot.add_trace(
            go.Bar(
                x=self.subgraph_nodes_num[::-1],
                y=[f"Sequence: {n}" for n in range(1, self.num_components+1)],
                name="Subgraphs",
                orientation="h",
                text=self.subgraph_nodes_num[::-1],
                textposition="auto",
                # marker_color='rgb(158,202,225)',
                # marker_line_color='rgb(8,48,107)',
                marker_line_width=1.5,
                opacity=0.6,
            )
        )
        bar_plot.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
        bar_plot.update_yaxes(showgrid=False, zeroline=False, showticklabels=True)
        bar_plot.update_layout(
            width=500,
            height=800,
            margin=dict(l=0, r=0, b=0, t=0,),
        )

        fig = make_subplots(
            rows=ceil(self.num_components/2),
            cols=2,
            subplot_titles=[f"Sequence: {n}, Count: {c}" for n, c in zip(
                range(1, self.num_components+1), self.subgraph_nodes_num)],
            horizontal_spacing=0.1,
            vertical_spacing=0.1,
            print_grid=False,
        )

        for ix, component in enumerate(self.connected_components):
            subgraph = self.G.subgraph(component).copy()

            # Getting positions for each node
            pos = nx.circular_layout(subgraph, center=[ix, ix])
            for n, p in pos.items():
                subgraph.nodes[n]['pos'] = p

            # Plot Edges
            edge_x = []
            edge_y = []
            for edge in subgraph.edges():
                x0, y0 = subgraph.nodes[edge[0]]['pos']
                x1, y1 = subgraph.nodes[edge[1]]['pos']
                edge_x.append(x0)
                edge_x.append(x1)
                edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                edge_y.append(None)

            fig.add_trace(
                go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=0.5, color='#888'),
                    hoverinfo='none',
                    mode='lines'
                ),
                row=(ix//2)+1, col=(ix % 2)+1
            )

            # Plot Nodes
            node_x = []
            node_y = []
            for node in subgraph.nodes():
                x, y = subgraph.nodes[node]['pos']
                node_x.append(x)
                node_y.append(y)

            fig.add_trace(
                go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    # hovertext=list(subgraph.nodes()),
                    hoverinfo='none',
                    text=list(subgraph.nodes()),
                    textposition='middle center',
                    marker=dict(
                        symbol="circle",
                        size=20,
                        line=dict(
                            width=3,
                            color='MediumPurple'
                        ),
                        colorscale='ice',
                        opacity=0.5,
                        line_width=2
                    )
                ),
                row=(ix//2)+1, col=(ix % 2)+1
            )

        fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            width=1000,
            height=1000,
        )

        return fig, bar_plot
