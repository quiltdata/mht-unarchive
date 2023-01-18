from extract import Extract
TEST_FILE='sample.mht'

def test_extract():
	ex = Extract(TEST_FILE)
	assert ex
	assert ex.html
	assert 'Brandon F' in ex.html
	assert ex.attrs
	keys = list(ex.attrs.keys())
	k1 = keys[0]
	assert 'css' in k1

	attrs = ex.attrs.get(k1)
	assert attrs
	#print(attrs)
	#assert False
