#globals

def init():
	global nodes, coord_port, coord_ip, num_active, keep_alive, sock, coord_initialized, nodes, end, done_server
	
	#stores the connection of nodes
	sock = [None] * 10
	coord_port = 8100
	coord_ip = "localhost"
	coord_initialized = 0
	nodes = [None]*10
	end = 0
	done_server = 0