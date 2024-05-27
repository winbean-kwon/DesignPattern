from datetime import datetime, timedelta
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_receipt(rental_info, payment_method, final_cost, total_fee):
    receipt = ""
    bar_length = 48  
    receipt += "─" * bar_length
    receipt += "\n🚗 Car Rent Service receipt\n"
    receipt += "─" * bar_length
    receipt += f"\n총 결제 금액: {final_cost}원\n"
    receipt += f"금액: {int(final_cost * 0.9)}원\n"
    receipt += f"부가세: {int(final_cost * 0.1)}원\n"
    receipt += "─" * bar_length

    car_info = rental_info['car']
    receipt += f"\n{car_info['model']}, {rental_info['rental_days']}일: {car_info['base_cost']}원/일\n"
    for option in car_info['options']:
        receipt += f"{option['name']}: {option['cost']}원/일\n"
    receipt += f"합산 금액: {rental_info['total_cost']}\n"
    receipt += f"추가 금액: {total_fee}원\n"

    if payment_method == "CardPaymentStrategy":
        payment_method_str = "card"
    elif payment_method == "AccountPaymentStrategy":
        payment_method_str = "account"
    elif payment_method == "PayPaymentStrategy":
        payment_method_str = "pay"
    else:
        payment_method_str = "unknown"
        
    receipt += f"결제 방식: {payment_method_str}\n"
    receipt += "─" * bar_length
    receipt += "\n저희 서비스를 이용해주셔서 감사합니다\n"
    receipt += "─" * bar_length
    print(receipt)

    print("\n영수증을 출력합니다")

def print_top_bar(title=""):
    current_time = datetime.now().strftime("%H:%M")
    battery = "🔋100%"
    signal = "📶"
    bar_length = 48  
    icons_length = len(current_time) + len(battery) +  len(signal) + 3
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