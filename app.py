import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stop_words and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


tfidf = pickle.load(open('model/vectorizer.pkl', 'rb'))
model = pickle.load(open('model/model.pkl', 'rb'))

st.title("SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button("Predict"):

    if input_sms.strip() == "":
        st.warning("Please enter a message")

    else:
        transformed_sms = transform_text(input_sms)

        st.write("Processed Text:")
        st.code(transformed_sms)

        vector_input = tfidf.transform([transformed_sms])

        result = model.predict(vector_input)[0]
        probability = model.predict_proba(vector_input)[0][1]

        if result == 1:
            st.header("Spam")
        else:
            st.header("Not Spam")

        st.write(f"Spam Confidence: {probability * 100:.2f}%")

        if probability > 0.8:
            st.info("Message contains promotional or suspicious patterns.")