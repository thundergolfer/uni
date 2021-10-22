import math
import re
import unittest
from collections import defaultdict

from typing import Iterable
from typing import NamedTuple
from typing import Set
from typing import Tuple


def tokenize(text: str) -> Set[str]:
    text = text.lower()
    all_words = re.findall("[a-z0-9]+", text)  # extract the words, and
    return set(all_words)


class Message(NamedTuple):
    text: str
    is_spam: bool


class NaiveBayesClassifier:
    def __init__(self, k: float = 0.5) -> None:
        self.k = k  # smoothing factor
        self.tokens: Set[str] = set()
        self.token_spam_counts: Dict[str, int] = defaultdict(int)
        self.token_ham_counts: Dict[str, int] = defaultdict(int)
        self.spam_messages = self.ham_messages = 0

    def train(self, messages: Iterable[Message]) -> None:
        for message in messages:
            # Increment message counts
            if message.is_spam:
                self.spam_messages += 1
            else:
                self.ham_messages += 1

            # Increment word counts
            for token in tokenize(message.text):
                self.tokens.add(token)
                if message.is_spam:
                    self.token_spam_counts[token] += 1
                else:
                    self.token_ham_counts[token] += 1

    def _probabilities(self, token: str) -> Tuple[float, float]:
        """
        returns P(token | spam) and P(token | ham)
        """
        spam = self.token_spam_counts[token]
        ham = self.token_ham_counts[token]

        p_token_spam = (spam + self.k) / (self.spam_messages + 2 * self.k)
        p_token_ham = (ham + self.k) / (self.ham_messages + 2 * self.k)

        return p_token_spam, p_token_ham

    def predict(self, text: str) -> float:
        text_tokens = tokenize(text)
        log_prob_if_spam = log_prob_if_ham = 0.0

        # Iterate through each word in our vocabulary
        for token in self.tokens:
            prob_if_spam, prob_if_ham = self._probabilities(token)

            # If *token* appears in the message,
            # add the log probability of seeing it
            if token in text_tokens:
                log_prob_if_spam += math.log(prob_if_spam)
                log_prob_if_ham += math.log(prob_if_ham)
            # Otherwise add the log probability of _not_ seeing it,
            # which is log(1 - probability of seeing it)
            else:
                log_prob_if_spam += math.log(1.0 - prob_if_spam)
                log_prob_if_ham += math.log(1.0 - prob_if_ham)
        prob_if_spam = math.exp(log_prob_if_spam)
        prob_if_ham = math.exp(log_prob_if_ham)
        return prob_if_spam / (prob_if_spam + prob_if_ham)


class TestNaiveBayes(unittest.TestCase):
    def test_prob_calculation(self):
        messages = [
            Message("spam rules", is_spam=True),
            Message("ham rules", is_spam=False),
            Message("hello ham", is_spam=False),
        ]

        model = NaiveBayesClassifier(k=0.5)
        model.train(messages)

        assert model.tokens == {"spam", "ham", "rules", "hello"}
        assert model.spam_messages == 1
        assert model.ham_messages == 2
        assert model.token_spam_counts == {"spam": 1, "rules": 1}
        assert model.token_ham_counts == {"ham": 2, "rules": 1, "hello": 1}

        text = "hello spam"

        probs_if_spam = [
            (1 + 0.5) / (1 + 2 * 0.5),  # "spam" (present)
            1 - (0 + 0.5) / (1 + 2 * 0.5),  # "ham" (not present)
            1 - (1 + 0.5) / (1 + 2 * 0.5),  # "rules" (not present)
            (0 + 0.5) / (1 + 2 * 0.5)  # "hello" (present)
        ]

        probs_if_ham = [
            (0 + 0.5) / (2 + 2 * 0.5),  # "spam" (present)
            1 - (2 + 0.5) / (2 + 2 * 0.5),  # "ham" (not present)
            1 - (1 + 0.5) / (2 + 2 * 0.5),  # "rules" (not present)
            (1 + 0.5) / (2 + 2 * 0.5),  # "hello" (present)
        ]

        p_if_spam = math.exp(sum(math.log(p) for p in probs_if_spam))
        p_if_ham = math.exp(sum(math.log(p) for p in probs_if_ham))

        # Should be about 0.83
        assert model.predict(text) == p_if_spam / (p_if_spam + p_if_ham)


if __name__ == "__main__":
    unittest.main()
