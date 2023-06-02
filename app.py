from flask import Flask
from flask import request
from chat_downloader import ChatDownloader
import json


app = Flask(__name__)

@app.get('/')
def index():
    try:
        chat = ChatDownloader().get_chat("https://www.youtube.com/watch?v=" + request.args.get('id'), message_groups=['messages','superchat'])
        chat_data = []
        for message in chat:
            message["author"]["images"] = message["author"]["images"][2]["url"]

            # if "badges" in message["author"]:
            #     message["author"]["badges"] = message["author"]["badges"][0]["title"]

            if "emotes" in message:
                del message["emotes"]

            # if "message_type" in message:
            #     del message["message_type"]

            if "action_type" in message:
                del message["action_type"]

            chat_data.append(message)
        return json.dumps(chat_data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == '__main__':
        app.run()