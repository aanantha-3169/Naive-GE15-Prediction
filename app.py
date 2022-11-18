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
@st.cache(allow_output_mutation=True)
def Pageviews():
    return []

pageviews=Pageviews()
pageviews.append('dummy')
# headings
title = "Naive GE15 Prediction 🇲🇾"
st.title(title)

st.write("source code: (https://github.com/aanantha-3169)")

#Content

st.header("*What can history tell us?*")
st.markdown("![Alt Text](https://media.giphy.com/media/ue5ZwFCaxy64M/giphy.gif)")
st.markdown('##')

st.markdown("Let's use results from PRU 13 & 14 to calculate the contribution of each party and make a prediction for PRU15 🤩")
st.markdown('##')
st.header("*What about the young voters?*")
st.markdown("![Alt Text](https://media.giphy.com/media/JTzPN5kkobFv7X0zPJ/giphy.gif)")
st.markdown('##')
st.markdown(" For all the youths out there wondering if you should vote, play around with the turnout of youngest to see how you can determine the future of this country!!!")
st.markdown('##')

st.markdown("Note: This analysis is simply using past results to predict the future and only looks at the 3 big coalition; BN 🔵,PN ⚫ and PH 🔴."
           )

#Sidebar
st.title("Scenarios ")
st.write("See how the results change by changing the following:")

# user inputs on sidebar
S = st.slider("How much do you think the ex BN folks(Bersatu) contributed to PH's victory in PRU14?(%)", value=100,min_value=0, max_value=100)
S = S/100
X = st.slider('What do you think will be the turnout of 18 - 21 year olds(%)?', value=80,min_value=0, max_value=100)
X = X/100
A = st.slider('How many 18 - 21 year olds do you think support BN (%) 🔵', value=38,min_value=0, max_value=100)

B = st.slider('How many 18 - 21 year olds do you think support PN (%) ⚫', value=21,min_value=0, max_value=100)

if A > 0 and B > 0:
 C = st.slider('How many 18 - 21 year olds do you think support PH (%) 🔴', value=100 - A - B,min_value=0, max_value=100)

else:
 C = st.slider('How many 18 - 21 year olds do you think support PH (%) 🔴', value=41,min_value=0, max_value=100)

if A+B+C == 100:
   pass

else:
 st.warning('Total Undi 18 votes must add up to 100% 🥴. Change values and try again', icon="⚠️")

A = A/100
B = B/100
C = C/100

####################
### ANALYSIS ###
####################

#Reading Relevant Files
#    Sources: 1)https://github.com/TindakMalaysia/General-Election-Data & https://undi.info/ --> Election results
#             2)https://www.data.gov.my/data/en_US/organization/election-commission-of-malaysia-spr?res_format=CSV --> Voter turnout
#             3)https://github.com/Thevesh/analysis-election-msia --> % Voters 18 - 21 years old """ 

pru14_pm = pd.read_csv('keputusan-pru-14-parlimen_v2.csv')
pru13_pm = pd.read_csv('keputusan-pru-13-parlimen.csv')
undi18_inputs = pd.read_csv('undi_18_inputs.csv')

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

list_LOKALITI = []
for state in pru14_pm.NEGERI.unique():
    for lokal in pru14_pm[pru14_pm.NEGERI == state].LOKALITI.unique():
     list_LOKALITI += [(state,lokal)]
####################
### Prediction ###
####################
list_winner = []
for state,lok in list_LOKALITI:
    
 #Get dataframe with PRU13 and PRU14 numbers for each lokaliti   
 pru_14 = pru14_pm[pru14_pm.LOKALITI == lok]
 pru_13 = pru13_pm[pru13_pm.LOKALITI == lok]
 
 #Get total number of voters and voter turnout
 undi_biasa_turnout = undi18_inputs[undi18_inputs.LOKALITI == lok]['undi_biasa_turnout'].unique()[0]
 undi_18_turnout = X
 undi_18 = undi18_inputs[undi18_inputs.LOKALITI == lok]['undi_18'].unique()[0]
 undi_biasa = undi18_inputs[undi18_inputs.LOKALITI == lok]['undi_biasa'].unique()[0]
 
 undi_18_attend = (undi_18 * undi_18_turnout)
 undi_biasa_attend = (undi_biasa*undi_biasa_turnout)
    
 total_attend = round((undi_18_attend + undi_biasa_attend))

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

 TOTAL_NORM = df_pred_v2['BILANGAN UNDI_x'].sum()
    
 BERSATU = (df_pred_v2[df_pred_v2.PARTI == 'BN']['BILANGAN UNDI_x'][0] - df_pred_v2[df_pred_v2.PARTI == 'BN']['BILANGAN UNDI_y_x'][0]) * S
 
 if BERSATU > 0:
    PN_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'PN']['BILANGAN UNDI_y_x'][1] + BERSATU
    
 else:
    PN_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'PN']['BILANGAN UNDI_y_x'][1]
    
 if BERSATU > 0:
    PH_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'PH']['BILANGAN UNDI_y_x'][2] - BERSATU
    
 else:
    PH_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'PH']['BILANGAN UNDI_y_x'][2]

 BN_PRU15 = df_pred_v2[df_pred_v2.PARTI == 'BN']['BILANGAN UNDI_y_x'][0] 
 
 #Get % of undi biasa voters
 PN_undi_biasa_PRU15_percent = round((PN_PRU15/TOTAL_NORM),2)
 BN_undi_biasa_PRU15_percent = round((BN_PRU15/TOTAL_NORM),2)
 PH_undi_biasa_PRU15_percent = round((PH_PRU15/TOTAL_NORM),2)
    
 #Get % of Undi18 voters
 PN_Undi18_PRU15_percent = B
 BN_Undi18_PRU15_percent = A
 PH_Undi18_PRU15_percent = C
    
 #Get % total voters
 PN_PRU15_final_percent = round(((PN_Undi18_PRU15_percent*undi_18_attend) + (PN_undi_biasa_PRU15_percent*undi_biasa_attend))/total_attend,2)
 BN_PRU15_final_percent = round(((BN_Undi18_PRU15_percent*undi_18_attend) + (BN_undi_biasa_PRU15_percent*undi_biasa_attend))/total_attend,2)
 PH_PRU15_final_percent = round(((PH_Undi18_PRU15_percent*undi_18_attend) + (PH_undi_biasa_PRU15_percent*undi_biasa_attend))/total_attend,2)
 
 dict_results_percent = {'BN':BN_PRU15_final_percent,'PN':PN_PRU15_final_percent,'PH':PH_PRU15_final_percent}
 
 #Identify winner and create dataframe 
 max_precent = max(dict_results_percent.values())
 max_keys = [k for k, v in dict_results_percent.items() if v == max_precent]
 winner = max_keys[0]

 list_votes = list(dict_results_percent.values())

 list_votes.sort()
 
 #Calculate margin of victory   
 margin = list_votes[2] - list_votes[1]

 if margin > 1:
        print(lok)
        
 list_winner += [[state,lok,winner,margin]]

#Create dataframe of results
pru15_pm_pred = pd.DataFrame(list_winner,columns = ['STATE','CONSTITUENCY','WINNER','MARGIN'])
pru15_pm_pred_sum = pru15_pm_pred.groupby('WINNER').agg(TOTAL =('CONSTITUENCY', 'count')).reset_index()
pru15_pm_pred_sum['PRECENT_TOTAL'] = pru15_pm_pred_sum.TOTAL.apply(lambda x: str(round((x/165) * 100)) + '%')
pru15_pm_pred_sum['FINAL_RESULT'] = pru15_pm_pred_sum.apply(lambda x: str(x.WINNER) + ' ' + str(x.PRECENT_TOTAL),axis = 1)

max_value = pru15_pm_pred_sum.TOTAL.max()
df_winner = pru15_pm_pred_sum[pru15_pm_pred_sum.TOTAL == max_value]['WINNER'].reset_index()
final_results = list(df_winner['WINNER'])
winner_name = df_winner['WINNER'][0]


if len(final_results) == 1:
    winning_party = final_results[0]
    st.subheader("The leader in Peninsular Malaysia is " +  winning_party + " 🥳!. They can lead the negotiations to form government")

elif len(final_results) > 1:
    st.subheader("It's a tie in Peninsular Malaysia 😱!")


####################
### Charts ###
####################
domains = ['PH', 'BN', 'PN']

color_scale = alt.Scale(
    domain=domains,
    range=['rgb(255,0,0)', 'rgb(0,128,255)', 'rgb(128,128,128)']
)

#Chart of overall results
# chart_1 = alt.Chart(pru15_pm_pred_sum).mark_arc(innerRadius=50).encode(
#     theta=alt.Theta(field="LOKALITI", type="quantitative"),
#     color=alt.Color('WINNER:N', legend=None, scale=color_scale),
#     tooltip = [alt.Tooltip('WINNER:N'),
#                alt.Tooltip('LOKALITI:Q')]
# ) 
# text_1 = chart_1.mark_text(innerRadius=50, size=20).encode(text="WINNER:N")

# st.altair_chart(chart_1 + text_1, use_container_width=True)


base = alt.Chart(pru15_pm_pred_sum).encode(
    theta=alt.Theta("TOTAL:Q", stack=True),
     color=alt.Color("WINNER:N", legend=None, scale=color_scale),
     tooltip = [alt.Tooltip('TOTAL:Q')]
)

pie = base.mark_arc(outerRadius=110,innerRadius=50)
text = base.mark_text(radius=150, size=20).encode(text="FINAL_RESULT:N")

st.altair_chart(pie + text, use_container_width=True)
#Chart to filter by State

st.subheader("State Level Results")
st.markdown("Keep an eye for constituencies with a small margin of victory, anything can happen 😰")
st.markdown("![Alt Text](https://media.giphy.com/media/xT1XGvP9PArEBYcFcQ/giphy.gif)")
source = pru15_pm_pred
state_mapping = {'JH':'JOHOR','KD':'KEDAH','KE':'KELANTAN','MK':'MELAKA','NS':'NEGERI SEMBILAN','PH':'PAHANG','PR':'PERAK','PL':'PERLIS',
'PN':'PULAU PINANG','SB':'SABAH','SW':'SARAWAK','SL':'SELANGOR','TR':'TERENGGANU','WP':'WP KUALA LUMPUR','WP':'WP PUTRAJAYA'}
source['STATE'] = source['STATE'].apply(lambda x : state_mapping[x])
all_state = pru15_pm_pred.STATE.unique()

states = st.multiselect("Choose a State(Hover on points for details)", all_state, all_state[:3])
source = source[source.STATE.isin(states)]

chart_2 = alt.Chart(source).mark_point(filled=True, opacity=1, size=100).encode(
    alt.X('x:O', axis=None),
    alt.Y('WINNER:O', axis=None),
    alt.Row('STATE:N', header=alt.Header(title='')),
    #alt.Shape('animal:N', legend=None, scale=shape_scale),
    alt.Color('WINNER:N', legend=None, scale=color_scale),
    tooltip = [alt.Tooltip('CONSTITUENCY:N'),
               alt.Tooltip('WINNER:N'),
               alt.Tooltip('MARGIN:Q')
              ]
).transform_window(
    x='rank()',
    groupby=['STATE', 'WINNER']
).properties(width=550, height=140)

st.altair_chart(chart_2, use_container_width=True)

