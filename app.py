from flask import Flask, request, jsonify
from chat_downloader import ChatDownloader
import gc
import json


app = Flask(__name__)

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
        return jsonify(chat_data)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == '__main__':
        app.run()