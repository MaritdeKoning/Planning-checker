# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 20:19:19 2022

@author: Petra
"""
#Import en pagina netjes maken
import streamlit as st
import pandas as pd
import math
from math import isnan
import time
from datetime import datetime
import datetime
import numpy as np
import time as t

st.header('Controle')

#Data inlezen
data = pd.read_excel(st.session_state.uploaded_file)
ritten = pd.read_excel(r'Connexxion data - 2022-2023.xlsx')

## Controle of alle busritten gereden worden.
dienst = data.Dienst
counter0 = 0
for i in range(len(data)):
    if dienst[i] == 'Dienstrit':
        counter0 += 1

ritten = ritten.values.tolist()
counter1 = len([a[3] for a in ritten])

st.markdown('---')
#printen van de eis
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 22px;">1.Controle eis: Alle diensten moeten worden gereden.</p>', unsafe_allow_html=True)
tekst1 = f'Het aantal busdiensten die gereden moeten worden zijn er: {counter1}.'
tekst2 = f'Het aantal busdiensten die werkelijk ingepland zijn er: {counter0}.'
st.caption(tekst1)
st.caption(tekst2)
title_goed = '<p style="font-family:sans-serif; color:Green; font-size: 18px;">Er wordt voldaan aan deze eis</p>'
title_fout = '<p style="font-family:sans-serif; color:Red; font-size: 18px;">Er wordt niet voldaan aan deze eis</p>'

if counter0 == counter1:
    st.markdown(title_goed, unsafe_allow_html=True)
else: 
    st.markdown(title_fout, unsafe_allow_html=True)
st.markdown('---')    

#Controle: De bus moet op het juiste startpunt aanwezig zijn als hij moet gaan rijden
## Een bus kan niet meerdere routes tegelijk rijden

st.markdown('<p style="font-family:sans-serif; color:black; font-size: 22px;">2.Controle eis: Een busdienst kan niet meerdere routes tegelijk rijden.</p>', unsafe_allow_html=True)
counter = 0
for i in range(1,len(data)):
    eindtijd = data['Aankomst'][i-1]
    starttijd = data['Vertrek'][i]
    bl = data['Buslijn'][i]
    if isnan(bl):
        if eindtijd > starttijd and data['Bus'][i]==data['Bus'][i-1]:
            st.caption(f'Bij bus {data.Bus[i]} die om {data.Vertrek[i]} vertrekt is de eindtijd = {eindtijd} en starttijd = {starttijd}')
            counter += 1

#printen van de eis
if counter == 0:
    st.caption('Een busdienst rijdt niet meerdere routes tegelijk')
    st.markdown(title_goed, unsafe_allow_html=True)
else: 
    st.markdown(title_fout, unsafe_allow_html=True)
st.markdown('---')    
    
## De bus moet op het juiste startpunt aanwezig zijn als hij moet gaan rijden

st.markdown('<p style="font-family:sans-serif; color:black; font-size: 22px;">3.Controle eis: Een bus moet op het juiste startpunt aanwezig zijn als deze gaat rijden.</p>', unsafe_allow_html=True)
counter2 = 0
for i in range(1,len(data)):
    eindlocatie = data['Eindlocatie'][i-1]
    startlocatie = data['Startlocatie'][i]
    if eindlocatie != startlocatie:
        counter2 += 1
        st.caption(f'Bij bus {data.Bus[i]} die om {data.Vertrek[i]} vertrekt is de eindlocatie = {eindlocatie} en startlocatie = {startlocatie}')

if counter2 == 0:
    st.caption('Een bus start altijd op het juiste startpunt')
    st.markdown(title_goed, unsafe_allow_html=True)
else: 
    st.markdown(title_fout, unsafe_allow_html=True)
st.markdown('---')

## Minimaal 15 minuten aan de oplader liggen

st.markdown('<p style="font-family:sans-serif; color:black; font-size: 22px;">4.Controle eis: Een bus moet minimaal 15 minuten aan de oplader liggen.</p>', unsafe_allow_html=True)
def calcTime(enter,exit):
    format="%H:%M:%S"
    #Parsing the time to str and taking only the hour,minute,second 
    #(without miliseconds)
    enterStr = str(enter).split(".")[0]
    exitStr = str(exit).split(".")[0]
    #Creating enter and exit time objects from str in the format (H:M:S)
    enterTime = datetime.strptime(enterStr, format)
    exitTime = datetime.strptime(exitStr, format)
    return exitTime - enterTime

counter3=0
counter4=0
for i in range(len(data)):
    if data.Buslijn[i] == 'Opladen':
        duration = calcTime(data.Vertrek[i],data.Aankomst[i])
        if str(duration) > '00:15:00':
            counter3+=1
        else:
            counter4+=1
            st.markdown(f'Bij bus {data.Bus[i]} die om {data.Vertrek[i]} vertrekt wordt er minder dan 15 minuten opgeladen: {duration}')
            
if counter4 == 0:
    st.caption('De bussen laden nooit korter op dan 15 minuten')
    st.markdown(title_goed, unsafe_allow_html=True)
else: 
    st.markdown(title_fout, unsafe_allow_html=True)
st.markdown('---')
    
## minimale en maximale reistijd
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 22px;">5.Controle eis: Lengte rit moet voldoen aan minimum en maximum tijd.</p>', unsafe_allow_html=True)
for i in range(len(data)):
    if data.Dienst[i] == 'Dienstrit':
        data.Dienst[i] = int(data.Buslijn[i])
        
#Dictionary met tijden aanmaken

reistijd = {
    400             : {"min"      : {"Eindhoven airport" : {"Eindhoven busstation"   : 22.0},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 22.0}},
                       "max"      : {"Eindhoven airport" : {"Eindhoven busstation"   : 24.0},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 24.0}}},
    401             : {"min"      : {"Eindhoven airport" : {"Eindhoven busstation"   : 22.0},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 22.0}},
                       "max"      : {"Eindhoven airport" : {"Eindhoven busstation"   : 25.0},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 24.0}}},
    "Materiaal rit" : {"min"      : {"Eindhoven airport" : {"Eindhoven busstation"   : 20.0,
                                                              "Eindhoven garage"     : 20.0},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 20.0,
                                                                 "Eindhoven garage"  : 4.0},
                                       "Eindhoven garage" : {"Eindhoven airport"     : 20.0,
                                                             "Eindhoven busstation"  : 4.0}},
                      "max"       : {"Eindhoven airport" : {"Eindhoven busstation"   : 20.0,
                                                              "Eindhoven garage"     : 20.0},
                                       "Eindhoven busstation" : {"Eindhoven airport" : 20.0,
                                                                 "Eindhoven garage"  : 4.0},
                                       "Eindhoven garage" : {"Eindhoven airport"     : 20.0,
                                                             "Eindhoven busstation"  : 4.0}}},
    "Opladen"      : {"min"       : {"Eindhoven garage" : {"Eindhoven garage"        : 15.0}},
                      "max"       : {"Eindhoven garage" : {"Eindhoven garage"        : 120.0}}}
}

#Lengte ritten berekenen

lengte_rit = []

for i in range(len(data)):
    a = data.Vertrek[i]
    b = data.Aankomst[i]
    da = datetime.timedelta(hours = a.hour, minutes = a.minute, seconds = a.second)
    db = datetime.timedelta(hours = b.hour, minutes = b.minute, seconds = b.second)

    lengte_rit.append(((db-da).seconds)/60)
    
#Checken of de rittijden kloppen
counter6 = 0
for i in range(len(data)):
    if lengte_rit[i] >= reistijd[data.Dienst[i]]['min'][data.Startlocatie[i]][data.Eindlocatie[i]] and lengte_rit[i] <= reistijd[data.Dienst[i]]['max'][data.Startlocatie[i]][data.Eindlocatie[i]]:
        pass
    else:
        counter6 += 1
        st.caption(f'Bij bus {data.Bus[i]} die om {data.Vertrek[i]} vertrekt is de lengte van de rit: {lengte_rit[i]} minuten en dus niet goed.')
        
if counter6 == 0:
    st.caption('De lengte van de ritten van de bussen zijn goed')
    st.markdown(title_goed, unsafe_allow_html=True)
else:
    st.markdown(title_fout, unsafe_allow_html=True)
st.markdown('---')

## SOC waarde mag niet onder en boven een bepaalde waarde komen
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 22px;">6.Controle eis: Soc-waarde mag niet te laag of te hoog worden.</p>', unsafe_allow_html=True)

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

# Gegeven waarden

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
counter5 = 0

for i in range(len(data)):
    #batterijwaarde_bus[data.Bus[i]-1]
    batterijwaarde_bus[data.Bus[i]-1] -= ritten[data.Dienst[i]][data.Spits[i]][data.Startlocatie[i]][data.Eindlocatie[i]]
    if data.Dienst[i] == 'Opladen':
        batterijwaarde_bus[data.Bus[i]-1] += (lengte_rit[i]*opladen_per_min)
        if batterijwaarde_bus[data.Bus[i]-1] > soc_max:
            st.caption(f'Bij bus {data.Bus[i]} die om {data.Vertrek[i]} vertrekt is de soc-waarde: {batterijwaarde_bus[data.Bus[i]-1]:.2f}, en is dus te hoog.')
            counter5 += 1
    if batterijwaarde_bus[data.Bus[i]-1] < soc_min:         
        st.caption(f'Bij bus {data.Bus[i]} die om {data.Vertrek[i]} vertrekt is de soc-waarde: {batterijwaarde_bus[data.Bus[i]-1]:.2f}, en is dus te laag.')
        counter5 += 1
        
if counter5 == 0:
    st.caption('De soc-waarde van de bus is nooit te laag of te hoog')
    st.markdown(title_goed, unsafe_allow_html=True)
else:
    st.markdown(title_fout, unsafe_allow_html=True)
st.markdown('---')
