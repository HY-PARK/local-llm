import ollama

stream = ollama.chat(
    model="gemma4:12b",
    messages=[
        {
            "role": "system",
            "content": "You are a quiz master. Ask the user one trivia question "
               "at a time. After they answer, tell them if they're right "
               "or wrong and explain the correct answer. Then ask another "
               "question. Keep score."
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
