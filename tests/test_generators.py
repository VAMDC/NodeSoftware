# coding: utf-8
"""
Comprehensive tests for vamdctap/generators.py

This test suite probes each function with various inputs including:
- Normal cases
- Edge cases (None, empty, zero values)
- Boundary conditions
- Error conditions
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from collections.abc import Iterable
import six


# Mock Django and node modules before any imports
mock_dicts = MagicMock()
mock_dicts.RETURNABLES = {
    'NodeID': 'TestNode',
    'XSAMSVersion': '1.0',
    'SchemaLocation': 'http://test.com/schema',
}

# Create a proper mock settings object
mock_settings = type('Settings', (), {'NODEPKG': 'node'})()

# Create mock django.conf module
mock_django_conf = MagicMock()
mock_django_conf.settings = mock_settings

# Pre-populate sys.modules with mocks
sys.modules['django'] = MagicMock()
sys.modules['django.conf'] = mock_django_conf
sys.modules['node'] = MagicMock()
sys.modules['node.dictionaries'] = mock_dicts

# Now we can import from vamdctap.generators
from vamdctap.generators import (
    isiterable, makeiter, makeloop, GetValue,
    makeOptionalTag, makeSourceRefs, makePrimaryType,
    makeReferencedTextType, makeRepeatedDataType,
    makeAccuracy, makeEvaluation, makeDataType,
    makeArgumentType, makeParameterType, checkXML,
    parityLabel, makeDataSeriesAccuracyType,
    makePartitionfunc, makeTermType, makeShellType,
    makeBroadeningType, makeDataSeriesType,
)


class TestIsIterable:
    """Test the isiterable lambda function"""

    def test_string_not_iterable(self):
        assert not isiterable("string")
        assert not isiterable("")
        assert not isiterable(u"unicode")

    def test_list_is_iterable(self):
        assert isiterable([1, 2, 3])
        assert isiterable([])

    def test_tuple_is_iterable(self):
        assert isiterable((1, 2, 3))
        assert isiterable(())

    def test_dict_is_iterable(self):
        assert isiterable({'a': 1})

    def test_number_not_iterable(self):
        assert not isiterable(42)
        assert not isiterable(3.14)
        assert not isiterable(0)

    def test_none_not_iterable(self):
        assert not isiterable(None)


class TestMakeiter:
    """Test the makeiter function"""

    def test_none_with_n_zero(self):
        result = makeiter(None)
        assert result == []

    def test_none_with_n_positive(self):
        result = makeiter(None, 3)
        assert result == [None, None, None]

    def test_empty_string_with_n_zero(self):
        result = makeiter("")
        assert result == []

    def test_empty_string_with_n_positive(self):
        result = makeiter("", 2)
        assert result == [None, None]

    def test_zero_value_with_n_zero(self):
        # Zero should be treated as valid value, not empty
        result = makeiter(0)
        assert result == [0]

    def test_zero_value_with_n_positive(self):
        result = makeiter(0, 3)
        assert result == [0, 0, 0]

    def test_scalar_with_n_zero(self):
        result = makeiter(42)
        assert result == [42]

    def test_scalar_with_n_positive(self):
        result = makeiter("test", 3)
        assert result == ["test", "test", "test"]

    def test_list_unchanged(self):
        input_list = [1, 2, 3]
        result = makeiter(input_list)
        assert result == input_list

    def test_tuple_unchanged(self):
        input_tuple = (1, 2, 3)
        result = makeiter(input_tuple)
        assert result == input_tuple

    def test_false_value(self):
        # False is a valid boolean value, should be preserved
        result = makeiter(False)
        assert result == [False]

    def test_false_value_with_n(self):
        # False is a valid boolean value, should be replicated
        result = makeiter(False, 2)
        assert result == [False, False]


class TestMakeloop:
    """Test the makeloop function"""

    def test_no_args(self):
        G = Mock(return_value="value")
        result = makeloop("Base", G)
        assert result == []

    def test_single_arg(self):
        G = Mock(side_effect=lambda key: [1, 2, 3] if key == "BaseName" else None)
        result = makeloop("Base", G, "Name")
        assert result == [[1, 2, 3]]

    def test_multiple_args_equal_length(self):
        def mock_g(key):
            if key == "BaseName":
                return ["A", "B", "C"]
            elif key == "BaseValue":
                return [1, 2, 3]
            return None

        G = Mock(side_effect=mock_g)
        result = makeloop("Base", G, "Name", "Value")
        assert result == [["A", "B", "C"], [1, 2, 3]]

    def test_multiple_args_unequal_length(self):
        def mock_g(key):
            if key == "BaseName":
                return ["A", "B", "C"]
            elif key == "BaseValue":
                return [1, 2]  # Shorter list
            return None

        G = Mock(side_effect=mock_g)
        result = makeloop("Base", G, "Name", "Value")
        # Third element of Value should be empty string due to exception
        assert result[0] == ["A", "B", "C"]
        assert result[1][0] == 1
        assert result[1][1] == 2
        assert result[1][2] == ""  # Exception handling fills with empty string

    def test_scalar_values(self):
        G = Mock(side_effect=lambda key: "scalar" if key == "BaseItem" else None)
        result = makeloop("Base", G, "Item")
        assert result == [["scalar"]]


class TestGetValue:
    """Test the GetValue function"""

    def test_key_not_in_returnables(self):
        with patch('vamdctap.generators.RETURNABLES', {}):
            result = GetValue('NonexistentKey', obj=Mock())
            assert result == ''

    def test_empty_value_in_returnables(self):
        with patch('vamdctap.generators.RETURNABLES', {'EmptyKey': ''}):
            result = GetValue('EmptyKey', obj=Mock())
            assert result == ''

    def test_none_value_in_returnables(self):
        with patch('vamdctap.generators.RETURNABLES', {'NoneKey': None}):
            result = GetValue('NoneKey', obj=Mock())
            assert result == ''

    def test_static_string_no_dot(self):
        with patch('vamdctap.generators.RETURNABLES', {'StaticKey': 'StaticValue'}):
            result = GetValue('StaticKey', obj=Mock())
            assert result == 'StaticValue'

    def test_simple_attribute(self):
        mock_obj = Mock()
        mock_obj.field = "value"

        with patch('vamdctap.generators.RETURNABLES', {'Key': 'Model.field'}):
            result = GetValue('Key', obj=mock_obj)
            assert result == "value"

    def test_nested_attributes(self):
        mock_obj = Mock()
        mock_obj.rel = Mock()
        mock_obj.rel.field = "nested_value"

        with patch('vamdctap.generators.RETURNABLES', {'Key': 'Model.rel.field'}):
            result = GetValue('Key', obj=mock_obj)
            assert result == "nested_value"

    def test_function_call(self):
        mock_obj = Mock()
        mock_obj.get_value = Mock(return_value="function_result")

        with patch('vamdctap.generators.RETURNABLES', {'Key': 'Model.get_value()'}):
            result = GetValue('Key', obj=mock_obj)
            assert result == "function_result"
            mock_obj.get_value.assert_called_once()

    def test_none_result_returns_empty_string(self):
        mock_obj = Mock()
        mock_obj.field = None

        with patch('vamdctap.generators.RETURNABLES', {'Key': 'Model.field'}):
            result = GetValue('Key', obj=mock_obj)
            assert result == ''

    def test_zero_integer_returns_zero_string(self):
        mock_obj = Mock()
        mock_obj.field = 0

        with patch('vamdctap.generators.RETURNABLES', {'Key': 'Model.field'}):
            result = GetValue('Key', obj=mock_obj)
            assert result == '0'

    def test_zero_float_returns_zero_decimal_string(self):
        mock_obj = Mock()
        mock_obj.field = 0.0

        with patch('vamdctap.generators.RETURNABLES', {'Key': 'Model.field'}):
            result = GetValue('Key', obj=mock_obj)
            assert result == '0.0'


class TestMakeOptionalTag:
    """Test the makeOptionalTag function"""

    def test_no_content_returns_empty(self):
        G = Mock(return_value='')
        result = makeOptionalTag('Tag', 'keyword', G)
        assert result == ''

    def test_none_content_returns_empty(self):
        G = Mock(return_value=None)
        result = makeOptionalTag('Tag', 'keyword', G)
        assert result == ''

    def test_simple_content(self):
        G = Mock(return_value='content')
        result = makeOptionalTag('Tag', 'keyword', G)
        assert result == '<Tag>content</Tag>'

    def test_content_with_xml_chars_escaped(self):
        G = Mock(return_value='<test>&value')
        result = makeOptionalTag('Tag', 'keyword', G)
        assert result == '<Tag>&lt;test&gt;&amp;value</Tag>'

    def test_iterable_content(self):
        G = Mock(return_value=['item1', 'item2'])
        result = makeOptionalTag('Tag', 'keyword', G)
        assert result == '<Tag>item1</Tag><Tag>item2</Tag>'

    def test_extra_attributes(self):
        G = Mock(return_value='content')
        result = makeOptionalTag('Tag', 'keyword', G, extraAttr={'attr1': 'val1', 'attr2': 'val2'})
        assert 'attr1="val1"' in result
        assert 'attr2="val2"' in result
        assert '<Tag' in result
        assert '>content</Tag>' in result

    def test_numeric_content(self):
        G = Mock(return_value=42)
        result = makeOptionalTag('Tag', 'keyword', G)
        assert result == '<Tag>42</Tag>'

    def test_zero_string_content(self):
        # GetValue converts numeric 0 to string '0', so this is what makeOptionalTag sees
        G = Mock(return_value='0')
        result = makeOptionalTag('Tag', 'keyword', G)
        assert result == '<Tag>0</Tag>'


class TestMakeSourceRefs:
    """Test the makeSourceRefs function"""

    def test_none_refs(self):
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeSourceRefs(None)
            assert result == ''

    def test_empty_refs(self):
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeSourceRefs([])
            assert result == ''

    def test_single_ref(self):
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeSourceRefs('REF1')
            assert result == '<SourceRef>BNODE-REF1</SourceRef>'

    def test_multiple_refs(self):
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeSourceRefs(['REF1', 'REF2', 'REF3'])
            assert '<SourceRef>BNODE-REF1</SourceRef>' in result
            assert '<SourceRef>BNODE-REF2</SourceRef>' in result
            assert '<SourceRef>BNODE-REF3</SourceRef>' in result

    def test_numeric_refs(self):
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeSourceRefs([1, 2])
            assert '<SourceRef>BNODE-1</SourceRef>' in result
            assert '<SourceRef>BNODE-2</SourceRef>' in result


class TestMakePrimaryType:
    """Test the makePrimaryType function"""

    def test_minimal_tag(self):
        G = Mock(return_value='')
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G)
            assert result == '<Tag>'

    def test_tag_not_closed(self):
        G = Mock(return_value='')
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G)
            assert not result.endswith('</Tag>')

    def test_with_method(self):
        def mock_g(key):
            if key == 'keywordMethod':
                return 'METHOD1'
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G)
            assert 'methodRef="MNODE-METHOD1"' in result

    def test_with_comment(self):
        def mock_g(key):
            if key == 'keywordComment':
                return 'Test comment'
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G)
            assert '<Comments>Test comment</Comments>' in result

    def test_comment_escaped(self):
        def mock_g(key):
            if key == 'keywordComment':
                return '<test>&value'
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G)
            assert '&lt;test&gt;&amp;value' in result

    def test_with_refs(self):
        def mock_g(key):
            if key == 'keywordRef':
                return ['REF1', 'REF2']
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G)
            assert '<SourceRef>BNODE-REF1</SourceRef>' in result
            assert '<SourceRef>BNODE-REF2</SourceRef>' in result

    def test_with_extra_attributes(self):
        G = Mock(return_value='')
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G, extraAttr={'attr1': 'val1'})
            assert 'attr1="val1"' in result

    def test_extra_attr_zero_value_included(self):
        G = Mock(return_value='')
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G, extraAttr={'count': 0})
            assert 'count="0"' in result

    def test_extra_attr_none_value_excluded(self):
        G = Mock(return_value='')
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePrimaryType('Tag', 'keyword', G, extraAttr={'attr': None})
            assert 'attr=' not in result


class TestMakeReferencedTextType:
    """Test the makeReferencedTextType function"""

    def test_no_value_returns_empty(self):
        G = Mock(side_effect=lambda key: '' if key == 'keyword' else '')
        result = makeReferencedTextType('Tag', 'keyword', G)
        assert result == ''

    def test_with_value(self):
        def mock_g(key):
            if key == 'keyword':
                return 'test value'
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeReferencedTextType('Tag', 'keyword', G)
            assert '<Tag>' in result
            assert '<Value>test value</Value>' in result
            assert '</Tag>' in result


class TestMakeAccuracy:
    """Test the makeAccuracy function"""

    def test_no_accuracy_returns_empty(self):
        G = Mock(side_effect=lambda key: None)
        result = makeAccuracy('keyword', G)
        assert result == ''

    def test_simple_accuracy(self):
        def mock_g(key):
            if key == 'keywordAccuracy':
                return 0.5
            return None

        G = Mock(side_effect=mock_g)
        result = makeAccuracy('keyword', G)
        assert '<Accuracy>0.5</Accuracy>' in result

    def test_accuracy_with_confidence(self):
        def mock_g(key):
            if key == 'keywordAccuracy':
                return 0.5
            elif key == 'keywordAccuracyConfidence':
                return '95%'
            return None

        G = Mock(side_effect=mock_g)
        result = makeAccuracy('keyword', G)
        assert 'confidenceInterval="95%"' in result

    def test_accuracy_with_type(self):
        def mock_g(key):
            if key == 'keywordAccuracy':
                return 0.5
            elif key == 'keywordAccuracyType':
                return 'statistical'
            return None

        G = Mock(side_effect=mock_g)
        result = makeAccuracy('keyword', G)
        assert 'type="statistical"' in result

    def test_accuracy_with_relative(self):
        def mock_g(key):
            if key == 'keywordAccuracy':
                return 0.5
            elif key == 'keywordAccuracyRelative':
                return True
            return None

        G = Mock(side_effect=mock_g)
        result = makeAccuracy('keyword', G)
        assert 'relative="true"' in result

    def test_multiple_accuracies(self):
        def mock_g(key):
            if key == 'keywordAccuracy':
                return [0.1, 0.2]
            return None

        G = Mock(side_effect=mock_g)
        result = makeAccuracy('keyword', G)
        assert result.count('<Accuracy>') == 2


class TestMakeEvaluation:
    """Test the makeEvaluation function"""

    def test_no_evaluation_returns_empty(self):
        G = Mock(side_effect=lambda key: None)
        result = makeEvaluation('keyword', G)
        assert result == ''

    def test_simple_evaluation(self):
        def mock_g(key):
            if key == 'keywordEval':
                return 'A'
            return None

        G = Mock(side_effect=mock_g)
        result = makeEvaluation('keyword', G)
        assert '<Quality>A</Quality>' in result
        assert '<Evaluation' in result

    def test_evaluation_with_method(self):
        def mock_g(key):
            if key == 'keywordEval':
                return 'A'
            elif key == 'keywordEvalMethod':
                return 'M1'
            return None

        G = Mock(side_effect=mock_g)
        result = makeEvaluation('keyword', G)
        assert 'methodRef="M1"' in result

    def test_evaluation_with_recommended(self):
        def mock_g(key):
            if key == 'keywordEval':
                return 'A'
            elif key == 'keywordEvalRecommended':
                return True
            return None

        G = Mock(side_effect=mock_g)
        result = makeEvaluation('keyword', G)
        assert 'recommended="true"' in result

    def test_evaluation_with_index(self):
        def mock_g(key):
            if key == 'keywordEval':
                return ['A', 'B']
            elif key == 'keywordEvalMethod':
                return ['M1', 'M2']
            return None

        G = Mock(side_effect=mock_g)
        result = makeEvaluation('keyword', G, j=0)
        # Should only process first evaluation
        assert '<Quality>A</Quality>' in result


class TestMakeDataType:
    """Test the makeDataType function"""

    def test_no_value_returns_empty(self):
        G = Mock(return_value='')
        result = makeDataType('Tag', 'keyword', G)
        assert result == ''

    def test_simple_value(self):
        def mock_g(key):
            if key == 'keyword':
                return '42'
            elif key == 'keywordUnit':
                return 'cm-1'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeDataType('Tag', 'keyword', G)
        assert '<Tag>' in result
        assert '<Value units="cm-1">42</Value>' in result
        assert '</Tag>' in result

    def test_value_without_unit(self):
        def mock_g(key):
            if key == 'keyword':
                return '42'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeDataType('Tag', 'keyword', G)
        assert '<Value units="unitless">42</Value>' in result

    def test_value_with_comment(self):
        def mock_g(key):
            if key == 'keyword':
                return '42'
            elif key == 'keywordComment':
                return 'test comment'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeDataType('Tag', 'keyword', G)
        assert '<Comments>test comment</Comments>' in result

    def test_iterable_value_delegates_to_repeated(self):
        def mock_g(key):
            if key == 'keyword':
                return ['1', '2']
            elif key == 'keywordUnit':
                return 'eV'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeDataType('Tag', 'keyword', G)
        # Should create multiple tags
        assert result.count('<Tag') >= 2


class TestMakeArgumentType:
    """Test the makeArgumentType function"""

    def test_basic_argument(self):
        def mock_g(key):
            if key == 'keywordName':
                return 'Temperature'
            elif key == 'keywordUnits':
                return 'K'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeArgumentType('Argument', 'keyword', G)
        assert "<Argument name='Temperature' units='K'>" in result
        assert '</Argument>' in result

    def test_with_description(self):
        def mock_g(key):
            if key == 'keywordName':
                return 'T'
            elif key == 'keywordUnits':
                return 'K'
            elif key == 'keywordDescription':
                return 'Temperature parameter'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeArgumentType('Argument', 'keyword', G)
        assert '<Description>Temperature parameter</Description>' in result

    def test_with_limits(self):
        def mock_g(key):
            if key == 'keywordName':
                return 'T'
            elif key == 'keywordUnits':
                return 'K'
            elif key == 'keywordLowerLimit':
                return '0'
            elif key == 'keywordUpperLimit':
                return '1000'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeArgumentType('Argument', 'keyword', G)
        assert '<LowerLimit>0</LowerLimit>' in result
        assert '<UpperLimit>1000</UpperLimit>' in result


class TestMakeParameterType:
    """Test the makeParameterType function"""

    def test_basic_parameter(self):
        def mock_g(key):
            if key == 'keywordName':
                return 'coefficient'
            elif key == 'keywordUnits':
                return 'unitless'
            elif key == 'keywordDescription':
                return 'A coefficient'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeParameterType('Parameter', 'keyword', G)
        assert "<Parameter name='coefficient' units='unitless'>" in result
        assert '<Description>A coefficient</Description>' in result
        assert '</Parameter>' in result


class TestCheckXML:
    """Test the checkXML function"""

    def test_object_without_xml_method(self):
        obj = Mock(spec=[])
        has_xml, result = checkXML(obj)
        assert has_xml is False
        assert result is None

    def test_object_with_xml_method(self):
        obj = Mock()
        obj.XML = Mock(return_value='<xml>test</xml>')
        has_xml, result = checkXML(obj)
        assert has_xml is True
        assert result == '<xml>test</xml>'
        obj.XML.assert_called_once()

    def test_custom_method_name(self):
        obj = Mock()
        obj.CustomXML = Mock(return_value='<custom/>')
        has_xml, result = checkXML(obj, 'CustomXML')
        assert has_xml is True
        assert result == '<custom/>'
        obj.CustomXML.assert_called_once()


class TestParityLabel:
    """Test the parityLabel function"""

    def test_even_integer(self):
        assert parityLabel(0) == 'even'
        assert parityLabel(2) == 'even'
        assert parityLabel(4) == 'even'

    def test_odd_integer(self):
        assert parityLabel(1) == 'odd'
        assert parityLabel(3) == 'odd'
        assert parityLabel(5) == 'odd'

    def test_string_convertible_to_int(self):
        assert parityLabel('2') == 'even'
        assert parityLabel('3') == 'odd'

    def test_non_convertible_string(self):
        result = parityLabel('not_a_number')
        assert result == 'not_a_number'

    def test_negative_numbers(self):
        assert parityLabel(-2) == 'even'
        assert parityLabel(-3) == 'odd'


class TestMakeRepeatedDataType:
    """Test the makeRepeatedDataType function"""

    def test_no_value_returns_empty(self):
        G = Mock(return_value='')
        result = makeRepeatedDataType('Tag', 'keyword', G)
        assert result == ''

    def test_single_value_becomes_list(self):
        def mock_g(key):
            if key == 'keyword':
                return '42'
            elif key == 'keywordUnit':
                return 'eV'
            elif key == 'keywordName':
                return 'energy'
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeRepeatedDataType('Tag', 'keyword', G)
            assert '<Tag' in result
            assert 'name="energy"' in result
            assert '<Value units="eV">42</Value>' in result

    def test_multiple_values(self):
        def mock_g(key):
            if key == 'keyword':
                return ['1', '2', '3']
            elif key == 'keywordUnit':
                return 'eV'
            elif key == 'keywordName':
                return ['E1', 'E2', 'E3']
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeRepeatedDataType('Tag', 'keyword', G)
            assert result.count('<Tag') == 3
            assert 'name="E1"' in result
            assert 'name="E2"' in result
            assert 'name="E3"' in result

    def test_replication_of_shorter_lists(self):
        def mock_g(key):
            if key == 'keyword':
                return ['1', '2', '3']
            elif key == 'keywordUnit':
                return 'eV'  # Single value, should be replicated
            elif key == 'keywordName':
                return ''
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeRepeatedDataType('Tag', 'keyword', G)
            # All three values should have same unit
            assert result.count('units="eV"') == 3


class TestMakeDataSeriesAccuracyType:
    """Test the makeDataSeriesAccuracyType function"""

    def test_no_accuracy_data_returns_empty(self):
        G = Mock(return_value='')
        result = makeDataSeriesAccuracyType('keyword', G)
        assert result == ''

    def test_with_error_list(self):
        def mock_g(key):
            if key == 'keywordAccuracyErrorList':
                return [0.1, 0.2, 0.3]
            elif key == 'keywordAccuracyType':
                return 'statistical'
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeDataSeriesAccuracyType('keyword', G)
            assert '<Accuracy' in result
            assert 'type="statistical"' in result  # makePrimaryType uses double quotes
            assert '<ErrorList' in result
            assert "count='3'" in result  # ErrorList uses single quotes
            assert '0.1 0.2 0.3' in result

    def test_with_error_value(self):
        def mock_g(key):
            if key == 'keywordAccuracyErrorValue':
                return '0.05'
            elif 'ErrorList' in key or 'ErrorFile' in key:
                return ''
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeDataSeriesAccuracyType('keyword', G)
            assert '<ErrorValue>0.05</ErrorValue>' in result

    def test_with_error_file(self):
        def mock_g(key):
            if key == 'keywordAccuracyErrorFile':
                return 'errors.dat'
            elif 'ErrorList' in key or 'ErrorValue' in key:
                return ''
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeDataSeriesAccuracyType('keyword', G)
            assert '<ErrorFile>errors.dat</ErrorFile>' in result


class TestMakePartitionfunc:
    """Test the makePartitionfunc function"""

    def test_no_value_returns_empty(self):
        G = Mock(return_value='')
        result = makePartitionfunc('keyword', G)
        assert result == ''

    def test_single_partition_function(self):
        def mock_g(key):
            if key == 'keyword':
                return [100, 200, 300]
            elif key == 'keywordUnit':
                return 'K'
            elif key == 'keywordQ':
                return [10, 20, 30]
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePartitionfunc('keyword', G)
            assert '<PartitionFunction>' in result
            assert 'units="K"' in result
            assert '100 200 300' in result
            assert '10 20 30' in result

    def test_multiple_partition_functions(self):
        def mock_g(key):
            if key == 'keyword':
                return [[100, 200], [150, 250]]
            elif key == 'keywordUnit':
                return ['K', 'K']
            elif key == 'keywordQ':
                return [[10, 20], [15, 25]]
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makePartitionfunc('keyword', G)
            assert result.count('<PartitionFunction>') == 2


class TestMakeBroadeningType:
    """Test the makeBroadeningType function"""

    def test_no_lineshape_returns_empty(self):
        G = Mock(return_value='')
        result = makeBroadeningType(G)
        assert result == ''

    def test_natural_broadening(self):
        def mock_g(key):
            # Function expects 'RadTransBroadening{name}LineshapeParameter' as the primary keyword
            if key == 'RadTransBroadeningNaturalLineshapeParameter':
                return '1.0'  # Some lineshape parameter value
            elif key == 'RadTransBroadeningNaturalLineshapeParameterUnit':
                return 'cm-1'
            elif key == 'RadTransBroadeningNaturalLineshapeParameterName':
                return 'gamma'
            elif key == 'RadTransBroadeningNaturalLineshapeName':
                return 'Lorentzian'
            return ''

        G = Mock(side_effect=mock_g)
        with patch('vamdctap.generators.NODEID', 'NODE'):
            result = makeBroadeningType(G, 'Natural')
            assert '<Broadening name="natural">' in result  # name is lowercased
            assert '<Lineshape name="Lorentzian">' in result


class TestMakeDataSeriesType:
    """Test the makeDataSeriesType function"""

    def test_with_data_list(self):
        def mock_g(key):
            if key == 'keywordParameter':
                return 'X'
            elif key == 'keywordUnit':  # Note: Unit not Units
                return 'cm-1'
            elif key == 'keyword':  # Data comes from base keyword
                return [1, 2, 3, 4, 5]
            elif key == 'keywordN':  # Count suffix
                return '5'
            return ''

        G = Mock(side_effect=mock_g)
        result = makeDataSeriesType('DataSeries', 'keyword', G)
        assert 'parameter="X"' in result  # makePrimaryType uses double quotes
        assert 'units="cm-1"' in result
        assert '<DataList' in result
        assert '1 2 3 4 5' in result

    def test_with_linear_sequence(self):
        def mock_g(key):
            if key == 'keywordParameter':
                return 'X'
            elif key == 'keywordUnit':
                return 'nm'
            elif key == 'keywordLinearA0':  # Required to trigger LinearSequence
                return '1.0'
            elif key == 'keywordLinearA1':  # Required to trigger LinearSequence
                return '1.0'
            elif key == 'keywordLinearInitial':
                return '0'
            elif key == 'keywordLinearIncrement':
                return '0.1'
            elif key == 'keywordLinearCount':
                return '100'
            elif key == 'keyword':  # Base keyword for data
                return ''
            return ''

        G = Mock(side_effect=mock_g)
        result = makeDataSeriesType('DataSeries', 'keyword', G)
        assert '<LinearSequence' in result
        assert 'count="100"' in result
        assert 'initial="0"' in result
        assert 'increment="0.1"' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
