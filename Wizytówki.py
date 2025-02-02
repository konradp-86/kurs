from faker import Faker

class BaseContact:
    def __init__(self, first_name, last_name, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number

    def contact(self):
        return f"Wybieram numer {self.phone_number} i dzwonię do {self.first_name} {self.last_name}"

    @property
    def label_length(self):
        return len(self.first_name) + len(self.last_name)

class BusinessContact(BaseContact):
    def __init__(self, first_name, last_name, email, phone_number, job_title, company, business_phone):
        super().__init__(first_name, last_name, email, phone_number)
        self.job_title = job_title
        self.company = company
        self.business_phone = business_phone

    def contact(self):
        return f"Wybieram numer {self.business_phone} i dzwonię do {self.first_name} {self.last_name}"

def create_contact(contact_type):
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone_number = fake.phone_number()

    if contact_type == 'base':
        return BaseContact(first_name, last_name, email, phone_number)
    elif contact_type == 'business':
        job_title = fake.job()
        company = fake.company()
        business_phone = fake.phone_number()
        return BusinessContact(first_name, last_name, email, phone_number, job_title, company, business_phone)
    else:
        raise ValueError("Niepoprawny typ wizytówki")

def create_contacts(contact_type, quantity):
    contacts = []
    for _ in range(quantity):
        contacts.append(create_contact(contact_type))
    return contacts

if __name__ == "__main__":
    contact_type = 'business'
    contacts = create_contacts(contact_type, 5)

    for contact in contacts:
        print(contact)
        print(contact.contact())
        print(f"Długość imienia i nazwiska: {contact.label_length}")