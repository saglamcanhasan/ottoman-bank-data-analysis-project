import plotly.express as px

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