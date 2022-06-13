import tensorflow as tf

counter = 0
for i in range(10):
    for j in range(10):
        if i+j == 15:
            counter += 1

print(counter)





