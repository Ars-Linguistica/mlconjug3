import click
import json
import logging
import sys
from mlconjug3 import *

def test_main(mocker):
    mock_conjugator = mocker.Mock(spec=Conjugator)
    mock_conjugator.conjugate.return_value = 'conjugated_verb'
    mocker.patch('conjugator.Conjugator', return_value=mock_conjugator)
    mock_open = mocker.mock_open()
    mocker.patch('builtins.open', mock_open)

    # create a test CLI runner
    runner = click.testing.CliRunner()
    # invoke the command with different input
    result = runner.invoke(main, ['verb'], obj={})
    assert result.exit_code == 0
    assert result.output == "conjugated_verb\n"
    result = runner.invoke(main, ['verb', '-l', 'en'], obj={})
    assert result.exit_code == 0
    assert result.output == "conjugated_verb\n"
    result = runner.invoke(main, ['verb', '-o', 'output.json'], obj={})
    assert result.exit_code == 0
    assert result.output == "The conjugations have been succesfully saved to output.json.\n"
    assert mock_open.called
    mock_open().write.assert_called_once_with('{"verb": "conjugated_verb"}')
