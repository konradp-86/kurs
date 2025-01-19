from faker import Faker

# Definicja klasy Wizytówka
class BusinessCard:
    def __init__(self, name, company, job_title, email, phone_number):
        self.name = name
        self.company = company
        self.job_title = job_title
        self.email = email
        self.phone_number = phone_number

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Company: {self.company}\n"
                f"Job Title: {self.job_title}\n"
                f"Email: {self.email}\n"
                f"Phone: {self.phone_number}")

# Funkcja tworząca losową wizytówkę
def create_random_business_card():
    fake = Faker()
    name = fake.name()
    company = fake.company()
    job_title = fake.job()
    email = fake.email()
    phone_number = fake.phone_number()
    
    return BusinessCard(name, company, job_title, email, phone_number)

# Testowanie funkcji
if __name__ == "__main__":
    card = create_random_business_card()
    print(card)

