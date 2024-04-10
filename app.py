from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

SONGS = pd.read_csv('spotify_songs.csv', encoding='latin-1', sep=';').transpose().to_dict()

max_id = 952

# retorna lista com todas músicas
@app.get("/songs")
def getSongs():
    return jsonify(SONGS)


# retorna uma música específica
#http://localhost:5000/song/<id>
@app.get("/song/<int:id>")
def getSong(id):
    try:
        return SONGS[id], 200
    except:
        return {"erro": "Musica nao encontrada"}, 404

# busca de uma múscica para um id específico
# ID aqui deve ser passado como um argumento na URL
# http://localhost:5000/song?id=valor
@app.get("/song")
def getSongByQuery():
    id = request.args.get('id',type=int)
    try: 
        return SONGS[id], 200
    except:
        return {"erro": "musica nao encontrada"}, 404

@app.put("/song/<int:id>")
def updateSong(id):
    try:
        artist_name =  request.json["artist(s)_name"]
        streams = request.json["streams"]
        track_name = request.json["track_name"]

        SONGS[id]["artist(s)_name"] = artist_name
        SONGS[id]["streams"] = streams
        SONGS[id]["track_name"] = track_name

        return "updated", 200

    except:
        return {"erro": "id nao encontrado"}, 404

    


#Adiciona um nova música recebendo um JSON
@app.post("/song")
def addSong():
    if request.is_json:
        song = request.get_json()
        global max_id
        max_id += 1
        song['id'] = max_id
        SONGS[max_id] = song
        return {'id':max_id}, 201
    return {"erro":"Formato deve ser JSON"}, 415

#Remove música pelo id passado como variável na URL
#http://localhost:5000/song/<id>
@app.delete("/song/<int:id>")
def deleteSong(id):
    if id in SONGS:
        del SONGS[id]
        return "removido", 200
        
    return {"erro": 'musica nao encontrada'}, 404
