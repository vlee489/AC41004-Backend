"""Customer DB Model"""
from dataclasses import dataclass

from .base import Base


@dataclass
class Customer(Base):
    pass
