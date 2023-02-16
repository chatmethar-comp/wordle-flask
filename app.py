# import Flask library
from flask import Flask, Response, request, session, render_template, redirect
import requests
import random
from datetime import timedelta

app = Flask(__name__)  # __name__ is defined

# Session Handling
app.secret_key = "_#Programming 4$%"  # set "common key" to encrypt
app.session_cookie_name = "PG4_session"
app.permanent_session_lifetime = timedelta(
    minutes=30)  # set session lifetime to 10mins


@app.route("/rescore", methods=["GET"])
def rescore():
    session.clear()
    session["score"] = [0, 0, 0, 0, 0, 0, 0]
    return redirect("/")


@app.route("/logout", methods=["GET"])
def clear():
    # session.clear()
    session.pop('word', default=None)
    session.pop('history', default=None)
    return redirect("/")
    # return Response("Session invalidated", mimetype="text/plain")


@app.route("/", methods=["GET"])  # map the URL "/" for a function below
def begin():
    # read dict
    try:
        if session.get("word", None) == None:
            dict_req = requests.get(
                "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt")
            dict_array = dict_req.text.splitlines()
            session["word"] = dict_array[random.randint(
                0, len(dict_array) - 1)]
            session["history"] = list()
            if session.get("score", None) == None:
                session["score"] = [0, 0, 0, 0, 0, 0, 0]

    except requests.exceptions.RequestException:  # just handle exceptions regarding HTTP
        return Response("Something went wrong to retrieve data", mimetype='text/plain')

    # session["word"] and session["history"] have data
    return render_template("wordle.html", current="", word=session["word"], history=session["history"], message="Let's get started!", score=session["score"])


@app.route("/", methods=["POST"])  # map the URL "/" for a function below
def ontheway():
    query = request.form["query"]

    try:
        word = session["word"]
        history = session["history"]
        try:
            score = session["score"]
        except:
            rescore()

        # check word length
        if len(query) != len(word):
            return render_template("wordle.html", current=history, word=word, history=history, message="Enter 5 letters word!!", score=score)
        # check word is valid!
        dict_req = requests.get(
            "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt")
        dict_array = dict_req.text.splitlines()
        if query not in dict_array or query in history:
            return render_template("wordle.html", current=history, word=word, history=history, message="Word not valid", score=score)
        # check word is valid!
        history.append(query)
        session["history"] = history

        if query == word:
            session.pop('word', default=None)
            session.pop('history', default=None)
            # score.append(len(history))
            scores = session["score"]
            scores[len(history)] += 1
            return render_template("wordle.html", current=query, word=word, history=history, message="Correct!", score=score)
        else:
            if len(history) == 6:
                return render_template("wordle.html", current=query, word=word,
                                       history=history, message="Game OVER!!", End=1, score=score)
            return render_template("wordle.html", current=query, word=word, history=history, message="Try again!", score=score)
    except Exception as e:
        print(e)
        return Response("Something went wrong to retrieve data: " + str(e), mimetype='text/plain')
