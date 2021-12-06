from logging import Logger
from flask import Blueprint, config, request, url_for, redirect, Response, make_response, jsonify, session, render_template
from flask import current_app as app
from flask_login import current_user as user
from neomodel import relationship
from models import ThingDescription
from neo4j_service import Neo4jService
from utils import is_json_request, format_thing_description

api = Blueprint('api', __name__)
ERROR_JSON = {"error": "Invalid request."}

def delete_local_thing_description(thing_id: str) -> bool:
    """Delete the thing description with the specific 'thing_id' in local directory and return whether the deletion is complete.
    This is the function that perform the real thing description deletion oepration. It will do it locally by deleting the 
    thing description specified by `thing_id` field. 
    Args:
        thing_id (str): ID for thing description to be deleted
    Return:
        bool: True if the deletion is complete, if any error happens in the whole prcesss, then return False
    """
    delete_thing = ThingDescription.nodes.first(thing_id=thing_id)
    if delete_thing is None:
        return True
    delete_thing.delete()
    return True


@api.route('/register', methods=['POST'])
def register():
    """Register thing description at the target location. 
    If the current directory is the target location specified by `location` argument, the operation is processed locally
    
    Args:
        All of the following arguments are required and passed in the request URL.
        td (JSON str): the information of the thing description to be registered in JSON format
        location (str): the location where the thing description should be registered
    Returns:
        HTTP Response: if the register is completed, a simple success string with HTTP status code 200 is returned
            Otherwise a reason is returned in the response and HTTP status code is set to 400
    """
    if not is_json_request(request, ["id"]):
        return jsonify(ERROR_JSON), 400
    
    body = request.get_json()
    thing_description = body # body['td']
    fmt_td = format_thing_description(thing_description, ["id", "title"])
    new_td = ThingDescription(thing_id =thing_description["id"], title = thing_description["title"], **fmt_td)

    if "links" in thing_description:
        for link in thing_description["links"]:
            rel = link["rel"]
            rel_thing_id = link["href"]
            try:
                _ = ThingDescription.nodes.first(thing_id=rel_thing_id)
            except Exception as e:
                new_err = ERROR_JSON
                new_err["error"] += "Thing in links not found"
                return jsonify(new_err), 400
            new_td.save()
            nsrv_obj = Neo4jService()
            rel_node = nsrv_obj.find_nodes_by_template("THING_DESCRIPTION", {"thing_id":rel_thing_id})[0]
            thing_node = nsrv_obj.find_nodes_by_template("THING_DESCRIPTION", {"thing_id":thing_description["id"]})[0]
            nsrv_obj.create_relationship(thing_node, rel, rel_node)
    else:
        new_td.save()
    
    return make_response("Created", 200)

