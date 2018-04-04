import pygame
import requests
import sys
import os
import button
import gui
import textbox
import label
import math
pygame.init()
coords = input().split(",")
response = None
zom = 1
type = "map"
def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a.split(" ")
    b_lon, b_lat = b.split(" ")
    a_lon,a_lat,b_lon,b_lat = float(a_lon),float(a_lat),float(b_lon),float(b_lat)
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)

    return distance
def get_json_request(tofind):
    geo_request = "http://geocode-maps.yandex.ru/1.x/"
    r = requests.get(geo_request, params={"geocode": tofind, "format": "json"})
    if r:return r.json()
    else: return "B"
def get_image(zoom,coords,type,points = ""):
    try:
        map_request = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "ll":",".join(coords),
            "z":zoom,
            "l":type,
            "size":"600,450"
        }
        if points: map_params["pt"] = point
        response = requests.get(map_request,params = map_params)

        if not response:
            sys.exit(1)
    except Exception as a:
        print(a)
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    res = pygame.image.load(map_file)
    os.remove(map_file)
    return res

image = get_image(zom,coords,"map")
# Инициализируем pygame

screen = pygame.display.set_mode((600, 450))
gui = gui.GUI()
map_button = button.Button(pygame.Rect(10,10,100,25),"карта")
gui.add_element(map_button)
sat_button = button.Button(pygame.Rect(10,45,100,25),"спутник")
gui.add_element(sat_button)
gib_button = button.Button(pygame.Rect(10,80,100,25),"гибрид")
gui.add_element(gib_button)
findbox = textbox.TextBox(pygame.Rect(300,10,300,50),"")
gui.add_element(findbox)
find_button = button.Button(pygame.Rect(500,70,100,25),"найти")
gui.add_element(find_button)
clear_button = button.Button(pygame.Rect(500,105,100,25),"стереть")
gui.add_element(clear_button)
stat = label.Label(pygame.Rect(10,425,600,25),"",pygame.Color("white"),pygame.Color("blue"))
gui.add_element(stat)
index_button = button.Button(pygame.Rect(500,140,100,25),"индекс")
gui.add_element(index_button)
# Рисуем картинку, загружаемую из только что созданного файла.
limit = [1,19]
# Переключаем экран и ждем закрытия окна.
running  = True
walkx=450
walky=240
wasfinded = ""
point = ""
index = False
find_button.font_color = pygame.Color("white")
map_button.font_color = pygame.Color("white")
sat_button.font_color = pygame.Color("white")
gib_button.font_color = pygame.Color("white")
index_button.font_color = pygame.Color("white")
clear_button.font_color = pygame.Color("white")
while running:
    prevcoords = coords.copy()
    for e in pygame.event.get():
        gui.get_event(e)
        if sat_button.pressed and type != "sat":
            type = "sat"
            image = get_image(zom,coords,type,point)
        if gib_button.pressed and type != "sat,skl":
            type = "sat,skl"
            image = get_image(zom,coords,type,point)
        if map_button.pressed and type != "map":
            type = "map"
            image = get_image(zom,coords,type, point)
        if (clear_button.pressed or (findbox.executed and findbox.text == "")) and point:
            point = ""
            findbox.executed = False
            image = get_image(zom, coords, type, point)
            stat.text = ""
        if index_button.pressed:
            if index:
                index_button.text ="индекс"
                stat.text = text
            else:
                index_button.text ="нет"
                stat.text = text + " | " + iindex
            index= not index
        if (find_button.pressed or findbox.executed) and wasfinded != findbox.text and findbox.text:
            findbox.executed = False
            req = get_json_request(findbox.text)
            if req != "B" and req["response"]["GeoObjectCollection"]["featureMember"]:
                try:
                    iindex = req["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                except Exception: iindex = "Unable to find"
                coordsOf = req["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
                point = ",".join(coordsOf)+",pm2gnl"
                coords = coordsOf.copy()
                image = get_image(zom,coords,type,point)
                text = req["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
                stat.text = text
                if index: stat.text +=" | " + iindex
            else:
                stat.text = "Unable to find"

        if e.type == pygame.MOUSEBUTTONDOWN and not findbox.active and all([not clear_button.pressed, not find_button.pressed,
                                                                            not gib_button.pressed,
                                                                            not index_button.pressed,
                                                                            not map_button.pressed,
                                                                            not sat_button.pressed]):
            x = str(float(coords[0]) + (walkx * ((e.pos[0] - 300) / 600)) / (2 ** (zom - 1)))
            y = str(float(coords[1]) + (-walky * ((e.pos[1] - 225) / 450)) / (2 ** (zom - 1)))
            if e.button == 1:
                req = get_json_request(",".join([x, y]))
                if req !="B" and req["response"]["GeoObjectCollection"]["featureMember"]:
                    text = req["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
                    stat.text = text
                    try:
                        iindex = req["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                    except Exception: iindex = "Unable to find"
                point = ",".join([x,y]) + ",pm2gnl"
                try:
                    image = get_image(zom, coords, type, point)
                except Exception: pass
            elif e.button == 3:
                try:
                    if findbox.text == "": findbox.text = "аптека"
                    req = requests.get("https://search-maps.yandex.ru/v1/?ll="+",".join([x, y])+"&ll="+",".join(coords)+"&spn=0.000045,0.000045&lang=ru_RU&results=1&apikey=3c4a592e-c4c0-4949-85d1-97291c87825c").json()
                    print(req)
                    if req["features"]:
                        index = "Unable to find"
                        text = req["features"][0]["properties"]["CompanyMetaData"]["name"]
                        point = ",".join(map(lambda x: str(x), req["features"][0]["geometry"]["coordinates"])) + ",pm2orl"
                        stat.text = text
                    image = get_image(zom, coords, type, point)
                except Exception: pass

        if e.type == pygame.QUIT: running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_PAGEUP and float(zom) <limit[1]:
                zom = zom+1
                image = get_image(zom,coords,type, point)
            if e.key == pygame.K_PAGEDOWN and float(zom) >limit[0]:
                zom = zom-1
                image = get_image(zom,coords,type, point)
            if e.key == pygame.K_UP:
                coords[1] = str(float(coords[1])+walky/(2**(zom-1)))
                try:
                    image = get_image(zom,coords,type, point)
                except: coords = prevcoords
            if e.key == pygame.K_DOWN:
                coords[1] = str(float(coords[1])-walky/ (2 ** (zom - 1)))
                try:
                    image = get_image(zom,coords,type, point)
                except:
                    coords = prevcoords
            if e.key == pygame.K_LEFT:
                coords[0] = str(float(coords[0]) - walkx/ (2 ** (zom - 1)))
                try:
                    image = get_image(zom, coords,type, point)
                except:
                    coords = prevcoords
            if e.key == pygame.K_RIGHT:
                coords[0] = str(float(coords[0]) + walkx/ (2 ** (zom - 1)))
                try:
                    image = get_image(zom, coords,type, point)
                except:
                    coords = prevcoords
    screen.blit(image, (0, 0))
    gui.render(screen)
    pygame.display.flip()
    pass
pygame.quit()

# Удаляем за собой файл с изображением.