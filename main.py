from geotools import convertgeo
from sys import exit


def main():
    print("\nFERRAMENTA CONVERTGEO")
    running = True
    while (running):
        # Print the menu
        print()  # blank line
        print('Selecionar opção:\n')
        print('\t1. Converter coordenadas UTM para grau decimal')
        print('\t2. Converter .csv para .kml')
        print('\t3. Sair\n')

        option = int(input('Número opção: '))
        if option == 1:
            name = input("Nome do ponto (ID por padrão): ")
            if name == '':
                name = 'ID'
            else:
                pass
            x_coord = float(input("X(m): "))
            y_coord = float(input("Y(m): "))
            utm_coord = float(input("UTM: "))

            data = convertgeo()
            coord = data.utm2geodeg(x_coord, y_coord, utm_coord, name)
            out = {'Point': coord[0], 'X': coord[1], 'Y': coord[2]}

            print('Ponto {0}:\n X: {1} m\n Y: {2} m'.format(
                out['Point'], out['X'], out['Y']))

        elif option == 2:
            tl_name = input('Nome Linha de Transmissão: ')
            # Datum = input('Insert Datum of Geographic Projection (Latitude, Longitude): ')
            csv_file_input = input('Nome do arquivo de entrada .csv: ')
            kml_file_output = input('Nome do arquivo de saída .kml: ')

            data = convertgeo()
            data.csv2kml(csv_file_input, kml_file_output, tl_name)
        else:
            exit()


if __name__ == '__main__':
    main()
