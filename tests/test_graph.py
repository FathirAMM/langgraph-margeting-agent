import unittest
import os
from src.state import AgentState
from src.graph import workflow  # Import workflow instead of compiled graph
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

class TestGraphStructure(unittest.TestCase):

    def setUp(self):
        # Use in-memory database for testing
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.graph = workflow.compile(checkpointer=self.memory)

    def test_graph_compilation(self):
        """Test that the graph compiles without errors."""
        self.assertIsNotNone(self.graph)

    def test_initial_state(self):
        """Test the state definition."""
        state = AgentState(messages=[], next="")
        self.assertEqual(state["messages"], [])

    def test_nodes_exist(self):
        """Test that all required nodes are present in the graph."""
        nodes = self.graph.nodes
        self.assertIn("Supervisor", nodes)
        self.assertIn("Senior_Researcher", nodes)
        self.assertIn("Content_Strategist", nodes)
        self.assertIn("SEO_Optimizer", nodes)
        self.assertIn("Visual_Designer", nodes)
        self.assertIn("Compliance_Officer", nodes)

if __name__ == '__main__':
    unittest.main()
