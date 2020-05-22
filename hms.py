import click
import yaml

@click.command()
@click.option("--puid", prompt="PUID for containers", help="The PUID of the user to run docker container from")
@click.option("--pgid", prompt="PGID for containers", help="The PGID of the user to run docker container from (usually docker group id)")
@click.option("--tz", prompt="Timezone for containers (America/New_York) format", help="The timezone to set the docker containers to (America/New_York)")
def generate(puid, pgid, tz):
    """Generates a docker-compose file for an automated home media server"""
    compose_file = { "version": "2", "services": {} }

    plex_service = create_service("linuxserver/plex", "plex", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz, "VERSION=docker"], [])
    jackett_service = create_service("linuxserver/jackett", "jackett", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz], [])
    sonarr_service = create_service("linuxserver/sonarr", "sonarr", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz], [])
    radarr_service = create_service("linuxserver/radarr", "radarr", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz], [])
    transmission_service = create_service("haugene/transmission-openvpn", "transmission", ["PUID=" + puid, "PGID=" + pgid], [])
    nzbget_service = create_service("linuxserver/nzbget", "nzbget", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz], [])

    compose_file["services"] = { 
        plex_service.get("container_name"): plex_service,
        jackett_service.get("container_name"): jackett_service,
        sonarr_service.get("container_name"): sonarr_service,
        radarr_service.get("container_name"): radarr_service,
        transmission_service.get("container_name"): transmission_service,
        nzbget_service.get("container_name"): nzbget_service
    }

    print(yaml.dump(compose_file))

def create_service(image_name, container_name, env, volumes):
    """Creates a template for a docker compose service"""
    return {
        "image": image_name,
        "container_name": container_name,
        "environment": env,
        "volumes": volumes,
        "restart": "always"
    }


if __name__ == "__main__":
    generate()