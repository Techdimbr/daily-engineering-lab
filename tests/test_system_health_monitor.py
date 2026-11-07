from src.linux_devops.system_health_monitor import LinuxSystemProbe

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
