import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')

def get_number(prompt):
    return float(input(prompt))

def main():

    operation = int(input("Podaj działanie, posługując się odpowiednią liczbą: 1 Dodawanie, 2 Odejmowanie, 3 Mnożenie, 4 Dzielenie: "))

    num1 = get_number("Podaj składnik 1: ")
    num2 = get_number("Podaj składnik 2: ")
    if operation == 1:
        result = num1 + num2
        logging.info(f"Dodaję {num1} i {num2}")
    elif operation == 2:
        result = num1 - num2
        logging.info(f"Odejmuję {num1} i {num2}")
    elif operation == 3:
        result = num1 * num2
        logging.info(f"Mnożę {num1} i {num2}")
    elif operation == 4:
        result = num1 / num2
        logging.info(f"Dzielę {num1} i {num2}")
    else:
        logging.error("Niepoprawny wybór operacji.")
        return
    print(f"Wynik to {result}")

if __name__ == "__main__":
    main()
    