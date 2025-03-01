import re
import pandas as pd
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import emoji
import os
from datetime import datetime

file_path = r'C:\Users\77475\.ipython\WhatsApp Chat with Алдияр.txt'
with open(file_path, "r", encoding="utf-8") as file:
    chat_lines = file.readlines()

pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}) - ([^:]+): (.+)")

messages = []
for line in chat_lines:
    match = pattern.match(line)
    if match:
        date, time, sender, message = match.groups()
        messages.append([date, time, sender, message])

df = pd.DataFrame(messages, columns=["Date", "Time", "Sender", "Message"])
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%y")

message_count = df["Sender"].value_counts()
print("Message count per user:")
print(message_count)

daily_messages = df.groupby("Date").size()
daily_messages.plot(kind="line", title="Messages per Day", figsize=(10, 5))
plt.xlabel("Date")
plt.ylabel("Message Count")
plt.show()

# Word Dictionary
word_categories = {
    "common_words": set(["да", "нет", "привет", "как", "что", "это", "я", "ты", "он", "она", "мы", "они"]),
    "stopwords": set(["и", "в", "на", "с", "о", "по", "у", "из", "к", "за"])
}

def get_most_common_words(df, top_n=50):
    all_words = []
    for msg in df["Message"]:
        if "<Media omitted>" not in msg:
            words = re.findall(r"\b[а-яА-Яa-zA-Z]{3,}\b", msg.lower())
            all_words.extend(words)
    word_counter = Counter(all_words)
    return word_counter.most_common(top_n), word_counter

common_words, word_counter = get_most_common_words(df)
print("Most common words:")
print(common_words)

# Эмодзи
emoji_categories = {
    "positive": set(["😀", "😂", "😍", "😊", "👍", "🎉"]),
    "negative": set(["😢", "😡", "💔", "👎"]),
    "neutral": set(["🤔", "😐", "👌"])
}

def get_most_common_emojis(df, top_n=10):
    all_emojis = []
    for msg in df["Message"]:
        all_emojis.extend([char for char in msg if emoji.is_emoji(char)])
    return Counter(all_emojis).most_common(top_n)

common_emojis = get_most_common_emojis(df)
print("Most common emojis:")
print(common_emojis)

user_stats = defaultdict(lambda: {"messages": 0, "words": 0, "emojis": 0})

for _, row in df.iterrows():
    sender = row["Sender"]
    user_stats[sender]["messages"] += 1
    user_stats[sender]["words"] += len(re.findall(r"\b[а-яА-Яa-zA-Z]{3,}\b", row["Message"].lower()))
    user_stats[sender]["emojis"] += sum(1 for char in row["Message"] if emoji.is_emoji(char))

print("User statistics:")
for user, stats in user_stats.items():
    print(f"{user}: {stats}")

word_freq_df = pd.DataFrame(common_words, columns=["Word", "Count"])
emoji_freq_df = pd.DataFrame(common_emojis, columns=["Emoji", "Count"])

# граф
plt.figure(figsize=(10, 4))
plt.bar(word_freq_df["Word"], word_freq_df["Count"])
plt.xticks(rotation=45)
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.title("TOP 200 words")
plt.show()
plt.figure(figsize=(12, 6))
plt.bar(emoji_freq_df["Emoji"], emoji_freq_df["Count"])
plt.xlabel("Emojis")
plt.ylabel("Frequency")
plt.title("Top 10 Most Common Emojis in Chat")
plt.show()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = os.path.join(os.getcwd(), f"chat_analysis_{timestamp}.csv")
df.to_csv(save_path, index=False)
print(f"Chat analysis saved to {save_path}")
