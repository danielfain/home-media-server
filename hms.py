import click
import yaml

@click.command()
@click.option("--puid", prompt="PUID", type=int)
@click.option("--pgid", prompt="PGID", type=int)
@click.option("--tz", prompt="Timezone", default="America/New_York")
def generate(puid, pgid, tz):
    """Generates a docker-compose file for an automated home media server"""
    compose_file = { "version": "2", "services": {} }

    plex_service = create_service("linuxserver/plex", "plex", ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz, "VERSION=docker"], [], [32400])
    jackett_service = create_service("linuxserver/jackett", "jackett", ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz], [], [9117])
    sonarr_service = create_service("linuxserver/sonarr", "sonarr", ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz], [], [8989])
    radarr_service = create_service("linuxserver/radarr", "radarr", ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz], [], [7878])

    if click.prompt("Transmission + VPN", default="y", type=str) == "y":
        print("----TRANSMISSION SETUP----")
        provider = click.prompt("VPN Provider", type=str)
        port = click.prompt("Transmission port", default=9091, type=int)

        transmission_service = create_service("haugene/transmission-openvpn", 
            "transmission",
            ["PUID=" + str(puid), "PGID=" + str(pgid), "CREATE_TUN_DEVICE=true", "OPENVPN_PROVIDER=" + provider],
            [],
            [port])
        print("--------------------------")

    if click.prompt("NZBGet", default="y", type=str) == "y":
        print("----NZBGET SETUP----")
        port = click.prompt("NZBGet port", default=6789, type=int)

        nzbget_service = create_service("linuxserver/nzbget", 
        "nzbget", 
        ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz], 
        [],
        [port])
        print("--------------------------")

    compose_file["services"] = { 
        plex_service.get("container_name"): plex_service,
        jackett_service.get("container_name"): jackett_service,
        sonarr_service.get("container_name"): sonarr_service,
        radarr_service.get("container_name"): radarr_service,
        transmission_service.get("container_name"): transmission_service,
        nzbget_service.get("container_name"): nzbget_service
    }

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

if __name__ == "__main__":
    generate()