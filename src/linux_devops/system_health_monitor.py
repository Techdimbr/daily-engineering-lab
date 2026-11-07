"""
Techdim Engineering Lab - Daily Engineering & Architecture
Module: Linux System Health & Memory Telemetry
Complexity: Lightweight /proc parser | No external daemon dependencies
Author: Eng. Deivis Irio Mayer (Kether1) <https://www.linkedin.com/in/deivismayer>
Company: TECHDIM INOVA SIMPLES (I.S.) - ME | CNPJ: 61.933.926/0001-24
Portal: https://techdim.com.br | Contact: techdimbrasil@gmail.com
"""

"""
Linux System Health & Memory Telemetry Probe
Parser nativo de /proc/meminfo e /proc/loadavg para auditoria de desempenho de servidores.
"""

import os
from typing import Dict, Any

class LinuxSystemProbe:
    @staticmethod
    def get_load_average() -> Dict[str, float]:
        load1, load5, load15 = os.getloadavg()
        return {
            "load_1m": round(load1, 2),
            "load_5m": round(load5, 2),
            "load_15m": round(load15, 2)
        }

    @staticmethod
    def parse_proc_meminfo(content: str) -> Dict[str, int]:
        mem_data = {}
        for line in content.splitlines():
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                val_parts = parts[1].strip().split()
                if val_parts:
                    try:
                        mem_data[key] = int(val_parts[0])
                    except ValueError:
                        pass
        return mem_data

    @classmethod
    def calculate_memory_usage(cls, meminfo: Dict[str, int]) -> Dict[str, Any]:
        total = meminfo.get("MemTotal", 1)
        free = meminfo.get("MemFree", 0)
        available = meminfo.get("MemAvailable", free)
        used = total - available
        usage_pct = (used / total) * 100.0

        return {
            "total_mb": round(total / 1024, 2),
            "available_mb": round(available / 1024, 2),
            "used_mb": round(used / 1024, 2),
            "usage_percent": round(usage_pct, 2)
        }
