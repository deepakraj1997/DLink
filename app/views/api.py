import json
from logging import Logger, error
from flask import Blueprint, config, request, url_for, redirect, Response, make_response, jsonify, session, render_template
from flask import current_app as app
from flask_login import current_user as user
from neomodel import relationship
from neomodel.exceptions import UniqueProperty
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

# Case links in same belongs to not handled
@api.route('/register', methods=['POST'])
def register():
    """Register thing description at the target location. 
    If the current directory is the target location specified by `location` argument, the operation is processed locally
    
    Args:
        All of the following arguments are required and passed in the request URL.
        td (JSON str): the information of the thing description to be registered in JSON format
    Returns:
        HTTP Response: if the register is completed, a simple success string with HTTP status code 200 is returned
            Otherwise a reason is returned in the response and HTTP status code is set to 400
    """
    if not is_json_request(request, ["td"]):
        return jsonify(ERROR_JSON), 400
    
    body = request.get_json()
    thing_description = body["td"]
    fmt_td = format_thing_description(thing_description, ["id", "title"])
    new_td = ThingDescription(thing_id=thing_description["id"], title = thing_description["title"], **fmt_td)    
    nsrv_obj = Neo4jService()
    try:
        # new_td.create_or_update() # new_td.save()
        new_td.save()
    except UniqueProperty as _:
        return make_response("Unique Property Violation, check your input", 400)

    if "links" in thing_description:
        for link in thing_description["links"]:
            rel = link["rel"]
            rel_thing_id = link["href"]
            if rel != "belongsTo":
                try:
                    # _ = ThingDescription.nodes.first(thing_id=rel_thing_id)
                    rel_node = nsrv_obj.find_nodes_by_template("ThingDescription", {"thing_id":rel_thing_id})
                    if not rel_node:
                        raise error("Rel Thing not found")
                except Exception as e:
                    print(e)
                    new_err = ERROR_JSON
                    new_err["error"] += "Thing in links not found"
                    return jsonify(new_err), 400
                except Exception as e:
                    return make_response("Internal Server Error", 500)
                print(rel_thing_id)
                rel_node = nsrv_obj.find_nodes_by_template("ThingDescription", {"thing_id":rel_thing_id})[0]
                thing_node = nsrv_obj.find_nodes_by_template("ThingDescription", {"thing_id":thing_description["id"]})[0]
                nsrv_obj.create_relationship(thing_node, rel, rel_node)
            else:
                thing_node = nsrv_obj.find_nodes_by_template("ThingDescription", {"thing_id":thing_description["id"]})[0]
                thing_node.add_label(rel_thing_id)
                nsrv_obj._graph.push(thing_node)
                label_nodes = nsrv_obj.find_nodes_by_template(rel_thing_id, {"setup": True})
                label_node = None
                setup_args = {"setup": True, "name": rel_thing_id}
                if not label_nodes:
                    label_node = nsrv_obj.create_node(rel_thing_id, **setup_args)
                else:
                    label_node = label_nodes[0]
                nsrv_obj.create_relationship(thing_node, rel, label_node)
    
    return make_response("Created", 200)

@api.route('/delete', methods=['POST', 'DELETE'])
@api.route('/delete/<thing_id>', methods=['POST', 'DELETE'])
def delete(thing_id):
    """
        Deletes a thing
    """
    nsrv_obj = Neo4jService()
    thing_node = nsrv_obj.find_nodes_by_template("ThingDescription", {"thing_id":thing_id})[0]
    nsrv_obj.delete_node(thing_node)
    return make_response("Deleted", 200)

@api.route('/action')
@api.route('/action/<action>/<thing_id>')
def action(action, thing_id):
    """
        Simulates an action of a thing
    """
    nsrv_obj = Neo4jService()
    thing_node = nsrv_obj.find_nodes_by_template("ThingDescription", {"thing_id":thing_id})[0]
    thing_actions = json.loads(thing_node["actions"])
    selected_action = thing_actions[action]
    thing_properties = json.loads(thing_node["properties"])

    if selected_action["forms"][0]["type"] == "self":
        if selected_action["forms"][0]["function"] != "on" and not thing_properties["on"]["status"]:
            return make_response("Thing is not on!", 400)
        if selected_action["forms"][0]["function"] in thing_properties:
            thing_properties[selected_action["forms"][0]["function"]]["status"] = not selected_action["forms"][0]["negate"]
            thing_node["properties"] = json.dumps(thing_properties)
            nsrv_obj._graph.push(thing_node)
    else:
        query_res = nsrv_obj.run_q("MATCH (m:ThingDescription)-[rel1]->(o:ThingDescription) where o.thing_id=$thing_id return m", {"thing_id": thing_id})
        child_nodes = query_res.data()

        for node in child_nodes:
            child_properties = json.loads(node['n']["properties"])
            if not child_properties["on"]["status"]:
                continue
            if selected_action["forms"][0]["function"] in child_properties:
                child_properties[selected_action["forms"][0]["function"]]["status"] = not selected_action["forms"][0]["negate"]
                node['n']["properties"] = json.dumps(child_properties)
                nsrv_obj._graph.push(node)             

    return make_response("Action Successful", 200)