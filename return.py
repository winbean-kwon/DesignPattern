from abc import ABC, abstractmethod
from rent import RentalServiceFacade


class ExcessFeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, rental_info):
        pass

class LateReturnFeeStrategy(ExcessFeeStrategy):
    def calcuate_fee(self, rental_info):
        suppose_date = rental_info['suppose_date']
        return_date = rental_info['return_date']
        if return_date > suppose_date:
            extra_days = return_date - suppose_date
            return extra_days * rental_info['car'].base_cost
        return 0

# class DamageFeeStrategy(ExcessFeeStrategy):
#     def calculate_fee(self, rental_info)

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CardPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying {amount} using Card.")

class AccountPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying {amount} using Account.")

class PayPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying {amount} using Pay service.")


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

def main():
    rental_service = RentalServiceFacade()
    
    rental_info = rental_service.main()
    
    return_date_str = input("반납 날짜를 입력하세요 (YYYY-MM-DD): %d")
    
    fee_strategies = LateReturnFeeStrategy()

    payment_strategy = CardPaymentStrategy()  # 또는 AccountPaymentStrategy(), PayPaymentStrategy()

    processor = RentalReturnProcessor(fee_strategies, payment_strategy)

    processor.process_return(rental_info, return_date_str)

if __name__ == "__main__":
    main()

# # fee_strategies = [LateReturnFeeStrategy(), DamageFeeStrategy()]
# fee_strategies = LateReturnFeeStrategy()

# payment_strategy = CardPaymentStrategy() # 또는 AccountPaymentStrategy(), PayPaymentStrategy()

# processor = RentalReturnProcessor(fee_strategies, payment_strategy)

# processor.process_return(rental_info)