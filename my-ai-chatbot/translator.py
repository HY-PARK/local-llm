import ollama

stream = ollama.chat(
    model="gemma4:12b",
    messages=[
        {
            "role": "system",
            "content": "You are a translator. When the user gives you text, "
               "translate it into Japanese, Spanish, and French. "
               "Format your response as a clean list."
        },
        {
            "role": "user",
            "content": "Start the quiz."
        }
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

print()
