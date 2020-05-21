import click
import yaml

@click.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
def generate():
    """Generates a docker-compose file for an automated home media server"""
    with open(r'docker-compose.yml') as file:
        boilerplate = yaml.load(file, Loader=yaml.SafeLoader)
        print(boilerplate['services'])

if __name__ == "__main__":
    generate()