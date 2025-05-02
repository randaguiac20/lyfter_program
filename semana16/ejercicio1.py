"""
>> Parte 1

1. Crea un bubble_sort por tu cuenta sin revisar el 
código de la lección.
"""

def bubble_sort(elements):
    print(elements)
    n_elements = len(elements)
    made_change = False
    for outer_index in range(0, n_elements - 1):
        for inner_index in range(0, n_elements - 1 - outer_index):
            current_element = elements[inner_index]
            next_element = elements[inner_index + 1]
            print(f" Iteration {outer_index} Index {inner_index} ==> current_element: {current_element} - Next: {next_element}")
            if current_element > next_element:
                print(f"  {current_element} is greater than next element {next_element}")
                elements[inner_index] = next_element
                elements[inner_index + 1] = current_element
                made_change = True
            print(f"\n     {elements}\n")
        if not made_change:
            return
    return elements

element_list = [34, 12, 25, 45, 2, 23, 0]
bubble_sort(element_list)

