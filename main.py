import json
import os


class Question:
    def __init__(self, text, choices, answer):
        self.text = text
        self.choices = choices
        self.answer = answer

    def checkAnswer(self, given_answer):
        return self.answer == given_answer

    def to_dict(self):
        return {
            "text": self.text,
            "choices": self.choices,
            "answer": self.answer
        }


    def from_dict(data):
        return Question(data["text"], data["choices"], data["answer"])


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.correct = 0
        self.questionIndex = 0

    def getQuestion(self):
        return self.questions[self.questionIndex]

    def display(self):
        question = self.getQuestion()
        print(f"\nSoru {self.questionIndex + 1}: {question.text}")
        for i, choice in enumerate(question.choices):
            print(f"  {chr(97 + i)}) {choice}")

        answer_index = input("Cevap harfini gir (a/b/c/d): ").lower()
        if answer_index in ['a', 'b', 'c', 'd']:
            try:
                selected_answer = question.choices[ord(answer_index) - 97]
                self.guess(selected_answer)
            except IndexError:
                print("Geçersiz seçim.")
        else:
            print("Geçersiz giriş.")
            self.display()

    def guess(self, answer):
        question = self.getQuestion()
        if question.checkAnswer(answer):
            self.correct += 1
        self.questionIndex += 1
        self.loadQuestion()

    def loadQuestion(self):
        self.displayProgress()
        if self.questionIndex == len(self.questions):
            self.showScore()
        else:
            self.display()

    def displayProgress(self):
        total = len(self.questions)
        current = self.questionIndex + 1
        print(f"{' Quiz ' + str(current) + ' / ' + str(total) + ' ':*^50}")

    def showScore(self):
        score = (self.correct / len(self.questions)) * 100
        print(f"\n100 üzerinden puanınız: {score:.1f}")




def load_questions_from_file(filename="questions.json"):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Question.from_dict(q) for q in data]


def save_question_to_file(question, filename="questions.json"):
    questions = load_questions_from_file(filename)
    questions.append(question)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([q.to_dict() for q in questions], f, indent=4, ensure_ascii=False)


def overwrite_questions(questions, filename="questions.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([q.to_dict() for q in questions], f, indent=4, ensure_ascii=False)



def list_questions():
    questions = load_questions_from_file()
    if not questions:
        print("Hiç soru bulunamadı.")
        return
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q.text} | Doğru cevap: {q.answer}")


def add_question():
    text = input("Soru metni: ")
    choices = []
    for i in range(4):
        secenek = input(f"{chr(97+i)}) şıkkı: ")
        choices.append(secenek)
    answer = input("Doğru cevabın metnini aynen gir: ")
    question = Question(text, choices, answer)
    save_question_to_file(question)
    print("Soru başarıyla eklendi.")


def start_quiz():
    questions = load_questions_from_file()
    if not questions:
        print("Soru bulunamadı. Önce soru ekleyin.")
        return
    quiz = Quiz(questions)
    quiz.loadQuestion()


def edit_question(filename="questions.json"):
    questions = load_questions_from_file(filename)
    if not questions:
        print("Hiç soru yok, önce soru ekleyin.")
        return

    print("\n--- Mevcut Sorular ---")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q.text} | Cevap: {q.answer}")

    try:
        secim = int(input("Düzenlemek istediğiniz soru numarasını girin: "))
        if secim < 1 or secim > len(questions):
            print("Geçersiz numara!")
            return
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
        return

    print("\n--- Yeni Soru Bilgilerini Girin ---")
    text = input("Yeni soru metni: ")
    choices = []
    for i in range(4):
        secenek = input(f"{chr(97+i)}) yeni şık: ")
        choices.append(secenek)
    answer = input("Yeni doğru cevabın metnini aynen girin: ")

    questions[secim - 1] = Question(text, choices, answer)
    overwrite_questions(questions, filename)
    print("Soru başarıyla güncellendi.")



def menu():
    while True:
        print("\n--- Quiz Uygulaması ---")
        print("1. Soru Ekle")
        print("2. Soruları Listele")
        print("3. Quiz'e Başla")
        print("4. Soru Düzenle")
        print("5. Çıkış")
        secim = input("Seçim: ")

        if secim == "1":
            add_question()
        elif secim == "2":
            list_questions()
        elif secim == "3":
            start_quiz()
        elif secim == "4":
            edit_question()
        elif secim == "5":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    menu()
