from PIL import Image, ImageFont, ImageDraw, ImageSequence
from rgbmatrix import graphics
import debug
import websocket
import json
import time
import random

class MainRenderer:
    def __init__(self, matrix):
        self.matrix = matrix
        self.canvas = matrix.CreateFrameCanvas()
        self.width = 64
        self.height = 32
        self.font = graphics.Font()
        self.font.LoadFont("/home/michael/message-flexer/fonts/test1.bdf")
        keep_writing = True
        textColor = graphics.Color(255, 255, 255)
        pos = self.canvas.width
        while keep_writing:
            self.canvas.Clear()
            len = graphics.DrawText(self.canvas, self.font, pos, 26, textColor, "ready to go")
            pos -= 1
            if (pos + len < 0):
                keep_writing = False
                pos = self.canvas.width
            time.sleep(0.05)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
        self.canvas.Clear()
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def on_error(self, ws, error):
        print("error: ", error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        print("### opening ###")

    def connect_websocket(self):
        ws = websocket.WebSocketApp("ws://127.0.0.1:3000", on_open = on_open, on_close = on_close)
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        
    def _draw_message(self, wsapp, message):
        my_text = json.loads(message)
        msg = my_text['message']
        self.canvas.Clear()

        if msg == "beer time":
            beers = random.choice([{"file":"/home/michael/message-flexer/assets/small_beers.gif", "loops": 3, "speed": 0.5},
            {"file":"/home/michael/message-flexer/assets/small_slide.gif", "loops": 2, "speed": 0.01},
            {"file":"/home/michael/message-flexer/assets/small_stumble.gif", "loops": 3, "speed": 0.01},
            {"file":"/home/michael/message-flexer/assets/small_cheers.gif", "loops": 2, "speed": 0.01}])
            # beer = Image.open("assets/small_beers.gif")
            beer = Image.open(beers['file'])
            frameNo = 0
            x = 0
            while x is not beers['loops']:
                try:
                    beer.seek(frameNo)
                except EOFError:
                    x += 1
                    frameNo = 0
                    beer.seek(frameNo)
                self.canvas.SetImage(beer.convert('RGB'), 0, 0)
                self.canvas = self.matrix.SwapOnVSync(self.canvas)
                frameNo += 1
                time.sleep(beers['speed'])
        else:
            keep_writing = True
            textColor = graphics.Color(255, 255, 255)
            pos = self.canvas.width
            while keep_writing:
                self.canvas.Clear()
                len = graphics.DrawText(self.canvas, self.font, pos, 26, textColor, msg)
                pos -= 1
                if (pos + len < 0):
                    keep_writing = False
                    pos = self.canvas.width
                time.sleep(0.05)
                self.canvas = self.matrix.SwapOnVSync(self.canvas)
                
        self.canvas.Clear()
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render(self):
        # websocket.enableTrace(True)
        wsapp = websocket.WebSocketApp("wss://socket.ubsub.io/stream?userId=HkBfpcjmt&userKey=aca059f330c46e319a4c2920ef5f60dd5234c603c908f5ef23571b4d1a5825d3&topicId=HJlJV6qoXY",
            on_message = self._draw_message,
            on_error = self.on_error,
            on_close = self.on_close,
            on_open = self.on_open)
        while True:
            wsapp.run_forever()