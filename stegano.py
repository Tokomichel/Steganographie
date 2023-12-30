from PIL import Image
from numpy import asarray, array

def hide(message: str, image_loc: str, result_image: str = "cache.png"):
    image = Image.open(image_loc)
    data = asarray(image)
    donnees = array(data)

    # on convertit le message en binaire
    message = message
    message_binaire = ""
    for elt in message:
        binary = bin(ord(elt))[2:]
        while len(binary) < 8:
            binary = "0" + binary
        message_binaire += binary
    
    taille_binaire = bin(len(message_binaire))[2:] # on converti en binaire la taille du message
    
    # on determine la longueur en binaire de la taille.
    # on encode la taille sur 16 bits ainsi on aura environ 2ko d'espace
    while len(taille_binaire) < 16:
        taille_binaire = "0" + taille_binaire
        
    print(len(message_binaire), taille_binaire)
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
                # print(f"octet: {message_binaire[tour]} \n")
                tour += 1
                if tour >= len(message_binaire):
                    break
            if tour >= len(message_binaire):
                break
        if tour >= len(message_binaire):
            break

    Image.fromarray(donnees).save(result_image)

def read(image: str, encode_lenght: int = 16):
    # on cherche d'abord la taille du message a lire
    data = asarray(Image.open(image))
    taille_message = ""
    x = 0

    # on sait que la taille a ete encoder sur 8 bits
    for i in range(len(data)):
        for j in range(len(data[i])):
            for k in range(len(data[i][j])):
                bit = bin(data[i][j][k])[2:]
                taille_message += bit[-1]
                x += 1
                if x >= encode_lenght:
                    break
            if x >= encode_lenght:
                break
        if x >= encode_lenght:
            break
    
    message_lenght = int(taille_message, 2)
    print(f"taille du message: {message_lenght}, taille message bin: {taille_message}")
    
    tour = 0
    message = ""
    for i in range(len(data)):
        for j in range(len(data[i])):
            for k in range(len(data[i][j])):
                if tour >= encode_lenght:
                    message += bin(data[i][j][k])[-1]
                tour += 1
                if tour >= (message_lenght + encode_lenght):
                    break
            if tour >= (message_lenght + encode_lenght):
                break
        if tour >= (message_lenght + encode_lenght):
            break    
    
    # on converti le message en chaine de caractere
    # sans oublier que chaque lettre etait encodee sur 8 bits
    clear_message = ""
    x = 0
    liste = split_by(message, 8)
    
    for elt in liste:
        clear_message += chr(int(elt, 2))
    
    print(clear_message)    

def split_by(chaine: str, lenght: int) -> list:

    x = 0
    lettre = ""
    liste = []
    clear_liste = []
    for elt in chaine:
        lettre += elt
        
        if x < (lenght - 1):
            x += 1 
        else:
            liste.append(lettre)
            lettre = ""
            x = 0
    
    return liste
    

        
          
if __name__ == "__main__":
    # hide("Je fais un teste plus performant avec un texte plus grand voir si ca marche", "eren.png")
    read("cache.png")
    
    
    