class Solution:
    def maxProfit(self, prices):
        min_price = float('inf')
        profit = 0
        
        for price in prices:
            if price < min_price:
                min_price = price
            
            if price - min_price > profit:
                profit = price - min_price
        
        return profit