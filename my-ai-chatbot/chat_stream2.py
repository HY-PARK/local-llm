import ollama

stream = ollama.chat(
    model="gemma4:12b",
    messages=[
        {
            "role": "system",
            "content": "You are an enthusiastic kindergarten teacher who uses simple words and lots of encouragement."
        },
        {
            "role": "user",
            "content": "What is photosynthesis?"
        }
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

print()
