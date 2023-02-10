import random


def generate_otp():
    number_list = [x for x in range(10)]
    code_items_for_otp = []

    for i in range(6):
        num = random.choice(number_list)
        code_items_for_otp.append(num)

    code_string = "".join(str(item) for item in code_items_for_otp)

    return code_string
