import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Configurer Streamlit
st.set_page_config(page_title="Cereal database project", layout="wide")

# Titre
st.title("Interactive Dashboard ")

st.write("INSTRUCTIONS")
st.write("On the left side of the page, there are filters. They are divided into state variables (region and cereals), productivity variables (production, cultivated area, yield) and climatic variables (precipitation, temperatures, etc.).. ")
st.write("In the section below, you will be able to explore and visualize various data. Please select the filters first.")


# Chargement des données
@st.cache_data
def load_data():
    return pd.read_excel('base_finale_céréales.xlsx')

df = load_data()

# Aperçu
#st.subheader("Aperçu des données")
#st.dataframe(df.head())

# Filtres interactifs
st.sidebar.header("Filters")

regions = df['Région'].unique()
cereales = df['Céréales'].unique()

regions_sel = st.sidebar.multiselect("Select one or more Regions", sorted(regions), default=sorted(regions)[:1])
cereales_sel = st.sidebar.multiselect("Select one or more Cereals", sorted(cereales), default=sorted(cereales)[:1])

# Choix de la variable de productivité
var_affiche1 = st.sidebar.selectbox("Productivity variable", ['Production (en tonnes)', 'Superficie (en ha)', 'Rendement (tonne/ha)'])

# Choix de la variable de climatique
var_affiche2 = st.sidebar.selectbox("Climate variable", ['Précipitations moyennes annuelles (en mm)', 'Nombre de jours de pluie', 
                                                            'Températures moyennes annuelles (en C°)', 'Humidité relative maximale (en %)',
                                                          'Vent moyen annuel (en m/s)', 'Durée ensoleillement (en h/jr)'])

# Filtres sur les variables d'état

#Filtre sur régions uniquement
df_filtre1 = df[(df['Région'].isin(regions_sel))]

#Filtre sur céréales uniquement
df_filtre2 = df[df['Céréales'].isin(cereales_sel)]

#Filtre sur régions et céréales
df_filtre = df[(df['Région'].isin(regions_sel)) & (df['Céréales'].isin(cereales_sel))]

#Affichage de la table de données en fonction des variables d'état

if regions_sel and not cereales_sel:
    st.subheader(f"Data table for {', '.join(regions_sel)}")
    st.dataframe(df_filtre1)
    
elif cereales_sel and not regions_sel:
    st.subheader(f"Data table for {', '.join(cereales_sel)}")
    st.dataframe(df_filtre2)

elif regions_sel and cereales_sel:
    st.subheader(f"Data table for {', '.join(regions_sel)} et {', '.join(cereales_sel)}")
    st.dataframe(df_filtre)

else:
    st.subheader("Please select at least one Region or Cereal.")


# Export Excel
st.write("Download filtered data")

# Créer un buffer Excel en mémoire
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    if regions_sel and not cereales_sel:
        df_filtre1.to_excel(writer, index=False, sheet_name='filtered data')
        data = output.getvalue()
    elif cereales_sel and not regions_sel:
        df_filtre2.to_excel(writer, index=False, sheet_name='filtered data')
        data = output.getvalue()
    elif regions_sel and cereales_sel:
        df_filtre.to_excel(writer, index=False, sheet_name='filtered data')
        data = output.getvalue()

st.download_button(
    label="Download in Excel",
    data=data,
    file_name='filtered_data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)


# Graphique et statistiques des variables productivité en fonction des régions  
st.subheader(" Productivity Chart and Statistics by Region ")
if not df_filtre1.empty:
    st.write(f" 1. Evolution of {var_affiche1} (1996 - 2022) for {', '.join(regions_sel)} ")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=df_filtre1,
        x='Année',
        y=var_affiche1,
        hue='Région',
        markers=True,
        dashes=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.ylabel(var_affiche1)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write(f" 2. Descriptive Statistics of {var_affiche1} for {', '.join(regions_sel)} ")
    stats = df_filtre1.groupby(['Région'])[var_affiche1].describe().reset_index()
    st.dataframe(stats)
else:
    st.warning("No data available for current selections.")


    
    
# Graphique et statistiques des variables productivité en fonction des céréales
st.subheader(" Graph and Statistics of Productivity by Cereal ")
if not df_filtre2.empty:
    st.write(f" 1. Evolution of {var_affiche1} (1996 - 2022) for {', '.join(cereales_sel)} ")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=df_filtre2,
        x='Année',
        y=var_affiche1,
        hue='Céréales',
        markers=True,
        dashes=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.ylabel(var_affiche1)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write(f" 2. Descriptive Statistics of {var_affiche1} for {', '.join(cereales_sel)} ")
    stats = df_filtre2.groupby(['Céréales'])[var_affiche1].describe().reset_index()
    st.dataframe(stats)
else:
    st.warning("No data available for current selections.")


# Graphique et statistiques des variables productivité en fonction des régions et des céréales
st.subheader(" Graph and Statistics of Productivity by Region and Cereal ")
if not df_filtre.empty:
    st.write(f" 1. Evolution of {var_affiche1} (1996 - 2022) for {', '.join(regions_sel)} and {', '.join(cereales_sel)}")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=df_filtre,
        x='Année',
        y=var_affiche1,
        hue='Région',
        style='Céréales',
        markers=True,
        dashes=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.ylabel(var_affiche1)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write(f" 2. Descriptive Statistics of {var_affiche1} for {', '.join(regions_sel)} and {', '.join(cereales_sel)} ")
    stats = df_filtre.groupby(['Région', 'Céréales'])[var_affiche1].describe().reset_index()
    st.dataframe(stats)
else:
    st.warning("Aucune donnée disponible pour les sélections actuelles.")
    

# Graphique et statistiques des variables climatiques en fonction des régions  
st.subheader(" Climate Chart and Statistics by Region ")
if not df_filtre1.empty:
    st.write(f" 1. Evolution of {var_affiche2} (1996 - 2022) for {', '.join(regions_sel)} ")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=df_filtre1,
        x='Année',
        y=var_affiche2,
        hue='Région',
        markers=True,
        dashes=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.ylabel(var_affiche2)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write(f" 2. Descriptive Statistics of {var_affiche2} for {', '.join(regions_sel)} ")
    stats = df_filtre1.groupby(['Région'])[var_affiche2].describe().reset_index()
    st.dataframe(stats)
else:
    st.warning("No data available for current selections.")
