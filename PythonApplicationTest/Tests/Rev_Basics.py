# DocString, type hints
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


#print(get_full_name("john", "doe"))

#print("aa".istitle())

NameList = ['a','g','s']
#new_rows_temp = new_rows.select([col(c).alias(c + append_a) for c in matching_cols] + ['Id'])  

def greet(name:str = 'You') -> str:
    """
    This function greets people by name
    Example1:
    >>> greet(name='John Doe')
    >>> 'Hello John Doe'
    Example2:
    >>> greet()
    >>> 'Hello You'
    """
    return f'Hello {name}'

#?greet
#print(greet.__doc__)
#greet()


dict_items = [('sape', 4139), ('guido', 4127), ('jack', 4098)]
my_dict = dict(dict_items)
#print([(k, v) for k, v in my_dict.items()])



#Enumerate two lists
A = ['a', 'b', 'c']
B = ['u', 'w', 'r']

# Using enumerate and zip to combine both lists with an index
result = [(i + 1, a, b) for i, (a, b) in enumerate(zip(A, B))]

#print(result)

#TypeHint & Dict

def process_items(prices: dict[str, float | str]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)
        print('\n')

dict_items = [('Shoe', 24), ('TV', 92), ('Blabla', 'No Price')]     
my_dict = dict(dict_items)

process_items(my_dict)
