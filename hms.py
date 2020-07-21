import click
import yaml

@click.command()
@click.option("--puid", prompt="PUID", type=int)
@click.option("--pgid", prompt="PGID", type=int)
@click.option("--tz", prompt="Timezone", default="America/New_York", type=str)
@click.option("--config-path", prompt="Absolute path to config folder", type=str)
def generate(puid, pgid, tz, config_path):
    """Generates a docker-compose file for an automated home media server"""
    compose_file = { "version": "2", "services": {} }

    num_volumes = click.prompt("Number of media volumes for Plex", default=1, type=int)

    media_vols = []

    for i in range(num_volumes):
        volume_path = click.prompt("Absolute path of media volume " + str(i + 1), type=str)
        media_vols.append(volume_path + ":/Media" + str(i + 1))

    media_vols.append("{}/plex:/config".format(config_path))
    media_vols.append(config_path + "/plex/transcode:/transcode")

    plex_service = create_service("linuxserver/plex", 
        "plex", 
        ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz, "VERSION=docker"], 
        media_vols, 
        [32400])

    compose_file["services"]["plex"] = plex_service

    if click.prompt("Transmission + VPN", default="y", type=str) == "y":
        print("----TRANSMISSION SETUP----")
        provider = click.prompt("VPN Provider", type=str)
        port = click.prompt("Port", default=9091, type=int)

        transmission_service = create_service("haugene/transmission-openvpn", 
            "transmission",
            ["PUID=" + str(puid), "PGID=" + str(pgid), "CREATE_TUN_DEVICE=true", "OPENVPN_PROVIDER=" + provider],
            ["{}/transmission/downloads:/downloads".format(config_path)],
            [port])

        transmission_service["cap_add"] = "NET_ADMIN"
            
        compose_file["services"]["transmission"] = transmission_service

        print("--------------------------")

    if click.prompt("NZBGet", default="y", type=str) == "y":
        print("-------NZBGET SETUP-------")
        port = click.prompt("Port", default=6789, type=int)

        nzbget_service = create_service("linuxserver/nzbget", 
            "nzbget", 
            ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz], 
            ["{}/nzbget:/config".format(config_path), 
            "{}/nzbget/downloads:/downloads".format(config_path)],
            [port])

        compose_file["services"]["nzbget"] = nzbget_service

        print("--------------------------")

    if click.prompt("Sonarr", default="y", type=str) == "y":
        print("-------SONARR SETUP-------")
        port = click.prompt("Port", default=8989, type=int)

        sonarr_service = create_service("linuxserver/sonarr", 
            "sonarr", 
            ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz], 
            ["{}/sonarr:/config".format(config_path), 
            "{}/transmission/downloads:/torrents".format(config_path),
            "{}/nzbget/downloads:/nzbs".format(config_path)],
            [port])
        
        compose_file["services"]["sonarr"] = sonarr_service

        print("--------------------------")

    if click.prompt("Radarr", default="y", type=str) == "y":
        print("-------RADARR SETUP-------")
        port = click.prompt("Port", default=7878, type=int)

        radarr_service = create_service("linuxserver/radarr", 
            "radarr", 
            ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz], 
            ["{}/radarr:/config".format(config_path),
            "{}/transmission/downloads:/torrents".format(config_path),
            "{}/nzbget/downloads:/nzbs".format(config_path)],
            [port])

        compose_file["services"]["radarr"] = radarr_service

        print("--------------------------")

    if click.prompt("Jackett", default="y", type=str) == "y":
        print("------JACKETT SETUP-------")
        port = click.prompt("Port", default=9117, type=int)

        jackett_service = create_service("linuxserver/jackett", 
            "jackett", 
            ["PUID=" + str(puid), "PGID=" + str(pgid), "TZ=" + tz], 
            ["{}/jackett:/config".format(config_path)],
            [port])

        compose_file["services"]["jackett"] = jackett_service

        print("--------------------------")

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