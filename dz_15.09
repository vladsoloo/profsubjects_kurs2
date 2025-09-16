def bool_calculator(a, b, operation):
    if operation == 'and':
        return a and b
    elif operation == 'or':
        return a or b
    elif operation == 'not':
        return not a
    else:
        return None


def truth_table_generator():
    print(" A | B | F")
    print("-----------")

    for a in [False, True]:
        for b in [False, True]:
            f = (a and not b) or (not a and b)
            a_val = 1 if a else 0
            b_val = 1 if b else 0
            f_val = 1 if f else 0
            print(f" {a_val} | {b_val} | {f_val}")


def print_circuit():
    circuit = """
 A ---[NOT]--\\
              > [OR] --- F
 B ---[NOT]--/
"""
    print(circuit)


if __name__ == "__main__":
    print("=== Задание 1: Базовый калькулятор ===")
    print(bool_calculator(True, False, 'and'))
    print(bool_calculator(True, False, 'or'))
    print(bool_calculator(True, None, 'not'))
    print(bool_calculator(True, False, 'xor'))

    print("\n=== Задание 2: Таблица истинности ===")
    truth_table_generator()

    print("\n=== Задание 3: Визуализация схемы ===")
    print_circuit()
