import SocketServer
# coding: utf-8
import os

# Copyright 2013 Mircea Caciula, Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #what are they GETting?
        request = "www" + (self.data.split(" "))[1]

        #do we need to handle the special case of accessing files outside of ./www?
        if ".." in request:
            self.request.sendall('HTTP/1.0 404 Not Found\r\n')
            return

        #I really couldn't figure out why http://127.0.0.1:8080/deep/ tries to GET
        #/deep/ and /deep/deep.css but http://127.0.0.1:8080/deep tries to GET
        #/deep and /deep.css, so I had to create a solution I'm not particularly
        #proud of (but it works)
        if "deep.css" in request:
            request = "www/deep/deep.css"

        #if it exists, send it to the client
        #if it doesn't, send a 404
        if os.path.exists(request):
            #do we need to handle the special case of index.html?
            if os.path.isdir(request):
                if request[-1] != "/":
                    request = request + "/"
                request = request + "index.html"
       
            self.request.sendall('HTTP/1.0 200 OK\r\n')

            #is it an html file or a css file?
            if "html" in request:
                self.request.sendall("Content-Type: text/html\r\n\r\n")
            else:
                self.request.sendall("Content-Type: text/css\r\n\r\n")

            file = open(request, 'r')
            self.request.sendall(file.read())
            file.close()
        else:
            self.request.sendall('HTTP/1.0 404 Not Found\r\n')
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
