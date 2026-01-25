"""
Project: The Last Question
Mark 0

A Python interface for theorem proving using LeanDojo.
This module provides utilities for attempting mathematical proofs
in Lean and recording the results.
"""

__version__ = "0.1.0"
__author__ = "Varun Srinivasan"


# ===============================================
# Section 0: Imports
# ===============================================

import time
import json
import logging
import tomllib
import hashlib
from pathlib import Path
from contextlib import contextmanager
from typing import Final, Literal, NamedTuple
from dataclasses import dataclass, asdict
from lean_dojo import LeanGitRepo, Theorem, Dojo, ProofFinished, TacticState, LeanError

# ===============================================
# Section 1: Logger Setup
# ===============================================

logger = logging.getLogger(__name__)

# ===============================================
# Section 2: Global Constants
# ===============================================

CONFIG_FILE_NAME: Final[str] = "config.toml"
CACHE_DIR: Final[str] = ".cache/tlq0"
ATTEMPTS_DIR: Final[str] = "attempts"

# ===============================================
# Section 3: Config / Settings
# ===============================================

def load_config() -> dict:
    """Load configuration from config.toml file.

    Reads the TOML configuration file located in the same directory
    as this module.

    Returns:
        dict: The parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
    """
    config_path = Path(__file__).parent / CONFIG_FILE_NAME

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "rb") as f:
        return tomllib.load(f)

# ===============================================
# Section 4: Utilities
# ===============================================

def stable_hash(*parts: str) -> str:
    """Generate a deterministic SHA-1 hash from string parts.

    'Stable' means the same inputs always produce the same hash,
    even across Python versions (unlike built-in hash()).
    Uses JSON serialization to preserve the structure of inputs.

    Args:
        *parts: String components to hash.

    Returns:
        A 40-character hexadecimal hash string.
    """
    return hashlib.sha1(json.dumps(parts).encode()).hexdigest()


def now_timestamp() -> float:
    """Return the current Unix timestamp.

    Returns:
        Current time as seconds since epoch (float).
    """
    return time.time()

# ===============================================
# Section 5: Domain Types
# ===============================================

AttemptRecordStatus = Literal["solved", "not_solved", "error"]
"""Type alias for valid proof attempt statuses."""


class RunTacticResult(NamedTuple):
    """Result of running a single tactic on a proof state.

    Attributes:
        status: One of "ok", "error", or "solved".
        message: The new proof state (if ok), error message (if error), or None (if solved).
        is_solved: True if the proof is complete.
    """
    status: str
    message: str | None
    is_solved: bool


@dataclass(frozen=True)
class RepoSpec:
    """Specification for a Git repository containing Lean code.

    Attributes:
        repo_url: The URL of the Git repository.
        commit: The specific commit hash to use.
    """
    repo_url: str
    commit: str


@dataclass(frozen=True)
class TheoremSpec:
    """Specification for a theorem to prove.

    Attributes:
        repo_spec: The repository containing the theorem.
        file_path: Path to the Lean file within the repository.
        theorem_name: The name of the theorem to prove.
    """
    repo_spec: RepoSpec
    file_path: str
    theorem_name: str


@dataclass
class AttemptRecord:
    """Record of a proof attempt.

    Attributes:
        attempt_id: Unique identifier for this attempt (hash of inputs).
        theorem_spec: The theorem that was attempted.
        tactics: List of tactics that were applied.
        status: Final status of the attempt.
        init_pp: Pretty-printed initial proof state.
        final_pp: Pretty-printed final proof state (if not solved).
        error_msg: Error message (if status is "error").
        started_ts: Unix timestamp when attempt started.
        completed_ts: Unix timestamp when attempt completed.
    """
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
# Section 6: LeanDojo Adapter
# ===============================================

@contextmanager
def dojo_session(theorem_spec: TheoremSpec):
    """Context manager for a LeanDojo proving session.

    Sets up a Dojo environment for the specified theorem, handling
    all the necessary initialization (repo, theorem object) and
    cleanup automatically.

    Args:
        theorem_spec: Specification of the theorem to prove.

    Yields:
        A tuple of (dojo, current_state) for interacting with Lean.

    Example:
        with dojo_session(theorem_spec) as (dojo, state):
            result = dojo.run_tac(state, "rfl")
    """
    logger.debug(f"Opening dojo session for theorem: {theorem_spec.theorem_name}")
    repo = LeanGitRepo(theorem_spec.repo_spec.repo_url, theorem_spec.repo_spec.commit)
    theorem = Theorem(repo, Path(theorem_spec.file_path), theorem_spec.theorem_name)
    with Dojo(theorem) as (dojo, current_state):
        logger.debug("Dojo session started successfully")
        yield dojo, current_state
    logger.debug("Dojo session closed")


class TacticRunner:
    """Handles running tactics on a proof state within a Dojo session.

    This class wraps a Dojo instance and manages the current proof state,
    providing a cleaner interface for running tactics sequentially.

    Attributes:
        dojo: The active Dojo instance.
        current_state: The current proof state (updated after each tactic).
    """

    def __init__(self, dojo: Dojo, current_state: TacticState):
        """Initialize the TacticRunner.

        Args:
            dojo: An active Dojo instance.
            current_state: The initial proof state.
        """
        self.dojo = dojo
        self.current_state = current_state

    def get_initial_pp(self) -> str:
        """Get the pretty-printed representation of the current proof state.

        Returns:
            The proof state as a human-readable string.
        """
        return self.current_state.pp

    def run_tactic(self, tactic: str) -> RunTacticResult:
        """Run a tactic on the current proof state.

        Applies the given tactic and updates the internal state if successful.

        Args:
            tactic: The Lean tactic to apply (e.g., "rfl", "simp").

        Returns:
            RunTacticResult containing:
                - status: "ok" (tactic applied), "error" (tactic failed), or "solved" (proof complete)
                - message: New proof state, error message, or None
                - is_solved: True if the proof is now complete
        """
        logger.debug(f"Running tactic: {tactic}")
        result = self.dojo.run_tac(state=self.current_state, tactic=tactic)

        if isinstance(result, ProofFinished):
            logger.info("Proof completed!")
            return RunTacticResult("solved", None, True)

        elif isinstance(result, TacticState):
            self.current_state = result
            logger.debug(f"Tactic succeeded, new state: {result.pp[:50]}...")
            return RunTacticResult("ok", result.pp, False)

        elif isinstance(result, LeanError):
            logger.warning(f"Tactic failed: {result.error}")
            return RunTacticResult("error", result.error, False)

        else:
            logger.error(f"Unknown result type: {type(result)}")
            return RunTacticResult("error", f"unknown result type {result}", False)

# ===============================================
# Section 7: Artifact Types
# ===============================================

def ensure_dir(path: Path) -> None:
    """Create a directory and all parent directories if they don't exist.

    Args:
        path: The directory path to create.
    """
    path.mkdir(parents=True, exist_ok=True)


def write_attempt_record(record: AttemptRecord) -> Path:
    """Write an AttemptRecord to disk as JSON.

    Creates a directory structure based on the attempt ID and saves
    the record as 'attempt.json'.

    Args:
        record: The AttemptRecord to save.

    Returns:
        The path to the saved JSON file.
    """
    dir_path = Path(CACHE_DIR) / ATTEMPTS_DIR / record.attempt_id
    ensure_dir(dir_path)
    record_as_dict = asdict(record)
    file_path = dir_path / "attempt.json"
    with open(file_path, "w") as f:
        json.dump(record_as_dict, f, indent=2)
    logger.info(f"Attempt record saved to: {file_path}")
    return file_path

# ===============================================
# Section 8: Proof Attempt Orchestration
# ===============================================

def attempt_proof(theorem_spec: TheoremSpec, tactics: list[str]) -> AttemptRecord:
    """Attempt to prove a theorem by applying a sequence of tactics.

    This is the main entry point for proof attempts. It:
    1. Opens a Dojo session for the theorem
    2. Applies each tactic in sequence
    3. Records the result (solved, error, or not_solved)
    4. Saves the attempt to disk

    Args:
        theorem_spec: The theorem to prove.
        tactics: List of tactics to apply in order.

    Returns:
        An AttemptRecord containing the full details of the attempt.
    """
    attempt_id = stable_hash(
        theorem_spec.repo_spec.repo_url,
        theorem_spec.repo_spec.commit,
        theorem_spec.file_path,
        theorem_spec.theorem_name,
        *tactics
    )
    logger.info(f"Starting proof attempt {attempt_id[:8]}... for {theorem_spec.theorem_name}")
    
    started_ts = now_timestamp()
    status: AttemptRecordStatus = "not_solved"
    error_msg: str | None = None
    final_pp: str | None = None

    with dojo_session(theorem_spec) as (dojo, current_state):
        init_pp = current_state.pp
        tactic_runner = TacticRunner(dojo, current_state)
        
        for i, tactic in enumerate(tactics, 1):
            logger.debug(f"Applying tactic {i}/{len(tactics)}: {tactic}")
            run_tactic_result = tactic_runner.run_tactic(tactic)
            
            if run_tactic_result.status == "solved":
                status = "solved"
                logger.info(f"Proof solved after {i} tactic(s)")
                break
            elif run_tactic_result.status == "error":
                status = "error"
                error_msg = run_tactic_result.message
                logger.warning(f"Proof attempt failed at tactic {i}: {error_msg}")
                break
            else:
                final_pp = run_tactic_result.message

    completed_ts = now_timestamp()
    duration = completed_ts - started_ts
    logger.info(f"Proof attempt completed in {duration:.2f}s with status: {status}")
    
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
    # Configure logging for command-line usage
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print(f"tlq v{__version__}")
    
    try:
        config = load_config()
        logger.info("Config loaded successfully")
    except FileNotFoundError as e:
        logger.error(f"Config error: {e}")

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
    print(f"TheoremSpec: {theorem_spec}")

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
