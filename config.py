import os

"""
Set up the configuration for flask environment using classes

:BaseConfig: the parent class for all configuration class, used for common settings

:TestConfig: the configuration class for test environment
:DevConfig: the configuration class for development environment
:DepConfig: the configuration class for deployment environment
"""


class BaseConfig(object):
    # Used for flask session to generate session id
    SECRET_KEY = os.urandom(128)

    @classmethod
    def to_dict(cls):
        """
        Convert attributes to a dictionary form, which is used for Eve library setting
        """
        return {attr: getattr(cls, attr) for attr in dir(cls) if attr.isupper()}

class TestConfig(BaseConfig):
    # Testing Environment Configuration
    ENV_NAME = "Test"


"""
Development configurations
"""
class DevConfig(BaseConfig):
    # Development Environment Configuration
    ENV_NAME = "Development"
    # Mongo Engine
    # MONGODB_HOST = 'localhost'
    # MONGODB_PORT = 27017
    # BOUNDING_BOX_COORDS = []
    NEO4J_HOST = 'localhost'
    NEO4J_PORT = 7474


class Level1DevConfig(DevConfig):
    BOUNDING_BOX_COORDS =   [
                                [
                                    -73.9413571357727,
                                    40.847376876001356
                                ],
                                [
                                    -73.94136786460875,
                                    40.84621629553305
                                ],
                                [
                                    -73.93925428390502,
                                    40.846524703514575
                                ],
                                [
                                    -73.93953323364258,
                                    40.84750672989431
                                ],
                                [
                                    -73.9413571357727,
                                    40.847376876001356
                                ]
                            ]
    HOST_NAME = "level1"
    ENV_NAME = "Level1-Dev"
    PORT=5001
    # mongo engine
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5001/'
    OAUTH2_JWT_KEY = 'level1-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600

dev_config = {
    "level1": Level1DevConfig,
}


class DepConfig(BaseConfig):
    # Deployment Environment Configurations
    ENV_NAME = "Deployment"
