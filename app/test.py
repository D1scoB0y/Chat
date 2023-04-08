# from sqlalchemy import create_engine, text
# from string import ascii_lowercase
# from random import randint, choice

# engine = create_engine('postgresql://postgres:zelel228@localhost:5432/chat_db')

# connection = engine.connect()

# for i in range(100):

#     random_word = ''

#     for i in range(randint(5, 18)):
#         random_word += choice(ascii_lowercase)

#     query_text = f'INSERT INTO public."User" (username, email, email_is_verified, password) VALUES (\'{random_word}\', \'jyjyartem@gmail.com\', false, \'zelel228\');'

#     print(query_text)

#     connection.execute(text(query_text))
from time import time


def benchmark(sort_function):

    def wrapper(array):

        start_time = time()
        sort_function(array)
        end_time = time()

        return str(round(end_time - start_time, 3)) + ' seconds'

    return wrapper


@benchmark
def simple_sorting(array):

    for i in range(0, len(array)-1):

        lowest = i

        for j in range(i+1, len(array)):
            if array[j] < array[lowest]:
                lowest = j

        array[lowest], array[i] = array[i], array[lowest]

    return array




def quick_sorting(array):

    if len(array) <= 1:
        return array


    el = array[0]
    l_b = [i for i in array if i < el]
    center = [i for i in array if i == el]
    r_b = [i for i in array if i > el]

    return quick_sorting(l_b) + center + quick_sorting(r_b)
    



test_list = [i for i in range(1000, 0, -1)]

print(simple_sorting(test_list))
print(quick_sorting(test_list))
