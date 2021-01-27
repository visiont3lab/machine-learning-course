from plotly import graph_objects as go
import pandas as pd
import numpy as np 
from datetime import datetime
import os

# Configurazione ambiente virtuale
# !pip install plotly==4.12.0 kaleido
# virtualenv env
# virtualenv --python=python3 env
# WINDOWS: source env/Scripts/activate
# MACOS/LINUX source env/bin/activate

# Installazione librerie
# pip install plotly==4.12.0 kaleido pandas
# pip list

def customPlot(df,toplot,diz,nameSave="Ciao"):
    #print(diz)
    fig = go.Figure()
    # Mettiamo le tracce
    for v in toplot:
        fig.add_traces(
            go.Scatter(
                x=df["data"].values,
                y=df[v].values,
                name=v,
                mode="lines",
                line_color=diz[v]
            )
        )
    # Aggiorniamo il layout
    fig.update_layout(
        title_text=nameSave,
        title_font_size=50,
        font_color="white",
        paper_bgcolor="black",
        plot_bgcolor="white",
        xaxis_showgrid=False,
        #xaxis_range=['2021-01-01','2021-01-31'],
        xaxis= dict(
                dtick="M1",
                tickformat="%d-%m-%Y",
                ticklabelmode="period",
            ),
        yaxis_showgrid=False,
        hovermode="x",  
    )

    d = datetime.now()
    dstring = d.strftime("%Y-%m-d_%H_%M_SS")
    fig.write_html("results/" + nameSave +dstring + ".html")
    fig.write_image("results/" + nameSave + dstring+ ".png")

    return fig

if __name__ == '__main__':
    try:
        os.makedirs("results")
    except OSError as e:
        print("directory already  exist", e)

    # Read data
    url ="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
    df = pd.read_csv(url) # lettura

    # Creazione dizionario
    l1 = ["deceduti", "totale_positivi", "totale_casi","variazione_totale_positivi","nuovi_positivi"]
    l2 = ["rgb(255,0,0)","rgb(0,255,221)","rgb(0,255,15)","rgb(0,255,155)","rgb(0,255,0)"]
    diz = {  k: v for k,v in zip(l1,l2) }

    # Figura 1 
    toplot1 = ["deceduti", "totale_positivi", "totale_casi"]
    fig1 = customPlot(df,toplot1,diz, nameSave="Andamento-Generale")

    # Figura 2
    toplot2 = ["variazione_totale_positivi"]
    fig2 = customPlot(df,toplot2,diz,nameSave="Variazione-Totale-Positivi")

    # Figura 3
    toplot3 = ["nuovi_positivi"]
    fig3 = customPlot(df,toplot3,diz,nameSave="Nuovi-Positivi")
