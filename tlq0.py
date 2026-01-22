"""
Project: The Last Question
Mark 0
"""

__version__ = "0.1.0"
__author__ = "Varun Srinivasan"


# ===============================================
# Section 0: Imports
# ===============================================

from pathlib import Path
import tomllib
from dataclasses import dataclass
import hashlib
import time

# ===============================================
# Section 1: Global variables
# ===============================================

CONFIG_FILE_NAME = "config.toml"

# ===============================================
# Section 2: Config / Settings
# ===============================================

def load_config() -> dict:
    """Loads config from config.toml"""
    config_path = Path(__file__).parent / CONFIG_FILE_NAME

    if not config_path.exists():
        print("Please check config file name and path")
        return {}

    with open(config_path, "rb") as f:
        print("Config loaded successfully!")
        return tomllib.load(f)

# ===============================================
# Section 3: Utilities
# ===============================================

def stable_hash(*parts: str) -> str:
    return hashlib.sha1(("\n".join(parts)).encode()).hexdigest()

def now_timestamp() -> float:
    return time.time()

# ===============================================
# Section 4: Domain Types
# ===============================================

@dataclass(frozen=True)
class RepoSpec:
    repo_url: str
    commit: str

@dataclass(frozen=True)
class TheoremSpec:
    repo_spec: RepoSpec
    file_path: str
    theorem_name: str


@dataclass
class AttemptRecord:
    attempt_id: str
    theorem_spec: TheoremSpec
    tactics: list[str]
    status: str # "solved" | "not_solved" | "error"
    init_pp: str
    final_pp: str | None = None
    error_msg: str | None = None
    started_ts: float = 0.0
    completed_ts: float = 0.0


if __name__ == "__main__":
    print("tlq v" + __version__)
    config = load_config()

    # Test our domain types
    print("\n--- Testing Domain Types ---")

    # Create a RepoSpec
    repo_spec = RepoSpec(
        repo_url="https://github.com/yangky11/lean4-example",
        commit="7b6ecb9ad4829e4e73600a3329baeb3b5df8d23f"
    )
    print(f"RepoSpec: {repo_spec}")

    # Create a TheoremSpec
    theorem_spec = TheoremSpec(
        repo_spec=repo_spec,
        file_path="Lean4Example.lean",
        theorem_name="hello_world"
    )
    print(f"TheoremSpec {theorem_spec}")

    # Create an AttemptRecord
    attempt_record = AttemptRecord(
        attempt_id="test123",
        theorem_spec=theorem_spec,
        tactics=["rfl"],
        status="solved",
        init_pp="⊢ 1 + 1 = 2"
    )
    print(f"AttemptRecord: {attempt_record}")

    # Testing utilities
    print("\n--- Testing Utilities ---")

    # Test stable_hash
    hash1 = stable_hash("a", "b", "c")
    hash2 = stable_hash("a", "b", "c")
    hash3 = stable_hash("a", "bc")

    print(f"hash1: {hash1}")
    print(f"hash2: {hash2}")
    print(f"hash3: {hash3}")
    print(f"hash1 == hash2? {hash1 == hash2}")  # Should be True
    print(f"hash1 == hash3? {hash1 == hash3}")  # Should be False

    # Test timestamp
    ts = now_timestamp()
    print(f"Current timestamp: {ts}")


    # Test immutability of frozen dataclasses
    try:
        repo_spec.commit = "different"  # This should fail!
    except Exception as e:
        print(f"\nFrozen works! Can't modify RepoSpec: {type(e).__name__}")




