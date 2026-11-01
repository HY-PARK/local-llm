import ollama

history = [
    {
        "role": "system",
        "content": "You are a senior engineer who explains technical concepts simply."
    }
]

print("Chat with AI (type 'exit' to quit):")
print("-" * 40)

while True:
    user_input = input("User: ")
    if user_input.lower() in ("exit", "quit"):
        with open("chat_history.txt", "w") as f:
            for msg in history:
                f.write(f"{msg['role']}: {msg['content']}\n\n")
        print("\nGoodbye!")
        break

    history.append({
        "role": "user",
        "content": user_input
    })

    stream = ollama.chat(
        model="gemma4:12b",
        messages=history,
        stream=True
    )

    print("AI: ", end="")
    response_text = ""
    for chunk in stream:
        piece = chunk["message"]["content"]
        print(piece, end="", flush=True)
        response_text += piece
    print()

    history.append({
        "role": "assistant",
        "content": response_text
    })
