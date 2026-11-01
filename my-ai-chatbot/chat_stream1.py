import ollama

stream = ollama.chat(
    model="gemma4:12b",
    messages=[
        {
            "role": "system",
            "content": "You are a strict math professor who demands precision."
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
