# Chapter 09. 큰 문제는 작은 문제의 조합이다

> **이번 Chapter의 핵심은 `def` 문법을 외우는 것이 아닙니다.**  
> 큰 문제를 **작은 책임으로 나누고**, 각각에 이름을 붙인 뒤 하나씩 해결하는 사고를 익히는 것이 목표입니다.

---

## 코드가 길어질수록 필요한 것은 새로운 문법이 아닙니다

Chapter 08에서는 여러 조건과 여러 데이터를 하나의 문제 안에서 다뤘습니다.

예를 들어 학생 데이터를 한 명씩 확인하면서:

- 수료 여부를 판단하고
- 우수 여부를 판단하고
- 결과를 저장하고
- 마지막에 출력했습니다.

처음에는 이 모든 일을 한 곳에서 처리해도 괜찮습니다.

하지만 요구사항이 늘어나면 코드가 점점 길어집니다.

```text
학생 정보 확인
→ 합격 여부 판단
→ 등급 판단
→ 평균 계산
→ 결과 저장
→ 결과 출력
→ 또 다른 조건 처리
→ 또 다른 계산
```

이때 초보자는 흔히 이렇게 생각합니다.

> "함수를 써야 하나?"

하지만 더 먼저 해야 할 질문이 있습니다.

> **"이 긴 코드 안에는 서로 다른 일이 몇 개 들어 있는가?"**

함수는 그 다음입니다.

---

## 1. 큰 문제를 작은 담당자에게 나눠 준다고 생각합니다

학생 성적 처리라는 큰 업무를 생각해 봅시다.

이 업무 안에는 여러 역할이 있습니다.

```text
학생 성적 처리
├─ 합격 여부 판단
├─ 등급 판단
├─ 평균 계산
└─ 결과 출력
```

![큰 문제를 작은 역할로 나누기](https://raw.githubusercontent.com/GilbertMoon/python-foundation-bootcamp-student/main/images/chapter09/task-decomposition.jpg)

회사에서 한 사람이 모든 일을 처리하는 것보다 역할을 나누면 이해하기 쉬운 것처럼, 프로그램도 마찬가지입니다.

예를 들어:

```text
합격 여부 담당자
→ 점수를 받아 합격/불합격을 판단

등급 담당자
→ 점수를 받아 A/B/C 등급을 판단

평균 담당자
→ 학생 목록을 받아 평균을 계산

출력 담당자
→ 결과를 보기 좋게 출력
```

큰 프로그램을 이해하기 어려울 때는 **작은 담당자 여러 명이 협력한다고 생각**하면 좋습니다.

> **큰 문제 = 작은 문제들의 조합**

---

## 2. 먼저 함수 없이 긴 코드를 봅시다

다음 학생 데이터를 사용하겠습니다.

```python
students = [
    {"name": "민수", "score": 85},
    {"name": "지영", "score": 72},
    {"name": "현우", "score": 91}
]
```

학생마다 합격 여부와 등급을 판단하고, 마지막에는 전체 평균도 출력한다고 해봅시다.

```python
students = [
    {"name": "민수", "score": 85},
    {"name": "지영", "score": 72},
    {"name": "현우", "score": 91}
]

for student in students:
    name = student["name"]
    score = student["score"]

    if score >= 80:
        result = "합격"
    else:
        result = "불합격"

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"

    print(name, score, result, grade)


total = 0

for student in students:
    total = total + student["score"]

average = total / len(students)

print("평균:", average)
```

이 코드는 틀리지 않았습니다.

그리고 지금 단계에서는 충분히 좋은 코드입니다.

하지만 요구사항이 더 늘어난다면 한 파일 안에서 여러 책임이 섞이기 시작합니다.

```text
합격 판단 코드
등급 판단 코드
평균 계산 코드
출력 코드
```

여기서 바로 함수를 만들기 전에 **역할 이름부터 붙여 봅니다.**

---

## 3. 코드 덩어리에 역할 이름을 붙입니다

첫 번째 코드 덩어리입니다.

```python
if score >= 80:
    result = "합격"
else:
    result = "불합격"
```

이 부분은 무슨 일을 합니까?

```text
점수를 보고 합격 여부를 판단한다.
```

그렇다면 역할 이름을 붙일 수 있습니다.

```text
합격 여부 판단
```

영어 함수 이름 후보로는:

```python
get_result
```

처럼 생각할 수 있습니다.

다음 코드입니다.

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

역할은 무엇입니까?

```text
점수를 보고 등급을 판단한다.
```

함수 이름 후보:

```python
get_grade
```

다음 코드입니다.

```python
total = 0

for student in students:
    total = total + student["score"]

average = total / len(students)
```

역할:

```text
학생들의 평균 점수를 계산한다.
```

함수 이름 후보:

```python
calculate_average
```

이렇게 **코드보다 역할 이름을 먼저 찾는 것**이 중요합니다.

---

## 4. 함수는 코드를 감싸는 문법이 아니라 역할에 이름을 붙이는 방법입니다

앞의 역할을 실제 함수로 옮겨 보겠습니다.

### 합격 여부 판단

```python
def get_result(score):
    if score >= 80:
        return "합격"
    else:
        return "불합격"
```

### 등급 판단

```python
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    else:
        return "C"
```

### 평균 계산

```python
def calculate_average(students):
    total = 0

    for student in students:
        total = total + student["score"]

    return total / len(students)
```

이렇게 작성하면 각 코드 블록에 **이름과 책임**이 생깁니다.

![긴 코드를 이름 있는 함수 블록으로 나누기](https://raw.githubusercontent.com/GilbertMoon/python-foundation-bootcamp-student/main/images/chapter09/code-to-function-blocks.jpg)

Before에서는 여러 역할이 한 곳에 섞여 있었습니다.

After에서는 다음처럼 읽을 수 있습니다.

```text
get_result      → 합격 여부 판단
get_grade       → 등급 판단
calculate_average → 평균 계산
```

함수 이름만 봐도 무슨 일을 하는지 어느 정도 예상할 수 있습니다.

> **좋은 함수 이름은 작은 문제의 이름입니다.**

---

## 5. 함수를 만들기 전에 세 가지를 먼저 적습니다

함수를 설계할 때 바로 `def`를 입력하지 마세요.

먼저 다음 세 가지를 적어 봅니다.

```text
1. 입력은 무엇인가?
2. 무슨 일을 하는가?
3. 결과는 무엇인가?
```

![함수의 입력·하는 일·결과를 정리하는 책임 카드](https://raw.githubusercontent.com/GilbertMoon/python-foundation-bootcamp-student/main/images/chapter09/function-responsibility-cards.jpg)

예를 들어 `get_result`를 설계해 봅시다.

```text
함수 이름
get_result

입력
점수 score

하는 일
80점 이상인지 판단

결과
"합격" 또는 "불합격"
```

이렇게 정리한 뒤 코드로 옮기면:

```python
def get_result(score):
    if score >= 80:
        return "합격"
    return "불합격"
```

코드가 훨씬 자연스럽게 나옵니다.

---

## 6. `get_grade`도 같은 방식으로 설계합니다

코드부터 작성하지 않고 먼저 책임 카드를 만듭니다.

```text
함수 이름
get_grade

입력
점수 score

하는 일
점수 구간을 판단

결과
A / B / C 중 하나
```

그 다음 Python으로 옮깁니다.

```python
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    else:
        return "C"
```

여기서 중요한 것은 `def`, 괄호, 콜론이 아닙니다.

먼저 다음 질문에 답할 수 있어야 합니다.

> **이 함수는 무엇을 받아서 무엇을 판단하고 무엇을 돌려주는가?**

---

## 7. `calculate_average`는 입력의 크기가 조금 다릅니다

`get_result`와 `get_grade`는 학생 한 명의 점수만 필요합니다.

하지만 평균을 계산하려면 여러 학생이 필요합니다.

그래서 입력도 달라집니다.

```text
함수 이름
calculate_average

입력
학생 목록 students

하는 일
모든 학생의 점수를 더하고 학생 수로 나눈다

결과
평균 점수
```

Python 코드:

```python
def calculate_average(students):
    total = 0

    for student in students:
        total = total + student["score"]

    average = total / len(students)

    return average
```

여기서 함수 입력이 왜 `score`가 아니라 `students`인지 설명할 수 있어야 합니다.

평균은 학생 한 명만 보고 만들 수 없기 때문입니다.

> **함수의 입력은 그 기능이 일을 하기 위해 꼭 필요한 데이터입니다.**

---

## 8. 한 함수는 한 가지 역할에 집중합니다

다음 함수를 생각해 봅시다.

```python
def process_student(score):
    if score >= 80:
        result = "합격"
    else:
        result = "불합격"

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"

    print(result, grade)
```

동작은 합니다.

하지만 한 함수가 다음 일을 모두 합니다.

```text
합격 여부 판단
등급 판단
출력
```

처음에는 괜찮을 수 있지만 기능이 계속 커지면 함수도 다시 복잡해집니다.

그래서 기본 원칙을 하나 기억합니다.

> **한 함수는 가능하면 한 가지 역할에 집중한다.**

예를 들어:

```python
def get_result(score):
    ...


def get_grade(score):
    ...
```

처럼 분리하면 각 기능을 독립적으로 생각할 수 있습니다.

---

## 9. 함수 이름은 "무슨 일을 하는가"를 설명해야 합니다

다음 함수 이름을 비교해 봅시다.

```python
def func1(score):
    ...
```

이름만 보고는 무엇을 하는지 알기 어렵습니다.

반면:

```python
def get_result(score):
    ...
```

이라고 하면 역할을 예상할 수 있습니다.

또 다음도 비교해 봅시다.

```python
def calc(students):
    ...
```

무엇을 계산하는지 모호합니다.

```python
def calculate_average(students):
    ...
```

평균을 계산한다는 뜻이 더 분명합니다.

함수 이름을 정할 때 다음 질문을 해보세요.

```text
이 이름만 읽어도 역할을 설명할 수 있는가?
```

좋은 이름은 코드를 읽는 사람에게 설명서 역할을 합니다.

---

## 10. 같은 로직이 반복되면 함수 후보가 됩니다

프로그램에서 다음 코드가 여러 번 등장한다고 생각해 봅시다.

```python
if score >= 80:
    result = "합격"
else:
    result = "불합격"
```

이 로직을 여러 곳에 복사하면 기준이 바뀔 때 모두 수정해야 합니다.

예를 들어 합격 기준이 80점에서 85점으로 변경되었다면 여러 곳을 찾아 수정해야 합니다.

하지만 판단 로직이 하나의 함수에 있다면:

```python
def get_result(score):
    if score >= 85:
        return "합격"
    return "불합격"
```

한 곳만 수정하면 됩니다.

함수의 장점 중 하나는 **같은 책임을 한 곳에 모을 수 있다는 것**입니다.

하지만 무조건 중복 코드를 보면 함수부터 만들어야 한다는 뜻은 아닙니다.

먼저:

> **이 코드들이 정말 같은 역할을 하는가?**

를 확인해야 합니다.

---

## 11. 작은 함수는 따로 테스트하기 쉽습니다

`get_result()` 함수가 있다고 해봅시다.

```python
def get_result(score):
    if score >= 80:
        return "합격"
    return "불합격"
```

전체 학생 프로그램을 실행하지 않아도 이 기능만 확인할 수 있습니다.

실행 전에 먼저 예상합니다.

```text
79 → 불합격
80 → 합격
91 → 합격
```

그 다음 확인합니다.

```python
print(get_result(79))
print(get_result(80))
print(get_result(91))
```

예상 결과:

```text
불합격
합격
합격
```

이것은 Chapter 03에서 했던 경계값 테스트와 같습니다.

다만 이제 판단 로직이 작은 함수 안에 들어 있기 때문에 기능 하나만 독립적으로 확인하기 쉬워졌습니다.

---

## 12. 함수로 나눈 뒤 전체 프로그램을 다시 봅시다

먼저 작은 기능들을 정의합니다.

```python
def get_result(score):
    if score >= 80:
        return "합격"
    else:
        return "불합격"


def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    else:
        return "C"


def calculate_average(students):
    total = 0

    for student in students:
        total = total + student["score"]

    return total / len(students)
```

그리고 학생 데이터를 준비합니다.

```python
students = [
    {"name": "민수", "score": 85},
    {"name": "지영", "score": 72},
    {"name": "현우", "score": 91}
]
```

이제 전체 처리 코드는 다음처럼 읽힙니다.

```python
for student in students:
    name = student["name"]
    score = student["score"]

    result = get_result(score)
    grade = get_grade(score)

    print(name, score, result, grade)

average = calculate_average(students)
print("평균:", average)
```

아까보다 코드의 역할이 더 분명해졌습니다.

```text
학생 한 명씩 반복
→ 합격 여부는 get_result에게 맡김
→ 등급은 get_grade에게 맡김
→ 출력

전체 평균은 calculate_average에게 맡김
```

이제 큰 프로그램을 읽을 때 작은 기능 이름을 따라가면 됩니다.

---

## 13. 하지만 함수를 너무 잘게 나누는 것도 목적은 아닙니다

다음처럼 작성한다고 생각해 봅시다.

```python
def get_name(student):
    return student["name"]


def get_score(student):
    return student["score"]
```

이것이 항상 나쁜 코드는 아닙니다.

하지만 현재 문제에서는 오히려 함수가 너무 많아져 전체 흐름을 읽기 어려워질 수도 있습니다.

함수를 만들 때는 단순히 "한 줄도 함수로 만들 수 있다"가 기준이 아닙니다.

다음 질문을 기준으로 판단합니다.

```text
이 부분은 독립적인 역할인가?
이름을 붙일 가치가 있는가?
여러 곳에서 사용할 가능성이 있는가?
이 기능만 따로 테스트하면 도움이 되는가?
이렇게 나누면 전체 코드가 더 이해하기 쉬워지는가?
```

> **함수 분리의 목적은 함수 개수를 늘리는 것이 아니라, 문제를 이해하기 쉽게 만드는 것입니다.**

---

## 14. 함수를 만들기 전에 종이에 먼저 나눠 봅시다

새로운 문제를 하나 보겠습니다.

> 주문 목록을 확인해서 무료배송 여부를 판단하고, 할인 금액을 계산하고, 전체 주문 금액 평균을 구해 출력하세요.

바로 코드를 쓰지 마세요.

먼저 역할을 나눕니다.

```text
무료배송 여부 판단
할인 금액 계산
전체 주문 평균 계산
결과 출력
```

그 다음 함수 후보 이름을 정합니다.

```python
get_shipping_result(amount)
calculate_discount(amount)
calculate_order_average(orders)
```

그 다음 각 함수의 책임 카드를 작성합니다.

예:

```text
함수 이름
get_shipping_result

입력
주문 금액

하는 일
50,000원 이상인지 판단

결과
무료배송 / 배송비 있음
```

이렇게 하면 Python 코드를 쓰기 전에 이미 문제의 구조가 상당 부분 해결됩니다.

---

## 15. 직접 실습 1 - 함수 후보 찾기

다음 코드를 보고 바로 함수로 바꾸지 마세요.

먼저 역할 이름을 붙여 보세요.

```python
for student in students:
    score = student["score"]

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"

    print(student["name"], grade)
```

질문:

```text
반복문 안에는 서로 다른 역할이 몇 개인가?
어떤 부분을 독립적으로 떼어낼 수 있는가?
그 역할의 이름은 무엇인가?
필요한 입력은 무엇인가?
결과는 무엇인가?
```

---

## 16. 직접 실습 2 - 책임 카드 작성하기

다음 기능의 책임 카드를 작성하세요.

```text
점수가 90 이상이면 우수,
80 이상이면 합격,
그 외에는 보완 필요를 반환한다.
```

다음 형식으로 먼저 작성합니다.

```text
함수 이름:
입력:
하는 일:
결과:
```

그 다음 Python 함수로 옮겨 보세요.

---

## 17. 직접 실습 3 - 평균 계산 함수 만들기

다음 데이터가 있습니다.

```python
products = [
    {"name": "키보드", "price": 45000},
    {"name": "마우스", "price": 28000},
    {"name": "모니터", "price": 320000}
]
```

문제:

> 상품들의 평균 가격을 반환하는 `calculate_average_price()` 함수를 만들어 보세요.

바로 코드로 가지 말고 먼저 씁니다.

```text
입력은 무엇인가?
반복해야 하는 대상은 무엇인가?
누적해야 하는 값은 무엇인가?
최종 결과는 무엇인가?
```

Chapter 06의 집계 사고가 함수 안으로 들어가는 문제입니다.

---

## 18. 직접 실습 4 - 긴 문제를 작은 기능으로 나누기

다음 요구사항을 읽어 봅시다.

> 학생 목록에서 수료 여부를 판단하고, 등급을 계산하고, 수료 학생 수를 구하고, 전체 평균을 출력하세요.

코드는 작성하지 않고 먼저 기능만 나눕니다.

예:

```text
기능 1:
기능 2:
기능 3:
기능 4:
```

그 다음 각각에 함수가 필요한지 판단합니다.

모든 기능을 반드시 함수로 만들 필요는 없습니다.

중요한 것은 **큰 문제를 작은 책임으로 나누어 설명할 수 있는가**입니다.

---

## 19. 초보자가 자주 하는 실수

### 실수 1. `def`를 배우자마자 모든 코드를 함수로 감싼다

```python
def program():
    # 모든 코드
```

문법적으로는 함수지만 문제를 나누지 않았다면 책임 분리라는 목적은 달성하지 못했습니다.

---

### 실수 2. 함수 이름이 역할을 설명하지 못한다

```python
def func1():
    ...
```

함수 이름은 무엇을 하는지 설명할 수 있어야 합니다.

---

### 실수 3. 한 함수에 너무 많은 일을 넣는다

```text
판단 + 계산 + 저장 + 출력 + 입력
```

기능이 커졌다면 다시 "역할이 몇 개인가?"를 질문합니다.

---

### 실수 4. 입력이 무엇인지 생각하지 않고 함수를 만든다

함수 안에서 필요한 값을 어디서 가져와야 할지 몰라 전역 변수에 지나치게 의존하게 될 수 있습니다.

먼저:

```text
이 기능을 수행하려면 어떤 데이터가 꼭 필요한가?
```

를 생각합니다.

---

### 실수 5. 함수로 나누면 무조건 좋은 코드라고 생각한다

너무 잘게 나누면 오히려 흐름을 따라가기 어렵습니다.

**읽기 쉬워지는가? 책임이 분명해지는가?**가 기준입니다.

---

## 20. AI에게 묻기 전에 스스로 답해야 할 질문

이번 Chapter에서도 AI는 마지막 검토 단계에서 사용합니다.

함수를 만들기 전에 다음 질문에 스스로 답해 보세요.

```text
1. 전체 문제는 무엇인가?
2. 서로 다른 역할은 몇 개인가?
3. 각 역할에 이름을 붙이면 무엇인가?
4. 독립적으로 떼어낼 수 있는 역할은 무엇인가?
5. 각 기능에 필요한 입력은 무엇인가?
6. 각 기능의 결과는 무엇인가?
7. 함수로 나누었을 때 전체 코드가 더 이해하기 쉬워지는가?
```

권장 순서:

```text
문제 읽기
→ 역할 나누기
→ 함수 책임 카드 작성
→ 직접 구현
→ 실행 전 결과 예측
→ 실행
→ 오류 수정
→ 필요하면 공식 문서 확인
→ 마지막에 AI로 구조 검토
```

AI에게는 다음과 같이 질문할 수 있습니다.

```text
제가 이 프로그램을 get_result, get_grade, calculate_average로 분리했습니다.
각 함수가 한 가지 책임에 집중하고 있는지 검토해 주세요.
제가 먼저 작성한 구조를 기준으로 개선점만 알려 주세요.
```

AI에게 처음부터 "함수로 나눠줘"라고 맡기기보다 자신이 먼저 문제를 분해한 뒤 검토받는 것이 이번 수업의 목적에 더 맞습니다.

---

## 21. 이번 Chapter 완료 체크리스트

다음 질문에 스스로 답할 수 있는지 확인해 보세요.

```text
□ 긴 코드에서 서로 다른 역할을 찾아낼 수 있다.
□ 코드보다 먼저 역할 이름을 붙일 수 있다.
□ 함수가 필요한지 스스로 판단할 수 있다.
□ 함수의 입력 / 하는 일 / 결과를 설명할 수 있다.
□ 함수 이름만 보고 역할을 어느 정도 알 수 있게 작성할 수 있다.
□ 한 함수가 너무 많은 일을 하는지 판단할 수 있다.
□ 반복되는 로직을 함수로 모아야 하는 이유를 설명할 수 있다.
□ 작은 함수를 독립적으로 테스트할 수 있다.
```

이 질문들에 대부분 답할 수 있다면 이번 Chapter의 목표를 달성한 것입니다.

---

## 22. 다음 Chapter에서는 작은 기능을 연결합니다

이번 Chapter에서는 큰 문제를 다음처럼 나눴습니다.

```text
큰 문제
→ 작은 책임 찾기
→ 역할에 이름 붙이기
→ 함수로 분리하기
```

하지만 실제 프로그램은 함수 여러 개를 따로 만들어 놓는 것으로 끝나지 않습니다.

이 작은 기능들이 서로 값을 주고받으며 하나의 흐름으로 연결되어야 합니다.

예를 들어:

```text
학생 점수
→ get_result()
→ get_grade()
→ 결과 데이터 만들기
→ 출력
```

다음 Chapter에서는 **작은 기능들이 입력을 받고 결과를 돌려주며 하나의 프로그램으로 연결되는 구조**를 연습합니다.

특히 `print`와 `return`의 차이도 문제 해결 관점에서 살펴보게 됩니다.

---

# 이번 Chapter의 한 문장

> **함수는 `def` 문법이 아니라, 큰 문제를 작은 책임으로 나누고 그 책임에 이름을 붙이는 도구입니다.**

큰 문제가 보이면 바로 코드를 쓰지 마세요.

먼저 물어보세요.

> **"이 문제 안에는 서로 다른 일이 몇 개 들어 있지?"**

그 질문에서 함수 설계가 시작됩니다.

---

## 다음 Chapter — Chapter 10

다음은 [Chapter 10. 작은 기능을 연결하면 프로그램이 된다](../chapter10/chapter10.md)입니다.

지금까지 익힌 내용을 다음 문제 해결 단계로 연결해 보세요.
