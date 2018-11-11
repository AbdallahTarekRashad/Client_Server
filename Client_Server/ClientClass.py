import socket
import threading
import os
class Client():
    def ActServer(self ,name,sock):
        conn , addr = sock.accept()
        print addr
        while True:
            filename = conn.recv(1024)
            print filename
            if os.path.isfile(filename):
                conn.send('EXISTS' + str(os.path.getsize(filename)))
                userResponse = conn.recv(1024)
                if userResponse[:2] == 'OK':
                    with open(filename,'rb') as f:
                        bytesToSend=f.read(1024)
                        conn.send(bytesToSend)
                        while bytesToSend != '':
                            bytesToSend = f.read(1024)
                            conn.send(bytesToSend)
                print 'File Sent To Client ',addr
            else:
                print 'Error With user',addr
                sock.send('ERR')
    def Download(self,sock,filename):
        sock.send(filename)
        data = sock.recv(1024)
        if data[:6] == 'EXISTS':
            filesize=long(data[6:])
            size = str(filesize)
            massage = input('File Exists' + size + 'Bytes , Download? (Y/N)? ->')
            if massage=='Y':
                sock.send('OK')
                f = open('new_'+filename ,'wb')
                data = sock.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv<filesize :
                    data = sock.recv(2048)
                    totalRecv = totalRecv+len(data)
                    f.write(data)
            print 'File Downloaded'
        else:
            print "File Dose Not Exists"
    def run(self,port):
        sock= socket.socket()
        sock.bind(('localhost' , port))
        sock.connect(('localhost',12345))
        while True:
            print '(1) To Registry \n(2) To Search \n(3)To Quit \n(4)Act As A Server And Wait Clients \n(5)Connect With Another Client To Download File \n(6)Reconnect With Server \n(7)Close Program'
            data=input('Enter Data==> ')
            if data=='1':
                sock.send(data)
                while True:
                    filename=input('Enter File Name(q=>Quit) ==> ')
                    if filename == 'q':
                        sock.send(filename)
                        break
                    else :
                        sock.send(filename)
                print sock.recv(1024)
            elif data=='2':
                sock.send(data)
                filename=input('Enter File Name : ')
                sock.send(filename)
                result = sock.recv(2048)
                print result
            elif data == '3':
                sock.send(data)
                sock.close()
            elif data =='4':
                sock.send('3')
                sock.close()
                sock = socket.socket()
                sock.bind(('localhost', port))
                sock.listen(5)
                t1 = threading.Thread(target=self.ActServer, args=('t1',sock))
                t1.start()
                t2 = threading.Thread(target=self.ActServer, args=('t2', sock))
                t2.start()
                t3 = threading.Thread(target=self.ActServer, args=('t3', sock))
                t3.start()
                t4 = threading.Thread(target=self.ActServer, args=('t4', sock))
                t4.start()
                t5 = threading.Thread(target=self.ActServer, args=('t5', sock))
                t5.start()
                break
            elif data =='5':
                sock.send('3')
                sock.close()
                sock = socket.socket()
                sock.bind(('localhost', port))
                port = input('Enter Port You Want To Connect With ==> ')
                port = int(port)
                sock.connect(('localhost',port))
                filename = input('Enter File Name: ')
                self.Download(sock,filename)
            elif data == '6':
                sock = socket.socket()
                sock.bind(('localhost', port))
                sock.connect(('localhost', 12345))
                print 'Reconnection with Server'
            elif data == '7':
                sock.close()
                break
            else:
                print 'Invalid Data'

