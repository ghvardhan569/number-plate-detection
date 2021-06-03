import socket
import sys
import zipfile
import os

host = '192.168.88.182'
port = 1998
k = int(sys.argv[1])
zip_name = 'main.zip'

s = socket.socket()
print('[+] Client socket is created.')

s.connect((host, port))
print('[+] Socket is connected to {}'.format(host))

with zipfile.ZipFile(zip_name, 'w') as file:
	for j in range(1, (k+1)):
		file.write('{}.jpeg'.format(j))
		print('[+] {}.jpeg is sent'.format(j))

s.send(zip_name.encode())

f = open(zip_name, 'rb')
l = f.read()
s.sendall(l)

#os.remove(zip_name)
f.close()
s.close()
