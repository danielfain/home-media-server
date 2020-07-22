from PyInquirer import prompt, print_json, Separator
import yaml
import os

def generate_compose_file(answers):
    """Generates the Docker Compose file from PyInquirer's answers"""
    print_json(answers)
    return

    compose_file = { 'version': '2', 'services': {} }

    puid = answers["puid"]
    pgid = answers["pgid"]
    tz = answers["tz"]

    plex_service = create_service('linuxserver/plex', 
        'plex', 
        ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz, "VERSION=docker"], 
        media_vols, 
        [32400])

    compose_file["services"]["plex"] = plex_service

    file = open("docker-compose.yml", "w")
    file.write(yaml.dump(compose_file))
    file.close()

def create_service(image_name, container_name, env, volumes, ports):
    """Creates a template for a docker compose service"""
    return {
        "image": image_name,
        "container_name": container_name,
        "environment": env,
        "volumes": volumes,
        "ports": ["{}:{}".format(p, p) for p in ports],
        "restart": "always"
    }

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
        'name': 'tz',
        'message': 'What timezone are you in?',
        'default': 'America/New_York',
    },
    {
        'type': 'input',
        'name': 'config_path',
        'message': 'What is the absolute path to the directory where all config files will be?',
        'validate': lambda answer: os.path.exists(answer) or 'Please enter a valid directory path.',
    },
    {
        'type': 'checkbox',
        'name': 'services',
        'message': 'Select services',
        'choices': [
            Separator('= Media Server ='),
            {
                'name': 'Plex'
            },
            Separator('= Media Downloaders ='),
            {
                'name': 'Transmission (w/ OpenVPN)'
            },
            {
                'name': 'NZBGet'
            },
            Separator('= Automated Media ='),
            {
                'name': 'Sonarr'
            },
            {
                'name': 'Radarr'
            },
            Separator('= Indexers ='),
            {
                'name': 'Jackett'
            },
        ],
        'validate': lambda answer: 'You must choose at least one service.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'num_media_volumes',
        'message': 'How many media volumes do you have for Plex?',
        'validate': lambda answer: answer.isdigit() or 'Please enter an integer.',
        'when': lambda answers: 'Plex' in answers['services']
    },
]

if __name__ == "__main__":
    answers = prompt(questions)
    generate_compose_file(answers)