'''
347. Top K Frequent Elements
Medium
Topics
Given an integer array nums and an integer k, 
return the k most frequent elements. You may return the answer in any order.

 

Example 1:

Input: nums = [1,1,1,2,2,3], k = 2

Output: [1,2]

Example 2:

Input: nums = [1], k = 1

Output: [1]

Example 3:

Input: nums = [1,2,1,2,1,2,3,1,3,2], k = 2

Output: [1,2]


Constraints:

1 <= nums.length <= 105
-104 <= nums[i] <= 104
k is in the range [1, the number of unique elements in the array].
It is guaranteed that the answer is unique.
 

Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
'''

# 1. Using bucket sort with defaultdict
from collections import Counter, defaultdict
from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Count frequency of each number
        count = defaultdict(int)
        for num in nums:
            count[num] += 1

        # Create buckets to group numbers by their frequency
        bucket = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            bucket[freq].append(num)

        # Create a new list to store top k frequent elements
        # Stop when we have k elements
        result = []
        for freq in range(len(nums) - 1, -1, -1):
            for num in bucket[freq]:
                result.append(num)
                if len(result) == k:
                    return result
                
# 2. Using bucket sort with Counter
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)

        bucket = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            bucket[freq].append(num)

        result = []
        for freq in range(len(nums) - 1, -1, -1):
            for num in bucket[freq]:
                result.append(num)
                if len(result) == k:
                    return result