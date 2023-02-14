# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:38:41 2022

@author: Petra
"""

import streamlit as st
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.header('Planningen vergelijken')
st.markdown('---')    
st.subheader('Hieronder kunt u 2 planningen invullen en deze vergelijken met elkaar.')
st.session_state.data_file1 = st.file_uploader("Kies uw eerste data bestand.", type =['xlsx'])
st.session_state.data_file2 = st.file_uploader("Kies uw tweede data bestand.", type =['xlsx'])
    
data = pd.read_excel(st.session_state.data_file1)
data1 = pd.read_excel(st.session_state.data_file2)

aantal_bussen2 = len(set(data['Bus']))
aantal_bussen3 = len(set(data1['Bus']))

DRU = 0
onbeladen_rit = 0
stilstaan = 0

for i in range(len(data.Dienst)):
    if data.Dienst[i] == 'Dienstrit':
        a = data.Vertrek[i]
        b = data.Aankomst[i]
        da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
        db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)
        lengte_rit = ((db-da).seconds)/60
        DRU += lengte_rit
    else:
        a = data.Vertrek[i]
        b = data.Aankomst[i]
        da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
        db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)
        lengte_rit = ((db-da).seconds)/60
        onbeladen_rit += lengte_rit
       
for i in range(len(data)-1):
    if data.Bus[i] == data.Bus[i+1]:
        a = data.Vertrek[i + 1]
        b = data.Aankomst[i]
        da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
        db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)
        lengte_pauze = ((da-db).seconds)/60
        stilstaan += lengte_pauze
    else:
        stilstaan += 0
        
DPRU = DRU + onbeladen_rit + stilstaan
DD = DPRU/DRU

DRU = 0
onbeladen_rit = 0
stilstaan = 0
        
for i in range(len(data1.Dienst)):
    if data1.Dienst[i] == 'Dienstrit':
        a = data1.Vertrek[i]
        b = data1.Aankomst[i]
        da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
        db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)
        lengte_rit = ((db-da).seconds)/60
        DRU += lengte_rit
    else:
        a = data1.Vertrek[i]
        b = data1.Aankomst[i]
        da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
        db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)
        lengte_rit = ((db-da).seconds)/60
        onbeladen_rit += lengte_rit
       
for i in range(len(data1)-1):
    if data1.Bus[i] == data1.Bus[i+1]:
        a = data1.Vertrek[i + 1]
        b = data1.Aankomst[i]
        da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
        db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)
        lengte_pauze = ((da-db).seconds)/60
        stilstaan += lengte_pauze
    else:
        stilstaan += 0
        
DPRU1 = DRU + onbeladen_rit + stilstaan
DD1 = DPRU/DRU

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

min_charge = []

for i in range(aantal_bussen):
    min_charge.append(31.5)

totaal_terugleveren = 0
for i in range(aantal_bussen):
    laagste_waarde_soc[i] -= min_charge[i]
    if laagste_waarde_soc[i] < 0:
        laagste_waarde_soc[i] = 0
    totaal_terugleveren += laagste_waarde_soc[i]
    print(f'Bij bus {i+1} kun je {laagste_waarde_soc[i]} kWh terugleveren.')

## voor data1
for i in range(len(data1)):
    if data1.Dienst[i] == 'Dienstrit':
        data1.Dienst[i] = int(data1.Buslijn[i])

Spits = []

for i in range(len(data1)):
    if data1.Vertrek[i] < datetime.time(9,0) and data1.Aankomst[i] > datetime.time(7,0):
        Spits.append('spits')
    elif data1.Vertrek[i] < datetime.time(19,0) and data1.Aankomst[i] > datetime.time(16,0):
        Spits.append('spits')
    else:
        Spits.append('niet_spits')

 

Spits = pd.DataFrame(Spits, columns=['Spits'])
data1 = pd.concat([data1, Spits], axis = 1)

# Gegeven waardes 
volle_batterij  = 315
soc_max         = 0.9 * volle_batterij
soc_min         = 0.1 * volle_batterij
opladen_per_min = 250/60

#Beginwaarde batterij per bus
batterijwaarde_bus = []
aantal_bussen = len(set(data1['Bus']))
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

for i in range(len(data1)):
    a = data1.Vertrek[i]
    b = data1.Aankomst[i]
    da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
    db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)

 

    lengte_rit.append(((db-da).seconds)/60)

# Check voor de te hoge of te lage SOC-Waarden
laagste_waarde_soc = batterijwaarde_bus

for i in range(len(data1)):
    batterijwaarde_bus[data1.Bus[i]-1] -= ritten[data1.Dienst[i]][data1.Spits[i]][data1.Startlocatie[i]][data1.Eindlocatie[i]]
    if batterijwaarde_bus[data1.Bus[i]-1] < laagste_waarde_soc[data1.Bus[i]-1]:
        laagste_waarde_soc[data1.Bus[i]-1] = batterijwaarde_bus[data1.Bus[i]-1]
    if data1.Dienst[i] == 'Opladen':
        batterijwaarde_bus[data1.Bus[i]-1] += (lengte_rit[i]*opladen_per_min)
        if batterijwaarde_bus[data1.Bus[i]-1] > soc_max:
            print('Deze omloopsplanning is niet haalbaar')
            print(f'Omdat de soc-waarde: {batterijwaarde_bus[data.Bus[i]-1]} van bus: {data.Bus[i]}, te hoog komt tijdens het opladen op tijdstip {data.Vertrek[i]}\n')
    if batterijwaarde_bus[data1.Bus[i]-1] < soc_min:         
        print('Deze omloopsplanning is niet haalbaar')
        print(f'Omdat de soc-waarde: {batterijwaarde_bus[data.Bus[i]-1]} van bus: {data.Bus[i]}, te laag komt op tijdstip {data.Vertrek[i]}\n')

min_charge = []

for i in range(aantal_bussen):
    min_charge.append(31.5)

totaal_terugleveren1 = 0
for i in range(aantal_bussen):
    laagste_waarde_soc[i] -= min_charge[i]
    if laagste_waarde_soc[i] < 0:
        laagste_waarde_soc[i] = 0
    totaal_terugleveren1 += laagste_waarde_soc[i]
    print(f'Bij bus {i+1} kun je {laagste_waarde_soc[i]} kWh terugleveren.')

minimale_bussen = 8
maximale_bussen = 20

minimale_DDs = 1.3
maximale_DDs = 1.8

minimale_DPRUs = 5234
maximale_DPRUs = 28800

minimale_verbruik = 0
maximale_verbruik_bus1 = 283.5*aantal_bussen2
maximale_verbruik_bus2 = 283.5*aantal_bussen3

st.markdown('---')    
st.subheader('Hier kunt u de resultaten zien:')
st.write('Aan de linkerkant staat de eerste dataset, aan de rechterkant staat de tweede dataset')

st.text('In dit figuur is te zien hoe goed de planningen scoren op het aantal bussen dat gebruikt wordt. De minimum lijn staat voor het aantal bussen dat minimaal gebruikt moet worden om alle ritten te rijden.     
f = go.FigureWidget()
f.add_scatter(y=[maximale_bussen, maximale_bussen], x=[0.5,2.5], marker=dict(size=0, color="red"), name = 'maximum')
f.add_scatter(y=[minimale_bussen, minimale_bussen], x=[0.5,2.5], marker=dict(size=0, color="red"), name = 'minimum')
f.update_layout(title = 'Aantal bussen dat gebruikt wordt voor de planning', title_x=0.45, xaxis_title = 'Datasets', yaxis_title = 'Aantal bussen')
f.add_bar(y=[aantal_bussen2, aantal_bussen3], x=[1,2], marker = dict(color = 'blue'), name = 'aantal bussen')
st.plotly_chart(f)
st.caption(f'Dataset 1: {aantal_bussen2} bussen')
st.caption(f'Dataset 2: {aantal_bussen3} bussen')

st.markdown('---')    
f1 = go.FigureWidget()
f1.add_scatter(y=[maximale_DDs, maximale_DDs], x=[0.5,2.5], marker=dict(size=0, color="red"), name = 'maximum')
f1.add_scatter(y=[minimale_DDs, minimale_DDs], x=[0.5,2.5], marker=dict(size=0, color="red"), name = 'minimum')
f1.update_layout(title = 'Verhouding DDs', title_x=0.45, xaxis_title = 'Datasets', yaxis_title = 'Verhouding DDs')
f1.add_bar(y=[DD, DD1],x=[1,2], marker = dict(color = 'blue'), name = 'Verhouding DDs')
st.plotly_chart(f1)
st.caption(f'Dataset 1: {DD:.2f} DDs')
st.caption(f'Dataset 2: {DD1:.2f} DDs')

st.markdown('---')    
f3 = go.FigureWidget()
f3.add_scatter(y=[maximale_DPRUs, maximale_DPRUs], x=[0.5,2.5], marker=dict(size=0, color="red"), name = 'maximum')
f3.add_scatter(y=[minimale_DPRUs, minimale_DPRUs], x=[0.5,2.5], marker=dict(size=0, color="red"), name = 'minimum')
f3.update_layout(title = 'Aantal DPRUs', title_x=0.45, xaxis_title = 'Datasets', yaxis_title = 'Aantal DPRUs')
f3.add_bar(y=[DPRU, DPRU1],x=[1,2], marker = dict(color = 'blue'), name = 'aantal DPRUs')
st.plotly_chart(f3)
st.caption(f'Dataset 1: {DPRU:.2f} DPRUs')
st.caption(f'Dataset 2: {DPRU1:.2f} DPRUs')

st.markdown('---')    
f4 = go.FigureWidget()
f4.add_scatter(y=[maximale_verbruik_bus1, maximale_verbruik_bus1], x=[0.5,2.5], marker=dict(size=0, color="red"), name = 'maximum dataset 1')
f4.add_scatter(y=[maximale_verbruik_bus2, maximale_verbruik_bus2], x=[0.5,2.5], marker=dict(size=0, color="orange"), name = 'maximum dataset 2')
#f4.add_scatter(y=[minimale_verbruik, minimale_verbruik], x=[0.5,2.5], marker=dict(size=0, color="red"), name = 'minimum')
f4.update_layout(title = 'Aantal kWh teruggeleverd', title_x=0.45, xaxis_title = 'Datasets', yaxis_title = 'Aantal kWh teruggeleverd')
f4.add_bar(y=[totaal_terugleveren, totaal_terugleveren1],x=[1,2], marker = dict(color = 'blue'), name = 'aantal kWh teruggeleverd')
st.plotly_chart(f4)
st.caption(f'Dataset 1: {totaal_terugleveren:.2f} kWh teruggeleverd')
st.caption(f'Dataset 2: {totaal_terugleveren1:.2f} kWh teruggeleverd')
st.markdown('---')    


















