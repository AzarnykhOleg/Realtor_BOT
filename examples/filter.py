def custom_filter(some_list: list) -> bool:
    """
The custom_filter function takes a list of elements as an argument and returns True if the sum of all integers
divisible by 7 in the list is less than or equal to 83. Otherwise, it returns False.

:param some_list: list: Specify the type of data that can be passed to the function
:return: True if the sum of elements in some_list that are divisible by 7 is less than or equal to 83
"""
    summ_el = 0
    for el in some_list:
        if not isinstance(el, int):
            pass
        else:
            if el % 7 == 0:
                summ_el += el
    return summ_el <= 83


some_list_1 = [7, 14, 28, 32, 32, 56]
some_list_2 = [7, 14, 28, 32, 32, '56']

print(custom_filter(some_list_1))
print(custom_filter(some_list_2))
# ----------------------------------------------------------

anonimous_filter = lambda x: x.lower().count('я') >= 23
anonymous_filter = lambda s: sum(1 for char in s if char.lower() == 'я') >= 23
"""
The function takes a string argument and returns True if the number of Russian letters 'Я' 
is at least 23 (the letter case is unimportant) and False otherwise.
"""
print(anonymous_filter('Я - последняя буква в алфавите!'))
print(anonymous_filter('яяяяяяяяяяяяяяяяяяяяяяяя, яяяяяяяяяяяяяяяя и яяяяяяяя тоже!'))
