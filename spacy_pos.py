
from collections import Counter
import streamlit as st
import spacy_streamlit

import pandas as pd
from PIL import Image
import urllib
import spacy

import dhlab as dh
import dhlab.nbtext as nb
import dhlab.api.dhlab_api as api
from dhlab.text.nbtokenizer import tokenize


@st.cache(suppress_st_warning=True, show_spinner = False)
def get_corpus(freetext=None, title=None, from_year=1900, to_year=2020):
    c = dh.Corpus(freetext=freetext, title=title,from_year=from_year, to_year=to_year)
    return c.corpus

image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket. Koden benytter modeller for norsk utviklet for [spaCy](https://spacy.io/models/nb). ')


st.title('Personer og steder')

#
antall = int(st.sidebar.number_input('enkeltnavn', value=30, min_value=10, max_value = 60, help = "høyere tall gir fler kandidater"))
ratio = st.sidebar.number_input('ratio', value=0.2,min_value=0.1, max_value=0.7, help="lavere tall gir færre kandidater")
## Velg en bok og analyser den


stikkord = st.text_input('Angi noen stikkord for å forme et utvalg tekster, som for eksempel forfatter og tittel, og velg deretter bok fra listen under')
period = st.slider('Begrens listen til år', 1800, 2022, (1980, 2020))
if stikkord == '':
    stikkord = None
corpus = get_corpus(freetext=stikkord, from_year=period[0], to_year=period[1])

choices = [', '.join([str(z) for z in x]) for x in corpus[['authors','title', 'year','urn']].values.tolist()]

with st.form(key='my_form'):
    valg = st.selectbox("Velg et dokument", choices)
    urn = valg.split(', ')[-1]
    submit_button = st.form_submit_button(label='Finn navn')

if submit_button:
    names = nb.names(urn[22:], ratio=ratio, cutoff=2)
    names = [x[0] for x in names[0].most_common(antall)]
    
    #st.write("antall kandidater", len(names))

    if len(names) > 0:
        #parts = [' OR '.join(names[i:i+10]) for i in range(0, len(names), 10)]

        #st.write(urn, urn[22:], parts)
        #w = dh.WordForm(tokenize(text_input.lower()))

        model = "nb_core_news_lg"

        nlp = spacy.load(model)

        #concs = [api.concordance(urns=[urn], words = p, limit = 100) for p in parts]
        concs = []
        st.write('henter data...')
        
        for i,p in enumerate(names):
            try:
                # if i % 20 == 0:
                #     st.write(i)
                concs += list(api.concordance(urns=[urn], words = p, limit = 10).conc.values)
            except:
                st.write(p)
                
        text = " ".join([s for s in concs]).replace('<b>','').replace('</b>','')
        #st.write(concs)
        st.write('analyserer data...')
        parses = nlp(text)

        d = Counter([(x.text, x.label_) for x in parses.ents ]) 
        df = pd.DataFrame([(x,y,d[(x,y)]) for (x,y) in d], columns = ['navn', 'type', 'frekvens'])

        #a = df.pivot_table(index=("type",'navn', 'frekvens'))
        #st.write(a)
        personer = df[df["type"] == "PER"] 
        steder = df[df['type'].str.contains('LOC')]
        col1, col2 = st.columns(2)

        with col1:
            st.header("Navn")
            st.write(personer.sort_values(by='frekvens', ascending = False))

        with col2:
            st.header("Steder")
            st.write(steder.sort_values(by='frekvens', ascending = False))


