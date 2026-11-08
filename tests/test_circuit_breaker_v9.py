import pytest
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
