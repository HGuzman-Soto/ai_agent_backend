from typing import List, Literal
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
import requests


class URLProcessorAgent:
    def __init__(self, model_name: str, temperature: float = 0):
        # Initialize the model and tools
        self.tools = [self.search_tool]
        self.tool_node = ToolNode(self.tools)
        self.model = ChatAnthropic(model=model_name, temperature=temperature).bind_tools(self.tools)
        self.checkpointer = MemorySaver()

        # Initialize the state graph
        self.workflow = self._build_state_graph()

    @staticmethod
    @tool
    def search_tool(query: str) -> str:
        """Fetches content from a URL."""
        try:
            response = requests.get(query)
            response.raise_for_status()  # Check for errors
            return response.text[:500]  # Limit content for LLM (e.g., first 500 characters)
        except Exception as e:
            return f"Failed to fetch content: {str(e)}"

    def _build_state_graph(self) -> StateGraph:
        """Builds the state graph with nodes and transitions."""
        workflow = StateGraph(MessagesState)

        # Define the two nodes: agent and tools
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tool_node)

        # Define the edges between nodes
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self.should_continue)
        workflow.add_edge("tools", "agent")

        return workflow

    def should_continue(self, state: MessagesState) -> Literal["tools", END]:
        """Determines whether to continue processing or stop."""
        messages = state['messages']
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    def call_model(self, state: MessagesState) -> dict:
        """Calls the LLM model with the current state."""
        messages = state['messages']
        response = self.model.invoke(messages)
        return {"messages": [response]}

    def process_urls(self, urls: List[str], thread_id: int = 42) -> List[str]:
        """Processes a list of URLs and returns their analysis."""
        results = []
        app = self.workflow.compile(checkpointer=self.checkpointer)
        
        for url in urls:
            # Invoke the app for each URL and append results
            final_state = app.invoke(
                {"messages": [HumanMessage(content=f"Analyze the content of this URL: {url}")]},
                config={"configurable": {"thread_id": thread_id}}  # Provide thread_id
            )
            result = final_state["messages"][-1].content
            results.append(result)
        
        return results
