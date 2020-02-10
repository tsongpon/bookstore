import docker

print('shutting down test environment')
docker_client = docker.from_env()
container = docker_client.containers.get("postgres-for-test")
container.stop()
container.remove()
