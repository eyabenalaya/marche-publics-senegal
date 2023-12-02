import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from neo4j import GraphDatabase
from neo4j.graph import Node, Relationship
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots  # Import make_subplots function

import networkx as nx
from neo4j import GraphDatabase

# Se connecter à Neo4j
NEO4J_URI= "neo4j+s://b0a21d6c.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="OU2jdTE7c1ikO8ronSWOQdFlb-9Yj67C58-0ZZeJXU8"
AURA_INSTANCEID="b0a21d6c"
AURA_INSTANCENAME="Instance01"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


st.title('Graphe des Marchés Publics au Sénégal de 2008 à 2021')

# Fetch tous les titulaire
q_tit = """
MATCH (t:Titulaire) RETURN t.Nom AS Titulaire
"""
with driver.session() as session:
    result = session.run(q_tit)
    data_tit = result.data()
Tit = []
for t in data_tit :
    Tit.append(t['Titulaire'])

Titul = st.selectbox("Choisissez le titulaire", options=Tit)

#Query en fonction du titulaire
query = f"""
MATCH (n:Autorite_Contractante)-[r:Vendu_par]-(m:Marche)-[t:Beneficiaire_de]-(p:Titulaire)
WHERE p.Nom =  "{Titul}"  
RETURN n AS Autorite_Contractante, r AS Vendu_par, m AS Marche, t AS Beneficiaire_de, p AS Titulaire
LIMIT 10
"""
with driver.session() as session:
    result = session.run(query)
    data = result.data()

# Fetch toutes les autorités
q_aut = """
MATCH (a:Autorite_Contractante) RETURN a.Nom AS Autorite_Contractante
"""
with driver.session() as session:
    result = session.run(q_aut)
    data_aut = result.data()

AutC = []
for a in data_aut :
    AutC.append(a['Autorite_Contractante'])


# Create a NetworkX graph
G = nx.Graph()

for row in data:
    autorite = row['Autorite_Contractante']
    marche = row['Marche']
    titulaire = row['Titulaire']

    G.add_node(autorite['Nom'], type='Autorite_Contractante', data=autorite)
    G.add_node(marche['Titre'], type='Marche', data=marche)
    G.add_node(titulaire['Nom'], type='Titulaire', data=titulaire)

    G.add_edge(autorite['Nom'], marche['Titre'], relationship='Vendu_par')
    G.add_edge(marche['Titre'], titulaire['Nom'], relationship='Beneficiaire_de')

# Create a Plotly figure
fig = make_subplots(rows=1, cols=1)

pos = nx.spring_layout(G)  # You can use different layout algorithms

node_colors = {
    'Autorite_Contractante': 'blue',
    'Marche': 'green',
    'Titulaire': 'red'
}

edge_colors = {
    'Vendu_par': 'black',
    'Beneficiaire_de': 'gray'
}

for edge in G.edges():
    source, target = edge
    edge_type = G.edges[edge]['relationship']
    x0, y0 = pos[source]
    x1, y1 = pos[target]
    color = edge_colors.get(edge_type, 'black')  # Default to black if type not found
    
    edge_trace = go.Scatter(
        x=[x0, x1],
        y=[y0, y1],
        mode='lines+text',  # Use 'lines+text' mode to display both line and text
        line={'width': 2, 'color': color},
        text=[edge_type],  # Set text to the relationship type
        hoverinfo='none',  # Disable hover info for the line
        textposition='top center',  # Position the text above the line
        showlegend=False,  # Exclude from legend
    )
    fig.add_trace(edge_trace)


for node in G.nodes():
    x, y = pos[node]
    node_type = G.nodes[node]['type']
    color = node_colors.get(node_type, 'gray')  # Default to gray if type not found
    hover_text = f"{node_type}: {node}"  # Use the node name as is
    node_trace = go.Scatter(
        x=[x], y=[y], mode='markers', marker={'size': 10, 'color': color}, text=hover_text, hoverinfo='text'
    )
    fig.add_trace(node_trace)


fig.update_layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(b=0, l=0, r=0, t=0),
)

fig.update_xaxes(showticklabels=False)  
fig.update_yaxes(showticklabels=False)  

st.plotly_chart(fig)

st.markdown(f'__________________________________',unsafe_allow_html=True)
Aut = st.selectbox("Choisissez l'Autorité Contractante", options=AutC)

#Query en fonction de l'autorité contractante
query_1 = f"""
MATCH (n:Autorite_Contractante)-[r:Vendu_par]-(m:Marche)-[t:Beneficiaire_de]-(p:Titulaire)
WHERE n.Nom =  "{Aut}" 
RETURN n AS Autorite_Contractante, r AS Vendu_par, m AS Marche, t AS Beneficiaire_de, p AS Titulaire
LIMIT 10
"""
with driver.session() as session:
    result_1 = session.run(query_1)
    data_1 = result_1.data()

# Create a NetworkX graph
G_1 = nx.Graph()

for row in data_1:
    autorite = row['Autorite_Contractante']
    marche = row['Marche']
    titulaire = row['Titulaire']

    G_1.add_node(autorite['Nom'], type='Autorite_Contractante', data=autorite)
    G_1.add_node(marche['Titre'], type='Marche', data=marche)
    G_1.add_node(titulaire['Nom'], type='Titulaire', data=titulaire)

    G_1.add_edge(autorite['Nom'], marche['Titre'], relationship='Vendu_par')
    G_1.add_edge(marche['Titre'], titulaire['Nom'], relationship='Beneficiaire_de')

# Create a Plotly figure
fig_1 = make_subplots(rows=1, cols=1)

pos_1 = nx.spring_layout(G_1)  # You can use different layout algorithms

node_colors = {
    'Autorite_Contractante': 'blue',
    'Marche': 'green',
    'Titulaire': 'red'
}

edge_colors = {
    'Vendu_par': 'black',
    'Beneficiaire_de': 'gray'
}

for edge in G_1.edges():
    source, target = edge
    edge_type = G_1.edges[edge]['relationship']
    x0, y0 = pos_1[source]
    x1, y1 = pos_1[target]
    color = edge_colors.get(edge_type, 'black')  # Default to black if type not found
    
    edge_trace = go.Scatter(
        x=[x0, x1],
        y=[y0, y1],
        mode='lines+text',  # Use 'lines+text' mode to display both line and text
        line={'width': 2, 'color': color},
        text=[edge_type],  # Set text to the relationship type
        hoverinfo='none',  # Disable hover info for the line
        textposition='top center',  # Position the text above the line
        showlegend=False,  # Exclude from legend
    )
    fig_1.add_trace(edge_trace)


for node in G_1.nodes():
    x, y = pos_1[node]
    node_type = G_1.nodes[node]['type']
    color = node_colors.get(node_type, 'gray')  # Default to gray if type not found
    hover_text = f"{node_type}: {node}"  # Use the node name as is
    node_trace = go.Scatter(
        x=[x], y=[y], mode='markers', marker={'size': 10, 'color': color}, text=hover_text, hoverinfo='text'
    )
    fig_1.add_trace(node_trace)


fig_1.update_layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(b=0, l=0, r=0, t=0),
)

fig_1.update_xaxes(showticklabels=False)  
fig_1.update_yaxes(showticklabels=False)  

st.plotly_chart(fig_1)



st.markdown(f'__________________________________',unsafe_allow_html=True)
An = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
annee = st.selectbox("Choisissez l'Année", options=An)

#Query en fonction de l'autorité contractante
query_2 = f"""
MATCH (n:Autorite_Contractante)-[r:Vendu_par]-(m:Marche)-[t:Beneficiaire_de]-(p:Titulaire)
WHERE left(r.Date,4) =  "{annee}" 
RETURN n AS Autorite_Contractante, r AS Vendu_par, m AS Marche, t AS Beneficiaire_de, p AS Titulaire
LIMIT 10
"""
with driver.session() as session:
    result_2 = session.run(query_2)
    data_2 = result_2.data()

# Create a NetworkX graph
G_2 = nx.Graph()

for row in data_2:
    autorite = row['Autorite_Contractante']
    marche = row['Marche']
    titulaire = row['Titulaire']

    G_2.add_node(autorite['Nom'], type='Autorite_Contractante', data=autorite)
    G_2.add_node(marche['Titre'], type='Marche', data=marche)
    G_2.add_node(titulaire['Nom'], type='Titulaire', data=titulaire)

    G_2.add_edge(autorite['Nom'], marche['Titre'], relationship='Vendu_par')
    G_2.add_edge(marche['Titre'], titulaire['Nom'], relationship='Beneficiaire_de')

# Create a Plotly figure
fig_2 = make_subplots(rows=1, cols=1)

pos_2 = nx.spring_layout(G_2)  # You can use different layout algorithms

node_colors = {
    'Autorite_Contractante': 'blue',
    'Marche': 'green',
    'Titulaire': 'red'
}

edge_colors = {
    'Vendu_par': 'black',
    'Beneficiaire_de': 'gray'
}

for edge in G_2.edges():
    source, target = edge
    edge_type = G_2.edges[edge]['relationship']
    x0, y0 = pos_2[source]
    x1, y1 = pos_2[target]
    color = edge_colors.get(edge_type, 'black')  # Default to black if type not found
    
    edge_trace = go.Scatter(
        x=[x0, x1],
        y=[y0, y1],
        mode='lines+text',  # Use 'lines+text' mode to display both line and text
        line={'width': 2, 'color': color},
        text=[edge_type],  # Set text to the relationship type
        hoverinfo='none',  # Disable hover info for the line
        textposition='top center',  # Position the text above the line
        showlegend=False,  # Exclude from legend
    )
    fig_2.add_trace(edge_trace)


for node in G_2.nodes():
    x, y = pos_2[node]
    node_type = G_2.nodes[node]['type']
    color = node_colors.get(node_type, 'gray')  # Default to gray if type not found
    hover_text = f"{node_type}: {node}"  # Use the node name as is
    node_trace = go.Scatter(
        x=[x], y=[y], mode='markers', marker={'size': 10, 'color': color}, text=hover_text, hoverinfo='text'
    )
    fig_2.add_trace(node_trace)


fig_2.update_layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(b=0, l=0, r=0, t=0),
)

fig_2.update_xaxes(showticklabels=False)  
fig_2.update_yaxes(showticklabels=False)  

st.plotly_chart(fig_2)
