import pygame,random,sys
pygame.init();W,H=400,600;S=pygame.display.set_mode((W,H));C=pygame.time.Clock()
font=pygame.font.SysFont(None,36)
def reset(): return pygame.Rect(W//2-20,H-40,40,30),[],0,False
P,F,score,over=reset();T=pygame.USEREVENT+1;pygame.time.set_timer(T,800)

while 1:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:pygame.quit();sys.exit()
        if over and e.type==pygame.KEYDOWN and e.key==pygame.K_r: P,F,score,over=reset()
        if not over and e.type==T: F.append(pygame.Rect(random.randint(0,W-20),-20,20,20))
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:P.x-=5
    if keys[pygame.K_RIGHT]:P.x+=5
    P.clamp_ip(S.get_rect())

    S.fill((30,60,30))
    if not over:
        for f in F[:]:
            f.y+=5;pygame.draw.rect(S,(200,0,0),f)
            if f.colliderect(P):over=True
            if f.y>H:F.remove(f);score+=1
    else:
        txt1=font.render("Game Over!",1,(255,255,255))
        txt2=font.render("Tekan R untuk Ulang",1,(255,255,255))
        S.blit(txt1,(W//2-txt1.get_width()//2,H//2-40))
        S.blit(txt2,(W//2-txt2.get_width()//2,H//2))

    pygame.draw.rect(S,(255,200,50),P)
    S.blit(font.render(f"Skor: {score}",1,(255,255,255)),(10,10))
    pygame.display.flip();C.tick(60)
