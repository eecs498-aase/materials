import json
import shutil
import tempfile
import unittest
from pathlib import Path
from assistant import ScriptedModel, categorize, dispatch, run
from inventory import Inventory

class AssistantTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        path = Path(self.tmp.name) / 'inventory.json'
        shutil.copyfile('fixture.json', path)
        self.inventory = Inventory(path)

    def test_failure_feedback_and_clarification_change_next_action(self):
        answers = iter(['yes', 'share', 'yes'])
        trace = run('Five markers', self.inventory, ScriptedModel(), lambda q: next(answers), lambda x: None)
        self.assertFalse(trace[1]['observation']['ok'])
        self.assertEqual({'marker': 3}, self.inventory.read()['reserved'])
        self.assertEqual(0, self.inventory.read()['stock']['marker'])

    def test_denial_does_not_change_stock(self):
        before = self.inventory.read()
        result = dispatch({'action': 'reserve', 'args': {'item': 'marker', 'quantity': 1}}, self.inventory, lambda q: 'no')
        self.assertFalse(result['changed'])
        self.assertEqual(before, self.inventory.read())

    def test_malformed_output_reaches_next_request_and_stops(self):
        requests = []
        def broken(messages):
            requests.append(json.loads(json.dumps(messages)))
            return {'content': 'not JSON'}
        trace = run('x', self.inventory, broken, emit=lambda x: None, limit=3)
        self.assertEqual(3, len(trace))
        self.assertIn('"ok": false', requests[1][-1]['content'])

    def test_bad_classification_cannot_change_inventory(self):
        before = self.inventory.read()
        with self.assertRaises(ValueError):
            categorize(self.inventory, lambda messages: {'content': '{"invented":"equipment"}'})
        self.assertEqual(before, self.inventory.read())

    def test_classification_is_one_call(self):
        calls = []
        def classify(messages):
            calls.append(messages)
            return {'content': json.dumps({'marker':'consumable','projector':'equipment','paper pad':'consumable'})}
        categorize(self.inventory, classify)
        self.assertEqual(1, len(calls))
        self.assertEqual('equipment', self.inventory.read()['categories']['projector'])
