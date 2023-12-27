from PIL import Image
from numpy import asarray, array

image = Image.open("eren.png")
data = asarray(image)
donnees = array(data)

# on convertit le message en binaire
message = "Bonjour"
message_binaire = ""
for elt in message:
    binary = bin(ord(elt))[2:]
    while len(binary) < 8:
        binary = "0" + binary
    message_binaire += binary
taille_binaire = bin(len(message))[2:]
while len(taille_binaire) < 8:
    taille_binaire = "0" + taille_binaire

message_binaire = taille_binaire + message_binaire
    
# on va parcourir notre tableau pour cacher le message dans chaque bits de chaque pixels
tour = 0
for i in range(len(donnees)):
    for j in range(len(donnees[i])):
        for k in range(len(donnees[i][j])):
            # print(donnees[i][j][k])
            pixel_unit = list(bin(donnees[i][j][k])[2:])
            del pixel_unit[-1]
            pixel_unit.append(message_binaire[tour])
            decimal = int("".join(pixel_unit), 2)
            donnees[i][j][k] = decimal
            # print(donnees[i][j][k])
            
            if tour >= len(message_binaire):
                break
        if tour >= len(message_binaire):
            break
    if tour >= len(message_binaire):
        break

Image.fromarray(donnees).save("cache.png")