"""
Cree unit tests para probar 3 casos de éxito 
distintos de cada uno de los ejercicios de
semana 6 (exceptuando el 1 y 2).
"""
import pytest
from strings import reverse_string

# Case 2: Revers all strings
def test_reverse_string():
    # Arrange
    string = "Hello World"
    # Act
    result = reverse_string(string)
    # Assert
    assert result == "dlroW olleH"
    
def test_reverse_string_not_a_string():
    # Arrange
    string = ["Hello World"]
    # Act & Assert
    with pytest.raises(TypeError):
        reverse_string(string)
        
def test_reverse_string_with_one_letter():
    # Arrange
    string = "H"
    # Act
    result = reverse_string(string)
    # Assert
    assert result == "H"

def test_reverse_string_with_empty_string():
    # Arrange
    string = ""
    # Act
    result = reverse_string(string)
    # Assert
    assert result == ""
