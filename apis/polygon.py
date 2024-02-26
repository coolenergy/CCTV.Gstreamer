# LOAD STANDARD PACKAGE
import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import shutil

# LOAD CUSTOMIZED PACKAGE
from app import db, Camera, Thumbnail, Video, Polygon
from sqlalchemy import or_, desc, not_

# Load ENV Values
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")

# RETURN blueprint FILE
def create_polygon_blueprint(blueprint_name: str, resource_type: str, resource_prefix: str) -> Blueprint:
    blueprint = Blueprint(blueprint_name, __name__)

    # desc: Get Polygons OF THE table
    # path: /polygons [GET]
    @blueprint.route(f'/{resource_prefix}/<camera_id>', methods=['GET'])
    def get_items(camera_id):        
        polygons = []
        for item in db.session.query(Polygon).filter_by(camera_id = camera_id).order_by(Polygon.id):
            del item.__dict__['_sa_instance_state']
            polygons.append(item.__dict__)
        return jsonify(polygons)

    # desc: ADD Polygon
    # path: /polygon [POST]
    @blueprint.route(f'/{resource_prefix}', methods=['POST'])
    def create_polygon():
        # ADD NEW POLYGON
        body = request.get_json()
        db.session.add(
            Polygon(body['name'], body['desc'], body['position'], body['color'], body['camera_id']))
        db.session.commit()

        return jsonify("polygons")

    # desc: UPDATE POLYGON'S INFO
    # path: /polygons/<id> [PUT]
    @blueprint.route(f'/{resource_prefix}/<id>', methods=['PUT'])
    def update_polygon(id):
        # ADD NEW CAMERA
        body = request.get_json()
        for item in db.session.query(Polygon).filter_by(id = id):
            # Camera(body['name'], body['ipaddress'], body['location'], body["thumbnail"], body["online"], body['timezone'], "YES"))
            item.desc = body['desc']
            item.position = body['position']
        db.session.commit()

        print(id, body["position"], body['desc'])

        return jsonify({"msg" : "Success"})
    
    # desc: DELETE POLYGON'S INFO
    # path: /polygons/<id> [DELETE]
    @blueprint.route(f'/{resource_prefix}/<id>', methods=['DELETE'])
    def delete_polygon(id):
        # DELETE POLYGON
        db.session.query(Polygon).filter_by(id = id).delete()
        db.session.commit()

        return jsonify({"msg" : "Success"})

    return blueprint
