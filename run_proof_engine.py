import hashlib
import json
import os
from datetime import datetime
from flask import Flask

app = Flask(__name__)

def execute_merkle_logic():
    tasks = [f'task_{i}' for i in range(1000)]
    leaves = [hashlib.sha256(str(t).encode()).hexdigest() for t in tasks]

    def build_tree(nodes):
        if len(nodes) == 1: return nodes[0]
        if len(nodes) % 2 != 0: nodes.append(nodes[-1])
        return build_tree([hashlib.sha256((nodes[i] + nodes[i+1]).encode()).hexdigest() for i in range(0, len(nodes), 2)])

    return build_tree(leaves)

@app.route('/')
def status_ping():
    root = execute_merkle_logic()
    return f"VERIFIED_ROOT: {root}"

if __name__ == '__main__':
    # Trigger logic on execution for GitHub Actions
    print(f"CANONICAL_ROOT: {execute_merkle_logic()}")
    # Run server for Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)