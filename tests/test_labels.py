import sys; sys.path.insert(0, '.')
import numpy as np
from ml.fix_labels import extract_number, fix_labels


def test_extract_number_simple():
    assert extract_number('alien_3') == 3


def test_extract_number_with_zeros():
    assert extract_number('class_03') == 3


def test_extract_number_uppercase():
    assert extract_number('CLS-12') == 12


def test_fix_labels_starts_from_zero():
    labels = ['alien_5', 'alien_2', 'alien_8']
    fixed, mapping = fix_labels(labels)
    assert min(fixed) == 0


def test_fix_labels_contiguous():
    labels = ['a_10', 'a_20', 'a_30']
    fixed, _ = fix_labels(labels)
    assert sorted(set(fixed.tolist())) == [0, 1, 2]


def test_fix_labels_count():
    labels = ['x_1', 'x_1', 'x_2']
    fixed, _ = fix_labels(labels)
    assert list(fixed).count(0) == 2
