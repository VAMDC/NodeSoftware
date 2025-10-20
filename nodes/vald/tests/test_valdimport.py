import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from valdimport import FieldDef, parse_wave, batch_iterator


def test_field_def_basic():
    """Test basic FieldDef parsing"""
    field = FieldDef('test', 0, 5, float, null_values=('X', ''))

    assert field.parse("12.34") == 12.34
    assert field.parse("    X") is None
    assert field.parse("  ") is None
    print("✓ test_field_def_basic passed")


def test_field_def_string():
    """Test string FieldDef parsing"""
    field = FieldDef('term', 0, 10, str.strip)

    assert field.parse("1S    ") == "1S"
    assert field.parse("        ") is None
    print("✓ test_field_def_string passed")


def test_field_def_int():
    """Test integer FieldDef parsing"""
    field = FieldDef('species', 0, 6, int)

    assert field.parse("  2601") == 2601
    print("✓ test_field_def_int passed")


def test_parse_wave():
    """Test wavelength selection logic"""
    # Create a mock line with measured and ritz wavelengths
    line_same = "516.73290      " + "516.73290      " + "rest..."
    assert parse_wave(line_same) == 516.7329

    # Create line where measured differs from ritz
    line_diff = "516.73290      " + "517.00000      " + "rest..."
    assert parse_wave(line_diff) == 517.0
    print("✓ test_parse_wave passed")


def test_batch_iterator():
    """Test batch iterator"""
    items = list(range(25))
    batches = list(batch_iterator(items, batch_size=10))

    assert len(batches) == 3
    assert batches[0] == list(range(10))
    assert batches[1] == list(range(10, 20))
    assert batches[2] == list(range(20, 25))
    print("✓ test_batch_iterator passed")


def test_batch_iterator_empty():
    """Test batch iterator with empty input"""
    items = []
    batches = list(batch_iterator(items, batch_size=10))
    assert len(batches) == 0
    print("✓ test_batch_iterator_empty passed")


if __name__ == '__main__':
    test_field_def_basic()
    test_field_def_string()
    test_field_def_int()
    test_parse_wave()
    test_batch_iterator()
    test_batch_iterator_empty()
    print("\nAll tests passed!")
