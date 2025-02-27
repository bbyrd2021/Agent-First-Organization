import logging

from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI

from agentorg.workers.worker import BaseWorker, register_worker
from agentorg.workers.message_worker import MessageWorker
from agentorg.workers.rag_worker import RAGWorker
from agentorg.utils.graph_state import MessageState
from agentorg.utils.model_config import COT_MODEL

logger = logging.getLogger(__name__)


@register_worker
class ChainOfThoughtWorker(BaseWorker):
    """
    A worker that generates a chain-of-thought explanation for the current message.
    """

    description = "Chain-of-thought reasoning worker"

    def __init__(self):
        super().__init__()
        self.llm = ChatOpenAI(model=COT_MODEL["model_type_or_path"], timeout=30000)

    def execute(self, msg_state: MessageState):
        # Create a prompt that encourages step-by-step reasoning.
        prompt = (
            f"Please analyze the following input: \n\n"
            f"{msg_state.message}\n\n"
            "Chain-of-thought:"
        )
        # Invoke the language model to generate the chain-of-thought reasoning.
        chain_reasoning = self.llm.invoke(prompt)
        # Attach the chain-of-thought output to the message state.
        msg_state.chain_of_thought = chain_reasoning
        return msg_state

    def _create_action_graph(self):
        workflow = StateGraph(MessageState)
        # Instantiate each worker.
        msg_worker = MessageWorker()

        # Add nodes for each worker.
        workflow.add_node("chain_of_thought_worker", self.execute)
        workflow.add_node("message_worker", msg_worker.execute)

        # Define the workflow edges.
        # The flow is: START -> RAG -> Chain-of-Thought -> Message

        workflow.add_edge(START, "chain_of_thought_worker")
        workflow.add_edge("chain_of_thought_worker", "message_worker")

        return workflow

    def execute(self, msg_state: MessageState):
        graph = self.action_graph.compile()
        result = graph.invoke(msg_state)
        return result
