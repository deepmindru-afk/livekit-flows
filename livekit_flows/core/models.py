from pydantic import BaseModel, Field
from .enums import FieldType, HttpMethod, ActionTriggerType


class DataField(BaseModel):
    name: str
    type: FieldType
    description: str
    required: bool = False


class CustomAction(BaseModel):
    id: str
    name: str
    description: str
    method: HttpMethod
    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    body_template: str | None = None
    timeout: int = 30
    store_response_as: str | None = None


class ActionTrigger(BaseModel):
    trigger_type: ActionTriggerType
    action_id: str


class Edge(BaseModel):
    condition: str
    id: str
    target_node_id: str | None = None
    collect_data: list[DataField] = Field(default_factory=list)
    actions: list[ActionTrigger] = Field(default_factory=list)


class FlowNode(BaseModel):
    id: str
    name: str
    instruction: str | None = None
    static_text: str | None = None
    is_final: bool = False
    edges: list[Edge] = Field(default_factory=list)
    actions: list[ActionTrigger] = Field(default_factory=list)


class ConversationFlow(BaseModel):
    system_prompt: str
    initial_node: str
    nodes: list[FlowNode]
    actions: list[CustomAction] = Field(default_factory=list)
    environment_variables: dict[str, str] = Field(default_factory=dict)
