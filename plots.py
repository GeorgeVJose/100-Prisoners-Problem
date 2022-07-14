import numpy as np
import plotly.graph_objects as go

def grid_boxes(n=100):
    """
    Returns a heatmap grid with the shuffled prisoner number in each box.
    """
    ns = np.ceil(np.sqrt(n)).astype(int)

    drawer_label = np.arange(1, n+1)
    prisoner_numbers = drawer_label.copy()

    np.random.shuffle(prisoner_numbers)
    prisoner_numbers = prisoner_numbers.reshape(ns, ns)

    drawer_label = drawer_label.reshape(ns, ns)[::-1]

    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z=prisoner_numbers,
            colorscale="ice",
            xgap=10,
            ygap=8,

            text=drawer_label,
            texttemplate="%{text}",
            textfont={"size": 20},

            showscale=False,

            hoverongaps=False,
            hoverinfo="z",

            hoverlabel=dict(
                bgcolor='white',
                font=dict(
                    family='Arial',
                    size=12,
                    color='black'
                ),
                bordercolor='black',
            )
        )
    )
    fig.update_xaxes(showgrid=False, visible=False)
    fig.update_yaxes(showgrid=False, visible=False)
    fig.update_layout(
        width=600,
        height=500,
        margin=dict(l=0, r=0, b=0, t=0,),
    )

    return prisoner_numbers.flatten(), fig

def nodes_histogram(subgraph_nodes_num):
    """
    Returns a histogram of the overall node count for each connected component.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=subgraph_nodes_num,
            name="Subgraphs",
            # marker_color='rgb(158,202,225)',
            # marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5,
            opacity=0.6,
        )
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=True)
    fig.update_layout(
        # width=500,
        height=400,
        margin=dict(l=0, r=0, b=0, t=0,),
    )

    return fig