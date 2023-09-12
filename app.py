from flask import Flask, request, jsonify
from chat_downloader import ChatDownloader
from pytube import YouTube
import gc
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

request_counter = 0  # Contador de requisições

@app.after_request
def cleanup(response):
    global request_counter

    # Incrementa o contador de requisições
    request_counter += 1

    # Limpa a memória a cada 5 requisições
    if request_counter % 5 == 0:
        gc.collect()

    return response


@app.get('/')
def index():
    try:
        video = YouTube(f'https://www.youtube.com/watch?v=' + request.args.get('id'))

        # Obter dados do vídeo
        title = video.title
        thumb = video.thumbnail_url
        publish_date = video.publish_date
        views = video.views
        duration = video.length

        # Obter dados do canal
        channel_title = video.author
        


        chat = ChatDownloader().get_chat("https://www.youtube.com/watch?v=" + request.args.get('id'), message_groups=['messages', 'superchat'])
        chat_data = []
        for message in chat:
            message["author"]["images"] = message["author"]["images"][2]["url"]

            if "badges" in message["author"]:
                message["author"]["badges"] = message["author"]["badges"][0]["title"]

            # if "emotes" in message:
            #     del message["emotes"]

            # if "message_type" in message:
            #     del message["message_type"]

            # if "action_type" in message:
            #     del message["action_type"]

            chat_data.append(message)

        data = {
            "video": {
                "title": title,
                "publish_date": publish_date,
                "views": views,
                "channel_title": channel_title,
                "thumb": thumb,
                "duration": duration
            },
            "chat": chat_data
        }
        return jsonify(data)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == '__main__':
        app.run()