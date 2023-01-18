from extract import Extract
TEST_FILE='sample.mht'

def test_extract():
	ex = Extract(TEST_FILE)
	assert ex