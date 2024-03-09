import models

starss = []
cat_obj = models.cat('Alyrine')
def start_menu():
    print('Welcome to Twinkle\nSelect mode:\n1 - Earn Stars\n2 - Star Cat\n3 - Create cat')
    mode = int(input())
    if mode == 1:
        return earn()
    elif mode == 2:
        return cat()
    elif mode == 3:
        pass
def clear():
    for i in range(10):
        print('\n')
def earn():
    clear()
    star = models.star()
    print('Key is ready!')
    correct = 0
    wrong = 0
    for i in range(8):
        num = input(f'Enter a {i+1} number:')
        if star.check(num,i):
            correct+=1
        else:
            wrong+=1
    print('----------------------------------------------')
    if correct//wrong >= 0.5:
        print('You get 1 star!')
        cat_obj.stars+=1
        starss.append(star)
    else:
        print('Oh no, your cat wants to eat!')
        cat.hungry = cat_obj.hungry-(cat_obj.stars*(correct+1)//7)
        print(f'Hungry: {cat.hungry}')
    print('----------------------------------------------')
    print(f'Star info:\nName: {star.name}\nRank: {star.rank}')
    print('----------------------------------------------')
    temp = input('\n\npress any key....')
    clear()
    start_menu()
def cat():
    clear()
    print(f'Cat`s name: {cat_obj.name}')
    print(f'Hungry: {cat_obj.stars}')
    print(f'Hungry: {cat_obj.hungry}')
    temp = int(input('\n\npress any key....'))
    if temp == 1:
        star = starss.pop()
        if star.rank == 'common':
            cat_obj.hungry += (100 - cat_obj.hungry) * 0.1
        elif star.rank == 'rare':
            cat_obj.hungry += (100 - cat_obj.hungry) * 0.2
        elif star.rank == 'epic':
            cat_obj.hungry += (100 - cat_obj.hungry) * 0.5
        elif star.rank == 'legendary':
            cat_obj.hungry += (100 - cat_obj.hungry) * 0.9
    clear()
    start_menu()