# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 12:10:04 2022

@author: Petra
"""
import streamlit as st
import pandas as pd
import datetime
import numpy as np
import plotly.express as px

data = pd.read_excel(st.session_state.uploaded_file)
st.header('Extra informatie')
st.subheader('Hoeveel kWh elke bus kan terug leveren')

for i in range(len(data)):
    if data.Dienst[i] == 'Dienstrit':
        data.Dienst[i] = int(data.Buslijn[i])

Spits = []

for i in range(len(data)):
    if data.Vertrek[i] < datetime.time(9,0) and data.Aankomst[i] > datetime.time(7,0):
        Spits.append('spits')
    elif data.Vertrek[i] < datetime.time(19,0) and data.Aankomst[i] > datetime.time(16,0):
        Spits.append('spits')
    else:
        Spits.append('niet_spits')

 

Spits = pd.DataFrame(Spits, columns=['Spits'])
data = pd.concat([data, Spits], axis = 1)

# Gegeven waardes 
volle_batterij  = 315
soc_max         = 0.9 * volle_batterij
soc_min         = 0.1 * volle_batterij
opladen_per_min = 250/60

#Beginwaarde batterij per bus
batterijwaarde_bus = []
aantal_bussen = len(set(data['Bus']))
for i in range(aantal_bussen):
    batterijwaarde_bus.append(315)

#Verbruik verwijzing 
ritten = {
    400             : {"spits"      : {"Eindhoven airport" : {"Eindhoven busstation" : 20.5000},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 21.4160}},
                       "niet_spits" : {"Eindhoven airport" : {"Eindhoven busstation" : 17.9375},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 18.7390}}},
    401             : {"spits"      : {"Eindhoven airport" : {"Eindhoven busstation" : 18.1000},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 18.0060}},
                       "niet_spits" : {"Eindhoven airport" : {"Eindhoven busstation" : 15.8375},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 15.7553}}},
    "Materiaal rit" : {"spits"      : {"Eindhoven airport" : {"Eindhoven busstation" : 12.9000,
                                                              "Eindhoven garage"     : 13.50000},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 12.9000,
                                                                 "Eindhoven garage"  : 2.4750},
                                       "Eindhoven garage" : {"Eindhoven airport"     : 13.5000,
                                                             "Eindhoven busstation"  : 2.4750}},
                      "niet_spits"  : {"Eindhoven airport" : {"Eindhoven busstation" : 12.9000,
                                                              "Eindhoven garage"     : 13.50000},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 12.9000,
                                                                 "Eindhoven garage"  : 2.4750},
                                       "Eindhoven garage" : {"Eindhoven airport"     : 13.5000,
                                                             "Eindhoven busstation"  : 2.4750}}},
    "Opladen"      : {"spits"       : {"Eindhoven garage" : {"Eindhoven garage"      : 0.0000}},
                      "niet_spits"  : {"Eindhoven garage" : {"Eindhoven garage"      : 0.0000}}}
}

 
# Berekenen lengte van een rit
lengte_rit = []

for i in range(len(data)):
    a = data.Vertrek[i]
    b = data.Aankomst[i]
    da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
    db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)

 

    lengte_rit.append(((db-da).seconds)/60)

# Check voor de te hoge of te lage SOC-Waarden
laagste_waarde_soc = batterijwaarde_bus
verbruik = []

for i in range(len(data)):
    batterijwaarde_bus[data.Bus[i]-1] -= ritten[data.Dienst[i]][data.Spits[i]][data.Startlocatie[i]][data.Eindlocatie[i]]
    if batterijwaarde_bus[data.Bus[i]-1] < laagste_waarde_soc[data.Bus[i]-1]:
        laagste_waarde_soc[data.Bus[i]-1] = batterijwaarde_bus[data.Bus[i]-1]
    if data.Dienst[i] == 'Opladen':
        batterijwaarde_bus[data.Bus[i]-1] += (lengte_rit[i]*opladen_per_min)
        if batterijwaarde_bus[data.Bus[i]-1] > soc_max:
            print('Deze omloopsplanning is niet haalbaar')
            print(f'Omdat de soc-waarde: {batterijwaarde_bus[data.Bus[i]-1]} van bus: {data.Bus[i]}, te hoog komt tijdens het opladen op tijdstip {data.Vertrek[i]}\n')
    if batterijwaarde_bus[data.Bus[i]-1] < soc_min:         
        print('Deze omloopsplanning is niet haalbaar')
        print(f'Omdat de soc-waarde: {batterijwaarde_bus[data.Bus[i]-1]} van bus: {data.Bus[i]}, te laag komt op tijdstip {data.Vertrek[i]}\n')
    verbruik.append(batterijwaarde_bus[data.Bus[i]-1])
min_charge = []

for i in range(aantal_bussen):
    min_charge.append(31.5)

totaal_terugleveren = 0
for i in range(aantal_bussen):
    laagste_waarde_soc[i] -= min_charge[i]
    if laagste_waarde_soc[i] < 0:
        laagste_waarde_soc[i] = 0
    totaal_terugleveren += laagste_waarde_soc[i]
    st.caption(f'Bij bus {i+1} kun je {laagste_waarde_soc[i]:.1f} kWh terugleveren.')
    
## Grafiek energie levels bussen
#st.subheader('Overzicht energie levels bus gedurende dag')
data['Verbruik'] = verbruik
# st.dataframe(data)

fig = px.line(data, x = 'Vertrek', y = 'Verbruik')


