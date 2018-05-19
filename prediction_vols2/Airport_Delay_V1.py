import numpy as np
import pandas as pd
from datetime import datetime
#pour création jeu de test/entrainement
from sklearn.model_selection import train_test_split

cie_aerienne_dict = {
'FL':'AirTran airways',
'AS':'Alaska airlines',
'AA':'American airlines',
'DL':'Delta airways',
'9E':'Endeavor air',
'MQ':'Envoy air',
'EV':'ExpressJet airlines',
'F9':'Frontier airlines',
'HA':'Hawaiian airlines',
'B6':'JetBlue airways',
'YV':'Mesa airlines',
'OO':'SkyWest airlines',
'WN':'Southwest airlines',
'NK':'Spirit airlines',
'UA':'United airlines',
'US':'US airways',
'VX':'Virgin America'
}

jour_semaine_dict = { 1:'Lundi',2:'Mardi',3:'Mercredi',4:'Jeudi',5:'Vendredi',6:'Samedi',7:'Dimanche' }

# Fonction créant une liste de valeurs distinctes d'une colonne d"un dataframe
def liste_distincte_col(df, nom_col, sep=""):
    """Créet une liste de valeurs distinctes d'une colonne d"un dataframe

    - Args:
        df(pandas.dataframe): dataframe
        nom_col(str): nom de la colonne
        sep(str): chaine de caractère séparateur (optionnel)
        
    - Returns:
        Liste contenant les colonnes contenant la chaîne de caractères.
    """
    liste_distincte = []
    for col in df[nom_col].values:
        #On exclut les données non renseignées
        if not isinstance(col, float):
            if sep != "" and sep in col:
                liste = col.split(sep)
                for l in liste:
                    if not (l in liste_distincte):
                        liste_distincte.append(l)
            else:
                if not (col in liste_distincte):
                    liste_distincte.append(col)
    return liste_distincte


# Fonction listant les colonnes dont le titre contient des chaines de caractères
def col_rech_titre(df, fin = True, suffix =""):
    """Affiche le nom des colonnes d'un dataframe contenant une chaîne de caractères.

    - Args:
        df(pandas.dataframe): dataframe
        fin(boolean): flag pour indiquer un préfixe ou un suffixe
        suffix(str): chaîne de caractères recherchée
        
    - Returns:
        Liste contenant les colonnes contenant la chaîne de caractères.
    """
    liste_col = []
    if suffix !="":
        if fin == True:
            for col in df.columns:
                if col.endswith(suffix) == True:
                    liste_col.append(col)
        else:
            for col in df.columns:
                if col.startswith(suffix) == True:
                    liste_col.append(col)                  
    return liste_col 

def MaxFlightsCode(df, airport_code):
    """Comptabilise le nombre de vols sur un code aéroport dans la base complète des vols (fly)

    - Args:
        df(pandas.dataframe): dataframe des vols
        airport_code(integer): Code aéroport
        
    - Returns:
        Renvoie le nombre de vols sur l'aéroport donné dans la base df
    """
    #df = fly
    # Calculates the most likely flights based on flight frequency.
    codeFrame = df.loc[df.ORIGIN_AIRPORT_ID == airport_code]
    numFlights = codeFrame.shape[0]
    # Get the number of rows in this frame
    return(numFlights)

def AirportCode (df_fly, df_airport, city):
    """Cherche quel est l'AIRPORT_ID d'un aéroport principal d'une ville

    - Args:
        df_fly(pandas.dataframe): dataframe des vols
        df_airport(pandas.dataframe): dataframe des aéroports
        city(string): Nom de la ville dont on cherche le code de l'aéroport principal
        
    - Returns:
        Renvoie le AIRPORT_ID d'un aéroport principal d'une ville
    """
    #Création d'une nouvelle colonne avec nom aéroport en minuscule
    df_airport['airport_minus'] = df_airport.Description.str.lower() #.str.strip()
    #Création dataFrame avec uniquement les aéroports cherché avec city
    lescodes = df_airport.loc[df_airport.airport_minus.str.contains(city.lower())].copy()
    if lescodes.shape[0]>0:
        #Recherche pour chacun de ces aéoports du dataFrame du nombre de vols total dans le df des vols
        lescodes['NumFlights'] = lescodes.apply(lambda row: MaxFlightsCode(df_fly, row['Code']), axis=1)
        #Recherhe de l'aéroport qui a le plus de vols dans NumFlights
        code_aeroport = lescodes.loc[lescodes.NumFlights == max(lescodes.NumFlights)]['Code'].values
        # Return our top airport
        return(code_aeroport[0])
    else:
        return(0)


def prediction2(param, coef, intercept, origin = '', destination = '', 
                carrier = '', month = 0, weekday = 0):
    '''
    This function allows you to input all of your flight information (no leaks!) and
    the function will return how late your flight will arrive based on the output from the 
    SGD Regressor.
        
    Inputs: 
        
            Origin (enter this as a city, state combo, or include the airport name (such as Bush
                        or Hobby). This will automatically calculate which airport you meant.
                 
            Destination (same as Origin, entered as a string)
                 
            Carrier (which Airline, use a string to represent the name (such as 'American' or 'United')
                 
            Month (the month the flight is scheduled for)
                 
            Weekday (Enter number between 1-7) such as 1:'Lundi',2:'Mardi',3:'Mercredi',4:'Jeudi',5:'Vendredi',6:'Samedi',7:'Dimanche'
                 
            Available Carriers:
            'FL':'AirTran airways',
            'AS':'Alaska airlines',
            'AA':'American airlines',
            'DL':'Delta airways',
            '9E':'Endeavor air',
            'MQ':'Envoy air',
            'EV':'ExpressJet airlines',
            'F9':'Frontier airlines',
            'HA':'Hawaiian airlines',
            'B6':'JetBlue airways',
            'YV':'Mesa airlines',
            'OO':'SkyWest airlines',
            'WN':'Southwest airlines',
            'NK':'Spirit airlines',
            'UA':'United airlines',
            'US':'US airways',
            'VX':'Virgin America
            
    Outputs: 
        int: Estimated delay for the arrival (in minutes, can be negative if the flight is expected to arrive early)
        text: Status of the estimation
    '''
    from sklearn import linear_model
    
    col_utiles = ['CARRIER_DELAY','WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY',
                'MONTH','DAY_OF_MONTH', 'DAY_OF_WEEK','UNIQUE_CARRIER',
                'ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID','CRS_DEP_TIME',
                'DISTANCE', 'AIR_TIME','CRS_ELAPSED_TIME','ACTUAL_ELAPSED_TIME', 'ARR_DELAY' ]    
    #Lecture du fichier d'input
    fly = pd.read_csv('2016_sample_file_Copy2_00.csv', sep=",", encoding='utf_8', low_memory=False,
                      error_bad_lines=False, usecols = col_utiles)
    #Et celui des aéroports
    airport = pd.read_csv('L_AIRPORT_ID.csv', sep=",", encoding='utf_8', low_memory=False, error_bad_lines=False)
    
    #Label encoding des cies aériennes
    Cie = liste_distincte_col(fly,'UNIQUE_CARRIER','|')
    Cie.sort()
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    le.fit(Cie)
    fly['CIE'] = le.transform(fly['UNIQUE_CARRIER'])

    #Création d'un df avec la liaison UNIQUE_CARRIER <-> CIE
    CIEdf = fly[['UNIQUE_CARRIER', 'CIE']].drop_duplicates() # On conserve un exemplaire unique

    #Elimination de la colonne UNIQUE_CARRIER
    fly.drop(['UNIQUE_CARRIER'], axis=1, inplace= True)

    #Elimination des colonnes Unnamed
    fly = fly.drop(col_rech_titre(fly, False, "Unnamed"), axis=1)
    
    #Recherche du code des aéroports
    id_origin=0
    id_destination=0
    if origin !='':
        id_origin = AirportCode(fly, airport, origin)
    if destination !='':
        id_destination = AirportCode(fly, airport, destination)
    
    #Création d'un marsk / filtre
    def mask(df, key, value):
        return df[df[key] == value]
    pd.DataFrame.mask = mask
    
    #Filtrage de Fly:
    if id_origin != 0:
        fly = fly.mask('ORIGIN_AIRPORT_ID', id_origin)
    
    if id_destination != 0 :
        fly = fly.mask('DEST_AIRPORT_ID', id_destination)
    
    if month != 0 :
        fly = fly.mask('MONTH', month)
    
    if weekday != 0 :
        fly = fly.mask('DAY_OF_WEEK', weekday)
    
    if carrier != '' :
        #Détermination de la CIE à partir de UNIQUE_CARRIER
        carrier_num = CIEdf[CIEdf.UNIQUE_CARRIER == carrier]
        carrier_num = carrier_num['CIE'].values[0]
        fly = fly.mask('CIE', carrier_num)
    
    #Remplacement des NaN
    fly['CARRIER_DELAY'].fillna(0, inplace=True)
    fly['WEATHER_DELAY'].fillna(0, inplace=True)
    fly['NAS_DELAY'].fillna(0, inplace=True)
    fly['SECURITY_DELAY'].fillna(0, inplace=True)
    fly['LATE_AIRCRAFT_DELAY'].fillna(0, inplace=True)
    
    if fly.shape[0] == 0 :
        return 0 , "Insuffisament de données pour prédire ! Soyez moins précis !"
    
    #Création des moyennes par colonne
    fly_mean= fly.mean()
    
    #Création d'un DataFRame mono observation reprenant la moyenne des infos nécessaires à la régression:
    ar = np.array([[fly_mean['CARRIER_DELAY'],fly_mean['WEATHER_DELAY'],fly_mean['NAS_DELAY'],
                fly_mean['SECURITY_DELAY'],fly_mean['LATE_AIRCRAFT_DELAY'],fly_mean['DISTANCE'],
                fly_mean['AIR_TIME'],fly_mean['CRS_ELAPSED_TIME'],fly_mean['ACTUAL_ELAPSED_TIME']   ]])
    df = pd.DataFrame(ar, index = [1], columns = ['CARRIER_DELAY','WEATHER_DELAY', 'NAS_DELAY',
                'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY','DISTANCE', 'AIR_TIME','CRS_ELAPSED_TIME',
                'ACTUAL_ELAPSED_TIME'])
    
    
    New_ridge = linear_model.Ridge(alpha=100)
    New_ridge.set_params=param
    New_ridge.coef_ = coef
    New_ridge.intercept_= intercept
    
    print("Prédiction d'avance/retard: ", int(New_ridge.predict(df)[0]), " minutes " )
    
    return int(New_ridge.predict(df)[0]) , "sans erreur"
    
    
    
