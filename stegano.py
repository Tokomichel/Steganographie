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

    taille_binaire = bin(len(message_binaire))[2:]  # on converti en binaire la taille du message

    # on determine la longueur en binaire de la taille.
    # on encode la taille sur 16 bits ainsi on aura environ 2kbits d'espace
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

    # on sait que la taille a ete encoder sur "encode_lenght" bits
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

    tour = 0
    message = ""
    clear_message = ""
    step = message_lenght + encode_lenght
    for i in range(len(data)):
        for j in range(len(data[i])):
            for k in range(len(data[i][j])):
                if tour >= encode_lenght:
                    message += bin(data[i][j][k])[-1]
                    if len(message) >= 8:
                        clear_message += chr(int(message, 2))
                        message = ""
                tour += 1
                if tour >= step:
                    break
            if tour >= step:
                break
        if tour >= step:
            break


    print(clear_message)



if __name__ == "__main__":
    # hide("Je fais un teste plus performant avec un texte plus grand voir si ca marche", "eren.png")
    read("cache.png")

