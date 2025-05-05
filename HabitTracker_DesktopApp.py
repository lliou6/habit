from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from datetime import datetime

class HabitTrackerApp(App):
    def build(self):
        self.habits = []
        self.dark_mode = False

        # Initial theme
        Window.clearcolor = (0.9, 0.9, 0.9, 1)

        # Main vertical layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 1) App title
        self.app_name = Label(
            text="Habit Tracker App",
            font_size=30,
            size_hint_y=None, height=50,
            color=(0.2, 0.6, 1, 1)
        )
        self.layout.add_widget(self.app_name)

        # 2) Scrollable habit list
        self.scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 300))
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)

        # 3) Input fields
        self.new_habit_input = TextInput(
            hint_text="Add a new habit", size_hint_y=None, height=40, multiline=False,
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.habit_progress_input = TextInput(
            hint_text="Enter your progress", size_hint_y=None, height=40, multiline=False,
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.layout.add_widget(self.new_habit_input)
        self.layout.add_widget(self.habit_progress_input)

        # 4) Add button
        self.add_button = Button(
            text="Add Habit", size_hint_y=None, height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.add_button.bind(on_press=self.add_habit)
        self.layout.add_widget(self.add_button)

        # 5) Welcome message
        self.welcome_message = Label(
            text="Welcome to your Habit Tracker!", font_size=18,
            size_hint_y=None, height=50,
            color=(0.2, 0.6, 1, 1)
        )
        self.layout.add_widget(self.welcome_message)

        # 6) Toggle Dark Mode *moved to bottom*
        self.theme_button = Button(
            text="Toggle Dark Mode", size_hint_y=None, height=40
        )
        self.theme_button.bind(on_press=self.toggle_theme)
        self.layout.add_widget(self.theme_button)

        return self.layout

    def toggle_theme(self, instance):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            Window.clearcolor = (0.1, 0.1, 0.1, 1)
            self.app_name.color = (1, 1, 1, 1)
            self.welcome_message.color = (1, 1, 1, 1)
        else:
            Window.clearcolor = (0.9, 0.9, 0.9, 1)
            self.app_name.color = (0.2, 0.6, 1, 1)
            self.welcome_message.color = (0.2, 0.6, 1, 1)
        self.update_habit_list()

    def add_habit(self, instance):
        habit = self.new_habit_input.text.strip()
        progress = self.habit_progress_input.text.strip()
        if habit and progress:
            today = datetime.now().strftime("%Y-%m-%d")
            self.habits.append({
                'habit': habit,
                'progress': progress,
                'date': today,
                'done': False,
                'streak': 1,
                'last_checked': today
            })
            self.new_habit_input.text = ""
            self.habit_progress_input.text = ""
            self.update_habit_list()

    def delete_habit(self, habit):
        if habit in self.habits:
            self.habits.remove(habit)
            self.update_habit_list()

    def on_checkbox_active(self, checkbox, value, habit):
        """Properly scoped callback for checkbox to avoid crash."""
        if value:  # only when checked
            today = datetime.now()
            last = datetime.strptime(habit['last_checked'], "%Y-%m-%d")
            delta = (today - last).days
            if delta == 1:
                habit['streak'] += 1
            elif delta > 1:
                habit['streak'] = 1
            habit['last_checked'] = today.strftime("%Y-%m-%d")
        habit['done'] = value
        self.update_habit_list()

    def update_habit_list(self):
        self.scroll_layout.clear_widgets()
        for habit in self.habits:
            container = BoxLayout(size_hint_y=None, height=60, spacing=10)
            # choose text color
            text_color = (1,1,1,1) if self.dark_mode else (0,0,0,1)
            lbl = Label(
                text=f"{habit['habit']} – {habit['progress']} "
                     f"(Date: {habit['date']}) | Streak: {habit['streak']}",
                size_hint_x=0.6, color=text_color
            )
            cb = CheckBox(active=habit['done'], size_hint_x=None, width=50)
            # bind with proper habit reference
            cb.bind(active=lambda cb_instance, val, h=habit: self.on_checkbox_active(cb_instance, val, h))
            btn = Button(text="Delete", size_hint_x=0.2)
            btn.bind(on_press=lambda inst, h=habit: self.delete_habit(h))
            container.add_widget(cb)
            container.add_widget(lbl)
            container.add_widget(btn)
            self.scroll_layout.add_widget(container)

if __name__ == "__main__":
    HabitTrackerApp().run()
