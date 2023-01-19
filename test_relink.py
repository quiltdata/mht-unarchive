from extract import Extract
from relink import *

from pathlib import Path
from pytest import fixture

TEST_FILE='sample.mht'

@fixture
def rel():
	ex = Extract(TEST_FILE)
	_rel = relink(ex, REVIEWER)
	return _rel

def test_rel(rel):
	assert rel

