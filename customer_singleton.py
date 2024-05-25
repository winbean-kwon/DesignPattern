import csv

class Customer:
    _instance = None
    customer_list = []
    csv_file = 'customers.csv' 
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._initiated = False
        return cls._instance

    def __init__(self):
        if not self._initiated:
            self.name = None
            self.phone = None
            self.email = None
            self.rent_history = []
            self._initiated = True
            self.load_customers_from_csv()

    def add_customer(self, name, phone, email):
        for customer_info in Customer.customer_list:
            if customer_info['email'] == email or customer_info['phone'] == phone:
                print("잘못 입력하셨습니다.")
                return False
        self.name = name
        self.phone = phone
        self.email = email
        Customer.customer_list.append({
            'name': name, 
            'phone': phone, 
            'email': email, 
            'rent_history': []
        })
        print(name + "님이 회원 등록이 되었습니다.")
        self.save_customers_to_csv()
        return True

    def search_customer(self, phone):
        for customer_info in Customer.customer_list:
            if customer_info['phone'] == phone:
                self.name = customer_info['name']
                self.phone = customer_info['phone']
                self.email = customer_info['email']
                self.rent_history = customer_info['rent_history']
                self.view_customer_info()
                return customer_info
        print("회원 정보를 찾을 수 없습니다.")
        return None

    def update_customer_info(self, customer_info, field, new_value):
        if field == 'phone':
            customer_info['phone'] = new_value
        elif field == 'email':
            customer_info['email'] = new_value
        self.name = customer_info['name']
        self.phone = customer_info['phone']
        self.email = customer_info['email']
        print("회원 정보가 성공적으로 업데이트 되었습니다.")
        self.save_customers_to_csv()

    def view_customer_info(self):
        print(f"이름: {self.name}")
        print(f"전화번호: {self.phone}")
        print(f"이메일: {self.email}")
        print("대여 기록:")
        for history in self.rent_history:
            print(history)

    def add_rent_history(self, customer_info, rent_info):
        customer_info['rent_history'].append(rent_info)
        self.save_customers_to_csv()

    def save_customers_to_csv(self):
        with open(Customer.csv_file, 'w', newline='') as csvfile:
            fieldnames = ['name', 'phone', 'email', 'rent_history']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for customer in Customer.customer_list:
                customer_copy = customer.copy()
                customer_copy['rent_history'] = str(customer_copy['rent_history'])
                writer.writerow(customer_copy)
    
    def load_customers_from_csv(self):
        try:
            with open(Customer.csv_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row['rent_history'] = eval(row['rent_history'])
                    Customer.customer_list.append(row)
        except FileNotFoundError:
            print("CSV 파일을 찾을 수 없습니다.")
