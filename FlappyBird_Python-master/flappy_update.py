import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(1400, random_pipe_pos + pipe_bot_diff))
    top_pipe = pipe_surface.get_rect(midbottom=(1400, random_pipe_pos - pipe_top_diff))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface if not training else pipe_surface_training, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface if not training else pipe_surface_training, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            if not died_last_frame:
                death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True
        return False

    return True


def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

        difficulty_surface = game_font_small.render(f'Easy: 1 Medium: 2 Hard: 3, Training: 4', True, (255, 255, 255))
        difficulty_rect = difficulty_surface.get_rect(center=(288, 400))
        screen.blit(difficulty_surface, difficulty_rect)
        

    if training:
        current_diff_surface = game_font.render(f'Training', True, (255, 255, 255))
        current_diff_rect = current_diff_surface.get_rect(center=(288, 150))
        screen.blit(current_diff_surface, current_diff_rect)

        if game_state == 'main_game':
            quit_training_surface = game_font.render(f'Press RETURN to quit', True, (255, 255, 255))
            quit_training_rect = quit_training_surface.get_rect(center=(288, 200))
            screen.blit(quit_training_surface, quit_training_rect)

            dead_counter_surface = game_font_small.render(f'Times died: {int(times_dead)}', True, (255, 255, 255))
            dead_counter_rect = dead_counter_surface.get_rect(center=(288, 230))
            screen.blit(dead_counter_surface, dead_counter_rect)


def update_score(score, high_score):
    high_score = max(score, high_score)
    return high_score


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 2, buffer = 1024)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)
game_font_small = pygame.font.Font('04B_19.ttf', 20)

# Game Variables
pipe_top_diff = 300
pipe_bot_diff = 0
gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0
can_score = True
bg_surface = pygame.image.load('assets/background-night.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100,512))

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)

pipe_surface_training = pygame.Surface.copy(pipe_surface)
pygame.Surface.set_alpha(pipe_surface_training, 90)

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

training = False
times_dead = 0
died_last_frame = False

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            elif event.key == pygame.K_SPACE and game_active == False:
                times_dead = 0
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
            elif event.key == pygame.K_1 and game_active == False:
                training = False
                pipe_bot_diff = 300
                pipe_top_diff = 600
            elif event.key == pygame.K_2 and game_active == False:
                training = False
                pipe_bot_diff = 190
                pipe_top_diff = 430
            elif event.key == pygame.K_3 and game_active == False:
                training = False
                pipe_bot_diff = 0
                pipe_top_diff = 300
            elif event.key == pygame.K_4 and game_active == False:
                training = True
            elif event.key == pygame.K_RETURN and game_active and training:
                game_active = False
            

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % 3

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        collide_state = check_collision(pipe_list)
        if not training:
            game_active = collide_state
        elif (not died_last_frame and not collide_state):
            times_dead += 1
            died_last_frame = True
        elif (collide_state):
            died_last_frame = False

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        if not training:
            high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
