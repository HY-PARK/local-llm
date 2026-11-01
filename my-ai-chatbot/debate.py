import ollama

historyGemma = [
    {
        "role": "system",
        "content": "You believe dogs are better pets than cats. Argue your position. "
        "Never change sides. Directly rebut the opponent's last point. "
        "Reply in under 80 words in Korean."
    },
]

historyQwen = [
    {
        "role": "system",
        "content": "You believe cats are better pets than dogs. Argue your position. "
        "Never change sides. Directly rebut the opponent's last point. "
        "Reply in under 80 words in Korean."
    },
]

# streamGemma = ollama.chat(
#         model="gemma4:12b",
#         messages=historyGemma,
#         stream=True
# )

# streamQwen = ollama.chat(
#         model="qwen3.8:27b",
#         messages=historyQwen,
#         stream=True
# )

# print("\n\n[Gemman's Opinion]\n\n")

# response_text = ""
# for chunk in streamGemma:
#     piece = chunk["message"]["content"]
#     print(piece, end="", flush=True)
#     response_text += piece


# for i in range(5):
#     print("\n\n---\n\n")

#     print(response_text)

#     historyQwen.append({
#         "role": "assistant",
#         "content": response_text
#     })

#     streamQwen = ollama.chat(
#         model="gemma4:12b",
#         messages=historyQwen,
#         stream=True
#     )

#     print("\n\n[Qwen's Opinion]\n\n")
#     for chunk in streamQwen:
#         piece = chunk["message"]["content"]
#         print(piece, end="", flush=True)
#         response_text += piece

#     print("\n\n---\n\n")

#     historyGemma.append({
#         "role": "assistant",
#         "content": response_text
#     })

#     streamGemma = ollama.chat(
#         model="gemma4:12b",
#         messages=historyGemma,
#         stream=True
#     )

#     print("\n\n[Gemman's Opinion]\n\n")
#     for chunk in streamGemma:
#         piece = chunk["message"]["content"]
#         print(piece, end="", flush=True)
#         response_text += piece


def speak_with_model(model_name, history):
    stream = ollama.chat(
        model=model_name,
        messages=history,
        stream=True
    )

    response_text = ""
    for chunk in stream:
        piece = chunk["message"]["content"]
        print(piece, end="", flush=True)
        response_text += piece

    return response_text

message =  "Why are cats the best pets?"

historyQwen.append({
    "role": "assistant",
    "content": message
})

for i in range(5):
    historyGemma.append({
        "role": "user",
        "content": message
    })

    print("\n\n[Gemman's Opinion]\n\n")
    gemma_response = speak_with_model("gemma4:12b", historyGemma)

    historyGemma.append({
        "role": "assistant",
        "content": gemma_response
    })

    historyQwen.append({
        "role": "user",
        "content": gemma_response
    })

    print("\n\n[Qwen's Opinion]\n\n")
    qwen_response = speak_with_model("qwen3.8:27b", historyQwen)
    historyQwen.append({
        "role": "assistant",
        "content": qwen_response
    })

    message = qwen_response
