import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ALPP.settings")

import django

django.setup()

from faker import Faker
from modules.models import Language, Module, Lesson, Section, Quiz, Question, Answer

fake = Faker()


def create_modules(num_modules=10, languages=None):
    modules = []
    if not languages:
        languages = Language.objects.all()
    for i in range(1, num_modules + 1):
        for language in languages:
            module_order = i
            module = Module.objects.create(
                title=f"Module #{i}",
                language=language,
                description=fake.paragraph(),
                order=module_order
            )
            modules.append(module)
    return modules


def create_lessons(num_lessons=10, modules=None):
    lessons = []
    if not modules:
        modules = Module.objects.all()
    for module in modules:
        for i in range(1, num_lessons + 1):
            lesson_order = i
            lesson = Lesson.objects.create(
                title=f"Lesson #{i} of {module.title}",
                module=module,
                description=fake.paragraph(),
                difficulty_level=fake.random_element(['Easy', 'Medium', 'Hard']),
                order=lesson_order
            )
            lessons.append(lesson)
    return lessons


def create_sections(num_sections=5, lessons=None):
    sections = []
    if not lessons:
        lessons = Lesson.objects.all()
    for lesson in lessons:
        for i in range(1, num_sections + 1):
            section = Section.objects.create(
                lesson=lesson,
                title=f"Section #{i} of {lesson.title}",
                contents=fake.paragraphs(nb=3),
            )
            sections.append(section)
    return sections


def create_quizzes(num_quizzes=10, modules=None):
    quizzes = []
    if not modules:
        modules = Module.objects.all()
    for module in modules:
        for i in range(1, num_quizzes + 1):
            quiz_order = i
            quiz = Quiz.objects.create(
                title=f"Quiz #{i} of {module.title}",
                module=module,
                description=fake.paragraph(),
                difficulty_level=fake.random_element(['Easy', 'Medium', 'Hard']),
                order=quiz_order,
            )
            quizzes.append(quiz)
    return quizzes


def create_questions(num_questions=5, quizzes=None):
    questions = []
    if not quizzes:
        quizzes = Quiz.objects.all()
    for quiz in quizzes:
        for i in range(1, num_questions + 1):
            question = Question.objects.create(
                quiz=quiz,
                text=f"Question #{i} of {quiz.title}",
                question_type=fake.random_element(['Single Choice', 'Multiple Choice', 'Open Text'])
            )
            questions.append(question)
    return questions


def create_answers(num_answers=4, questions=None):
    answers = []
    if not questions:
        questions = Question.objects.all()
    for question in questions:
        for i in range(1, num_answers + 1):
            answer = Answer.objects.create(
                question=question,
                text=f"Answer #{i} of {question.text}",
                is_correct=fake.random_element(['Correct', 'Incorrect'])
            )
            answers.append(answer)
    return answers


def main():
    languages = Language.objects.all()
    modules = create_modules(languages=languages)
    lessons = create_lessons(modules=modules)
    sections = create_sections(lessons=lessons)
    quizzes = create_quizzes(modules=modules)
    questions = create_questions(quizzes=quizzes)
    answers = create_answers(questions=questions)


if __name__ == "__main__":
    main()
