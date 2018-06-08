from random import randrange
# variables
tired = 0
hunger = 0

states = ['patrol','shootout', 'rest','dead', 'winner']
current_state = 'patrol'

foundEnemy = 0
killedEnemy = 0
enemyCount = 3
fatigue = 0

running = True
max_limit = 100
game_time = 0

while running:
    game_time += 1

    # PATROL: Loops patrol until Guard sees enemy
    if current_state is 'patrol':
        
        # If find an enemy, change state to shootout
        print("Searching for an Enemy...")
        foundEnemy = randrange(0,9)
        if foundEnemy >=5 :
            print("ENEMY FOUND, DROP YOUR WEAPON!")
            current_state = 'shootout'
        if foundEnemy <= 4:
            print("Hmm...Nothing here...")
            fatigue += 1
        if fatigue > 3:
            current_state = 'rest'

    # SHOOTOUT: Will attempt to shoot enemy, and has a chance of dying.
    elif current_state is 'shootout':
        
        # Attempt to kill enemy; guard dies on failure
        killedEnemy = randrange(0,9)
        killedEnemy += fatigue
        if killedEnemy <= 7:
            print("Enemy Defeated. Returning to Patrol")
            current_state = 'patrol'
            enemyCount -= 1
            fatigue += 2
            if enemyCount == 0:
                current_state = 'winner'
        if killedEnemy >= 8:
            current_state = 'dead'
    
    # REST: Takes a rest to recover
    elif current_state is 'rest':
        print("Ahh...A good rest, I feel more alert - back to work")
        fatigue = 0;
        current_state = 'patrol'
        
        
    # DEAD: An end state, completing the program
    elif current_state is 'dead':
        # Dead
        print("Oh no, I'm Dead..")
        game_time = 101
            
    # WINNER: An end state, after defeating 5 enemies with success, completes the program
    elif current_state is 'winner':
      # Winner
      print("I am the last one standing Hooray!")
      game_time = 101;


        
    # Check for end of game time
    if game_time > max_limit:
        running = False

print('-- Good Game --')


    
