import collections
import matplotlib.pyplot as plt

# Taken from https://github.com/joelgrus/data-science-from-scratch/blob/master/scratch/statistics.py#L2
# fmt: off
num_friends = [100.0,49,41,40,25,21,21,19,19,18,18,16,15,15,15,15,14,14,13,13,13,13,12,12,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# fmt: on

friend_counts = collections.Counter(num_friends)
xs = range(101)  # Largest value in num_friends is 100
ys = [friend_counts[x] for x in xs]  # height is just num of friends
plt.bar(xs, ys)
plt.axis([0, 101, 0, 25])
plt.title("Histogram of friend counts")
plt.xlabel("# of friends")
plt.ylabel("# of people having friend count x")
plt.show()

num_points = len(num_friends)  # 204
largest_value = max(num_friends)  # 100
smallest_value = max(num_friends)  # 1

sorted_values = sorted(num_friends)
smallest_value = sorted_values[0]  # 1

second_smallest_value = sorted_values[1]  # 1
second_largest_value = sorted_values[-2]  # 49

# CENTRAL TENDENCIES

# TODO(Jonathon): Continue on from page 65
