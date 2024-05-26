import csv

# singleton 패턴 파트
class Customer:
    _instance = None    # singleton 인스턴스 저장
    customer_list = []  # 고객 정보 저장 리스트
    csv_file = 'customers.csv' # 고객 정보 및 렌탈 정보를 csv 파일에 저장
    
    def __new__(cls, *args, **kwargs):  # singleton 패턴 구현
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._initiated = False
        return cls._instance    # 이미 인스턴스가 존재하면 기존 인스턴스 반환

    def __init__(self):
        if not self._initiated: # 고객 정보 초기화
            self.name = None
            self.phone = None
            self.email = None
            self.rent_history = []
            self._initiated = True # True로 바꿨기에 더 이상 초기화 되지 않음
            self.load_customers_from_csv()  # csv 파일에서 고객 정보 불러옴 
            #-> 기존에 저장된 고객 정보 메모리에 로드해서, 조회 및 수정 가능하게 할 수 있음 (아래 메소드 있어요)

    def add_customer(self, name, phone, email): # 고객 추가 메소드
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
        print("\n\t"+ name + "님이 회원 등록이 되었습니다.")
        self.save_customers_to_csv()
        return True

    def search_customer(self, phone):   # 고객 검색 메소드 (추후 검색 방식 변경 가능. 의견주세요! ... 저는 이름으로 검색하는게 좋은 것 같기도 해요 ㅎ)
        for customer_info in Customer.customer_list:    # 리스트에 있는 고객 정보 순차 검색
            if customer_info['phone'] == phone: # 해당하는 고객이 있으면
                self.name = customer_info['name']
                self.phone = customer_info['phone']
                self.email = customer_info['email']
                self.rent_history = customer_info['rent_history']
                self.view_customer_info()   # 고객 정보 출력 (아래 메소드 있어요)
                return customer_info
        print("회원 정보를 찾을 수 없습니다.")
        return None

    def update_customer_info(self, customer_info, field, new_value):    # 고객 정보 수정 메소드
        if field == 'phone':    # 지금은 번호랑 이메일만 수정하게 했는데 이름도 바꿀 수 있게 할까요? + 바꾸려는거 선택해서 바꿀 수 있게?
            # ex) 전화번호만 바꾸고싶으면 전화번호만 바꿀 수 있게 -> 근데 이런 디테일까지는 필요 없을 것 같기도 하고요..
            customer_info['phone'] = new_value
        elif field == 'email':
            customer_info['email'] = new_value
        self.name = customer_info['name']
        self.phone = customer_info['phone']
        self.email = customer_info['email']
        print("  회원 정보가 성공적으로 업데이트 되었습니다.")
        self.save_customers_to_csv()

    def view_customer_info(self):   # 고객 탐색 메소드
        print(f"\t\t이름: {self.name}")
        print(f"\t\t전화번호: {self.phone}")
        print(f"\t\t이메일: {self.email}")
        print("\t\t대여 기록:")
        for history in self.rent_history:
            print(history)

    def add_rent_history(self, customer_info, rent_info):   # 대여 내역 추가
        customer_info['rent_history'].append(rent_info)
        self.save_customers_to_csv()

    def save_customers_to_csv(self):    # csv파일에 고객 정보 저장. 근데 current_rent 하나 추가해야할듯
        with open(Customer.csv_file, 'w', newline='') as csvfile:
            fieldnames = ['name', 'phone', 'email', 'rent_history']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for customer in Customer.customer_list:
                customer_copy = customer.copy()
                customer_copy['rent_history'] = str(customer_copy['rent_history'])
                writer.writerow(customer_copy)
    
    def load_customers_from_csv(self):  # csv파일로부터 고객 정보 읽음
        try:
            with open(Customer.csv_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row['rent_history'] = eval(row['rent_history'])
                    Customer.customer_list.append(row)
        except FileNotFoundError:
            print("CSV 파일을 찾을 수 없습니다.")
