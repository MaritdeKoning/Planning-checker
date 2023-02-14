# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:40:28 2022

@author: Petra
"""
import streamlit as st
st.header('Belang wensen')
st.subheader('Bepaal hier hoe belangerijk u de wensen voor de planning vind op een schaal van 1 tot 10')

#alle eisen op een rijtje
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 18px;">Wens 1: Aantal bussen die worden gebruikt voor de planning.</p>', unsafe_allow_html=True)
st.session_state.belang_wens1 = st.number_input('Belang wens 1', min_value = 1, max_value = 10)
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 18px;">Wens 2: Aantal DPRUs wat word gereden door alle bussen samen.</p>', unsafe_allow_html=True)
st.session_state.belang_wens2 = st.number_input('Belang wens 2', min_value = 1, max_value = 10)
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 18px;">Wens 3: Verhouding tussen DPRUs en DRUs (ook wel DDs).</p>', unsafe_allow_html=True)
st.session_state.belang_wens3 = st.number_input('Belang wens 3', min_value = 1, max_value = 10)
st.markdown('<p style="font-family:sans-serif; color:black; font-size: 18px;">Wens 4: Aantal verbruik wat terug geleverd kan worden in de ochtend.</p>', unsafe_allow_html=True)
st.session_state.belang_wens4 = st.number_input('Belang wens 4', min_value = 1, max_value = 10)

