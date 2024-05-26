import os
from rent import RentalServiceFacade
from return_car import RentalReturnProcessor, LateReturnFeeStrategy, CardPaymentStrategy, AccountPaymentStrategy, PayPaymentStrategy
from customer_singleton import Customer
from datetime import datetime, timedelta
from receipt_visual import print_receipt

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
            while True:
                clear_screen()
                print_top_bar("차량 렌트  ")
                print("  **취소를 원하시면 '취소'를 입력해주세요**") 
                phone = input("\t전화번호를 입력하세요: ").strip()
                if phone.lower() == '취소':  # '취소' 입력 시 루프 종료
                    break
                customer_info = customer.search_customer(phone)
                if customer_info:
                    input("\n\t계속 진행하시려면 Enter를 눌러주세요.")
                    break
                else:
                    input("\n\t다시 입력하시려면 Enter를 눌러주세요.")
            
            if phone.lower() == '취소':  # 메인 메뉴로 돌아감
                continue

            while True:
                clear_screen()
                print_top_bar("차량 렌트  ")
                print("\t전기차, SUV, 소형, 중형, 대형, 밴")
                model_type = input("\t차종을 입력하세요: ").strip()
                if model_type in ["전기차", "SUV", "소형", "중형", "대형", "밴"]:
                    break
                else:
                    input("\n\t잘못된 차종입니다.\n\t다시 입력하시려면 Enter를 눌러주세요.")

            while True:
                try:
                    clear_screen()
                    print_top_bar("차량 렌트  ")
                    rental_days = int(input("\t렌트 기간(일)을 입력하세요: ").strip())
                    if rental_days > 0:
                        break
                    else:
                        print("\n\t기한을 잘못 입력하셨습니다.\n\t1 이상의 숫자여야 합니다.") # 0을 입력한 경우 오류 처리
                except ValueError:
                    print("\n\t잘못 입력하셨습니다.\n\t1 이상의 숫자여야 합니다.") # 기한 이외의 것을 입력한 경우 오류 처리
                input("\n\t다시 입력하시려면 Enter를 눌러주세요.")
            
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
                    selected_numbers = map(int, input("\n\t추가하고 싶은 옵션의 번호를\n\t쉼표로 구분하여 입력하세요\n\t(예: 1, 3, 5): ").split(','))
                    selected_options = [list(options.keys())[i - 1] for i in selected_numbers if 1 <= i <= len(options)]
                    
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
                    customer.print_rent_info(customer_info['current_rent'])
                    input("\n\t확인 후 Enter를 눌러주세요")
                    break
                except ValueError:
                    print("\n\t잘못 입력하셨습니다.") # 옵션 입력 형식에 맞지 않는 경우 오류 처리 
                    input("\n\t다시 입력하시려면 Enter를 눌러주세요")
                    clear_screen()
        
        
        elif choice == '2':
            while True:
                clear_screen()
                print_top_bar("차량 반납")
                print("  **취소를 원하시면 '취소'를 입력해주세요**")
                phone = input("\t전화번호를 입력하세요: ").strip()
                if phone.lower() == '취소':  
                    break
                customer_info = customer.search_customer(phone)
                if customer_info:
                    if 'current_rent' in customer_info and customer_info['current_rent']:
                        input("\n  대여 정보가 맞으시면 Enter를 눌러주세요")
                        break
                    else:
                        print("\n\t대여 정보가 없습니다.")
                        input("\n\t메인으로 돌아가시려면 Enter를 눌러주세요")
                        break
                else:
                    input("\n\t다시 입력하시려면 Enter를 눌러주세요")
            
            if phone.lower() == '취소':  # 메인 메뉴로 돌아감
                continue
            
            if customer_info and customer_info['current_rent']:
                while True:
                    clear_screen()
                    print_top_bar("차량 반납")
                    rent_info = customer_info['current_rent']
                    print("\t< 현재 대여 정보 >")
                    customer.print_rent_info(customer_info['current_rent'])
                    
                    return_date_str = input("\n\t반납 날짜를 입력하세요\n\t(YYYY-MM-DD): ").strip()
                    try:
                        return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
                        break  # 날짜 형식이 올바르면 루프 종료
                    except ValueError:
                        print("\t잘못된 날짜 형식입니다.")
                        input("\n\t다시 입력하시려면 Enter를 눌러주세요")
                
                due_date = datetime.strptime(rent_info['due_date'], "%Y-%m-%d").date()
                rent_info['return_date'] = return_date_str

                if return_date > due_date:
                    overdue_days = (return_date - due_date).days
                    fee_strategies = [LateReturnFeeStrategy(overdue_days)]
                else:
                    fee_strategies = []

                while True:
                    payment_method = input("\n\t결제 방법을 입력해주세요\n\t(card/account/pay): ").strip()
                    if payment_method == "card":
                        payment_strategy = CardPaymentStrategy()
                        break
                    elif payment_method == "account":
                        payment_strategy = AccountPaymentStrategy()
                        break
                    elif payment_method == "pay":
                        payment_strategy = PayPaymentStrategy()
                        break
                    else:
                        print("\t잘못된 결제 방법입니다.")
                        input("\n\t다시 입력하시려면 Enter를 눌러주세요")
                
                clear_screen()
                print_top_bar()
                processor = RentalReturnProcessor(fee_strategies, payment_strategy)
                processor.process_return(rent_info, return_date)                 
                total_fee, final_cost, rental_info = processor.process_return(rent_info, return_date)

                customer.return_car(customer_info, return_date_str) 

                print("\t차량이 반납되었습니다.")
                
                #영수증 출력
                print_receipt(rent_info, payment_method, final_cost, total_fee)

                input("\n\t계속 진행하시려면 Enter를 눌러주세요")

            else:
                print("\t대여 정보가 없습니다.")
                input("\n\t계속 진행하시려면 Enter를 눌러주세요")
                input("\n\t확인 후 Enter를 눌러주세요")

        
        elif choice == '3':
            clear_screen()
            print_top_bar("회원 등록  ")
            print("  **취소를 원하시면 '취소'를 입력해주세요**")
            name = input("\t이름을 입력하세요: ").strip()
            if name.lower() == '취소':  
                continue
            phone = input("\t전화번호를 입력하세요: ").strip()
            if phone.lower() == '취소':  
                continue
            email = input("\t이메일을 입력하세요: ").strip()
            if email.lower() == '취소':  
                continue
            customer.add_customer(name, phone, email)
            input("\n   메인화면으로 돌아가려면 Enter를 눌러주세요")
        
        elif choice == '4':
            while True:
                customer_info = None
                clear_screen()
                print_top_bar("회원 검색  ")
                print("  **취소를 원하시면 '취소'를 입력해주세요**")           
                phone = input("\t전화번호를 입력하세요: ").strip()
                if phone.lower() == '취소':  
                    break
                customer_info = customer.search_customer(phone)
                if customer_info:
                    input("\n  회원 정보를 확인 후 Enter를 눌러주세요.")
                    break
                else:
                    input("\n  다시 입력하시려면 Enter를 눌러주세요.")
                    
            if phone.lower() == '취소':  # 메인 메뉴로 돌아감
                continue
                            
        elif choice == '5':
            while True:
                clear_screen()
                print_top_bar("회원 정보 수정")
                print("  **취소를 원하시면 '취소'를 입력해주세요**")
                phone = input("\t전화번호를 입력하세요: ").strip()
                if phone.lower() == '취소':  
                    break
                customer_info = customer.search_customer(phone)
                if customer_info:
                    input("\n\t수정을 원하시면 Enter를 눌러주세요.")
                    break
                else:
                    input("\n\t다시 입력하시려면 Enter를 눌러주세요.")

            if phone.lower() == '취소':  # 메인 메뉴로 돌아감
                continue

            if customer_info:
                while True:
                    clear_screen()
                    print_top_bar("회원 정보 수정")
                    field = input("\t수정할 필드를 입력하세요\n\t(phone/email): ").strip()
                    if field in ["phone", "email"]:
                        while True:
                            new_value = input(f"\t{field}의 새로운 값을 입력하세요\n\t: ").strip()
                            if customer.update_customer_info(customer_info, field, new_value):
                                input("\n\t메인화면으로 돌아가시려면\n\tEnter를 눌러주세요.")
                                break
                            else:
                                input("\n\t다시 입력하시려면 Enter를 눌러주세요.")
                        break
                    else:
                        print("\t잘못된 필드입니다.") # phone, email 이외의 입력 시 오류 처리
                        input("\n\t다시 입력하시려면 Enter를 눌러주세요.")
                continue # 메인 메뉴로 돌아감
       
        
        elif choice == '6':
            break
        
        else:
            input("\n\t잘못된 옵션입니다.\n\t다시 시도하시려면 Enter를 눌러주세요.")

if __name__ == "__main__":
    main()
