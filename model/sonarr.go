package model

import "log"

// CreateSonarrConfig generates a Docker-Compose service in YAML
func CreateSonarrConfig() {
	sonarrService := Service{
		Image:         "linuxserver/sonarr",
		ContainerName: "sonarr",
		Environment: Environment{
			Variables: make(map[string]string),
		},
	}

	log.Println(sonarrService.Image)
}
