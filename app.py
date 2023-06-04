import os
import random
import json
import pickle
import sys
import numpy as np
import nltk
import time
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import load_model
from flask import Flask, render_template_string, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json", encoding="utf-8").read())

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

def train_model():
    lemmetizer = WordNetLemmetizer()
    intents = json.loads(open("intents.json", encoding="utf-8").read())
    words = []
    classes = []
    documents = []
    ignore_letters = ["?", ".", "!", ","]

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list, intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    words = [lemmetizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words))

    classes = sorted(set(classes))

    pickle.dump(words, open("words.pkl", "wb"))
    pickle.dump(classes, open("classes.pkl", "wb"))

    training = []
    output_empty = [0] * len(classes)

    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmetizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)

    training_x = list(training[:, 0])
    training_y = list(training[:, 1])

    model = Sequential()
    model.add(Dense(128, input_shape=(len(training_x[0]),), activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(training_y[0]), activation="softmax"))

    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

    mychatbotmodel = model.fit(
        np.array(training_x), np.array(training_y), epochs=2000, batch_size=5, verbose=1
    )
    model.save("chatbotmodel.h5", mychatbotmodel)
    print("Done")

model = load_model("chatbotmodel.h5")

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

@app.route("/uploadfile", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        filename = secure_filename(file.filename)  # type: ignore
        if filename != "intents.json":
            return "Wrong file name", 400
        file.save(filename)
        try:
            train_model()  # Spustite trénovanie modelu
            os.execv(sys.executable, ["python"] + sys.argv)
            return "File uploaded and model training started", 200
        except Exception as e:
            return str(e), 500
    return render_template_string(
        """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file style="margin: 30px 0;">
      <input type=submit value=Upload>
    </form>
    """
    )



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

def run():
    try:
        app.run(host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        run()

@app.route("/restart", methods=["POST"])
def restart():
    time.sleep(1)
    os.kill(os.getpid(), signal.SIGINT)
    return "Server is restarting..."


if __name__ == "__main__":
    run()
