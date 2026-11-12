"""
Techdim Engineering Lab - Daily Engineering & Architecture
Module: Circuit Breaker Pattern (Benchmark & Refactor #23)
Complexity: State Machine: Closed -> Open -> Half-Open
Author: Eng. Deivis Irio Mayer (Kether1) <https://www.linkedin.com/in/deivismayer>
Company: TECHDIM INOVA SIMPLES (I.S.) - ME | CNPJ: 61.933.926/0001-24
Portal: https://techdim.com.br | Contact: techdimbrasil@gmail.com
"""

"""
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

# Automated Continuous Refactoring & Benchmark Iteration 23
