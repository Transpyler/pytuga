import pytest
import pytuga.keywords as keywords

def test_iskeyword():
	k = 'is'
	assert type(keywords.iskeyword(k)) is bool

