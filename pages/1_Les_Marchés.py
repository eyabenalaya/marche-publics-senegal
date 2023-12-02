import streamlit as st
import plotly_express as px
from neo4j import GraphDatabase
import neo4j
import pandas as pd

# Établir une connexion à la base de données Neo4j
NEO4J_URI= "neo4j+s://b0a21d6c.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="OU2jdTE7c1ikO8ronSWOQdFlb-9Yj67C58-0ZZeJXU8"
AURA_INSTANCEID="b0a21d6c"
AURA_INSTANCENAME="Instance01"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

query_1 = """
Match (m:Marche)-[r:Vendu_par]-(n)
Return left(r.Date,4) AS Year, count(m.Titre) AS NbrMarche
"""
df_1 = driver.execute_query(
    query_1,
    result_transformer_=neo4j.Result.to_df
)

query_2 = """
Match (m:Marche)
Return m.Type AS Type, count(m.Titre) AS NbrMarche
"""
df_2 = driver.execute_query(
    query_2,
    result_transformer_=neo4j.Result.to_df
)

query_3 = """
Match (m:Marche)
Return m.Secteur AS Secteur, count(m.Titre) AS NbrMarche
"""
df_3 = driver.execute_query(
    query_3,
    result_transformer_=neo4j.Result.to_df
)

query_4 = """
MATCH (m:Marche)-[r]-(t:Titulaire)
RETURN r.Date AS Date, sum(r.Montant) AS Montant
"""
df_4 = driver.execute_query(
    query_4,
    result_transformer_=neo4j.Result.to_df
)
df_4['Date'] = pd.to_datetime(df_4['Date'])
df_4 = df_4.sort_values('Date', ascending=False)

driver.close()

st.title('Les Marchés Publics')
st.markdown('Nombre de marchés acquis par an')

annee = st.selectbox("Choisissez l'année", options=df_1['Year'])
i = df_1.index[df_1['Year'] == annee].tolist()
if i[0]>0:
    d = float(df_1['NbrMarche'][i[0]] - df_1['NbrMarche'][i[0]-1])
else : 
    d = 0

c1,c2,c3 = st.columns(3)

css='''
[data-testid="metric-container"] {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] > div {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] label {
    width: fit-content;
    margin: auto;
}
'''

c2.markdown(f'<style>{css}</style>',unsafe_allow_html=True)

with open ('style.css') as f:
			c2.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
c2.metric(label="Nombre d'Acquisitions", value = df_1['NbrMarche'][i], delta= d )

plot_1 = px.bar(df_1,
                x=df_1['Year'], 
                y=df_1['NbrMarche'],
                labels={'Year':'Année', 'NbrMarche':'Nombre de Marchés'}
                )
st.plotly_chart(plot_1)
st.markdown(f'__________________________________',unsafe_allow_html=True)
st.markdown('Répartitions des marchés public par types')

plot_2 = px.pie(df_2,
                names=df_2['Type'], 
                values=df_2['NbrMarche'],
                )
st.plotly_chart(plot_2)
st.markdown(f'__________________________________',unsafe_allow_html=True)

st.markdown("Secteurs d'activité des Marchés Publics")

plot_3 = px.bar(df_3,
                x=df_3['Secteur'], 
                y=df_3['NbrMarche'],
                labels={'Secteur':'Secteur', 'NbrMarche':'Nombre de Marchés'}
                )
st.plotly_chart(plot_3)

st.markdown(f'__________________________________',unsafe_allow_html=True)

st.markdown('Evolution des montant dépensés sur les marchés publics')

plot_4 = px.line(df_4,
                x="Date", 
                y="Montant",
                )
st.plotly_chart(plot_4)

st.markdown(f'__________________________________',unsafe_allow_html=True)
