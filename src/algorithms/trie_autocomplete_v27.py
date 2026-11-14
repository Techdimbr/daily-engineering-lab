"""
Techdim Engineering Lab - Daily Engineering & Architecture
Module: Trie Prefix Tree with Autocomplete (Benchmark & Refactor #27)
Complexity: Insert: O(L) | Search Prefix: O(P + K) onde L=tamanho palavra
Author: Eng. Deivis Irio Mayer (Kether1) <https://www.linkedin.com/in/deivismayer>
Company: TECHDIM INOVA SIMPLES (I.S.) - ME | CNPJ: 61.933.926/0001-24
Portal: https://techdim.com.br | Contact: techdimbrasil@gmail.com
"""

"""
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

# Automated Continuous Refactoring & Benchmark Iteration 27
