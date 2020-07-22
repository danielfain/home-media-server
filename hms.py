from PyInquirer import prompt, print_json
import yaml
import os

questions = [
    {
        'type': 'input',
        'name': 'puid',
        'message': 'What is your PUID?',
        'validate': lambda answer: answer.isdigit() or 'Your PUID should be an integer.',
    },
    {
        'type': 'input',
        'name': 'pgid',
        'message': 'What is your PGID?',
        'validate': lambda answer: answer.isdigit() or 'Your PGID should be an integer.',
    },
    {
        'type': 'input',
        'name': 'timezone',
        'message': 'What timezone are you in?',
        'default': 'America/New_York',
    },
    {
        'type': 'input',
        'name': 'config_path',
        'message': 'What is the absolute path to the directory where all config files will be?',
        'validate': lambda answer: os.path.exists(answer) or 'Please enter a valid directory path.',
    },
]

if __name__ == "__main__":
    answers = prompt(questions)
    print_json(answers)