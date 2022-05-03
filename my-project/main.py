import os

from flask import Flask, render_template, request, abort
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage,
    ImageMessage, VideoMessage
)

from modules.conversation import line_conversation
from modules.operate_firebase import register_message
# from modules.write_tmp import read_temporary
from settings.line_init import line_bot_api, handler
# from test_line import line_bot_api, handler  # debug

app = Flask(__name__)


@app.route("/")
def hello_world():
    param = {
        'title': 'Index',
        'message': 'Myhabits with Line-Bot'
    }
    # file_lines = read_temporary('test')
    # param.update({'file_lines': file_lines})
    # sche: display firebase-data 
    return render_template('index.html', param=param)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    register_message(body, 1)
    # get profile
    # message_source = ast.literal_eval(body)['events'][0]['source']
    # if message_source['type'] == 'user':
    #     user_id = message_source['userId']
    # handle webhook body
    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_conversation(event, line_bot_api)


@handler.add(MessageEvent, message=[ImageMessage, VideoMessage])
def handle_content(event):
    def get_contents(message_id, file_path:str='./tmp.png'):
        """コンテンツを取得する
        """
        content = line_bot_api.get_message_content(message_id)
        with open(file_path, 'wb') as fd:
            for chunk in content.iter_content():
                fd.write(chunk)
    get_contents(event.id)


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)