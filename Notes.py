import json
import os
from datetime import datetime

class Note:
    def __init__(self, id, title, message, timestamp):
        self.id = id
        self.title = title
        self.message = message
        self.timestamp = timestamp

class NotesApp:
    def __init__(self, file_path='notes.json'):
        self.file_path = file_path
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                notes_data = json.load(file)
                self.notes = [Note(**note) for note in notes_data]

    def save_notes(self):
        notes_data = [{'id': note.id, 'title': note.title, 'message': note.message, 'timestamp': note.timestamp}
                      for note in self.notes]
        with open(self.file_path, 'w') as file:
            json.dump(notes_data, file)

    def add_note(self, title, message):
        note_id = len(self.notes) + 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_note = Note(id=note_id, title=title, message=message, timestamp=timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print('Заметка успешно сохранена.')

    def list_notes(self, filter_date=None):
        for note in self.notes:
            if filter_date is None or note.timestamp.startswith(filter_date):
                print(f'ID: {note.id}, Заголовок: {note.title}, Дата/время: {note.timestamp}')
                print(f'Тело заметки: {note.message}\n')

    def edit_note(self, note_id, title, message):
        for note in self.notes:
            if note.id == note_id:
                note.title = title
                note.message = message
                note.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                print('Заметка успешно отредактирована.')
                return
        print('Заметка с указанным ID не найдена.')

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()
        print('Заметка успешно удалена.')

if __name__ == '__main__':
    app = NotesApp()

    while True:
        print('\nСписок команд:')
        print('1 - добавить заметку')
        print('2 - просмотреть список заметок')
        print('3 - редактировать заметку')
        print('4 - удалить заметку')
        print('0 - выход из программы')

        print('\nВведите номер команды:')
        command = input('> ')

        if command == '1':
            title = input('Введите заголовок заметки: ')
            message = input('Введите тело заметки: ')
            app.add_note(title, message)

        elif command == '2':
            filter_date = input('Введите дату (гггг-мм-дд) для фильтрации (или нажмите Enter для вывода всех заметок): ')
            app.list_notes(filter_date)

        elif command == '3':
            note_id = int(input('Введите ID заметки для редактирования: '))
            title = input('Введите новый заголовок заметки: ')
            message = input('Введите новое тело заметки: ')
            app.edit_note(note_id, title, message)

        elif command == '4':
            note_id = int(input('Введите ID заметки для удаления: '))
            app.delete_note(note_id)

        elif command == '0':
            break

        else:
            print('Неверный номер команды. Пожалуйста, введите корректный номер команды (1, 2, 3, 4, 0).')
