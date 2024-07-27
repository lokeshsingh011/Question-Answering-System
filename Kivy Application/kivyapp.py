from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import requests

class QAApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.question_input = TextInput(hint_text='Enter your question', size_hint_y=None, height=40)
        self.context_input = TextInput(hint_text='Enter context', size_hint_y=None, height=100)
        self.result_label = Label(text='Answer will appear here', size_hint_y=None, height=40)

        submit_button = Button(text='Submit', size_hint_y=None, height=40)
        submit_button.bind(on_press=self.submit_question)


        layout.add_widget(self.context_input)
        layout.add_widget(self.question_input)
        layout.add_widget(submit_button)
        layout.add_widget(self.result_label)

        return layout

    def submit_question(self, instance):
        question = self.question_input.text
        context = self.context_input.text

        if not question or not context:
            self.show_popup('Error', 'Both question and context are required.')
            return

        try:
            response = requests.post('http://127.0.0.1:8000/qa/', json={
                'question': question,
                'context': context
            })

            if response.status_code == 200:
                answer = response.json().get('answer', 'No answer found')
                self.result_label.text = f'Answer: {answer}'
            else:
                self.show_popup('Error', f'Error fetching answer from server. Status Code: {response.status_code}')

        except requests.RequestException as e:
            self.show_popup('Error', f'Error: {str(e)}')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    QAApp().run()
