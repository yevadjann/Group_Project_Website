from app import app, db, User, QuizResult

def get_all_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

def get_all_quiz_results():
    with app.app_context():
        quiz_results = QuizResult.query.all()
        for result in quiz_results:
            print(
                f"User ID: {result.user_id}, Quiz: {result.quiz_name}, Score: {result.score}/{result.total_questions}")


if __name__ == "__main__":
    print("Fetching all users:")
    get_all_users()

    print("\nFetching all quiz results:")
    get_all_quiz_results()
