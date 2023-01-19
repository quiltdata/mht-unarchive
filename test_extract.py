from extract import * 
from pathlib import Path
from pytest import fixture

TEST_FILE='sample.mht'

@fixture
def ex():
	ex = Extract(TEST_FILE)
	return ex

def test_ex_html(ex):
	assert ex
	assert ex.html
	assert 'Brandon F' in str(ex)

def test_ex_attrs(ex):
	assert ex.attrs
	keys = ex.files()
	file_name = keys[0]
	assert 'css' in file_name

	attrs = ex.attrs.get(file_name)
	assert attrs
	assert MAGIC_EXT in attrs['uri']
	assert MAGIC_EXT not in file_name
	assert '.css' in file_name

def test_ex_suffix(ex):
	"""every filename has a suffix"""
	for key in ex.files():
		suffix = Path(key).suffix
		assert suffix 

def test_ex_update_link(ex):
	keys = ex.files()
	file_name = keys[0]
	attrs = ex.attrs.get(file_name)
	uri = attrs['uri']

	assert uri in str(ex)

def test_unquote(ex):
	assert '=3D"' in ex.raw_html
	assert '=3D"' not in ex.html
