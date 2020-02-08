"""
This module contains tests for the xmltree.py module
"""
import pytest
import xmltree as xt


def test_make_dict_from_tree():
    """
    Ensures that the output is as expected
    """
    xml = open('xmlexample.xml').read()
    returned = xt.make_dict_from_tree(xml)
    assert isinstance(returned, dict)

