import streamlit as st


st.title('Tableau de Bord des Marchés Publics Au Sénégal')
image = "Flag_of_Senegal.png"
st.image(image, width=500)
st.title('A propos')
st.markdown ('## Contenu')
st.write("Bienvenue sur le tableau de bord interactif de la Base de Données des Marchés Publics de l'Agence de Régulation des Marchés Publics (ARMP). Cette plateforme a été conçue pour vous offrir un accès convivial et dynamique aux informations cruciales concernant les marchés publics. Grâce à cette interface, vous avez la possibilité d'explorer et d'analyser les données relatives aux marchés publics, qu'il s'agisse des autorités contractantes, des titulaires, des marchés eux-mêmes, ou des transactions entre ces acteurs.\n\
        Notre objectif est de faciliter l'accès à des données transparentes et actualisées, favorisant ainsi une meilleure compréhension et une prise de décision éclairée dans le domaine des marchés publics. Vous pouvez filtrer, visualiser et interagir avec les informations de manière intuitive, grâce à des outils de graphiques et de visualisation avancés.")

col_1, col_2 = st.columns([1,1])

with col_1:
    st.markdown('## Contenu \n\
    - Accueil \n\
    - Graphe des Marchés Publics \n\
    - Les Marchés \n\
    - Les Autorités Contractantes \n\
    - Les Titulaires \n\
    ')

with col_2:
    st.markdown('## Fonctionnalités \n\
    - Explorez la structure et les relations des marchés publics à travers des graphiques de réseau interactifs \n\
    - Accédez à une vue détaillée des marchés publics actuels et passés.\n\
    - Découvrez les Autorités Contractantes qui ont joué un rôle clé dans les marchés publics.  \n\
    - Explorez les titulaires des marchés publics et leur participation dans les transactions. ')