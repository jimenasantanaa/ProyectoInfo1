F = open("personas.txt", "r")
linea = F.readline()

conteo_edades = {}

while linea:
    trozos = linea.split()
    edad = int(trozos[1])

    if edad in conteo_edades:
        conteo_edades[edad] += 1
    else:
        conteo_edades[edad] = 1

    linea = F.readline()

F.close()
