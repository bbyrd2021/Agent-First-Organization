import logging

from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI

from agentorg.workers.worker import BaseWorker, register_worker
from agentorg.workers.message_worker import MessageWorker
from agentorg.workers.rag_worker import RAGWorker
from agentorg.workers.cot_worker import ChainOfThoughtWorker
from agentorg.utils.graph_state import MessageState
from agentorg.utils.model_config import COT_MODEL

logger = logging.getLogger(__name__)


@register_worker
class RagChainMsgWorker(BaseWorker):
    """
    A composite worker that chains together the RAG, Chain-of-Thought, and Message Workers.
    """

    description = "A combination of RAG, chain-of-thought, and Message Workers"

    def __init__(self):
        super().__init__()
        self.action_graph = self._create_action_graph()
        self.llm = ChatOpenAI(model=COT_MODEL["model_type_or_path"], timeout=30000)

    def _create_action_graph(self):
        workflow = StateGraph(MessageState)
        # Instantiate each worker.
        rag_worker = RAGWorker()
        cot_worker = ChainOfThoughtWorker()
        msg_worker = MessageWorker()

        # Add nodes for each worker.
        workflow.add_node("rag_worker", rag_worker.execute)
        workflow.add_node("chain_of_thought_worker", cot_worker.execute)
        workflow.add_node("message_worker", msg_worker.execute)

        # Define the workflow edges.
        # The flow is: START -> RAG -> Chain-of-Thought -> Message
        workflow.add_edge(START, "rag_worker")
        workflow.add_edge("rag_worker", "chain_of_thought_worker")
        workflow.add_edge("chain_of_thought_worker", "message_worker")

        return workflow

    def execute(self, msg_state: MessageState):
        graph = self.action_graph.compile()
        result = graph.invoke(msg_state)
        return result
