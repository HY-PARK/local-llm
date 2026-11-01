# [2주차 스터디] Ollama와 Python으로 로컬 AI 챗봇 만들기

2주차에는 Mac에서 Ollama 모델을 실행하고, Python으로 간단한 챗봇을 만드는 방법을 학습했다. 기본 질문부터 시스템 프롬프트, 스트리밍, 대화 기록 저장까지 실습한 뒤 두 모델이 서로 토론하는 프로그램으로 확장했다.

## 1. 로컬 모델 실행하기

Ollama로 모델을 내려받고 터미널에서 대화하는 방법을 배웠다. 모델을 선택할 때는 모델 크기와 컴퓨터의 메모리를 함께 고려하고, 양자화로 모델의 메모리 사용량을 줄일 수 있다는 점도 학습했다.

이번 실습에서는 `gemma4:12b`와 `qwen3.8:27b`를 사용했다. 기본 실행 명령은 다음과 같다.

```bash
ollama pull gemma4:12b  # 모델 다운로드
ollama run gemma4:12b   # 터미널에서 대화
ollama list            # 설치된 모델 확인
ollama ps              # 실행 중인 모델 확인
```

## 2. Python 개발 환경 준비하기

스터디에서는 VS Code와 Python 개발 환경을 준비하고, 프로젝트별로 패키지를 관리하기 위한 가상환경 사용법을 다뤘다. `my-ai-chatbot` 프로젝트에도 `.venv`를 만들고 필요한 패키지를 설치했다.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install ollama streamlit
```

설치한 패키지는 `requirements.txt`로 기록해 두었다. 다른 환경에서도 같은 버전의 패키지를 설치할 때 사용할 수 있다.

```bash
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

이번에 작성한 예제는 터미널에서 실행하는 Python 프로그램이다.

## 3. Python으로 모델에 질문하기

`chat_basic.py`에서는 모델에 질문 하나를 보내고 답변을 출력했다. `ollama.chat()`에 모델 이름과 메시지를 전달하면 응답을 받을 수 있다.

```python
import ollama

response = ollama.chat(
    model="gemma4:12b",
    messages=[
        {"role": "user", "content": "펭귄에 대한 사실을 알려줘"}
    ],
)

print(response["message"]["content"])
```

이 구조를 바탕으로 질문과 역할을 바꾸면서 다른 예제로 확장했다.

## 4. 시스템 프롬프트로 역할 정하기

메시지는 역할에 따라 구분한다.

| 역할 | 용도 |
| --- | --- |
| `system` | 모델의 역할과 응답 지침 설정 |
| `user` | 사용자의 질문이나 요청 |
| `assistant` | 모델이 생성한 답변 |

`chat_stream1.py`부터 `chat_stream3.py`까지는 “광합성이란 무엇인가?”라는 같은 질문에 서로 다른 역할을 설정한 예제다. 엄격한 수학 교수, 쉬운 단어를 사용하는 유치원 선생님, 책을 추천하는 사서라는 지침을 각각 작성했다.

질문뿐 아니라 어떤 역할과 설명 방식을 지정하는지도 챗봇을 구성하는 중요한 요소라는 점을 배웠다.

## 5. 스트리밍으로 답변 출력하기

`chat_stream.py`에서는 `stream=True`를 사용했다. 답변 전체가 완성될 때까지 기다리는 대신, 생성 중인 내용을 전달받는 대로 화면에 출력하는 방식이다.

```python
stream = ollama.chat(
    model="gemma4:12b",
    messages=[{"role": "user", "content": "인터넷에 대해 알려줘"}],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
```

`flush=True`는 출력 내용을 버퍼에 남겨 두지 않고 바로 표시하도록 한다. 스트리밍을 적용하면 사용자가 답변이 나오는 과정을 볼 수 있다.

## 6. 대화 이어 가기와 기록 저장하기

`chat_history.py`에서는 사용자 입력을 반복해서 받고, 질문과 답변을 `history` 리스트에 추가했다. 다음 요청에도 이 리스트를 함께 전달해 앞선 대화를 참고할 수 있도록 했다.

```text
사용자 입력 → 기록에 추가 → 모델 호출 → 답변을 기록에 추가 → 다음 입력
```

대화 맥락을 유지하려면 사용자 질문뿐 아니라 모델의 답변도 함께 보관해야 한다는 점을 배웠다.

`chat_history_improve.py`에는 `exit` 또는 `quit`으로 종료할 때 대화 내용을 `chat_history.txt`에 저장하는 기능을 추가했다. 실제 저장 파일에서 시스템 프롬프트와 사용자 질문, 모델 답변을 확인할 수 있었다. 현재는 저장까지 구현했으며, 다음 실행에서 파일을 읽어 대화를 이어 가는 기능은 포함하지 않았다.

## 7. 번역기와 퀴즈 봇으로 응용하기

시스템 프롬프트를 바꿔 간단한 용도의 예제도 작성했다.

- **번역기 (`translator.py`)**: “Start the quiz.”를 일본어, 스페인어, 프랑스어로 번역하고 목록으로 출력하도록 설정했다.
- **퀴즈 봇 (`quiz_bot.py`)**: 퀴즈 진행자 역할을 지정하고 “Start the quiz.”라는 메시지로 첫 문제를 요청했다.

퀴즈 봇에는 정답 확인과 점수 관리 지침도 넣었지만, 현재 코드는 첫 응답을 받는 단계까지다. 실제로 문제를 계속 풀려면 사용자 입력과 대화 기록을 유지하는 루프를 연결해야 한다.

## 8. 두 모델에게 토론시키기

마지막으로 `debate.py`에서는 “개와 고양이 중 누가 더 좋은 반려동물인가?”라는 주제로 두 모델이 대화하도록 만들었다.

| 모델 | 역할 |
| --- | --- |
| `gemma4:12b` | 개가 더 좋은 반려동물이라는 입장 |
| `qwen3.8:27b` | 고양이가 더 좋은 반려동물이라는 입장 |

각 모델에 자신의 입장을 유지하며 상대의 의견에 답하도록 지시했다. 한 모델의 답변을 다른 모델의 입력으로 전달하고, 각자의 대화 기록을 유지하면서 5라운드 동안 번갈아 응답하게 했다.

실행 결과, Gemma는 개의 충성심과 정서적 교감을 강조했고, Qwen은 고양이의 독립성과 자발적인 애정을 강조했다. 저장된 결과의 일부는 다음과 같다.

> **Gemma:** “훈련은 개와 인간이 서로를 이해하기 위한 약속이며, 이를 통해 개는 우리를 보호하고 지지하는 든든한 파트너가 됩니다.”

> **Qwen:** “공동의 약속”이라지만, 누가 그 조건을 정했습니까? 인간이 일방적으로 요구를 씌우는 게 진정한 상호이해입니까?

서로 자기 의견만 말하는 것이 아니라, **상대가 한 말을 받아서 반박하는 대화가 잘 이어지는 것을 확인할 수 있었다.** 기본 챗봇에서 배운 역할 설정과 대화 기록을 활용해 두 모델의 토론까지 구현할 수 있었다.

학습 자료: [Core skills: Building your first AI chatbot](https://gasidaseo.notion.site/Core-skills-Building-your-first-AI-chatbot-40650aec5edf80f3adadf4442b2e6166)  
API 참고: [Ollama Python 라이브러리 공식 문서](https://github.com/ollama/ollama-python)
