

from functools import lru_cache

def brute_force_missing_coin_sum(coins):
    """
    Brute force approach - checks each sum from 1 onwards
    """
    @lru_cache
    def can_make_sum(target, coins):
        if target == 0:
            return True
        if not coins or target < 0:
            return False
        
        return (can_make_sum(target - coins[0], coins[1:]) or
                can_make_sum(target, coins[1:])
               )
    sum_val = 1
    while True:
        if not can_make_sum(sum_val, tuple(coins)):
            return sum_val
        sum_val += 1


def top_down_dp_missing_coin_sum(coins):
    """
    Top-down dynamic programming approach for finding the smallest positive integer
    that cannot be formed as a sum of coins.
    
    Approach:
    1. Sort coins to process smaller coins first
    2. Use DP to track which sums can be formed
    3. Find the first sum that cannot be formed
    
    Time Complexity: O(n * max_sum) where max_sum is the answer
    Space Complexity: O(n * max_sum) for memoization
    """
    if not coins:
        return 1
    
    # Sort coins to process smaller coins first
    coins = sorted(coins)
    
    @lru_cache(maxsize=None)
    def can_make_sum(target, coin_index):
        """
        Check if we can make 'target' sum using coins from index 'coin_index' onwards
        
        Args:
            target: The sum we want to make
            coin_index: Current index in the coins array
            
        Returns:
            True if target can be made, False otherwise
        """
        # Base case: target is 0, we can always make 0 (by not using any coins)
        if target == 0:
            return True
        
        # Base case: no more coins or target is negative
        if coin_index >= len(coins) or target < 0:
            return False
        
        current_coin = coins[coin_index]
        
        # Option 1: Use the current coin (if target >= current_coin)
        # Option 2: Skip the current coin
        use_coin = False
        if target >= current_coin:
            use_coin = can_make_sum(target - current_coin, coin_index + 1)
        
        skip_coin = can_make_sum(target, coin_index + 1)
        
        return use_coin or skip_coin
    
    # Find the smallest positive integer that cannot be formed
    sum_val = 1
    while True:
        if not can_make_sum(sum_val, 0):
            return sum_val
        sum_val += 1


def optimized_top_down_dp(coins):
    """
    Optimized top-down DP approach using a different strategy.
    
    Instead of checking each sum individually, we can use the fact that
    if we can make sums 1, 2, ..., k, then we can make k+1 if we have a coin <= k+1.
    
    Time Complexity: O(n * log n) for sorting + O(n) for processing
    Space Complexity: O(n) for the coins array
    """
    if not coins:
        return 1
    
    # Sort coins in ascending order
    coins = sorted(coins)
    
    # The smallest sum we cannot make yet
    smallest_unreachable = 1
    
    for coin in coins:
        # If current coin is greater than smallest_unreachable,
        # then we cannot make smallest_unreachable
        if coin > smallest_unreachable:
            break
        
        # If we can make sums 1, 2, ..., smallest_unreachable-1,
        # and we have a coin of value 'coin', then we can make
        # smallest_unreachable, smallest_unreachable+1, ..., smallest_unreachable+coin-1
        smallest_unreachable += coin
    
    return smallest_unreachable


# Test cases
def test_solutions():
    """Test all solutions with various test cases"""
    
    test_cases = [
        ([2, 9, 1, 2, 7], 6),  # Given example
        ([1, 2, 3], 7),         # Can make 1,2,3,4,5,6 but not 7
        ([1, 1, 1], 4),         # Can make 1,2,3 but not 4
        ([2, 3, 4], 1),         # Cannot make 1
        ([1], 2),               # Can make 1 but not 2
        ([2], 1),               # Cannot make 1
        ([], 1),                # Empty array
        ([1, 2, 4, 8, 16], 32), # Powers of 2
    ]
    
    print("Testing Missing Coins Sum Solutions:")
    print("=" * 50)
    
    for coins, expected in test_cases:
        print(f"\nCoins: {coins}")
        print(f"Expected: {expected}")
        
        # Test brute force
        try:
            brute_result = brute_force_missing_coin_sum(coins)
            print(f"Brute Force: {brute_result}")
        except Exception as e:
            print(f"Brute Force: Error - {e}")
        
        # Test top-down DP
        try:
            dp_result = top_down_dp_missing_coin_sum(coins)
            print(f"Top-down DP: {dp_result}")
        except Exception as e:
            print(f"Top-down DP: Error - {e}")
        
        # Test optimized solution
        try:
            opt_result = optimized_top_down_dp(coins)
            print(f"Optimized: {opt_result}")
        except Exception as e:
            print(f"Optimized: Error - {e}")
        
        print(f"Correct: {expected == dp_result == opt_result}")


if __name__ == "__main__":
    # Original test case
    coins = [2, 9, 1, 2, 7]
    print(f"Original coins: {coins}")
    print(f"Brute force result: {brute_force_missing_coin_sum(coins)}")
    print(f"Top-down DP result: {top_down_dp_missing_coin_sum(coins)}")
    print(f"Optimized result: {optimized_top_down_dp(coins)}")
    
    print("\n" + "="*60)
    test_solutions()