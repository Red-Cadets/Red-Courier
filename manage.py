from __future__ import annotations
from tgbot.config import get_config

import uvicorn
import typer


cli = typer.Typer()

config = get_config()


@cli.command("migrate-db")
def migrate_db():
    """Apply database migrations"""
    import subprocess

    subprocess.run(("alembic", "upgrade", "head"))

@cli.command("makemigrations")
def make_db_migrations():
    """Make database migrations"""
    import subprocess

    subprocess.run(("alembic", "revision", "--autogenerate", "-m", "auto", "--head", "head"))

@cli.command("run")
def run_server(
    port: int = config.wh.port,
    host: str = "0.0.0.0",
    log_level: str = "debug",
    reload: bool = config.wh.debug,
):
    """Run the API development server(uvicorn)."""
    migrate_db()
    uvicorn.run(
        "bot:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


if __name__ == "__main__":
    cli()