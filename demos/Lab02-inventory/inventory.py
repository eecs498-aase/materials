"""Ordinary stockroom functions, supplied before the AI exercise."""
import json
from pathlib import Path

class Inventory:
    def __init__(self, path='inventory.json'):
        self.path = Path(path)

    def read(self):
        return json.loads(self.path.read_text())

    def save(self, state):
        self.path.write_text(json.dumps(state, indent=2) + '\n')

    def reserve(self, item, quantity):
        if type(quantity) is not int or quantity <= 0:
            raise ValueError('quantity must be a positive integer')
        state = self.read()
        if item not in state['stock']:
            raise ValueError(f'unknown item: {item}')
        available = state['stock'][item]
        if quantity > available:
            raise ValueError(f'only {available} {item} available; ask about reducing quantity or changing the plan')
        state['stock'][item] -= quantity
        state['reserved'][item] = state['reserved'].get(item, 0) + quantity
        self.save(state)
        return {'reserved': quantity, 'item': item, 'remaining': state['stock'][item]}

    def categorize(self, labels):
        state = self.read()
        if not isinstance(labels, dict) or set(labels) != set(state['stock']):
            raise ValueError('classify exactly the known stock items')
        if any(label not in ('equipment', 'consumable', 'other') for label in labels.values()):
            raise ValueError('unknown category')
        state['categories'] = labels
        self.save(state)
        return labels
