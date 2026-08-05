"""메뉴와 게임 진행을 담당하는 QuizGame 클래스"""

import json

from .quiz import DEFAULT_QUIZZES, Quiz

# 데이터 파일은 프로젝트 루트에 둔다.
STATE_FILE = 'state.json'


class QuizGame:
    """퀴즈 목록을 관리하고 메뉴를 진행한다."""

    def __init__(self):
        self.quizzes = []
        self.load()

    def load(self):
        """state.json에서 퀴즈를 불러온다. 없거나 손상되었으면 기본 퀴즈를 쓴다."""
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.quizzes = [
                Quiz(item['question'], item['choices'], item['answer'])
                for item in data['quizzes']
            ]
            print(f'저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)')
        except FileNotFoundError:
            print('저장된 파일이 없어 기본 퀴즈로 시작합니다.')
            self.use_default_quizzes()
        except (json.JSONDecodeError, TypeError, KeyError) as error:
            print(f'저장 파일을 읽을 수 없어 기본 퀴즈로 복구합니다. ({error})')
            self.use_default_quizzes()

    def use_default_quizzes(self):
        """기본 퀴즈 데이터로 초기화한다."""
        self.quizzes = list(DEFAULT_QUIZZES)

    def save(self):
        """퀴즈를 state.json에 UTF-8로 저장한다."""
        data = {'quizzes': [quiz.to_dict() for quiz in self.quizzes]}
        try:
            with open(STATE_FILE, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f'저장에 실패했습니다. ({error})')

    def input_number(self, prompt, minimum, maximum):
        """정해진 범위의 숫자를 입력받는다. 잘못된 입력이면 다시 입력받는다."""
        while True:
            value = input(prompt).strip()
            if value == '':
                print(f'입력이 비어 있습니다. {minimum}부터 {maximum} 사이의 숫자를 입력하세요.')
                continue
            try:
                number = int(value)
            except ValueError:
                print(f'숫자가 아닙니다. {minimum}부터 {maximum} 사이의 숫자를 입력하세요.')
                continue
            if number < minimum or number > maximum:
                print(f'{minimum}부터 {maximum} 사이의 숫자를 입력하세요.')
                continue
            return number

    def show_menu(self):
        """메뉴를 출력한다."""
        print()
        print('===== 나만의 퀴즈 게임 =====')
        print('1. 퀴즈 풀기')
        print('2. 퀴즈 추가')
        print('3. 퀴즈 목록')
        print('4. 점수 확인')
        print('5. 종료')
        print('===========================')

    def play(self):
        """저장된 퀴즈를 순서대로 출제하고 맞힌 개수를 알려준다."""
        if not self.quizzes:
            print('등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.')
            return

        print(f'\n퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)')
        score = 0
        for number, quiz in enumerate(self.quizzes, 1):
            quiz.show(number)
            selected = self.input_number('정답 번호 (1-4): ', 1, 4)
            if quiz.is_correct(selected):
                print('정답입니다!')
                score += 1
            else:
                print(f'오답입니다. 정답은 {quiz.answer}번입니다.')

        print(f'\n결과: {len(self.quizzes)}문제 중 {score}문제 정답!')

    def run(self):
        """메뉴를 반복해서 보여 주고 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = self.input_number('선택: ', 1, 5)
            if choice == 1:
                self.play()
            elif choice == 5:
                print('게임을 종료합니다.')
                break
            else:
                print('아직 준비 중인 기능입니다.')
        self.save()
