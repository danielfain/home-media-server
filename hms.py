import click
import yaml

@click.command()
@click.option("--puid", prompt="PUID")
@click.option("--pgid", prompt="PGID")
@click.option("--tz", prompt="Timezone", default="America/New_York")
@click.option("--vpn", prompt="Transmission + VPN", default="y")
@click.option("--nzbget", prompt="NZBGet", default="y")
def generate(puid, pgid, tz, vpn, nzbget):
    """Generates a docker-compose file for an automated home media server"""
    compose_file = { "version": "2", "services": {} }

    plex_service = create_service("linuxserver/plex", "plex", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz, "VERSION=docker"], [], [32400])
    jackett_service = create_service("linuxserver/jackett", "jackett", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz], [], [9117])
    sonarr_service = create_service("linuxserver/sonarr", "sonarr", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz], [], [8989])
    radarr_service = create_service("linuxserver/radarr", "radarr", ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz], [], [7878])

    if vpn == "y":
        provider = click.prompt("VPN Provider")
        port = click.prompt("Transmission port", default=9091)

        transmission_service = create_service("haugene/transmission-openvpn", 
            "transmission",
            ["PUID=" + puid, "PGID=" + pgid, "CREATE_TUN_DEVICE=true", "OPENVPN_PROVIDER=" + provider],
            [],
            [port])

    if nzbget == "y":
        port = click.prompt("NZBGet port", default=6789)

        nzbget_service = create_service("linuxserver/nzbget", 
        "nzbget", 
        ["PUID=" + puid, "PGID=" + pgid, "TZ=" + tz], 
        [],
        [port])

    compose_file["services"] = { 
        plex_service.get("container_name"): plex_service,
        jackett_service.get("container_name"): jackett_service,
        sonarr_service.get("container_name"): sonarr_service,
        radarr_service.get("container_name"): radarr_service,
        transmission_service.get("container_name"): transmission_service,
        nzbget_service.get("container_name"): nzbget_service
    }

    print(yaml.dump(compose_file))

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