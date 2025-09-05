from enum import Enum


class FieldType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ActionTriggerType(str, Enum):
    ON_ENTER = "on_enter"
    ON_EXIT = "on_exit"
    ON_EDGE = "on_edge"
