from datetime import datetime, timedelta


class ExcessFeeStrategy:
    def calculate_fee(self, rental_info):
        pass

class LateReturnFeeStrategy(ExcessFeeStrategy):
    def __init__(self, overdue_days):
        self.overdue_days = overdue_days

    def calculate_fee(self, rental_info):
        due_date_str = rental_info['due_date']
        return_date_str = rental_info['return_date']
        
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
        
        if return_date > due_date:
            print("대여 일수가 초과되었습니다. 초과분까지 정산합니다.")
            extra_days = (return_date - due_date).days
            return extra_days * rental_info['car'].base_cost
        return 0

class RentalReturnProcessor:
    def __init__(self, fee_strategies, payment_strategy):
        self.fee_strategies = fee_strategies
        self.payment_strategy = payment_strategy

    def process_return(self, rental_info, return_date):
        total_fee = 0
        for strategy in self.fee_strategies:
            total_fee += strategy.calculate_fee(rental_info)
        self.payment_strategy.pay(total_fee)

class PaymentStrategy:
    def pay(self, amount):
        pass

class CardPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"신용카드로 {amount}원을 결제합니다.")

class AccountPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"계좌이체로 {amount}원을 결제합니다.")

class PayPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"모바일 페이로 {amount}원을 결제합니다.")


def update_rent_history(phone, rent_index, rent_info):
    pass