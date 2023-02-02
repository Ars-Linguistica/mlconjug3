import sys
import os
import click
from .mlconjug import Conjugator
import json
import tomlkit
import yaml
import logging
import rich
from textual import Terminal

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main() -> None:
    ...

def load_config(config_file: str) -> dict:
    ...
