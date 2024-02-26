from typing import Optional

from gi.repository import Gst
from utils import must_link

class HLSLiveSink:
    def __new__(
        cls,
        location: str,
        playlist_location: str,
    ) -> Gst.Element:

        sink = Gst.ElementFactory.make("hlssink")
        sink.set_property("location", location)
        sink.set_property("target-duration", 1)
        sink.set_property("max-files", 5)
        sink.set_property("playlist-location", playlist_location)
      
        bin = Gst.Bin()
        bin.add(sink)

        capsfilter = Gst.ElementFactory.make("capsfilter", "filter1")
        caps = Gst.caps_from_string("video/x-raw, width=800,height=400")
        capsfilter.set_property("caps", caps)

        scale = Gst.ElementFactory.make("videoscale", "scale")
        bin.add(scale)

        bin.add(capsfilter)

        enc = Gst.ElementFactory.make("x264enc")
        enc.set_property("bitrate", 4000)
        enc.set_property("tune", "zerolatency")
        enc.set_property("key-int-max", 60)
        enc.set_property("speed-preset", "ultrafast")
        bin.add(enc)

        mpegtsmux = Gst.ElementFactory.make("mpegtsmux", "mpegtsmux")
        if not mpegtsmux:
            sys.stderr.write(" Unable to create mpegtsmux \n")
        bin.add(mpegtsmux)

        # try:
        try:
            must_link(scale.link(capsfilter))
            must_link(capsfilter.link(enc))
            must_link(enc.link(mpegtsmux))
            must_link(mpegtsmux.link(sink))
        except RuntimeError as err:
            raise RuntimeError('Could not link source') from err

        sink_pad = scale.get_static_pad('sink')

        ghost_sink = Gst.GhostPad.new('sink', sink_pad)
        bin.add_pad(ghost_sink)
        return bin

class OSDH264RTMPSink:

    def __new__(
        cls,
        location: str,
        # bitrate = 2000000
    ) -> Gst.Element:
        rtmpsink = Gst.ElementFactory.make("rtmpsink")
        rtmpsink.set_property("location", location)

        bin = Gst.Bin()
        bin.add(rtmpsink)


        enc = Gst.ElementFactory.make("x264enc")
        enc.set_property("bitrate", 4000)
        enc.set_property("tune", "zerolatency")
        enc.set_property("key-int-max", 60)
        enc.set_property("speed-preset", "ultrafast")
        bin.add(enc)

        flvmux = Gst.ElementFactory.make("flvmux")
        
        if not flvmux:
            sys.stderr.write(" Unable to create flvmux \n")
        bin.add(flvmux)

        # flvmux.set_property("streamable", True)
        # flvmux.set_property("latency", 500)
        bin.add(flvmux)
        # print(flvmux)
   
        try:
            must_link(enc.link(flvmux))
            must_link(flvmux.link(rtmpsink))
        except RuntimeError as err:
            raise RuntimeError('Could not link source') from err

        print('osd')
        sink= enc.get_static_pad('sink')
        ghost_pad = Gst.GhostPad.new('sink', sink)
        bin.add_pad(ghost_pad)
        return bin
