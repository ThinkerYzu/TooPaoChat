gst-launch-1.0 -v ximagesrc ! videoscale ! 'video/x-raw,height=540,width=960' ! videoconvert ! vp8enc ! rtpvp8pay ! udpsink host=127.0.0.1 port=5001
