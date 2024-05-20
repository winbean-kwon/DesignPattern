from abc import ABC, abstractmethod

# Car 클래스: 차종과 기본 요금 관리, 옵션 추가 메서드, 총 비용 계산 메서드
class Car:
    def __init__(self, model, base_cost):
        self.model = model
        self.base_cost = base_cost
        self.options = []
    
    def add_option(self, option):
        self.options.append(option)
    
    def calculate_total_cost(self, days):
        total_cost = self.base_cost * days
        for option in self.options:
            total_cost += option.cost * days
        return total_cost
    
    def display(self):
        print(f"차종: {self.model}")
        print(f"기본 요금: {self.base_cost}")
        print("옵션:")
        for option in self.options:
            print(f"- {option.name}: {option.cost}원/1일")
        print()

# CarFactory 클래스 - 추상 클래스
class AbstractCarFactory(ABC):
    @abstractmethod
    def create_car(self, model_type):
        pass

# CarFactory 클래스 - 구체 클래스
class CarFactory(AbstractCarFactory):
    def create_car(self, model_type):
        if model_type == "전기차":
            return Car("전기차", 20000)
        elif model_type == "SUV":
            return Car("SUV", 35000)
        elif model_type == "소형":
            return Car("소형차", 15000)
        elif model_type == "중형":
            return Car("중형차", 30000)
        elif model_type == "대형":
            return Car("대형차", 40000)
        elif model_type == "밴":
            return Car("밴", 50000)
        else:
            raise ValueError("존재하지 않는 차종입니다.")

# Option 클래스: 옵션과 추가 비용 정의
class Option:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

# CarOptionBuilder 클래스: 차량 옵션 추가
class CarOptionBuilder(ABC):
    @abstractmethod
    def add_navigation(self):
        pass
    
    @abstractmethod
    def add_insurance(self):
        pass
    
    @abstractmethod
    def add_childseat(self):
        pass
    
    @abstractmethod
    def add_bikerack(self):
        pass
    
    @abstractmethod
    def add_wifi(self):
        pass
    
    @abstractmethod
    def add_sunroof(self):
        pass
    
    @abstractmethod
    def build(self):
        pass

class ConcreteCarOptionBuilder(CarOptionBuilder):
    def __init__(self, car):
        self.car = car
    
    def add_navigation(self):
        self.car.add_option(Option("네비게이션", 1000))
        return self
    
    def add_insurance(self):
        self.car.add_option(Option("보험", 5000))
        return self
    
    def add_bikerack(self):
        self.car.add_option(Option("바이크 랙", 2000))
        return self
    
    def add_childseat(self):
        self.car.add_option(Option("유아용 카시트", 3000))
        return self
    
    def add_wifi(self):
        self.car.add_option(Option("와이파이", 2500))
        return self
    
    def add_sunroof(self):
        self.car.add_option(Option("선루프", 4000))
        return self
    
    def build(self):
        return self.car


# RentalServiceFacade 클래스 - 내부에 RentStage1, RentStage2, RentStage3를 가진다
# RentStage1 : 자동차 모델 선택
class RentStage1:
    def __init__(self, car_factory):
        self.car_factory = car_factory
    
    def select_car(self, model_type):
        return self.car_factory.create_car(model_type)

# RentStage2 : 옵션 추가
class RentStage2:
    def __init__(self, option_builder):
        self.option_builder = option_builder
    
    def add_options(self, car, options):
        builder = self.option_builder(car)
        for option in options:
            getattr(builder, f"add_{option}")()
        return builder.build()

# RentStage3 : 최종 비용 산정
class RentStage3:
    def finalize_rental(self, car, rental_days):
        total_cost = car.calculate_total_cost(rental_days)
        car.display()
        print(f"{rental_days}일간 렌트시 최종 금액: {total_cost}원")

# RentalServiceFacade 클래스: 모든 대여 과정을 처리
class RentalServiceFacade:
    def __init__(self):
        self.stage1 = RentStage1(CarFactory())
        self.stage2 = RentStage2(ConcreteCarOptionBuilder)
        self.stage3 = RentStage3()
    
    def rent_car(self, model_type, rental_days, options):
        car = self.stage1.select_car(model_type)
        car = self.stage2.add_options(car, options)
        self.stage3.finalize_rental(car, rental_days)


def main():
    model_type = input("차종을 입력하세요 (전기차, SUV, 소형, 중형, 대형, 밴): ")
    rental_days = int(input("대여기간을 입력하세요: "))
    
    options = {
      "navigation" : "네비게이션",
      "insurance" : "보험",
      "bikerack" : "바이크 랙",
      "childseat" : "유아용 카시트",
      "wifi" : "와이파이",
      "sunroof" : "선루프"
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
    rental_service.rent_car(model_type, rental_days, selected_options)

if __name__ == "__main__":
    main()