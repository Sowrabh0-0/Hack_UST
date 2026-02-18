import re
from collections import Counter


LOG_FILE = "sample.log" 
THRESHOLD = 0.01

with open(LOG_FILE, "r") as file:
    lines = file.readlines()

all_words = []

for line in lines:
    words = re.findall(r'\b\w+\b', line.lower())
    all_words.extend(words)

word_count = Counter(all_words)

total_words = sum(word_count.values())

print("Total words:", total_words)
print("Unique words:", len(word_count))
print()

rare_words = set()

for word, count in word_count.items():
    if count / total_words < THRESHOLD:
        rare_words.add(word)

print("Rare words found:", len(rare_words))
print("\nSuspicious Lines\n")

for line in lines:
    words_in_line = re.findall(r'\b\w+\b', line.lower())
    
    for word in words_in_line:
        if word in rare_words:
            print(line.strip())
            break 
