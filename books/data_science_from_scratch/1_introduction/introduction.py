"""
Introduction / Finding Key Connectors

... In particular, he wants you to identify who the "key connectors" are among data scientists.
To this end, he gives you a dump of the entire DataSciencester network.
(In real life, people don't typically hand you thje data you need. Chapter 9 is devoted to getting data.)

What does this data dump look like? It consists of a list of users,each represented by a
`dict` that contains that user's `id` (which is a number) and `name` (which, in one of the great cosmic
coincidences, rhymes with the user's `id`):
"""
import collections

from typing import Dict, Union

users = [
    {"id": 0, "name": "Hero"},
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"},
]

friendship_pairs = [
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (5, 7),
    (6, 8),
    (7, 8),
    (8, 9),
]

# Initialize the dict with an empty list for each user id:
friendships = collections.defaultdict(list)
for left, right in friendship_pairs:
    friendships[left].append(right)
    friendships[right].append(left)


def number_of_friends(user: Dict[str, Union[int, str]]):
    """How many friends does _user_ have?"""
    user_id = user["id"]
    friend_ids = friendships[user_id]
    return len(friend_ids)


total_connections = sum(number_of_friends(user) for user in users)

num_users = len(users)
avg_connections = total_connections / num_users

# Create a list (user_id, number_of_friends)
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]

num_friends_by_id.sort(
    key=lambda id_and_friends: id_and_friends[1],
    reverse=True,
)

# Ranking users by their number of friends, most to least.
print(num_friends_by_id)

# Data Scientists You May Know
##############################


def foaf_ids_bad(user):
    """foaf is short for 'friend of a friend'."""
    return [
        foaf_id
        for friend_id in friendships[user["id"]]
        for foaf_id in friendships[friend_id]
    ]


assert foaf_ids_bad(users[0]) == [0, 2, 3, 0, 1, 3]


def friends_of_friends(user):
    user_id = user["id"]
    return collections.Counter(
        foaf_id
        for friend_id in friendships[user["id"]]  # For each of my freinds
        for foaf_id in friendships[friend_id]  # find their friends
        if foaf_id != user_id  # who aren't me
        and foaf_id not in friendships[user_id]  # and aren't my friends
    )


print(friends_of_friends(users[3]))


assert friends_of_friends(users[3]) == collections.Counter({0: 2, 5: 1})


"""
As a data scientist, you know that you also might enjoy meeting users with similar interests.
(This is a good examples of the "substantive expertise" aspect of data science.) After asking
around, you manage to get your hands on this data, as a list of pairs (user_id, interest):
"""

interests = [
    (0, "Hadoop"),
    (0, "Big Data"),
    (0, "HBase"),
    (0, "Java"),
    (0, "Spark"),
    (0, "Storm"),
    (0, "Cassandra"),
    (1, "NoSQL"),
    (1, "MongoDB"),
    (1, "Cassandra"),
    (1, "HBase"),
    (1, "Postgres"),
    (2, "Python"),
    (2, "scikit-learn"),
    (2, "scipy"),
    (2, "numpy"),
    (2, "statsmodels"),
    (2, "pandas"),
    (3, "R"),
    (3, "Python"),
    (3, "statistics"),
    (3, "regression"),
    (3, "probability"),
    (4, "machine learning"),
    (4, "regression"),
    (4, "decision trees"),
    (4, "libsvm"),
    (5, "Python"),
    (5, "R"),
    (5, "Java"),
    (5, "C++"),
    (5, "Haskell"),
    (5, "programming languages"),
    (6, "statistics"),
    (6, "probability"),
    (6, "mathematics"),
    (6, "theory"),
    (7, "machine learning"),
    (7, "scikit-learn"),
    (7, "Mahout"),
    (7, "neural networks"),
    (8, "neural networks"),
    (8, "deep learning"),
    (8, "Big Data"),
    (8, "artificial intelligence"),
    (9, "Hadoop"),
    (9, "Java"),
    (9, "MapReduce"),
    (9, "Big Data"),
]


# Works but recomputes on every call.
def data_scientists_who_list(target_interest: str):
    """Find the ids of all users who like the target interest."""
    return [user_id for user_id, interest in interests if interest == target_interest]


user_ids_by_interest = collections.defaultdict(list)
for user_id, interest_ in interests:
    user_ids_by_interest[interest_].append(user_id)

interests_by_user_id = collections.defaultdict(list)
for user_id, interest_ in interests:
    interests_by_user_id[user_id].append(interest_)


# Now it's easy to find who has the most interests in common with a given user


def most_common_interests_with(user):
    return collections.Counter(
        interested_user_id
        for interest in interests_by_user_id[user["id"]]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user["id"]
    )


# Salaries and Experience
##############################


"""
Right as you're about to head to lunch, the VP of Public Relations asks if you can provide
some fun facts about how much data scientists earn. Salary data is of course sensitive,
but he manages to provide you an anonymous dataset containing each user's `salary` (in dollars)
and `tenure` as a data scientist (in years).
"""


salaries_and_tenures = [
    (83000, 8.7),
    (88000, 8.1),
    (48000, 0.7),
    (76000, 6),
    (69000, 6.5),
    (76000, 7.5),
    (60000, 2.5),
    (83000, 10),
    (48000, 1.9),
    (63000, 4.2),
]

salary_by_tenure = collections.defaultdict(list)
for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)

# Keys are years, each value is average salary for that tenure
average_salary_by_tenure = {
    tenure: sum(salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}

print(f"Not particularly useful: {average_salary_by_tenure}")


def tenure_bucket(tenure):
    if tenure < 2:
        return "less than two"
    elif tenure < 5:
        return "between two and five"
    else:
        return "more than five"


# Keys are tenure buckets, values are lists of salaries for that bucket.
salary_by_tenure_bucket = collections.defaultdict(list)
for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)

average_salary_by_bucket = {
    tenure_bucket: sum(salaries) / len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.items()
}

print("Ave salary by bucket:")
print(average_salary_by_bucket)

# Paid Accounts
##############################

"""
When you get back to your desk, the VP of Revenue is waiting for you. She wants to
better understand which users pay for accounts and which don't. (She knows their names,
but that's not particularly actionable information.
"""


def predict_paid_or_unpaid(years_experience):
    if years_experience < 3.0:
        return "paid"
    elif years_experience < 8.5:
        return "unpaid"
    else:
        return "paid"


# Topics of Interest
##############################

"""
As you're wrapping up your first day, the VP of Content Strategy asks you for data about
what topics users are most interested in, so that she can plan out her blog calendar accordingly.
You already have the raw data from the friend-suggester project.

One simple (if not particularly exciting) way to find the most popular interest is to count the words.
"""

words_and_counts = collections.Counter(
    word for user, interest in interests for word in interest.lower().split()
)

print("\nPOPULAR TOPICS:")
for word, count in words_and_counts.most_common():
    if count > 1:
        print(word, count)
