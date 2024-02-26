from typing import Optional
from io import BytesIO
from gi.repository import Gst
from utils import must_link
from datetime import datetime;
import requests
from dotenv import load_dotenv
import os
from pytz import timezone

# LOAD ENV VALUES
load_dotenv()

ROOT_PATH = os.getenv("ROOT_PATH")

REQUEST_URL = "http://localhost:5000/api/thumbnails"

class JpegSink:
    def __init__(self):
        self.first = 0
        self.flag = 0
        self.index = 0
        self.ct = datetime.now()
        
    def new_buffer(self, sink, data, location, zone):
        sample = sink.emit("pull-sample")
        buf = sample.get_buffer()
        buffer = buf.extract_dup(0, buf.get_size())

        if self.first == 0:
            self.first = buf.pts 
            self.ct = datetime.now(timezone(zone))
            print(self.ct)
            path = "{}/{}/thumbnails/{}.jpeg".format(ROOT_PATH, location, self.ct.strftime('%Y-%m-%d %H:%M:%S'))
            binary_file = open("..{}/{}/thumbnails/{}.jpeg".format(ROOT_PATH,location, self.ct.strftime('%Y-%m-%d %H:%M:%S')), "ab")
            print(path)
            binary_file.write(buffer)
            binary_file.close()

            r = requests.post(REQUEST_URL, json={
                "path" : path,
                "time" : self.ct.strftime('%Y-%m-%d %H:%M:%S'),
                "time2str" : self.ct.strftime('%Y-%m-%d %H:%M:%S'),
                "camera_id" : location
                })
            self.flag = 1
        
        if(self.flag == 0):
            self.ct = datetime.now(timezone(zone))
            path = "{}/{}/thumbnails/{}.jpeg".format(ROOT_PATH, location, self.ct.strftime('%Y-%m-%d %H:%M:%S'))
            binary_file = open("..{}/{}/thumbnails/{}.jpeg".format(ROOT_PATH,location, self.ct.strftime('%Y-%m-%d %H:%M:%S')), "ab")
            print(path)
            binary_file.write(buffer)
            binary_file.close()

            r = requests.post(REQUEST_URL, json={
                "path" : path,
                "time" : self.ct.strftime('%Y-%m-%d %H:%M:%S'),
                "time2str" : self.ct.strftime('%Y-%m-%d %H:%M:%S'),
                "camera_id" : location
                })
            self.index +=1
            self.flag = 1

        if((buf.pts - self.first) > 2000000000):
            self.flag = 0
            self.first = buf.pts
        
        return Gst.FlowReturn.OK

    def genObj(
        self,
        location: int,
        zone: str
    ) -> Gst.Element:

        print('sink')

        sink = Gst.ElementFactory.make("appsink")
        sink.set_property("emit-signals", True)
        sink.connect("new-sample", self.new_buffer, sink, location, zone)
      
        bin = Gst.Bin()
        bin.add(sink)

        enc = Gst.ElementFactory.make("jpegenc", "encoder")
        bin.add(enc)

        capsfilter = Gst.ElementFactory.make("capsfilter", "filter1")
        caps = Gst.caps_from_string("video/x-raw, width=800,height=400")
        capsfilter.set_property("caps", caps)

        scale = Gst.ElementFactory.make("videoscale", "scale")
        bin.add(scale)

        bin.add(capsfilter)
        # try:
        try:
            must_link(scale.link(capsfilter))
            must_link(capsfilter.link(enc))
            must_link(enc.link(sink))
            #must_link(mpegtsmux.link(sink))
        except RuntimeError as err:
            raise RuntimeError('Could not link source') from err

        sink_pad = scale.get_static_pad('sink')

        ghost_sink = Gst.GhostPad.new('sink', sink_pad)
        bin.add_pad(ghost_sink)
        return bin