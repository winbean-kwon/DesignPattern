class Customer:
    _instance = None
    customer_list = []  # 회원 정보 저장
    
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
        print("회원 정보가 성공적으로 업데이트되었습니다.")
        self.view_customer_info()

    def view_customer_info(self):
        print("=== 회원 기본 정보 ===")
        print("이름:", self.name)
        print("전화번호:", self.phone)
        print("이메일:", self.email)
        print("")

    def view_history(self):
        if self.rent_history:
            print("=== 과거 이력 조회 ===")
            for history in self.rent_history:
                print("차종:", history['car_type'])
                print("대여기간:", history['rental_period'])
                print("옵션:", history['options'])
                print("초과금액:", history['overdue_fee'])
                print("총 금액:", history['total_amount'])
                print("결제상태:", history['payment_status'])
                print("")
        else:
            print("과거 이력이 없습니다.")

