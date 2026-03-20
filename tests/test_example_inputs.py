import unittest
import json
import os
from index import handler

EXAMPLE_INPUTS_DIR = "src/agent/utils/example_inputs"


class TestExampleInputs(unittest.TestCase):
    """
    Tests that each example input file in src/agent/utils/example_inputs/
    can be processed end-to-end through the handler and returns a valid
    ChatResponse with status 200.
    """

    def _load_example(self, filename: str) -> dict:
        path = os.path.join(EXAMPLE_INPUTS_DIR, filename)
        with open(path, "r") as f:
            return json.load(f)

    def _run_example(self, filename: str) -> dict:
        payload = self._load_example(filename)
        event = {"body": json.dumps(payload)}
        return handler(event, None)

    def test_example_input_1(self):
        result = self._run_example("example_input_1.json")
        self.assertEqual(result.get("statusCode"), 200)
        body = json.loads(result.get("body"))
        self.assertIn("output", body)
        self.assertIsNotNone(body["output"].get("content"))

    def test_example_input_2(self):
        result = self._run_example("example_input_2.json")
        self.assertEqual(result.get("statusCode"), 200)
        body = json.loads(result.get("body"))
        self.assertIn("output", body)
        self.assertIsNotNone(body["output"].get("content"))

    def test_example_input_3(self):
        result = self._run_example("example_input_3.json")
        self.assertEqual(result.get("statusCode"), 200)
        body = json.loads(result.get("body"))
        self.assertIn("output", body)
        self.assertIsNotNone(body["output"].get("content"))
