gst-launch-1.0 -v udpsrc port=5001 reuse=true caps="application/x-rtp, payload=96" ! rtpvp8depay ! vp8dec ! xvimagesink
