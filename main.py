from rent import RentalServiceFacade
from return_car import RentalReturnProcessor, LateReturnFeeStrategy, CardPaymentStrategy, AccountPaymentStrategy, PayPaymentStrategy
from customer_singleton import Customer

def rental_main():
    check_user = input("가입한 회원인가요? (네/아니오)")
    if check_user =="네":
        input("성함을 입력해주세요: ")
    # else: 
    model_type = input("차종을 입력하세요 (전기차, SUV, 소형, 중형, 대형, 밴): ")
    rental_days = int(input("대여기간을 입력하세요: "))
    
    options = {
        "navigation": "네비게이션",
        "insurance": "보험",
        "bikerack": "바이크 랙",
        "childseat": "유아용 카시트",
        "wifi": "와이파이",
        "sunroof": "선루프"
    }
        
    print("옵션 리스트:")
    for i, (key, value) in enumerate(options.items(), 1):
        print(f"{i}. {value}")

    while True:
        try:
            selected_numbers = map(int, input("추가하고 싶은 옵션의 번호를 쉼표로 구분하여 입력하세요 (예: 1, 3, 5): ").split(','))
            selected_options = [list(options.keys())[i - 1] for i in selected_numbers if 1 <= i <= len(options)]
            break
        except ValueError:
            print("잘못된 입력입니다. 번호만 입력해주세요.")
        except IndexError:
            print("범위를 벗어난 번호가 있습니다. 올바른 번호를 입력해주세요.")

    rental_service = RentalServiceFacade()
    rental_info = rental_service.rent_car(model_type, rental_days, selected_options)
    return rental_info

def return_main(rental_info):
    return_date_str = input("실제 대여 날짜를 입력하세요:")

    fee_strategies = [LateReturnFeeStrategy()]
    payment_strategy = CardPaymentStrategy()  # 또는 AccountPaymentStrategy(), PayPaymentStrategy()

    processor = RentalReturnProcessor(fee_strategies, payment_strategy)
    processor.process_return(rental_info, return_date_str)

def customer_main():
    customer = Customer()
    
    while True:
        print("1. 회원 등록")
        print("2. 회원 검색")
        print("3. 회원 정보 수정")
        print("4. 종료")
        choice = input("선택: ")
        
        if choice == '1':
            print("회원 등록을 선택하셨습니다. 정보를 입력해주세요.")
            try:
                name, phone, email = input("입력: 이름 전화번호 이메일: ").split()
                customer.add_customer(name, phone, email)
            except:
                print("잘못 입력하셨습니다.")
        
        elif choice == '2':
            print("회원 검색을 선택하셨습니다.")
            phone = input("전화번호를 입력하세요: ")
            customer.search_customer(phone)
        
        elif choice == '3':
            print("회원 정보 수정을 선택하셨습니다. 회원 전화번호:")
            phone = input("전화번호를 입력하세요: ")
            customer_info = customer.search_customer(phone)
            if customer_info:
                print("수정하실 정보를 선택하세요 (전화번호/이메일):")
                field = input("선택: ")
                if field == '전화번호':
                    new_phone = input("새로운 전화번호를 입력하세요: ")
                    customer.update_customer_info(customer_info, 'phone', new_phone)
                elif field == '이메일':
                    new_email = input("새로운 이메일을 입력하세요: ")
                    customer.update_customer_info(customer_info, 'email', new_email)
                else:
                    print("잘못 입력하셨습니다.")
        
        elif choice == '4':
            print("메인 메뉴로 이동합니다.")
            break
        
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

def main():
    while True:
        print("1. 차량 렌트")
        print("2. 차량 반납")
        print("3. 회원 관리")
        print("4. 종료")
        choice = input("선택: ")

        if choice == '1':
            rental_info = rental_main()
        elif choice == '2':
            return_main(rental_info)
        elif choice == '3':
            customer_main()
        elif choice == '4':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()