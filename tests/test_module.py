import unittest
from lf_toolkit.chat import ChatRequest, ChatResponse
from src.module import chat_module


class TestChatModuleFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use chat_module() to check your algorithm works as it should.
    """

    def _make_request(self, **kwargs) -> ChatRequest:
        defaults = {
            "conversationId": "1234Test",
            "messages": [{"role": "USER", "content": "Hello, World"}],
            "user": {"type": "LEARNER"},
        }
        defaults.update(kwargs)
        return ChatRequest.model_validate(defaults)

    def test_missing_conversation_id(self):
        request = ChatRequest.model_validate({
            "messages": [{"role": "USER", "content": "Hello"}],
            "user": {"type": "LEARNER"},
        })
        with self.assertRaises(Exception) as cm:
            chat_module(request)
        self.assertIn("conversation id", str(cm.exception))

    def test_agent_output(self):
        request = self._make_request()
        result = chat_module(request)
        self.assertIsInstance(result, ChatResponse)
        self.assertIsNotNone(result.output)
        self.assertIsNotNone(result.output.content)

    def test_processing_time_in_metadata(self):
        request = self._make_request()
        result = chat_module(request)
        self.assertIsNotNone(result.metadata)
        self.assertIn("processingTimeMs", result.metadata)
        self.assertGreaterEqual(result.metadata["processingTimeMs"], 0)

    def test_with_conversation_history(self):
        request = self._make_request(
            messages=[
                {"role": "USER", "content": "What is this question about?"},
                {"role": "ASSISTANT", "content": "It's about vectors."},
                {"role": "USER", "content": "Can you help me?"},
            ]
        )
        result = chat_module(request)
        self.assertIsInstance(result, ChatResponse)
        self.assertIsNotNone(result.output.content)
