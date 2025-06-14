"""
>> Parte 1

2. Modifica el bubble_sort para que funcione de derecha a izquierda, 
ordenando los números menores primero (como en la imagen de abajo).
"""

def bubble_sort(elements):
    print(elements)
    n_elements = len(elements)
    made_change = False
    for outer_index in range(n_elements):
        for inner_index in range(n_elements - 1, 0, -1):
            current_element = elements[inner_index]
            next_element = elements[inner_index - 1]
            print(f" Iteration: {outer_index} Index {inner_index} ==> current_element: {current_element} - Next: {next_element}")
            if current_element < next_element:
                print(f"  {current_element} is lower than next element {next_element}")
                elements[inner_index] = next_element
                elements[inner_index - 1] = current_element
                made_change = True
            print(f"\n     {elements}\n")
        if not made_change:
            return

element_list = [34, 12, 25, 45, 2, 23, 0]
bubble_sort(element_list)
