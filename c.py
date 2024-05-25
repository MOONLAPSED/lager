from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, Any, TypeVar, Generic, Union, Optional
import struct
import json
import sys
import argparse
import types
import threading

T = TypeVar('T')

# Constants
BANNED_WORDS = ["TOKEN", "PARSER", "COMPILER", "POINTER", "FACTOR", "LEXER", "SHELL", "TERMINAL", "AI", "MODEL", "ATTRIBUTE", "DICTIONARY", "DICT"]

# Argument parser setup
args = argparse.ArgumentParser(description="Hypothesis? Use a simple, terse English statement.")
if any(word in ' '.join(args.description.split()) for word in BANNED_WORDS):
    for word in BANNED_WORDS:
        print(f"You cannot use the word {word} in your arguments.")
    sys.exit(1)

# Define a simple linked list node for the scratch arena
class Node:
    def __init__(self, size: int):
        self.data = bytearray(size)
        self.next: Optional['Node'] = None
        self.size = size
        self.used = 0

class ScratchArena:
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size
        self.head = Node(chunk_size)
        self.current = self.head

    def allocate(self, size: int) -> memoryview:
        if size > self.chunk_size:
            raise ValueError("Allocation size exceeds chunk size")

        # If there's not enough space in the current chunk, create a new one
        if self.current.used + size > self.current.size:
            new_node = Node(self.chunk_size)
            self.current.next = new_node
            self.current = new_node

        # Allocate memory from the current chunk
        start = self.current.used
        self.current.used += size
        return memoryview(self.current.data)[start:start + size]

    def reset(self):
        # Reset all chunks for reuse
        node = self.head
        while node:
            node.used = 0
            node = node.next
        self.current = self.head

# Abstract base class
class Atom(ABC):
    @abstractmethod
    def encode(self) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> None:
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def parse_expression(self, expression: str) -> Union['AtomicData', 'FormalTheory']:
        pass

    @abstractmethod
    def tautology(self, expression: Callable[..., bool]) -> bool:
        pass

# An example to serialize callable objects using identifiers
def encode_callable(func: Callable) -> int:
    lookup = {
        'reflexivity': 1,
        'symmetry': 2,
        'transitivity': 3,
        'transparency': 4,
        'top': 5,
        'bottom': 6,
        'if_else_a': 7,
        'negation': 8,
        'conjunction': 9,
        'disjunction': 10,
        'implication': 11,
        'biconditional': 12,
        'nor': 13,
        'nand': 14,
        'contrapositive': 15,
    }
    return lookup[func.__name__]

def decode_callable(value: int) -> Callable:
    reverse_lookup = {
        1: reflexivity,
        2: symmetry,
        3: transitivity,
        4: transparency,
        5: top,
        6: bottom,
        7: if_else_a,
        8: negation,
        9: conjunction,
        10: disjunction,
        11: implication,
        12: biconditional,
        13: nor,
        14: nand,
        15: contrapositive,
    }
    return reverse_lookup[value]

# Example global functions to replace lambdas
def reflexivity(x):
    return x == x

def symmetry(x, y):
    return x == y

def transitivity(x, y, z):
    return x == y and y == z and x == z

def transparency(f, x, y):
    return f(x, y) if x == y else None

def top(x, _):
    return x

def bottom(_, y):
    return y

def if_else_a(a, b):
    return a if a else b

def negation(a):
    return not a

def conjunction(a, b):
    return a and b

def disjunction(a, b):
    return a or b

def implication(a, b):
    return (not a) or b

def biconditional(a, b):
    return (a and b) or (not a and not b)

def nor(a, b):
    return not (a or b)

def nand(a, b):
    return not (a and b)

def contrapositive(a, b):
    return (not b) or (not a)


@dataclass
class AtomicData(Atom):
    data: Any
    scratch_arena: ScratchArena = field(default_factory=lambda: ScratchArena(1024))

    def encode(self) -> bytes:
        # Basic example of using struct to encode basic data
        if isinstance(self.data, int):
            return struct.pack('!i', self.data)
        elif isinstance(self.data, float):
            return struct.pack('!f', self.data)
        elif isinstance(self.data, str):
            data_bytes = self.data.encode('utf-8')
            return struct.pack(f'!I{len(data_bytes)}s', len(data_bytes), data_bytes)
        elif isinstance(self.data, dict):
            data_bytes = json.dumps(self.data).encode('utf-8')
            return struct.pack(f'!I{len(data_bytes)}s', len(data_bytes), data_bytes)
        else:
            raise ValueError("Unsupported data type for struct serialization")

    def decode(self, data: bytes) -> None:
        try:
            self.data = struct.unpack('!i', data)[0]
        except struct.error:
            try:
                self.data = struct.unpack('!f', data)[0]
            except struct.error:
                data_len = struct.unpack('!I', data[:4])[0]
                try:
                    self.data = struct.unpack(f'!{data_len}s', data[4:4 + data_len])[0].decode('utf-8')
                except UnicodeDecodeError:
                    self.data = json.loads(struct.unpack(f'!{data_len}s', data[4:4 + data_len])[0])

    def execute(self, *args, **kwargs) -> Any:
        return self.data

    def __repr__(self) -> str:
        return f"AtomicData(data={self.data})"

    def parse_expression(self, expression: str) -> Union['AtomicData', 'FormalTheory']:
        return AtomicData(data=expression)

    def tautology(self, expression: Callable[..., bool]) -> bool:
        return expression()


class ThreadSafeContextManager:
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()

class ScopeLifetimeGarden:  # rename of ThreadLocalScratchArena
    def __init__(self):
        self.local_data = threading.local()

    def get(self) -> AtomicData:
        if not hasattr(self.local_data, 'scratch'):
            self.local_data.scratch = AtomicData(data={})
        return self.local_data.scratch

    def set(self, value: AtomicData):
        self.local_data.scratch = value

@dataclass
class FormalTheory(Atom, Generic[T]):
    reflexivity: Callable[[T], bool] = reflexivity
    symmetry: Callable[[T, T], bool] = symmetry
    transitivity: Callable[[T, T, T], bool] = transitivity
    transparency: Callable[[Callable[..., T], T, T], T] = transparency
    case_base: Dict[str, Callable[..., bool]] = field(default_factory=dict)

    def __post_init__(self):
        self.case_base.update({
            '⊤': top,
            '⊥': bottom,
            'a': if_else_a,
            '¬': negation,
            '∧': conjunction,
            '∨': disjunction,
            '→': implication,
            '↔': biconditional,
            '¬∨': nor,  # NOR operation
            '¬∧': nand,  # NAND operation
            'contrapositive': contrapositive
        })

    def encode(self) -> bytes:
        # Encode attributes using struct
        attribute_values = [
            encode_callable(self.reflexivity),
            encode_callable(self.symmetry),
            encode_callable(self.transitivity),
            encode_callable(self.transparency),
        ]
        attribute_bytes = struct.pack(f'!4I', *attribute_values)

        # Encode case_base
        case_base_keys = sorted(self.case_base.keys())
        case_base_values = [encode_callable(self.case_base[k]) for k in case_base_keys]
        case_base_bytes = json.dumps(case_base_keys).encode('utf-8')
        packed_case_base = struct.pack(f"!I{len(case_base_bytes)}s{len(case_base_values)}I", len(case_base_bytes), case_base_bytes, *case_base_values)

        # Combine everything
        return attribute_bytes + packed_case_base


    def decode(self, data: bytes) -> None:
        # Extract attribute values
        attribute_values = struct.unpack('!4I', data[:16])
        self.reflexivity = decode_callable(attribute_values[0])
        self.symmetry = decode_callable(attribute_values[1])
        self.transitivity = decode_callable(attribute_values[2])
        self.transparency = decode_callable(attribute_values[3])

        # Decode the case_base
        rest = data[16:]
        case_base_len = struct.unpack('!I', rest[:4])[0]
        case_base_keys = json.loads(rest[4:4 + case_base_len])
        case_base_values = struct.unpack(f"!{len(case_base_keys)}I", rest[4 + case_base_len:])
        self.case_base = {case_base_keys[i]: decode_callable(case_base_values[i]) for i in range(len(case_base_keys))}

    def execute(self, *args, **kwargs) -> Any:
        return self.transparency(*args, **kwargs)

    def __repr__(self) -> str:
        return f"FormalTheory(reflexivity={self.reflexivity}, symmetry={self.symmetry}, transitivity={self.transitivity}, transparency={self.transparency})"

    def parse_expression(self, expression: str) -> Union['AtomicData', 'FormalTheory']:
        return self.case_base.get(expression, None)

    def tautology(self, expression: Callable[..., bool]) -> bool:
        return expression()

def main():
    # Demonstration of FormalTheory
    formal_theory = FormalTheory[int]()

    encoded_ft = formal_theory.encode()
    print("Encoded FormalTheory:", encoded_ft)

    new_formal_theory = FormalTheory[int]()
    new_formal_theory.decode(encoded_ft)
    print("Decoded FormalTheory:", new_formal_theory)

    # Execution example
    result = formal_theory.execute(lambda x, y: x + y, 1, 2)
    print("Execution Result:", result)

    # Demonstration of AtomicData
    atomic_data = AtomicData(data="Hello World")
    encoded_data = atomic_data.encode()
    print("Encoded AtomicData:", encoded_data)

    new_atomic_data = AtomicData(data=None)
    new_atomic_data.decode(encoded_data)
    print("Decoded AtomicData:", new_atomic_data)

    # Thread-safe context example
    print("Using ThreadSafeContextManager")
    with ThreadSafeContextManager():
        # Any thread-safe operations here
        pass

    # Using ScopeLifetimeGarden 
    print("Using ScopeLifetimeGarden")
    garden = ScopeLifetimeGarden()
    garden.set(AtomicData(data="Initial Data"))
    print("Garden Data:", garden.get())

    # Example usage of ScratchArena
    arena = ScratchArena(chunk_size=1024)  # Create a scratch arena with chunks of 1024 bytes

    # Allocate some memory
    data1 = arena.allocate(100)
    data2 = arena.allocate(200)

    # Fill allocated memory with some data
    data1[:] = b'a' * 100
    data2[:] = b'b' * 200

    print(bytes(data1))
    print(bytes(data2))

    # Reset the arena for reuse
    arena.reset()

if __name__ == "__main__":
    main()