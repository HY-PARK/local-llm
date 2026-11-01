import ollama

response = ollama.chat(
    model="gemma4:12b",
    messages=[
        {"role": "user", "content": "펭귄에 대한 사실을 알려줘"}
    ],
)

print(response["message"]["content"])
