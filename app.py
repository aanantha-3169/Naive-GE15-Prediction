# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 2022
@author: aanan
"""
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from PIL import Image

# headings
title = "Naive GE15 Prediction 🇲🇾"
st.title(title)

st.write("by  [Aanan](aananmariappan@gmail.com)")

#Sidebar
st.sidebar.title("Scenarios")
st.sidebar.write("See how the results change by changing the following:")

# user inputs on sidebar
S = st.sidebar.slider('% of PH votes in PRU14 contributed by Bersatu', value=1.0,min_value=0.0, max_value=1.0)

X = st.sidebar.slider('% of Undi 18 turnout', value=0.8,min_value=0.0, max_value=1.0)

#Content

st.header("*Why Undi 18 Matters!*")
st.markdown("This simple simulation aim to demonstrate how young voters can change the elections 😱"
" We use results from PRU 13 & 14 to calculate the contribution of each party to a coalition.")
image = Image.open('Timeline.jpeg')
st.image(image,caption='Evolution of Coalitions')

st.markdown("Note: For simplicity we are ignoring GTA 👴🏼 and Independents 🤠 for this analysis")

####################
### ANALYSIS ###
####################

#Reading Relevant Files
pru14_pm = pd.read_csv('keputusan-pru-14-parlimen_v2.csv')
pru13_pm = pd.read_csv('keputusan-pru-13-parlimen.csv')
LOKALITI_FINAL = pd.read_csv('undi_18_inputs.csv')

#Formatting Files
pru14_pm['BILANGAN UNDI'] = pru14_pm['BILANGAN UNDI'].apply(lambda x: x.replace(',',''))
pru14_pm['BILANGAN UNDI'] = pd.to_numeric(pru14_pm['BILANGAN UNDI'])

list_parties = ['MIC','UMNO','MCA','GERAKAN','PPP','BN','PKR','DAP','PAS']
pru13_pm = pru13_pm[pru13_pm.PARTI.isin(list_parties)]
pru14_pm = pru14_pm[pru14_pm.PARTI.isin(list_parties)]

dict_party = {'MIC':'BN','UMNO':'BN','MCA':'BN','GERAKAN':'BN','PPP':'BN','PKR':'PH','PAS':'PN','IND':'BEBAS'
              ,'BERJASA':'BERJASA','BERSAMA':'BERSAMA','KITA':'KITA','PCM':'PCM','DAP':'PH','BN':'BN','BEBAS':'BEBAS'
             ,'PRM':'PRM','MU':'MU','PFP':'PFP'}

pru13_pm['PARTI'] = pru13_pm.PARTI.apply(lambda x : dict_party[x])
pru14_pm['PARTI'] = pru14_pm.PARTI.apply(lambda x : dict_party[x])

####################
### Prediction ###
####################
list_winner = []
df_percent = pd.DataFrame(columns = ['LOKALITI','PARTI','PERCENT_VOTES'])

list_LOKALITI = []
for state in pru14_pm.NEGERI.unique():
    for lokal in pru14_pm[pru14_pm.NEGERI == state].LOKALITI.unique():
     list_LOKALITI += [(state,lokal)]

for state,lok in list_LOKALITI:
    
 #Get dataframe with PRU13 and PRU14 numbers for each lokaliti   
 pru_14 = pru14_pm[pru14_pm.LOKALITI == lok]
 pru_13 = pru13_pm[pru13_pm.LOKALITI == lok]
 
    
 #Create dataframe to capture results from PRU13 & PRU14   
 dict_df = {'PARTI':['BN','PN','PH','BERSATU']}

 df_pred = pd.DataFrame(dict_df)
    
 df_pred_v2 = df_pred.merge(pru_13,on = 'PARTI',how = 'left').merge(pru_14,on = 'PARTI',how = 'left')
 df_pred_v2 = df_pred_v2[['PARTI','BILANGAN UNDI_x','BILANGAN UNDI_y']]
 df_pred_v2 = df_pred_v2.fillna(0)

 PRU13_sum = df_pred_v2['BILANGAN UNDI_x'].sum()
 PRU14_sum = df_pred_v2['BILANGAN UNDI_y'].sum()
 
 #Normalize PRU14 results based on PRU13 turnout
 df_pred_v2['BILANGAN UNDI_y_x'] = df_pred_v2.apply(lambda x: round((x['BILANGAN UNDI_y']/PRU14_sum)*PRU13_sum),axis = 1)
 
 #Get expected number of votes by each party

 TOTAL = df_pred_v2['BILANGAN UNDI_x'].sum()
    
 BERSATU = (df_pred_v2[df_pred_v2.PARTI == 'BN']['BILANGAN UNDI_x'][0] - df_pred_v2[df_pred_v2.PARTI == 'BN']['BILANGAN UNDI_y_x'][0])*S
 
 if BERSATU > 0:
    PN_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'PN']['BILANGAN UNDI_y_x'][1] + BERSATU
    
 else:
    PN_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'PN']['BILANGAN UNDI_y_x'][1]
    
 if BERSATU > 0:
    PH_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'PH']['BILANGAN UNDI_y_x'][2] - BERSATU
    
 else:
    PH_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'PH']['BILANGAN UNDI_y_x'][2]

 BN_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'BN']['BILANGAN UNDI_y_x'][0] 
 
 #Get % of voter by party
 PN_PRU15_percent = round(PN_PRU15/TOTAL,2)
 BN_PRU15_percent = round(BN_PRU15/TOTAL,2)
 PH_PRU15_percent = round(PH_PRU15/TOTAL,2)
 
 dict_results_percent = {'BN':BN_PRU15_percent,'PN':PN_PRU15_percent,'PH':PH_PRU15_percent}
 
 #Create dataframe with % of votes by party
 df_pred_v2['PERCENT_VOTES'] = df_pred_v2['PARTI'].apply(lambda x: dict_results_percent[x] if x != 'BERSATU' else 0)
 df_pred_v2['LOKALITI'] = lok
 df_pred_v3 = df_pred_v2[['LOKALITI','PARTI','PERCENT_VOTES']]

 frame = [df_percent,df_pred_v3]
 df_percent = pd.concat(frame)

 #Identify winner and create dataframe   
 dict_results_inverse = {BN_PRU15: 'BN',PN_PRU15:'PN',PH_PRU15:'PH'}
 
 winner = dict_results_inverse[max(dict_results_inverse)]
 
 list_votes = [i for i in dict_results_inverse.keys()]

 list_votes.sort()
 
 #Calculate margin of victory   
 margin = round(((list_votes[2] - list_votes[1]) / TOTAL),2)

 if margin > 100:
        print(lok)
 list_winner += [[state,lok,winner,margin]]

#Create dataframe of results
pru15_pm_pred = pd.DataFrame(list_winner,columns = ['STATE','LOKALITI','WINNER','MARGIN'])
pru15_pm_pred_sum = pru15_pm_pred.groupby('WINNER').LOKALITI.count().reset_index()


max_value = pru15_pm_pred_sum.LOKALITI.max()
df_winner = pru15_pm_pred_sum[pru15_pm_pred_sum.LOKALITI == max_value]['WINNER'].reset_index()
winner_name = df_winner['WINNER'][0]


if winner_name == 'PH':
    st.subheader("The winner is Pakatan Harapan!")

elif winner_name == 'BN':
    st.subheader("The winner is Barisan Nasional!")
    
elif winner_name == 'PN':
    st.subheader("The winner is Perikatan Nasional!")


####################
### Charts ###
####################
domains = ['PH', 'BN', 'PN']

color_scale = alt.Scale(
    domain=domains,
    range=['rgb(255,0,0)', 'rgb(0,128,255)', 'rgb(0,255,0)']
)

#Chart of overall results
chart_1 = alt.Chart(pru15_pm_pred_sum).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="LOKALITI", type="quantitative"),
    color=alt.Color('WINNER:N', legend=None, scale=color_scale),
    tooltip = [alt.Tooltip('WINNER:N'),
               alt.Tooltip('LOKALITI:Q')]
) 

st.altair_chart(chart_1, use_container_width=True)

#Chart to filter by State

st.subheader("State Level Results")
st.markdown("Keep an eye for constituencies with small margin of victory, anything can happen 😰")

source = pru15_pm_pred
all_symbols = pru15_pm_pred.STATE.unique()
symbols = st.multiselect("Choose a State(Hover on points for details)", all_symbols, all_symbols[:3])
source = source[source.STATE.isin(symbols)]

chart_2 = alt.Chart(source).mark_point(filled=True, opacity=1, size=100).encode(
    alt.X('x:O', axis=None),
    alt.Y('WINNER:O', axis=None),
    alt.Row('STATE:N', header=alt.Header(title='')),
    #alt.Shape('animal:N', legend=None, scale=shape_scale),
    alt.Color('WINNER:N', legend=None, scale=color_scale),
    tooltip = [alt.Tooltip('LOKALITI:N'),
               alt.Tooltip('WINNER:N'),
               alt.Tooltip('MARGIN:Q')
              ]
).transform_window(
    x='rank()',
    groupby=['STATE', 'WINNER']
).properties(width=550, height=140)

st.altair_chart(chart_2, use_container_width=True)
