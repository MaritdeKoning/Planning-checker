# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 10:56:30 2022

@author: Petra
"""

import streamlit as st
from PIL import Image

st.header('Welkom')

st.text('Op deze website kunt U busplanningen checken hier krijgt U er een overzichtelijk \nrooster bij. Hieronder in de afbeelding kunt U zien welke route de bussen door \nEindhoven rijden.')

image1 = Image.open(r'Busritten kaart.png')
st.image(image1, caption='Busrit 400 en busrit 401', width = 600, output_format= 'PNG')

