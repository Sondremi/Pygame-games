import pygame as pg
import random as rd
from pygame.locals import (K_LEFT, K_RIGHT, K_SPACE)

pg.init() # Starter pygame
pg.display.set_caption("Multipong spesiallaget til Bartosz")

bredde = 500 # Bredden til brettet
hoyde = 500 # Høyden til brettet
brett = pg.display.set_mode([bredde, hoyde]) # Lager et brett på 500x500 px

font = pg.font.SysFont("Arial", 24) # Skrifttype og størrelse

class Ball:
    """Klassen Ball representerer alle ballene/hinderne"""
    def __init__(self, x, y, x_fart, y_fart, radius, farger, brett):
        """Konstroktør til Ball, henter informasjon om x og y koordinater, x og y fart, radius og farger til ballene"""
        self.x = x
        self.y = y
        self.x_fart = x_fart
        self.y_fart = y_fart
        self.radius = radius
        self.brett = brett
        self.farger = farger
    
    def tegn_ball(self):
        """Funksjonen blir brukt til å tegne en ny ball/hinder"""
        pg.draw.circle(brett, (self.farger), (self.x, self.y), self.radius) # Sirkel, plasseres på brettet, farge, koordinater, radius på sirkel
    
    def flytt_ballen(self):
        """Funksjonen gjør at ballene beveger seg i ulik retning og snur ved kantene. 
        I tillegg blir spillet ferdig om ballen treffet nedre kant"""
        if (self.x - self.radius) <= 0 or (self.x + self.radius) >= bredde:
            self.x_fart =- self.x_fart # Hvis ballen treffer venstre eller høyre side, snur ballen
        
        elif (self.y - self.radius) <= 0:
            self.y_fart =- self.y_fart # Hvis ballen treffer taket, snur ballen
        
        elif (self.y + self.radius) >= hoyde: # Hvis ballen treffer bakken
            # Fjerner ballene fra brettet
            for ball in baller:
                ball.x = -10

            return True

        # Ellers så beveger ballene seg med farten som er definert
        self.x += self.x_fart
        self.y += self.y_fart

    def beregn_avstand(self):
        """Funksjonen beregner avstanden mellom ballene og linja/spilleren
        Hvis ballen treffer spilleren snur ballen og går andre vei.
        I tillegg oppstår det en ny ball, et tilfeldig sted på brettet."""
        linje_venstre, linje_hoyre, linje_y = linje.beveg_linje() # Henter koordinater til linja

        if (linje_venstre < self.x < linje_hoyre) and (self.y+self.radius) >= linje_y:
            self.y_fart =- self.y_fart # Hvis ballen treffer linja, snur ballen
            self.y -= 10 # Fikser feil ved at ball setter seg fast i linja

            # Også tegnes det en ny ball
            ny_ball = Ball(rd.randint(20,400), rd.randint(50,250), 0.12, 0.12, 8, (rd.randint(0, 200), rd.randint(0, 200), rd.randint(0, 200)), brett)
            baller.append(ny_ball)
    
class Linje:
    """Klassen Linje representerer linja som kan styres, altså spilleren"""
    def __init__(self, farge, start_x, start_y, stopp_x, stopp_y, bredde):
        """Konstroktør til klassen Linje. henter informasjon om fargen til linja. Koordinatene med start og stopp for å bestemme lengde 
        på linja og bredden."""
        self.farge = farge
        self.start_x = start_x
        self.start_y = start_y
        self.stopp_x = stopp_x
        self.stopp_y = stopp_y
        self.bredde = bredde
    
    def tegn_linje(self):
        """Funksjonen brukes til å tegne spilleren"""
        pg.draw.line(brett, self.farge, (self.start_x, self.start_y), (self.stopp_x, self.stopp_y), self.bredde)
    
    def beveg_linje(self):
        """Bunksjonen brukes slik at spilleren kan beveges til høyre og venstre"""
        trykkede_taster = pg.key.get_pressed()
        
        if trykkede_taster[K_LEFT]: # Beveger linja til venstre
            self.start_x -= 0.2 # Farten på linja er satt til 0.2
            self.stopp_x -= 0.2
            if self.start_x <= 0: # Flytter linja tilbake på brettet om den treffer venstre vegg
                self.start_x += 10
                self.stopp_x += 10
        elif trykkede_taster[K_RIGHT]: # Beveger linje til høyre
            self.start_x += 0.2
            self.stopp_x += 0.2
            if self.stopp_x >= bredde: # Flytter linja tilbake på brettet om den treffer høyre vegg
                self.stopp_x -= 10
                self.start_x -= 10
        
        return self.start_x, self.stopp_x, self.start_y # Returnerer koordinatene til linja / Spilleren
            

# Lager en løkke som kjører så lenge spilleren ønsker, altså at spillet kan restarte
while True:
    # Definerer koordinatene til de ulike tekst boksene
    s1_koordinat = (20, 20)
    s2_koordinat = (0, -100)
    s3_koordinat = (0, -50)

    baller = [] # Oppretter en liste som skal inneholde alle ballene
    linje = Linje((0, 0, 255), 200, 470, 300, 470, 5) # Definerer linja / spilleren

    # Legger til første ball når spillet starter
    ball = Ball(rd.randint(30,470), rd.randint(10,250), 0.12, 0.12, 8, (rd.randint(0,200), rd.randint(0,200), rd.randint(0,200)), brett)
    baller.append(ball)

    # Oppretter en løkke som kjører programmet
    fortsett = True
    while fortsett:
        for event in pg.event.get():
            if event.type == pg.QUIT: # Sjekker om bruker krysser ut vinduet
                fortsett = False
                pg.quit()
            
        brett.fill((100, 255, 255)) # Velger turquise bakgrunnsfarge

        for ball in baller: # Kjører funksjonene på alle ballene som blir lagt til i lista Baller
            ball.tegn_ball()
            ball.flytt_ballen()
            ball.beregn_avstand()

        linje.tegn_linje() # Oppretter spilleren på brettet
        linje.beveg_linje()
            
        poengsum = len(baller) # Definerer poengsum etter hvor mange baller det er på banen

        if ball.flytt_ballen(): # Hvis en ball har truffet bunnen, så er spillet ferdig
            s1_koordinat = (0, -100)
            s2_koordinat = (100, 200)
            s3_koordinat = (80, 240)

        s1_tekst = f"Poengsum: {poengsum}" # Viser poengsummen øverst til venstre
        s1_vis = font.render(s1_tekst, True, (0, 0, 200))
        brett.blit(s1_vis, s1_koordinat)

        s2_tekst = f"Du tapte! Din poengsum ble {poengsum}" # Viser en tekst når du har tapt
        s2_vis = font.render(s2_tekst, True, (0, 0, 200))
        brett.blit(s2_vis, s2_koordinat)

        s3_tekst = f"Vil du spille på nytt? Trykk SPACE" # Ber spiller trykke space for å restarte
        s3_vis = font.render(s3_tekst, True, (0, 0, 200))
        brett.blit(s3_vis, s3_koordinat)


        trykkede_taster = pg.key.get_pressed()
        if trykkede_taster[K_SPACE]: # Hvis spilleren trykker på space, starter spillet på nytt
            break # Restarter løkken

        pg.display.flip() # Oppdaterer spillbrettet