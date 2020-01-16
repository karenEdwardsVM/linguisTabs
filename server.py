#!/usr/bin/env python3 
import flask
from flask import Flask, render_template, request
import random
import sqlite3
import json
from vocabulary import mostMots, manyPhrases

app = Flask(__name__)

def initDB():
    createTableQuery = """create table if not exists frenchVocab (
                            id integer primary key autoincrement, 
                            word text not null, 
                            definition text not null, 
                            keyword text default null,
                            unique(word, definition)
                          );"""

    addWordsQuery = """insert or ignore into 'frenchVocab' (word, definition) 
                       values (:0, :1);"""

    connect = sqlite3.connect("vocab.db")
    cursor = connect.cursor()
    cursor.execute(createTableQuery)
    cursor.executemany(addWordsQuery, mostMots)
    connect.commit()
    cursor.close()

def getRow():
    with sqlite3.connect("vocab.db") as connect:
        cursor = connect.cursor()
        cursor.execute("select count(*) from frenchVocab;")
        rowCount = cursor.fetchone()[0]
        rowNum = random.randint(1, rowCount)
        cursor.execute("""select * from frenchVocab where id = ?;""", (rowNum,))
        chosenRow = cursor.fetchall()
    
    return {"word":chosenRow[0][1], "definition":chosenRow[0][2], "keyword":chosenRow[0][3]}

@app.route('/setKeyword', methods=['POST'])
def setKeyword(): 
    data = flask.request.get_json()
    with sqlite3.connect("vocab.db") as connect:
        cursor = connect.cursor()
        cursor.execute("""update frenchVocab set keyword = ? where word = ?;""", (data["keyword"], data["word"]))
        connect.commit()
        cursor.execute("""select * from frenchVocab where word = ?;""", (data["word"],))
    return {"message": "success"}

@app.route('/')
def randWord():
    randRow = json.dumps(getRow())
    #return render_template('displayWords.html', randRow=randRow)
    return render_template('randWord.html', randRow=randRow)

if __name__ == '__main__':
    try: 
        initDB()
        app.run(debug = False, port = 6970)
    finally: 
        if connect: 
            connect.close()
        print("sqlite connection closed")
