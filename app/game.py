"""메뉴와 게임 진행을 담당하는 QuizGame 클래스"""

import json

from app.quiz import DEFAULT_QUIZZES, Quiz

# 데이터 파일은 프로젝트 루트에 둔다.
STATE_FILE = "state.json"


class QuizGame:
    """퀴즈 목록을 관리하고 메뉴를 진행한다."""

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load()

    def load(self):
        """state.json에서 퀴즈를 불러온다. 없거나 손상되었으면 기본 퀴즈를 쓴다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.quizzes = [Quiz(item["question"], item["choices"], item["answer"]) for item in data["quizzes"]]
            self.best_score = data["best_score"]
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")
        except FileNotFoundError:
            print("저장된 파일이 없어 기본 퀴즈로 시작합니다.")
            self.use_default_quizzes()
        except (json.JSONDecodeError, TypeError, KeyError) as error:
            print(f"저장 파일을 읽을 수 없어 기본 퀴즈로 복구합니다. ({error})")
            self.use_default_quizzes()

    def use_default_quizzes(self):
        """기본 퀴즈 데이터로 초기화한다."""
        self.quizzes = list(DEFAULT_QUIZZES)
        self.best_score = None

    def save(self):
        """퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"저장에 실패했습니다. ({error})")

    def input_number(self, prompt, minimum, maximum):
        """정해진 범위의 숫자를 입력받는다. 잘못된 입력이면 다시 입력받는다."""
        while True:
            value = input(prompt).strip()
            if value == "":
                print(f"입력이 비어 있습니다. {minimum}부터 {maximum} 사이의 숫자를 입력하세요.")
                continue
            try:
                number = int(value)
            except ValueError:
                print(f"숫자가 아닙니다. {minimum}부터 {maximum} 사이의 숫자를 입력하세요.")
                continue
            if number < minimum or number > maximum:
                print(f"{minimum}부터 {maximum} 사이의 숫자를 입력하세요.")
                continue
            return number

    def input_text(self, prompt):
        """비어 있지 않은 문장을 입력받는다."""
        while True:
            value = input(prompt).strip()
            if value != "":
                return value
            print("빈 값은 입력할 수 없습니다. 다시 입력하세요.")

    def show_menu(self):
        """메뉴를 출력한다."""
        print()
        print("===== 나만의 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("===========================")

    def play(self):
        """저장된 퀴즈를 순서대로 출제하고 맞힌 개수를 알려준다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        print(f"\n퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0
        for number, quiz in enumerate(self.quizzes, 1):
            quiz.show(number)
            selected = self.input_number("정답 번호 (1-4): ", 1, 4)
            if quiz.is_correct(selected):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n결과: {len(self.quizzes)}문제 중 {score}문제 정답!")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
        self.save()

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 넣고 파일에 저장한다."""
        print("\n새로운 퀴즈를 추가합니다.")
        question = self.input_text("문제: ")
        choices = []
        for number in range(1, 5):
            choices.append(self.input_text(f"선택지 {number}: "))
        answer = self.input_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print(f"퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)")

    def list_quizzes(self):
        """등록된 퀴즈 목록을 출력한다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, 1):
            print(f"[{number}] {quiz.question}")

    def show_score(self):
        """최고 점수를 출력한다."""
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
            return

        print(f"\n최고 점수: {self.best_score}문제 정답")

    def run(self):
        """메뉴를 반복해서 보여 주고 선택한 기능을 실행한다."""
        try:
            while True:
                self.show_menu()
                choice = self.input_number("선택: ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                else:
                    print("게임을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다. 저장하고 종료합니다.")
        self.save()
