from socketserver import TCPServer, BaseRequestHandler

class HTTPServer(TCPServer):

    def __init__(self, addr, handler, bind_and_activate=True):
        super().__init__(addr, handler, bind_and_activate)

        # Associates address with a method that returns the MIME type and content
        self.pages = {"/": self.root, "/style.css": self.style }

    def root(self):
        # /
        data = self.__get_file_data("index.html")
        return("text/html; charset=utf-8", data)

    def style(self):
        # style.css
        data = self.__get_file_data("style.css")
        return("text/css; charset=utf-8", data)

    def __get_file_data(self, filename):
        # open and return file data from [filename]
        with open(filename, "r") as fp:
            data = fp.read()
        return data

class HTTPRequestHandler(BaseRequestHandler):

    def handle(self):
        # Handle HTTP request
        # Get the request type
        print("got request")
        data_string = self.request.recv(1024).strip().decode()
        data = data_string.split("\r\n")
        request_type = data[0].split()[0]

        if request_type == "GET":
            response = self.do_get_request(data)
        else:
            response = b""
        print("sending  ")
        self.request.sendall(response)

    def do_get_request(self, data):
        # Handles GET requests
        # Get the web page the user is looking for
        requested_route = data[0].split()[1]
        # Split along / in case the requested page is /<page>/<page2>
        split_route = requested_route.split("/")

        # Check if it is a valid route
        if requested_route not in self.server.pages.keys() and "/"+split_route[1] not in self.server.pages.keys():
            # Page not found
            response = self.assemble_response("404", "NOT FOUND", "text/plain", "Page Not Found")
        else:
            mime, content = self.server.pages[requested_route]()

        # Check for redirect
        response = self.assemble_response("200", "OK", mime, content)
            
        return response

    def assemble_response(self, code, msg, mime, content):
        status = "HTTP/1.1 " + code + " " + msg + "\r\n"
        if code == "200" or code == "404":
            # Build Header fields
            #OK or NOT Found
            try:
                length = "Content-Length: " + str(len(bytes(content,"ascii"))) + "\r\n"
            except UnicodeEncodeError:
                # If the content cannot be converted to ascii, convert to utf-8
                length = "Content-Length: " + str(len(bytes(content, "utf-8"))) + "\r\n"
            except TypeError:
                # For images
                length = "Content-Lenght: " + str(len(content)) + "\r\n"
            no_sniff = "X-Content-Type-Options: nosniff\r\n"
            contenttype = "Content-Type: " + mime + "\r\n\r\n"

            # Construct response
            header =  status + length + no_sniff + contenttype
            response = header.encode("ascii")
        else:
            response = b""
    
        return response


def main():
    print("starting server:")
    HOST, PORT = "0.0.0.0", 8000

    with HTTPServer((HOST, PORT), HTTPRequestHandler) as server:
        server.serve_forever()

if __name__ == "__main__":
    print("before main")
    main()

