# LOAD STANDARD PACKAGE
import os
from flask import Blueprint, jsonify, request
import datetime
from dotenv import load_dotenv
from apis.utils import remove_less_1000
from apis.m3u8convert import convert_m3u8_files

import shutil
# LOAD CUSTOMIZED PACKAGE
from app import db, Video

# Load ENV Values
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")

# RANDOM Path
RANDOM_PATH = "./share/random/videos"

# RETURN BLUEPRINT FILE


def create_video_blueprint(blueprint_name: str, resource_type: str, resource_prefix: str) -> Blueprint:
    blueprint = Blueprint(blueprint_name, __name__)

    # ============================================================================================
    # desc: ADD RANDOM IMAGES
    # path: /test [GET]
    @blueprint.route(f'/{resource_prefix}/random/<camera_id>', methods=['GET'])
    def create_random(camera_id):
        date = datetime.datetime(2023, 2, 1, 12, 20, 5)
        for i in range(0, 300):
            date += datetime.timedelta(seconds=2)
            video_path = "output{}.ts"
            video_path = video_path.format(i)
            db.session.add(Video(video_path, date, camera_id))
        db.session.commit()
        return "success"
    # ============================================================================================

    # desc: ADD NEW Video IN THE TABLE
    # path: /video [POST]
    @blueprint.route(f'/{resource_prefix}', methods=['POST'])
    def create_video():
        # ADD NEW VIDEO
        body = request.get_json()
        db.session.add(
            Video(body['path'], body['time'], body['time2str'],body['duration'], body['camera_id']))
        db.session.commit()

        return "Thumbnail created & Camera thumbnail updated"

    #desc: M3U8 CONVERT TO MP4 FILE
    #path: /convert/<path> [GET]
    @blueprint.route(f'/{resource_prefix}/convert/<path>', methods=['GET'])
    def convert_mp4(path):
        convert_m3u8_files('./share/m3u8/download{}'.format(path))

        return jsonify('/share/m3u8/download{}'.format(path.replace("m3u8", "mp4")))

    # desc: REQUEST FOR HLS PLAY
    # path: /play/<camera_id> [GET]
    @blueprint.route(f'/{resource_prefix}/play/<camera_id>/<start>/<end>/<mode>/<video>', methods=['GET'])
    def play_hls(camera_id, start, end, mode, video):
        vod_url = video.replace("*", "/")
        print(vod_url)
        remove_less_1000(".{}".format("/share/m3u8/"), 10, 2)
        if os.path.exists(".{}".format(vod_url)):
            os.remove(".{}".format(vod_url))
        videos = []
        output1 = output = '''#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:2
#EXT-X-MEDIA-SEQUENCE:0

'''
        print("start:", start, "end:", end)
        for item in db.session.query(Video).filter(Video.camera_id == camera_id, Video.time >= start, Video.time <= end).order_by(Video.id):
            print(item)
            del item.__dict__['_sa_instance_state']
            if(item.__dict__["path"] == '/share/gray.ts'):
                output = output+'#EXT-X-DISCONTINUITY\n'+"#EXTINF:{},\n".format(item.__dict__["duration"])+item.__dict__["path"]+"\n"+'#EXT-X-DISCONTINUITY\n'
            else:
                output = output+"#EXTINF:{},\n".format(item.__dict__["duration"])+item.__dict__["path"]+"\n"
                output1 = output1+"#EXTINF:{},\n".format(item.__dict__["duration"])+item.__dict__["path"]+"\n"
        output += "#EXT-X-ENDLIST"
        output1 += "#EXT-X-ENDLIST"
        path0 = ".{}/m3u8/{}{}.m3u8"
        path1="{}/m3u8/{}{}.m3u8"
        path2=".{}/m3u8/download{}{}.m3u8"
        output1 = output1.replace("/share", "..")
        i=0
        while(True):
            date = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            if os.path.exists(path0.format(ROOT_PATH, date, i)):
                i+=1
            else:   
               path0 =  path0.format(ROOT_PATH, date, i)
               path1 =  path1.format(ROOT_PATH, date, i)
               path2 =  path2.format(ROOT_PATH, date, i)
               break
        f = open(path0, "w")
        f.write(output)
        f.close()

        f = open(path2, "w")
        f.write(output1)
        f.close()
        return jsonify(path1)
    return blueprint
