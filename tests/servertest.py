import json
from json.decoder import JSONDecodeError
import asyncio

from tornado.ioloop import IOLoop
from tornado.web import Application, RedirectHandler, RequestHandler
import tornado.gen
from socket import gethostname

class LocalWebController(Application):
    
    def __init__(self, port=8887, mode='manual'):
        ''' 
        Create and publish variables needed on many of 
        the web handlers.
        '''
        print('Starting Donkey Server...', end='')

        self.mode = mode
        self.recording = False
        self.port = port

        handlers = [
            (r"/", RedirectHandler, dict(url="/drive")),
            (r"/drive", DriveAPI),
        ]

        settings = {'debug': True}
        super().__init__(handlers, **settings)
        print("... you can now go to {}.local:8887 to drive "
              "your car.".format(gethostname()))

    def run(self):
        ''' Start the tornado webserver. '''
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.listen(self.port)
        IOLoop.instance().start()

class DriveAPI(RequestHandler):

    def get(self):
        # Set up response dictionary.
        self.response = dict()
        self.response['mode'] = self.mode
        self.response['outgoing_arg_2'] = 12345
        output = json.dumps(self.response)
        self.write(output)

    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            print('Got JSON data:', data)
            self.write({ 'got' : 'your data' })
            for k, v in data.items():
                print(k,v)
        except JSONDecodeError as e:
            print('Could not decode message',self.request.body)

if __name__ == '__main__':
    
    srv = LocalWebController()
    srv.run()


