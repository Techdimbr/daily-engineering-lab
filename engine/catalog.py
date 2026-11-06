"""
Techdim Kether Engineering Catalog
Repositório de desafios técnicos, algoritmos, padrões de projeto e arquitetura de software
usados pela automação para gerar commits de valor real e comprovável.
"""

from typing import List, Dict, Any

MODULES: List[Dict[str, Any]] = [
    {
        "category": "algorithms",
        "slug": "lru_cache",
        "title": "Least Recently Used (LRU) Cache",
        "complexity": "Time: O(1) get/put | Space: O(capacity)",
        "code": '''"""
Least Recently Used (LRU) Cache Implementation
Utiliza Hash Map + Doubly Linked List para garantir O(1) em get() e put().
"""

class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: Node):
        """Adiciona nó logo após o head (mais recentemente usado)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        """Remove nó existente da lista encadeada."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node):
        """Move nó acessado para o início da lista."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """Remove o nó menos recentemente usado."""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if not node:
            return -1
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)
        if not node:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)
            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]
        else:
            node.value = value
            self._move_to_head(node)
''',
        "test": '''import pytest
from .lru_cache import LRUCache

def test_lru_operations():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts key 2
    assert cache.get(2) == -1
    cache.put(4, 4)  # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
''',
        "description": "Implementação clássica de cache LRU de alta performance para sistemas de baixa latência."
    },
    {
        "category": "algorithms",
        "slug": "binary_search_rotated",
        "title": "Search in Rotated Sorted Array",
        "complexity": "Time: O(log n) | Space: O(1)",
        "code": '''"""
Search in Rotated Sorted Array
Busca binária modificada para localizar elementos em vetores ordenados que sofreram rotação.
"""

from typing import List

def search_rotated_array(nums: List[int], target: int) -> int:
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        # Metade esquerda está ordenada
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Metade direita está ordenada
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
''',
        "test": '''from .binary_search_rotated import search_rotated_array

def test_search_rotated():
    nums = [4, 5, 6, 7, 0, 1, 2]
    assert search_rotated_array(nums, 0) == 4
    assert search_rotated_array(nums, 3) == -1
    assert search_rotated_array([1], 0) == -1
    assert search_rotated_array([1], 1) == 0
''',
        "description": "Busca binária modificada resiliente a deslocamentos cíclicos."
    },
    {
        "category": "design_patterns",
        "slug": "circuit_breaker",
        "title": "Circuit Breaker Pattern",
        "complexity": "State Machine: Closed -> Open -> Half-Open",
        "code": '''"""
Circuit Breaker Pattern para Resiliência em Microsserviços
Previne falhas em cascata interrompendo chamadas a serviços instáveis.
"""

import time
from typing import Callable, Any

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time_secs: float = 5.0):
        self.failure_threshold = failure_threshold
        self.recovery_time_secs = recovery_time_secs
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_state_change = time.time()

    def call(self, func: Callable, *args, **kwargs) -> Any:
        current_time = time.time()

        if self.state == "OPEN":
            if current_time - self.last_state_change >= self.recovery_time_secs:
                self.state = "HALF_OPEN"
                self.last_state_change = current_time
            else:
                raise CircuitBreakerOpenException("Circuit is open. Request blocked.")

        try:
            result = func(*args, **kwargs)
            self._handle_success()
            return result
        except Exception as e:
            self._handle_failure()
            raise e

    def _handle_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def _handle_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_state_change = time.time()
''',
        "test": '''import pytest
import time
from .circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

def failing_call():
    raise RuntimeError("Remote call failed")

def test_circuit_breaker_flow():
    cb = CircuitBreaker(failure_threshold=2, recovery_time_secs=0.1)
    
    # Falhas até abrir
    with pytest.raises(RuntimeError):
        cb.call(failing_call)
    assert cb.state == "CLOSED"

    with pytest.raises(RuntimeError):
        cb.call(failing_call)
    assert cb.state == "OPEN"

    # Imediatamente bloqueia
    with pytest.raises(CircuitBreakerOpenException):
        cb.call(lambda: "ok")

    # Espera recuperação
    time.sleep(0.15)
    # Sucesso no HALF_OPEN restaura para CLOSED
    res = cb.call(lambda: "recovered")
    assert res == "recovered"
    assert cb.state == "CLOSED"
''',
        "description": "Padrão de estabilidade arquitetural para ambientes distribuídos e APIs críticas."
    },
    {
        "category": "design_patterns",
        "slug": "rate_limiter_token_bucket",
        "title": "Token Bucket Rate Limiter",
        "complexity": "Time: O(1) | Space: O(1)",
        "code": '''"""
Token Bucket Rate Limiter
Algoritmo de limitação de tráfego que suporta rajadas (bursts) controladas.
"""

import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        if new_tokens > 0:
            self.tokens = min(float(self.capacity), self.tokens + new_tokens)
            self.last_refill = now

    def allow_request(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
''',
        "test": '''import time
from .rate_limiter_token_bucket import TokenBucketRateLimiter

def test_rate_limiter():
    limiter = TokenBucketRateLimiter(capacity=3, refill_rate_per_sec=10.0)
    assert limiter.allow_request(1) is True
    assert limiter.allow_request(1) is True
    assert limiter.allow_request(1) is True
    assert limiter.allow_request(1) is False
    time.sleep(0.15)
    assert limiter.allow_request(1) is True
''',
        "description": "Controle de taxa e proteção contra DoS em gateways de API e microserviços."
    },
    {
        "category": "system_architecture",
        "slug": "consistent_hashing",
        "title": "Consistent Hashing Ring",
        "complexity": "Lookup: O(log N) via bisect | Balanceamento com V-Nodes",
        "code": '''"""
Consistent Hashing com Nós Virtuais (Virtual Nodes)
Essencial para balanceamento em bancos de dados distribuídos (DynamoDB, Cassandra, Memcached).
"""

import hashlib
import bisect
from typing import List, Optional

class ConsistentHashRing:
    def __init__(self, replicas: int = 100):
        self.replicas = replicas
        self.ring = []       # hashes ordenados
        self.node_map = {}   # hash -> nó físico

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        for i in range(self.replicas):
            vnode_key = f"{node}#vnode_{i}"
            h = self._hash(vnode_key)
            bisect.insort(self.ring, h)
            self.node_map[h] = node

    def remove_node(self, node: str) -> None:
        for i in range(self.replicas):
            vnode_key = f"{node}#vnode_{i}"
            h = self._hash(vnode_key)
            idx = bisect.bisect_left(self.ring, h)
            if idx < len(self.ring) and self.ring[idx] == h:
                del self.ring[idx]
                del self.node_map[h]

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.node_map[self.ring[idx]]
''',
        "test": '''from .consistent_hashing import ConsistentHashRing

def test_consistent_hashing():
    ring = ConsistentHashRing(replicas=50)
    ring.add_node("server-node-1")
    ring.add_node("server-node-2")
    ring.add_node("server-node-3")

    node_a = ring.get_node("user_session_9823")
    node_b = ring.get_node("user_session_4102")
    assert node_a in ["server-node-1", "server-node-2", "server-node-3"]
    assert node_b in ["server-node-1", "server-node-2", "server-node-3"]

    # Removendo um nó
    ring.remove_node("server-node-2")
    node_after = ring.get_node("user_session_9823")
    assert node_after in ["server-node-1", "server-node-3"]
''',
        "description": "Algoritmo de particionamento e roteamento distribuído de alta disponibilidade."
    },
    {
        "category": "algorithms",
        "slug": "trie_autocomplete",
        "title": "Trie Prefix Tree with Autocomplete",
        "complexity": "Insert: O(L) | Search Prefix: O(P + K) onde L=tamanho palavra",
        "code": '''"""
Trie (Árvore de Prefixos) com Sistema de Autocomplete
Estrutura otimizada para motores de busca e corretores gramaticais.
"""

from typing import List, Dict

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def autocomplete(self, prefix: str, max_results: int = 5) -> List[str]:
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        self._dfs(node, prefix.lower(), results, max_results)
        return results

    def _dfs(self, node: TrieNode, current_word: str, results: List[str], max_results: int):
        if len(results) >= max_results:
            return
        if node.is_end_of_word:
            results.append(current_word)
        for char, child_node in sorted(node.children.items()):
            self._dfs(child_node, current_word + char, results, max_results)
''',
        "test": '''from .trie_autocomplete import Trie

def test_trie():
    trie = Trie()
    for w in ["docker", "dock", "download", "database", "debian"]:
        trie.insert(w)

    assert trie.search("docker") is True
    assert trie.search("docke") is False
    assert trie.starts_with("deb") is True

    auto = trie.autocomplete("do")
    assert "dock" in auto
    assert "docker" in auto
    assert "download" in auto
''',
        "description": "Mecanismo ágil de busca por prefixo e auto-completar indexado em árvore."
    },
    {
        "category": "linux_devops",
        "slug": "system_health_monitor",
        "title": "Linux System Health & Memory Telemetry",
        "complexity": "Lightweight /proc parser | No external daemon dependencies",
        "code": '''"""
Linux System Health & Memory Telemetry Probe
Parser nativo de /proc/meminfo e /proc/loadavg para auditoria de desempenho de servidores.
"""

import os
from typing import Dict, Any

class LinuxSystemProbe:
    @staticmethod
    def get_load_average() -> Dict[str, float]:
        load1, load5, load15 = os.getloadavg()
        return {
            "load_1m": round(load1, 2),
            "load_5m": round(load5, 2),
            "load_15m": round(load15, 2)
        }

    @staticmethod
    def parse_proc_meminfo(content: str) -> Dict[str, int]:
        mem_data = {}
        for line in content.splitlines():
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                val_parts = parts[1].strip().split()
                if val_parts:
                    try:
                        mem_data[key] = int(val_parts[0])
                    except ValueError:
                        pass
        return mem_data

    @classmethod
    def calculate_memory_usage(cls, meminfo: Dict[str, int]) -> Dict[str, Any]:
        total = meminfo.get("MemTotal", 1)
        free = meminfo.get("MemFree", 0)
        available = meminfo.get("MemAvailable", free)
        used = total - available
        usage_pct = (used / total) * 100.0

        return {
            "total_mb": round(total / 1024, 2),
            "available_mb": round(available / 1024, 2),
            "used_mb": round(used / 1024, 2),
            "usage_percent": round(usage_pct, 2)
        }
''',
        "test": '''from .system_health_monitor import LinuxSystemProbe

SAMPLE_MEMINFO = """MemTotal:       16301248 kB
MemFree:         4123840 kB
MemAvailable:   11200420 kB
Buffers:          340120 kB
Cached:          7200500 kB
"""

def test_meminfo_parser():
    parsed = LinuxSystemProbe.parse_proc_meminfo(SAMPLE_MEMINFO)
    assert parsed["MemTotal"] == 16301248
    assert parsed["MemAvailable"] == 11200420

    metrics = LinuxSystemProbe.calculate_memory_usage(parsed)
    assert metrics["total_mb"] == 15919.19
    assert metrics["usage_percent"] < 50.0
''',
        "description": "Telemetria de sistema operacional sem dependências externas para containers e host."
    },
    {
        "category": "system_architecture",
        "slug": "event_driven_cqrs_bus",
        "title": "CQRS Event-Driven In-Memory Bus",
        "complexity": "Pub/Sub O(1) registration | O(M) dispatch handlers",
        "code": '''"""
Event-Driven CQRS (Command Query Responsibility Segregation) Message Bus
Desacopla comandos de mutação de consultas através de barramento assíncrono.
"""

from typing import Dict, List, Callable, Any

class MessageBus:
    def __init__(self):
        self._command_handlers: Dict[str, Callable] = {}
        self._event_subscribers: Dict[str, List[Callable]] = {}

    def register_command_handler(self, command_name: str, handler: Callable):
        if command_name in self._command_handlers:
            raise ValueError(f"Handler already registered for command {command_name}")
        self._command_handlers[command_name] = handler

    def subscribe_event(self, event_name: str, subscriber: Callable):
        if event_name not in self._event_subscribers:
            self._event_subscribers[event_name] = []
        self._event_subscribers[event_name].append(subscriber)

    def execute_command(self, command_name: str, payload: Any) -> Any:
        handler = self._command_handlers.get(command_name)
        if not handler:
            raise LookupError(f"No handler registered for {command_name}")
        return handler(payload)

    def publish_event(self, event_name: str, payload: Any) -> None:
        subscribers = self._event_subscribers.get(event_name, [])
        for sub in subscribers:
            sub(payload)
''',
        "test": '''from .event_driven_cqrs_bus import MessageBus

def test_cqrs_bus():
    bus = MessageBus()
    audit_log = []

    bus.register_command_handler("CreateOrder", lambda data: {"order_id": 101, "total": data["amount"]})
    bus.subscribe_event("OrderCreated", lambda evt: audit_log.append(evt["order_id"]))

    order = bus.execute_command("CreateOrder", {"amount": 250.0})
    assert order["order_id"] == 101

    bus.publish_event("OrderCreated", {"order_id": 101})
    assert audit_log == [101]
''',
        "description": "Arquitetura limpa para separação estrita de leitura e escrita em sistemas corporativos."
    }
]
