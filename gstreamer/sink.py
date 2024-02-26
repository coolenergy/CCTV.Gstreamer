from typing import Optional
from io import BytesIO
from gi.repository import Gst
from utils import must_link
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import numpy as np
from moviepy.editor import *
from pytz import timezone
from db import run_query, select_query

from GetDuration import get_duration
# LOAD ENV VALUES
load_dotenv()

ROOT_PATH = os.getenv("ROOT_PATH")
REQUEST_URL = "http://localhost:5000/api/videos"


class HLSAPPSINK:
    def __init__(self):
        self.first = 0
        self.flag = 0
        self.index = 0
        self.ct = datetime.now()
        self.key = 0
    def new_buffer(self, sink, data, location, zone):
        if self.key == 0:
            query = "UPDATE camera SET flag = 'YES' where id = {}".format(location)
            run_query(query)
            self.key = 1
        sample = sink.emit("pull-sample")
        buf = sample.get_buffer()
        buffer = buf.extract_dup(0, buf.get_size())
        if self.first == 0:
            self.first = buf.pts 
            self.ct = datetime.now(timezone(zone))
            self.flag = 1
        
        if(self.flag == 0):
            self.ct = datetime.now(timezone(zone))
            self.index +=1
            self.flag = 1
        binary_file = open("..{}/{}/videos/{}.ts".format(ROOT_PATH, location, self.ct.strftime('%Y-%m-%d %H:%M:%S')), "ab")
        binary_file.write(buffer)
        if((buf.pts - self.first) > 2000000000):
            path = "{}/{}/videos/{}.ts".format(ROOT_PATH, location, self.ct.strftime('%Y-%m-%d %H:%M:%S'))
            print(path)
            self.flag = 0
            self.first = buf.pts
            # duration = get_duration("..{}/{}/videos/{}.ts".format(ROOT_PATH, location, self.ct.strftime('%Y-%m-%d %H:%M:%S')))
            # print(duration)
            r = requests.post(REQUEST_URL, json={
                    "path" : path,
                    "time" : self.ct.strftime('%Y-%m-%d %H:%M:%S'),
                    "time2str" : self.ct.strftime('%Y-%m-%d %H:%M:%S'),
                    "camera_id" : location,
                    "duration": 2.0
                    })
        
        binary_file.close()
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
        # sink.set_property("location", location)
        # sink.set_property("target-duration", 5)
        # sink.set_property("playlist-location", playlist_location)
      
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
