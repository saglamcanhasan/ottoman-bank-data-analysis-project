import numpy as np
import pandas as pd
from typing import Literal
import plotly.express as px
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
    )

def error(type: Literal["server", "chart"]):
    text = "We couldn’t display this chart.<br>Please try again later on." if type == "server" else "This chart is not yet available"

    fig = go.Figure()

    theme(fig)

    fig.add_annotation(
        text=f"<b>{text}.</b>",
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=25),
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        meta=dict(error=True, type=type)
    )

    return fig

def plot(df, x_label, y_label, title, color_index=0):
    if df is None:
        return error("server")
    elif isinstance(df, str):
        return error("chart")
    
    fig = px.line(df, x_label, y_label, title=title)

    theme(fig)

    fig.update_traces(
        mode="lines+markers",
        line=dict(color=colors[color_index % len(colors)], width=3),
        name=y_label
    )

    return fig

def bar(df, x_label, y_label, title, color_index=0, orientation="v", x_title="", y_title=""):
    if df is None:
        return error("server")
    elif isinstance(df, str):
        return error("chart")
    
    if df.empty:
        fig = px.bar()

        theme(fig)

        return fig
    
    if orientation == "h":
        x_label, y_label = y_label, x_label

    marker_colors = colors[color_index % len(colors)] if color_index >= 0 else sample_colorscale([[0, "#B08D57"], [0.5, "#7C0A02"], [1, "#200000"]], np.linspace(1, 0, len(df)))
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
    if df is None:
        return error("server")
    elif isinstance(df, str):
        return error("chart")
    
    names = df.columns.tolist()
    values = df.iloc[0].values.tolist()

    pie_colors =  sample_colorscale([[0, "#B08D57"], [0.5, "#7C0A02"], [1, "#200000"]], np.linspace(1, 0, len(names)))
    fig = px.pie(df, names, values, title=title, color_discrete_sequence=pie_colors)

    theme(fig, "left")

    return fig

def gantt(df, x_start_column, x_end_column, y_column, color_column, xlabel, xstartlabel, xendlabel, ylabel, title="", color_title=""):
    if df is None:
        return error("server")
    elif isinstance(df, str):
        return error("chart")
    
    if df.empty:
        fig = px.timeline()

        theme(fig)
        
        return fig
    
    fig = px.timeline(df, 
                      x_start=x_start_column,
                      x_end=x_end_column, 
                      y=y_column,    
                      color=color_column,
                      color_discrete_sequence=colors,
                      labels={y_column: ylabel, 
                              x_start_column: xstartlabel, 
                              x_end_column: xendlabel, 
                              color_column: color_title},
                      title=title)
    
    fig.update_layout(xaxis_title=xlabel, yaxis_title=ylabel)
    
    theme(fig, "right")

    return fig

def sankey(elements: dict, title: str):
    if elements is None:
        return error("server")
    elif isinstance(elements, str):
        return error("chart")
    
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

    fig.update_layout(title_text=title, font_size=10)

    return fig

def table(df, columns_to_display=None, title="Table Title"):
    if df is None:
        return error("server")
    elif isinstance(df, str):
        return error("chart")
    
    if df.empty:
        fig = go.Figure()

        theme(fig)

        return fig 

    if columns_to_display is None:
        df_filtered = df
    else:
        df_filtered = df[columns_to_display]

    # Create the table trace
    table_trace = go.Table(
        header=dict(values=list(df_filtered.columns),
                    fill_color="#7C0A02",  # Header background color
                    align="center",
                    font=dict(color="white")),
        cells=dict(values=[df_filtered[col] for col in df_filtered.columns],
                   fill_color="#EFEBD6",  # Cells background color
                   align="center")
    )

    fig = go.Figure(data=[table_trace])

    fig.update_layout(title=title)
    theme(fig) 

    return fig

def box(df, x_col, y_col, color_col, title, x_title, y_title,  show_legend=True):
    if df is None:
        return error("server")
    elif isinstance(df, str):
        return error("chart")
    
    if df.empty:
        fig = px.box()

        theme(fig)

        return fig
    
    fig = px.box(df, 
                 x= x_col,
                 y= y_col, 
                 title= title,
                 color= color_col,
                 boxmode='group',
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
    if df is None:
        return error("server")
    elif isinstance(df, str):
        return error("chart")
    
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
                     hover_data=hover_cols)

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
    )

    theme(fig)  
    return fig

def map(nodes, edges):
    if nodes is None:
        return error("server")
    elif isinstance(nodes, str):
        return error("chart")

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

    for lat, lon, width in zip(edges["latitudes"], edges["longitudes"], edges["sizes"]):
        fig.add_trace(go.Scattergeo(
            lat=lat,
            lon=lon,
            mode="lines",
            line=dict(width=width, color="#7C0A02"),
            opacity=0.2,
            showlegend=False
        )
    )

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        geo=dict(bgcolor="#EFEBD6"),
        paper_bgcolor="#EFEBD6"
    )

    fig.update_traces(
        marker=dict(
            line=dict(color="#EFEBD6"),
            color=nodes["colors"],
            opacity=0.7
        ),
        hovertemplate="%{hovertext}<extra></extra>"
    )
    
    theme(fig)

    return fig

def combine(figures_y_left: list, figures_y_right: list, x_label, y_labels, title, legend_location: Literal["top", "left", "right"]="top"):
    if all(figure.layout.meta and figure.layout.meta.get("error", False) for figure in figures_y_left + figures_y_right):
        return error((figures_y_left + figures_y_right)[0].layout.meta["type"])
    
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