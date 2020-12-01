from http.server import BaseHTTPRequestHandler, HTTPServer
import psycopg2

conn = psycopg2.connect(database="test", user="test", password="root", host="postgres", port=5432)
class Handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        self._set_response()
        curr = conn.cursor()
        curr.execute("SELECT * FROM requests")
        data = curr.fetchall()
        print("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self.wfile.write("GET request for {}. Data is: {}".format(self.path, data).encode('utf-8'))
        
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        self._set_response()
        data = str(data.decode('utf-8'))
        curr = conn.cursor()
        curr.execute("INSERT INTO requests (data) VALUES (%s)", (data,))
        print("POST request: {}, {}".format(self.path, data))
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        
def run(server_class=HTTPServer, handler_class=Handler, port=9000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    
if __name__ == '__main__':
    run()
