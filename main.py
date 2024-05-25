from rent import RentalServiceFacade
from return_car import RentalReturnProcessor, LateReturnFeeStrategy, CardPaymentStrategy, AccountPaymentStrategy, PayPaymentStrategy
from customer_singleton import Customer
from datetime import datetime, timedelta

def main():
    customer = Customer()
    rental_service = RentalServiceFacade()
    
    while True:
        print("\n차량 렌트 관리자 시스템입니다.")
        print("1. 차량 렌트")
        print("2. 차량 반납")
        print("3. 회원 등록")
        print("4. 회원 검색")
        print("5. 회원 정보 수정")
        print("6. 종료")

        choice = input("옵션을 선택하세요: ")
        
        if choice == '1':
            phone = input("전화번호를 입력하세요: ")
            customer_info = customer.search_customer(phone)
            if customer_info:
                model_type = input("차종을 입력하세요: ")
                rental_days = int(input("렌트 기간(일)을 입력하세요: "))
                options = {
                    'navigation': '네비게이션',
                    'insurance': '보험',
                    'bikerack': '바이크 랙',
                    'childseat': '유아용 카시트',
                    'wifi': '와이파이',
                    'sunroof': '선루프'
                }

                while True:
                    try:
                        print("옵션 리스트:")
                        for i, (key, value) in enumerate(options.items(), 1):
                            print(f"{i}. {value}")
                        selected_numbers = map(int, input("추가하고 싶은 옵션의 번호를 쉼표로 구분하여 입력하세요 (예: 1, 3, 5): ").split(','))
                        selected_options = [list(options.keys())[i - 1] for i in selected_numbers if 1 <= i <= len(options)]
                        rental_info = rental_service.rent_car(model_type, rental_days, selected_options)
                        
                        # 대여 시작일과 due_date 계산
                        rental_start_date = datetime.now().date()
                        rental_info['rental_start_date'] = rental_start_date.strftime("%Y-%m-%d")
                        due_date = rental_start_date + timedelta(days=rental_days)
                        rental_info['due_date'] = due_date.strftime("%Y-%m-%d")

                        customer.add_rent_history(customer_info, rental_info)
                        break
                    except ValueError:
                        print("잘못된 입력입니다. 번호만 입력해주세요.")
                    except IndexError:
                        print("범위를 벗어난 번호가 있습니다. 올바른 번호를 입력해주세요.")
        
        elif choice == '2':
            phone = input("전화번호를 입력하세요: ")
            customer_info = customer.search_customer(phone)
            if customer_info:
                rent_index = int(input("반납할 대여 기록 인덱스를 입력하세요: "))
                if rent_index < len(customer_info['rent_history']):
                    rent_info = customer_info['rent_history'][rent_index]
                    due_date = datetime.strptime(rent_info['due_date'], "%Y-%m-%d").date()
                    return_date_str = input("반납 날짜를 입력하세요 (YYYY-MM-DD): ")
                    return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
                    rent_info['return_date'] = return_date_str

                    # 초과 요금 계산
                    if return_date > due_date:
                        overdue_days = (return_date - due_date).days
                        fee_strategies = [LateReturnFeeStrategy(overdue_days)]
                    else:
                        fee_strategies = []

                    payment_method = input("결제 방법을 입력하세요 (card/account/pay): ")
                    if payment_method == "card":
                        payment_strategy = CardPaymentStrategy()
                    elif payment_method == "account":
                        payment_strategy = AccountPaymentStrategy()
                    elif payment_method == "pay":
                        payment_strategy = PayPaymentStrategy()
                    else:
                        print("잘못된 결제 방법입니다.")
                        continue
                    processor = RentalReturnProcessor(fee_strategies, payment_strategy)
                    processor.process_return(rent_info, return_date)

                    customer.update_rent_history(phone, rent_index, rent_info)
        
        elif choice == '3':
            name = input("이름을 입력하세요: ")
            phone = input("전화번호를 입력하세요: ")
            email = input("이메일을 입력하세요: ")
            customer.add_customer(name, phone, email)
        
        elif choice == '4':
            phone = input("전화번호를 입력하세요: ")
            customer.search_customer(phone)
        
        elif choice == '5':
            phone = input("전화번호를 입력하세요: ")
            customer_info = customer.search_customer(phone)
            if customer_info:
                field = input("수정할 필드를 입력하세요 (phone/email): ")
                new_value = input(f"{field}의 새로운 값을 입력하세요: ")
                customer.update_customer_info(customer_info, field, new_value)
        
        elif choice == '6':
            break
        
        else:
            print("잘못된 옵션입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()
