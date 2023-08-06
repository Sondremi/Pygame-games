import pygame
import random

# Starter Pygame
pygame.init()

# Skjermstørrelse
BREDDE, HØYDE = 600, 600
skjerm = pygame.display.set_mode((BREDDE, HØYDE))
pygame.display.set_caption("Stigespillet av Sondre Indset")

# Farger
HVIT = (255, 255, 255)
SVART = (0, 0, 0)
GRØNN = (0, 255, 0)
RØD = (255, 0, 0)
BRUN = (101, 67, 33)

# Spillerens posisjon og stige/slangeposisjoner
spiller_posisjon = 1
stige_posisjoner = {2: 38, 4: 14, 8: 30, 21: 42, 28: 76, 50: 67, 71: 92, 80: 99}
slange_posisjoner = {32: 10, 36: 6, 48: 26, 62: 18, 88: 24, 95: 56, 97: 78}
teller = 0

# Klokke for å kontrollere oppdateringshastighet
klokke = pygame.time.Clock()

kaster_terning = False
kjører = True
while kjører:
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            kjører = False
        elif hendelse.type == pygame.KEYDOWN:
            if hendelse.key == pygame.K_SPACE:
                if not kaster_terning and spiller_posisjon < 100:
                    kast = random.randint(1, 6)
                    print(f"Du kastet {kast}'er")
                    spiller_posisjon += kast
                    print(f"Din posisjon er nå {spiller_posisjon}")
                    teller += 1
                    kaster_terning = True

    if kaster_terning:
        # Simulerer terningkast ved å vise tallene i noen millisekunder
        pygame.time.wait(10)
        kaster_terning = False

        # Oppdater spillerens posisjon
        if spiller_posisjon in stige_posisjoner:
            spiller_posisjon = stige_posisjoner[spiller_posisjon]
            print(f"Du landet på en stige! Din nye posisjon er {spiller_posisjon}")
        elif spiller_posisjon in slange_posisjoner:
            spiller_posisjon = slange_posisjoner[spiller_posisjon]
            print(f"Å nei, du landet på en slange. Din nye posisjon er {spiller_posisjon}")

        # Begrens spillerens posisjon til brettets størrelse
        if spiller_posisjon >= 100:
            spiller_posisjon = 100
            print("Du vant!")
            print(f"Du brukte {teller} kast.")

    # Tegn brettet
    skjerm.fill(HVIT)
    for rad in range(10):
        for kolonne in range(10):
            pygame.draw.rect(skjerm, SVART, (kolonne * 60, rad * 60, 60, 60), 2)
            num = (9 - rad) * 10 + kolonne + 1

            if num in stige_posisjoner:
                pygame.draw.rect(skjerm, GRØNN, (kolonne * 60 + 1, rad * 60 + 1, 58, 58))
                pygame.draw.line(skjerm, GRØNN, (kolonne * 60 + 30, rad * 60 + 30), ((stige_posisjoner[num] - 1) % 10 * 60 + 30, (9 - (stige_posisjoner[num] - 1) // 10) * 60 + 30), 6)
            
            elif num in slange_posisjoner:
                pygame.draw.rect(skjerm, RØD, (kolonne * 60 + 1, rad * 60 + 1, 58, 58))
                pygame.draw.line(skjerm, RØD, (kolonne * 60 + 30, rad * 60 + 30), ((slange_posisjoner[num] - 1) % 10 * 60 + 30, (9 - (slange_posisjoner[num] - 1) // 10) * 60 + 30), 10)
            
            font = pygame.font.Font(None, 36)
            tekst = font.render(str(num), True, SVART)
            tekst_rekt = tekst.get_rect(center=(kolonne * 60 + 30, rad * 60 + 30))
            skjerm.blit(tekst, tekst_rekt)
    
    # Tegn spilleren
    rad = 9 - (spiller_posisjon - 1) // 10
    kolonne = (spiller_posisjon - 1) % 10
    pygame.draw.circle(skjerm, SVART, (kolonne * 60 + 30, rad * 60 + 30), 25)
    
    pygame.display.flip()
    klokke.tick(5)  # Begrenser oppdateringshastighet

pygame.quit()
