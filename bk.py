import sys
import math 
input = sys.stdin.readline

# 두 값의 차이가 양수이거나 음수인것의 개수를 세면 되지 않을까..

class beakjoon():
    def __init__(self):
        self.num = 0
        self.count = 0
        
    def func1(self,n,arr):
        dp = [1 for _ in range(n)]

        for i in range(n):
            for j in range(i):
                if arr[i][1] > arr[j][1]:
                    dp[i] = max(dp[i],dp[j]+1)
        return max(dp) ,dp

def main():

    n = int(input()) # 두 전봇대 사이의 전깃술의 개수
    class_name = beakjoon()
    arr = sorted([list(map(int,input().split())) for _ in range(n)])
    rst ,dp = class_name.func1(n,arr)
    # print(dp)
    # print(arr)
    print(n-rst)

if __name__ == "__main__":
    main()
