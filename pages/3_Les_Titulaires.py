import streamlit as st
import plotly_express as px
from neo4j import GraphDatabase
import neo4j

# Établir une connexion à la base de données Neo4j
NEO4J_URI= "neo4j+s://b0a21d6c.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="OU2jdTE7c1ikO8ronSWOQdFlb-9Yj67C58-0ZZeJXU8"
AURA_INSTANCEID="b0a21d6c"
AURA_INSTANCENAME="Instance01"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

query_1 = """
MATCH (m:Marche)-[v]-(A:Titulaire)
RETURN A.Nom AS AutCont, count(m.Titre) AS nbrMarche
"""
df_1 = driver.execute_query(
    query_1,
    result_transformer_=neo4j.Result.to_df
)
df_1 = df_1.sort_values('nbrMarche', ascending=False)
df_1 = df_1.head()

query_2 = """
MATCH (m:Marche)-[r]-(a:Titulaire)
RETURN a.Nom AS Autorite, sum(r.Montant) AS Montant
"""
df_2 = driver.execute_query(
    query_2,
    result_transformer_=neo4j.Result.to_df
)
df_2 = df_2.sort_values('Montant', ascending=False)
df_2 = df_2.head()

driver.close()


st.title('Les Titulaires')

st.markdown("Top 5 des Autorités avec le plus de contrats")

plot_1 = px.funnel(df_1,
                x=df_1['AutCont'], 
                y=df_1['nbrMarche'],
                labels={'AutCont':'Titulaires', 'nbrMarche':'Nombre de Marchés'}
                )
st.plotly_chart(plot_1)

st.markdown(f'__________________________________',unsafe_allow_html=True)

st.markdown("Top 5 des Titulaire avec le plus montants dépensés pour l'acquisition des marchés publics")

plot_2 = px.funnel(df_2,
                x=df_2['Autorite'], 
                y=df_2['Montant'],
                labels={'Autorite':'Autorité Contractante', 'Montant':'Nombre de Marchés'}
                )
st.plotly_chart(plot_2)

st.markdown(f'__________________________________',unsafe_allow_html=True)
