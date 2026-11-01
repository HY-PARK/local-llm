import ollama
import time

stream = ollama.chat(
    model="gemma4:12b",
    #model="qwen3.8:27b",
    messages=[
        {
            "role": "system",
            "content": "나의 조수이며, 나의 질문에 대해 깊은 지식으로 간결한 핵심을 알려줘"
        },
        {
            "role": "user",
            "content": "인터넷에 대해 알려줘"
        }
    ],
    stream=True
)

start_time = time.time()
for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

print()
end_time = time.time()
print(f"Response time: {end_time - start_time:.2f} seconds")
