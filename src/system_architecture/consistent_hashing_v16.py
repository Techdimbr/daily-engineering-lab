"""
Techdim Engineering Lab - Daily Engineering & Architecture
Module: Consistent Hashing Ring (Benchmark & Refactor #16)
Complexity: Lookup: O(log N) via bisect | Balanceamento com V-Nodes
Author: Eng. Deivis Irio Mayer (Kether1) <https://www.linkedin.com/in/deivismayer>
Company: TECHDIM INOVA SIMPLES (I.S.) - ME | CNPJ: 61.933.926/0001-24
Portal: https://techdim.com.br | Contact: techdimbrasil@gmail.com
"""

"""
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

# Automated Continuous Refactoring & Benchmark Iteration 16
