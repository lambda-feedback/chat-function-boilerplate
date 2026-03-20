import unittest
import json
from index import handler


class TestChatIndexFunction(unittest.TestCase):
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

    Use handler() to check your algorithm works as it should.

    The expected input of the handler is a muEd ChatRequest.
    """

    def _make_event(self, payload: dict) -> dict:
        return {"body": json.dumps(payload)}

    def _valid_event(self) -> dict:
        return self._make_event({
            "conversationId": "1234Test",
            "messages": [
                {"role": "USER", "content": "Hello, World"}
            ],
            "user": {
                "type": "LEARNER"
            }
        })

    def test_missing_messages(self):
        event = self._make_event({
            "conversationId": "1234Test",
            "user": {"type": "LEARNER"}
        })
        result = handler(event, None)
        self.assertEqual(result.get("statusCode"), 400)

    def test_invalid_json_body(self):
        event = {"body": "not valid json {"}
        result = handler(event, None)
        self.assertEqual(result.get("statusCode"), 400)

    def test_correct_arguments(self):
        result = handler(self._valid_event(), None)
        self.assertEqual(result.get("statusCode"), 200)

    def test_correct_response(self):
        result = handler(self._valid_event(), None)
        self.assertEqual(result.get("statusCode"), 200)
        body = json.loads(result.get("body"))
        self.assertIn("output", body)
