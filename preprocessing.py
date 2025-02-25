import json
from nltk.tokenize import word_tokenize

with open("test_review.json", "r", encoding="utf8") as f:
    origin_data = json.load(f)

print(word_tokenize(origin_data))