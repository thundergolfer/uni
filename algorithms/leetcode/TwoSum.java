package algorithms.leetcode;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class TwoSum {
    static class Solution {
        public int[] twoSum(int[] nums, int target) {
            Map<Integer, Integer> complements = new HashMap<>();
            for (int i = 0; i < nums.length; i++) {
                int current = nums[i];
                int compl = target - current;
                if (complements.containsKey(compl)) {
                    return new int[]{
                            complements.get(compl),
                            i,
                    };
                }
                complements.put(current, i);
            }
            return new int[]{-1, -1};
        }
    }

    public static void main(String[] args) {
        Solution solution = new TwoSum.Solution();
        int[] nums = new int[]{3, 2, 4};
        int[] result = solution.twoSum(nums, 6);
        System.out.println(Arrays.toString(result));
    }
}

