from rent import Car

def print_receipt(rental_info):
    print("🚗Car Rent Service🚗".center(48))
    print("총 결제 금액".ljust(24), f"{rental_info['total_cost']}원".rjust(24))
    print("부가세".ljust(24), f"{rental_info['total_cost'] * 0.1}원".rjust(24))
    print("-" * 48)
    print("고객명".ljust(24), rental_info['customer_name'].rjust(24))
    print("자동차".ljust(24), rental_info['model_type'].rjust(24))
    print("대출기간".ljust(24), f"{rental_info['rental_start_date']} ~ {rental_info['due_date']}".rjust(24))
    print("옵션".ljust(24), ", ".join(rental_info['options']).rjust(24))
    print("합산 금액".ljust(24), f"{rental_info['total_cost']}원".rjust(24))
    print("할인".ljust(24), f"{rental_info['discount']}원".rjust(24))
    print("-" * 48)
    print("저희 서비스를 이용해주셔서 감사합니다".center(48))
