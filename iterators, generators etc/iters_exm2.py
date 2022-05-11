def get_all_average(N):
    count = 0
    S = 0
    for i in range(1, N+1):
        count += 1
        S += i
        yield S/count


if __name__ == '__main__':
    for i in get_all_average(10):
        print(i)
