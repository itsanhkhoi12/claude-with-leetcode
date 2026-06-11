# Sliding Window

## Video Solution

For more details about **Longest Substring Without Repeating Characters**, watch the walkthrough at [https://www.youtube.com/watch?v=wiGpQwVHdE0](https://www.youtube.com/watch?v=wiGpQwVHdE0).

## Concept

The sliding window technique maintains a **window** that satisfies a certain property (here: all characters are unique) while we scan the array/string once.  
We keep two pointers, `left` and `right`, that delimit the current window. As we expand `right`, we shrink `left` whenever the property is violated. This lets us achieve linear time instead of re‑checking every possible substring.

**Real‑world analogy**: Imagine a buffer that holds the most recent distinct songs played on a radio. When a song repeats, you drop songs from the start of the buffer until the repeat disappears, then continue adding new songs.

## When to Use It

Use sliding window when you see:
- A request for the **longest/shortest** subarray or substring that satisfies a condition.
- The condition can be checked incrementally when you add or remove one element (e.g., “no duplicates”, “sum ≤ k”, “contains all characters of T”).
- The input is ordered (array/string) and you need **contiguous** segments.

## Template

```python
def sliding_window(nums):
    left = 0
    best = 0
    state = {}          # whatever we need to track the window property

    for right in range(len(nums)):
        # expand window by including nums[right]
        update_state_add(nums[right])

        # shrink from left while window is invalid
        while not window_is_valid():
            update_state_remove(nums[left])
            left += 1

        # window [left, right] is now valid
        best = max(best, right - left + 1)

    return best
```

- `update_state_add` / `update_state_remove` modify the bookkeeping structure in O(1).
- `window_is_valid()` checks the condition (here: all counts ≤ 1).

---

## LeetCode Problem Walkthrough

### Problem: 3. Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/

### Approach 1: Brute Force

**Algorithm**
1. Enumerate every possible start index `i`.
2. For each `i`, expand an end index `j` forward, keeping a set of seen characters.
3. Stop when a duplicate appears; record the length `j‑i`.
4. Return the maximum length found.

**Implementation**

```python
def lengthOfLongestSubstring_bruteforce(s: str) -> int:
    n = len(s)
    max_len = 0

    for i in range(n):
        seen = set()
        for j in range(i, n):
            if s[j] in seen:          # duplicate -> cannot extend further
                break
            seen.add(s[j])
            max_len = max(max_len, j - i + 1)

    return max_len
```

**Complexity Analysis**
- Time complexity: O(n²) — two nested loops, each up to n.
- Space complexity: O(min(n, charset)) — the set stores at most the size of the character set.

### Approach 2: Sliding Window with HashMap

**Intuition**
When we encounter a repeated character, we can jump the left pointer directly to the position **after** its previous occurrence, because any window that starts before that would still contain the duplicate. This avoids moving `left` one step at a time.

**Algorithm**
1. Keep a dictionary `last_idx` mapping each character to its most recent index.
2. `left` marks the start of the current window with all unique characters.
3. Iterate `right` from 0 to n‑1:
   - If `s[right]` was seen inside the current window (`last_idx[s[right]] >= left`), move `left` to `last_idx[s[right]] + 1`.
   - Update `last_idx[s[right]] = right`.
   - Update answer with `right - left + 1`.

**Implementation**

```python
def lengthOfLongestSubstring_hashmap(s: str) -> int:
    last_idx = {}          # char -> most recent index
    left = 0
    max_len = 0

    for right, ch in enumerate(s):
        if ch in last_idx and last_idx[ch] >= left:
            left = last_idx[ch] + 1          # shrink window past previous dup
        last_idx[ch] = right                 # record latest position
        max_len = max(max_len, right - left + 1)

    return max_len
```

**Complexity Analysis**
- Time complexity: O(n) — each character processed once.
- Space complexity: O(min(n, charset)) — dictionary stores at most one entry per distinct character.

### Approach 3: Sliding Window with Fixed‑Size Array (ASCII)

**Intuition**
Since the input consists of ASCII characters (0‑255), we can replace the hashmap with a simple integer array of size 256, where each slot stores the last index of that character. Array access is O(1) with a smaller constant factor.

**Algorithm**
1. Create an array `last` of length 256, initialized to -1 (meaning “not seen yet”).
2. Use the same two‑pointer logic as in Approach 2, but look up/update `last[ord(ch)]` instead of a dictionary.
3. Update `left` to `max(left, last[ord(ch)] + 1)` when a duplicate is found inside the window.
4. Track the maximum window size.

**Implementation**

```python
def lengthOfLongestSubstring_array(s: str) -> int:
    last = [-1] * 256          # assuming extended ASCII
    left = 0
    max_len = 0

    for right, ch in enumerate(s):
        idx = ord(ch)
        if last[idx] >= left:          # duplicate inside window
            left = last[idx] + 1
        last[idx] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

**Complexity Analysis**
- Time complexity: O(n) — single pass.
- Space complexity: O(1) — fixed 256‑integer array, independent of input length.

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

## Dry Run

Input: `s = "abcabcbb"`

```
| Step | right | ch  | left before | last[ch] | Action (move left?) | left after | window (s[left:right+1]) | max_len |
|------|-------|-----|-------------|----------|----------------------|------------|--------------------------|---------|
| 1    | 0     | a   | 0           | -1       | no                   | 0          | a                        | 1       |
| 2    | 1     | b   | 0           | -1       | no                   | 0          | ab                       | 2       |
| 3    | 2     | c   | 0           | -1       | no                   | 0          | abc                      | 3       |
| 4    | 3     | a   | 0           | 0        | yes -> left = 0+1=1  | 1          | bca                      | 3       |
| 5    | 4     | b   | 1           | 1        | yes -> left = 1+1=2  | 2          | cab                      | 3       |
| 6    | 5     | c   | 2           | 2        | yes -> left = 2+1=3  | 3          | abc                      | 3       |
| 7    | 6     | b   | 3           | 4        | yes -> left = 4+1=5  | 5          | cb                       | 3       |
| 8    | 7     | b   | 5           | 6        | yes -> left = 6+1=7  | 7          | b                        | 3       |
```

The longest window size observed is **3**, matching the expected answer.

--- 

**Commit the lecture file** as `2025-09-26-sliding-window.md` in the `/lectures/` directory. Ensure no other lecture files are modified.