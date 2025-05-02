"""
>> Parte 2

2. Analice los siguientes algoritmos usando la Big O Notation:
"""

# >> print_numbers_times_2
# Big O Notation of O(n)
def print_numbers_times_2(numbers_list):
	for number in numbers_list:
		print(number * 2)

# >> check_if_lists_have_an_equal
# Big O Notation of O(n^2)
def check_if_lists_have_an_equal(list_a, list_b):
	for element_a in list_a:
		for element_b in list_b:
			if element_a == element_b:
				return True
				
	return False

# >> print_10_or_less_elements
# Big O Notation of O(1)
def print_10_or_less_elements(list_to_print):
	list_len = len(list_to_print)
	for index in range(min(list_len, 10)):
		print(list_to_print[index])

# >> generate_list_trios
# Big O Notation of O(n^3)
def generate_list_trios(list_a, list_b, list_c):
	result_list = []
	for element_a in list_a:
		for element_b in list_b:
			for element_c in list_c:
				result_list.append(f'{element_a} {element_b} {element_c}')
				
	return result_list
