import streamlit as st
from neo4j import GraphDatabase, Result
import pandas as pd

css='''
/* Centering text in each gray box */
div.css-1ht1j8u.e16fv1kl0 {
  text-align: center;
}

/* Row 1 */
div.css-1r6slb0.e1tzin5v2 {
    background-color: rgb(63, 79, 107);
    padding: 3% 3% 3% 3%;
    border-radius: 5px;
}

/* Row 2 */
div.css-12w0qpk.e1tzin5v2 {
    background-color: rgba(220, 220, 220, 0.60);
    padding: 3% 3% 3% 3%;
    border-radius: 5px;
}
div.css-dm3ece.everg990{

}
'''

st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)

# Établir une connexion à la base de données Neo4j
NEO4J_URI = "neo4j+s://b0a21d6c.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "OU2jdTE7c1ikO8ronSWOQdFlb-9Yj67C58-0ZZeJXU8"
AURA_INSTANCEID = "b0a21d6c"
AURA_INSTANCENAME = "Instance01"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

query_1 = """
MATCH (m:Marche)
WHERE m.Secteur ="Santé"
RETURN count(m.Titre) AS NbrMarche 
"""

with driver.session() as session:
    result: Result = session.run(query_1)
    records = result.data()

st.title('Les Indicateurs de Performance Clés')
st.write('Nombre de marchés publics par domaine')
c1,c2,c3 = st.columns(3)


# Assurez-vous que records n'est pas vide avant d'accéder à la première ligne
if records:
    df_1 = pd.DataFrame(records)
    NbrMarche = df_1['NbrMarche'][0]
    c1.metric('Santé',NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")
query_2 = """
MATCH (m:Marche)
WHERE m.Secteur ="Pétrole et Energies"
RETURN count(m.Titre) AS NbrMarche 
"""

with driver.session() as session:
    result: Result = session.run(query_2)
    records_2 = result.data()

if records_2:
    df_2 = pd.DataFrame(records_2)
    NbrMarche = df_2['NbrMarche'][0]
    c2.metric("Pétrole et Energies",NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")

query_3 = """
MATCH (m:Marche)
WHERE m.Secteur ="Education et Recherche"
RETURN count(m.Titre) AS NbrMarche 
"""

with driver.session() as session:
    result: Result = session.run(query_3)
    records_3 = result.data()

if records_3:
    df_3 = pd.DataFrame(records_3)
    NbrMarche = df_3['NbrMarche'][0]
    c3.metric("Education et Recherche",NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")
s1,s2,s3 = st.columns(3)

query_4 = """
MATCH (m:Marche)
WHERE m.Secteur ="Justice"
RETURN count(m.Titre) AS NbrMarche 
"""

with driver.session() as session:
    result: Result = session.run(query_4)
    records_4 = result.data()

if records_4:
    df_4 = pd.DataFrame(records_4)
    NbrMarche = df_4['NbrMarche'][0]
    s1.metric("Justice",NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")

query_5 = """
MATCH (m:Marche)
WHERE m.Secteur = "Mines et de la Géologie"
RETURN count(m.Titre) AS NbrMarche 
"""

with driver.session() as session:
    result: Result = session.run(query_5)
    records_5 = result.data()

if records_5:
    df_5 = pd.DataFrame(records_5)
    NbrMarche = df_5['NbrMarche'][0]
    s2.metric("Mines et de la Géologie",NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")


query_6 = """
MATCH (m:Marche)
WHERE m.Secteur = "Urbanisme, Habitat et Hygiène"
RETURN count(m.Titre) AS NbrMarche 
"""

with driver.session() as session:
    result: Result = session.run(query_6)
    records_6 = result.data()

if records_6:
    df_6 = pd.DataFrame(records_6)
    NbrMarche = df_6['NbrMarche'][0]
    s3.metric("Urbanisme, Habitat et Hygiène",NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")


# ___________________________________________________________________________________________________________

st.write('Nombre de marchés')
c1,c2,c3 = st.columns(3)

query_1_1 = """
match (m:Marche)-[r]-(a:Autorite_Contractante) return count(m) AS NbrMarche
"""

with driver.session() as session:
    result: Result = session.run(query_1_1)
    records_1_1 = result.data()

if records_1_1:
    df_1_1 = pd.DataFrame(records)
    NbrMarche = df_1_1['NbrMarche'][0]
    c2.metric('Avec avenant',NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")

query_1_2 = """
MATCH (m:Marche)
RETURN count(m) AS NbrMarche 
"""

with driver.session() as session:
    result: Result = session.run(query_1_2)
    records_1_2 = result.data()

if records_1_2:
    df_1_2 = pd.DataFrame(records_1_2)
    NbrMarche = df_1_2['NbrMarche'][0]
    c1.metric("Total",NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")

query_1_3 = """
MATCH (m:Marche)
RETURN count(m) AS NbrMarche 
"""

with driver.session() as session:
    result: Result = session.run(query_1_3)
    records_1_3 = result.data()

if records_1_3:
    df_1_3 = pd.DataFrame(records_1_3)
    NbrMarche = df_1_3['NbrMarche'][0]-df_1_1['NbrMarche'][0]
    c3.metric("Sans Avenant",NbrMarche)
else:
    st.warning("Aucun résultat trouvé pour la requête.")


query_3_1 = """
Match (m:Marche)-[r:Vendu_par]-(n)
Return left(r.Date,4) AS Year, count(m.Titre) AS NbrMarche
"""

with driver.session() as session:
    result: Result = session.run(query_3_1)
    records_3_1 = result.data()
st.write("Cumul du nombre de marchés par an")
if records_3_1:
    df_3_1 = pd.DataFrame(records_3_1)
    df_3_1 = df_3_1.sort_values('Year')
    df = df_3_1.set_index('Year').cumsum()
    st.line_chart(df)

else:
    st.warning("Aucun résultat trouvé pour la requête.")

