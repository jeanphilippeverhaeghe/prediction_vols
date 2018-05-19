import numpy as np
import pandas as pd

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


def prediction(origin = 'Dallas', destination = 'Chicago', 
                carrier = 'AA', dept_time = 17, arr_time = 20,
                month = 1, day = 28, weekday = 1):
    '''
    This function allows you to input all of your flight information (no leaks!) and
    the function will return how late your flight will arrive based on the output from the 
    SGD Regressor.
        
    Inputs: 
        
            Origin (enter this as a city, state combo, or include the airport name (such as Bush
                        or Hobby). This will automatically calculate which airport you meant.
                 
            Destination (same as Origin, entered as a string)
                 
            Carrier (which Airline, use a string to represent the name (such as 'American' or 'United')
                 
            Departing Hour scheduled (just the hour of departure, based on a 24 hour cycle. This means
                                noon would be 12, and midnight would be 0.)
                
            Arriving Hour scheduled (same format as departing)
                 
            Month (the month the flight is scheduled for)
                 
            Day (the day of the month the flight is scheduled for)
                 
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
    #Lecture du fichier d'input
    fly = pd.read_csv('Travel_Step_1_working_file.csv', sep=",", encoding='utf_8', low_memory=False, error_bad_lines=False)
    #Et celui des aéroports
    airport = pd.read_csv('L_AIRPORT_ID.csv', sep=",", encoding='utf_8', low_memory=False, error_bad_lines=False)
    
    #Elimination des colonnes Unnamed
    fly.drop(col_rech_titre(fly, False, "Unnamed"), axis=1, inplace= True)
    
    #Création d'un df avec la liaison UNIQUE_CARRIER <-> CIE
    CIEdf = fly[['UNIQUE_CARRIER', 'CIE']].drop_duplicates() # On conserve un exemplaire unique
    
    #Elimination des données inutiles
    fly.drop(['UNIQUE_CARRIER', 'CRS_DEP_TIME', 'CRS_ARR_TIME'], axis=1, inplace= True)
    fly.drop(['CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME', 'AVANCE_RETARD_en_VOL'], axis=1, inplace= True)
    
    #Elimination des lignes avec des NA
    fly = fly.dropna(how='any',axis='index')
    
    #Création des groupes de données
    scalingDF = fly[['DISTANCE']].astype('float') # Numerical features
    categDF = fly[['MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK','ORIGIN_AIRPORT_ID',
                   'DEST_AIRPORT_ID','CRS_DEP_HOUR', 'CRS_ARR_HOUR','CIE']] # Categorical features
    
    #One hot encoding des variables catégorielles
    from sklearn.preprocessing import OneHotEncoder
    encoder = OneHotEncoder() # Create encoder object
    categDF_encoded = encoder.fit_transform(categDF) # Can't convert this to dense array: too large!
    type(categDF_encoded)
    
    #Passage en matrice creuse des données numériques
    from scipy import sparse # Need this to create a sparse array
    scalingDF_sparse = sparse.csr_matrix(scalingDF)
    
    #Empilage de la matrice catégorielle et celle numérique
    x_final = sparse.hstack((scalingDF_sparse, categDF_encoded))
    
    #La donnée à prédire ARR_DELAY
    y_final = fly['ARR_DELAY'].values
    
    #Split Training / Test
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x_final,y_final,test_size = 0.3,random_state = 0) # Do 70/30 split
    
    #Normalisation des données
    x_train_numerical = x_train[:, 0].toarray() # We only want the first features which are the numerical ones.
    x_test_numerical = x_test[:, 0].toarray()
    
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler() # create scaler object
    scaler.fit(x_train_numerical) # fit with the training data ONLY
    x_train_numerical = sparse.csr_matrix(scaler.transform(x_train_numerical)) # Transform the data and convert to sparse
    x_test_numerical = sparse.csr_matrix(scaler.transform(x_test_numerical))
    
    #Remplacement des données normalisées dans les matrices finales
    x_train[:, 0] = x_train_numerical
    x_test[:, 0] = x_test_numerical
    
    #SGD Regressor
    from sklearn.linear_model import SGDRegressor
    from sklearn.model_selection  import GridSearchCV
    
    SGD_params = {'alpha': 10.0**-np.arange(1,7)} # Suggested range we try
    #SGD_model = GridSearchCV(SGDRegressor(random_state = 0), SGD_params, scoring = 'neg_mean_absolute_error', cv = 5) # Use 5-fold CV 
    SGD_model = GridSearchCV(SGDRegressor(random_state = 0), SGD_params, scoring = 'r2', cv = 5) # Use 5-fold CV 
    SGD_model.fit(x_train, y_train) # Fit the model
    
    #Régression:
    from sklearn.metrics import mean_absolute_error
    y_true, y_pred = y_test, SGD_model.predict(x_test) # Predict on our test set
    #print (f"Mean absolute error of SGD regression was: {mean_absolute_error(y_true, y_pred):.2f} minutes")
    
    #print (f"RMSE hors metrics {np.sqrt(((y_test-SGD_model.predict(x_test))**2).sum()/len(y_test)) }          np.sqrt(((y_test-SGD_model.predict(x_test))**2).sum()/len(y_test))")
    #print (f"R² vaut {SGD_model.score(x_test,y_test)}          SGD_model.score(x_test,y_test)")
    
    ################################
    #### Début de la Prédiction ####
    ################################
    origin_code = AirportCode(fly, airport, origin)
    destination_code = AirportCode(fly, airport, destination)
    
    try:
        distance = np.array(float(fly[(fly.ORIGIN_AIRPORT_ID == origin_code) & 
                    (fly.DEST_AIRPORT_ID == destination_code)].DISTANCE.drop_duplicates()))
    except:
        return -1 , "Route inconnue dans les données. SVP essayez une ville différente ou une nouvelle destination."
    
    #Détermination de la CIE à partir de UNIQUE_CARRIER
    carrier_num = CIEdf[CIEdf.UNIQUE_CARRIER == carrier]
    carrier_num = carrier_num['CIE'].values[0]

    #Le jour de la semaine est le numéro du jour 
    weekday_num = weekday

    
    numerical_values = np.c_[distance] 
    
    #Scale les données
    numerical_values_scaled = scaler.transform(numerical_values)
    
    # Now create our array of categorical values.
    categorical_values = np.zeros(8)
    categorical_values[0] = int(month)
    categorical_values[1] = int(day)
    categorical_values[2] = int(weekday_num)
    categorical_values[3] = int(origin_code)
    categorical_values[4] = int(destination_code)
    categorical_values[5] = int(dept_time)
    categorical_values[6] = int(arr_time)
    categorical_values[7] = int(carrier_num)
    
    # Apply the one-hot encoding to these.
    categorical_values_encoded = encoder.transform([categorical_values]).toarray()
         
    # Combine these into the final test example that goes into the model
    final_test_example = np.c_[numerical_values_scaled, categorical_values_encoded]
         
    # Now predict this with the model 
    pred_delay = SGD_model.predict(final_test_example)
    #print (f"Your predicted delay is, {int(pred_delay[0])}, minutes.")
    
    return int(pred_delay[0]) , "prédiction sans erreur"
    
    
    
