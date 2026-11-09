"""
Techdim Engineering Lab - Daily Engineering & Architecture
Module: Search in Rotated Sorted Array (Benchmark & Refactor #13)
Complexity: Time: O(log n) | Space: O(1)
Author: Eng. Deivis Irio Mayer (Kether1) <https://www.linkedin.com/in/deivismayer>
Company: TECHDIM INOVA SIMPLES (I.S.) - ME | CNPJ: 61.933.926/0001-24
Portal: https://techdim.com.br | Contact: techdimbrasil@gmail.com
"""

"""
Search in Rotated Sorted Array
Busca binária modificada para localizar elementos em vetores ordenados que sofreram rotação.
"""

from typing import List

def search_rotated_array(nums: List[int], target: int) -> int:
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        # Metade esquerda está ordenada
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Metade direita está ordenada
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1

# Automated Continuous Refactoring & Benchmark Iteration 13
