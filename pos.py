import streamlit as st
import dhlab.text as dh
import pandas as pd
from PIL import Image
import urllib

max_conc = 20000

@st.cache(suppress_st_warning=True, show_spinner = False)
def konk(corpus = None, query = None): 
    concord = dh.Concordance(corpus, query, limit = max_conc)
    return concord

@st.cache(suppress_st_warning=True, show_spinner = False)
def korpus():
    corpusdata =  pd.read_csv('vannkorpus.csv', index_col = 0)
    corpus = dh.Corpus_from_identifiers(list(corpusdata.urn.values))
    return corpus

def set_markdown_link_conc(conc, corpus, query):
    corps = corpus.corpus.set_index('urn')
    conc['link'] = conc['urn'].apply(lambda c: "[{display}](https://www.nb.no/items/{x}?searchText={q})".format(x = c, display = f"{corps.loc[c].title} - {corps.loc[c].authors} : {corps.loc[c].year}" , q = urllib.parse.quote(query)))
    return conc[[
        'link', 'concordance'
    ]]

water_corpus = korpus()
#st.write(post_memory_corpus.corpus)

image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket')


st.title('Søk i bøker fra korpuset Norgeshistorie')


words = st.text_input(
    'Søk etter ord og fraser', 
    "vasshjul*", 
    help="Bruk anførselstegn for å gruppere fraser. Trunker med * etter ord. Kombiner med OR eller AND. For ord nær hverandre bruk NEAR(ord1 ord2, Antall ord i mellom)")

concord_dh = konk(corpus = water_corpus, query = words)

samplesize = int(
    st.number_input(
        "Vis et visst antall konkordanser i gangen:", 
        min_value=5,
        value=100, 
        help="Minste verdi er 5, default er 100"
    )
)

konk = set_markdown_link_conc(
    concord_dh.show(
        style=False, 
        n=int(samplesize)
    ), 
    water_corpus, 
    words
)
    
st.markdown(f"## Konkordanser for __{words}__")

if samplesize < concord_dh.size:
    if st.button(f"Klikk her for flere konkordanser. Sampler {samplesize} av {concord_dh.size}"):
        #st.write('click')
        konk = set_markdown_link_conc(concord_dh.show(style=False, n=int(samplesize)), water_corpus, words)
else:
    if concord_dh.size == 0:
        st.write(f"Ingen treff")
    else:
        st.write(f"Viser alle {concord_dh.size} konkordansene ")
        
st.markdown('\n\n'.join(
    [f"{r[1][0]}  {r[1][1]}" for r in konk.iterrows()]
).replace('<b>','**').replace('</b>', '**'))

