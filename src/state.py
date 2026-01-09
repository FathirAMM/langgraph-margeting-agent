import operator
from typing import Annotated, List, TypedDict, Union
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # The list of messages in the conversation
    messages: Annotated[List[BaseMessage], operator.add]
    # The next agent to act
    next: str
