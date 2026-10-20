#so its a revived txt which exists purely bc I'm lazy ahh. I realized that I have been straight up -hand writing- but still copying most of the complex tutorials. eh changed 1 or 2 of these to simpler ones
#also every note and commentary was deleten since I cant read a think with those I really did fried my head back than huh

import pygame
pygame.init()


SCREEN_W = 800
SCREEN_H = 800



screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
run = True


player = pygame.Rect(100, 400, 50, 50)
bot = pygame.Rect(700, 400, 50, 50)


clock = pygame.time.Clock()
player_x, player_y = player.topleft
bot_x, bot_y = bot.topleft
spd = 150
push_spd = spd
bot_spd = spd + 50





DS = {"ust": (0, -1), "alt": (0, 1), "sol": (-1, 0), "sag": (1, 0)}
ARKA = {"ust": "alt", "alt": "ust", "sol": "sag", "sag": "sol"}
ORDER = ["ust", "sag", "alt", "sol"]   # hate the fact I cant change these to english with "=" or ti gives error. I dont want to change them hand by hand Ç-Ç
bot_yon = "sol"



RNG = 200
EDGE = 50



def sensor_mesafe(begin, yon):
    begin = pygame.Vector2(begin)
    end = begin + pygame.Vector2(yon) * RNG 
    kesim = player.clipline(begin, end)
    if kesim:
        return begin.distance_to(pygame.Vector2(kesim[0]))   #kesim kesişim
    return RNG




def sensor_oku():
    sol_x = bot.left + 10
    sag_x = bot.right - 10
    ust_y = bot.top + 10
    alt_y = bot.bottom - 10
    return {
        "ust": (sensor_mesafe((sol_x, bot.top), DS["ust"]),
                sensor_mesafe((sag_x, bot.top), DS["ust"])),
        "alt": (sensor_mesafe((sol_x, bot.bottom), DS["alt"]),
                sensor_mesafe((sag_x, bot.bottom), DS["alt"])),
        "sol": (sensor_mesafe((bot.left, ust_y), DS["sol"]),
                sensor_mesafe((bot.left, alt_y), DS["sol"])),
        "sag": (sensor_mesafe((bot.right, ust_y), DS["sag"]),
                sensor_mesafe((bot.right, alt_y), DS["sag"])),
    }





def edge_oku():
    return {                # mesafe edge
        "sol": bot.left,
        "sag": SCREEN_W - bot.right,
        "ust": bot.top,
        "alt": SCREEN_H - bot.bottom,
    }




while run:
    screen.fill((0, 0, 0))

    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False





    previous_player = player.copy()
    previous_bot = bot.copy()





    key = pygame.key.get_pressed()
    dx = key[pygame.K_d] - key[pygame.K_a]
    dy = key[pygame.K_s] - key[pygame.K_w]





    direct = pygame.Vector2(dx, dy)     #eklediğim son şey ondan turkish
    if direct.length_squared() > 0:
        direct.normalize_ip()
        if key[pygame.K_LSHIFT]:
            push_spd = 300 #içinden geçiyordu push_spd aynı kaldığından sjsjsjsjsjsj
            player_x += direct.x * 300 * dt
            player_y += direct.y * 300 * dt
        else:
            push_spd = spd
            player_x += direct.x * spd * dt
            player_y += direct.y * spd * dt
        player.topleft = (round(player_x), round(player_y))
        #özgürüm

        #KENDİNE NOT: STR SÖZLÜĞÜ EKLE, NOT AL YA DA HEPSİNİ BAŞTAN YAZ

   
   

    sens = sensor_oku()
    EDGE_D = edge_oku()





    #kinda wrote over my own code gosh how bad was it seemingly straight pulled it off the tutorial that I will never remember
    #made it simpler
    #dont question the reason why I speak english. I just write faster like this for some unparticular reason bla bla.........bbleeehhh


    #search for player
    i = ORDER.index(bot_yon)
    right = ORDER[(i + 1) % 4]    #aint sugarcoating, took this straight from tutorial cant change it much anyway
    left = ORDER[(i - 1) % 4]
    back = ARKA[bot_yon]

    if min(sens[bot_yon]) < RNG:
        pass                      #front sensors see the player than just keep facing
    elif min(sens[right]) < RNG:
        bot_yon = right           #player on the right side, turn right
    elif min(sens[left]) < RNG:
        bot_yon = left            #same think but left
    elif min(sens[back]) < RNG:
        bot_yon = right           #behind. could have done 180 but ykr the side sensors will see it either way why write more? the fact I'm writing more with this commentary is ironic tho lmfao
    
    
    #away from edges
    kacgit = []
    if EDGE_D["sol"] < EDGE:
        kacgit.append("sag")
    if EDGE_D["sag"] < EDGE:
        kacgit.append("sol")
    if EDGE_D["ust"] < EDGE:
        kacgit.append("alt")
    if EDGE_D["alt"] < EDGE:
        kacgit.append("ust")
    if kacgit and bot_yon not in kacgit:
        bot_yon = kacgit[0]



    bot_dir = pygame.Vector2(DS[bot_yon])
    bot_x += bot_dir.x * bot_spd * dt
    bot_y += bot_dir.y * bot_spd * dt
    bot.topleft = (round(bot_x), round(bot_y))






    player_motion = pygame.Vector2(
        player.centerx - previous_player.centerx,
        player.centery - previous_player.centery,
    )
    bot_motion = pygame.Vector2(
        bot.centerx - previous_bot.centerx,
        bot.centery - previous_bot.centery,
    )




    if player.colliderect(bot):
        toward_bot = pygame.Vector2(bot.center) - pygame.Vector2(player.center)

        if toward_bot.length_squared() > 0:
            toward_bot.normalize_ip()
            player_seen = pygame.Vector2(player_motion)

            if player_seen.length_squared() > 0:
                player_seen.normalize_ip()





            
                if player_seen.dot(toward_bot) > 0:
                    bot_x += player_seen.x * push_spd * dt
                    bot_y += player_seen.y * push_spd * dt
                    bot.topleft = (round(bot_x), round(bot_y))




            bot_seen = pygame.Vector2(bot_motion)

            if bot_seen.length_squared() > 0:
                bot_seen.normalize_ip()

                if bot_seen.dot(-toward_bot) > 0:
                    player_x += bot_seen.x * bot_spd * dt
                    player_y += bot_seen.y * bot_spd * dt
                    player.topleft = (round(player_x), round(player_y))





    player.clamp_ip(screen.get_rect())
    bot.clamp_ip(screen.get_rect())
    player_x, player_y = player.topleft
    bot_x, bot_y = bot.topleft



    pygame.draw.rect(screen, (0, 0, 255), player) #reminder DS=DirectionS
    frontx, fronty = DS[bot_yon]
    sidex, sidey = -fronty, frontx
    cx = bot.centerx
    cy = bot.centery
    tip    = (bot.centerx + frontx * 25, bot.centery + fronty * 25)
    back_1 = (bot.centerx - frontx * 25 + sidex * 25, cy - fronty * 25 + sidey * 25)
    back_2 = (cx - frontx * 25 - sidex * 25, cy - fronty * 25 - sidey * 25)

    pygame.draw.polygon(screen, (255, 0, 0), [tip, back_1, back_2])



    pygame.display.update()

#ai dan yazdirim mi dediğimi istersen atarım abi okumadım fln ama ai kullanırsan chati at dedin ya. Ai kullanmadığımın kanıtı olarak
#kodun üstüne kod yazdım yazmasına ama ben daha cumartesi yazdığım koddan nasıl utanabilirim abi ya aradan 2-3 gün geçti level mi atladım ben