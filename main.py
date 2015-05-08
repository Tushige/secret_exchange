#main.py

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


#Globals
sock = {}

def main():
	globals.init()
	start_server()

def start_server():
	serv = threading.Thread(target = server(), args = ())
	serv.setDaemon(True)
	serv.start()

#receives connection from the nodes
def server():
	global s_server, server_port, sock, num_clients
	s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try: # setup server socket
		s_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s_server.bind((globals.coord_ip, int(globals.coord_port)))
	
	# if server setup fail
	except socket.error , msg:
		print '[[ Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1] + ' ]]' + '\n'
		sys.exit()

	print '[Coord] Socket bind complete.\n'
	s_server.listen(32)
	print '[Coord] Socket listening on ' + str(globals.coord_port)
	globals.coord_initialized = 1;
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
		except:
			continue
		if len(data) == 0:
			continue
		while data[-1] != '\n' and self.end==0:
			data = data + conn.recv(1024)
		messages = data.split('\n')
		for ss in messages:
			buf = ss.split(' ')
			if(buf[0] == ''):
				continue
			#acknowledge the connection
			elif(buf[0] == "REGISTRATION"):
				print 'Connected with node%d\n'%int(buf[1])
				#save socket
				sock[int(buf[1])] = conn
				send_msg("ROGER", sock[int(buf[1])])
			# received request form 1 node to connect to another
			elif buf[0] == "CONNECT_REQUEST":
				print '[Coord] %s wants to connect to %s\n'%(buf[1], buf[2])
				connect_handler(int(buf[1]), int(buf[2]))

def connect_handler(source_id, dest_id):
	#check if node buf[2] is up
	if sock.has_key(dest_id)==0:
		send_msg("WARNING! %d is not in the network"%dest_id, sock[source_id])
		print 'dest_id not in network\n'
	else:
		send_msg("SECRET " + str(dest_id) +' ' + "localhost " + str(globals.coord_port + dest_id), sock[source_id])
		print 'sent SECRET KEY! with node %d to node %d\n'%(dest_id, source_id)

def send_msg(msg, conn):
	conn.sendall(msg+'\n')

def create_node(node_id, cs_int, next_req, tot_exec_time, option):
	my_node = Node(node_id, cs_int, next_req, tot_exec_time, globals.sets[node_id],option)
	globals.nodes[node_id] = my_node	
	s_server.close()

#execution starts here
if __name__ == "__main__":
	main()

