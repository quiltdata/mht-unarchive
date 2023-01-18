from extract import Extract
from pathlib import Path
from pytest import fixture

TEST_FILE='sample.mht'

@fixture
def ex():
	ex = Extract(TEST_FILE)
	return ex

def test_extract(ex):
	assert ex
	assert ex.html
	assert 'Brandon F' in ex.html

def test_ex_attrs(ex):
	assert ex.attrs
	keys = ex.files()
	file_name = keys[0]
	assert 'css' in file_name

	attrs = ex.attrs.get(file_name)
	assert attrs
	assert '@mhtml.blink' in attrs['uri']
	assert '@mhtml.blink' not in file_name
	assert '.css' in file_name

def test_ex_suffix(ex):
	"""every filename has a suffix"""
	for key in ex.files():
		suffix = Path(key).suffix
		assert suffix 
