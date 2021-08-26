from http.server import ThreadingHTTPServer
from http.server import SimpleHTTPRequestHandler
from http import HTTPStatus

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/"):
            self.send_error(HTTPStatus.BAD_REQUEST, "Must be a file, not a folder")
            return None

        if self.path.endswith('htm'):
            self.path += 'l'

        f = None

        try:
            relative_path = self.path[1:]
            f = open(relative_path, 'rb')
            text = f.read()

            self.send_response(200)
            self.send_header('Content-type', self.guess_type(self.path))
            self.send_header('Content-length', len(text))
            self.end_headers()
            self.wfile.write(text)

            f.close()
            return None

        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        


def run(server_class=ThreadingHTTPServer, handler_class=RequestHandler):
    print('Starting server, use <Ctrl-C> to stop')
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()