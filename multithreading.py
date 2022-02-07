from asyncio.subprocess import STDOUT
import mimetypes
import os
import socket
import subprocess
import threading
class HTTPServer:
    '''
        Remove the pass statement below and write your code here
    '''
    def _init_(self,host,port) :

        self._host = host
        self._port = port
        self.rootdirectory = os.getcwd()
        self.sock = socket.socket()
        self.seraddress = (self._host, self._port)
        self.sock.bind(self.seraddress)
        self.start()

    def start(self): 
        self.sock.listen()
        while True:
            print('waiting for connection ---')
            c,cip = self.sock.accept()
            self.clienturl(c)
            process=threading.Thread(target=self.clienturl,args=(c,))
            process.start()
            process.join()

    def clienturl(self,c):

            msg = c.recv(1024).decode()
            msg_headers = msg.splitlines()
            file_name = msg_headers[0].split(" ")[1] 
            url = os.getcwd() + file_name
            if file_name == '/':
                self.disp(c)
            elif file_name == '/www':
                self.Ls(url,file_name,c) 
            elif 'bin' in file_name:
                self.Dynamiccontent(url,file_name,c)
            elif os.path.isfile(url):
                self.Staticcontent(url,c)
            else:
                c.send("HTTP/1.1 404 Failed\r\n".encode())

    def Ls(self,url,file_name,c):
            
                res = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 1024\nConnection: Closed\n\n"
                for subdirs,dirs,files in os.walk(url):
                    for file in files:
                        res+= "<html><body><a href" + "=" + os.path.join(file_name,file) + ">"+file+"</a><br></body></html>\r\n\r\n" +"\r\n"
                c.sendall(res.encode())
    
    def Staticcontent(self,url,c): 
        
                f = open(url,'rb')
                req_file = f.read()
                f.close()
                file = os.path.basename(url) 
                Content_Type = mimetypes.MimeTypes().guess_type(file)[0] 
                Content_Length = len(req_file)
                res = f"HTTP/1.1 200 OK\n Content-Type: {Content_Type} \n Content-Length: {Content_Length} \n Connection: closed\n\n"
                response = res.encode()
                resbytes = response + req_file
                c.sendall(resbytes)
                
    def Dynamiccontent(self,url,file_name,c):
                if file_name == '/bin' :
                    response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 1024\nConnection: Closed\n\n"
                    for root,dir,files in os.walk(url):
                        for file in files:
                            response+= "<html><body><a href" + "=" + os.path.join(file_name,file) + ">"+file+"</a><br></body></html>\r\n\r\n" +"\r\n"
                    c.sendall(response.encode())
                elif file_name=='/bin/test.py':
                    process=subprocess.Popen('python D:\\ComputerSystems-p3\\ComputerSystems-p3\\bin\\test.py', shell=True, stdout=subprocess.PIPE)
                    comm = process.communicate()[0]
                    d=comm.decode()
                    data= "HTTP/1.1 200 OK\nContent-Type: text/plain \n Content-Length: 1024\nConnection: Closed\n\n"
                    data=data.encode()
                    res=data+d.encode()
                    c.sendall(res) 
                elif file_name=='/bin/ls' :
                    res = os.popen('dir/w')
                    read=res.read()
                    data= "HTTP/1.1 200 OK\nContent-Type: text/plain \n Content-Length: 1024\nConnection: Closed\n\n"
                    data=data.encode()
                    res=data+read.encode()
                    c.sendall(res)
                
    def disp(self,c):
                    
                data = "HTTP/1.1 200 OK\r\n"
                data += "Content-Type: text/html \r\n"
                data += "Content-Length: "+ str(1024) + "\r\n"
                data += "Connection: closed\r\n" 
                data += "\r\n"
                data += "<html><body><h1>Tiny webserver is under construction</h1></body></html>\r\n\r\n"
                data += "<a href = '/www'>www</a>\n"
                data += "<a href = '/bin'>bin</a>\n"
                c.sendall(data.encode())
    
def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)

if __name__ == "__main__":
    main()