import socket
import sys, getopt
import threading
import thread
import time
import datetime
import random
from collections import deque
#my imports
from node import Node
import globals

#global variables
node_id = None
coord = None
sock = {}
def main(argv):
	global node_id
	globals.init()
	node_id = int(argv[0])

	connect_to(1, globals.coord_ip, globals.coord_port)
	start_threads()

def start_threads():
	#server thread
	server_t = threading.Thread(target = server, args = ())
	server_t.setDaemon(True)
	server_t.start()

	input = threading.Thread(target = user_input, args = ())
	input.start()

def connect_to(isCoord, ip, port):
	global coord
	#setup connection to coordinator
	try:
		#create an AF_INET, STREAM socket (TCP)
		sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1] + '\n'
		sys.exit();

	try:
		sockfd.connect((ip , port))
	except socket.error, msg:
		print 'Failed to connect socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1] + '\n'
		sys.exit();

	if isCoord==1:
		coord = sockfd

	#register client to the coordinator'
	print 'sending registration to %d at port %d\n'%(port - globals.coord_port, port)
	send_msg("REGISTRATION " + str(node_id), sockfd)

	#server thread - receives messages from the coordinator
	server_t=threading.Thread(target = recvThread, args = (sockfd,))
	server_t.start()

#receives connection from the nodes
def server():
	global s_server, server_port, sock, num_clients
	s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_port = globals.coord_port + node_id
	try: # setup server socket
		s_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s_server.bind((globals.coord_ip, my_port))
	
	# if server setup fail
	except socket.error , msg:
		print '[[ Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1] + ' ]]' + '\n'
		sys.exit()

	print '\n[Node %d] Socket bind complete.\n'%node_id
	s_server.listen(32)
	print '\n[Node %d] Socket listening on '%node_id + str(my_port)
	globals.done_server = 1;
	while(1):
		conn, addr = s_server.accept()
		recv_t = threading.Thread(target=recvThread, args=(conn,))
		recv_t.setDaemon(True)
		recv_t.start()
	conn.close()

def recvThread(conn):
	while(not globals.end):
		try:
			data = conn.recv(1024)
			#print data
		except:
			continue
		if len(data) == 0:
			continue
		while data[-1] != '\n' and end==0:
			data = data + conn.recv(1024)
		messages = data.split('\n')
		for ss in messages:
			buf = ss.split(' ')
			if(buf[0] == ''):
				continue
			# register itself as an active node
			elif buf[0] == "REGISTRATION":
				print '\n[Node %d] connected to Node %s\n'%(node_id, buf[1])
				sock[int(buf[1])] = conn
				send_msg("ROGER " + str(node_id), conn)
				#user_input()
			# acknowledge connection
			elif(buf[0] == "ROGER"):
				try:
					if buf[1] != None:
						print '\n[Node %c] connected with Node %s\n'%(node_id, buf[1])
						sock[int(buf[1])] = conn
					else:
						print '\n[Node %c] connected with coordinator %s\n'%node_id
				except:
					pass
				#user_input()
			#coord allowed my request to connect to another node. Setup the connection now
			elif buf[0] == "SECRET":
				print '\n[Node %d] Received SECRET key to node %d\n'%(node_id, int(buf[1]))
				connect_to(0, buf[2], int(buf[3]))
			# Got a regular Message
			elif buf[0] == "MESSAGE":
				length = len(buf)
				for i in range(3, length):
					buf[2] = buf[2] + ' ' +buf[i]
				print '\n[Node %d] Node %d sent: %s\n'%(node_id, int(buf[1]), str(buf[2]))
				#user_input()
			elif buf[0] == "WARNING!":
				print ss
				#user_input()

def send_handler(msg, dest_id):
	if sock.has_key(dest_id) == 0:
		print '\n[Node %d] not connected to requested node. Please, connect first\n'%node_id
		#user_input()
	else:
		send_msg("MESSAGE "+ str(node_id) + ' '+msg, sock[dest_id])
		

def connect_handler(dest_id):
	if sock.has_key(dest_id) == 0:
		send_msg("CONNECT_REQUEST " + str(node_id) + ' ' + str(dest_id), coord)
	else:
		print '\n[Node %d] Already connected to node %d\n'%(node_id, dest_id)
		#user_input()

def send_msg(msg, conn):
	conn.sendall(msg+'\n')
	print 'sending '
	print msg

def user_input():
	while(globals.done_server == 0):
		pass
	while(1):
		buf = raw_input('Enter a COMMAND: ')
		cmd = buf.split(' ')
		if cmd[0] == "send" and cmd[1] != None and cmd[2] != None:
			length = len(cmd)
			for i in range(3, length):
				cmd[2] = cmd[2] + ' ' +cmd[i]
			send_handler(cmd[2], int(cmd[1]))
		elif cmd[0] == "connect" and cmd[1] != None:
			connect_handler(int(cmd[1]))
		else:
			print 'Invalid Input'

#execution starts here
if __name__ == "__main__":
	print sys.argv
	main(sys.argv[1:])