from pydantic import BaseModel, Field


class Edge(BaseModel):
    condition: str
    id: str
    target_node_id: str | None = None


class FlowNode(BaseModel):
    id: str
    name: str
    instruction: str | None = None
    static_text: str | None = None
    edges: list[Edge] = Field(default_factory=list)


class ConversationFlow(BaseModel):
    system_prompt: str
    initial_node: str
    nodes: list[FlowNode]
