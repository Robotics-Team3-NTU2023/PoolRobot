import socket

HOST = "172.20.10.2" 
PORT = 80         

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.settimeout(1) # timeout 1s
	while True:
		try: 
			s.sendall(input().encode())
		except KeyboardInterrupt:
			exit()
		except:
			pass
