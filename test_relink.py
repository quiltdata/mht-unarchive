from extract import Extract
from relink import *
#from test_extract import ANCHOR

from pathlib import Path
from pytest import fixture

TEST_MHT='sample.mhtml'
TEST_ANCHOR='jss5'

@fixture
def soup():
	ex = Extract(TEST_MHT)
	rel = relink(ex, TEST_ANCHOR)
	return ex.soup

def test_rel(soup):
	assert soup

def untest_toc(soup):
	print(RID_TOC)
	toc = soup.find(id=RID_TOC)
	#print(soup.prettify())
	assert toc
	assert 'List' in str(toc)
	assert RID in toc['id']
	assert len(toc.contents) > 1
	olist = toc.contents[1]
	item = olist.contents[0]
	anchor = item.contents[0]
	assert anchor
	assert RID in anchor['href']

def test_div(soup):
	sib = soup.find(class_=RID_PARENT)
	print(str(soup.body.div.div.div)[500:1000])
	#assert sib
	#assert sib['class']
	#assert RID_PARENT in sib['class']

def untest_ex_get(ex):
	PREFIX="PRComment"
	result = ex.get_all('b', string='User F')
	assert result
	assert len(result) == 41
	tag = result[0]
	n = 1
	tag['id'] = f'{PREFIX}_{n:03}'
	tag.string = f'{PREFIX} #{n:03}. {tag.string}'
	assert 'Comment_001' in str(tag)
	assert 'Comment_001' in str(ex)
