import pygame as pg
import random as rd

pg.init()
vindu = pg.display.set_mode((600, 400))

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bredde = 10
        self.hoyde = 100

    def flytt_opp(self):
        # Så lenge y posisjonen ikke er høyere enn brettet kan paddle flyttes oppover
        if self.y > 0:
            self.y -= 7

    def flytt_ned(self):
        # Så lenge y posisjon+paddle høyde, altså bunnen av paddle, kan paddle flyttes nedover
        if self.y+self.hoyde < 400:
            self.y += 7
        
    def tegn(self, vindu):
        # Tegner paddle
        pg.draw.line(vindu, (0, 0, 0), (self.x, self.y), (self.x, self.y+self.hoyde), self.bredde)
    
    def returner_pos(self):
        # Returnerer verdier slik at jeg enkelt kan hente det ut senere i programmet
        return self.x, self.y, self.hoyde
    
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.fart_x = 5
        self.fart_y = 5

    def flytt(self):
        # Endrer x og y posisjon med farten
        self.x += self.fart_x
        self.y += self.fart_y

    def sjekk_vegg_kollisjon(self):
        # Hvis ballen treffen venstre eller høyre side er spillet over
        if (self.x - self.radius) <= 0 or (self.x + self.radius) >= 600:
            pg.quit()
        
        # Hvis ballen treffer toppen eller bunnen endrer ballen retning
        elif (self.y - self.radius) <= 0 or (self.y + self.radius) >= 400:
            self.fart_y =- self.fart_y # Farten skifter fra positiv til negativ


    def sjekk_paddle_kollisjon(self, paddle):
        # Henter verdier fra paddle
        paddle_x, paddly_y, paddle_hoyde = paddle.returner_pos()

        # Sjekker om ballen har samme x verdi som paddle
        if paddle_x == self.x:
            # Sjekker om ballen også er mellom toppen og bunnen av paddle
            if paddly_y <= self.y <= paddly_y+paddle_hoyde:
                # Da snur ballen
                self.fart_x =- self.fart_x

    def tegn(self, vindu):
        # Tegner ballen
        pg.draw.circle(vindu, (0, 0, 200), (self.x, self.y), self.radius) # Sirkel, plasseres på brettet, farge, koordinater, radius på sirkel


clock = pg.time.Clock()

venstre_paddle = Paddle(30, 150)
hoyre_paddle = Paddle(560, 150)
ball = Ball(200, 200)

fortsett = True
while fortsett:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    trykkede_taster = pg.key.get_pressed()

    if trykkede_taster[pg.K_w]:
        venstre_paddle.flytt_opp()
    elif trykkede_taster[pg.K_s]:
        venstre_paddle.flytt_ned()
    if trykkede_taster[pg.K_UP]:
        hoyre_paddle.flytt_opp()
    elif trykkede_taster[pg.K_DOWN]:
        hoyre_paddle.flytt_ned()

    ball.flytt()
    ball.sjekk_vegg_kollisjon()
    ball.sjekk_paddle_kollisjon(venstre_paddle)
    ball.sjekk_paddle_kollisjon(hoyre_paddle)

    vindu.fill((100, 200, 250))
    venstre_paddle.tegn(vindu)
    hoyre_paddle.tegn(vindu)
    ball.tegn(vindu)

    pg.display.update()
    clock.tick(60)