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
from typing import NewType
from json import dumps
from dataclasses import dataclass


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
    max_nodes: int
    max_depth: int
    timeout_s: float

if __name__ == "__main__":
    print(f"tlq0 v{__version__}")
