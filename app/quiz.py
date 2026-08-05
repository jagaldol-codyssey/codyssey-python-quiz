"""퀴즈 한 문제를 표현하는 Quiz 클래스와 기본 퀴즈 데이터"""


class Quiz:
    """문제, 선택지 4개, 정답 번호를 가지는 퀴즈 한 문제"""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self, number):
        """문제 번호와 함께 문제와 선택지를 출력한다."""
        print()
        print(f'[문제 {number}] {self.question}')
        for index, choice in enumerate(self.choices, 1):
            print(f'{index}. {choice}')

    def is_correct(self, selected):
        """입력한 번호가 정답이면 True를 돌려준다."""
        return selected == self.answer

    def to_dict(self):
        """JSON 파일에 저장할 수 있도록 딕셔너리로 바꾼다."""
        return {
            'question': self.question,
            'choices': self.choices,
            'answer': self.answer,
        }


# 주제: 개발자 기본 도구 (터미널, 파일 권한, Git, Python)
DEFAULT_QUIZZES = [
    Quiz(
        '현재 작업 디렉터리의 절대 경로를 출력하는 명령은?',
        ['cd', 'pwd', 'ls', 'mkdir'],
        2,
    ),
    Quiz(
        '숨김 파일까지 포함해 파일 정보를 자세히 보는 명령은?',
        ['ls', 'ls -h', 'ls -la', 'ls --detail'],
        3,
    ),
    Quiz(
        '새 Git 저장소를 만들면서 기본 브랜치를 main으로 지정하는 명령은?',
        ['git start main', 'git init -b main', 'git branch main', 'git clone main'],
        2,
    ),
    Quiz(
        '파일 권한 644가 뜻하는 것은?',
        [
            '누구나 읽고 쓰고 실행할 수 있다',
            '소유자는 읽기와 쓰기, 나머지는 읽기만 할 수 있다',
            '소유자만 읽을 수 있다',
            '아무도 읽을 수 없다',
        ],
        2,
    ),
    Quiz(
        'Python의 input()이 입력의 끝을 만나면 발생하는 예외는?',
        ['ValueError', 'KeyboardInterrupt', 'EOFError', 'StopIteration'],
        3,
    ),
]
