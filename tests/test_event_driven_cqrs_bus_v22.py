from .event_driven_cqrs_bus import MessageBus

def test_cqrs_bus():
    bus = MessageBus()
    audit_log = []

    bus.register_command_handler("CreateOrder", lambda data: {"order_id": 101, "total": data["amount"]})
    bus.subscribe_event("OrderCreated", lambda evt: audit_log.append(evt["order_id"]))

    order = bus.execute_command("CreateOrder", {"amount": 250.0})
    assert order["order_id"] == 101

    bus.publish_event("OrderCreated", {"order_id": 101})
    assert audit_log == [101]
