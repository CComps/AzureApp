import os
import random
import json
import pickle
import numpy as np
import nltk
import time
import webbrowser
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from gtts import gTTS
from flask import Flask, request, jsonify

try:
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("omw-1.4")
    nltk.download("*")
except:
    pass

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json", encoding="utf-8").read())

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))
model = load_model("chatbotmodel.h5")


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["response"])
            break
    return result


@app.route("/", methods=["GET"])
def home():
    text = request.args.get("text")
    if text is not None:
        ints = predict_class(text)
        res = get_response(ints, intents)

        with open("log.log", "a", encoding="utf-8") as f:
            f.write(f"Text: {text}; AI: {res};\n")
        # check if the res is a url
        if "http" in res:
            response = {"answer": res, "question": text}
            return jsonify(response)

        else:
            response = {"answer": res, "question": text}
            return jsonify(response)
    else:
        return "Please provide a text parameter."


if __name__ == "__main__":
    app.run()
