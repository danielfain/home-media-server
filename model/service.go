package model

// Service is a docker-compose service in YAML
type Service struct {
	Image         string
	ContainerName string `yaml:"container_name"`
	Environment   Environment
	Volumes       struct{}
	Ports         struct{}
	Restart       string
}

// Environment is where all environment variables are stored
type Environment struct {
	Variables map[string]string
}

type Volumes struct {
}
