import pytest
from unittest.mock import Mock, patch
from observable_agent.agent import ObservableAgent
from observable_agent.contract import Contract


class TestAgentCreation:
    def test_after_tool_callback_is_called(self):
        on_tool_call = Mock()
        contract = Contract(commitments=[])

        agent = ObservableAgent(
            name="test",
            description="A test agent",
            model="gemini-2.0-flash",
            instruction="do stuff",
            contract=contract,
            on_tool_call=on_tool_call
        )

        callback = agent.after_tool_callback
        mock_tool = Mock()
        mock_tool.name = "my_tool"

        callback(
            tool=mock_tool,
            args={"arg": "value"},
            tool_context=Mock(),
            tool_response="result"
        )

        on_tool_call.assert_called_once()

    def test_after_agent_callback_captures_span_when_observer_provided(self):
        observer = Mock()
        contract = Contract(commitments=[])
        callback_context = Mock()

        agent = ObservableAgent(
            name="test",
            description="A test agent",
            model="gemini-2.0-flash",
            instruction="do stuff",
            contract=contract,
            observer=observer
        )

        callback = agent.after_agent_callback
        callback(callback_context=callback_context)

        observer.capture_span.assert_called_once()

    def test_after_agent_callback_calls_on_implementation_complete(self):
        contract = Contract(commitments=[])
        on_implementation_complete = Mock()
        callback_context = Mock()

        agent = ObservableAgent(
            name="test",
            description="A test agent",
            model="gemini-2.0-flash",
            instruction="do stuff",
            contract=contract,
            on_implementation_complete=on_implementation_complete
        )

        callback = agent.after_agent_callback
        callback(callback_context=callback_context)

        on_implementation_complete.assert_called_once()
