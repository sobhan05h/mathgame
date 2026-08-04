import random
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

# تنظیم ابعاد اولیه پنجره برای تست
# Window.size = (400, 650)
Window.clearcolor = (0.08, 0.1, 0.16, 1)


class MathGameApp(App):
    def build(self):
        self.correct_count = 0
        self.current_answer = 0

        # چیدمان اصلی برنامه
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[20, 30, 20, 30],
            spacing=15
        )

        # 1. عنوان
        self.title_label = Label(
            text="Math Challenge",
            font_size='26sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(self.title_label)

        # 2. امتیاز
        self.score_label = Label(
            text="Streak: 0 / 3",
            font_size='18sp',
            color=(0.3, 0.7, 1, 1),
            size_hint=(1, 0.08)
        )
        main_layout.add_widget(self.score_label)

        # 3. کارت نمایش سوال
        self.question_card = BoxLayout(
            orientation='vertical',
            padding=15,
            size_hint=(1, 0.3)
        )
        with self.question_card.canvas.before:
            Color(0.15, 0.2, 0.32, 1)
            self.rect = RoundedRectangle(
                pos=self.question_card.pos, size=self.question_card.size, radius=[15])
        self.question_card.bind(pos=self._update_rect, size=self._update_rect)

        self.question_label = Label(
            text="?",
            font_size='38sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        self.question_card.add_widget(self.question_label)
        main_layout.add_widget(self.question_card)

        # 4. ورودی پاسخ
        self.user_input = TextInput(
            hint_text="Enter your answer...",
            multiline=False,
            input_filter='float',
            font_size='20sp',
            halign='center',
            size_hint=(1, 0.12),
            background_normal='',
            background_color=(0.18, 0.24, 0.35, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 12, 10, 12]
        )
        main_layout.add_widget(self.user_input)

        # 5. دکمه ثبت
        self.submit_btn = Button(
            text="Submit Answer",
            font_size='18sp',
            bold=True,
            size_hint=(1, 0.12),
            background_normal='',
            background_color=(0.15, 0.75, 0.4, 1)
        )
        self.submit_btn.bind(on_press=self.check_answer)
        main_layout.add_widget(self.submit_btn)

        # 6. متن بازخورد
        self.feedback_label = Label(
            text="",
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.15)
        )
        main_layout.add_widget(self.feedback_label)

        self.generate_question()
        return main_layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def generate_question(self):
        num1 = random.randint(1, 15)
        num2 = random.randint(1, 15)
        number = random.randint(1, 7)

        if number == 1:
            x = "+"
            self.current_answer = num1 + num2
        elif number == 2:
            x = "-"
            self.current_answer = num1 - num2
        elif number == 3:
            x = "*"
            self.current_answer = num1 * num2
        elif number == 4:
            x = "/"
            self.current_answer = round(num1 / num2, 2)
        elif number == 5:
            x = "//"
            self.current_answer = num1 // num2
        elif number == 6:
            x = "%"
            self.current_answer = num1 % num2
        else:
            num1 = random.randint(1, 5)
            num2 = random.randint(1, 4)
            x = "**"
            self.current_answer = num1 ** num2

        self.question_label.text = f"{num1}  {x}  {num2}"

    def check_answer(self, instance):
        if not self.user_input.text.strip():
            return

        try:
            val = float(self.user_input.text)
        except ValueError:
            return

        if abs(val - self.current_answer) < 0.01:
            self.correct_count += 1
            self.score_label.text = f"Streak: {self.correct_count} / 3"

            if self.correct_count == 3:
                self.feedback_label.color = (1, 0.85, 0, 1)
                self.feedback_label.text = "Congratulations! You won! 🎉"
                self.submit_btn.disabled = True
            else:
                self.feedback_label.color = (0.2, 0.9, 0.4, 1)
                self.feedback_label.text = "Correct! Good job!"
                self.user_input.text = ""
                self.generate_question()
        else:
            self.correct_count = 0
            self.score_label.text = "Streak: 0 / 3"
            self.feedback_label.color = (1, 0.3, 0.3, 1)
            self.feedback_label.text = f"Wrong! Answer was: {self.current_answer}"
            self.user_input.text = ""
            self.generate_question()


if __name__ == '__main__':
    MathGameApp().run()
