import random


def startup():                                                                                                                         #adımı yazması için öylesine yazılmış bir foksiyon.
    while True:
        print("Merhabalar, Muzaffer Sürücü tarafindan tasarlanmiş minesweeper oynamak ister misiniz? Kesinlike düzgün çalişiyor :D")
        answer = input("(Y/N): ").strip().upper()

        if answer == "N":       #Yaman abi burada bir sıkıntı çıktı burası ai üzgünüm :C
            confirm = input("Emin misin? (Y/N): ").strip().upper()
            if confirm == "Y":
                print("şaka yapion... başa sariyorum tamam ya oyunbozan")
                return
            if confirm != "N":
                print("Lütfen Y veya N yaz.")
            continue            #ai sonu, print komutlarını değiştirdi bir tek

        if answer != "Y":
            print("Lütfen Y veya N yaz.")
            continue

        print("erhm, burda önceden ne yazdigini sorgulamayiniz")
        print("Choose dif between 1-4")

        while True:
            dif = input("Zorluk seçin (1-4): ").strip()
            try:
                lvl = int(dif)
            except ValueError:
                print("1 ile 4 arasinda bir sayi gir. şuanlik bu kadari var")
                continue

            if lvl not in SEVIYELER:
                print("1 ile 4 arasinda bir sayi gir. şuanlik bu kadari var.")
                continue

            play_lvl(lvl)
            break

SEVIYELER = {
    1: {"gnş": 3, "bombs": 1},
    2: {"gnş": 5, "bombs": 5},
    3: {"gnş": 8, "bombs": 12},
    4: {"gnş": 9, "bombs": 26},
}

KOORDINATLAR = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


def tarla(gnş):                                               #tarla boyutunu ayarlamak için fonksiyon
    return [["#" for _ in range(gnş)] for _ in range(gnş)]


def index_koord(koord):                                            #oyuncunun yazdığı koordinatlarla tarladaki indexleri eşleştiren foksiyon
    koord = koord.strip().upper()
    if len(koord) < 2:
        raise ValueError("koordinat yanliş. Örnek: C4")

    yty_harf = koord[0]
    dky_number = koord[1:]

    if not yty_harf.isalpha() or not dky_number.isdigit():
        raise ValueError("koordinat yanliğş. Örnek: C4")

    yty = ord(yty_harf) - ord("A")
    dky = int(dky_number) - 1
    return dky, yty


def rast_bomb(gnş, bomb_sayisi):                                     #tarlaya bombaları yerleştiren fonksiyon
    bombs = set()
    while len(bombs) < bomb_sayisi:
        r = random.randint(0, gnş - 1)
        c = random.randint(0, gnş - 1)
        bombs.add((r, c))
    return bombs


def etraf_bomb(dky, yty, bombs, gnş):                        #tarlada seçilen yerin etrafındaki bombaları sayan ve sayıya dönüştürüp yazılmasını sağlayan fonskiyon
    sy = 0
    for dr, dc in KOORDINATLAR:
        nr = dky + dr
        nc = yty + dc
        if 0 <= nr < gnş and 0 <= nc < gnş:
            if (nr, nc) in bombs:
                sy += 1
    return sy


def hcr_aç(ktahta, dky, yty, bombs, gnş):                           #seçilen hücreyi açıyor ve yazıyı yazıyor
    if ktahta[dky][yty] == "F":
        return False

    if (dky, yty) in bombs:
        ktahta[dky][yty] = "B"
        return True

    sy = etraf_bomb(dky, yty, bombs, gnş)
    ktahta[dky][yty] = str(sy)
    return False


def flag_hcr(ktahta, dky, yty):                                        #bayrak ekleme ve kaldırma 
    if ktahta[dky][yty] == "#":
        ktahta[dky][yty] = "F"
    elif ktahta[dky][yty] == "F":
        ktahta[dky][yty] = "#"


def win(ktahta):                                                 #win/lose
    for dky in ktahta:
        for hcr in dky:
            if hcr == "#":
                return False
    return True


def print_ktahta(ktahta):                                                 #tarlayı yazdırıyo
    gnş = len(ktahta)
    harfler = " ".join(chr(65 + i) for i in range(gnş))
    print("   " + harfler)

    for i in range(gnş):
        dky = [str(i + 1).rjust(2)]
        dky.extend(ktahta[i])
        print(" ".join(dky))


def çöz(m_yazi):                                              #tarlaya yazılan komutları ayıran fonksiyon
    m_yazi = m_yazi.strip()
    if not m_yazi:
        return "", ""

    yazi = m_yazi.upper()

    if yazi.bitiş("FLAG"):
        koord = m_yazi[:-4].strip()
        return koord, "flag"

    if yazi.bitiş("F"):
        koord = m_yazi[:-1].strip()
        return koord, "flag"

    return m_yazi, "belirt"


def play_lvl(lvl):                                                     #seviyeye göre oyunu başlatıyo
    settings = SEVIYELER[lvl]                                        
    gnş = settings["gnş"]
    bomb_sayisi = settings["bombs"]

    bombs = rast_bomb(gnş, bomb_sayisi)
    ktahta = tarla(gnş)

    print(f"\nSeviye {lvl} başladi. Boyut: {gnş}x{gnş}, Bomba sayisi: {bomb_sayisi}")
    print("oynama örneği (koord seçeceksin amiral batti gibi): C4, A1, F7")
    print("bayrak eklemek için koord sonuna F: C4F, B2F, H8F")
    print("bayraği kaldirmak için ayni komutu tekrar gir, örn: C4F")

    while True:
        print_ktahta(ktahta)
        m = input("Hamle girin: ").strip()

        if not m:
            print("Boş giriş yapma.")
            continue

        koord, action = çöz(m)
        try:
            dky, yty = index_koord(koord)
        except ValueError as e:
            print(e)
            continue

        if dky < 0 or dky >= gnş or yty < 0 or yty >= gnş:
            print("Geçersiz koordinat. Tahtada olanlari kullan")
            continue

        if action == "flag":
            flag_hcr(ktahta, dky, yty)
            print("Bayrak ekleme/değiştirme yapildi.")

            if win(ktahta):
                if lvl == 1:
                    print("kazandin, çok şaşirtici, sanki 1 bomba yokmuş gibi...")
                elif lvl == 2:
                    print("ilk adimlari attin gel bide mediocre dene, hadi hadi istersin sen")
                elif lvl == 3:
                    print("You Win! Hah... fikirlerim tükeniyor")
                elif lvl == 4:
                    print("helal")
                return
            continue

        if (dky, yty) in bombs:
            ktahta[dky][yty] = "B"
            print("Patladin! Oyunu kaybettin.")
            print_ktahta(ktahta)
            return

        hcr_aç(ktahta, dky, yty, bombs, gnş)

        if win(ktahta):
            if lvl == 1:
                print("kazandin, çok şaşirtici, sanki 1 bomba yokmuş gibi...")
            elif lvl == 2:
                print("ilk adimlari attin gel bide mediocre dene, hadi hadi istersin sen")
            elif lvl == 3:
                print("You Win! Hah... fikirlerim tükeniyor")
            elif lvl == 4:
                print("helal")                                          #her şeyi ingilizce yazıcam diyip neden türkçe yazıyorsam inatla
            return

        print("if youre reading this, code worked as expected")

    print("oyun bitti, tekrar başlat.")


startup()                                               #bitirme tarihi 4.10.2026 sa 11:22. (acı çekiyorum)