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

# Is It Feasible As a Project of First Year of Undergraduates?

The most hot critics of this project is too difficult for the college
students in their first year.  To build a video chatroom, you need to
know how to capture video from webcam & desktop screen/or a window,
and stream the video to a server and back the client.  People think
these are impossible for the first year students, however, as you can
see here, powerful libraries and tools are already there.  You don't
need to create it from scratch.

According the requirements in the spec of the project, all 3rd party
libraries should be available in source level; not shared object, dll
or any binary formats.  It implys building the 3rd party libraries
from source code with your build system.  For the case of gstreamer,
it is easy at least for Linux.  For Windows, it may be more difficult,
but there are loads of documents about building it for Windows.  And,
there must has similar projects for Windows native.

# How Can Students Know These Components?

For the students who just learn about softwares, they very probably
don't know these libraries and components.  That is why we have TA in
schools.  TAs are supposed to give help by sharing them information
like this.  TAs also need to explain some basic idea about these
libraries.

For example, with gstreamer, TAs have to explain what pipelines are,
and how they work, and show them some workable examples of building a
pipeline.  A lecture of sharing information of this kinds should be
short, not long.  I guess it should be one hours or less.

# Difficulties I Have Found!

Threading! For the first year students, they may not know
multi-threading and async tasks. TAs should share them an example of
integrate your I/O code with the main event loop of glib, the base of
gstreamer.

Changing pipelines dynamically is also difficult.  TAs also need to
share students with examples, and give some explaination.

# Conclusion

Overall, I think this is a good project for undergraduates, even for
their first year.  They may not know enough to build it, but TAs
should help them by sharing them with related information.  Then, they
will be fine.  Students tend to find information from others.  Some of
them must learn these knowledge very quick.  Others will seek for
helps.  Students can either learn how to integrate projects, team
works and finding helps.
