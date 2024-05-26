import os
from rent import RentalServiceFacade
from return_car import RentalReturnProcessor, LateReturnFeeStrategy, CardPaymentStrategy, AccountPaymentStrategy, PayPaymentStrategy
from customer_singleton import Customer
from datetime import datetime, timedelta
from recipe import print_receipt

def print_top_bar(title=""):
    current_time = datetime.now().strftime("%H:%M")
    battery = "🔋100%"
    signal = "📶"
    bar_length = 48  
    icons_length = len(current_time) + len(battery) + len(signal) + 3
    print("─" * bar_length)
    print(f"{signal} {current_time}{' ' * (bar_length - icons_length)}{battery}")
    print("─" * bar_length)
    if title:
        print(f"{title}".center(bar_length))
        print("─" * bar_length)

def print_bottom_bar(message=""):
    bar_length = 48 
    print("─" * bar_length)
    print(f"{message}".center(bar_length))
    print("─" * bar_length)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    customer = Customer()
    rental_service = RentalServiceFacade()
    
    while True:
        clear_screen()
        print_top_bar("차량 렌트 관리자 시스템        ")
        print("\t\t1. 차량 렌트")
        print("\t\t2. 차량 반납")
        print("\t\t3. 회원 등록")
        print("\t\t4. 회원 검색")
        print("\t\t5. 회원 정보 수정")
        print("\t\t6. 종료")
        print_bottom_bar("옵션을 선택하세요        ")
        
        choice = input().strip()
        
        if choice == '1':
            clear_screen()
            print_top_bar("차량 렌트  ")
            phone = input("\t전화번호를 입력하세요: ").strip()
            customer_info = customer.search_customer(phone)
            input("\n\t계속 진행하시려면 Enter를 눌러주세요")
            if customer_info:
                clear_screen()
                print_top_bar("차량 렌트  ")
                print("\t전기차, SUV, 소형, 중형, 대형, 밴")
                model_type = input("\t차종을 입력하세요: ").strip()
                rental_days = int(input("\t렌트 기간(일)을 입력하세요: ").strip())
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
                        clear_screen()
                        print_top_bar("차량 렌트 옵션 선택    ")
                        print("\t\t<옵션 리스트>")
                        for i, (key, value) in enumerate(options.items(), 1):
                            print(f"\t\t{i}. {value}")
                        selected_numbers = map(int, input("\n추가하고 싶은 옵션의 번호를\n쉼표로 구분하여 입력하세요 (예: 1, 3, 5): ").split(','))
                        selected_options = [list(options.keys())[i - 1] for i in selected_numbers if 1 <= i <= len(options)]    # selected_numbers가 옵션 개수보다 같거나 작을 때 selected_options에 추가
                        
                        clear_screen()
                        print_top_bar("차량 렌트  ")
                        for opt in selected_options:
                            print(f"\t{options[opt]} 옵션이 추가되었습니다.")
                        input("\n\t최종 렌트 정보를 확인하시겠습니까? \n\t\tEnter를 눌러주세요.")
                        clear_screen()
                        print_top_bar("렌트 정보 확인      ")
                        
                        rental_info = rental_service.rent_car(model_type, rental_days, selected_options)
                        
                        rental_start_date = datetime.now().date()   # 현재 날짜를 rental_start_date로 설정
                        rental_info['rental_start_date'] = rental_start_date.strftime("%Y-%m-%d")
                        due_date = rental_start_date + timedelta(days=rental_days)  # 렌탈 일 수를 입력 받아 현재 날짜에서 더함
                        rental_info['due_date'] = due_date.strftime("%Y-%m-%d") # 마찬가지로 due_date에 저장

                        customer.add_current_rent(customer_info, rental_info)
                        
                        print("\t렌트 정보가 추가되었습니다. ")
                        print("\n\t회원 이름: ", customer_info['name'])
                        print("\t차량 모델: ", model_type)
                        print("\t렌트 기간: ", rental_days, "일")
                        print("\t추가 옵션: ", ", ".join(options[opt] for opt in selected_options))
                        print("\t시작 날짜: ", rental_info['rental_start_date'])
                        print("\t반납 날짜: ", rental_info['due_date'])
                        input("\n\t계속 진행하시려면 Enter를 눌러주세요")
                        break
                    except ValueError:
                        print("\n\t잘못된 입력입니다. 다시 시도해주세요.")
                        input("\n\t계속 진행하시려면 Enter를 눌러주세요")
                        clear_screen()
        
        
        elif choice == '2':
            clear_screen()
            print_top_bar("차량 반납  ")
            phone = input("\t전화번호를 입력하세요: ").strip()
            customer_info = customer.search_customer(phone)
            input("\n\t대여 정보가 맞으시면 Enter를 눌러주세요")
            if customer_info and customer_info['current_rent']:
                clear_screen()
                print_top_bar("차량 반납  ")
                rent_info = customer_info['current_rent']
                print("\t- 현재 대여 정보 -")
                for key, value in rent_info.items():
                    print(f"\t{key}: {value}")
                return_date_str = input("\n\t반납 날짜를 입력하세요\n\t(YYYY-MM-DD): ").strip()
                try:
                    return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
                except ValueError:
                    print("\t잘못된 날짜 형식입니다.")
                    input("\n\t계속 진행하시려면 Enter를 눌러주세요")
                    continue

                due_date = datetime.strptime(rent_info['due_date'], "%Y-%m-%d").date()
                rent_info['return_date'] = return_date_str

                if return_date > due_date:
                    overdue_days = (return_date - due_date).days
                    fee_strategies = [LateReturnFeeStrategy(overdue_days)]
                else:
                    fee_strategies = []

                payment_method = input("\n\t결제 방법을 입력하세요\n\t(card/account/pay): ").strip()
                if payment_method == "card":
                    payment_strategy = CardPaymentStrategy()
                elif payment_method == "account":
                    payment_strategy = AccountPaymentStrategy()
                elif payment_method == "pay":
                    payment_strategy = PayPaymentStrategy()
                else:
                    print("\t\t잘못된 결제 방법입니다.")
                    input("\n\t계속 진행하시려면 Enter를 눌러주세요")
                    continue

                processor = RentalReturnProcessor(fee_strategies, payment_strategy)
                processor.process_return(rent_info, return_date)


                customer.return_car(customer_info, return_date_str)

                print("\t차량이 반납되었습니다.")
                print_receipt(rental_info)  # 반납 영수증 출력
                input("\n\t계속 진행하시려면 Enter를 눌러주세요")
            else:
                print("\t대여 정보가 없습니다.")
                input("\n\t계속 진행하시려면 Enter를 눌러주세요")
        
        elif choice == '3':
            clear_screen()
            print_top_bar("회원 등록  ")
            name = input("\t이름을 입력하세요: ").strip()
            phone = input("\t전화번호를 입력하세요: ").strip()
            email = input("\t이메일을 입력하세요: ").strip()
            customer.add_customer(name, phone, email)
            input("\n   메인화면으로 돌아가려면 Enter를 눌러주세요")
        
        elif choice == '4':
            clear_screen()
            print_top_bar("회원 검색  ")
            phone = input("\t전화번호를 입력하세요: ").strip()
            customer.search_customer(phone)
            input("\n\t확인 후 Enter를 눌러주세요")
        
        elif choice == '5':
            clear_screen()
            print_top_bar("회원 정보 수정   ")
            phone = input("\t전화번호를 입력하세요: ").strip()
            customer_info = customer.search_customer(phone)
            input("\n\t수정을 원하시면 Enter를 눌러주세요")
            if customer_info:
                clear_screen()
                print_top_bar("회원 정보 수정   ")
                field = input("\t수정할 필드를 입력하세요\n\t(phone/email): ").strip()
                new_value = input(f"\t{field}의 새로운 값을 입력하세요\n\t: ").strip()
                customer.update_customer_info(customer_info, field, new_value)
                input("\n  메인화면으로 돌아가시려면 Enter를 눌러주세요")
        elif choice == '6':
            break
        
        else:
            print("\n잘못된 옵션입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()
