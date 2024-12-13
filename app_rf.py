import streamlit as st # type: ignore
import pandas as pd
import numpy as np
import joblib  # Pour charger et sauvegarder le modèle
from sklearn.preprocessing import LabelEncoder

# Charger le modèle entraîné
model = joblib.load('model.joblib') 

# Titre de l'application
st.title("Prédiction du prix des locations Airbnb à Paris")

# Sidebar pour les entrées utilisateur
st.sidebar.header("Entrez les caractéristiques du logement")

# Fonction pour obtenir les entrées utilisateur
def user_input_features():
    neighbourhood = st.sidebar.selectbox("Quartier", 
                                         ['Observatoire', 'Hôtel-de-Ville', 'Buttes-Chaumont', 
                                          'Louvre', 'Popincourt', 'Buttes-Montmartre', 'Gobelins', 
                                          'Bourse', 'Ménilmontant', 'Reuilly', 'Entrepôt', 
                                          'Temple', 'Élysée', 'Panthéon', 'Luxembourg', 
                                          'Opéra', 'Batignolles-Monceau', 'Vaugirard', 
                                          'Palais-Bourbon', 'Passy'])
    latitude = st.sidebar.slider("Latitude", 48.80, 48.90)
    longitude = st.sidebar.slider("Longitude", 2.25, 2.50)
    host_listings_count = st.sidebar.number_input("Nombre de logements du propriétaire", 1, 100, 1)
    room_type = st.sidebar.selectbox("Type de chambre", 
                                     ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room'])
    accommodates = st.sidebar.number_input("Nombre de personnes hébergées", 1, 10, 2)
    bathrooms = st.sidebar.slider("Nombre de salles de bain", 1, 5, 1)
    bedrooms = st.sidebar.slider("Nombre de chambres", 1, 5, 1)
    beds = st.sidebar.slider("Nombre de lits", 1, 5, 1)
    minimum_nights = st.sidebar.number_input("Nombre minimum de nuits", 1, 365, 1)
    maximum_nights = st.sidebar.number_input("Nombre maximum de nuits", 1, 365, 30)
    is_central = st.sidebar.selectbox("Est-ce central ?", [0, 1])
    amenities_count = st.sidebar.number_input("Nombre d'équipements", 1, 50, 10)
    
    # Créer un DataFrame avec les entrées utilisateur
    data = {
        'neighbourhood_cleansed': [neighbourhood],
        'latitude': [latitude],
        'longitude': [longitude],
        'host_listings_count': [host_listings_count],
        'room_type': [room_type],
        'accommodates': [accommodates],
        'bathrooms': [bathrooms],
        'bedrooms': [bedrooms],
        'beds': [beds],
        'minimum_nights': [minimum_nights],
        'maximum_nights': [maximum_nights],
        'is_central': [is_central],
        'amenities_count': [amenities_count]
    }
    
    input_df = pd.DataFrame(data)
    
    # Encodage des colonnes catégorielles (exemple : 'room_type' et 'neighbourhood_cleansed')
    le_room_type = LabelEncoder()
    input_df['room_type_encoded'] = le_room_type.fit_transform(input_df['room_type'])
    
    # Ajouter des colonnes manquantes avec des valeurs par défaut ou calculées (exemples fictifs)
    input_df['host_total_listings_count'] = 1  # Exemple d'une valeur par défaut
    input_df['calculated_host_listings_count_entire_homes'] = 0  # Exemple d'une valeur par défaut
    input_df['calculated_host_listings_count_private_rooms'] = 0  # Exemple d'une valeur par défaut
    input_df['neighbourhood_cleansed_encoded'] = le_room_type.fit_transform(input_df['neighbourhood_cleansed'])
    
    return input_df

# Obtenir les données utilisateur
input_df = user_input_features()

# Afficher les entrées utilisateur
st.subheader("Caractéristiques fournies :")
st.write(input_df)

# Faire une prédiction
if st.button("Prédire le prix"):
    try:
        prediction = model.predict(input_df)
        st.subheader("Prix prédit :")
        st.write(f"{prediction[0]:.2f} €")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")