import networkx as nx
from neo4j import GraphDatabase
import pandas as pd
import datetime

# Chargement du dataset tabulaire depuis un fichier CSV
df = pd.read_csv('Datawarehouse.csv')
i = df.index[df['Clean_Date'] == "14/14/2021"].tolist()
df['Clean_Date'][i] = "14/12/2021"

i = df.index[df['Clean_Date'] == "30/60/2021"].tolist()
df['Clean_Date'][i] = "30/06/2021"

# Création d'un nouveau graphe non orienté
graph = nx.Graph()

# Ajout des nœuds au graphe
graph.add_nodes_from(df['Titre'], node_type='Marché')
graph.add_nodes_from(df['Titulaire'], node_type='Titulaire')
graph.add_nodes_from(df['Autorite_Contractante'], node_type='Autorite_Contractante')

# Ajout des arêtes et des attributs correspondants
for _, row in df.iterrows():
    input_date = datetime.datetime.strptime(row['Clean_Date'], "%d/%m/%Y")
    Clean_Date = input_date.strftime("%Y/%m/%d")
    
    marché = row['Titre']
    titulaire = row['Titulaire']
    autorite = row['Autorite_Contractante']
    date = Clean_Date
    montant = row['Montant_cfa']
    
    # Ajout de l'arête entre Marché et Titulaire avec les propriétés Date et Montant
    graph.add_edge(marché, titulaire, relation='Beneficiaire_de', Date=date, Montant=montant)
    
    # Ajout de l'arête entre Marché et Autorite_Contractante
    graph.add_edge(marché, autorite, relation='Vendu_par',Date=date, Montant=montant)

# Calcul des features pour les nœuds Titulaire et Autorite_Contractante
titulaire_count = df['Titulaire'].value_counts()
autorite_count = df['Autorite_Contractante'].value_counts()

for node in graph.nodes:
    if graph.nodes[node]['node_type'] == 'Marché':
        # Ajouter les features spécifiques au nœud Marché
        graph.nodes[node]['Type'] = df.loc[df['Titre'] == node, 'Type'].iloc[0]
        graph.nodes[node]['Secteur'] = df.loc[df['Titre'] == node, 'Secteur'].iloc[0]
    elif graph.nodes[node]['node_type'] == 'Titulaire':
        # Calcul du nombre de marché acquis pour le Titulaire
        graph.nodes[node]['Nombre_Marché_Acquis'] = titulaire_count.get(node, 0)
    elif graph.nodes[node]['node_type'] == 'Autorite_Contractante':
        # Calcul du nombre de marché vendus pour l'Autorite_Contractante
        graph.nodes[node]['Nombre_Marché_Vendus'] = autorite_count.get(node, 0)

NEO4J_URI= "neo4j+s://b0a21d6c.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="OU2jdTE7c1ikO8ronSWOQdFlb-9Yj67C58-0ZZeJXU8"
AURA_INSTANCEID="b0a21d6c"
AURA_INSTANCENAME="Instance01"


uri = "bolt://localhost:7687"
username = "neo4j"
password = "012345678"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
driver

with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

# Parcourir les noeuds du graphe et les ajouter à Neo4j
for node, attributes in graph.nodes(data=True):
    node_type = attributes['node_type']
    if node_type == 'Marché':
        # Ajouter un noeud Marché avec ses attributs à Neo4j
        with driver.session() as session:
            session.run(
                "CREATE (m:Marche {Titre: $titre, Type: $type, Secteur: $secteur})",
                titre=node, type=attributes['Type'], secteur=attributes['Secteur']
            )
    elif node_type == 'Titulaire':
        # Ajouter un noeud Titulaire avec ses attributs à Neo4j
        with driver.session() as session:
            session.run(
                "CREATE (t:Titulaire {Nom: $nom, Nombre_Marché_Acquis: $nombre_marché_acquis})",
                nom=node, nombre_marché_acquis=attributes['Nombre_Marché_Acquis']
            )
    elif node_type == 'Autorite_Contractante':
        # Ajouter un noeud Autorite_Contractante avec ses attributs à Neo4j
        with driver.session() as session:
            session.run(
                "CREATE (a:Autorite_Contractante {Nom: $nom, Nombre_Marché_Vendus: $nombre_marché_vendus})",
                nom=node, nombre_marché_vendus=attributes['Nombre_Marché_Vendus']
            )

# Parcourir les arêtes du graphe et les ajouter à Neo4j
for source, target, attributes in graph.edges(data=True):
    relation = attributes['relation']
    date = attributes.get('Date', '')  
    montant = attributes.get('Montant', '')  
    
    # Ajouter une relation entre les nœuds source et target à Neo4j avec les propriétés "Date" et "Montant"
    with driver.session() as session:
        session.run("MATCH (source), (target) WHERE source.Titre = $source AND target.Nom = $target "
                    "CREATE (source)-[:%s {Date: $date, Montant: $montant}]->(target)" % relation,
                    {"source": source, "target": target, "date": date, "montant": montant})

# Fermer la connexion au driver Neo4j
driver.close()