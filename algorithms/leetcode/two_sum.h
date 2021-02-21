#include "algorithms/leetcode/cpp_standards.h"

/**
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

EXAMPLE 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Output: Because nums[0] + nums[1] == 9, we return [0, 1].

**/
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // go through numbers sequentially and at each number
        // first check if in a map if map[target - x] is present. If match:
        // return current index and value at map[target - x].
        // If no match:
        // add an entry to a map that has a key of the value `y` where `y` is `target - x = y`
        // and `x` is the value of the current number
        map<int, int> pairReference;
        int curr;
        vector<int> ans;
        for (int index = 0; index < nums.size(); ++index) {
            curr = nums[index];
            if (pairReference.count(curr) > 0) {
                // pair is found!
                ans = { pairReference[curr], index};
                break;
            } else {
                int pair = target - curr;
                pairReference.insert({pair, index});
            }
        }
        return ans; // Should *never* occur if inputs always have one and only one answer.
    }
};
