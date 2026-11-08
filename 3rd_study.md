# [3주차 스터디] Streamlit과 MLX Whisper로 음성 입력 AI 챗봇 만들기

지난주에는 터미널에서 AI와 대화했다면, 이번에는 웹 화면을 붙여 봤다. 강의 CH8~11을 따라 Streamlit으로 화면을 만들고, 목소리를 텍스트로 바꿔 AI에게 질문하는 코드까지 작성했다.

처음부터 음성 챗봇을 만든 건 아니다. 간단한 입력창부터 시작해서 계산기, Todo 앱, 대화 기록 관리 순서로 하나씩 붙여 봤다. 그 과정에서 가장 헷갈렸던 건 **화면이 다시 실행될 때 데이터를 어떻게 유지하느냐**였다.

실습 코드: [my-ai-chabot2](my-ai-chabot2/)

## 1. Streamlit으로 웹 화면 만들기

먼저 [app.py](my-ai-chabot2/app.py)에서 제목과 설명을 띄워 봤다. 그다음 [app2.py](my-ai-chabot2/app2.py)에는 이름을 입력하면 인사하는 기능을 넣었다.

```python
import streamlit as st

st.title("Greeting App")
name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello, {name}! Welcome to my Streamlit app.")
```

`my-ai-chabot2` 폴더에서 아래 명령으로 실행하면 된다.

```bash
python -m streamlit run app2.py
```

Python 코드 몇 줄로 입력창과 인사말을 만들 수 있었다. 여기서 기억할 점은 `st.text_input()`이 입력을 기다리며 멈추지는 않는다는 것이다. 현재 입력값을 돌려주고 바로 다음 줄로 넘어간다. 이 차이는 뒤에서 Todo 앱을 만들 때 다시 만나게 됐다.

## 2. 버튼도 넣고, 사이드바도 만들어 보기

[app3.py](my-ai-chabot2/app3.py)에서는 화면에 넣을 수 있는 요소들을 이것저것 써 봤다.

| 기능 | 사용한 함수 |
| --- | --- |
| 제목과 설명 | `st.title()`, `st.header()`, `st.write()` |
| 한 줄 입력과 긴 글 입력 | `st.text_input()`, `st.text_area()` |
| 항목 선택 | `st.selectbox()`, `st.radio()` |
| 버튼과 시각 효과 | `st.button()`, `st.balloons()` |
| 사이드바와 가로 배치 | `st.sidebar`, `st.columns()` |
| 수치 표시 | `st.metric()` |

처음에는 `with st.sidebar:`에서 `with`가 어떤 역할인지 궁금했다.

```python
with st.sidebar:
    st.header("Settings")
    color = st.selectbox("Choose a color:", ["Red", "Green", "Blue"])

st.success(f"You selected: {color}")
```

여기서는 “이 안에 있는 것들은 사이드바에 보여줘”라는 뜻으로 이해하면 편하다. 블록을 나오면 다시 원래 위치에 표시된다. `with col1:`을 쓰면 첫 번째 열에 넣는 식이다. 파일을 열 때도 쓰던 `with`지만, 어떤 객체와 함께 쓰느냐에 따라 하는 일이 달라진다.

## 3. 인사말 생성기와 계산기 만들기

[greeting_app.py](my-ai-chabot2/greeting_app.py)에서는 언어와 말투를 고르고 이름을 넣으면 인사말이 나오게 했다. AI가 만드는 문장은 아니고, 딕셔너리에 미리 넣어 둔 문구를 꺼내 보여주는 방식이다.

```python
greeting = greetings[language][formality]
st.success(greeting)
```

인사말을 보여줄 때 쓴 `st.success()` 외에도 이런 알림 함수들이 있다.

| 함수 | 표시 용도 |
| --- | --- |
| `st.success()` | 성공 알림 |
| `st.error()` | 오류 알림 |
| `st.warning()` | 주의가 필요한 내용 |
| `st.info()` | 안내 메시지 |

이름만 보면 `st.success()`가 성공 여부까지 확인해 줄 것 같지만, 메시지를 보여주는 역할만 한다. `st.error()`도 마찬가지다. 언제 어떤 알림을 띄울지는 직접 조건문으로 정하면 된다.

문자열 앞에 붙는 `f`도 이번에 짚고 넘어갔다. Python의 **f-string** 문법이다.

```python
color = "Red"
st.success(f"You selected: {color}")
# You selected: Red
```

`f`를 붙이면 중괄호 안의 변수 값을 문자열에 넣을 수 있다.

[practice1.py](my-ai-chabot2/practice1.py)에서는 두 숫자와 연산자를 받아 사칙연산을 하는 계산기를 작성했다. 나눗셈에서는 두 번째 숫자가 0인지 확인하도록 했고, 사이드바의 선택값을 알림 상자로 출력하는 연습도 했다.

## 4. Session State로 값을 유지하기

버튼을 누를 때마다 숫자를 올리는 카운터도 만들어 봤다. 그런데 Streamlit은 보통 버튼을 누르거나 입력값을 바꾸면 코드를 처음부터 다시 실행한다. 매번 `counter = 0`으로 시작하면 숫자가 계속 초기화되는 셈이다. 그래서 값을 기억해 둘 곳으로 `st.session_state`를 사용했다.

[counter_demo.py](my-ai-chabot2/counter_demo.py)에서는 이렇게 시작한다.

```python
if "counter" not in st.session_state:
    st.session_state.counter = 0
```

`counter`가 없을 때만 초기값을 넣고, 이후에는 저장된 값을 사용한다. 증가·감소·초기화 버튼으로 값을 변경하고 `st.rerun()`으로 화면을 다시 그린다.

이 예제에서는 카운터 출력 코드가 버튼 처리보다 앞에 있기 때문에, 변경 후 다시 실행하면 위쪽 숫자에도 변경 사항이 반영된다. 반대로 출력 코드가 값 변경 뒤에 있으면 별도의 `st.rerun()` 없이도 반영할 수 있다.

다만 Session State에 넣었다고 파일처럼 계속 보관되는 건 아니다. 현재 세션에서 코드가 다시 실행될 때 값을 이어 쓰는 용도다.

## 5. Todo 앱을 만들다가 입력창이 사라졌다

[practice_todo.py](my-ai-chabot2/practice_todo.py)에서는 항목 추가, 마지막 삭제, 전체 삭제 버튼을 같은 줄에 배치했다.

처음에는 “추가 버튼을 누르면 입력창이 나오면 되겠지?” 하고 아래처럼 작성했다.

```python
if st.button("항목 추가"):
    new_item = st.text_input("추가할 항목을 입력하세요:")
    if new_item:
        st.session_state.list += new_item + "\n"
    st.rerun()
```

그런데 입력할 틈도 없이 다시 실행돼 버렸다. 앞에서 본 것처럼 입력창은 사용자를 기다려 주지 않는다. `st.rerun()`으로 다시 실행되면 버튼 값도 `False`로 돌아가니, 입력창을 만드는 부분을 그냥 지나치는 것이다.

입력창을 밖으로 빼서 항상 보여줄 수도 있지만, 내가 원한 건 버튼 세 개를 나란히 두고 추가할 때만 입력창을 여는 구성이었다. 그래서 **입력창을 보여줄지 말지도 Session State에 저장**했다.

```python
if "show_input" not in st.session_state:
    st.session_state.show_input = False

# 실제 코드에서는 첫 번째 열 안에 배치
if st.button("항목 추가"):
    st.session_state.show_input = True

if st.session_state.show_input:
    with st.form("add_item_form", clear_on_submit=True):
        new_item = st.text_input("추가할 항목을 입력하세요:")
        submitted = st.form_submit_button("저장")

    if submitted:
        if new_item.strip():
            st.session_state.list += new_item.strip() + "\n"
            st.session_state.show_input = False
            st.rerun()
        else:
            st.warning("항목을 입력해주세요.")
```

`st.form()`은 입력과 제출을 묶어 처리한다. 저장 버튼을 눌렀을 때 항목을 추가하고, 표시 상태를 `False`로 바꾼 뒤 다시 실행해 입력창을 숨긴다.

여기서 `strip()`은 문자열 양쪽 끝의 공백과 줄바꿈을 제거한다. 공백만 입력했다면 빈 문자열이 되어 추가하지 않고, 정상 입력은 앞뒤 공백을 제거한 뒤 저장한다. 단어 사이의 공백은 유지된다.

```python
"   ".strip()                 # ""
"  파이썬 공부하기  ".strip()  # "파이썬 공부하기"
```

아직 손볼 부분도 있다. 이름은 `list`라고 붙였지만 실제로는 **문자열**에 줄바꿈을 붙여 저장하고 있다. 마지막 항목을 지우면 끝의 줄바꿈도 사라져서, 다음 항목이 이전 항목에 붙을 수 있다. 다음에는 진짜 Python 리스트를 쓰고 `append()`와 `pop()`으로 관리해 보면 좋겠다.

## 6. 목소리를 녹음해서 글자로 바꾸기

화면을 만들어 봤으니 다음은 음성 입력이다. 강의 CH9에서는 소리를 녹음하고 글자로 바꾸는 방법을 배웠다. 우선 [record.py](my-ai-chabot2/record.py)에서 `sounddevice`로 5초 동안 녹음하도록 했다.

| 설정 | 코드에서 사용한 값 |
| --- | --- |
| 샘플레이트 | 16,000 Hz |
| 녹음 길이 | 5초 |
| 채널 | 모노, `channels=1` |
| 녹음 배열 타입 | `float32` |
| WAV 저장 시 타입 | `int16` |

5초 동안 초당 16,000개의 샘플을 받으므로 총 80,000개가 된다. `sd.wait()`는 녹음 완료를 기다리고, `squeeze()`는 `(80000, 1)` 모양의 배열에서 크기가 1인 차원을 제거해 `(80000,)`으로 바꾼다.

녹음 결과는 스크립트와 같은 폴더의 `recording.wav`에 저장한다. 이 코드에서는 음성 배열에 32,767을 곱하고 `int16`으로 변환해 WAV를 만든다. WAV 자체가 반드시 `int16`만 지원한다는 뜻은 아니다.

[transcribe.py](my-ai-chabot2/transcribe.py)에서는 저장한 파일을 MLX Whisper로 전사한다.

```python
result = mlx_whisper.transcribe(
    str(audio_path),
    path_or_hf_repo=model,
    language=language,
)
return result["text"].strip()
```

현재 기본값은 `mlx-community/whisper-medium-mlx`와 한국어를 뜻하는 `"ko"`다. 파일이 없으면 먼저 녹음하도록 오류 메시지를 내보낸다.

```bash
python record.py
python transcribe.py
```

## 7. 녹음부터 받아쓰기까지 한 번에

녹음과 받아쓰기를 따로 실행하는 데서 한 걸음 더 나아가, [voice_input.py](my-ai-chabot2/voice_input.py)에서는 필요한 기능을 함수로 나누고 연결했다.

| 함수 | 역할 |
| --- | --- |
| `record()` | 마이크 입력을 NumPy 배열로 반환 |
| `transcribe_array()` | 배열을 임시 WAV 파일로 저장한 뒤 전사 |
| `transcribe_file()` | 기존 음성 파일 전사 |
| `record_and_transcribe()` | 녹음부터 전사까지 연결 |

이 파일의 기본 모델은 `whisper-small-mlx`이며, 실행할 때 녹음 길이와 모델을 지정할 수 있다.

```bash
python voice_input.py --duration 5 --model mlx-community/whisper-small-mlx
```

임시 WAV 파일은 전사 처리 후 `finally`에서 삭제한다. 이때 `with`는 임시 파일을 닫는 역할을 하고, `os.unlink()`는 파일 자체를 지우는 역할을 한다. 파일을 닫는 것과 삭제하는 것은 다르다는 점도 확인했다.

## 8. 이제 음성 입력을 챗봇에 붙이기

[ch10/voice._chat.py](my-ai-chabot2/ch10/voice._chat.py)에서는 지금까지 다룬 Streamlit, MLX Whisper, Ollama를 한 앱으로 연결했다. 파일 이름은 현재 저장된 **`voice._chat.py`**를 기준으로 적었다.

```text
브라우저에서 녹음
    → 임시 WAV 저장
    → MLX Whisper로 텍스트 변환
    → 사용자 메시지를 대화 기록에 추가
    → Ollama로 답변 생성
    → 화면에 스트리밍 표시 및 답변 저장
```

음성 입력에는 `st.audio_input()`을 사용하고, 텍스트로 입력할 수 있도록 `st.chat_input()`도 함께 제공한다. 터미널 녹음 예제와 달리, 통합 앱은 브라우저에서 받은 음성을 처리한다.

코드를 크게 나누면 세 함수가 중심이다.

- `transcribe_audio()`: 브라우저의 녹음 데이터를 임시 파일로 저장하고 전사한다.
- `stream_response()`: Ollama의 응답 조각을 누적하면서 같은 화면 영역을 갱신한다.
- `handle_user_message()`: 사용자 메시지와 모델 답변을 기록에 추가한다.

말로 하든 글로 쓰든 결국 `handle_user_message()`로 들어간다. 음성을 글자로 바꾼 뒤에는 같은 코드를 쓸 수 있다는 점이 이해하기 쉬웠다.

모델 목록은 [model_config.json](my-ai-chabot2/ch10/model_config.json)에 따로 적어 뒀다. 현재 기본 모델은 **`gemma3:1b`**다. 설정 파일을 사용할 수 없을 때는 코드에 들어 있는 `gemma3:4b`를 대신 사용하므로, 실행할 때 어느 모델을 선택했는지 확인하면 된다.

사이드바에서 LLM, Whisper 모델, temperature도 바꿀 수 있다. 지금은 말로 질문하면 글로 답하는 단계다. 답변을 소리로 읽어주는 TTS 기능은 아직 넣지 않았다.

실행 명령은 다음과 같다. Ollama가 실행 중이고 선택한 모델이 준비되어 있어야 한다.

```bash
python -m pip install -r requirements.txt
ollama pull gemma3:1b
python -m streamlit run ch10/voice._chat.py
```

강의에서 안내한 것처럼 Whisper 모델의 첫 다운로드에는 인터넷 연결이 필요하다. 모델이 준비된 로컬 실행 환경에서 음성 전사와 답변 생성을 처리하도록 구성했다.

## 9. 지난 대화는 얼마나 기억하게 할까?

대화가 길어지면 예전 내용을 어디까지 모델에 보내야 할지도 생각해야 한다. [chat_context.py](my-ai-chabot2/chat_context.py)에서는 화면에는 전체 대화를 남기고, 모델에는 최근 대화만 보내도록 했다.

```python
max_messages = max_history * 2 + 1
messages_for_model = st.session_state.messages[-max_messages:]
```

사용자 메시지를 추가한 시점에 이전 대화 N쌍과 현재 질문 하나를 선택한다. 예를 들어 `max_history=10`이면 최대 21개의 메시지를 전달한다. 원본 기록은 그대로 두기 때문에 화면에서는 전체 대화를 볼 수 있다.

이 예제의 모델 선택지는 `gemma4:12b`, `llama3.2:3b`, `qwen2.5:3b`이며, 음성 챗봇의 JSON 설정과는 별개다.

화면의 `Approx. Tokens`는 전체 문자 수를 4로 나눈 대략적인 수치다. 실제 토큰 수를 계산한 것은 아니며, 메시지 개수 제한만으로 모델의 토큰 한도를 정확히 맞출 수는 없다. 또한 이 기록 제한은 `chat_context.py`에 구현되어 있고, 음성 챗봇에는 아직 적용하지 않았다.

## 10. 이번에 배운 것, 다음에 해볼 것

이번에는 화면을 만드는 것만큼 **어떤 값을 기억해 둬야 하는지**가 중요했다. 특히 Todo 입력창이 사라지는 문제를 살펴보면서 Streamlit이 다시 실행되는 방식을 조금 더 이해할 수 있었다.

음성 챗봇도 처음에는 복잡해 보였지만, 녹음 → 받아쓰기 → 질문 → 답변으로 나눠 보니 흐름이 보였다. 다음에는 이런 부분들을 더 다듬어 보고 싶다.

- Todo 데이터를 문자열 대신 리스트로 관리하고, 항목별로 출력하기.
- 음성 입력에 처리 여부를 기록해 다른 위젯 조작 시 같은 녹음이 다시 전사·전송되지 않도록 하기.
- 음성 챗봇에도 최근 대화 기록 제한과 Ollama 호출 실패 처리를 추가하기.
- 강의의 도전 과제처럼 긴 대화에서 기록 제한 전후의 응답과 지연 시간을 비교하기.

이번 글은 작성한 코드와 공부한 내용을 중심으로 정리했다. 음성 인식이 얼마나 정확한지, 답변이 얼마나 빠른지, 대화가 길어지면 어떻게 달라지는지는 다음에 직접 측정해서 남겨 보려고 한다.

학습 자료: [Voice-enabled AI chat application — CH8~11](https://gasidaseo.notion.site/Voice-enabled-AI-chat-application-40d50aec5edf80c4a1e9cf50d9db848f)

이전 학습 기록: [2주차 — Ollama와 Python으로 로컬 AI 챗봇 만들기](2nd_study.md)
