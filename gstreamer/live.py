
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

Gst.init(None)

str = 'filesrc location=../share/gray.mp4 ! qtdemux ! h264parse ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=800, height=400 ! x264enc bitrate=512 ! video/x-h264,profile=\"high\" ! mpegtsmux ! hlssink max-files=0 playlist-location=../share/3/graylist.m3u8 location=../share/3/segment.%05d.ts target-duration=2'

pipeline = Gst.parse_launch(str)

pipeline.set_state(Gst.State.PLAYING)

bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

pipeline.set_state(Gst.State.NULL)
