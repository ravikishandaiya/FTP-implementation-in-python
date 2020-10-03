import socket
import threading
import os
import time

ip='127.0.0.1'
control_port=5000
data_port=3214


## Function to send a file to client
def retrFile(name,c):
    filename=c.recv(1024).decode('utf-8')
    if os.path.isfile(filename):
        dtl='EXISTS'+str(os.path.getsize(filename))
        c.send(dtl.encode('utf-8'))
        userresponse=c.recv(1024).decode('utf-8')
        if userresponse[:2]=='OK':
            with open(filename,'rb') as f:
                bytes_to_send=f.read(1024)
                c.send(bytes_to_send)
                while bytes_to_send!='':
                    bytes_to_send=f.read(1024)
                    c.send(bytes_to_send)
                    
    else:
        error='ERR'
        c.send(error.encode('utf-8'))
    

## Function to store file in server directory
def storeFile(c):
    filename=c.recv(1024).decode('utf-8')
    fs=c.recv(1024).decode('utf-8')
    filesize=int(fs)
    if os.path.isfile(filename):
        st='ALREADY'
        c.send(st.encod('utf-8'))
    else:
        f=open(filename,'wb')
        data=cs.recv(1024).decode('utf-8')
        totalrecv=len(data)
        f.write(data)
        while totalrecv<filesize:
            data=cs.recv(1024).decode('utf-8')
            totalrecv+=len(data)
            f.write(data)
        print("File Uploaded successfully")



## Main Function
cs=socket.socket()
cs.bind((ip,control_port))
cs.listen(100)


os.system('cls')

print("Server Started")
while True :
    c,addr1=cs.accept()

    portno=str(data_port)
    c.send(portno.encode('utf-8'))
    print("Got Connection From IP<"+str(addr1)+">")
    st=c.recv(1024).decode('utf-8')
    option=int(st)
    if option==1:
        ls=os.listdir()
        c.send(ls[0].encode('utf-8'))
        for i in range(1,len(ls)):
            c.send(ls[i].encode('utf-8'))
        end='\r\n'
        c.send(end.encode('utf-8'))
    elif option==3:
        st=os.getcwd()
        time.sleep(0.5)
        c.send(st.encode('utf-8'))
    elif option==5:
        st=c.recv(1024).decode('utf-8')
        os.chdir(st)
        st=os.getcwd()
        c.send(st.encode('utf-8'))
    elif option==7:
        t=threading.Thread(target=retrFile,args=("retrThread",c))
        t.start()
    elif option==8:
        tt=threading.Thread(target=storeFile,args=(c))
        tt.start()
        
    elif option==9:
        c.close()
    
    
    

cs.close()
