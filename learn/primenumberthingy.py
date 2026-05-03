max_number=100
count=0
print("the prime numbers from 1 to",max_number, "is:")
for w in range (2,max_number+1):
    is_prime = True
    for x in range (2,w):
         # print('w=', w, ' x=',x)
         if w%x == 0:
             # print(w, "is a composite number")
             is_prime=False
             break
    if is_prime == True:
        print(w)
        count=count+1

print("the total amount of prime numbers from 1 to", max_number, "is", count)
        
