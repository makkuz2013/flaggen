import pygame
import sys
import os.path

pygame.init()

screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
running = True

loading_type = "hex" if len(sys.argv) > 2 and sys.argv[2] == "hex" else "txt"

filename = sys.argv[1] if len(sys.argv) > 1 else "data"
basename = os.path.basename(filename)

if loading_type == "txt":
    with open(filename, "rb") as f:
        data_bytes = f.read()
else:
    with open(filename, "r") as f:
        data_bytes = data_bytes = bytes(int(x, 16) for x in f.read().split())

flag = []
color_bytes = []
channels_in_color = 0

print(f'File data (Hex): {", ".join(f"0x{byte:02x}" for byte in data_bytes)}')

for byte in data_bytes:
    color_bytes.append(byte)
    channels_in_color += 1
    if channels_in_color == 3:
        channels_in_color = 0

        color_hexcode = int.from_bytes(color_bytes, byteorder="big")

        color_bytes.clear()

        flag.append(color_hexcode)

leftover = color_bytes.copy()

color_count = len(flag)
color_width = screen.get_width() / color_count

leftover_string = "+ " + ", ".join(f"0x{byte:02x}" for byte in leftover) if leftover else ""

font = pygame.font.Font(None, 48)

def screenshot():
    print("Saved screenshot!")
    pygame.image.save(screen, f"images/{basename}.png")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                screenshot()

    screen.fill("white")

    for i in range(color_count):
        rect = pygame.Rect(i*color_width,0,color_width+1,screen.get_height())
        pygame.draw.rect(screen, flag[i], rect)

    text_surf = font.render(leftover_string, False, "white")
    text_rect = text_surf.get_rect()
    text_rect.bottomright = screen.get_size()

    screen.blit(text_surf, text_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
