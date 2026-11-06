from src.system_architecture.consistent_hashing import ConsistentHashRing

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
