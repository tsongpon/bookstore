import docker
import socket
from contextlib import closing
import os


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


print('preparing environment for testing, be patient')
docker_client = docker.from_env()
env = {
    "POSTGRES_PASSWORD": "pingu123",
    "POSTGRES_DB": "bookstore"
}
db_port = os.getenv('DB_PORT')
port_env = {'5432/tcp': str(db_port)}
docker_client.containers.run("postgres:9", environment=env, detach=True, ports=port_env, name='postgres-for-test')
container = docker_client.containers.get('postgres-for-test')
