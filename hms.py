from PyInquirer import prompt, print_json, Separator
import yaml
import os

def generate_compose_file(answers):
    """Generates the Docker Compose file from PyInquirer's answers"""
    print(answers)
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

default_questions = [
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
]

def ask_plex():
    answers = {}

    if 'Plex' in default_answers['services']:
        num_media = prompt({
            'type': 'input',
            'name': 'num_media_vols',
            'message': 'How many media volumes do you have for Plex?',
            'validate': lambda answer: answer.isdigit() or 'Please enter an integer.',
        })

        answers['num_media_vols'] = num_media['num_media_vols']
        answers['media_vols'] = []

        for i in range(int(num_media['num_media_vols'])):
            media_path = prompt({
                'type': 'input',
                'name': 'path',
                'message': 'What is the absolute path for media volume ' + str(i + 1) + '?',
                'validate': lambda answer: os.path.exists(answer) or 'Please enter a valid directory path.',
            })
            answers.get('media_vols').append(media_path['path'])

    return answers

def ask_transmission():
    answers = {}

    if 'Transmission (w/ OpenVPN)' in default_answers['services']:
        transmission_questions = [
            {
            'type': 'input',
            'name': 'transmission_port',
            'message': 'Which port should Transmission be on?',
            'default': '9091',
            'validate': lambda answer: answer.isdigit() or 'Please enter an integer.',
            },
            {
            'type': 'input',
            'name': 'vpn_provider',
            'message': 'Who is your VPN provider?',
            'default': 'PIA',
            # 'validate': TODO import list of supported providers and check here
            },
            {
            'type': 'input',
            'name': 'vpn_config',
            'message': 'Which location for your VPN?',
            # 'validate': TODO import list of configs and check here
            },
            {
            'type': 'input',
            'name': 'vpn_username',
            'message': 'What is your username for your VPN?',
            },
            {
            'type': 'password',
            'name': 'vpn_password',
            'message': 'What is your password for your VPN?',
            },
            {
            'type': 'input',
            'name': 'local_network',
            'message': 'What is your LAN subnet?',
            'default': '192.168.1.0/24',
            },
        ]
        answers = prompt(transmission_questions)

    return answers

def ask_nzbget():
    answers = {}

    if 'NZBGet' in default_answers['services']:
        nzbget_questions = [
            {
            'type': 'input',
            'name': 'nzbget_port',
            'message': 'Which port should NZBGet be on?',
            'default': '6789',
            'validate': lambda answer: answer.isdigit() or 'Please enter an integer.',
            },
        ]
        answers = prompt(nzbget_questions)

    return answers

def ask_sonarr():
    answers = {}

    if 'Sonarr' in default_answers['services']:
        sonarr_questions = [
            {
            'type': 'input',
            'name': 'sonarr_port',
            'message': 'Which port should Sonarr be on?',
            'default': '8989',
            'validate': lambda answer: answer.isdigit() or 'Please enter an integer.',
            },
            {
            'type': 'input',
            'name': 'tv_path',
            'message': 'Which directory from your media volume(s) contain your TV shows?',
            'validate': lambda answer: os.path.exists(answer) or 'Please enter a valid directory path.',
            },
        ]
        answers = prompt(sonarr_questions)

    return answers

def ask_radarr():
    answers = {}

    if 'Radarr' in default_answers['services']:
        radarr_questions = [
            {
            'type': 'input',
            'name': 'radarr_port',
            'message': 'Which port should Radarr be on?',
            'default': '7878',
            'validate': lambda answer: answer.isdigit() or 'Please enter an integer.',
            },
            {
            'type': 'input',
            'name': 'movie_path',
            'message': 'Which directory from your media volume(s) contain your movies?',
            'validate': lambda answer: os.path.exists(answer) or 'Please enter a valid directory path.',
            },
        ]
        answers = prompt(radarr_questions)

    return answers

def ask_jackett():
    answers = {}

    if 'Jackett' in default_answers['services']:
        jackett_questions = [
            {
            'type': 'input',
            'name': 'jackett_port',
            'message': 'Which port should Jackett be on?',
            'default': '9117',
            'validate': lambda answer: answer.isdigit() or 'Please enter an integer.',
            },
        ]
        answers = prompt(jackett_questions)

    return answers

if __name__ == "__main__":
    default_answers = prompt(default_questions)        
    plex_answers = ask_plex()
    transmission_answers = ask_transmission()
    nzbget_answers = ask_nzbget()
    sonarr_answers = ask_sonarr()
    radarr_answers = ask_radarr()
    jackett_answers = ask_jackett()

    answers = {**default_answers, **plex_answers, **transmission_answers, **nzbget_answers, **sonarr_answers, **radarr_answers, **jackett_answers} # merges dicts

    generate_compose_file(answers)