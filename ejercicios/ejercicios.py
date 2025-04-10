def palabra_invertida(frase, caracter):
    palabras = frase.split()

    i = 0
    while i < len(palabras):
        palabra = palabras[i]
        if palabra[0].lower() == caracter.lower():
            print(palabra[::-1])
            return
        i += 1

    print("No se encontró ninguna palabra")

frase = input("Introduce una frase: ")
caracter = input("Introduce el carácter: ")

palabra_invertida(frase, caracter)



