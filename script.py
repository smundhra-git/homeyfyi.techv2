import requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
from typing import Dict
import pathlib
from openai import OpenAI
import openai
from textblob import TextBlob
from transformers import pipeline


def calculate_sustainability_ratings(file_path):
    # Load the dataset
    df = pd.read_csv(file_path, low_memory=False)

    # Including the Property ID in the DataFrame
    df_sustainability = df[[
        'Property Id',  # Property ID column
        'Latitude',
        'Longitude',
        'Total GHG Emissions (Metric Tons CO2e)',
        'Property GFA - Self-Reported (ft²)',
        'Site EUI (kBtu/ft²)',
        'Weather Normalized Source EUI (kBtu/ft²)',
        'Water Use (All Water Sources) (kgal)',
        'Percent of Total Electricity Generated from Onsite Renewable Systems',
        'ENERGY STAR Score'
    ]].copy()

    # Convert columns to numeric, handling errors, except for 'Property Id'
    numeric_columns = df_sustainability.columns.drop(['Property Id','Latitude', 'Longitude'])
    df_sustainability[numeric_columns] = df_sustainability[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Replace inf/-inf with NaN, then handle NaN values
    df_sustainability.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_sustainability.fillna(0, inplace=True)

    # Log transformation for `sp`ecific columns
    for column in ['Total GHG Emissions (Metric Tons CO2e)', 'Property GFA - Self-Reported (ft²)', 
                   'Site EUI (kBtu/ft²)', 'Weather Normalized Source EUI (kBtu/ft²)', 
                   'Water Use (All Water Sources) (kgal)']:
        df_sustainability[column] = np.log1p(df_sustainability[column])

    # Store and drop Property Id for normalization
    property_ids = df_sustainability['Property Id']
    latitudes = df_sustainability['Latitude']
    longitudes = df_sustainability['Longitude']
    df_sustainability.drop(columns=['Property Id', 'Latitude', 'Longitude'], inplace=True)
    
    # Apply MinMaxScaler
    scaler = MinMaxScaler()
    df_sustainability_scaled = scaler.fit_transform(df_sustainability)
    df_sustainability = pd.DataFrame(df_sustainability_scaled, columns=df_sustainability.columns)

    # Calculate the composite sustainability score
    df_sustainability['Composite Sustainability Score'] = df_sustainability.mean(axis=1)

    # Normalize the composite score to a scale of 0-100
    df_sustainability['Normalized Sustainability Score'] = df_sustainability['Composite Sustainability Score'] * 100

    # Add the property IDs back to the DataFrame
    df_sustainability['Property Id'] = property_ids
    df_sustainability['Latitude'] = latitudes
    df_sustainability['Longitude'] = longitudes

    # Return the dataframe sorted by sustainability score
    return df_sustainability[['Property Id', 'Latitude', 'Longitude', 'Normalized Sustainability Score']].sort_values(by='Normalized Sustainability Score', ascending=False)


# Usage

def get_coordinates(api_key, location):
#Get the latitude and longitude of a location using Google Geocoding API.
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    try:
        response = requests.get(base_url, params={"address": location, "key": api_key})
        response.raise_for_status()
        response_json = response.json()

        if response_json["status"] == "OK":
            result = response_json["results"][0]
            return result["geometry"]["location"]["lat"], result["geometry"]["location"]["lng"]
        else:
            return None, None
    except requests.RequestException as e:
        return None, None

def haversine_vectorized(df, lat1, lon1):
#Vectorized calculation of distances between two sets of points.
    lat2 = df['Latitude'].astype(float)
    lon2 = df['Longitude'].astype(float)

    R = 6371 # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    distance = R * c
    return distance

def find_nearest_locations(api_key, location, df, k):
#Find the k nearest locations to the given location.
    lat, lon = get_coordinates(api_key, location)
    if lat is None or lon is None:
        return "Invalid location or API key."

    # Sort the dataframe first by distance, then by normalized sustainability score
    df['Distance'] = haversine_vectorized(df, lat, lon)
    df_sorted = df.sort_values(by=['Distance', 'Normalized Sustainability Score'], ascending=[True, False])

    # Return the top k rows
    return df_sorted.head(k)[['Property Id', 'Distance', 'Normalized Sustainability Score']]

# find closest results



def return_nearest_scores(location = "", k = 3):
    ESG_API_KEY = "AIzaSyCemo-YZEd0EWrbat0G8g2XjUrX3ZvcdZk"
    filename = "./Energy_and_Water_Data_Disclosure_for_Local_Law_84_2021__Data_for_Calendar_Year_2020_.csv" 
    sustainability_scores = calculate_sustainability_ratings(filename)
    if location == "":
        return 50

    try:
        nearest_locations = find_nearest_locations(ESG_API_KEY, location, sustainability_scores, k)
        average_score = nearest_locations['Normalized Sustainability Score'].mean()
        return average_score
    except:
        return 50

arcc_api_key = os.environ.get('ARCC_API_KEY')
#get_file_type
def get_file_type(filename: str) -> str:
   type_mapper = {'.png': 'image/png', '.jpg': 'image/jpeg', 'jpg': 'image/jpeg', '.mp4': 'video/mp4'}
   file_extension = pathlib.Path(filename).suffix
   if file_extension in type_mapper:
       return type_mapper[file_extension]
   raise Exception(f'Unknown file extension: {file_extension}')



#upload file
def post_files(filename: str, api_key):
    url = 'https://api.archetypeai.dev/v0.3/files'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    with open(filename, 'rb') as file_handle:
        encoder = MultipartEncoder({
            'file': (os.path.basename(filename), file_handle, get_file_type(filename))
        })
        response = requests.post(url, data=encoder, headers={**auth_headers, 'Content-Type': encoder.content_type})
        return response.status_code, response.json() if response.status_code == 200 else {}

# def delete_files(filename: str, api_key = arcc_api_key):
#    url = 'https://api.archetypeai.dev/v0.3/files'
#    auth_headers = {"Authorization": f'Bearer {api_key}'}
#    with open(filename, 'rb') as file_handle:
#        encoder = MultipartEncoder({'file': (os.path.basename(filename), file_handle.read(), get_file_type(filename))})
#        response = requests.delete(url, data=encoder, headers={**auth_headers, 'Content-Type': encoder.content_type})
#        response_data = response.json() if response.status_code == 200 else {}
#        return response.status_code, response_data



#summarize the image for me
def summarize(file_ids, api_key = arcc_api_key):
    url = 'https://api.archetypeai.dev/v0.3/summarize'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    query = "Analyze the provided images of the house with a focus on promptly identifying and diagnosing specific details that reveal immediate structural or functional concerns. Look for signs of wear, damage, or any anomalies that suggest potential issues, including but not limited to cracks in the foundation, roof damage, water intrusion, mold growth, and signs of pest infestation. Evaluate the condition of visible structural elements and any utilities or systems captured in the images. Provide a detailed report on each identified concern, specifying its nature, location, and the potential impact on the house's safety and functionality. Highlight the urgency of any findings, categorizing them by the level of immediate action required to address them."
    data_payload = {'query': query, 'file_ids': file_ids}
    response = requests.post(url, data=json.dumps(data_payload), headers=auth_headers)
    response_data = response.json() if response.status_code == 200 else {}
    return response.status_code, response_data

#describe the image for me
def describe(query: str, file_ids, api_key = arcc_api_key):
    url = 'https://api.archetypeai.dev/v0.3/describe'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    data_payload = {'query': query, 'file_ids': file_ids}
    response = requests.post(url, data=json.dumps(data_payload), headers=auth_headers)
    response_data = response.json() if response.status_code == 200 else {}
    return response.status_code, response_data


def get_summarized_test(value_res):
  return value_res['response']['processed_text']

def gpt_helper(prompt):
    client = OpenAI(api_key = "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")
    ask_gpt(prompt)

def ask_gpt(prompt, engine="text-davinci-003"):
    """
    Send a prompt to OpenAI's ChatGPT and return the output.

    :param prompt: The prompt to send to ChatGPT.
    :param api_key: Your OpenAI API key. If None, expects OPENAI_API_KEY environment variable to be set.
    :param engine: The OpenAI engine to use. Defaults to "text-davinci-003".
    :return: The output from ChatGPT as a string.
    """
    client = OpenAI(api_key = "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")
    api_key = "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"
    # Ensure the API key is provided either directly or through the environment
    if api_key is None:
        raise ValueError("API key must be provided or set as an environment variable.")

    # Initialize the OpenAI API client with the provided API key
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    prompt1 = "\n Based on an FPV analysis detailing structural integrity, aesthetic condition, and visible wear or damage, predict potential issues within the next 3-6 months. Consider age, maintenance history, environmental exposure, and defects. Provide insights on immediate and future concerns, focusing on both minor and major aspects affecting stability and safety. Summarize in 500 characters: should one buy this house? Highlight the good, the bad, and required fixes."
    prompt = prompt + prompt1
    # Send the prompt to ChatGPT and get the response
    response = client.chat.completions.create(
        messages = [{
            "role" : "user",
            "content" : prompt

        }],
        model = "gpt-3.5-turbo"
    )

    # Extract and return the text of the response
    return response

later_use = ""
def summarize_files_and_get_insights(files, text = ""):
    size = len(text)
    later_use = text
    arcc_api_key = "gt51b6ea"
    for file_name in files:
        # Assuming post_files and summarize functions are correctly implemented
        #post_files(file_name, arcc_api_key)  # Ensure this function is correctly defined to handle file uploads
        #query = "Generating the top three insights as tailored maintenance and protection recommendations for homeowners, based on the individual condition of their house. What would you happen in 3-6 months if we keep the house this way?"
        status_code, data = summarize([file_name], arcc_api_key)
        if status_code == 200:
            Sum_data = get_summarized_test(data)
            text += "\n" + Sum_data
        else:
            # Handle error
            pass
    return text

def analyze_sentiment_and_get_score(Data_Summary, location = ""):
    res = ask_gpt(Data_Summary + later_use)
    text = res.choices[0].message.content
    # Normalize to 0-1 scale for TextBlob
    blob = TextBlob(text)
    textblob_score = (blob.sentiment.polarity + 1) / 2

    # Ensure text is within limits for transformers
    text = text[:511]

    # Specify the model and revision explicitly
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    model_revision = "af0f99b"  # Example revision, adjust as needed

    transformer_pipeline = pipeline("sentiment-analysis", model=model_name, revision=model_revision)
    transformer_result = transformer_pipeline(text)
    if transformer_result[0]['label'] == 'POSITIVE':
        transformers_score = transformer_result[0]['score']
    else:
        transformers_score = 1 - transformer_result[0]['score']  # Convert to a 0-1 scale

    combined_env_score = (textblob_score + transformers_score) / 2
    combined_environment_score = return_nearest_scores(location, 3)
    combined_score = int((combined_env_score*50) + (0.5*combined_environment_score))
    return combined_score


