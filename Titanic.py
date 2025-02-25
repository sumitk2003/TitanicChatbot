import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import requests
import os


file_path = os.path.join(os.path.dirname(__file__), "Titanic.csv")


df = pd.read_csv(file_path)

Titanic_app = FastAPI()
 

Titanic_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@Titanic_app.get("/stats")
def get_stats():
    return {
        "total_passengers": len(df),
        "male_percentage": df['Sex'].value_counts(normalize=True)['male'] * 100,
        "avg_fare": df['Fare'].mean(),
        "embarked_counts": df["Embarked"].value_counts().to_dict(),
    }



def run_fastapi():
    uvicorn.run(Titanic_app, host="127.0.0.1", port=8008)




threading.Thread(target=run_fastapi, daemon=True).start()


st.title("Titanic Chatbot 🚢")
st.write("Ask questions about the Titanic dataset!")

question = st.text_input("Enter your query:")

if question:
    if "percentage of passengers were male" in question.lower():
        response = requests.get("http://127.0.0.1:8008/stats").json()
        st.write(f"Approximately {response['male_percentage']:.2f}% of passengers were male.")

    elif "average ticket fare" in question.lower():
        response = requests.get("http://127.0.0.1:8008/stats").json()
        st.write(f"The average ticket fare was ${response['avg_fare']:.2f}.")

    elif "histogram of passenger ages" in question.lower():
        fig, ax = plt.subplots()
        sns.histplot(df["Age"].dropna(), bins=20, kde=True, ax=ax)
        st.pyplot(fig)

    elif "passengers embarked from each port" in question.lower():
        response = requests.get("http://127.0.0.1:8008/stats").json()
        st.write("Passengers per embarkation port:")
        st.write(response["embarked_counts"])
