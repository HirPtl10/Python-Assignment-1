from collections import deque
from typing import List, Dict, Optional, Tuple

class AhoCorasickNode:
    def __init__(self):
        self.children: Dict[str, AhoCorasickNode] = {}
        self.fail: Optional[AhoCorasickNode] = None
        self.is_end: bool = False

class AhoCorasickAutomaton:
    def __init__(self):
        self.root = AhoCorasickNode()

    def add_word(self, word: str):
        word = word.lower()
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
            node = node.children[char]
        node.is_end = True

    def build_failure_links(self):
        queue = deque()
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                fail_node = current.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children[char] if fail_node else self.root
                if child.fail.is_end:
                    child.is_end = True
                queue.append(child)

    def contains_any(self, text: str) -> bool:
        text = text.lower()
        node = self.root
        for char in text:
            while node is not None and char not in node.children:
                node = node.fail
            if node is None:
                node = self.root
                continue
            node = node.children[char]
            if node.is_end:
                return True
        return False

def check_repeated_chars(pwd: str, max_allowed: int = 3) -> bool:
    if not pwd:
        return False
    count = 1
    for i in range(1, len(pwd)):
        if pwd[i] == pwd[i - 1]:
            count += 1
            if count > max_allowed:
                return True
        else:
            count = 1
    return False

def classify_password(pwd: str, automaton: AhoCorasickAutomaton) -> str:
    if automaton.contains_any(pwd):
        return "COMPROMISED"

    if len(pwd) < 6 or len(pwd) > 12:
        return "WEAK_LENGTH"

    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(c in "$#@" for c in pwd)

    if not (has_lower and has_upper and has_digit and has_special):
        return "WEAK_PATTERN"

    if check_repeated_chars(pwd, max_allowed=3):
        return "WEAK_PATTERN"

    return "STRONG"

def audit_passwords(banned_words: List[str], passwords: List[str]) -> List[str]:
    automaton = AhoCorasickAutomaton()
    for word in banned_words:
        if word:
            automaton.add_word(word)
    automaton.build_failure_links()

    results: List[str] = []
    for idx, pwd in enumerate(passwords, 1):
        classification = classify_password(pwd, automaton)
        results.append(f"{idx}: {classification}")
    return results

if __name__ == "__main__":
    import sys
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if lines:
        b = int(lines[0])
        banned_words = lines[1:1+b]
        n = int(lines[1+b])
        passwords = lines[2+b:2+b+n]
        output = audit_passwords(banned_words, passwords)
        for line in output:
            print(line)
