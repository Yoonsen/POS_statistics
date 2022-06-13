
from collections import Counter
import streamlit as st
import pandas as pd
from PIL import Image
import urllib
import spacy

import dhlab as dh
from dhlab.text.nbtokenizer import tokenize


image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket. Koden benytter en av [spaCys](https://spacy.io/models/nb) modeller for norsk. ')


st.title('Tell opp kategorier i en tekst')


text_input = st.text_area("Lim inn teksten her:", value="Eksempel på tekst.", height=7, help="Hent tekst fra en nettside med ctrl-A ctrl-C (velg alt og kopier), eller kopier for eksempel fra MS Word.")

#w = dh.WordForm(tokenize(text_input.lower()))

if text_input != "":
    nlp = spacy.load("nb_core_news_lg")

    analyze = nlp(text_input)


    res = pd.DataFrame.from_dict(Counter([token.pos_ for token in analyze]), orient='index')
    res.columns = ["Frekvens"]
    res['Prosent'] = res.Frekvens*100/res.Frekvens.sum()

    st.markdown("Statistikk")
    st.write(res.sort_values(by="Frekvens", ascending=False))


    st.markdown("Analyse")
    st.write(pd.DataFrame([(x.text,x.lemma_, x.pos_, x.dep_) for x in analyze], columns=["Ord", "Stamme", "Kategori", "Relasjon"]))