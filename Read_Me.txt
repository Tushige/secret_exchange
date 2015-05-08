*** READ ME ***

I. How to run the program

	1. run the server first
		- python main.py
	2. run the clients on separate terminals, giving each different integer id
		- python client.py <numeric id>

II. Initial Behavior
	1. initially the client won't be able to talk to each other. But all clients can talk to the server.

	2. Each client can request to get a connection with a particular client by sending a request to the server
		- connect <client id to talk to>
	3. Upon request, the server will send the "secret" key it shares with the requested client to the requester

	4. Upon learning this key, the requester can finally establish a connection and talk to the client of interest

III. Possible Commands
	
	1. Send <destination client-id> <Message>
		- Sends a message to the client-id if connection exists.
		- If there is no connection, then a failed message will show.  
	2. Connect <client-id>
		- requests from the server to help requester and requested client to talk to each other. The server will share its secret key with the requester.
