import os
from pathlib import Path

# Define backend folder structure
structure = {
    "notesync": {
        "backend": {
            "app": {
                "routers": {
                    "_files": ["auth_router.py", "notes_router.py"]
                },
                "_files": [
                    "main.py",
                    "config.py",
                    "db.py",
                    "models.py",
                    "schemas.py",
                    "auth.py",
                    "crud.py",
                    "websocket_mgr.py"
                ]
            },
            "_files": ["requirements.txt", "Dockerfile"]
        }
    }
}

def create_structure(base, structure):
    """Recursively create folders and files."""
    for name, content in structure.items():
        if name == "_files":
            for file in content:
                file_path = Path(base) / file
                file_path.touch(exist_ok=True)
        else:
            dir_path = Path(base) / name
            dir_path.mkdir(parents=True, exist_ok=True)
            create_structure(dir_path, content)

# Run the script
create_structure(".", structure)
print("Backend folder structure created successfully.")
