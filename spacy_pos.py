
from collections import Counter
import streamlit as st
import spacy_streamlit

import pandas as pd
from PIL import Image
import urllib
import spacy

import dhlab as dh
from dhlab.text.nbtokenizer import tokenize


@st.cache(suppress_st_warning=True, show_spinner = False)
def get_corpus(freetext=None, title=None, from_year=1900, to_year=2020):
    c = dh.Corpus(freetext=freetext, title=title,from_year=from_year, to_year=to_year)
    return c.corpus

image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket. Koden benytter modeller for [spaCys](https://spacy.io/models/nb) for norsk (bokmål). ')


st.title('Personer og steder i teksten')


stikkord = st.text_input('Angi noen stikkord for å forme et utvalg tekster, som for eksempel forfatter og tittel, og velg deretter bok fra listen under')

text_input = st.text_area("Lim inn teksten her:", value="Eksempel på tekst.", height=7, help="Hent tekst fra en nettside med ctrl-A ctrl-C (velg alt og kopier), eller kopier for eksempel fra MS Word.")

#w = dh.WordForm(tokenize(text_input.lower()))
model = "nb_core_news_lg"

doc = spacy_streamlit.process_text(model, text_input)


spacy_streamlit.visualize_ner(
    doc,
    show_table=True,
    title="Persons, dates and locations",
)

# if text_input != "":
#     nlp = spacy.load("nb_core_news_sm")

#     analyze = nlp(text_input)


#     res = pd.DataFrame.from_dict(Counter([token.pos_ for token in analyze]), orient='index')
#     res.columns = ["Frekvens"]
#     res['Prosent'] = res.Frekvens*100/res.Frekvens.sum()

#     st.markdown("Statistikk")
#     st.write(res.sort_values(by="Frekvens", ascending=False))


#     st.markdown("Analyse")
#     st.write(pd.DataFrame([(x.text,x.lemma_, x.pos_, x.dep_) for x in analyze], columns=["Ord", "Stamme", "Kategori", "Relasjon"]))