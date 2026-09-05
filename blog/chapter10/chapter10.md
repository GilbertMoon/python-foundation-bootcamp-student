# Chapter 10. 작은 기능을 연결하면 프로그램이 된다

> **이번 Chapter의 핵심은 함수를 많이 만드는 것이 아닙니다.**  
> 작은 기능들이 **무엇을 입력받고, 무엇을 처리하고, 무엇을 다음 단계로 전달하는지** 연결해서 하나의 프로그램 흐름을 만드는 것이 목표입니다.

---

## 함수를 나누는 것만으로 프로그램이 완성되지는 않습니다

Chapter 09에서는 큰 문제를 작은 책임으로 나누었습니다.

예를 들어 학생 성적 프로그램을 다음처럼 나눴습니다.

```text
합격 여부 판단
등급 판단
평균 계산
결과 출력
```

각 기능을 함수로 만들 수 있습니다.

```python
get_result(score)
get_grade(score)
calculate_average(students)
print_result(...)
```

하지만 함수가 각각 따로 존재하기만 하면 아직 하나의 프로그램은 아닙니다.

이제 다음 질문이 필요합니다.

```text
각 함수는 무엇을 받아야 하는가?
함수가 만든 결과는 어디로 가야 하는가?
다음 함수는 그 결과를 어떻게 받아야 하는가?
전체 흐름은 어떤 순서로 이어져야 하는가?
```

> **작은 기능들이 서로 데이터를 주고받으며 연결될 때 하나의 프로그램이 됩니다.**

---

## 1. 함수는 작은 처리 기계라고 생각해 봅시다

함수를 어렵게 생각하지 말고 작은 처리 기계라고 생각해 봅시다.

```text
입력
 ↓
처리
 ↓
결과
```

![함수의 입력 처리 출력 구조](https://raw.githubusercontent.com/GilbertMoon/python-foundation-bootcamp-student/main/images/chapter10/function-input-process-output.jpg)

예를 들어 합격 여부를 판단하는 함수가 있습니다.

```python
def get_result(score):
    if score >= 80:
        return "합격"
    else:
        return "불합격"
```

이 함수의 구조를 사람의 말로 읽으면 다음과 같습니다.

```text
입력
→ score

처리
→ score가 80 이상인지 판단

결과
→ "합격" 또는 "불합격"
```

함수를 볼 때 가장 먼저 문법을 보지 말고 다음 세 가지를 확인하세요.

> **무엇을 받는가? → 무슨 일을 하는가? → 무엇을 돌려주는가?**

---

## 2. 매개변수는 함수가 일을 하기 위해 받는 입력입니다

다음 함수를 보겠습니다.

```python
def get_result(score):
    if score >= 80:
        return "합격"
    else:
        return "불합격"
```

여기서 `score`는 함수가 일을 하기 위해 필요한 입력입니다.

```python
get_result(85)
```

호출하면 함수 안에서 `score`는 85를 의미합니다.

```text
입력 85
→ 80 이상인지 판단
→ "합격"
```

다른 값을 넣으면 같은 기능을 다시 사용할 수 있습니다.

```python
get_result(72)
```

```text
입력 72
→ 80 이상인지 판단
→ "불합격"
```

즉 함수의 중요한 장점 중 하나는 **같은 처리 방법을 다른 데이터에 재사용할 수 있다는 것**입니다.

---

## 3. `return`은 함수가 만든 값을 밖으로 전달합니다

초보자가 함수에서 가장 자주 헷갈리는 부분이 `return`입니다.

다시 코드를 보겠습니다.

```python
def get_result(score):
    if score >= 80:
        return "합격"
    else:
        return "불합격"
```

`return`은 단순히 함수 실행을 끝내는 표시가 아닙니다.

여기서는 함수가 만든 결과를 **함수를 호출한 곳으로 돌려주는 역할**을 합니다.

```python
result = get_result(85)
```

실행 흐름은 다음과 같습니다.

```text
85를 함수에 전달
        ↓
get_result가 합격 여부 판단
        ↓
"합격"을 return
        ↓
result 변수에 저장
```

결과적으로:

```python
result == "합격"
```

이제 `result` 값은 다음 코드에서 다시 사용할 수 있습니다.

---

## 4. `print`와 `return`은 역할이 다릅니다

두 함수를 비교해 봅시다.

### 화면에 출력하는 함수

```python
def get_result(score):
    if score >= 80:
        print("합격")
    else:
        print("불합격")
```

이 함수는 사람에게 결과를 보여줍니다.

### 값을 돌려주는 함수

```python
def get_result(score):
    if score >= 80:
        return "합격"
    else:
        return "불합격"
```

이 함수는 결과를 다음 코드가 사용할 수 있도록 전달합니다.

![print와 return 비교](https://raw.githubusercontent.com/GilbertMoon/python-foundation-bootcamp-student/main/images/chapter10/print-vs-return.jpg)

간단히 구분하면 다음과 같습니다.

```text
print
→ 사람에게 화면으로 보여준다.

return
→ 다음 코드가 사용할 값을 전달한다.
```

예를 들어:

```python
result = get_result(85)
```

라고 값을 받아서:

```python
if result == "합격":
    print("수료 처리 대상입니다.")
```

처럼 다음 단계에서 사용할 수 있습니다.

> **함수끼리 연결하려면 화면에 보이는 것보다 값이 전달되는 것이 더 중요합니다.**

---

## 5. 등급 판단 함수도 같은 구조로 만듭니다

다음 기능은 점수를 받아 등급을 돌려줍니다.

```python
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    else:
        return "C"
```

이 함수도 같은 방식으로 분석할 수 있습니다.

```text
입력
→ score

처리
→ 점수 구간 판단

결과
→ A / B / C
```

예를 들어:

```python
grade = get_grade(91)
```

결과:

```python
grade == "A"
```

Chapter 09에서 중요한 것이 **한 함수의 책임**이었다면, Chapter 10에서는 그 함수의 **입력과 결과가 어디로 연결되는지**가 중요합니다.

---

## 6. 여러 함수를 하나의 흐름으로 연결해 봅시다

다음 학생 데이터가 있습니다.

```python
student = {
    "name": "민수",
    "score": 85
}
```

우리는 이 학생에게 다음 작업을 하고 싶습니다.

```text
학생 점수 확인
→ 합격 여부 판단
→ 등급 판단
→ 요약 문장 만들기
→ 출력
```

![여러 함수가 연결되는 파이프라인](https://raw.githubusercontent.com/GilbertMoon/python-foundation-bootcamp-student/main/images/chapter10/function-pipeline.jpg)

먼저 각 함수의 입력과 출력을 종이에 적어 봅시다.

```text
get_result
입력: score
출력: result

get_grade
입력: score
출력: grade

make_summary
입력: name, score, result, grade
출력: summary

print
입력: summary
출력: 화면 표시
```

이렇게 연결 관계를 먼저 정리하면 코드를 작성하기가 훨씬 쉬워집니다.

---

## 7. 요약 생성 함수를 만들어 봅시다

```python
def make_summary(name, score, result, grade):
    return f"{name} / {score}점 / {result} / {grade}등급"
```

이 함수는 여러 값을 입력받습니다.

```text
입력
→ name
→ score
→ result
→ grade
```

처리:

```text
여러 값을 하나의 문장으로 조합
```

결과:

```text
민수 / 85점 / 합격 / B등급
```

호출하면:

```python
summary = make_summary("민수", 85, "합격", "B")
```

이제 `summary` 값을 화면에 출력할 수 있습니다.

```python
print(summary)
```

---

## 8. 전체 프로그램 흐름을 먼저 사람의 말로 적습니다

함수를 모두 작성했다고 바로 실행 코드를 만들지 말고, 먼저 전체 흐름을 적어 봅시다.

```text
1. 학생 한 명을 선택한다.
2. 학생의 점수를 꺼낸다.
3. 점수를 get_result에 전달한다.
4. 반환된 합격 여부를 result에 저장한다.
5. 같은 점수를 get_grade에 전달한다.
6. 반환된 등급을 grade에 저장한다.
7. name, score, result, grade를 make_summary에 전달한다.
8. 반환된 요약 문장을 summary에 저장한다.
9. summary를 출력한다.
```

이 흐름은 이미 하나의 프로그램 설계입니다.

이제 Python으로 번역하면 됩니다.

---

## 9. 작은 함수를 연결해 하나의 프로그램을 만듭니다

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


def make_summary(name, score, result, grade):
    return f"{name} / {score}점 / {result} / {grade}등급"


student = {
    "name": "민수",
    "score": 85
}

name = student["name"]
score = student["score"]

result = get_result(score)
grade = get_grade(score)
summary = make_summary(name, score, result, grade)

print(summary)
```

예상 결과:

```text
민수 / 85점 / 합격 / B등급
```

여기서 가장 중요한 부분은 마지막 네 줄입니다.

```python
result = get_result(score)
grade = get_grade(score)
summary = make_summary(name, score, result, grade)
print(summary)
```

이 부분만 읽어도 프로그램의 큰 흐름을 이해할 수 있습니다.

```text
합격 판단
→ 등급 판단
→ 요약 생성
→ 출력
```

세부 조건문을 모두 읽지 않아도 전체 프로그램의 목적을 파악할 수 있습니다.

---

## 10. 여러 학생에게 같은 함수를 재사용합니다

이제 학생이 여러 명이라고 해봅시다.

```python
students = [
    {"name": "민수", "score": 85},
    {"name": "지영", "score": 72},
    {"name": "현우", "score": 91}
]
```

함수는 그대로 두고 반복문에서 재사용하면 됩니다.

```python
for student in students:
    name = student["name"]
    score = student["score"]

    result = get_result(score)
    grade = get_grade(score)
    summary = make_summary(name, score, result, grade)

    print(summary)
```

예상 결과:

```text
민수 / 85점 / 합격 / B등급
지영 / 72점 / 불합격 / C등급
현우 / 91점 / 합격 / A등급
```

여기서 함수의 재사용성이 분명해집니다.

```text
학생이 바뀐다
→ 입력값이 바뀐다
→ 같은 함수가 다시 사용된다
```

함수 내부 코드를 학생마다 다시 작성할 필요가 없습니다.

---

## 11. 평균 계산 함수도 전체 프로그램에 연결합니다

Chapter 09에서 만든 평균 계산 기능을 추가해 봅시다.

```python
def calculate_average(students):
    total = 0

    for student in students:
        total = total + student["score"]

    return total / len(students)
```

이 함수의 구조는:

```text
입력
→ students

처리
→ 모든 점수 합계 계산
→ 학생 수로 나눔

결과
→ average
```

전체 프로그램 마지막에 연결합니다.

```python
average = calculate_average(students)
print("전체 평균:", average)
```

학생 세 명의 평균은 약 다음과 같습니다.

```text
82.67
```

이제 프로그램은 다음 두 가지 일을 합니다.

```text
각 학생 처리
→ 합격 여부
→ 등급
→ 요약 출력

전체 학생 처리
→ 평균 계산
→ 평균 출력
```

---

## 12. 세부 기능과 전체 흐름을 분리해서 봅니다

프로그램이 커질수록 두 가지 수준을 나누어 보는 습관이 중요합니다.

### 세부 기능

```python
def get_result(score):
    ...


def get_grade(score):
    ...


def make_summary(name, score, result, grade):
    ...


def calculate_average(students):
    ...
```

각 함수가 **어떻게** 일을 하는지 담당합니다.

### 전체 흐름

```python
for student in students:
    result = get_result(student["score"])
    grade = get_grade(student["score"])
    summary = make_summary(
        student["name"],
        student["score"],
        result,
        grade
    )
    print(summary)

average = calculate_average(students)
print("전체 평균:", average)
```

이 부분은 프로그램이 **어떤 순서로** 일을 하는지 보여줍니다.

이렇게 나누면 긴 프로그램도 이해하기 쉬워집니다.

> **함수는 세부 작업을 숨기고, 전체 흐름은 프로그램의 이야기를 보여줍니다.**

---

## 13. 데이터가 끊기는 지점을 찾아야 합니다

함수 연결에서 자주 발생하는 문제는 **필요한 값이 다음 단계로 전달되지 않는 것**입니다.

예를 들어:

```python
def get_result(score):
    if score >= 80:
        print("합격")
    else:
        print("불합격")

result = get_result(85)
print(result)
```

화면에는 다음처럼 보일 수 있습니다.

```text
합격
None
```

왜 `None`이 나올까요?

`get_result()` 함수는 화면에 글자를 출력했지만 값을 `return`하지 않았기 때문입니다.

즉 데이터 흐름이 함수 안에서 끊겼습니다.

수정:

```python
def get_result(score):
    if score >= 80:
        return "합격"
    else:
        return "불합격"
```

함수 연결 문제를 만났을 때는 다음 질문을 하세요.

```text
이 함수의 입력은 제대로 들어왔는가?
함수 내부에서 값은 제대로 만들어졌는가?
그 값을 return 했는가?
호출한 쪽에서 반환값을 받았는가?
다음 함수에 올바르게 전달했는가?
```

---

## 14. 실행 전에 데이터 흐름을 손으로 추적합니다

민수의 점수 85가 프로그램을 통과한다고 생각해 봅시다.

| 단계 | 입력 | 처리 | 결과 |
|---|---|---|---|
| 1 | 85 | `get_result` | 합격 |
| 2 | 85 | `get_grade` | B |
| 3 | 민수, 85, 합격, B | `make_summary` | 요약 문장 |
| 4 | 요약 문장 | `print` | 화면 표시 |

이 표를 작성할 수 있다면 함수가 어떻게 연결되는지 이해한 것입니다.

코드를 실행하기 전에 먼저 예측해 보세요.

> **입력값이 어느 함수로 들어가고, 어떤 값으로 바뀌어 다음 단계로 이동하는가?**

---

## 15. 함수 파이프라인은 데이터 처리의 기본 구조입니다

이번에 만든 흐름을 다시 봅시다.

```text
학생 데이터
→ 합격 판정
→ 등급 판정
→ 요약 생성
→ 출력
```

이런 구조를 **파이프라인(Pipeline)**처럼 생각할 수 있습니다.

각 단계는 자신의 일을 하고 다음 단계가 사용할 값을 전달합니다.

이 사고는 앞으로 훨씬 넓게 사용됩니다.

```text
원본 데이터
→ 정제
→ 변환
→ 분석
→ 결과 생성
```

데이터 분석에서도 비슷합니다.

```text
CSV 읽기
→ 필요한 행 필터링
→ 값 계산
→ 집계
→ 시각화
```

웹 프로그램에서도 비슷합니다.

```text
사용자 입력
→ 검증
→ 처리
→ 데이터 저장
→ 결과 응답
```

즉 지금 배우는 함수 연결은 작은 Python 예제에만 필요한 기술이 아닙니다.

> **데이터가 여러 처리 단계를 지나 최종 결과가 되는 흐름을 설계하는 연습입니다.**

---

## 16. 직접 실습해 봅시다

### 실습 1. 함수의 입력과 결과 먼저 적기

다음 함수 이름을 보고 코드를 작성하기 전에 입력과 결과를 적으세요.

```text
get_result
get_grade
calculate_average
make_summary
```

형식:

```text
함수 이름:
입력:
하는 일:
결과:
```

---

### 실습 2. `print`를 `return`으로 바꾸기

다음 함수를 수정하세요.

```python
def get_grade(score):
    if score >= 90:
        print("A")
    elif score >= 80:
        print("B")
    else:
        print("C")
```

목표:

```python
grade = get_grade(85)
print(grade)
```

가 정상적으로 동작하도록 만드세요.

---

### 실습 3. 이름과 결과를 받아 메시지 만들기

다음과 같이 사용할 수 있는 함수를 만드세요.

```python
message = make_result_message("민수", "합격")
```

예상 결과:

```text
민수 학생은 합격입니다.
```

먼저 적어야 할 것:

```text
입력은 무엇인가?
결과는 무엇인가?
함수 안에서 하는 일은 무엇인가?
```

---

### 실습 4. 주문 처리 파이프라인 만들기

학생 문제가 아닌 주문 문제로 바꿔 봅시다.

```python
order = {
    "customer": "민수",
    "amount": 72000
}
```

다음 기능을 생각합니다.

```text
배송비 여부 판단
등급 할인 판단
최종 메시지 생성
출력
```

코드보다 먼저 다음을 설계하세요.

```text
각 함수의 이름은?
각 함수가 받는 입력은?
각 함수가 돌려주는 결과는?
어떤 순서로 연결되는가?
```

---

## 17. 초보자가 자주 하는 실수

### 실수 1. 모든 함수에서 `print()`만 사용한다

값을 다음 단계에서 써야 한다면 `return`이 필요합니다.

---

### 실수 2. 함수에 필요한 입력을 명확히 정하지 않는다

함수 내부에서 갑자기 외부 변수를 가져다 쓰기보다 먼저 질문하세요.

> 이 함수가 일을 하기 위해 반드시 필요한 값은 무엇인가?

---

### 실수 3. 반환값을 받지 않는다

다음처럼 호출만 하면:

```python
get_result(85)
```

반환값을 이후 코드에서 사용하기 어렵습니다.

필요하면 변수에 저장합니다.

```python
result = get_result(85)
```

---

### 실수 4. 다음 함수가 무엇을 필요로 하는지 생각하지 않는다

함수 하나만 보고 끝내지 마세요.

```text
이 함수의 결과를 누가 사용할 것인가?
```

까지 생각해야 합니다.

---

### 실수 5. 처음부터 함수 코드를 모두 작성한다

먼저 종이에 다음만 연결해도 좋습니다.

```text
score
→ get_result
→ result

score
→ get_grade
→ grade

name + score + result + grade
→ make_summary
→ summary
```

이 흐름이 맞는지 확인한 뒤 코드를 작성하세요.

---

## 18. AI를 사용하기 전에 스스로 확인할 것

이번 Chapter에서도 AI는 마지막 검증 도구로 사용합니다.

먼저 스스로 다음 질문에 답하세요.

```text
각 함수의 입력을 설명할 수 있는가?
각 함수의 결과를 설명할 수 있는가?
return된 값이 어디로 가는지 설명할 수 있는가?
print와 return의 차이를 설명할 수 있는가?
전체 함수 호출 순서를 말할 수 있는가?
데이터가 끊기는 지점을 찾을 수 있는가?
```

그다음 직접 코드를 작성합니다.

```text
생각
→ 입력/출력 연결
→ 결과 예측
→ 코드 작성
→ 실행
→ 오류 분석
→ 공식 문서 확인
→ 수정
→ 마지막에 AI 검토
```

AI에게 물어볼 때도 다음과 같이 질문하는 편이 좋습니다.

```text
"정답 코드를 새로 작성해 주세요"가 아니라
"제가 설계한 함수 입력/출력 연결이 자연스러운지 검토해 주세요."
```

---

## 19. 이번 Chapter 완료 체크

다음 질문에 스스로 답할 수 있는지 확인하세요.

- [ ] 함수의 입력과 결과를 코드 작성 전에 설명할 수 있다.
- [ ] 매개변수가 왜 필요한지 설명할 수 있다.
- [ ] `return`된 값이 어디로 가는지 설명할 수 있다.
- [ ] `print`와 `return`의 차이를 설명할 수 있다.
- [ ] 한 함수의 결과를 다음 코드에서 사용할 수 있다.
- [ ] 여러 함수를 순서대로 연결할 수 있다.
- [ ] 함수 내부의 세부 로직과 전체 프로그램 흐름을 구분할 수 있다.
- [ ] 데이터가 함수 사이에서 끊기는 지점을 찾을 수 있다.
- [ ] 같은 함수를 여러 데이터에 재사용할 수 있다.

---

## 20. 다음 Chapter로 연결

지금까지 우리는 다음 과정을 거쳤습니다.

```text
문제 구조 찾기
→ 작은 단계로 나누기
→ 조건 판단
→ 반복 발견
→ 필터링
→ 집계
→ 데이터 구조 설계
→ 복합 요구사항 해결
→ 큰 문제를 함수로 분해
→ 작은 함수를 연결해 프로그램 구성
```

이제 프로그램이 어느 정도 커졌습니다.

그리고 프로그램이 커지면 반드시 만나게 되는 것이 있습니다.

> **예상한 대로 동작하지 않는 순간, 즉 오류입니다.**

다음 Chapter에서는 오류를 무작정 고치는 것이 아니라:

```text
예상 결과 확인
→ 실제 결과 확인
→ 차이 찾기
→ 원인 위치 좁히기
→ 가설 세우기
→ 하나씩 수정
→ 다시 검증
```

하는 **디버깅 사고**를 연습합니다.

---

## 오늘의 핵심 문장

> **작은 함수는 각자의 역할을 수행하고, `return`으로 결과를 전달하면서 연결될 때 하나의 프로그램이 됩니다.**

함수를 잘 만든다는 것은 `def`를 많이 쓰는 것이 아닙니다.

> **데이터가 어디에서 들어오고, 어떤 처리를 거치며, 어디로 전달되는지 설명할 수 있어야 합니다.**

---

## 다음 Chapter — Chapter 11

다음은 [Chapter 11. 오류는 실패가 아니라 단서다](../chapter11/chapter11.md)입니다.

지금까지 익힌 내용을 다음 문제 해결 단계로 연결해 보세요.
