import pygame
import random

directions = {"UP": (0,-1), "DOWN": (0,1),"LEFT": (-1,0), "RIGHT": (1,0)}

class Cube:
    def __init__(self, position, color, direction_key):
        self.position = position
        self.color = color
        self.direction = direction_key

    def __repr__(self):
        return str(self.position) + ":" + str(self.color) + ":" + str((self.x_dir,self.y_dir))

    def move(self,direction_key):
        self.direction = direction_key
        move_dir = directions.get(self.direction)
        self.position = self.position[0] + move_dir[0], self.position[1] + move_dir[1]

    def draw(self,window, square_size):
        x_pos,y_pos= self.position
        pygame.draw.rect(window,self.color, (x_pos*square_size+1,y_pos*square_size+1,square_size-2,square_size-2))


class Snake:
    def __init__(self,position):
        self.color = ((50,205,50))
        self.body = []
        self.direction = "UP"
        self.head = Cube(position, (0,0,255), self.direction)
        self.body.append(self.head)
        self.turns = {}

    def grow_tail(self):
        tail_end = self.body[-1]

        if tail_end.direction == "RIGHT":
            self.body.append(Cube((tail_end.position[0]-1,tail_end.position[1]), self.color, tail_end.direction))
        elif tail_end.direction == "LEFT":
            self.body.append(Cube((tail_end.position[0]+1,tail_end.position[1]), self.color, tail_end.direction))
        elif tail_end.direction == "DOWN":
            self.body.append(Cube((tail_end.position[0],tail_end.position[1]-1), self.color, tail_end.direction))
        elif tail_end.direction == "UP":
            self.body.append(Cube((tail_end.position[0],tail_end.position[1]+1), self.color, tail_end.direction))

    def reset(self):
        self.head = Cube((10,10),(0,0,255), "UP")
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction = "UP"

    def turn(self, new_direction):
        if new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
            self.turns[self.head.position[:]] = self.direction
        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
            self.turns[self.head.position[:]] = self.direction
        elif new_direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
            self.turns[self.head.position[:]] = self.direction
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
            self.turns[self.head.position[:]] = self.direction

    def move(self,rows):
        for c in self.body:
            p = c.position
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn)
                if c == self.body[-1]:
                    self.turns.pop(p)
            else:
                c.move(c.direction)

    def draw(self,window,square_size):
        for c in self.body:
            c.draw(window,square_size)


class Game:
    def __init__(self, screen_size, rows, FPS):
        pygame.display.set_caption("SNAAAAAAAAAAAAAAKE!!!")
        self.screen_size = screen_size
        self.rows = rows
        self.game_window = pygame.display.set_mode((screen_size,screen_size))
        self.snake = self.create_snake()
        self.current_snack = self.create_snack()
        self.clock = pygame.time.Clock()
        self.fps = FPS

    def create_snake(self):
        return Snake((10,10))

    def create_snack(self):
        return Cube(self.place_random_snack(), (0,255,0), "UP")

    def tick(self):
        pygame.time.delay(50)
        self.clock.tick(self.fps)
        self.snake.move(self.rows)
        if self.snake.body[0].position == self.current_snack.position:
            self.snake.grow_tail()
            self.current_snack = self.create_snack()

        if self.snake.head.position[0] < 0 or self.snake.head.position[0] > self.rows or self.snake.head.position[1] < 0 or self.snake.head.position[1] > self.rows:
            self.snake.reset()
            
        for cube in range(len(self.snake.body)):
            if self.snake.body[cube].position in list(map(lambda z:z.position, self.snake.body[cube+1:])):
                print("Snake dead!")
                self.snake.reset()
                break
        self.draw_game()

    def turn_snake(self,new_direction):
        self.snake.turn(new_direction)



    def draw_game(self):
        square_size = self.screen_size//self.rows
        self.game_window.fill((0,0,0))
        self.current_snack.draw(self.game_window,square_size)
        self.snake.draw(self.game_window,square_size)
        for row_index in range(self.rows-1):
            line_endpoint = square_size*(row_index+1)
            pygame.draw.line(self.game_window,(255,255,255), (line_endpoint,0), (line_endpoint,self.screen_size))
            pygame.draw.line(self.game_window,(255,255,255), (0,line_endpoint), (self.screen_size,line_endpoint))
        pygame.display.update()

    def place_random_snack(self):
        while True:
            snack_x_pos = random.randrange(self.rows)
            snack_y_pos = random.randrange(self.rows)
            if len(list(filter(lambda z:z.position == (snack_x_pos,snack_y_pos), self.snake.body))) > 0:
                continue
            else:
                break
        return (snack_x_pos,snack_y_pos)



def game_loop():
    running = True
    FPS = 10
    game_instance = Game(800,20,FPS)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                game_instance.turn_snake("LEFT")

            elif keys[pygame.K_RIGHT]:
                game_instance.turn_snake("RIGHT")

            elif keys[pygame.K_UP]:
                game_instance.turn_snake("UP")

            elif keys[pygame.K_DOWN]:
                game_instance.turn_snake("DOWN")

        game_instance.tick()
    pygame.quit()


if __name__ == "__main__":
    game_loop()
