"""
Techdim Engineering Lab - Daily Engineering & Architecture
Module: CQRS Event-Driven In-Memory Bus (Benchmark & Refactor #22)
Complexity: Pub/Sub O(1) registration | O(M) dispatch handlers
Author: Eng. Deivis Irio Mayer (Kether1) <https://www.linkedin.com/in/deivismayer>
Company: TECHDIM INOVA SIMPLES (I.S.) - ME | CNPJ: 61.933.926/0001-24
Portal: https://techdim.com.br | Contact: techdimbrasil@gmail.com
"""

"""
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

# Automated Continuous Refactoring & Benchmark Iteration 22
