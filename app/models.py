
   
"""
Classes defined in this file are used with neo4j ORM library mongoengine
For more information, Please refer to its website: http://mongoengine.org/
"""

from neomodel import (config, StringProperty, IntegerProperty,
    RelationshipTo, Relationship)
from neomodel.contrib import SemiStructuredNode 
from config import config as fl_config

config.DATABASE_URL = fl_config["db"]["uri"]

print(config.DATABASE_URL)
class ThingDescription(SemiStructuredNode):
    """ORM class of Thing Description in the neo4j
    """
    thing_id = StringProperty(unique_index=True, required=True)
    title = StringProperty()
    # controlled = RelationshipTo('ThingDescription', 'ControlledBy')
    # connected = Relationship('ThingDescription', 'ControlledBy')

class Resource(SemiStructuredNode):
    """ORM class of Resource in the neo4j
    """
    id = StringProperty(unique_index=True, required=True)

class Action(SemiStructuredNode):
    """ORM class of Action in the neo4j
    """
    conditions = StringProperty(unique_index=True, required=True)

class Subject(SemiStructuredNode):
    """ORM class of Subject in the neo4j
    """
    subject = StringProperty(unique_index=True, required=True)

class Rule(SemiStructuredNode):
    """ORM class of Rule in the neo4j
    """
    ruleid = StringProperty(unique_index=True, required=True)
    context  = StringProperty()
    
    subject = RelationshipTo(Subject, 'HAS_SUBJECT')
    action = RelationshipTo(Action, 'HAS_ACTION')
    resource = RelationshipTo(Resource, 'HAS_RESOURCE')

class Policy(SemiStructuredNode):
    """ORM class of Policy in the neo4j
    """
    policyid = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    targets = StringProperty()
    effect = StringProperty()
    priority = IntegerProperty()

    rules = RelationshipTo(Rule, 'CONTAINS_RULE')