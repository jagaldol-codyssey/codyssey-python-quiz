"""메뉴와 게임 진행을 담당하는 QuizGame 클래스"""


class QuizGame:
    """메뉴를 보여 주고 사용자가 고른 기능을 실행한다."""

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

    def run(self):
        """메뉴를 반복해서 보여 주고 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = self.input_number('선택: ', 1, 5)
            if choice == 5:
                print('게임을 종료합니다.')
                break
            print('아직 준비 중인 기능입니다.')
