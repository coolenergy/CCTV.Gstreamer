from gi.repository import Gst
from utils import must_link

class H264Decode:
    def __new__(cls) -> Gst.Bin:
        bin = Gst.Bin()
        print('H264Decode')
        decodebin = Gst.ElementFactory.make("decodebin", "decodebin")
        bin.add(decodebin)

        videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        bin.add(videoconvert)

        # clockoverlay = Gst.ElementFactory.make("clockoverlay", "clockoverlay")
        # bin.add(clockoverlay)

        decodebin.connect("pad-added", pad_added, videoconvert)
        # videoconvert.link(clockoverlay)

        sink_pad = decodebin.get_static_pad('sink')
        sink_ghost = Gst.GhostPad.new('sink', sink_pad)
        bin.add_pad(sink_ghost)

        src_pad = videoconvert.get_static_pad('src')
        src_ghost = Gst.GhostPad.new('src', src_pad)
        bin.add_pad(src_ghost)

        return bin

def pad_added(element, pad, element2):

    pad_type = pad.get_current_caps().get_structure(0).get_name()
    pad.link(element2.get_static_pad("sink"))
    print('decodebin')
    print(pad_type)