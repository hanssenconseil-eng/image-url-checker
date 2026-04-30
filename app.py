#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import requests
from PIL import Image
import imagehash
from io import BytesIO

REFERENCE_URL = "https://www.etatpur.es/media/catalog/product/b/f/bf597016e078a87e85df6a92e5b26b77-_7b151144_7d__7b_7d__7b06vb1035003_7d.jpg"
THRESHOLD = 5


def load_image(url):
    try:
        r = requests.get(url, timeout=10)
        return Image.open(BytesIO(r.content)).convert("RGB")
    except:
        return None


def get_hash(img):
    return imagehash.phash(img)


st.title("Image URL Checker")

uploaded_file = st.file_uploader("Choisir un fichier CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = df[["ProductCode", "DisplayUrl"]].copy()

    st.write("Aperçu des données")
    st.dataframe(df)

    if st.button("Lancer analyse"):
        ref_img = load_image(REFERENCE_URL)
        ref_hash = get_hash(ref_img)

        results = []
        progress = st.progress(0)

        total = len(df)

        for i, url in enumerate(df["DisplayUrl"]):
            img = load_image(url)

            if img is None:
                results.append("PAS D'IMAGE")
            else:
                diff = ref_hash - get_hash(img)
                results.append("ERREUR D'URL" if diff < THRESHOLD else "Validé")

            progress.progress((i + 1) / total)

        df["URL"] = results

        st.success("Analyse terminée")

        st.write("Statistiques")
        st.write(df["URL"].value_counts())

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "Exporter CSV",
            data=csv,
            file_name="result.csv",
            mime="text/csv"
        )


# In[ ]:




