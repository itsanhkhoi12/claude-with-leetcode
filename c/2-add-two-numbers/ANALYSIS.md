# Linked List

## Video Solution

For more details about **Add Two Numbers**, watch the walkthrough at [https://www.youtube.com/watch?v=wgFPrzTjm7s](https://www.youtube.com/watch?v=wgFPrzTjm7s)

## Concept

Adding two numbers stored in reverse‑order linked lists mirrors the way we add numbers by hand: start from the least‑significant digit (the head of each list), add the corresponding digits together with any carry from the previous step, write down the unit digit as a new node, and propagate the carry forward. Because the lists are already reversed, we never need to reverse them or backtrack—just a single forward pass.

## When to Use It

Use this pattern when you see:
- Two (or more) linked lists where each node holds a single digit.
- The digits are stored in **reverse order** (least‑significant digit first).
- The task is to perform arithmetic (addition, subtraction) that requires processing digit‑by‑digit with a carry/borrow.
- Constraints guarantee no leading zeros except the number 0 itself.

## Template

```python
# Definition for singly‑linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def add_two_numbers(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Template for adding two reverse‑order digit linked lists.
    Returns the head of the resulting linked list.
    """
    dummy = ListNode()          # placeholder to simplify head handling
    cur = dummy                 # pointer to the last node in the result
    carry = 0                   # carry from the previous digit addition

    # Traverse both lists while there are digits left or a carry remains
    while l1 or l2 or carry:
        # Extract current digits (0 if the list is exhausted)
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0

        # Compute sum and new carry
        total = v1 + v2 + carry
        carry = total // 10
        digit = total % 10

        # Append the digit as a new node
        cur.next = ListNode(digit)
        cur = cur.next

        # Advance input pointers
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    return dummy.next          # skip the dummy node and return real head
```

---

## LeetCode Problem Walkthrough

### Problem: 2. Add Two Numbers  
https://leetcode.com/problems/add-two-numbers/

### Approach 1: Brute Force – Convert to Arrays (or Numbers)

**Algorithm**  
1. Traverse each linked list and store its node values in a Python list (`stack1`, `stack2`).  
   Because the lists are already in reverse order, the list directly holds the digits from least‑ to most‑significant.  
2. Pad the shorter list with zeros so both have equal length.  
3. Iterate from index 0 to the end, adding corresponding digits together with a carry, storing each result digit in a new list `res`.  
4. After the loop, if a carry remains, append it.  
5. Build a new linked list from `res` and return its head.

**Implementation**

```python
def addTwoNumbers_bruteforce(l1: ListNode, l2: ListNode) -> ListNode:
    # 1. Extract digits
    stack1, stack2 = [], []
    while l1:
        stack1.append(l1.val)
        l1 = l1.next
    while l2:
        stack2.append(l2.val)
        l2 = l2.next

    # 2. Ensure same length (least‑significant first, so pad at the end)
    if len(stack1) < len(stack2):
        stack1 += [0] * (len(stack2) - len(stack1))
    else:
        stack2 += [0] * (len(stack1) - len(stack2))

    # 3. Add digitwise with carry
    carry = 0
    res = []
    for d1, d2 in zip(stack1, stack2):
        total = d1 + d2 + carry
        carry = total // 10
        res.append(total % 10)
    if carry:
        res.append(carry)

    # 4. Build result linked list
    dummy = ListNode()
    cur = dummy
    for d in res:
        cur.next = ListNode(d)
        cur = cur.next
    return dummy.next
```

**Complexity Analysis**

- Time complexity: **O(max(n, m))** – we traverse each list once to fill the arrays and once more to add them.  
- Space complexity: **O(max(n, m))** – the two stacks and the result list each hold up to the length of the longer input.

---

### Approach 2: Optimal – One‑Pass with Carry (Dummy Head)

**Intuition**  
Instead of first copying the digits into auxiliary arrays, we can add them on the fly while walking the lists. The only state we need to keep between steps is the carry from the previous addition. A dummy head node simplifies handling the result list’s head, especially when the result is longer than either input (e.g., `999 + 1`).

**Algorithm**  
1. Initialise a dummy node (`dummy`) and a pointer (`cur`) to build the answer. Set `carry = 0`.  
2. While at least one list still has nodes **or** `carry` is non‑zero:  
   a. Take the current node’s value from each list (0 if the list is exhausted).  
   b. Compute `total = v1 + v2 + carry`.  
   c. Update `carry = total // 10` and the digit to store as `total % 10`.  
   d. Append a new node with that digit to `cur.next` and advance `cur`.  
   e. Advance `l1` and `l2` if they are not None.  
3. Return `dummy.next` (the real head of the result list).

**Implementation**

```python
def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode()          # placeholder start node
    cur = dummy
    carry = 0

    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0

        total = v1 + v2 + carry
        carry = total // 10
        digit = total % 10

        cur.next = ListNode(digit)
        cur = cur.next

        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    return dummy.next
```

**Complexity Analysis**

- Time complexity: **O(max(n, m))** – each list is visited at most once; the loop runs until both lists are exhausted and no carry remains.  
- Space complexity: **O(1)** – only a few pointers and integer variables are used; the output list does not count as extra space.

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

We dry‑run the optimal algorithm on the classic example:

**Input:** `l1 = [2,4,3]`, `l2 = [5,6,4]` (representing 342 + 465)

| Step | l1.val | l2.val | carry-in | total | digit (total%10) | carry-out | Action                              |
|------|--------|--------|----------|-------|------------------|-----------|-------------------------------------|
| 1    | 2      | 5      | 0        | 7     | 7                | 0         | Append 7 → result: [7]              |
| 2    | 4      | 6      | 0        | 10    | 0                | 1         | Append 0 → result: [7,0]            |
| 3    | 3      | 4      | 1        | 8     | 8                | 0         | Append 8 → result: [7,0,8]          |
| 4    | None   | None   | 0        | –     | –                | –         | Both lists exhausted & carry=0 → stop |

The constructed linked list is `[7,0,8]`, which matches the expected output.

---