import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

st.set_page_config(page_title="Surveillance de Paul Midy", layout="wide")

@st.cache_data
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return pd.DataFrame([json.loads(line) for line in f])

# Chargement
try:
    df_mentions = load_data("mentions_paulmidy.json")
except:
    st.error("Fichier 'mentions_paulmidy.json' introuvable.")
    st.stop()

# Analyse de sentiment
analyzer = SentimentIntensityAnalyzer()
df_mentions['sentiment'] = df_mentions['content'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
df_mentions['label'] = df_mentions['sentiment'].apply(lambda x: 'positif' if x > 0.05 else ('négatif' if x < -0.05 else 'neutre'))
df_mentions['date'] = pd.to_datetime(df_mentions['date']).dt.date

# Interface
st.title("Surveillance e-réputation de Paul Midy sur Twitter")
st.subheader("Analyse des tweets contenant 'Paul Midy'")

# Courbe temporelle
sentiment_temps = df_mentions.groupby(['date', 'label']).size().unstack().fillna(0)
st.line_chart(sentiment_temps)

# Tweets récents
st.subheader("Exemples de tweets récents")
st.write(df_mentions[['date', 'content', 'label']].sort_values(by="date", ascending=False).head(10))
