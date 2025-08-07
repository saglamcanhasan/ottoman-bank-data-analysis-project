import plotly.express as px
import dash_cytoscape as cyto
from plotly.subplots import make_subplots
from plotly.colors import sample_colorscale

colors = ["#B08D57", "#00587A", "#00487A", "#7C0A02","#300000"]

def theme(fig):
    fig.update_layout(
        font=dict(
            family="Cormorant SC",
            size=16,
            color= "#7C0A02",
            weight=600
        ),
        title_font=dict(
            family="Cormorant SC",
            size=28,
            color="#7C0A02"
        ),
        hoverlabel=dict(
            font_family="Cormorant Garamond",
            font_size=20,
            font_color="#EFEBD6",
            bordercolor="#B08D57"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#DFC6A0",
            linecolor="#DFC6A0",
            zerolinecolor="#B08D57", 
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#DFC6A0",
            linecolor="#DFC6A0",
            zerolinecolor="#B08D57", 
        ),
        yaxis2=dict(
            showgrid=True,
            linecolor="#DFC6A0",
            zerolinecolor="#DFC6A0"
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="left",
            x=0
        ),
        paper_bgcolor="#EFEBD6",
        plot_bgcolor="#EFEBD6",
    )

def plot(df, x_label, y_label, title, color_index=0):
    fig = px.line(df, x_label, y_label, title=title)

    theme(fig)

    fig.update_traces(
        mode="lines+markers",
        line=dict(color=colors[color_index % len(colors)], width=3),
        name=y_label
    )

    return fig

def bar(df, x_label, y_label, title, color_index=0, orientation="v"):
    if orientation == "h":
        x_label, y_label = y_label, x_label

    fig = px.bar(df, x_label, y_label, title=title, orientation=orientation)

    theme(fig)

    fig.update_traces(
        marker_color=colors[color_index % len(colors)],
        name=y_label if orientation == "v" else x_label
    )

    return fig

def combine(figures_y_left: list, figures_y_right: list, x_label, y_labels, title):
    is_there_second_y_label = len(figures_y_right) != 0
    
    supfig = make_subplots(specs=[[{"secondary_y": is_there_second_y_label}]])
    
    for figure_list_index, figure_list in enumerate([figures_y_left, figures_y_right]):
        secondary_y = figure_list_index == 1
        for figure in figure_list:
            for trace in figure.data:
                supfig.add_trace(trace, secondary_y=secondary_y)
                
    supfig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_labels[0],
        barmode="group",
    )

    if is_there_second_y_label:
        supfig.update_yaxes(title_text=y_labels[1], secondary_y=True)

    theme(supfig)

    supfig.update_traces(showlegend=True)

    return supfig

def plot_bar(df, x, y, title, xlabel, ylabel, top_n=10, horizontal=True):
    df_sorted = df.sort_values(by=x, ascending=False).head(top_n)

    fig = px.bar(
        df_sorted,
        x=x if not horizontal else None,
        y=y if horizontal else None,
        orientation='h' if horizontal else 'v',
        title=title,
        labels={x: xlabel, y: ylabel},
        template='plotly_white'
    )

    fig.update_layout(
        margin=dict(l=120, r=40, t=50, b=40),
        yaxis=dict(autorange='reversed') if horizontal else {}
    )

    return fig

def build_cyto_from_networkx(G, positions=None, is_colored=False):
    
    def get_gradient_color(value, min_val, max_val, colorscale):
        norm_value = (value - min_val) / (max_val - min_val) if max_val != min_val else 0
        return sample_colorscale(colorscale, [norm_value])[0]
    
    ottoman_colorscale = [
        [0.0, "#B08D57"],  # gold
        [0.4, "#7C0A02"],  # red
        [0.7, "#300000"],  # dark red
        [1.0, "#200000"]   # darkest red
    ]
    
    # cyto cose computes positions itself. if springlayout and fixed positions used, pass it down
    node_weights = {}
    for node in G.nodes(): # Sum of weights of edges connected to node
        total_weight = sum(data['weight'] for _, _, data in G.edges(node, data=True))
        node_weights[node] = total_weight

    elements = []
    max_weight = max(node_weights.values()) if node_weights else 1

    for node in G.nodes():
        weight = node_weights.get(node, 0)
        size = 20 + (weight / max_weight) * 30  # base size 20, up to 50
        if is_colored:
            color = get_gradient_color(weight, 0, max_weight, ottoman_colorscale)
        else:
            color = "#B08D57"   
        # You can normalize color similarly, or assign categories
        elements.append({
            "data": {
                "id": node,
                #"label": node,
                "weight": weight,
                "size": size,
                "color": color
            }
        })


    for source, target, data in G.edges(data=True):
        elements.append({
            "data": {
                "source": source,
                "target": target,
                #"label": f"{data['weight']} years"
            }
        })

    return elements

def plot_cyto(elements, graph_id="", width="100%", height="100%", node_size_attr="size"):
    return cyto.Cytoscape(
        id=graph_id,
        style={"width": width, "height": height},
        elements=elements,
        layout={'name': 'cose', 'animate': False}
    )