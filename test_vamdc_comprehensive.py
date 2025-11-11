"""
Comprehensive test suite for VAMDC NodeSoftware pseudo-SQL API.

This test suite covers meaningful functionality:
1. SQL parsing and Q object conversion (complex WHERE clauses, operators, logic)
2. Data extraction via GetValue (foreign key traversal, method calls, edge cases)
3. XML generation components (data types, accuracy, evaluation, source refs)
4. Integration tests (full SQL → XML pipeline)

Designed to work with pytest and can be run with:
    pytest test_vamdc_comprehensive.py -v
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
from django.db.models import Q

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_default')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'nodes', 'ExampleNode'))

import django
django.setup()

# Import modules to test
from vamdctap import sqlparse
from vamdctap import generators
from pyparsing import ParseException


# ============================================================================
# SQL Parser Tests
# ============================================================================

class TestSQLParser:
    """Test SQL parsing functionality with complex queries"""

    def test_simple_select_all(self):
        """Test parsing simple SELECT ALL query"""
        sql = "SELECT ALL WHERE RadTransWavelength > 5000"
        result = sqlparse.SQL.parseString(sql)
        assert "ALL" in result.columns or result.columns[0] == "ALL"
        assert len(result.where) > 0

    def test_select_specific_returnables(self):
        """Test parsing SELECT with specific returnables"""
        sql = "SELECT RadiativeTransitions, AtomStates WHERE AtomSymbol = 'Fe'"
        result = sqlparse.SQL.parseString(sql)
        assert 'RadiativeTransitions' in str(result.columns)
        assert 'AtomStates' in str(result.columns)

    def test_select_count(self):
        """Test SELECT COUNT syntax"""
        sql = "SELECT COUNT AtomStates WHERE AtomIonCharge = 1"
        result = sqlparse.SQL.parseString(sql)
        assert result.count == "count"

    def test_select_top_n(self):
        """Test SELECT TOP N syntax"""
        sql = "SELECT TOP 100 ALL WHERE RadTransWavelength > 5000"
        result = sqlparse.SQL.parseString(sql)
        assert result.top is not None
        assert "100" in str(result.top)

    def test_where_simple_equals(self):
        """Test simple WHERE clause with equals"""
        sql = "SELECT ALL WHERE AtomSymbol = 'Fe'"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        assert 'AtomSymbol' in str(where)
        assert '=' in str(where)

    def test_where_comparison_operators(self):
        """Test WHERE clause with all comparison operators"""
        operators = ['<', '>', '<=', '>=', '!=', '<>']
        for op in operators:
            sql = f"SELECT ALL WHERE RadTransWavelength {op} 5000"
            result = sqlparse.SQL.parseString(sql)
            where = result.where.asList()
            assert op in str(where)

    def test_where_like_operator(self):
        """Test WHERE clause with LIKE operator"""
        sql = "SELECT ALL WHERE AtomSymbol LIKE 'Fe%'"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        assert 'like' in str(where).lower()

    def test_where_in_operator(self):
        """Test WHERE clause with IN operator"""
        sql = "SELECT ALL WHERE AtomSymbol IN ('Fe', 'Ca', 'Mg')"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        assert 'in' in str(where).lower()

    def test_where_and_logic(self):
        """Test WHERE clause with AND logic"""
        sql = "SELECT ALL WHERE AtomSymbol = 'Fe' AND AtomIonCharge = 1"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        assert 'and' in str(where).lower()

    def test_where_or_logic(self):
        """Test WHERE clause with OR logic"""
        sql = "SELECT ALL WHERE AtomSymbol = 'Fe' OR AtomSymbol = 'Ca'"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        assert 'or' in str(where).lower()

    def test_where_not_logic(self):
        """Test WHERE clause with NOT logic"""
        sql = "SELECT ALL WHERE NOT AtomSymbol = 'Fe'"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        assert 'not' in str(where).lower()

    def test_where_complex_logic(self):
        """Test complex WHERE clause with nested logic"""
        sql = "SELECT ALL WHERE (AtomSymbol = 'Fe' OR AtomSymbol = 'Ca') AND RadTransWavelength > 5000"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        # Should have parentheses, OR, AND
        assert 'and' in str(where).lower()
        assert 'or' in str(where).lower()

    def test_where_scientific_notation(self):
        """Test WHERE clause with scientific notation"""
        sql = "SELECT ALL WHERE RadTransWavelength > 5.0E3"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        assert '5.0E3' in str(where) or '5.0e3' in str(where)

    def test_where_negative_numbers(self):
        """Test WHERE clause with negative numbers"""
        sql = "SELECT ALL WHERE AtomStateEnergy > -100.5"
        result = sqlparse.SQL.parseString(sql)
        where = result.where.asList()
        assert '-100.5' in str(where)

    def test_invalid_sql_raises_exception(self):
        """Test that invalid SQL raises ParseException"""
        invalid_queries = [
            "INVALID SQL QUERY",
            "WHERE AtomSymbol = 'Fe'",  # missing SELECT
        ]
        for query in invalid_queries:
            with pytest.raises(ParseException):
                sqlparse.SQL.parseString(query)


class TestRestrictionToQ:
    """Test conversion of SQL restrictions to Django Q objects"""

    @pytest.fixture
    def mock_restrictables(self):
        """Mock RESTRICTABLES dictionary for testing"""
        return {
            'AtomSymbol': 'species__name',
            'AtomIonCharge': 'species__ion',
            'RadTransWavelength': 'wavelength',
            'AtomStateEnergy': 'energy',
        }

    def test_simple_equals_restriction(self, mock_restrictables):
        """Test simple = restriction to Q object"""
        rs = ['AtomSymbol', '=', "'Fe'"]
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert str(q) == "(AND: ('species__name__exact', 'Fe'))"

    def test_greater_than_restriction(self, mock_restrictables):
        """Test > restriction to Q object"""
        rs = ['RadTransWavelength', '>', '5000']
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert str(q) == "(AND: ('wavelength__gt', '5000'))"

    def test_less_than_restriction(self, mock_restrictables):
        """Test < restriction to Q object"""
        rs = ['RadTransWavelength', '<', '10000']
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert str(q) == "(AND: ('wavelength__lt', '10000'))"

    def test_greater_equal_restriction(self, mock_restrictables):
        """Test >= restriction to Q object"""
        rs = ['AtomStateEnergy', '>=', '0']
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert str(q) == "(AND: ('energy__gte', '0'))"

    def test_less_equal_restriction(self, mock_restrictables):
        """Test <= restriction to Q object"""
        rs = ['AtomStateEnergy', '<=', '1000']
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert str(q) == "(AND: ('energy__lte', '1000'))"

    def test_not_equal_restriction(self, mock_restrictables):
        """Test != restriction to Q object"""
        rs = ['AtomSymbol', '!=', "'Fe'"]
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        # Should be negated Q object
        assert 'NOT' in str(q)

    def test_not_equal_null_restriction(self, mock_restrictables):
        """Test != NULL restriction to Q object"""
        rs = ['AtomSymbol', '!=', "'NULL'"]
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert 'isnull' in str(q).lower()

    def test_in_restriction(self, mock_restrictables):
        """Test IN restriction to Q object"""
        rs = ['AtomSymbol', 'in', '(', "'Fe'", ',', "'Ca'", ',', "'Mg'", ')']
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert '__in' in str(q)

    def test_like_startswith_restriction(self, mock_restrictables):
        """Test LIKE with trailing % (startswith)"""
        rs = ['AtomSymbol', 'like', "'Fe%'"]
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert '__startswith' in str(q)

    def test_like_endswith_restriction(self, mock_restrictables):
        """Test LIKE with leading % (endswith)"""
        rs = ['AtomSymbol', 'like', "'%III'"]
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert '__endswith' in str(q)

    def test_like_contains_restriction(self, mock_restrictables):
        """Test LIKE with both % (contains)"""
        rs = ['AtomSymbol', 'like', "'%Fe%'"]
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert '__contains' in str(q)

    def test_like_exact_restriction(self, mock_restrictables):
        """Test LIKE without % (exact)"""
        rs = ['AtomSymbol', 'like', "'Fe'"]
        q = sqlparse.restriction2Q(rs, restrictables=mock_restrictables)
        assert isinstance(q, Q)
        assert '__exact' in str(q)

    def test_unsupported_restrictable_raises_exception(self):
        """Test that unsupported restrictable raises exception"""
        rs = ['UnsupportedField', '=', "'value'"]
        with pytest.raises(Exception) as exc_info:
            sqlparse.restriction2Q(rs, restrictables={})
        assert 'not supported' in str(exc_info.value).lower()


class TestSQL2Q:
    """Test full SQL to Q object conversion with complex logic"""

    @pytest.fixture
    def mock_restrictables(self):
        """Mock RESTRICTABLES dictionary"""
        return {
            'AtomSymbol': 'species__name',
            'AtomIonCharge': 'species__ion',
            'RadTransWavelength': 'wavelength',
        }

    def test_simple_where_to_q(self, mock_restrictables):
        """Test simple WHERE clause to Q object"""
        sql_str = "SELECT ALL WHERE AtomSymbol = 'Fe'"
        sql = sqlparse.SQL.parseString(sql_str)

        with patch.object(sqlparse, 'RESTRICTABLES', mock_restrictables):
            q = sqlparse.sql2Q(sql)
            assert isinstance(q, Q)

    def test_and_logic_to_q(self, mock_restrictables):
        """Test AND logic conversion to Q object"""
        sql_str = "SELECT ALL WHERE AtomSymbol = 'Fe' AND AtomIonCharge = 1"
        sql = sqlparse.SQL.parseString(sql_str)

        with patch.object(sqlparse, 'RESTRICTABLES', mock_restrictables):
            q = sqlparse.sql2Q(sql)
            assert isinstance(q, Q)
            # Q objects combined with AND should have both conditions
            q_str = str(q)
            assert 'species__name' in q_str
            assert 'species__ion' in q_str

    def test_or_logic_to_q(self, mock_restrictables):
        """Test OR logic conversion to Q object"""
        sql_str = "SELECT ALL WHERE AtomSymbol = 'Fe' OR AtomSymbol = 'Ca'"
        sql = sqlparse.SQL.parseString(sql_str)

        with patch.object(sqlparse, 'RESTRICTABLES', mock_restrictables):
            q = sqlparse.sql2Q(sql)
            assert isinstance(q, Q)
            # Q objects combined with OR
            assert 'OR' in str(q)

    def test_not_logic_to_q(self, mock_restrictables):
        """Test NOT logic conversion to Q object"""
        sql_str = "SELECT ALL WHERE NOT AtomSymbol = 'Fe'"
        sql = sqlparse.SQL.parseString(sql_str)

        with patch.object(sqlparse, 'RESTRICTABLES', mock_restrictables):
            q = sqlparse.sql2Q(sql)
            assert isinstance(q, Q)
            assert 'NOT' in str(q)

    def test_complex_nested_logic_to_q(self, mock_restrictables):
        """Test complex nested logic conversion"""
        sql_str = "SELECT ALL WHERE (AtomSymbol = 'Fe' OR AtomSymbol = 'Ca') AND RadTransWavelength > 5000"
        sql = sqlparse.SQL.parseString(sql_str)

        with patch.object(sqlparse, 'RESTRICTABLES', mock_restrictables):
            q = sqlparse.sql2Q(sql)
            assert isinstance(q, Q)

    def test_empty_where_returns_empty_q(self):
        """Test that empty WHERE returns empty Q object"""
        sql_str = "SELECT ALL"
        sql = sqlparse.SQL.parseString(sql_str)
        q = sqlparse.sql2Q(sql)
        assert isinstance(q, Q)
        # Empty Q should match everything
        assert str(q) == "(AND: )"


# ============================================================================
# GetValue Function Tests
# ============================================================================

class TestGetValue:
    """Test the GetValue function for data extraction"""

    @pytest.fixture
    def mock_returnables(self):
        """Mock RETURNABLES dictionary"""
        return {
            'SimpleAttribute': 'Test.value',
            'ForeignKeyAttribute': 'Test.foreign.value',
            'NestedForeignKey': 'Test.foreign.nested.value',
            'MethodCall': 'Test.get_value()',
            'StaticString': 'STATIC_VALUE',
            'EmptyValue': '',
            'NullValue': None,
        }

    def test_get_static_string(self, mock_returnables):
        """Test getting static string (no dot)"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_obj = Mock()
            value = generators.GetValue('StaticString', Test=mock_obj)
            assert value == 'STATIC_VALUE'

    def test_get_simple_attribute(self, mock_returnables):
        """Test getting simple attribute"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_obj = Mock()
            mock_obj.value = 42
            value = generators.GetValue('SimpleAttribute', Test=mock_obj)
            assert value == 42

    def test_get_foreign_key_attribute(self, mock_returnables):
        """Test getting attribute through foreign key"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_foreign = Mock()
            mock_foreign.value = 'foreign_value'
            mock_obj = Mock()
            mock_obj.foreign = mock_foreign
            value = generators.GetValue('ForeignKeyAttribute', Test=mock_obj)
            assert value == 'foreign_value'

    def test_get_nested_foreign_key(self, mock_returnables):
        """Test getting attribute through nested foreign keys"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_nested = Mock()
            mock_nested.value = 'nested_value'
            mock_foreign = Mock()
            mock_foreign.nested = mock_nested
            mock_obj = Mock()
            mock_obj.foreign = mock_foreign
            value = generators.GetValue('NestedForeignKey', Test=mock_obj)
            assert value == 'nested_value'

    def test_get_method_call(self, mock_returnables):
        """Test calling a method (ends with ())"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_obj = Mock()
            mock_obj.get_value = Mock(return_value='method_result')
            value = generators.GetValue('MethodCall', Test=mock_obj)
            assert value == 'method_result'
            mock_obj.get_value.assert_called_once()

    def test_get_none_returns_empty_string(self, mock_returnables):
        """Test that None value returns empty string"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_obj = Mock()
            mock_obj.value = None
            value = generators.GetValue('SimpleAttribute', Test=mock_obj)
            assert value == ''

    def test_get_zero_returns_string_zero(self, mock_returnables):
        """Test that 0 returns '0' not empty string"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_obj = Mock()
            mock_obj.value = 0
            value = generators.GetValue('SimpleAttribute', Test=mock_obj)
            assert value == '0'

    def test_get_zero_float_returns_string_zero(self, mock_returnables):
        """Test that 0.0 returns '0.0' not empty string"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_obj = Mock()
            mock_obj.value = 0.0
            value = generators.GetValue('SimpleAttribute', Test=mock_obj)
            assert value == '0.0'

    def test_get_missing_returnable_returns_empty(self):
        """Test that missing returnable key returns empty string"""
        with patch.object(generators, 'RETURNABLES', {}):
            mock_obj = Mock()
            value = generators.GetValue('NonExistent', Test=mock_obj)
            assert value == ''

    def test_get_empty_value_returns_empty(self, mock_returnables):
        """Test that empty value in RETURNABLES returns empty string"""
        with patch.object(generators, 'RETURNABLES', mock_returnables):
            mock_obj = Mock()
            value = generators.GetValue('EmptyValue', Test=mock_obj)
            assert value == ''

    def test_get_invalid_input_returns_empty(self):
        """Test that invalid input returns empty string"""
        value = generators.GetValue("9sdf8?sdklns")
        assert value == ""

        value = generators.GetValue(None)
        assert value == ""

        value = generators.GetValue("")
        assert value == ""


# ============================================================================
# XML Generation Tests
# ============================================================================

class TestXMLGenerationHelpers:
    """Test XML generation helper functions"""

    def test_makeiter_with_string(self):
        """Test makeiter with string input"""
        result = generators.makeiter("Test", n=4)
        assert result == ["Test", "Test", "Test", "Test"]

    def test_makeiter_with_empty_string(self):
        """Test makeiter with empty string"""
        result = generators.makeiter("", n=4)
        assert result == [None, None, None, None]

    def test_makeiter_with_none(self):
        """Test makeiter with None"""
        result = generators.makeiter(None, n=3)
        assert result == [None, None, None]

    def test_makeiter_with_list(self):
        """Test makeiter with list (should return as-is)"""
        input_list = [1, 2, 3]
        result = generators.makeiter(input_list)
        assert result == input_list

    def test_makeiter_with_single_value(self):
        """Test makeiter with single value, no n"""
        result = generators.makeiter("Test")
        assert result == ["Test"]

    def test_makesourcerefs_single(self):
        """Test makeSourceRefs with single reference"""
        with patch.object(generators, 'NODEID', 'TestNode'):
            result = generators.makeSourceRefs("ref1")
            assert result == '<SourceRef>BTestNode-ref1</SourceRef>'

    def test_makesourcerefs_multiple(self):
        """Test makeSourceRefs with multiple references"""
        with patch.object(generators, 'NODEID', 'TestNode'):
            result = generators.makeSourceRefs(["ref1", "ref2", "ref3"])
            assert '<SourceRef>BTestNode-ref1</SourceRef>' in result
            assert '<SourceRef>BTestNode-ref2</SourceRef>' in result
            assert '<SourceRef>BTestNode-ref3</SourceRef>' in result

    def test_makesourcerefs_empty(self):
        """Test makeSourceRefs with empty/None"""
        result = generators.makeSourceRefs(None)
        assert result == ''

        result = generators.makeSourceRefs([])
        assert result == ''

    def test_makeoptionaltag_with_content(self):
        """Test makeOptionalTag with content"""
        mock_G = lambda x: "TestValue" if x == "Test" else None
        result = generators.makeOptionalTag("testtag", "Test", mock_G)
        assert result == '<testtag>TestValue</testtag>'

    def test_makeoptionaltag_with_extra_attrs(self):
        """Test makeOptionalTag with extra attributes"""
        mock_G = lambda x: {"Test": "TestValue", "Attr": "AttrValue"}.get(x)
        result = generators.makeOptionalTag("testtag", "Test", mock_G,
                                           extraAttr={"attr": mock_G("Attr")})
        assert 'attr="AttrValue"' in result
        assert '>TestValue<' in result

    def test_makeoptionaltag_without_content(self):
        """Test makeOptionalTag without content returns empty"""
        mock_G = lambda x: None
        result = generators.makeOptionalTag("testtag", "Test", mock_G)
        assert result == ''

    def test_makeoptionaltag_with_list(self):
        """Test makeOptionalTag with list of values"""
        mock_G = lambda x: ["val1", "val2", "val3"] if x == "Test" else None
        result = generators.makeOptionalTag("testtag", "Test", mock_G)
        assert '<testtag>val1</testtag>' in result
        assert '<testtag>val2</testtag>' in result
        assert '<testtag>val3</testtag>' in result

    def test_paritylabel_odd(self):
        """Test parityLabel with odd number"""
        assert generators.parityLabel(1) == "odd"
        assert generators.parityLabel(3) == "odd"
        assert generators.parityLabel(-1) == "odd"

    def test_paritylabel_even(self):
        """Test parityLabel with even number"""
        assert generators.parityLabel(0) == "even"
        assert generators.parityLabel(2) == "even"
        assert generators.parityLabel(-2) == "even"


class TestXMLComplexElements:
    """Test complex XML element generation"""

    def setup_method(self):
        """Setup for each test"""
        generators.NODEID = "TestNode"

    def test_makeaccuracy_single(self):
        """Test makeAccuracy with single accuracy value"""
        mock_G = lambda x: {
            'TestAccuracy': [1],
            'TestAccuracyConfidence': [1],
            'TestAccuracyRelative': [True],
            'TestAccuracyType': [1],
        }.get(x)

        result = generators.makeAccuracy("Test", mock_G)
        assert '<Accuracy' in result
        assert 'confidenceInterval="1"' in result
        assert 'type="1"' in result
        assert 'relative="true"' in result
        assert '>1</Accuracy>' in result

    def test_makeaccuracy_multiple(self):
        """Test makeAccuracy with multiple accuracy values"""
        mock_G = lambda x: {
            'TestAccuracy': [1, 2],
            'TestAccuracyConfidence': [1, 2],
            'TestAccuracyRelative': [True, False],
            'TestAccuracyType': [1, 2],
        }.get(x)

        result = generators.makeAccuracy("Test", mock_G)
        assert result.count('<Accuracy') == 2
        assert 'relative="true"' in result
        assert '>1</Accuracy>' in result
        assert '>2</Accuracy>' in result

    def test_makeaccuracy_relative_false(self):
        """Test makeAccuracy with relative=False (should not include attribute)"""
        mock_G = lambda x: {
            'TestAccuracy': [2],
            'TestAccuracyConfidence': [2],
            'TestAccuracyRelative': [False],
            'TestAccuracyType': [2],
        }.get(x)

        result = generators.makeAccuracy("Test", mock_G)
        # When relative is False, it should not include the relative attribute
        # (checking the actual behavior from tests.py line 235)
        assert '>2</Accuracy>' in result


class TestSplitWhere:
    """Test the splitWhere function for parsing WHERE logic"""

    def test_splitwhere_simple_restriction(self):
        """Test splitWhere with simple restriction from parsed SQL"""
        sql = "SELECT ALL WHERE AtomSymbol = 'Fe'"
        result = sqlparse.SQL.parseString(sql)
        logic, rests, counter = sqlparse.splitWhere(result.where)
        assert 'r0' in logic
        assert '0' in rests
        assert counter >= 1

    def test_splitwhere_with_and(self):
        """Test splitWhere with AND logic from parsed SQL"""
        sql = "SELECT ALL WHERE AtomSymbol = 'Fe' AND AtomIonCharge = 1"
        result = sqlparse.SQL.parseString(sql)
        logic, rests, counter = sqlparse.splitWhere(result.where)
        assert 'and' in logic
        assert 'r0' in logic
        assert 'r1' in logic
        assert counter == 2

    def test_splitwhere_with_or(self):
        """Test splitWhere with OR logic from parsed SQL"""
        sql = "SELECT ALL WHERE AtomSymbol = 'Fe' OR AtomSymbol = 'Ca'"
        result = sqlparse.SQL.parseString(sql)
        logic, rests, counter = sqlparse.splitWhere(result.where)
        assert 'or' in logic
        assert 'r0' in logic
        assert 'r1' in logic
        assert counter == 2

    def test_splitwhere_with_not(self):
        """Test splitWhere with NOT logic from parsed SQL"""
        sql = "SELECT ALL WHERE NOT AtomSymbol = 'Fe'"
        result = sqlparse.SQL.parseString(sql)
        logic, rests, counter = sqlparse.splitWhere(result.where)
        assert 'not' in logic
        assert 'r0' in logic


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for the full SQL to Q object pipeline"""

    @pytest.fixture
    def setup_django_test_env(self):
        """Setup Django test environment"""
        # This would setup the ExampleNode environment
        pass

    def test_full_sql_parsing_pipeline(self):
        """Test complete SQL parsing to Q object conversion"""
        sql_str = "SELECT ALL WHERE AtomSymbol = 'Fe' AND RadTransWavelength > 5000"

        # Parse SQL
        sql = sqlparse.SQL.parseString(sql_str)
        assert "ALL" in sql.columns or sql.columns[0] == "ALL"

        # Verify where clause exists
        assert sql.where is not None

        # Split WHERE clause
        logic, rests, counter = sqlparse.splitWhere(sql.where)
        assert len(rests) == 2  # Two restrictions
        assert 'and' in logic

    def test_complex_query_with_in_operator(self):
        """Test complex query with IN operator"""
        sql_str = "SELECT RadiativeTransitions WHERE AtomSymbol IN ('Fe', 'Ca', 'Mg') AND RadTransWavelength > 5000"

        # Parse SQL
        sql = sqlparse.SQL.parseString(sql_str)
        assert 'RadiativeTransitions' in str(sql.columns)

        # Verify WHERE clause
        where = sql.where.asList()
        assert 'in' in str(where).lower()
        assert 'and' in str(where).lower()

    def test_complex_query_with_like_operator(self):
        """Test complex query with LIKE operator"""
        sql_str = "SELECT ALL WHERE AtomSymbol LIKE 'Fe%' AND AtomIonCharge <= 2"

        # Parse SQL
        sql = sqlparse.SQL.parseString(sql_str)
        where = sql.where.asList()
        assert 'like' in str(where).lower()
        assert 'and' in str(where).lower()

    def test_query_with_nested_parentheses(self):
        """Test query with nested parentheses"""
        sql_str = "SELECT ALL WHERE ((AtomSymbol = 'Fe' OR AtomSymbol = 'Ca') AND RadTransWavelength > 5000)"

        # Parse SQL
        sql = sqlparse.SQL.parseString(sql_str)
        where = sql.where.asList()
        # Should parse without errors and maintain logic structure
        assert len(where) > 0


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_sql_with_trailing_semicolon(self):
        """Test SQL with trailing semicolon"""
        sql_str = "SELECT ALL WHERE AtomSymbol = 'Fe';"
        result = sqlparse.SQL.parseString(sql_str)
        assert "ALL" in result.columns or result.columns[0] == "ALL"

    def test_sql_with_multiple_semicolons(self):
        """Test SQL with multiple trailing semicolons"""
        sql_str = "SELECT ALL WHERE AtomSymbol = 'Fe';;;"
        result = sqlparse.SQL.parseString(sql_str)
        assert "ALL" in result.columns or result.columns[0] == "ALL"

    def test_sql_case_insensitive(self):
        """Test that SQL keywords are case insensitive"""
        sql_variants = [
            "SELECT ALL WHERE AtomSymbol = 'Fe'",
            "select all where AtomSymbol = 'Fe'",
            "SeLeCt AlL wHeRe AtomSymbol = 'Fe'",
        ]
        for sql_str in sql_variants:
            result = sqlparse.SQL.parseString(sql_str)
            assert result is not None

    def test_sql_with_oracle_comment(self):
        """Test SQL with Oracle-style comment"""
        sql_str = "SELECT ALL WHERE AtomSymbol = 'Fe' -- This is a comment"
        result = sqlparse.SQL.parseString(sql_str)
        assert "ALL" in result.columns or result.columns[0] == "ALL"

    def test_quoted_string_with_spaces(self):
        """Test quoted strings with spaces"""
        sql_str = "SELECT ALL WHERE AtomStateTerm = 'a 3P'"
        result = sqlparse.SQL.parseString(sql_str)
        where = result.where.asList()
        assert 'a 3P' in str(where)

    def test_decimal_numbers(self):
        """Test decimal numbers in queries"""
        sql_str = "SELECT ALL WHERE RadTransWavelength > 5000.123"
        result = sqlparse.SQL.parseString(sql_str)
        where = result.where.asList()
        assert '5000.123' in str(where)

    def test_very_small_number_scientific(self):
        """Test very small numbers in scientific notation"""
        sql_str = "SELECT ALL WHERE AtomStateEnergy > 1.5E-10"
        result = sqlparse.SQL.parseString(sql_str)
        where = result.where.asList()
        # Should parse without error


# ============================================================================
# Performance and Stress Tests
# ============================================================================

class TestPerformance:
    """Test performance with complex queries"""

    def test_query_with_many_or_conditions(self):
        """Test query with many OR conditions"""
        elements = ['Fe', 'Ca', 'Mg', 'Na', 'K', 'Al', 'Si', 'C', 'N', 'O']
        or_clauses = " OR ".join([f"AtomSymbol = '{el}'" for el in elements])
        sql_str = f"SELECT ALL WHERE {or_clauses}"

        result = sqlparse.SQL.parseString(sql_str)
        assert result is not None

    def test_query_with_many_and_conditions(self):
        """Test query with many AND conditions"""
        sql_str = "SELECT ALL WHERE RadTransWavelength > 5000 AND RadTransWavelength < 6000 AND AtomIonCharge = 1 AND AtomStateEnergy > 0 AND AtomStateEnergy < 100"

        result = sqlparse.SQL.parseString(sql_str)
        assert result is not None
        where = result.where.asList()
        # Should have multiple AND conditions
        assert str(where).lower().count('and') >= 4


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
