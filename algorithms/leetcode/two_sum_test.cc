#include "algorithms/leetcode/two_sum.h"

#include "gtest/gtest.h"

TEST(TwoSumTest, Test1) {
  Solution solution;

  vector<int> nums = {2, 7, 0, 9};
  vector<int> expected = {0, 1};

  EXPECT_EQ(solution.twoSum(nums, 9), expected);
}

TEST(TwoSumTest, Test2) {
  Solution solution;

  vector<int> nums = {3, 2, 4};
  vector<int> expected = {1, 2};

  EXPECT_EQ(solution.twoSum(nums, 6), expected);
}


int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
