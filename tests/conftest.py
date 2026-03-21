import sys
from pathlib import Path

# Add project root to path so `from backend.x import ...` works
sys.path.insert(0, str(Path(__file__).parent.parent))

# Also add backend dir so bare imports (`from prompts import ...`) work
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
