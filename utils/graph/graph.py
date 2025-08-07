import plotly.express as px
import dash_cytoscape as cyto
from plotly.colors import sample_colorscale

def plot(df, x_label, y_label, title):
    fig = px.line(df, x_label, y_label, title=title)

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
            bgcolor="#00587A",
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
        paper_bgcolor="#EFEBD6",
        plot_bgcolor="#EFEBD6",
    )

    fig.update_traces(
        mode="lines+markers",
        line=dict(color="#00587A", width=3)
    )

    return fig

def plot_bar(df, x, y, title, xlabel, ylabel, top_n=10, horizontal=True):
    
    if df.empty:
        return px.bar()  # Returning an empty bar chart
    
    df = df.dropna(subset=[x])
    df_sorted = df.sort_values(by=x, ascending=False).head(top_n)

    fig = px.bar(
        df_sorted,
        x=x ,
        y=y ,
        orientation='h' if horizontal else 'v',
        title=title,
        labels={x: xlabel, y: ylabel},
        template='plotly_white',
        color=y,
        color_discrete_sequence=["#7C0A02","#852010","#8D361E","#964C2D","#9F613B","#A77749","#B08D57"]
    )

    if horizontal:
        fig.update_layout(
            yaxis=dict(autorange='reversed')  # This ensures largest values are at the top
        )
    
    fig.update_layout(
        font=dict(
            family="Cormorant SC",
            size=16,
            color="#7C0A02",
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
            bgcolor="#00587A",
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
        paper_bgcolor="#EFEBD6",
        plot_bgcolor="#EFEBD6",
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
        size = 5 + (weight / max_weight) * 15  # base size 5, up to 20
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