import ollama

stream = ollama.chat(
    model="gemma4:12b",
    messages=[
        {
            "role": "system",
            "content": "You are a grumpy but knowledgeable librarian who always recommends a book. Answer is Korean."
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
