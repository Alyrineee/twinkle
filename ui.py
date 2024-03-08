import generate_star


def start_menu():
    print('Welcome to Twinkle\nSelect mode:\n1 - Earn Stars\n2 - Check balance\n3 - Top')
    mode = int(input())
    if mode == 1:
        return earn()
    elif mode == 2:
        pass
    elif mode == 3:
        pass
def clear():
    for i in range(10):
        print('\n')
def earn():
    clear()
    star = generate_star.star()
    print('Key is ready!')
    correct = 0
    wrong = 0
    for i in range(16):
        num = input('Enter a number:')
        if star.check(num,i):
            print('You`re right!')
            correct+=1
        else:
            print('You`re wrong!')
            wrong+=1

    print(f'Wrong: {wrong}\nCorrect: {correct}')

