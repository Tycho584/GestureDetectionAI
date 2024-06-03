import pygame
import time
import random
import threading
import gestureDetectionCamera
import math

class Speler(pygame.Rect): 

    def __init__(self,afbeelding,afbKogel,BREEDTE,HOOGTE,snelheid,kogelsnelheid):
        
        self.afb = pygame.image.load(afbeelding)
        self.afb=pygame.transform.scale(self.afb,(30,30))
        self.afbkogel =  pygame.image.load(afbKogel)

        self.x = BREEDTE//2-self.afb.get_width()//2
        self.y= HOOGTE-self.afb.get_height()
        self.kogel_x = BREEDTE//2-self.afb.get_width()//2
        self.kogel_y = HOOGTE-self.afb.get_height()
        self.kan_schieten = True
        self.kogels = []
        self.tijd = 0
        self.snelheid = snelheid
        self.kogelsnelheid = kogelsnelheid
        super().__init__(self.x,self.y, self.afb.get_width(),self.afb.get_height())

    
    def bewegen(self,hand_beweging):

        if camera.handMovement != {}:
            nieuwe_x= self.x
            #links bewegen
            if camera.handMovement["moveLeft"]:
                nieuwe_x = self.x - self.snelheid
            #naar rechts
            if camera.handMovement['moveRight']:
                nieuwe_x = self.x + self.snelheid

            if not self.randGeraakt(nieuwe_x):
                self.x=nieuwe_x
            
    
    def randGeraakt(self,nieuwe_x):       
        if nieuwe_x <=0 or nieuwe_x+ self.afb.get_width() >=BREEDTE:
            return True
        
        return False
    
    def schieten(self, hand_beweging):
        if self.tijd > time.time() - 0.5:
            return
        
        self.kan_schieten = True

        if camera.handMovement['shoot']:
            self.kan_schieten = False
            self.kogels.append(pygame.Rect(self.x+ self.afb.get_width()//2,self.y,self.afbkogel.get_width(),self.afbkogel.get_height()))
            self.tijd = time.time()
        
        pass

    def raakttegenstander(self,tegenstanders, Huidigetegenstander, score):
        for kogel in self.kogels:
            geraakt = kogel.collidelist(tegenstanders)

            if geraakt != -1:
                self.kogels.remove(kogel)
                tegenstanders.pop(geraakt)
                score=score+100
                if geraakt < Huidigetegenstander: 
                    Huidigetegenstander-=1

        return Huidigetegenstander, score

    def raaktbunker(self,bunkers):
        for kogel in self.kogels:
            geraakt = kogel.collidelist(bunkers)
            if geraakt != -1:
                self.kogels.remove(kogel)
                bunkers.pop(geraakt)
                
        
class Tegenstander(pygame.Rect):

    def __init__(self,afb,afbKogel,x,y,snelheid): 
        self.afb = pygame.image.load(afb)
        self.afb =pygame.transform.scale(self.afb,(35,35))
        self.afbKogel= pygame.image.load(afbKogel)
        self.afbKogel= pygame.transform.rotate(self.afbKogel,-90)
        super().__init__(x,y, self.afb.get_width(),self.afb.get_height())
        
        self.snelheid = snelheid
        self.kogels = []
        self.time = 0
        self.schietkans = 9999

 
        pass

    def kogeltoevoegen(self,tegenstanders):
         aantal_tegenstanders = len(tegenstanders)
         self.schietkans = int(10000 - (50-aantal_tegenstanders) * 202.857)
            
         schietgetal = random.randint(1,self.schietkans+1)
         if schietgetal >= self.schietkans: 

            # Maak kogel aan.
             self.kogels.append(pygame.Rect(self.x+ self.afb.get_width()//2,self.y,self.afbKogel.get_width(),self.afbKogel.get_height()))
    
    def kogelbewegen(self):
        for kogel in self.kogels:
            kogel.y= kogel.y+5
        

    def kogeltekenen(self,screen):
        for kogel in self.kogels:
            screen.blit(self.afbKogel,(kogel.x,kogel.y))
        
    
    def beweeghorizontaal(self,richting,BREEDTE):


        #rechts
        if richting == "Rechts":
            self.x = self.x + 9
            if self.x + self.afb.get_width() >= BREEDTE:
                return True
        #links
        elif richting == "Links":
            self.x = self.x - 9
            if self.x <= 0:
                return True
        return False
    
    def beweegverticaal(self):
        self.y = self.y + 10
    
    def raaktspeler(self,speler,levens):
        for kogel in self.kogels:
            geraakt = kogel.colliderect(speler)
            print(speler)
            if geraakt:
                self.kogels.remove(kogel)
                levens.pop(0)
    
    def raaktbunker(self,bunkers):
        for kogel in self.kogels:
            geraakt = kogel.collidelist(bunkers)

            if geraakt != -1:
                self.kogels.remove(kogel)
                bunkers.pop(geraakt)

                


class Bunker(pygame.Rect):
    def __init__(self,left,top,width, height,kleur):
        super().__init__(left,top,width, height)
        self.kleur=kleur
    
    def geraakt(self):
        pass


    pass

BREEDTE,HOOGTE= 600,600


afb_kogels= pygame.image.load(r"kogel.png")
afb_kogels=pygame.transform.rotate(afb_kogels,90)

pygame.init()
screen = pygame.display.set_mode((BREEDTE,HOOGTE ))

bunkers=[]
# bunker 1
levens=[]

for i in range(3):
    levens.append(Speler(r"Space-Invaders-PNG-Images-HD.png",r"kogel.png",BREEDTE,HOOGTE,2,10))

Groote_bunker=5

for i in range(7):
    for j in range(13):
        bunkers.append(Bunker(50+j*5,HOOGTE-100+i*Groote_bunker,Groote_bunker,Groote_bunker,(0,255,0)))
   

for i in range(7):
    for j in range(13):
        bunkers.append(Bunker(175+j*5,HOOGTE-100+i*Groote_bunker,Groote_bunker,Groote_bunker,(0,255,0)))

for i in range(7):
    for j in range(13):
        bunkers.append(Bunker(350+j*5,HOOGTE-100+i*Groote_bunker,Groote_bunker,Groote_bunker,(0,255,0)))
   
for i in range(7):
    for j in range(13):
        bunkers.append(Bunker(475+j*5,HOOGTE-100+i*Groote_bunker,Groote_bunker,Groote_bunker,(0,255,0)))
   
tegenstanders=[]
richting = "Links"
beweging= "horizontaal"
Huidigetegenstander = -1


afbTegenstander_breedte=40
afbTegenstander_hoogte=60
for i in range(5):
    for j in range(10):
        tegenstanders.append(Tegenstander(r"mannetje rij 1.png",r"kogel.png",100+j*afbTegenstander_breedte,350-i*afbTegenstander_hoogte,3))

gewonnen= 0


klok = pygame.time.Clock()
FPS = 60
gebotst = []

score= 0
font = pygame.font.SysFont("Arial", 72)
font2=pygame.font.SysFont("Arial", 30)
hallo_afb = font.render( "YOU WIN", True, (0,255,0) )
verloren_afb = font.render( "YOU LOSE" , True, (255,0,0) )

camera = gestureDetectionCamera.Webcam(1)
camera.start()

while True:
    klok.tick(FPS)

    for event in pygame.event.get():
            # Check for the quit event
            if event.type == pygame.QUIT:
                # Quit the game
                camera.stop()
                pygame.quit()
    
    if len(levens) == 0:
        gewonnen = -1
    elif len(tegenstanders) == 0:
        # 1. Definieer een font voor de tekst. 
        # 2. Maak afbeelding van tekst (via methode render).
        # 3. Blit afbeelding op frame.
        gewonnen=1
    else:
        "doen"
        speler = levens[0]

        hand_beweging = {"naar_links": True , "naar_rechts": False, "schieten": False, "positie":(0.1,0.1)}
        pygame.draw.circle(screen,(255,0,0),(hand_beweging["positie"][0]*BREEDTE,hand_beweging["positie"][1]*HOOGTE), 5)
        pygame.event.pump()
        
        # muis = pygame.mouse.get_pos()

        # hand_beweging = {"naar_links": muis[0] < BREEDTE/2, "naar_rechts": muis[0] > BREEDTE/2, "schieten": pygame.mouse.get_pressed()[0]}

       


        speler.bewegen(hand_beweging)
        speler.schieten(hand_beweging)
        for index,kogel in enumerate(speler.kogels) : speler.kogels[index][1] = speler.kogels[index][1] - speler.kogelsnelheid

        Huidigetegenstander+=1
        if Huidigetegenstander >= len(tegenstanders):
            Huidigetegenstander= 0
            beweging= "horizontaal"
            if any(gebotst): 
                # for tegenstander in tegenstanders:
                #     tegenstander.beweegverticaal()
                beweging = "verticaal"
                richting = "Links" if richting == "Rechts" else "Rechts"
            gebotst = []

        if beweging == "horizontaal":
            gebotst.append(tegenstanders[Huidigetegenstander].beweeghorizontaal(richting,BREEDTE))
        else:
            tegenstanders[Huidigetegenstander].beweegverticaal()
        
        Huidigetegenstander,score = speler.raakttegenstander(tegenstanders, Huidigetegenstander, score)
        speler.raaktbunker(bunkers)
        for tegenstander in tegenstanders:
            tegenstander.raaktspeler(speler,levens)
            tegenstander.raaktbunker(bunkers)
        

        for tegenstander in tegenstanders:
            tegenstander.kogeltoevoegen(tegenstanders)
            tegenstander.kogelbewegen()
            
    
    "tekenen"
    screen.fill( (0,0,0) )
    
    for bunker in bunkers:
        pygame.draw.rect(screen,bunker.kleur,bunker)

    for tegenstander in tegenstanders:
        screen.blit(tegenstander.afb,(tegenstander.x,tegenstander.y))
    
    for tegenstander in tegenstanders:
        tegenstander.kogeltekenen(screen)

    if gewonnen == 1:
        screen.blit(hallo_afb, (100,100))
    elif gewonnen == -1:
        screen.blit(verloren_afb,(100,100))
    else:
        if speler.kan_schieten:
            kleur_cursor = (0,255,0)
        else:
            kleur_cursor = (255,0,0)

        if camera.handMovement != {}:
            pygame.draw.circle(screen,kleur_cursor,(camera.handMovement['middleFingerMCPXPosition'] * BREEDTE,camera.handMovement['middleFingerMCPYPosition'] * HOOGTE), 10)
        screen.blit(speler.afb,(speler.x,speler.y))
        for index,kogel in enumerate(speler.kogels): screen.blit(afb_kogels, (kogel[0],kogel[1]))
        Levens_afb=font2.render(f"Levens: {len(levens)}/3",1,True, (0,255,0) )
        High_score=font2.render(f"High-score: {score}",True, (0,255,0))
        screen.blit(Levens_afb,(20,10))
        screen.blit(High_score,(20,40))

    pygame.display.flip()