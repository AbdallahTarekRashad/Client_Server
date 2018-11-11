import socket
import threading
peers = {}
def register (addr,files):
    peers.update({addr[1]:files})

def search (filename):
    result = []
    for key in peers:
        for val in peers[key]:
            if val == filename:
                result.append(key)
    if len(result)==0:
        return 'Not Exists'
    return result

def connect(name,sock):
    conn , addr = sock.accept()
    print(addr)
    while True:
        # print '(1) To Registry \n(2) To Search \n(3)To Quit'
        data=conn.recv(1024)
        if data == '3':
            conn.close()
            print ('close connection with' , addr)
            break;
        elif data == '1' :
            print 'User ', addr, ' Registering'
            FileList = []
            while True:
                filename = conn.recv(1024)
                if filename == 'q':
                    break
                else:
                    FileList.append(filename)
            register(addr, FileList)
            print 'User ', addr, ' Registered'
            print peers
            conn.send('\nNow You Are Registered\n')
        elif data == '2':
            x=conn.recv(1024)
            result = search(x)
            print result
            if result == 'Not Exists':
                conn.send(result)
            else:
                conn.send(str(result))
        else :
            conn.send('Invalid Data Type Again')

sock = socket.socket()
sock.bind(('localhost' , 12345))
sock.listen(5)
t1 = threading.Thread(target=connect,args=( 'th1',sock))
t1.start()
t2 = threading.Thread(target=connect,args=( 'th2',sock))
t2.start()
t3 = threading.Thread(target=connect,args=( 'th3',sock))
t3.start()
t4 = threading.Thread(target=connect,args=( 'th4',sock))
t4.start()
t5 = threading.Thread(target=connect,args=( 'th5',sock))
t5.start()

