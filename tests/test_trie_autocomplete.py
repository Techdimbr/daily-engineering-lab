from src.algorithms.trie_autocomplete import Trie

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
