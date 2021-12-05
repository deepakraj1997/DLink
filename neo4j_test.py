from py2neo import data, Graph, NodeMatcher, Node, Relationship, RelationshipMatcher, database


class Directory(object):
    """
    This object provides a set of helper methods for creating and retrieving nodes and relationships from
    a Neo4j database holding information about players, teams, fans, comments and their relationships.
    """

    # Note:
    # I tend to avoid object mapping frameworks. Object mapping frameworks are fun in the beginning
    # but tend to be annoying after a while. So, I did not create types Player, Team, etc.
    #


    # Connects to the DB and sets a Graph instance variable.
    # Also creates a NodeMatcher and RelationshipMatcher, which are a py2neo framework classes.
    def __init__(self,  auth=('neo4j', 'deepak'), host='localhost', port=7687, secure=False, ):
        self._graph = Graph(secure=secure,
                            bolt=True,
                            auth=auth,
                            host=host,
                            port=port)
        self._node_matcher = NodeMatcher(self._graph)
        self._relationship_matcher = RelationshipMatcher(self._graph)

    def run_q(self, qs, args):
        """

        :param qs: Query string that may have {} slots for parameters.
        :param args: Dictionary of parameters to insert into query string.
        :return:  Result of the query, which executes as a single, standalone transaction.
        """
        try:
            tx = self._graph.begin(autocommit=False)
            result = self._graph.run(qs, args)
            return result
        except Exception as e:
            print("Run exaception = ", e)

    def run_match(self, labels=None, properties=None):
        """
        Uses a NodeMatcher to find a node matching a "template."
        :param labels: A list of labels that the node must have.
        :param properties: A dictionary of {property_name: property_value} defining the template that the
            node must match.
        :return: An array of Node objects matching the pattern.
        """
        #ut.debug_message("Labels = ", labels)
        #ut.debug_message("Properties = ", json.dumps(properties))

        if labels is not None and properties is not None:
            result = self._node_matcher.match(labels, **properties)
        elif labels is not None and properties is None:
            result = self._node_matcher.match(labels)
        elif labels is None and properties is not None:
            result = self._node_matcher.match(**properties)
        else:
            raise ValueError("Invalid request. Labels and properties cannot both be None.")

        # Convert NodeMatch data into a simple list of Nodes.
        full_result = []
        for r in result:
            full_result.append(r)

        return full_result

    def find_nodes_by_template(self, tmp):
        """

        :param tmp: A template defining the label and properties for Nodes to return. An
         example is { "label": "Fan", "template" { "last_name": "Ferguson", "first_name": "Donald" }}
        :return: A list of Nodes matching the template.
        """
        labels = tmp.get('label', None)
        props = tmp.get("template", None)
        result = self.run_match(labels=labels, properties=props)
        return result

    def create_node(self, label, **kwargs):
        n = Node(label, **kwargs)
        tx = self._graph.begin(autocommit=True)
        tx.create(n)
        return n
    
    def create_relationship(self, source_a, relationship, source_b):
        rl = Relationship(source_a, relationship, source_b)
        # tx = self._graph.begin(autocommit=True)
        self._graph.create(rl)
        return rl

    def find_relationships(self, source_label, source_id, relationship, template):

        # cypher = "MATCH (:%s {manager_id: '%s'}) - [%s] - (end_node) RETURN end_node" % (source_label, source_id, relationship)
        cypher = "MATCH (:%s {manager_id: '%s'}) - [%s:%s] - (end_node) RETURN end_node" % (source_label, source_id, relationship, relationship)
        results = self._graph.run(cypher)
        return [dict(row["end_node"]) for row in results]

def clevel1():
    dir_obj = Directory()
    lvl1 = {"id":"level1"}
    try:
        dir_obj.create_node("DIRECTORY", **lvl1)
    except database.work.ClientError as e:
        print("Directory Already Exists")
    schema = database.Schema(dir_obj._graph)
    if 'id' not in schema.get_uniqueness_constraints("DIRECTORY"):
        schema.create_uniqueness_constraint("DIRECTORY", "id")
    if 'id' not in schema.get_uniqueness_constraints("THING"):
        schema.create_uniqueness_constraint("THING", "id")
    smart_home_ctrl = {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "id": "urn:dev:wot:com:example:servient:sm_hw_ctrl",
        "title": "Smart Home Controller - Main",
        "@type": "smart_controller",
        "securityDefinitions": {
            "basic_sc": {
                "scheme": "basic",
                "in": "header"
            },
            "nosec_sc": {
                "scheme": "nosec"
            }
        },
        "security": [
            "nosec_sc"
        ],
        "properties": {
            "on": {
                "writable": True,
                "schema": { "type": "boolean" },
                "forms": [{ "href": "/things/smart_controller/properties/on" }]
            },
            "geo": {
                "coordinates": [
                    -73.97286,
                    40.73948
                ],
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "readproperty"
                        ]
                    }
                ]
            }
        },
        "actions": {
            "switch_on_lights": {
                "inputSchema": {
                "type": "object",
                "fields": [
                    {
                        "name": "thing_id",
                        "schema": { "type": "string" }
                    },
                    {
                        "name": "command",
                        "schema": { "type": "string" }
                    }
                ]
                },
                "forms": [{ "href": "/things/smart_controller/actions/switch_on_lights" }]
            }
        },
        "events": {
            "irregular_shutdown": {
                "description": "Emergency / Failure shutdown",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "subscribeevent"
                        ]
                    }
                ]
            }
        }
    }
    td_light1 = {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "id": "urn:dev:wot:com:example:servient:light1",
        "title": "Light 1",
        "@type": "light",
        "securityDefinitions": {
            "basic_sc": {
                "scheme": "basic",
                "in": "header"
            },
            "nosec_sc": {
                "scheme": "nosec"
            }
        },
        "security": [
            "nosec_sc"
        ],
        "properties": {
            "on": {
                "writable": True,
                "schema": { "type": "boolean" },
                "forms": [{ "href": "/things/lamp/properties/on" }]
            },
            "brightness": {
                "writable": True,
                "schema": "range",
                "forms": [{ "href": "/things/lamp/properties/brightness" }]
            }
        },
        "actions": {
            "switch-on": {
                "description": "On the light",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "invokeaction"
                        ]
                    }
                ],
                "safe": False,
                "idempotent": False
            }, 
            "switch-off": {
                "description": "Off the light",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "invokeaction"
                        ]
                    }
                ],
                "safe": False,
                "idempotent": False
            }
        },
        "events": {
            "send_status": {
                "description": "Send status to the controller",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "subscribeevent"
                        ]
                    }
                ]
            },
            "get_status": {
                "description": "Get status from the controller",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "subscribeevent"
                        ]
                    }
                ]
            },
            "alert": {
                "description": "Send alert to the controller",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "subscribeevent"
                        ]
                    }
                ]
            }
        },
        "links": [{
            "href": "urn:dev:wot:com:example:servient:sm_hw_ctrl",
            "rel": "controlledBy",
            "mediaType": "application/td"
        }]
    }
    td_light2 = {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "id": "urn:dev:wot:com:example:servient:light2",
        "title": "Light 2",
        "@type": "light",
        "securityDefinitions": {
            "basic_sc": {
                "scheme": "basic",
                "in": "header"
            },
            "nosec_sc": {
                "scheme": "nosec"
            }
        },
        "security": [
            "nosec_sc"
        ],
        "properties": {
            "on": {
                "writable": True,
                "schema": { "type": "boolean" },
                "forms": [{ "href": "/things/lamp/properties/on" }]
            },
            "brightness": {
                "writable": True,
                "schema": "range",
                "forms": [{ "href": "/things/lamp/properties/brightness" }]
            }
        },
        "actions": {
            "switch-on": {
                "description": "On the light",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "invokeaction"
                        ]
                    }
                ],
                "safe": False,
                "idempotent": False
            }, 
            "switch-off": {
                "description": "Off the light",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "invokeaction"
                        ]
                    }
                ],
                "safe": False,
                "idempotent": False
            }
        },
        "events": {
            "send_status": {
                "description": "Send status to the controller",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "subscribeevent"
                        ]
                    }
                ]
            },
            "get_status": {
                "description": "Get status from the controller",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "subscribeevent"
                        ]
                    }
                ]
            },
            "alert": {
                "description": "Send alert to the controller",
                "forms": [
                    {
                        "href": "http:www.a.a",
                        "contentType": "application/json",
                        "op": [
                            "subscribeevent"
                        ]
                    }
                ]
            }
        },
        "links": [{
            "href": "urn:dev:wot:com:example:servient:sm_hw_ctrl",
            "rel": "controlledBy",
            "mediaType": "application/td"
        }]
    }
    try:
        dir_obj.create_node("THING", **smart_home_ctrl)
    except database.work.ClientError as e:
        print("THING Already Exists", e)
    try:
        dir_obj.create_node("THING", **td_light1)
    except database.work.ClientError as e:
        print("THING Already Exists")
    try:
        dir_obj.create_node("THING", **td_light2)
    except database.work.ClientError as e:
        print("THING Already Exists")


    ''' try:
        template = {
            "template": {
                "id":"level1"
            },
            "label": "DIRECTORY"
        }
        level = dir_obj.find_nodes_by_template(template)
        template["template"]["id"] = "urn:dev:wot:com:example:servient:sm_hw_ctrl"
        template["label"] = "THING"
        sm1 = dir_obj.find_nodes_by_template(template)
        template["template"]["id"] = "urn:dev:wot:com:example:servient:light1"
        tdl1 = dir_obj.find_nodes_by_template(template)
        template["template"]["id"] = "urn:dev:wot:com:example:servient:light2"
        tdl2 = dir_obj.find_nodes_by_template(template)
        dir_obj.create_relationship(sm1, "BELONGS_TO", level)
        dir_obj.create_relationship(tdl1, "BELONGS_TO", level)
        dir_obj.create_relationship(tdl2, "BELONGS_TO", level)
        print(sm1)
        print(tdl1)
    except database.work.ClientError as e:
        print("THING Already Exists")
    '''



if __name__ == "__main__":
    clevel1()