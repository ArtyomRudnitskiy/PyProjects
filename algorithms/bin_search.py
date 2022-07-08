# list:  ☐ ☐ ☐ ☐
#        ^      ^
#       low    high
#
# len(list)=4, low=0, high=3

# !!! LIST SHOULD BE SORTED !!!

def binary_search(list, item):
    low = 0  # the left border
    high = len(list) - 1  # the right border

    # until the borders cross
    while low <= high:
        mid = int((low + high) / 2)  # divide the list in half
        guess = list[mid]

        if guess == item:  # if we immediately found the value
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


def main():
    my_list = [1, 2, 3, 4, 5]

    print(binary_search(my_list, 4))
    print(binary_search(my_list, 6))


if __name__ == '__main__':
    main()
