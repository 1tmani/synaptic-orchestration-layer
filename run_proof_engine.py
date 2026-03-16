import hashlib
import json
import os
from datetime import datetime
from flask import Flask

app = Flask(__name__)

def execute_merkle_logic():
    ledger_path = 'continuity_ledger.json'
    if os.path.exists(ledger_path):
        with open(ledger_path, 'r') as f: ledger = json.load(f)
    else:
        ledger = {'history': []}

    # Preserve exact logic from notebook
    tasks = [f'task_{i}' for i in range(1000)]
    leaves = [hashlib.sha256(str(t).encode()).hexdigest() for t in tasks]

    def build_tree(nodes):
        if len(nodes) == 1: return nodes[0]
        if len(nodes) % 2 != 0: nodes.append(nodes[-1])
        return build_tree([hashlib.sha256((nodes[i] + nodes[i+1]).encode()).hexdigest() for i in range(0, len(nodes), 2)])

    current_root = build_tree(leaves)
    entry = {
        'root': current_root,
        'timestamp': datetime.now().isoformat(),
        'task_count': 1000,
        'status': 'RENDER_CLOUD_SYNCED'
    }
    ledger['history'].append(entry)
    with open(ledger_path, 'w') as f: json.dump(ledger, f, indent=4)
    return current_root

@app.route('/')
def status_ping():
    root = execute_merkle_logic()
    return f"✅ DISPATCHER_ACTIVE | LATEST_ROOT: {root[:16]}..."

if __name__ == '__main__':
    # Render binds to port 10000 by default for web services
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)