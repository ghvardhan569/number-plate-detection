import socket
import sys
import zipfile
import os

host = '192.168.88.217'
port = 1998
zip_name = 'main.zip'

s = socket.socket()
print('[+] Client socket is created.')

s.connect((host, port))
print('[+] Socket is connected to {}'.format(host))

with zipfile.ZipFile(zip_name, 'w') as file:
        file.write('data.csv')


s.send(zip_name.encode())

f = open(zip_name, 'rb')
l = f.read()
s.sendall(l)

#os.remove(zip_name)
f.close()
s.close()
