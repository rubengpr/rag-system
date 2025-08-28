"""
Intents Package

This package contains modular intent detection classes organized by category.
Each module handles a specific type of user intent.
"""

from .base_intent import BaseIntent
from .basic_intents import BasicIntents
from .document_intents import DocumentIntents
from .system_intents import SystemIntents
from .specialized_intents import SpecializedIntents
from .error_intents import ErrorIntents

__all__ = [
    'BaseIntent',
    'BasicIntents', 
    'DocumentIntents',
    'SystemIntents',
    'SpecializedIntents',
    'ErrorIntents'
]
