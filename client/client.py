import socket
import os
import time

ip='127.0.0.1'
control_port=5000
data_port=5001
os.system('cls')

cs=socket.socket()
cs.connect((ip,control_port))

print("Connected to server")

portno=cs.recv(1024).decode('utf-8')
data_port=int(portno)

#ds=socket.socket()
#ds.connect((ip,data_port))



#1.List of Directory from server
def server_ls():
    os.system('cls')
    st='1'
    cs.send(st.encode('utf-8'))
    st=cs.recv(1024).decode('utf-8')
    while st!='\r\n':
        st=cs.recv(1024).decode('utf-8')
        print(st)


#2.List of Directory from client
def client_ls():
    os.system('cls')
    l=os.listdir()
    for entry in l:
        print(entry)


#3.Current Directory of server
def server_cwd():
    os.system('cls')
    st='3'
    time.sleep(0.5)
    cs.send(st.encode('utf-8'))
    di=cs.recv(1024).decode('utf-8')
    print("Server Current working Directory:")
    print(di)

#4.Current Directory of client
def client_cwd():
    os.system('cls')
    print("Client Current working Directory:")
    print(os.getcwd())


#5.Change Directory of server
def server_cd():
    os.system('cls')
    print("Give directroy to go on:")
    di=input()
    st='5'
    cs.send(st.encode('utf-8'))
    time.sleep(0.5)
    cs.send(di.encode('utf-8'))
    di=cs.recv(1024).decode('utf-8')
    print("Server Current working Directory:")
    print(di)


#6.Change Directory of client
def client_cd():
    os.system('cls')
    print("Give directroy to go on:")
    di=str(input())
    os.chdir(di)
    print("New CWD:")
    print(os.getcwd())


#7.Download files form server
def download():
    os.system('cls')
    filename=input('Enter File Name:>')
    if os.path.isfile(filename):
        print("File already exist in Clients directory. Do you want to replace it ?Y/N")
        comm=input('>')
    if not(os.path.isfile(filename)) or comm=='Y' or comm=='y':
        if filename!='Quit':
            st='7'
            cs.send(st.encode('utf-8'))
            cs.send(filename.encode('utf-8'))
            data=cs.recv(1024).decode('utf-8')
            if data[:6]=='EXISTS':
                filesize=int(data[6:])
                print('File Exist and size :',end="")
                print(filesize,end="")
                print('Bytes')
                msg=input('Download it? Y/N ? >')
                if msg=='Y' or msg=='y':
                    req='OK'
                    cs.send(req.encode('utf-8'))
                    f=open(filename,'wb')
                    data=cs.recv(1024)
                    totalrecv=len(data)
                    f.write(data)
                    while totalrecv<filesize:
                        data=cs.recv(1024)
                        totalrecv+=len(data)
                        f.write(data)
                    print("File receved successfully")
                else:
                    print('File download denied by user')
            else :
                print('File does Not Exist')
        


#8.Upload files on server
def upload():
    st='5'
    cs.send(st.encode('utf-8'))
    filename=input("Enter File name:")
    cs.send(filename.encode('utf-8'))
    fs=str(os.path.getsize(filename))
    cs.send(fs.encode('utf-8'))
    #time.sleep(0.5)
    responce=cs.recv(1024).decode('utf-8')
    if responce=="ALREADY":
        print("File already exist you can't rewrite it")
    else:
        with open(filename,'rb') as f:
            bytes_to_send=f.read(1024)
            cs.send(bytes_to_send)
            while bytes_to_send!='':
                bytes_to_send=f.read(1024)
                cs.send(bytes_to_send)
    


    
option=0
while option!=9:
    print("****************************************")
    print("1.List of Directory from server")
    print("2.List of Directory from client")
    print("3.Current Directory of server")
    print("4.Current Directory of client")
    print("5.Change Directory of server")
    print("6.Change Directory of client")
    print("7.Download files form server")
    print("8.Upload files on server")
    print("9.Exit")
    print("****************************************")
    option=int(input("Choose an option:>"))
    if option==1:
        server_ls()
        aa=input()
    elif option==2:
        client_ls()
        aa=input()
    elif option==3:
        server_cwd()
        aa=input()
    elif option==4:
        client_cwd()
        aa=input()
    elif option==5:
        server_cd()
        aa=input()
    elif option==6:
        client_cd()
        aa=input()
    elif option==7:
        download()
        aa=input()
    elif option==8:
        upload()
        aa=input()
    elif option==9:
        print("SEE YOU SOON, bye!")
    else:
        print('Wrong Input Try again')
        aa=input()


cs.close()