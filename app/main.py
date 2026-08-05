"""나만의 퀴즈 게임 실행 진입점"""

from app.game import QuizGame


def main():
    """게임을 만들고 실행한다."""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
