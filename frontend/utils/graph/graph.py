import numpy as np
from dash import dcc
from typing import Literal
import plotly.express as px
import dash_cytoscape as cyto
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import sample_colorscale

colors = sample_colorscale([[0, "#00587A"], [0.2, "#00487A"], [0.4, "#B08D57"], [0.6, "#7C0A02"],[0.8, "#300000"], [1, "#200000"]], np.linspace(0, 1, 11))

def theme(fig, legend_location="top"):
    if legend_location == "top":
        legend = dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="left",
            x=0
        )
    elif legend_location == "left":
        legend = dict(
            orientation="v",
            yanchor="top",
            y=0.875,
            xanchor="left",
            x=-0.25
        )
    elif legend_location == "right":
        legend = dict(
            orientation="v",
            yanchor="top",
            y=0.875,
            xanchor="right",
            x=1.25
        )

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
        legend=legend,
        paper_bgcolor="#EFEBD6",
        plot_bgcolor="#EFEBD6",
        margin={"l": 25, "r": 25, "t": 100, "b": 25}
    )

def error(type: Literal["server", "chart"]):
    text = "We couldn’t display this chart.<br>Please try again later on." if type == "server" else "This chart is not yet available."

    fig = go.Figure()

    theme(fig)

    fig.add_annotation(
        text=f"<b>{text}</b>",
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=25),
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        meta=dict(error=True, type=type),
        margin={"l": 0, "r": 0, "t": 0, "b": 0}
    )

    return fig

def plot(df, x_label, y_label, title, color_index=0):
    if df is None or isinstance(df, str):
        return df
    
    fig = px.line(df, x_label, y_label, title=title)

    theme(fig)

    fig.update_traces(
        mode="lines+markers",
        line=dict(color=colors[color_index % len(colors)], width=3),
        name=y_label
    )

    return fig

def bar(df, x_label, y_label, title, color_index=0, orientation="v", x_title="", y_title=""):
    if df is None or isinstance(df, str):
        return df
    
    if df.empty:
        fig = px.bar()

        theme(fig)

        return fig
    
    if orientation == "h":
        x_label, y_label = y_label, x_label

    marker_colors = colors[color_index % len(colors)] if color_index >= 0 else sample_colorscale(colors, np.linspace(1, 0, len(df)))
    fig = px.bar(df, x_label, y_label, title=title, orientation=orientation)

    theme(fig)

    if orientation == "h":
        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )
        
    fig.update_layout(
        xaxis_title= x_title if x_title != "" else x_label,
        yaxis_title= y_title if y_title != "" else y_label,
    )
    
    fig.update_traces(
        marker_color=marker_colors,
        name=y_label if orientation == "v" else x_label
    )

    return fig

def pie(df, title):
    if df is None or isinstance(df, str):
        return df
    
    names = df.columns.tolist()
    values = df.iloc[0].values.tolist()

    pie_colors =  sample_colorscale(colors, np.linspace(1, 0, len(names)))
    fig = px.pie(df, names, values, title=title, color_discrete_sequence=pie_colors)

    theme(fig, "left")

    return fig

def gantt(df, x_label, y_label, title):
    if df is None or isinstance(df, str):
        return df
    
    fig = px.timeline(
        df, 
        x_start="starts",
        x_end="ends", 
        y="tasks",    
        color="colors",
        color_discrete_sequence=sample_colorscale(colors, np.linspace(1, 0, len(np.unique(df["tasks"]))))[::-1],
        hover_name="hovertexts",
        title=title,
    )
    
    theme(fig)
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        showlegend=False
    )

    fig.update_traces(
        hovertemplate="%{hovertext}<extra></extra>"
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    return fig

def sankey(elements: dict, title: str):
    if elements is None or isinstance(elements, str):
        return elements
    
    fig = go.Figure(
        data=[go.Sankey(
            arrangement="snap",
            node=dict(
                pad=20,
                thickness=20,
                line=dict(color="#7C0A02", width=0.25),
                label=elements["nodes"],
                color=elements["colors"],
                hovertemplate=elements["node_hovertemplate"],
                customdata=elements["node_customdata"],
            ),
            link=dict(
                source=elements["sources"],
                target=elements["targets"],
                value=elements["values"],
                color="rgba(124, 10, 2, 0.2)",
                hovertemplate=elements["line_hovertemplate"],
                customdata=elements["link_customdata"],
            )
        )]
    )

    theme(fig)

    fig.update_layout(
        title_text=title,
        font_size=20,
        margin={"l": 10, "r": 10, "t": 100, "b": 10}
    )

    return fig

def table(df, title):
    if df is None or isinstance(df, str):
        return df

    # create the table trace
    table_trace = go.Table(
        header=dict(
            values=list(df.columns),
            fill_color=colors[6],
            align="center",
            font=dict(color="#EFEBD6"),
            line=dict(color=colors[4], width=2)
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=[["#EFEBD6", "#DBD7BB"]*(len(df)//2 + 1)],
            align="center",
            line=dict(color=colors[4], width=2)
        )
    )

    fig = go.Figure(data=[table_trace])

    fig.update_layout(
        title=title
    )

    theme(fig) 

    return fig

def box(df, x_col, y_col, color_col, title, x_title, y_title,  show_legend=True):
    if df is None or isinstance(df, str):
        return df
    
    if df.empty:
        fig = px.box()

        theme(fig)

        return fig
    
    fig = px.box(df, 
        x=x_col,
        y=y_col, 
        title=title,
        color=color_col,
        boxmode="group",
        color_discrete_sequence=colors  
    )


    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=show_legend
    )
    
    theme(fig)

    return fig

def scatter(df, x_col, y_col, title, x_title, y_title, hover_cols=None):
    if df is None or isinstance(df, str):
        return df
    
    if df.empty:
        fig = px.scatter()

        theme(fig)

        return fig

    if hover_cols is None: hover_cols = []
        
    fig = px.scatter(df, 
        x=x_col, 
        y=y_col, 
        title=title,
        labels={x_col: x_title, y_col: y_title},
        color=df[x_col],
        color_continuous_scale=colors,
        opacity=0.85,
        hover_data=hover_cols
    )

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
    )

    theme(fig)  
    return fig

def geo(nodes, edges):
    if nodes is None or isinstance(nodes, str):
        return nodes

    fig = px.scatter_geo(
        nodes,
        lat="latitudes",
        lon="longitudes",
        size="sizes",
        hover_name="hovertexts",
        projection="natural earth",
        scope="world"
    )

    fig.update_geos(
        showframe=False,
        showcountries=True,
        countrycolor="#B08D57",
        showland=True,
        landcolor="#DDD0BE",
        showlakes=True,
        lakecolor="#3E9BC0",
        showocean=True,
        oceancolor="#1D81A9",
        fitbounds="locations"
    )

    fig.update_traces(
        marker=dict(
            line=dict(color="#EFEBD6"),
            color=nodes["colors"],
            opacity=0.7
        ),
        hovertemplate="%{hovertext}<extra></extra>"
    )

    for lat, lon, width in zip(edges["latitudes"], edges["longitudes"], edges["sizes"]):
        fig.add_trace(go.Scattergeo(
            lat=lat,
            lon=lon,
            mode="lines",
            line=dict(width=width, color="#7C0A02"),
            opacity=0.2,
            showlegend=False,
            hoverinfo="skip"
        )
    )
    
    theme(fig)

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        geo=dict(bgcolor="#EFEBD6"),
        paper_bgcolor="#EFEBD6"
    )

    return fig

def combine(figures_y_left: list, figures_y_right: list, x_label, y_labels, title, legend_location: Literal["top", "left", "right"]="top"):
    if all(figure is None or isinstance(figure, str) for figure in figures_y_left + figures_y_right):
        return error((figures_y_left + figures_y_right)[0])
    
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

    theme(supfig, legend_location)

    supfig.update_traces(showlegend=True)

    return supfig

def graph(figure):
    if figure is None:
        return dcc.Graph(
            figure=error("server"),
            className="graph",
            config={'responsive': True}
        )

    elif isinstance(figure, str):
        return dcc.Graph(
            figure=error("chart"),
            className="graph",
            config={'responsive': True}
        )

    elif isinstance(figure, go.Figure):
        return dcc.Graph(
            figure=figure,
            className="graph",
            config={'responsive': True}
        )
    
    elif isinstance(figure, list):
        return cyto.Cytoscape(
            className="graph",
            layout={"name": "concentric"},
            style={"width": "100%", "height": "100%"},
            elements=figure,
            stylesheet=[
                {"selector": "node",
                    "style": {
                    "label": "data(label)",
                    "width": "data(size)",
                    "height": "data(size)",
                    "background-color": "data(color)",
                    "font-size": "8px",
                    "font-family": "Cormorant SC, Georgia, serif",
                    "font-weight": "600" 
                }},
                {"selector": "edge",
                    "style": {
                    "curve-style": "bezier",
                    "line-color": "#7C0A02",
                    "opacity": 0.2,
                    "width": "data(size)"
                }},                   
            ],
        )