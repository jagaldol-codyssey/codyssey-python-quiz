# 나만의 퀴즈 게임

## 프로젝트 개요

Python 표준 라이브러리만 사용해 터미널에서 동작하는 4지선다 퀴즈 게임이다.
메뉴에서 번호를 골라 퀴즈를 풀고, 새 퀴즈를 등록하고, 목록과 최고 점수를 확인할 수 있다.
등록한 퀴즈와 최고 점수는 `state.json`에 저장되므로 프로그램을 종료하고 다시 실행해도 그대로 남는다.

## 퀴즈 주제와 선정 이유

주제는 **개발자 기본 도구**다. 터미널 명령, 파일 권한, Git, Python 예외를 다룬다.

입학연수 과제 1에서 개발 환경을 직접 설정하며 사용해 본 도구들이라,
어디서 가져온 문제가 아니라 내가 직접 확인한 내용을 그대로 문제로 옮길 수 있었다.
기본 5문제는 모두 직접 작성했다.

## 실행 방법

Python 3.10 이상이 필요하고, 설치할 외부 라이브러리는 없다.

### uv로 실행하기 (권장)

[uv](https://docs.astral.sh/uv/)는 Python 버전과 가상 환경을 대신 준비해 주는 도구다.
설치되어 있지 않다면 먼저 설치한다.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

macOS에서 Homebrew를 쓴다면 `brew install uv`로 설치해도 되고,
Windows PowerShell에서는 `irm https://astral.sh/uv/install.ps1 | iex`로 설치한다.

```bash
git clone https://github.com/jagaldol-codyssey/codyssey-python-quiz.git
cd codyssey-python-quiz
uv run python -m app.main
```

`uv run`이 `.python-version`에 적힌 Python 3.10을 자동으로 준비한 뒤 프로그램을 실행한다.

### uv 없이 실행하기

Python 3.10 이상이 이미 설치되어 있다면 그대로 실행해도 된다.

```bash
cd codyssey-python-quiz
python3 -m app.main
```

## 기능 목록

| 번호 | 기능 | 설명 |
| --- | --- | --- |
| 1 | 퀴즈 풀기 | 저장된 퀴즈를 순서대로 출제하고, 문제마다 정답/오답과 최종 결과를 알려준다. |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력받아 목록에 넣고 파일에 저장한다. |
| 3 | 퀴즈 목록 | 저장된 퀴즈 목록을 번호와 함께 보여 준다. |
| 4 | 점수 확인 | 지금까지의 최고 점수를 보여 준다. |
| 5 | 종료 | 현재 상태를 저장하고 종료한다. |

입력값은 앞뒤 공백을 지운 뒤 처리한다. 빈 입력, 숫자가 아닌 입력, 허용 범위를 벗어난 숫자는
안내 메시지를 출력하고 다시 입력받는다. `Ctrl+C`나 입력 종료(EOF)가 발생해도 안내 메시지를
출력하고 저장한 뒤 정상적으로 끝난다.

## 파일 구조

```text
codyssey-python-quiz/
├── app/
│   ├── __init__.py
│   ├── main.py          # 프로그램 진입점
│   ├── quiz.py          # Quiz 클래스와 기본 퀴즈 5문제
│   └── game.py          # QuizGame 클래스 (메뉴, 게임 진행, 파일 저장/불러오기)
├── state.json           # 퀴즈와 최고 점수 저장 파일 (첫 실행 시 자동 생성)
├── pyproject.toml       # 프로젝트 정보와 Python 3.10 이상 요구 사항
├── uv.lock              # uv가 관리하는 잠금 파일
├── .python-version      # 실행에 사용할 Python 버전 (3.10)
├── .gitignore
├── README.md
└── MISSION.md           # 과제 요구 사항
```

## 클래스 구조

- `Quiz` (`app/quiz.py`): 퀴즈 한 문제를 담당한다.
  속성은 문제(`question`), 선택지 4개(`choices`), 정답 번호(`answer`)이고,
  문제와 선택지를 출력하는 `show()`, 정답인지 확인하는 `is_correct()`,
  저장용 딕셔너리로 바꾸는 `to_dict()` 메서드를 가진다.
- `QuizGame` (`app/game.py`): 게임 전체를 담당한다.
  속성은 퀴즈 목록(`quizzes`)과 최고 점수(`best_score`)이고,
  메뉴 표시·입력 검증·퀴즈 풀기·추가·목록·점수 확인·파일 저장/불러오기를
  각각 별도 메서드로 나눠 처리한다.

## 데이터 파일 설명 (`state.json`)

- **경로**: 프로젝트 루트의 `state.json`
- **인코딩**: UTF-8
- **역할**: 퀴즈 목록과 최고 점수를 저장해, 프로그램을 종료하고 다시 실행해도 유지되게 한다.
- **생성 시점**: 저장소에는 포함하지 않는다. 처음 실행하면 기본 퀴즈 5문제로 자동 생성된다.
- **예외 처리**: 파일이 없으면 기본 퀴즈로 시작하고,
  파일이 손상되었으면 안내 메시지를 출력한 뒤 기본 퀴즈로 복구한다.

```json
{
  "quizzes": [
    {
      "question": "현재 작업 디렉터리의 절대 경로를 출력하는 명령은?",
      "choices": ["cd", "pwd", "ls", "mkdir"],
      "answer": 2
    }
  ],
  "best_score": 4
}
```

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `quizzes` | 배열 | 퀴즈 목록 |
| `quizzes[].question` | 문자열 | 문제 |
| `quizzes[].choices` | 문자열 배열 | 선택지 4개 |
| `quizzes[].answer` | 정수 | 정답 번호 (1~4) |
| `best_score` | 정수 또는 `null` | 최고 정답 개수. 아직 퀴즈를 풀지 않았으면 `null` |
