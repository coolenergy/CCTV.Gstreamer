# LOAD STANDARD PACKAGE
import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import shutil

# LOAD CUSTOMIZED PACKAGE
from app import db, Camera, Thumbnail, Video
from sqlalchemy import or_, desc, not_

# Load ENV Values
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")

# RETURN blueprint FILE
def create_camera_blueprint(blueprint_name: str, resource_type: str, resource_prefix: str) -> Blueprint:
    blueprint = Blueprint(blueprint_name, __name__)

    # desc: Get cameras OF THE table
    # path: /cameras [GET]
    @blueprint.route(f'/{resource_prefix}', methods=['GET'])
    def get_items():
        cameras = []
        for item in db.session.query(Camera).all():
            del item.__dict__['_sa_instance_state']
            cameras.append(item.__dict__)
        return jsonify(cameras)

    # desc: GET CAMERA'S STATE
    # path: /cameras/online/<id> [GET]
    @blueprint.route(f'/{resource_prefix}/online/<id>', methods=['GET'])
    def live_status(id):

        item = db.session.query(Camera).filter_by(id = id)[0]
        del item.__dict__['_sa_instance_state']
        
        # item1 = db.session.query(Thumbnail).filter_by(camera_id = id).order_by(desc(Thumbnail.time))[0]
        item1 = db.session.query(Thumbnail).filter(not_(Thumbnail.path.contains("gray"))).filter_by(camera_id = id).order_by(desc(Thumbnail.time))[0]
        del item1.__dict__['_sa_instance_state']
        return jsonify(item.__dict__, item1.__dict__)
    
    # desc: UPDATE CAMERA'S INFO
    # path: /cameras/<id> [PUT]
    @blueprint.route(f'/{resource_prefix}/<id>', methods=['PUT'])
    def update_camera(id):
        # ADD NEW CAMERA
        body = request.get_json()
        for item in db.session.query(Camera).filter_by(id = id):
            # Camera(body['name'], body['ipaddress'], body['location'], body["thumbnail"], body["online"], body['timezone'], "YES"))
            item.name = body['name']
            item.ipaddress = body['ipaddress']
            item.location = body['location']
            item.timezone = body['timezone']
        db.session.commit()

        return jsonify({"msg" : "Success"})

    # desc: DELETE CAMERA'S INFO
    # path: /cameras/<id> [DELETE]
    @blueprint.route(f'/{resource_prefix}/<id>', methods=['DELETE'])
    def delete_camera(id):
        # DELETE NEW CAMERA
        shutil.rmtree('./share/{}'.format(id))
        db.session.query(Video).filter_by(camera_id = id).delete()
        db.session.query(Thumbnail).filter_by(camera_id = id).delete()
        db.session.query(Camera).filter_by(id = id).delete()
        db.session.commit()

        return jsonify({"msg" : "Success"})

    # desc: USE CAMERA IN LIVE MOD
    # path: /cameras/<id> [GET]
    @blueprint.route(f'/{resource_prefix}/<id>/<mode>/<video>', methods=['GET'])
    def live_mod(id, mode, video):
        vod_url = video.replace("*", "/")
        if(mode == "VOD"):
            if os.path.exists(".{}".format(vod_url)):
                print("----------------------------------------",vod_url)
                os.remove(".{}".format(vod_url))
        return jsonify({"id": id, "action": "Live MOD"})

    # desc: GET cameras WITH FILTERS
    # path: /cameras/<location>/<name> [GET]
    @blueprint.route(f'/{resource_prefix}/search/<name>', methods=['GET'])
    def search_camera(name):

        # SEARCH WITH NAME AND LOCATION
        cameras = []
        for item in db.session.query(Camera).filter(or_(Camera.name.contains(name), Camera.location.contains(name))):
            del item.__dict__['_sa_instance_state']
            cameras.append(item.__dict__)
        return jsonify(cameras)

    # desc: ADD Camera
    # path: /cameras [POST]
    @blueprint.route(f'/{resource_prefix}', methods=['POST'])
    def create_camera():
        # ADD NEW CAMERA
        body = request.get_json()
        db.session.add(
            Camera(body['name'], body['ipaddress'], body['location'], body["thumbnail"], body["online"], body['timezone'], "YES"))
        db.session.commit()

        camera = {}
        for item in db.session.query(Camera).all():
            del item.__dict__['_sa_instance_state']
            camera = item.__dict__

        # CREATE NEW SUB ROOT DIR FOR NEW CAMERA
        path = ".{}".format(ROOT_PATH)
        sub_root = os.path.join(path, '{}'.format(camera["id"]))
        os.mkdir(sub_root)

        # CREATE DIR FOR VIDEO STORE
        video_dir = os.path.join(sub_root, "videos")
        os.mkdir(video_dir)

        # CREATE DIR FOR THUMBNAIL STORE
        thumbnail_dir = os.path.join(sub_root, "thumbnails")
        os.mkdir(thumbnail_dir)

        return camera

    return blueprint
