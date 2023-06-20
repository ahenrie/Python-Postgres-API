import subprocess

def create_postgres_container():
# Start the PostgreSQL container using Docker Compose
    subprocess.run(['docker-compose', 'up', '-d'])

def destroy_container():
# Stop and remove the PostgreSQL container using Docker Compose
    subprocess.run(['docker-compose', 'down'])
