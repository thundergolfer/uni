#include "algorithms/leetcode/add_binary.h"

#include "gtest/gtest.h"

TEST(AddBinaryTest, Test1) {
  Solution solution;
  EXPECT_EQ(solution.addBinary("0", "0"), "0");
}

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
