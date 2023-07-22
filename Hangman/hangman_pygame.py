import pygame as pg
import random as rd
from pygame.locals import *
import ordliste

class Stativ:
    def __init__(self, skjerm):
        self.skjerm = skjerm
        self.stativ_farge = (100, 50, 0)
        self.plattform_farge = (100, 100, 100)

    def tegn_stativ(self):
        # Tegner stativet
        pg.draw.rect(self.skjerm, self.stativ_farge, (150, 50, 20, 400))
        pg.draw.rect(self.skjerm, self.stativ_farge, (100, 450, 120, 20))
        pg.draw.rect(self.skjerm, self.stativ_farge, (100, 100, 200, 20))

        # Tegner plattformen
        pg.draw.rect(self.skjerm, self.plattform_farge, (50, 470, 540, 10))
        
class Figur:
    def __init__(self, skjerm):
        self.skjerm = skjerm
        self.kroppsdeler = []

    def tegn_figur(self):
        liv = spill.hent_liv()
        
        hode = (self.skjerm, SVART, (250, 150), 30)
        kropp = (self.skjerm, SVART, (250, 180), (250, 300), 5)
        venstre_arm = (self.skjerm, SVART, (250, 200), (220, 250), 5)
        høyre_arm = (self.skjerm, SVART, (250, 200), (280, 250), 5)
        venstre_ben = (self.skjerm, SVART, (250, 300), (220, 350), 5)
        høyre_ben = (self.skjerm, SVART, (250, 300), (280, 350), 5)

        kroppsdeler = [kropp, venstre_arm, høyre_arm, venstre_ben, høyre_ben]

        if liv > 0:
            pg.draw.circle(*hode)

            for i in range(liv-1):
                pg.draw.line(*kroppsdeler[i])
   
class Game:
    def __init__(self):
        self.ordliste = ordliste.ordliste_str
        self.fasit_ord = rd.choice(self.ordliste)
        self.gjettet = ""
        self.riktige = []
        self.liv = 6
        self.bokstaver = "abcdefghijklmnopqrstuvwxyzæøå"
        self.output_ord = list("_" * len(self.fasit_ord))

    def game(self):
        if self.liv > 0:
            # Viser ordet som gjettes
            output_ord_tekst = " ".join(self.output_ord)
            output_ord_vis = font.render(output_ord_tekst, True, SVART)
            skjerm.blit(output_ord_vis, (VINDU_STØRRELSE[0] // 2 - output_ord_vis.get_width() // 2, 370))

            # Viser bokstavene som er gjettet
            gjettet_tekst = f"Bokstaver gjettet: {self.gjettet}"
            gjettet_vis = font_xsmall.render(gjettet_tekst, True, SVART)
            skjerm.blit(gjettet_vis, (10, 10))

            # Kjører til ordet er gjettet
            if ("_") in self.output_ord:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                        if event.unicode in self.bokstaver:
                            bruker_gjett = event.unicode.lower()

                            #print("Fasit: " + self.fasit_ord)

                            if bruker_gjett not in self.gjettet:
                                self.gjettet += (bruker_gjett + ", ")

                                if bruker_gjett in self.fasit_ord:
                                    print(f"Bokstaven {bruker_gjett} er i ordet")
                                else:
                                    print(f"Bokstaven {bruker_gjett} er ikke i ordet")
                                    self.liv -= 1

                                teller = 0
                                for bokstav in self.fasit_ord:
                                    if bruker_gjett == bokstav:
                                        self.output_ord[teller] = bruker_gjett
                                        self.riktige.append(bruker_gjett)
                                    teller += 1
                            else:
                                print(f"Du har allerede gjettet bokstaven {bruker_gjett}")
            else:
                seier_tekst = "Du vant!"
                seier_vis = font.render(seier_tekst, True, SVART)
                skjerm.blit(seier_vis, (
                VINDU_STØRRELSE[0] // 2, VINDU_STØRRELSE[1] // 2 - seier_vis.get_height() // 2))

                restart_tekst = "Restart: R"
                restart_vis = font_small.render(restart_tekst, True, SVART)
                skjerm.blit(restart_vis, (
                VINDU_STØRRELSE[0] // 2, VINDU_STØRRELSE[1] // 2 - seier_vis.get_height() // 2 + restart_vis.get_height() + 20))

                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:  # Press R to restart
                            self.reset_game()
        
        else:
            tap_tekst = "Du tapte"
            tap_vis = font.render(tap_tekst, True, SVART)
            skjerm.blit(tap_vis, (VINDU_STØRRELSE[0] // 2 - 30, 320))
            
            fasit_tekst = f"Ordet var: {self.fasit_ord}"
            fasit_vis = font.render(fasit_tekst, True, SVART)
            skjerm.blit(fasit_vis, (VINDU_STØRRELSE[0] // 2 - 100, 370))

            restart_tekst = "Restart: R"
            restart_vis = font_small.render(restart_tekst, True, SVART)
            skjerm.blit(restart_vis, (
            VINDU_STØRRELSE[0] // 2, VINDU_STØRRELSE[1] // 2 + 40))

            for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:  # Press R to restart
                            self.reset_game()

    def hent_liv(self):
        return self.liv
    
    def reset_game(self):
        self.fasit_ord = rd.choice(self.ordliste)
        self.gjettet = ""
        self.riktige = []
        self.liv = 6
        self.output_ord = list("_" * len(self.fasit_ord))

# Initialiserer Pygame
pg.init()

# Farger
SVART = (0, 0, 0)
BAKGRUNN = (100, 200, 250)

# Oppretter et vindu
VINDU_STØRRELSE = (640, 480)
skjerm = pg.display.set_mode(VINDU_STØRRELSE)
pg.display.set_caption("Hangman by Sondre Indset")

stativ = Stativ(skjerm)
figur = Figur(skjerm)
spill = Game()

font = pg.font.SysFont("Arial", 50)
font_small = pg.font.SysFont("Arial", 30)
font_xsmall = pg.font.SysFont("Arial", 20)


while True:
    for hendelse in pg.event.get():
        if hendelse.type == pg.QUIT:
            pg.quit()
            quit()
        
    skjerm.fill(BAKGRUNN)

    stativ.tegn_stativ()
    figur.tegn_figur()
    spill.game()

    pg.display.flip()