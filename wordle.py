### Author: MoolsDogTwo, do not steel.

import pygame
import random

pygame.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MAX_WORD_LENGTH = 5
SLOT_COUNT = 6
WORD_FONT = pygame.font.SysFont(None, 64, bold=True)
UI_FONT = pygame.font.SysFont(None, 12)
COL_WHITE = pygame.Color(255, 255, 255)
COL_EMPTY = pygame.Color(50, 50, 50)
RECT_SIZE = 50
RECT_MARGIN = 20
RECT_PAD = 10

### Internal Functions ###
def get_random_word():
    try:
        with open("words.txt", "r") as read:
            words = read.readlines()
            return random.choice(words)
    except FileNotFoundError:
        print("Error: Words.txt not found. How did you even manage this bru.")


def input_word(key, current_word):
    print(current_word)
    if len(current_word) < MAX_WORD_LENGTH:
        return current_word + str(key)
    else:
        return current_word


### Drawing Functions ###
def draw_ui(scr, word, word_slots, current_word, current_attempt):
    for i in range(SLOT_COUNT):
        for j in range(MAX_WORD_LENGTH):
            left_pos = j * (RECT_SIZE + RECT_MARGIN) + RECT_PAD
            top_pos = i * (RECT_PAD + RECT_SIZE)
            pygame.draw.rect(scr, COL_EMPTY, pygame.Rect(left_pos, top_pos, RECT_SIZE, RECT_SIZE))
            # if i == current_attempt:
            #     if current_word:
            #         draw_text(scr, current_word[j], (left_pos, top_pos), WORD_FONT, COL_WHITE)
            # else:
            #     if word_slots[i]:
            #         draw_text(scr, current_word[j], (left_pos, top_pos), WORD_FONT, COL_WHITE)


def draw_text(scr, msg, pos, font, color):
    the_text = font.render(msg, antialias=False, color=color)
    scr.blit(the_text, pos)


### Main Stuff ###
def main():
    word = get_random_word()
    word_slots = []
    current_word = ""
    current_attempt = 0

    # Setup pygame
    pygame.display.set_caption("PyWordle")
    scr = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Event loop
    while True:
        scr.fill(pygame.Color(0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    key = event.unicode.upper()
                    current_word = input_word(key, current_word)
                if event.key == pygame.K_BACKSPACE:
                    if current_word:
                        print(current_word)
                        current_word = current_word[:-1]

        # draw_text(scr, current_word, (0, 0), WORD_FONT, COL_WHITE)
        draw_ui(scr, word, word_slots, current_word, current_attempt)
        pygame.display.flip()


if __name__ == "__main__":
    main()
