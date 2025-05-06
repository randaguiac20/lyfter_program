"""
Cree unit tests para probar 3 casos de éxito 
distintos de cada uno de los ejercicios de
semana 6 (exceptuando el 1 y 2).
"""
import pytest
from numbers_addition import add_numbers

# Case 1: Suma de números positivos
def test_add_numbers_positive():
    # Arrange
    number_list = [1, 2, 3, 4]
    # Act
    result = add_numbers(number_list)
    # Assert
    assert result == 10

def test_add_numbers_when_not_a_number():
    # Arrange
    number_list = ["1", 2, 3, 4]
    # Act & Assert
    with pytest.raises(TypeError):
        add_numbers(number_list)
    
def test_add_numbers_positive_with_empty_list():
    # Arrange
    number_list = []
    # Act
    result = add_numbers(number_list)
    # Assert
    assert result == 0