# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:35:06 2022

@author: Petra
"""
#Verschillende imports en opmaak pagina
import streamlit as st
import plotly.express as px
import plotly
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data = pd.read_excel(st.session_state.uploaded_file)

st.set_page_config(page_title="Gantt diagram")
st.header('Gantt diagram')

#data inlezen en bepaalde gegevens apart zetten
data = pd.read_excel(st.session_state.uploaded_file)

starttijd = data['Vertrek']
eindtijd = data['Aankomst']
bus = data['Bus']
tijdsbesteding = data['Dienst']
order = {'Tijdsbesteding': ["400", "401", "Opladen", "Materiaal rit"]}
colors = {'Materiaal rit': '#2794e3', '400': '#ff0511', '401': '#faab23', 'Opladen': '#50fc2d'}

#lijst maken met 400 en 401 ipv dienstrit
lijn = data.Dienst
for i in range(len(data)):
    if lijn[i] == 'Dienstrit':
        lijn[i] = int(data.Buslijn[i])

#input voor timeline
lijst = []
for i in range(len(data)):
    lijst.append(dict(Bus=str(bus[i]), Start=str(starttijd[i]), End=str(eindtijd[i]), Tijdsbesteding=str(tijdsbesteding[i])))
    
df = pd.DataFrame(lijst)

#Omzetten naar tijdreeksen waarbij ook word gekeken naar de dagen 
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

for i in range(len(data)):
    if (str(df['Start'][i])[11:13]) < '05':
        df["Start"][i] = df["Start"].apply(lambda x: x.replace(year=2023, month=1, day=2))[i]
    else:
        df["Start"][i] = df["Start"].apply(lambda x: x.replace(year=2023, month=1, day=1))[i]

for i in range(len(data)):
    if (str(df['End'][i])[11:13]) < '05':
        df["End"][i] = df["End"].apply(lambda x: x.replace(year=2023, month=1, day=2))[i]
    else:
        df["End"][i] = df["End"].apply(lambda x: x.replace(year=2023, month=1, day=1))[i]
        
#plotten van het figuur
fig = px.timeline(df, x_start="Start", x_end="End", y="Bus", color_discrete_map = colors, color="Tijdsbesteding", hover_name = lijn, category_orders = order)

fig.update_layout(
                        title='Omloopplanning bussen',
                        hoverlabel_bgcolor='#DAEEED',   #Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
                        bargap=0.2,
                        height=600,              
                        xaxis_title="Tijd", 
                        yaxis_title="Busnummer",                   
                        title_x=0.45,                    #Make title centered                     
                        xaxis=dict()
                    )


fig.update_yaxes(autorange= 'reversed')
fig.update_xaxes(tickangle=0, tickfont=dict(family='Rockwell', color='black', size=15))

fig.update_traces(marker=dict(
        
        line=dict(color='rgba(58, 71, 80, 1.0)', width=1.5)
    ))

st.plotly_chart(fig,use_container_height=True,width=200)
