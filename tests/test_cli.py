import click
import json
import logging
import sys
from mlconjug3 import *
from mlconjug3 import cli
import pytest
from click.testing import CliRunner

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

class TestCLI:
    verbiste = Verbiste(language='fr')
    conjugator = Conjugator()

    def test_command_line_interface(self):
        """Test the CLI."""
        verb = 'aller'
        runner = CliRunner()
        result = runner.invoke(cli.main, [verb])
        assert result.exit_code == 0
        assert 'allassions' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        # assert 'Console script for mlconjug3.' in help_result.output

    @pytest.mark.skipif('3.5' in sys.version,
                        reason="Random TypeError('invalid file') on Python 3.5.")
    def test_save_file(self, tmpdir):
        """
        Tests file saving feature.
        """
        test_verb = self.conjugator.conjugate('aller')
        path = tmpdir.mkdir("sub").join('conjugations.json')
        verb = 'aller'
        runner = CliRunner()
        result = runner.invoke(cli.main, [verb, '-o', path])
        assert result.exit_code == 0
        my_file = Path(path)
        assert my_file.is_file()
        with open(my_file, encoding='utf-8') as file:
            output = json.load(file)
        assert output['aller'] == test_verb.conjug_info
