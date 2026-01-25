"""
Project: The Last Question
Mark 0
"""

__version__ = "0.1.0"
__author__ = "Varun Srinivasan"


# ===============================================
# Section 0: Imports
# ===============================================

import os
import time
import json
import tomllib
import hashlib
from pathlib import Path
from contextlib import ExitStack, contextmanager
from typing import Literal, NamedTuple
from dataclasses import dataclass, asdict
from lean_dojo import LeanGitRepo, Theorem, Dojo, ProofFinished, TacticState, LeanError

# ===============================================
# Section 1: Global variables
# ===============================================

CONFIG_FILE_NAME = "config.toml"
CACHE_DIR = ".cache/tlq0"
ATTEMPTS_DIR = "attempts"

# ===============================================
# Section 2: Config / Settings
# ===============================================

def load_config() -> dict:
    """Loads config from config.toml.

    Raises:
        FileNotFoundError: If config file doesn't exist.
    """
    config_path = Path(__file__).parent / CONFIG_FILE_NAME

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "rb") as f:
        return tomllib.load(f)

# ===============================================
# Section 3: Utilities
# ===============================================

def stable_hash(*parts: str) -> str:
    return hashlib.sha1(json.dumps(parts).encode()).hexdigest()

def now_timestamp() -> float:
    return time.time()

# ===============================================
# Section 4: Domain Types
# ===============================================

AttemptRecordStatus = Literal["solved", "not_solved", "error"]

class RunTacticResult(NamedTuple):
    status: str
    message: str | None
    is_solved: bool

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
    status: AttemptRecordStatus
    init_pp: str
    final_pp: str | None = None
    error_msg: str | None = None
    started_ts: float = 0.0
    completed_ts: float = 0.0

# ===============================================
# Section 5: LeanDojo Adapter
# ===============================================

@contextmanager
def dojo_session(theorem_spec: TheoremSpec):
    repo = LeanGitRepo(theorem_spec.repo_spec.repo_url, theorem_spec.repo_spec.commit)
    theorem = Theorem(repo, Path(theorem_spec.file_path), theorem_spec.theorem_name)
    with Dojo(theorem) as (dojo, current_state):
        yield dojo, current_state

class TacticRunner:
    def __init__(self, dojo : Dojo, current_state : TacticState):
        self.dojo = dojo
        self.current_state = current_state

    def get_initial_pp(self) -> str:
        return self.current_state.pp

    def run_tactic(self, tactic: str) -> RunTacticResult:
        """
        Run a tactic on the current state.
        Returns:
            tuple of (status, message, is_solved)
            - status: "ok" | "error" | "solved"
            - message: new proof state PP, or error message, or None
            - is_solved: True if proof is complete
        """
        result = self.dojo.run_tac(state=self.current_state, tactic=tactic)

        if isinstance(result, ProofFinished):
            return RunTacticResult("solved", None, True)

        elif isinstance(result, TacticState):
            self.current_state = result
            return RunTacticResult("ok", result.pp, False)

        elif isinstance(result, LeanError):
            return RunTacticResult("error", result.error, False)

        else:
            return RunTacticResult("error", f"unknown result type {result}", False)

# ===============================================
# Section 6: Artifact Types
# ===============================================

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def write_attempt_record(record: AttemptRecord) -> Path:
    dir_path = Path(CACHE_DIR) / ATTEMPTS_DIR / record.attempt_id
    ensure_dir(dir_path)
    record_as_dict = asdict(record)
    file_path = dir_path / "attempt.json"
    with open(file_path, "w") as f:
        json.dump(record_as_dict, f, indent=2)
    return file_path

# ===============================================
# Section 7: Proof Attempt Orchestration
# ===============================================

def attempt_proof(theorem_spec: TheoremSpec, tactics: list[str]) -> AttemptRecord:
    attempt_id = stable_hash(
        theorem_spec.repo_spec.repo_url,
        theorem_spec.repo_spec.commit,
        theorem_spec.file_path,
        theorem_spec.theorem_name,
        *tactics)
    started_ts = now_timestamp()
    status: AttemptRecordStatus = "not_solved"
    error_msg: str | None = None
    final_pp: str | None = None

    with dojo_session(theorem_spec) as (dojo, current_state):
        init_pp = current_state.pp
        tactic_runner = TacticRunner(dojo, current_state)
        for tactic in tactics:
            run_tactic_result = tactic_runner.run_tactic(tactic)
            if run_tactic_result.status == "solved":
                status = "solved"
                break
            elif run_tactic_result.status == "error":
                status = "error"
                error_msg = run_tactic_result.message
                break
            else:
                final_pp = run_tactic_result.message

    completed_ts = now_timestamp()
    attempt_record = AttemptRecord(
        attempt_id=attempt_id,
        theorem_spec=theorem_spec,
        tactics=tactics,
        status=status,
        init_pp=init_pp,
        final_pp=final_pp,
        error_msg=error_msg,
        started_ts=started_ts,
        completed_ts=completed_ts
    )
    write_attempt_record(attempt_record)
    return attempt_record


if __name__ == "__main__":
    print("tlq v" + __version__)
    try:
        config = load_config()
    except FileNotFoundError as e:
        print(f"Error {e}")
        print(f"Error {e}")

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

    # Test Artifact Types
    attempt_record_path = write_attempt_record(attempt_record)
    print(f"AttemptRecord path: {attempt_record_path}")

    # Test LeanDojo Adapter
    print("\n--- Testing LeanDojo Adapter ---")
    with dojo_session(theorem_spec) as (dojo, current_state):
        initial_state = current_state.pp
        tactic_runner = TacticRunner(dojo, current_state)
        print(f"Initial state: {initial_state}")
        status, msg, solved = tactic_runner.run_tactic("rw [add_assoc, add_comm b, ←add_assoc]")
        print(f"After tactic: status={status}, solved={solved}")
        if msg:
            print(f"Message: {msg}")

    # Test Proof Attempt Orchestration
    result = attempt_proof(
        theorem_spec=theorem_spec,
        tactics=["rw [add_assoc, add_comm b, ←add_assoc]"]
    )
    print(f"Attempt result: {result.status}")
    print(f"Attempt ID: {result.attempt_id}")
    print(f"Saved to: .cache/tlq0/attempts/{result.attempt_id}/attempt.json")

    # Test immutability of frozen dataclasses
    try:
        repo_spec.commit = "different"  # This should fail!
    except Exception as e:
        print(f"\nFrozen works! Can't modify RepoSpec: {type(e).__name__}")




