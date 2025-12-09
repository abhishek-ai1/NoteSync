import os
from pathlib import Path

# Define folder structure
structure = {
    "notesync": {
        "backend": {
            "app": {
                "models": {},
                "routes": {},
                "websocket": {},
                "services": {},
                "auth": {},
                "_files": ["main.py"]
            },
            "_files": ["requirements.txt", "Dockerfile"]
        },
        "frontend": {
            "src": {},
            "_files": ["package.json", "Dockerfile"]
        },
        "_files": ["docker-compose.yml"],
        "k8s": {
            "_files": [
                "backend-deploy.yaml",
                "frontend-deploy.yaml",
                "mongo.yaml",
                "redis.yaml",
                "ingress.yaml"
            ]
        }
    }
}

def create_structure(base, structure):
    """Recursively create folders and files."""
    for name, content in structure.items():
        if name == "_files":
            # Create each file inside base directory
            for file in content:
                file_path = Path(base) / file
                file_path.touch(exist_ok=True)
        else:
            # Create folder and recurse
            dir_path = Path(base) / name
            dir_path.mkdir(parents=True, exist_ok=True)
            create_structure(dir_path, content)

# Run the creation
create_structure(".", structure)
print("Folder structure created successfully.")