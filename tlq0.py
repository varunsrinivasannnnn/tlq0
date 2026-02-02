#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tlq0 (The Last Question) - Mark 0

A self-learning theorem prover that learns from scratch through
compression-driven self-play.

Core thesis: Intelligence = compression of predictive structure over state transitions.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 0: IMPORTS  + GLOBAL VARIABLES + PROJECT META DATA
# ═══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import hashlib
import platform
import random
import sys
from typing import NewType
from json import dumps
from dataclasses import dataclass, field
from pathlib import Path
import time

__version__ = "0.1.0"
__author__ = "Varun Srinivasan"

DEFAULT_RUNS_DIR = "runs"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: TYPED IDS + HASHING UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

RunId = NewType("RunId", str)
TheoremId = NewType("TheoremId", str)
StateId = NewType("StateId", str)

def stable_hash(data: str) -> str:
    """Returns SHA-256 hex digest of the input string"""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def stable_json_dumps(obj: object) -> str:
    """Returns stable JSON string dump for any object """
    return dumps(obj, sort_keys=True, separators=(",", ":"))

def hash_object(obj: object) -> str:
    """Hash any JSONS serializable object deterministically"""
    return stable_hash(stable_json_dumps(obj))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: ERROR TAXONOMY + PRECONDITIONS
# ═══════════════════════════════════════════════════════════════════════════════

class TLQ0Error(Exception):
    """Base exception for all tlq0 errors"""
    pass

class ConfigError(TLQ0Error):
    """Raised when configuration is invalid."""
    pass

class ValidationError(TLQ0Error):
    """Raised when data validation fails."""
    pass

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: CONFIG SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class SearchConfig:
    """Snapshot of the search configuration."""
    max_nodes: int = 1000
    max_depth: int = 50
    timeout_s: float = 60.0

@dataclass(frozen=True)
class TrainConfig:
    """Snapshot of the training configuration."""
    seed: int = 0
    device: str = "cpu"

@dataclass(frozen=True)
class TLQ0Config:
    """Snapshot of the current tlq configuration."""
    schema_version : int = 1
    search_config : SearchConfig = field(default_factory=SearchConfig)
    train_config : TrainConfig = field(default_factory=TrainConfig)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: RUN DIRECTORY + ATOMIC WRITES + ENVIRONMENT SNAPSHOT
# ═══════════════════════════════════════════════════════════════════════════════

def timestamp_now() -> float:
    """Returns the current UNIX"""
    return time.time()

def create_run_dir(seed: int) -> Path:
    """Creates the run directory"""
    current_ts = timestamp_now()
    p = Path(DEFAULT_RUNS_DIR) / f"run_{current_ts}_seed_{seed}"
    p.mkdir(parents=True, exist_ok=True)
    (p / "artifacts").mkdir(parents=True, exist_ok=True)
    return p

def atomic_writing(path: Path, content: str):
    """Ensures atomic saving of the files"""
    (path.parent / (path.name + ".tmp")).write_text(content)
    (path.parent / (path.name + ".tmp")).replace(path)

def get_env_snapshot() -> dict:
    """Returns a dictionary capturing the current state of the environment."""
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "tlq0_version": __version__,
        "timestamp": timestamp_now()}

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: RNG DISCIPLINE + DETERMINISM LAYER
# ═══════════════════════════════════════════════════════════════════════════════

def seed_everything(seed: int):
    """Unifying the seed for all RNG operations for every run."""
    return random.seed(seed)


class RNG:
    def __init__(self, seed: int):
        self._rng = random.Random(seed)

    def random(self):
        return self._rng.random()

    def randint(self, a: int, b: int):
        return self._rng.randint(a, b)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: STRUCTURED EVENT LOGGING
# ═══════════════════════════════════════════════════════════════════════════════

class EventLogger:
    def __init__(self, path: Path):
        self.path = path

    def log(self, kind: str, payload: dict):
        with self.path.open("a") as f:
            f.write(stable_json_dumps({
                "ts": timestamp_now(),
                "kind": kind,
                "payload": payload}) + "\n")



if __name__ == "__main__":
    print(f"tlq0 v{__version__}")
