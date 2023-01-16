def setup_logging(logger: logging.Logger):
    pass

def conjugate_verbs(verbs: List[str], language:str, subject:str) -> Dict[str, Dict[str, str]]:
    pass

def write_conjugations_to_file(results: Dict[str, Dict[str, str]], output:str):
    pass

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('verbs', nargs=-1)
@click.option('-l', '--language',
              default='fr',
              help=_("The language for the conjugation pipeline."
                     " The values can be 'fr', 'en', 'es', 'it', 'pt' or 'ro'."
                     " The default value is fr."),
              type=click.STRING)
@click.option('-o', '--output',
              default=None,
              help=_("Path of the filename for storing the conjugation tables."),
              type=click.STRING)
@click.option('-s', '--subject',
              default='abbrev',
              help=_("The subject format type for the conjugated forms."
                     " The values can be 'abbrev' or 'pronoun'. The default value is 'abbrev'."),
              type=click.STRING)
def main(verbs: Tuple[str], language:str, output:str, subject:str):
    pass
