from pathlib import Path

from fabric import Connection

BASE_DIR = Path(__file__).resolve().parent.parent.parent

HOST = ...
USER = "ubuntu"
PRIVATE_KEY_PATH = BASE_DIR / "aws" / ...
GITHUB_REPO_SUFFIX = ...
GITHUB_REPO_TOKEN = ...
GITHUB_REPO_NAME = ...

c = Connection(
    host=HOST,
    user=USER,
    connect_kwargs={"key_filename": str(PRIVATE_KEY_PATH)},
)
print("Starting Deploy script...")
if c.run(f"test -d {GITHUB_REPO_NAME}", warn=True).failed:
    c.run(f"git clone https://oauth:{GITHUB_REPO_TOKEN}@github.com/{GITHUB_REPO_SUFFIX}")

with c.cd("Bridge-Web"):
    c.run("git pull")
    c.run("sudo docker-compose -f production.yml build --progress=plain")
    c.run("sudo docker-compose -f production.yml down")
    c.run("sudo docker-compose -f production.yml up -d")
