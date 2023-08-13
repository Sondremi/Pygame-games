
import pygame, random

# Definerer farger og skjermstørrelse
SKJERM_STØRRELSER = [720, 480]
bakgrunnsfarge = (0, 0, 0)  # Svart
snakefarge = (0, 255, 0)  # grønn
matfarge = (255, 255, 255)  # Hvit

# Definer verdier til slangen og maten
BREDDE = 20
HOYDE = 20
SNAKE_HASTIGHET = 15
SNAKE_MAT_INCREMENT = 1

# Setter opp Pygame
pygame.init()
skjerm = pygame.display.set_mode((SKJERM_STØRRELSER[0], SKJERM_STØRRELSER[1]))
pygame.display.set_caption("Snake Game by Sondre Indset")

# Klasse for slangen
class Snake:
    def __init__(self):
        self.x = ((SKJERM_STØRRELSER[0] // 2) - (BREDDE // 2))
        self.y = (SKJERM_STØRRELSER[1] // 2) - (HOYDE // 2)
        self.retning = "HØYRE"
        self.snake_kropps_deler = [[self.x, self.y]]
        self.mat_spist = 0

    def bevegelse(self):
        """ Metoden gjør at slangen kan bevege seg, og øker i størrelse hvis den spiser mat """
        # Kopier posisjonen til hodet
        ny_hode_pos = self.snake_kropps_deler[0].copy()

        # Flytt slangen i riktig retning
        if self.retning == "HØYRE":
            ny_hode_pos[0] += SNAKE_HASTIGHET
            self.x += SNAKE_HASTIGHET
        elif self.retning == "VENSTRE":
            ny_hode_pos[0] -= SNAKE_HASTIGHET
            self.x -= SNAKE_HASTIGHET
        elif self.retning == "OPP":
            ny_hode_pos[1] -= SNAKE_HASTIGHET
            self.y -= SNAKE_HASTIGHET
        elif self.retning == "NED":
            ny_hode_pos[1] += SNAKE_HASTIGHET
            self.y += SNAKE_HASTIGHET

        # Legger til ny hodeposisjon i starten av listen
        self.snake_kropps_deler.insert(0, ny_hode_pos)

        # Hvis slangen ikek spiser mat fjernes siste kroppsdelen
        if self.mat_spist > 0:
            self.mat_spist -= 1
        else:
            self.snake_kropps_deler.pop()

    def tegn_snake(self):
        """ Metoden tegner slangen med hodet og alle kroppsdelene """
        for delen in self.snake_kropps_deler:
            pygame.draw.rect(skjerm, snakefarge, [delen[0], delen[1], BREDDE, HOYDE])

# Klasse for maten
class Mat:
    def __init__(self):
        self.x = random.randrange(0, (SKJERM_STØRRELSER[0] // BREDDE)) * BREDDE
        self.y = random.randrange(0, (SKJERM_STØRRELSER[1] // HOYDE)) * HOYDE

    def tegn_mat(self):
        """ Metoden tegner maten på skjermen med en tilfeldig posisjon"""
        pygame.draw.rect(skjerm, matfarge, [self.x, self.y, BREDDE, HOYDE])


# Oppretter slangen og maten
snake = Snake()
mat = Mat()

# Setter opp spillet
game_over = False
score = 0
font = pygame.font.SysFont("Arial", 25)

# Setter opp klokken
klokke = pygame.time.Clock()

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.retning != "HØYRE":
                snake.retning = "VENSTRE"
            elif event.key == pygame.K_RIGHT and snake.retning != "VENSTRE":
                snake.retning = "HØYRE"
            elif event.key == pygame.K_UP and snake.retning != "NED":
                snake.retning = "OPP"
            elif event.key == pygame.K_DOWN and snake.retning != "OPP":
                snake.retning = "NED"

    # Tegner alt på skjermen
    skjerm.fill(bakgrunnsfarge)
    snake.tegn_snake()
    mat.tegn_mat()

    # Beveger slangen
    snake.bevegelse()

    # Sjekk om slangen spiser maten, hvis slangen spiser mat øker også hastigheten
    spiste_mat = (snake.x - BREDDE // 2 <= mat.x <= snake.x + BREDDE // 2) and (snake.y - HOYDE // 2 <= mat.y <= snake.y + HOYDE // 2)

    if spiste_mat:
        mat = Mat()
        score += 1
        SNAKE_HASTIGHET += 0.5
        snake.mat_spist += 1
        
    # Sjekk om hodet til slangen treffer en av veggene eller seg selv
    if (snake.x + BREDDE // 2 <= 0) or (snake.x >= SKJERM_STØRRELSER[0] - BREDDE // 2) or (snake.y <= 0) or (snake.y >= SKJERM_STØRRELSER[1] - HOYDE):
        game_over = True
    for delen in snake.snake_kropps_deler[1:]:
        if delen == [snake.x, snake.y]:
            game_over = True
            break

    # Viser poengscoren
    poengtekst = font.render("Score: " + str(score), True, (255, 255, 255))
    skjerm.blit(poengtekst, (5, 5))

    pygame.display.flip()

    # Begrens oppdateringshastighet
    klokke.tick(10)  # Her kan du justere antall oppdateringer per sekund

pygame.quit()
