"""Command-line interface for cc."""

from __future__ import annotations

import json
import os
import shutil
from typing import Optional

import requests
import typer
from dotenv import load_dotenv

from . import __version__

load_dotenv()

app = typer.Typer(help="cc command-line interface")

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_MISSING = 2
EXIT_TIMEOUT = 3
EXIT_NETWORK = 4
EXIT_AUTH = 5
EXIT_INTERNAL = 10


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit(code=EXIT_OK)


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    return


@app.command()
def env(json_: bool = typer.Option(False, "--json", help="Output JSON")) -> None:
    """Afficher les variables d'environnement utiles."""
    data = {"API_BASE": os.environ.get("API_BASE", "")}
    if json_:
        typer.echo(json.dumps(data))
    else:
        for k, v in data.items():
            typer.echo(f"{k}={v}")


@app.command()
def check(json_: bool = typer.Option(False, "--json", help="Output JSON")) -> None:
    """Verifier les prerequis."""
    docker = shutil.which("docker") is not None
    if docker:
        msg = "Docker OK"
        code = EXIT_OK
    else:
        msg = "Docker absent"
        code = EXIT_MISSING
    if json_:
        typer.echo(json.dumps({"docker": docker, "message": msg}))
    else:
        typer.echo(msg)
    raise typer.Exit(code=code)


@app.command()
def ping(timeout: float = typer.Option(5.0, help="Delai en secondes")) -> None:
    """Tester la disponibilite de l'API."""
    api_base = os.environ.get("API_BASE")
    if not api_base:
        typer.echo("pong")
        raise typer.Exit(code=EXIT_OK)
    url = api_base.rstrip("/") + "/healthz"
    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.Timeout:
        typer.echo("timeout")
        raise typer.Exit(code=EXIT_TIMEOUT)
    except requests.exceptions.RequestException:
        typer.echo("erreur reseau")
        raise typer.Exit(code=EXIT_NETWORK)
    if response.status_code == 401:
        typer.echo("erreur authentification")
        raise typer.Exit(code=EXIT_AUTH)
    if response.status_code >= 400:
        typer.echo(f"erreur {response.status_code}")
        raise typer.Exit(code=EXIT_INTERNAL)
    typer.echo("pong")
    raise typer.Exit(code=EXIT_OK)


if __name__ == "__main__":
    app()
