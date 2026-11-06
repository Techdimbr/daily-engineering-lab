import time
from src.design_patterns.rate_limiter_token_bucket import TokenBucketRateLimiter

def test_rate_limiter():
    limiter = TokenBucketRateLimiter(capacity=3, refill_rate_per_sec=10.0)
    assert limiter.allow_request(1) is True
    assert limiter.allow_request(1) is True
    assert limiter.allow_request(1) is True
    assert limiter.allow_request(1) is False
    time.sleep(0.15)
    assert limiter.allow_request(1) is True
