### Author: MoolsDogTwo, do not steel.

import pygame
import random

pygame.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WORD_FONT_SIZE= 64
UI_FONT_SIZE = 32
MAX_WORD_LENGTH = 5
SLOT_COUNT = 6
WORD_FONT = pygame.font.SysFont(None, WORD_FONT_SIZE, bold=True)
UI_FONT = pygame.font.SysFont(None, UI_FONT_SIZE)
COL_WHITE = pygame.Color(255, 255, 255)
COL_ERROR = pygame.Color(255, 0, 0)
COL_RIGHT_SPOT = pygame.Color(0, 160, 0)
COL_RIGHT_LETTER = pygame.Color(160, 130, 0)
COL_EMPTY = pygame.Color(50, 50, 50)
RECT_SIZE = 50
RECT_PAD = 5
words = None

### Internal Functions ###
def load_words():
    global words
    try:
        with open("words.txt", "r") as read:
            words = read.read().splitlines()
    except FileNotFoundError:
        print("Error: Words.txt not found. How did you even manage this bru.")


def input_word(key, current_word) -> str:
    print(current_word)
    if len(current_word) < MAX_WORD_LENGTH:
        return current_word + str(key)
    else:
        return current_word


def is_in_word_list(current_word) -> bool:
    return current_word.lower() in words


def check_word(current_word) -> tuple[bool, str]:
    if not len(current_word) == MAX_WORD_LENGTH:
        return (False, "Word must be 5 letters long")
    if not is_in_word_list(current_word):
        return (False, "Not in word list")
    return (True, "")


### Drawing Functions ###
def t_pad(pos):
    """ t = Translate """
    return pos + RECT_PAD


def get_box_colour(i, j, word_slots, word):
    try:
        if word_slots[i]:
            current_word = word_slots[i].lower()
            if current_word[j] in word: # Check if the current letter exists in the word
                return COL_RIGHT_LETTER
            # TODO: Check if the current letter is in the right spot
            else:
                return COL_EMPTY
    except IndexError:
        pass
    return COL_EMPTY


def draw_ui(scr, word, word_slots, current_word, current_attempt) -> None:
    for i in range(SLOT_COUNT):
        for j in range(MAX_WORD_LENGTH):
            left_pos = j * (RECT_SIZE + RECT_PAD)
            top_pos = i * (RECT_SIZE + RECT_PAD)
            pygame.draw.rect(scr, get_box_colour(i, j, word_slots, word), pygame.Rect(left_pos, top_pos, RECT_SIZE, RECT_SIZE))
            if i == current_attempt:  # Draw the current word differently to the word slots
                try:
                    draw_text(scr, current_word[j], (t_pad(left_pos), t_pad(top_pos)), WORD_FONT, COL_WHITE)
                except IndexError:
                    pass
            else:
                try:
                    draw_text(scr, word_slots[i][j], (t_pad(left_pos), t_pad(top_pos)), WORD_FONT, COL_WHITE)
                except IndexError:
                    pass


def draw_text(scr, msg, pos, font, color) -> None:
    the_text = font.render(msg, antialias=False, color=color)
    scr.blit(the_text, pos)


### Main Stuff ###
def main():
    load_words()
    # word = random.choice(words)
    word = "aback"
    word_slots = ["", "", "", "", "", ""]
    current_word = ""
    current_attempt = 0
    error = ()

    # Setup pygame
    pygame.display.set_caption("PyWordle")
    scr = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Event loop
    while True:
        scr.fill(pygame.Color(0, 0, 0))
        draw_text(scr, f"The word is \"{word}\"", (0, SCREEN_HEIGHT - (UI_FONT_SIZE * 2)), UI_FONT, COL_RIGHT_SPOT)

        idk_anymore = (RECT_SIZE + RECT_PAD) * (SLOT_COUNT - 1)
        draw_text(scr, f"Attempt {current_attempt + 1}/{SLOT_COUNT}", (idk_anymore, 0), UI_FONT, COL_WHITE)
        
        # Draw an error if there is one. This error tuple method just sucks.
        if error:
            draw_text(scr, error[1], (0, SCREEN_HEIGHT - UI_FONT_SIZE), UI_FONT, COL_ERROR)

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
                elif event.key == pygame.K_RETURN:
                    result = check_word(current_word)
                    if result[0]:
                        word_slots[current_attempt] = current_word
                        current_attempt += 1
                        current_word = ""
                        error = ()
                    else:
                        error = result

        draw_ui(scr, word, word_slots, current_word, current_attempt)
        pygame.display.flip()


if __name__ == "__main__":
    main()
