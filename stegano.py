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
    taille_binaire = bin(len(message_binaire))[2:]
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
    print(message_lenght, taille_message)
    
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
    hide("Je fais un teste plus performant avec un texte plus grand voir si ca marche", "eren.png")
    read("cache.png")
    
    
    # chaine = "010010100110010100100000011101000110010101110011011101000110010100100000011101010110111000100000"
    # split_by(chaine, 8)
    
    """
    01001010011001010010000001110100011001010111001101110100011001010010000001110101011011100010000001110000011
    0010101010111010100100000011011000110000100100000011100100110010101100111011011000110010100100000011001000
    11001010111001100100000001100110011000100100000011000110110000101110010011000010110
    001101110100011001010111001001100101011100110010000001110110011011110110100101110010001000000111001101101001
    
    0100101001100101001000000111010001100101011100110111010001100101001000000111010101101110001000000111000001100
    101011101010010000001101100011000010010000001110010011001010110011101101100011001010010000
    """
    
    