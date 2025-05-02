"""
Cree unit tests para probar 3 casos de éxito 
distintos de cada uno de los ejercicios de
semana 6 (exceptuando el 1 y 2).
"""

from strings import reverse_string

# Case 2: Revers all strings
def test_reverse_string():
    # Arrange
    string = "Hello World"
    # Act
    result = reverse_string(string)
    # Assert
    assert result == "dlroW olleH"