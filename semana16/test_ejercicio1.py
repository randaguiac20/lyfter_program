"""
1. Cree los siguientes unit tests para el algoritmo `bubble_sort`:
    1. Funciona con una lista pequeña.
    2. Funciona con una lista grande
       (de más de 100 elementos.)
    3. Funciona con una lista vacía.
    4. No funciona con parámetros que no sean una lista.
"""
import pytest
from ejercicio1 import bubble_sort

# 1. Funciona con una lista pequeña.
def test_bubble_sort_small_list():
    """
    Test para verificar que el algoritmo bubble_sort funciona
    correctamente con una lista pequeña.
    """
    # Arrange
    input_list = [34, 12, 25, 45, 2, 23, 0]
    expected_output = [0, 2, 12, 23, 25, 34, 45]
    # Act
    result = bubble_sort(input_list)
    # Assert
    assert result == expected_output

# 2. Funciona con una lista grande (de más de 100 elementos.)
def test_bubble_sort_large_list():
    """
    Test para verificar que el algoritmo bubble_sort funciona
    correctamente con una lista grande.
    """
    # Arrange
    input_list = [i for i in range(102, 0, -1)]
    expected_output = [i for i in range(1, 103)]
    # Act
    result = bubble_sort(input_list)
    # Assert
    assert result == expected_output
    
    
# 3. Funciona con una lista vacía.
def test_bubble_sort_empty_list():
    """
    Test para verificar que el algoritmo bubble_sort funciona
    correctamente con una lista vacía.
    """
    # Arrange
    input_list = []
    expected_output = []
    # Act
    result = bubble_sort(input_list)
    # Assert
    assert result == expected_output

# 4. No funciona con parámetros que no sean una lista.
def test_bubble_sort_invalid_input():
    """
    Test para verificar que el algoritmo bubble_sort no funciona
    con parámetros que no son una lista.
    """
    # Arrange
    input_value = "not a list"
    # Act & Assert
    with pytest.raises(TypeError):
        bubble_sort(input_value)