"""
Classes defined in this file are used with neo4j ORM library mongoengine
For more information, Please refer to its website: http://mongoengine.org/
"""

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo)
from neomodel.contrib import SemiStructuredNode 

config.DATABASE_URL = 'bolt://neo4j:deepak1234@localhost:7687'

class ThingDescription(SemiStructuredNode):
    """ORM class of Thing Description in the neo4j

    """
    tid = StringProperty(unique_index=True, required=True)
    title = StringProperty()

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

# class DynamicAttributes(DynamicDocument):
#     """"ORM class that stores dynamic attributes int he database
#     """
#     attribute_id = StringField(db_field='attribute_id',
#                            required=True, unique=False, max_length=160)
#     attribute_name = StringField(db_field='attribute_name')
#     attribute_type = StringField(db_field='attribute_type')
#     attribute_value = IntField(db_field='attribute_value')
#     attribute_datetime = DateTimeField(db_field = 'attribute_date')
#     user_id = IntField(db_field='user_id',
#                            required=True, unique=False)
#     meta = {'collection': 'dynamic_attributes'}


# class LevelBoundingBox(DynamicDocument):
#     """"ORM class that stores bounding box of each level
#     """
#     level = StringField(db_field='level',
#                            required=True, unique=True)
#     geometry = PolygonField(db_field='geometry', required = False)
#     meta = {'collection': 'level_bounding_box'}

