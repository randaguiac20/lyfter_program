"""
Cree un programa que lea nombres de canciones
de un archivo (línea por línea) y guarde en otro archivo
los mismos nombres ordenados alfabéticamente.
"""


file_name = "songs.txt"
sort_lines_file = "sorted_songs.txt"


def print_sort_lines(sort_list, lines_list):
    for line in lines_list:
        print(line)
        sort_list.append(line)
        sort_list.sort()
    return sort_list
    
def read_file(filename):
    sort_list = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        list_lines = print_sort_lines(sort_list, lines)
        return list_lines


def write_file(filename, order_list):
    with open(filename, 'w') as f:
        for song in order_list:
            print(song)
            f.write(song)


song_list_sort = read_file(file_name)
write_file(sort_lines_file, song_list_sort)
