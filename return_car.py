from abc import ABC, abstractmethod
from rent import RentalServiceFacade


class ExcessFeeStrategy(ABC): # strategy 패턴
    @abstractmethod
    def calculate_fee(self, rental_info):
        pass

class LateReturnFeeStrategy(ExcessFeeStrategy):
    def calculate_fee(self, rental_info):
        suppose_date = rental_info['suppose_date']
        return_date = rental_info['return_date']
        if return_date > suppose_date:
            extra_days = return_date - suppose_date
            return extra_days * rental_info['car'].base_cost
        return 0

# class DamageFeeStrategy(ExcessFeeStrategy):
#     def calculate_fee(self, rental_info)

class PaymentStrategy(ABC): # strategy 패턴
    @abstractmethod
    def pay(self, amount):
        pass

class CardPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"신용카드로 {amount} 원이 결제되었습니다.")

class AccountPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"계좌이체로 {amount} 원이 결제되었습니다.")

class PayPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"페이로 {amount} 원이 결제되었습니다.")


class RentalReturnProcessor:
    def __init__(self, fee_strategies, payment_strategy):
        self.fee_strategies = fee_strategies
        self.payment_strategy = payment_strategy

    def process_return(self, rental_info, return_date):
        total_fee = 0
        rental_info['return_date'] = return_date

        for strategy in self.fee_strategies:
            total_fee += strategy.calculate_fee(rental_info)
        
        is_late = return_date > rental_info['due_date']
        if is_late:
            late_days = (return_date - rental_info['due_date']).days
            total_fee += rental_info['car'].base_cost * late_days

        print(f"Total excess fee: {total_fee}")
        self.payment_strategy.pay(total_fee)

# # fee_strategies = [LateReturnFeeStrategy(), DamageFeeStrategy()]
# fee_strategies = LateReturnFeeStrategy()

# payment_strategy = CardPaymentStrategy() # 또는 AccountPaymentStrategy(), PayPaymentStrategy()

# processor = RentalReturnProcessor(fee_strategies, payment_strategy)

# processor.process_return(rental_info)