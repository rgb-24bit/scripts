# -*- coding: utf-8 -*-

from socketserver import BaseRequestHandler, ThreadingTCPServer


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Connected by: %s:%s' % self.client_address)
        while True:
            msg = self.request.recv(1024)
            if not msg:
                break
            self.request.send(msg)


if __name__ == '__main__':
    serv = ThreadingTCPServer(('127.0.0.1', 10086), EchoHandler)
    print('Listening on: %s:%s' % serv.server_address)
    serv.serve_forever()
