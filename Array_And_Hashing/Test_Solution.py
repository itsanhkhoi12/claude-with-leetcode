import pytest
from Solution import Solution

sol = Solution()

# Test cases as tuples: (input, expected_output)
test_cases = [
    ([7,1,5,3,6,4], 5),
    ([7,6,4,3,1], 0),
    ([1,2,3,4,5], 4),
    ([], 0),
    ([2], 0)
]

@pytest.mark.parametrize("prices,expected", test_cases)
def test_max_profit(prices, expected):
    assert sol.maxProfit(prices) == expected