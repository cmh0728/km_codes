class Fibonacci:
    def __init__(self):
        pass
    
    def fb(self, n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

def main():
    try:
        n = int(input("피보나치 수열의 길이를 입력하세요: "))
        fibonacci = Fibonacci()
        result = fibonacci.fb(n)
        print("결과:", result)
        
    except Exception as e:
        print("오류가 발생했습니다:", e)

if __name__ == "__main__":
    main()
