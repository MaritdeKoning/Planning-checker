# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:34:47 2022

@author: Petra
"""
#Imports
import streamlit as st
import pandas as pd

st.header('Input data')

st.markdown('---')
st.text('Vul als eerste hier de data van de dienstregeling in:')
st.session_state.uploaded_data = st.file_uploader("Kies de data van de dienstregeling", type =['xlsx'])

if st.session_state.uploaded_data:
    dp = pd.read_excel(st.session_state.uploaded_data)
st.markdown('---')

#voorbeeld data
st.text('We willen dat de geleverde data er zo uit ziet (dit is een voorbeeld):\nAls U verder naar beneden scrollt kunt U de data voor de busritten invoeren')
data = pd.read_excel(r'voorbeeld.xlsx')
buslijn = data.Buslijn
for i in range(len(data)):
    if buslijn[i] == 400:
        buslijn[i] = str('400')
    elif buslijn[i] == 401:
        buslijn[i] = str('401')
    else:
        pass

starttijd = data.Vertrek
eindtijd = data.Aankomst
for i in range(len(data)):
    starttijd[i] = str(starttijd[i])
    eindtijd[i] = str(eindtijd[i])
    
st.markdown('---')
st.dataframe(data)
st.markdown('---')

#data invoeren
st.text('Hier kunt U de data voor de busritten invoeren:')
st.session_state.uploaded_file = st.file_uploader("Kies een bestand", type =['xlsx'])

if st.session_state.uploaded_file:
    df = pd.read_excel(st.session_state.uploaded_file)
