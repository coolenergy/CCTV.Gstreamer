from gi.repository import Gst
from utils import must_link


class FakeVideoSource:

    def __new__(cls, num_buffers=300):
        bin = Gst.Bin()
        src = fakesrc(
            num_buffers=num_buffers
        )
        bin.add(src)

        return bin

class RTSPH264Source:

    def __new__(cls, location: str):
        bin = Gst.Bin()

        rtspsrc = Gst.ElementFactory.make("rtspsrc", "rtspsrc")
        rtspsrc.set_property("location", location)
        rtspsrc.set_property("protocols", "tcp")
        rtspsrc.set_property("retry", 100)
        rtspsrc.set_property("latency", 1000)
        rtspsrc.set_property("buffer-mode", 'auto')
        bin.add(rtspsrc)
        
        rtph264depay = Gst.ElementFactory.make("rtph264depay", "rtph264depay")
        if not rtph264depay:
            sys.stderr.write(" Unable to create rtph264depay \n")
        bin.add(rtph264depay)

        h264parse = Gst.ElementFactory.make("h264parse", "h264parse")
        if not h264parse:
            sys.stderr.write(" Unable to create h264parse \n")
        bin.add(h264parse)

        rtspsrc.connect('pad-added', _rtsp_pad_added, rtph264depay)
        try:
            rtph264depay.link(h264parse)
        except RuntimeError as err:
            raise RuntimeError('Could not link source') from err

        src_pad = h264parse.get_static_pad('src')
        ghost_src = Gst.GhostPad.new('src', src_pad)
        bin.add_pad(ghost_src)
        return bin


def _rtsp_pad_added(_: Gst.Element, pad: Gst.Pad, depay: Gst.Element):

    caps =pad.get_current_caps().get_structure(0).get_name()
    depay_pad = depay.get_static_pad('sink')
    pad.link(depay_pad)


