from extract import Extract
from pathlib import Path

TEST_FILE='sample.mht'

def test_extract():
	ex = Extract(TEST_FILE)
	assert ex
	assert ex.html
	assert 'Brandon F' in ex.html
	assert ex.attrs
	keys = list(ex.attrs.keys())
	file_name = keys[0]
	assert 'css' in file_name

	attrs = ex.attrs.get(file_name)
	assert attrs
	assert '@mhtml.blink' in attrs['uri']
	assert '@mhtml.blink' not in file_name
	assert '.css' in file_name

	for key in keys:
		suffix = Path(key).suffix
		assert suffix # every filename has a suffix
