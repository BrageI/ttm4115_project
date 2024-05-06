from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

try:
	while True:
		print('Ready.')
		connectionSocket, addr = serverSocket.accept()
		try:
			message =  connectionSocket.recv(1024).decode()
			filepath = message.split()[1]
			f = open(filepath[1:])
			outputdata = f.read()

			connectionSocket.send(("HTTP/1.1 200 OK\r\n\r\n").encode())
			
			response = outputdata + "\r\n"
			connectionSocket.send(response.encode())
			connectionSocket.close()

		except (IOError, IndexError):
			
			connectionSocket.send("HTTP/1.1 404 NOT FOUND\r\n\r\n".encode())
			connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

		connectionSocket.close()

finally:
	serverSocket.close()
