# Why??

Why this project?  Just to prove it is possible to implement a simple
video chat platform without much efforts.

 - https://bangqu.com/Ea8W71.html

# Tests

server/stupid_server.py is a server implementation that is very
stupid, but still can be used as a proof of concept.  It supports two
users only, user1 and user2, right now.  Their passwords are user1_123
& user2_123, respectively.

client/stupid_client.py is a stupid client uploading your webcam
stream to the server.

STEPS:
 - python server/stupid_server.py
   - start the server at the port 8001
 - python client/stupid_client.py SERVER_IP 8001 user1 user1_123 
   - connect to the server and start streaming for user1
 - python client/stupid_client.py SERVER_IP 8001 user2 user2_123 
   - connect to the server and start streaming for user2

You will see two windows, one for each user.  Both window shows two
streams from user1 & user2.

However, it may be blocked if you run two instances of the client at
the same device sicne you have only one webcam.  You can try the test
video instead of the webcam.

To try the test video, you have to change code of client/gstclient.py.
In GstClient._build_upload() function, you can find a line of
videotestsrc.  Uncomment that line, and comment the lines of v4l2src.
