from helper import *

def test_main_help():
  actual = call_main_with('--help')

  assert actual[0] is 0,       '--help should exit zero'
  assert 'Usage' in actual[1], '--help should print Usage to stdout'
  assert actual[2] is None,    '--help should not print stderr'

def test_main_with_nothing():
  actual = call_main_with()

  assert actual[0] is not 0,   'main should exit non-zero when no subcommand is given'
  assert 'Usage' in actual[1], 'main should print Usage to stdout when no subcommand is given'
  assert actual[2] is None,    'main should not print stderr when no subcommand is given'

def test_main_with_nothing():
  actual = call_main_with('--nope')

  assert actual[0] is not 0,   'main should exit non-zero when an unknown subcommand is given'
  assert actual[1] is None,    'main should not print stdout when an unknown subcommand is given'
  assert 'Usage' in actual[2], 'main should print Usage to stderr when an unknown subcommand is given'
