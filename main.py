import pandas as pd
import numpy as np
from fastapi import FastAPI, Path, UploadFile, File

app=FastAPI(title='Machine Learning Operations (MLOps)',
            description='Here we can do some consults')

steam_games = pd.read_csv("C:/Users/FE15/OneDrive/Desktop/Henry-DataFT16/PI_ML_OPS-main/dataset_ready/merged_users_items_reviews_games.csv")
# user_reviews = pd.read_excel('./dataset_ready/user_reviews.xlsx')
# user_items = pd.read_excel('./dataset_ready/user_items.xlsx')

@app.get("/get_free_content/")
async def developer(developer_name: str):
    # Masks
    mask_developer = steam_games['developer'] == developer_name
    mask_free = steam_games['price_string'].str.contains('free', case=False, na=False)
    
    free_games = steam_games[mask_developer & mask_free]
    
    # Grouping by 'release_year'
    quantity_free_items = free_games.groupby('release_year').size().reset_index(name='Quantity_of_items')
    
    # Quantity of free items of that developer
    total_items = steam_games[mask_developer].groupby('release_year').size().reset_index(name='Total_items')
    
    # Merging the results and calculating the percentage of free content
    result = pd.merge(total_items, quantity_free_items, on='release_year', how='left').fillna(0)
    result['Free_content'] = (result['Quantity_of_items'] / result['Total_items']) * 100
    
    result = result[['release_year', 'Quantity_of_items', 'Free_content']]
    
    return result

# Para correrlo pa:

# primero instala: fastapi y uvicorn
# pip install fastapi
# pip install uvicorn

# Abri la terminal desde este notebook, Clickeando arriba "Terminal" - "New Terminal"
# Y abajo, donde ya aparece la terminal, pega esta linea que esta debajo (sin el numeral, eso fue para dejarlo texto)
# python -m uvicorn main:app --reload

# Con esto, basicamente tu API y estos datos y funciones, estan en linea.

# Abri el google chrome, copia y pega en la URL esta ruta: http://127.0.0.1:8000/docs
# Tadaaaaaasas


# def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora

def developer(desarrollador: str):

    # Mask developer
    mask_developer = steam_merged['developer'] == desarrollador
    # Mask price = 0 --> free
    mask_free = steam_merged['price2'] == 0
    # sum of masks    
    free_games = steam_merged[mask_developer & mask_free]
        
    # Grouping by 'release_year'
    quantity_free_items = free_games.groupby('year').size().reset_index(name='Quantity_of_items')
        
    # Quantity of free items of that developer
    total_items = steam_merged[mask_developer].groupby('year').size().reset_index(name='Total_items')
        
    # Merging the results and calculating the percentage of free content
    result = pd.merge(total_items, quantity_free_items, on='year', how='left').fillna(0)
    result['Free_content'] = ((result['Quantity_of_items'] / result['Total_items']) * 100).astype(int)
        
    result = result[['year', 'Quantity_of_items', 'Free_content']].to_dict()

    return result


# def userdata( User_id : str ): Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

def userdata( User_id : str ):

    # Mask user_id
    mask_user = steam_merged['user_id'] == User_id
    # Mask recomend == True
    mask_positive = steam_merged['recommend'] == True
    # Mask recomend == True
    mask_negative = steam_merged['recommend'] == False
    # sum of masks of reviews    
    total_reviews = steam_merged[(mask_positive + mask_negative & mask_user)].count()[0]
    # total items
    total_items = steam_merged[mask_user].count().astype(int)[0]
    # postives reviews
    positive_items = steam_merged[mask_positive & mask_user].count().astype(int)[0]
    # % positive percentage of
    p_percentage = (100*positive_items / total_reviews).astype(int) 
    # Total gasto
    total_gasto = steam_merged[mask_user].agg({'price2': 'sum', 'user_id': 'count'}).rename(index={'user_id': 'cantidad de items', 'price2': 'gasto total'})
    # dictionary with results
    dict_result = {'Usuario':User_id,'Total Items':total_items, '%positivo':p_percentage, 'Total Gasto':total_gasto['gasto total']}

    return dict_result