"""
>> Parte 2

1. Analice el algoritmo de bubble_sort usando la Big O Notation.
"""

def bubble_sort(elements):
    print(elements) # => O(1)
    n_elements = len(elements) # => O(1)
    made_change = False # => O(1)
    for outer_index in range(n_elements): # => O(n)
        for inner_index in range(n_elements - 1, 0, -1): # => O(n^2)
            current_element = elements[inner_index] # => O(1)
            next_element = elements[inner_index - 1] # => O(1)
            print(f" Iteration: {outer_index} Index {inner_index} ==> current_element: {current_element} - Next: {next_element}") # => O(1)
            if current_element < next_element: # => O(1)
                print(f"  {current_element} is lower than next element {next_element}") # => O(1)
                elements[inner_index] = next_element # => O(1)
                elements[inner_index - 1] = current_element # => O(1)
                made_change = True # => O(1)
            print(f"\n     {elements}\n") # => O(1)
        if not made_change: # => 
            return

element_list = [34, 12, 25, 45, 2, 23, 0] # => O(1)
bubble_sort(element_list) # => O(n^2)

# As a conclusion:
# variable element_list is classified as O(1)
# function bubble_sort is classified as 0(n^2)
# Over all this script then is a Big O notation of 0(n^2)