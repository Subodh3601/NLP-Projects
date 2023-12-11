import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


def preprocessed_text(text):
    text = text.lower()  # lower case
    text = nltk.word_tokenize(text)  # word tokenizaztion

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


st.title('SMS spam classifier')

input_sms = st.text_input('Enter the sms')

if st.button('Predict'):

    # stes
    # 1. preprocess
    transformd_sms = preprocessed_text(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform(transformd_sms)
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
