"""
Cree unit tests para probar 3 casos de éxito 
distintos de cada uno de los ejercicios de
semana 6 (exceptuando el 1 y 2).
"""
from letter_counter import letter_case_counter

# Case 3: Contar letras mayúsculas y minúsculas
def test_letter_case_counter():
    # Arrange
    string = "This is a test string with 2 numbers 123 and 3 letters"
    # Act
    result = letter_case_counter(string)
    # Assert
    assert result == "There's 1 upper cases and 37 lower cases"