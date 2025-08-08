import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.colors import sample_colorscale
import pandas as pd

colors = ["#00587A", "#00487A", "#B08D57", "#7C0A02","#300000", "#200000"]

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
        showlegend=False,
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

    colors = colors[color_index % len(colors)] if color_index >= 0 else sample_colorscale([[0, "#B08D57"], [0.5, "#7C0A02"], [1, "#200000"]], np.linspace(1, 0, len(df)))
    fig = px.bar(df, x_label, y_label, title=title, orientation=orientation)

    theme(fig)

    if orientation == "h":
        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )

    fig.update_traces(
        marker_color=colors,
        name=y_label if orientation == "v" else x_label
    )

    return fig

def plot_gantt(df, x_start_column, x_end_column, y_column, color_column, xlabel, ylabel):
    if df.empty:
        return px.timeline()  # Returning an empty bar chart
    
    df['Start'] = pd.to_datetime(df['Start'], format='%Y')  # Convert to datetime (if not already)
    df['Finish'] = pd.to_datetime(df['Finish'], format='%Y')  # Convert to datetime (if not already)

    fig = px.timeline(df, 
                      x_start=x_start_column,
                      x_end=x_end_column, 
                      y=y_column,    
                      color=color_column,
                      labels={y_column: ylabel, 
                              x_start_column: xlabel, 
                              x_end_column: "End Year", 
                              color_column: "Country/Agency"},
                      title="Employee Career Timeline by Country/Agency")
    
    fig.update_layout(xaxis_title=xlabel, yaxis_title=ylabel)
    
    theme(fig)

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