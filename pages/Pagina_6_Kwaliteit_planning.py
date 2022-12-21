# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 19:49:38 2022

@author: Petra
"""
import streamlit as st
import pandas as pd
import datetime
import numpy as np

st.header('Kwaliteit planning')
st.subheader('De volgende kwaliteiten zitten aan de volgende wensen')
data = pd.read_excel(st.session_state.uploaded_file)
ritten = pd.read_excel(r'C:/Users/Petra/OneDrive - Office 365 Fontys/Toegepaste wiskunde/Jaar 2/Project/Project 5/programmeren/Connexxion data - 2022-2023.xlsx')

aantal_bussen = len(set(data['Bus']))

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
        a = data.Vertrek[i+1]
        b = data.Aankomst[i]
        da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
        db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)
        lengte_pauze = ((da-db).seconds)/60
        stilstaan += lengte_pauze
    else:
        stilstaan += 0
        
DPRU = DRU + onbeladen_rit + stilstaan
DD = DPRU/DRU

## wat je terug kan leveren
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

minimale_bussen = 8
maximale_bussen = 20
kwaliteit_bussen = ((maximale_bussen-aantal_bussen)/(maximale_bussen-minimale_bussen))*100

minimale_DDs = 1.3
maximale_DDs = 1.8
kwaliteit_DDs = ((maximale_DDs-DD)/(maximale_DDs-minimale_DDs))*100

minimale_DPRUs = 5234
maximale_DPRUs = 28800
kwaliteit_DPRUs = ((maximale_DPRUs-DPRU)/(maximale_DPRUs-minimale_DPRUs))*100

minimale_verbruik = 0
maximale_verbruik = 283.5*aantal_bussen
kwaliteit_verbruik = ((totaal_terugleveren)/(maximale_verbruik-minimale_verbruik))*100

st.markdown('<p style="font-family:sans-serif; color:black; font-size: 13px;">Wens 1: Aantal bussen die worden gebruikt.</p>', unsafe_allow_html=True)
st.caption(f'kwaliteit= {kwaliteit_bussen:.1f}%')
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 13px;">Wens 2: Aantal DPRUs wat word gereden.</p>', unsafe_allow_html=True)
st.caption(f'kwaliteit= {kwaliteit_DPRUs:.1f}%')
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 13px;">Wens 3: Verhouding tussen DPRUs en DRUs (ook wel DDs).</p>', unsafe_allow_html=True)
st.caption(f'kwaliteit= {kwaliteit_DDs:.1f}%')
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 13px;">Wens 4: Aantal verbruik wat terug geleverd kan worden in de ochtend.</p>', unsafe_allow_html=True)
st.caption(f'kwaliteit= {kwaliteit_verbruik:.1f}%')

kwaliteit_planning = (kwaliteit_bussen*st.session_state.belang_wens1 + kwaliteit_DDs*st.session_state.belang_wens3 + kwaliteit_DPRUs*st.session_state.belang_wens2 + kwaliteit_verbruik*st.session_state.belang_wens4)/(st.session_state.belang_wens1+st.session_state.belang_wens2+st.session_state.belang_wens3+st.session_state.belang_wens4)
st.subheader(f'kwaliteit planning totaal: {kwaliteit_planning:.1f}%')
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 13px;">In de totale kwaliteit zijn de belangen die u hiervoor heeft ingevuld meegerekend.</p>', unsafe_allow_html=True)
