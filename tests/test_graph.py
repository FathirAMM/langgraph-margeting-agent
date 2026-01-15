import unittest
from src.state import AgentState
from src.graph import graph
from langchain_core.messages import HumanMessage

class TestGraphStructure(unittest.TestCase):

    def test_graph_compilation(self):
        """Test that the graph compiles without errors."""
        self.assertIsNotNone(graph)

    def test_initial_state(self):
        """Test the state definition."""
        state = AgentState(messages=[], next="")
        self.assertEqual(state["messages"], [])

if __name__ == '__main__':
    unittest.main()
