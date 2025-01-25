import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def add(a, b):
    logging.info(f"Dodaję {a} i {b}")
    return a + b

def subtract(a, b):
    logging.info(f"Odejmuję {a} i {b}")
    return a - b

def multiply(a, b):
    logging.info(f"Mnożę {a} i {b}")
    return a * b

def divide(a, b):
    logging.info(f"Dzielę {a} i {b}")
    return a / b

def perform_operation(operation, num1, num2):
    if operation == 1:
        return add(num1, num2)
    elif operation == 2:
        return subtract(num1, num2)
    elif operation == 3:
        return multiply(num1, num2)
    elif operation == 4:
        return divide(num1, num2)
    else:
        logging.error("Niepoprawny wybór operacji.")
        raise ValueError("Niepoprawny wybór operacji.")

def get_number(Liczba):
    while True:
        try:
            return float(input(Liczba))
        except ValueError:
            print("Podana wartość nie jest liczbą, spróbuj ponownie.")
            
def main():
    try:
        operation = int(input("Podaj działanie, posługując się odpowiednią liczbą: 1 Dodawanie, 2 Odejmowanie, 3 Mnożenie, 4 Dzielenie: "))
        num1 = get_number("Podaj Liczbę 1: ")
        num2 = get_number("Podaj Liczbę 2: ")
        result = perform_operation(operation, num1, num2)
        print(f"Wynik to {result}")
    except ValueError as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    main()