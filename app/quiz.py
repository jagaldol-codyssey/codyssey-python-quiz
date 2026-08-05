"""퀴즈 한 문제를 표현하는 Quiz 클래스"""


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
