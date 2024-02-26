# LOAD STANDARD PACKAGE
import os
from flask import Blueprint, jsonify, request
import datetime
from dotenv import load_dotenv
from datetime import datetime, timezone
from PIL import Image
import math

# LOAD CUSTOMIZED PACKAGE
from app import db, Camera, Thumbnail

# Load ENV Values
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")

# RANDOM Path
RANDOM_PATH = os.getenv("RANDOM_PATH")

# RETURN BLUEPRINT FILE


def create_thumbnail_blueprint(blueprint_name: str, resource_type: str, resource_prefix: str) -> Blueprint:
    blueprint = Blueprint(blueprint_name, __name__)

    # ============================================================================================
    # desc: ADD RANDOM IMAGES
    # path: /test [GET]
    @blueprint.route(f'/{resource_prefix}/random/<camera_id>', methods=['GET'])
    def create_random(camera_id):
        date = datetime.datetime(2023, 2, 1, 12, 20, 5)
        for i in range(0, 300):
            date += datetime.timedelta(seconds=2)
            imgpath = "/share/random/thumbnails/{}.jpg"
            imgpath = imgpath.format(i)
            db.session.add(Thumbnail(imgpath, date, camera_id))
        db.session.commit()
        return "success"

    # desc: ADD NEW THUMBNAIL IN THE TABLE & UPDATE THE CAMERA THUMBNAIL
    # path: /thumbnail [POST]
    @blueprint.route(f'/{resource_prefix}', methods=['POST'])
    def create_thumbnail():
        # ADD NEW THUMBNAIL
        body = request.get_json()
        db.session.add(
            Thumbnail(body['path'], body['time'], body['time2str'], body['camera_id']))
        db.session.commit()

        # UPDATE THUMBNAIL OF CAMERA
        db.session.query(Camera).filter_by(id=body['camera_id']).update(
            dict(thumbnail=body['path']))
        db.session.commit()

        return "Thumbnail created & Camera thumbnail updated"

    # desc: View VIDEO IN VOD MOD
    # path: /thumbnail/<id> [GET]
    @blueprint.route(f'/{resource_prefix}/<id>', methods=['GET'])
    def vod_mod(id):
        return jsonify({"id": id, "action": "VOD MOD"})

    # desc: GET THUMBNAILS WITH FILTERS
    # path: /thumbnail/<camera_id>/<start>/<end>/<duration> [GET]
    @blueprint.route(f'/{resource_prefix}/<camera_id>/<start>/<end>/<duration>/<mode>/<video>', methods=['GET'])
    def search_thumbnail(camera_id, start, end, duration, mode, video):
        thumbnails = []

        vod_url = video.replace("*", "/")
        
        if os.path.exists(".{}".format(vod_url)):
            os.remove(".{}".format(vod_url))
                
        start1 = datetime.strptime(start, '%Y-%m-%dT%H:%M').strftime("%Y-%m-%d %H:%M:%S")
        end1 = datetime.strptime(end, '%Y-%m-%dT%H:%M').strftime("%Y-%m-%d %H:%M:%S")

        for item in db.session.query(Thumbnail).filter(Thumbnail.camera_id == camera_id, Thumbnail.time >= start1, Thumbnail.time <= end1).order_by(Thumbnail.id):
            del item.__dict__['_sa_instance_state']
            thumbnails.append(item.__dict__)
        
        # images = []
        # sources = []
        # for item in thumbnails:
        #     img1 = Image.open(item["path"].replace("/share", "./share"))
        #     images.append(img1)
        
        # img_01_size = images[0].size

        # new_im = Image.new('RGB', (5*img_01_size[0],6*img_01_size[1]), (250,250,250))
        # j = 0
        # for i in range(math.ceil(len(images)/30)):
        #     for k in range(5):
        #         for l in range(6):
        #             if(i*30+j < len(images)):
        #                 new_im.paste(images[i*30+j], (k*img_01_size[0], l*img_01_size[1]))
        #                 thumbnails[i*30+j]["x"] = k
        #                 thumbnails[i*30+j]["y"] = l
        #                 thumbnails[i*30+j]["source"] = "merged_images{}.png".format(i)
        #             j+=1

        #     new_im.save("merged_images{}.png".format(i), "PNG")
        #     sources.append("merged_images{}.png".format(i))
        #     new_im = Image.new('RGB', (5*img_01_size[0],6*img_01_size[1]), (250,250,250))
        #     j=0

        return jsonify(thumbnails)

    return blueprint
