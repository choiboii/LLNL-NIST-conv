# This is a script designed to convert thermodynamic data of elements taken from nist.gov into different units.
import time
import scipy.constants as spc


''' Conversion equations:

    Each conversion has its inverse equation supported.


    Supported conversions for entropy: (Entropy conversions start with "S")
    J/mol/k <-> kB/atom
    erg/g/K (cgs) <-> kB/atom
    J/g/K (SI units) <-> kB/atom
    Mbar-cc/g/K (bdivK) <-> kB/atom
    J/mol/K <-> J/g/K
    J/g/K <-> erg/g/K (cgs)
    Mbar-cc/g/K (bdivK) <-> J/g/K


    Supported conversions for energy: (Energy conversions start with "E")
    kJ/mol <-> meV/atom   
    eV/atom <-> er/g
    J/g <-> eV/atom
    Ry/atom <-> eV/atom
    Ry/atom <-> erg/g

    '''


# Entropy conversions:
def Sconvert_JmolK_to_kBatom(entropy):
    return entropy / (spc.k * spc.N_A)


def Sconvert_kBatom_to_JmolK(entropy):
    return entropy * (spc.k * spc.N_A)


def Sconvert_erggK_to_kBatom(entropy, atomic_mass):
    return entropy * atomic_mass / (spc.k / spc.erg * spc.N_A)


def Sconvert_kBatom_to_erggK(entropy, atomic_mass):
    return entropy * spc.k / spc.erg * spc.N_A / atomic_mass


def Sconvert_JgK_to_kBatom(entropy, atomic_mass):
    return entropy * atomic_mass / (spc.k * spc.N_A)


def Sconvert_kBatom_to_JgK(entropy, atomic_mass):
    return entropy * spc.k * spc.N_A / atomic_mass


def Sconvert_MbarccgK_to_kBatom(entropy, atomic_mass):
    return entropy * atomic_mass * pow(10, 5) / (spc.k * spc.N_A)


def Sconvert_kBatom_to_MbarccgK(entropy, atomic_mass):
    return entropy * spc.k * spc.N_A / (atomic_mass * pow(10, 5))


def Sconvert_JmolK_to_JgK(entropy, atomic_mass):
    return entropy / atomic_mass


def Sconvert_JgK_to_JmolK(entropy, atomic_mass):
    return entropy * atomic_mass


def Sconvert_JgK_to_erggK(entropy):
    return entropy / spc.erg


def Sconvert_erggK_to_JgK(entropy):
    return entropy * spc.erg


def Sconvert_MbarccgK_to_JgK(entropy):
    return entropy * pow(10, 5)


def Sconvert_JgK_to_MbarccgK(entropy):
    return entropy / pow(10, 5)


# Energy conversions:
def Econvert_kJmol_to_meVatom(energy):
    return 1000 * energy / (spc.e * spc.N_A / 1000)


def Econvert_meVatom_to_kJmol(energy):
    return energy * (spc.e * spc.N_A / 1000) / 1000


def Econvert_eVatom_to_ergg(energy, atomic_mass):
    return energy * (spc.e * spc.N_A / spc.erg) / atomic_mass


def Econvert_ergg_to_eVatom(energy, atomic_mass):
    return energy * atomic_mass / (spc.e * spc.N_A / spc.erg)


def Econvert_Jg_to_eVatom(energy, atomic_mass):
    return energy * atomic_mass / (spc.e * spc.N_A)


def Econvert_eVatom_to_Jg(energy, atomic_mass):
    return energy * spc.e * spc.N_A / atomic_mass


def Econvert_Ryatom_to_ergg(energy, atomic_mass):
    return energy * (2.17987 * pow(10, -11)) * spc.N_A / atomic_mass


def Econvert_ergg_to_Ryatom(energy, atomic_mass):
    return energy * atomic_mass / ((2.17987 * pow(10, -11)) * spc.N_A)


def Econvert_Ryatom_to_eVatom(energy):
    return energy * 13.6056


def Econvert_eVatom_to_Ryatom(energy):
    return energy / 13.6056


''' Updates and creates a file called "atomic_masses_list.txt" to use for creating the conversion tables for
    entropy/energy. This draws values from a .txt file called "howerton_atomic_masses.txt" which is extracted from
    a .pdf file containing the tested atomic mass values from a paper by "Robert J. Howerton" on July 16, 1985.
'''


def update_atomic_mass():
    import mendeleev as md
    atomic_mass_list = []
    for i in range(118):
        element = md.element(i + 1)
        atomic_mass_list.append(element.atomic_weight)

    try:
        with open("howerton_atomic_masses.txt") as in_file:
            for line in in_file:
                atomic_contents = line.split(" ")
                atomic_number = int(atomic_contents[0])
                atomic_mass = float(atomic_contents[2])
                atomic_mass_list[atomic_number - 1] = atomic_mass
    except FileNotFoundError:
        print("\nThere is no such file called howerton_atomic_masses!")
        exit(-1)

    try:
        with open("atomic_masses_list.txt", "w") as out_file:
            for i in range(118):
                element = md.element(i + 1)
                out_file.write("{} %s %s : {}\n".format((i + 1), atomic_mass_list[i]) % (element.symbol, element.name))
    except FileNotFoundError:
        print("\nThere is no such file called atomic_masses_list!")
        exit(-1)


''' Returns an array of all the atomic mass values extracted from the .txt file, "atomic_masses_list.txt"
    The index of an atomic mass refers to their atomic number - 1; ex. atomic_masses[0] = Hydrogen's AM = 1.00798.
'''


def create_atomic_mass_list():
    atomic_masses = []
    try:
        with open("atomic_masses_list.txt") as in_file:
            for line in in_file:
                line_elements = line.split(" ")
                atomic_masses.append(float(line_elements[4]))
    except FileNotFoundError:
        print("\nThere is no such file called atomic_masses_list")
        exit(-1)

    return atomic_masses


# Creation of conversion tables:
''' Each conversion table goes through this process:
    Extracts the values from "atomic_masses_list.txt" into an array using create_atomic_mass_list().
    Creates a new file corresponding to the type of table and unit conversion direction.
    Writes a table with all of the conversion factors corresponding to their unit and element.
'''


def create_conversion_table_entropy():
    atomic_masses = create_atomic_mass_list()
    out_file_name = "entropy_conversion_table.txt"
    try:
        with open(out_file_name, "w") as out_file:
            out_file.write("Starting Unit\t\t\terg/g/K\t\tMbar-cc/g/K\tJ/g/K\t\tJ/mol/K\n")
            out_file.write("Ending Unit\t\t\tkB/atom\t\tkB/atom\t\tkB/atom\t\tJ/g/K\n")
            out_file.write("Element\t\tAMass\n")
            for i in range(118):
                # Obtain all of the correct conversion factors for each unit conversion
                conversion_1 = Sconvert_erggK_to_kBatom(1, atomic_masses[i])
                conversion_2 = Sconvert_JgK_to_kBatom(1, atomic_masses[i])
                conversion_3 = Sconvert_MbarccgK_to_kBatom(1, atomic_masses[i])
                conversion_4 = Sconvert_JmolK_to_JgK(1, atomic_masses[i])
                out_file.write("{}\t\t{:.6f}\t{:.6E}\t{:.6f}\t{:.6E}\t{:.6f}\n".format(i + 1, atomic_masses[i],
                                                                                       conversion_1, conversion_2,
                                                                                       conversion_3, conversion_4))
    except FileNotFoundError:
        print("\nThere is no such file called %s!" % out_file_name)
        exit(-1)


def create_conversion_table_entropy_reverse():
    atomic_masses = create_atomic_mass_list()
    out_file_name = "entropy_conversion_table_reverse.txt"
    try:
        with open(out_file_name, "w") as out_file:
            out_file.write("Starting Unit\t\t\tkB/atom\t\tkB/atom\t\tkB/atom\t\tJ/g/K\n")
            out_file.write("Ending Unit\t\t\terg/g/K\t\tMbar-cc/g/K\tJ/g/K\t\tJ/mol/K\n")
            out_file.write("Element\t\tAMass\n")
            for i in range(118):
                # Obtain all of the correct conversion factors for each unit conversion
                conversion_1 = Sconvert_kBatom_to_erggK(1, atomic_masses[i])
                conversion_2 = Sconvert_kBatom_to_JgK(1, atomic_masses[i])
                conversion_3 = Sconvert_kBatom_to_MbarccgK(1, atomic_masses[i])
                conversion_4 = Sconvert_JgK_to_JmolK(1, atomic_masses[i])
                out_file.write("{}\t\t{:.6f}\t{:.6E}\t{:.6f}\t{:.6E}\t{:.6f}\n".format(i + 1, atomic_masses[i],
                                                                                       conversion_1, conversion_2,
                                                                                       conversion_3, conversion_4))
    except FileNotFoundError:
        print("\nThere is no such file called %s!" % out_file_name)
        exit(-1)


def create_conversion_table_energy():
    atomic_masses = create_atomic_mass_list()
    out_file_name = "energy_conversion_table.txt"
    try:
        with open(out_file_name, "w") as out_file:
            out_file.write("Starting Unit\t\t\terg/g\t\tJ/g\t\tRy/atom\t\tRy/atom\n")
            out_file.write("Ending Unit\t\t\teV/atom\t\teV/atom\t\teV/atom\t\terg/g\n")
            out_file.write("Element\t\tAMass\n")
            for i in range(118):
                # Obtain all of the correct conversion factors for each unit conversion
                conversion_1 = Econvert_ergg_to_eVatom(1, atomic_masses[i])
                conversion_2 = Econvert_Jg_to_eVatom(1, atomic_masses[i])
                conversion_3 = Econvert_Ryatom_to_eVatom(1)
                conversion_4 = Econvert_Ryatom_to_ergg(1, atomic_masses[i])
                out_file.write("{}\t\t{:.6f}\t{:.6E}\t{:.6E}\t{:.6f}\t{:.6E}\n".format(i + 1, atomic_masses[i],
                                                                                       conversion_1, conversion_2,
                                                                                       conversion_3, conversion_4))
    except FileNotFoundError:
        print("\nThere is no such file called %s!" % out_file_name)
        exit(-1)


def create_conversion_table_energy_reverse():
    atomic_masses = create_atomic_mass_list()
    out_file_name = "energy_conversion_table_reverse.txt"
    try:
        with open(out_file_name, "w") as out_file:
            out_file.write("Starting Unit\t\t\teV/atom\t\teV/atom\t\teV/atom\t\terg/g\n")
            out_file.write("Ending Unit\t\t\terg/g\t\tJ/g\t\tRy/atom\t\tRy/atom\n")
            out_file.write("Element\t\tAMass\n")
            for i in range(118):
                # Obtain all of the correct conversion factors for each unit conversion
                conversion_1 = Econvert_eVatom_to_ergg(1, atomic_masses[i])
                conversion_2 = Econvert_eVatom_to_Jg(1, atomic_masses[i])
                conversion_3 = Econvert_eVatom_to_Ryatom(1)
                conversion_4 = Econvert_ergg_to_Ryatom(1, atomic_masses[i])
                out_file.write("{}\t\t{:.6f}\t{:.6E}\t{:.6f}\t{:.6f}\t{:.6E}\n".format(i + 1, atomic_masses[i],
                                                                                       conversion_1, conversion_2,
                                                                                       conversion_3, conversion_4))
    except FileNotFoundError:
        print("\nThere is no such file called %s!" % out_file_name)
        exit(-1)


''' This method searches a specific table in order to find the right factor asked by the user.
    The table used for the parameter is specified when using the method "get_factor_from_table()"
'''


def access_factor_from_table(table, element, starting_unit, ending_unit):
    in_file_name = table + ".txt"
    starting_index = []
    ending_index = []

    try:
        with open(in_file_name) as in_file:
            for line in in_file:
                line_elements = line.split("\t")
                line_data = list(filter(None, line_elements))
                line_data[len(line_data) - 1] = line_data[len(line_data) - 1].rstrip("\n")
                ''' Find the correct index for both the starting unit and ending unit, as some tables have the same unit
                    listed for a starting unit or ending unit.
                '''
                if line_data[0] == "Starting Unit":
                    for count, unit in enumerate(line_data):
                        if unit == starting_unit:
                            starting_index.append(count)
                if line_data[0] == "Ending Unit":
                    for count, unit in enumerate(line_data):
                        if unit == ending_unit:
                            ending_index.append(count)
                # If a common index exists when finding the indices for the starting unit and ending unit:
                unit_index = common_member(starting_index, ending_index)
                for i in unit_index:
                    index = i

                ''' Index will always be defined before this call, as the program searches for the common index before
                    trying to find the element to match the user inputted.
                '''
                if line_data[0] == str(element):
                    with open("atomic_masses_list.txt") as f:
                        for _line in f:
                            element_data = _line.split(" ")
                            if str(element) == element_data[0]:
                                element_name = element_data[2]
                    print("%s, %s -> %s: %s " % (element_name, starting_unit, ending_unit, line_data[index + 1]))
                    choice = input("\nWould you like to get another conversion factor? (Y/N) ")
                    if choice.upper() == "Y":
                        get_factor_from_table()
                    else:
                        print("\nExiting...")
                        time.sleep(.5)
                        exit(0)

    except FileNotFoundError:
        print("\nThere is no such file called %s!" % in_file_name)
        exit(-1)


''' Helper method for access_factor_from_table()
    Finds a common member between two Sets.
'''


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)

    return a_set & b_set


''' This is the main method for getting the user input and outputting the correct conversion factor.
    This method first gets the user's input of parameters consisting of the element, starting unit, and ending unit.
    The input is protected regardless of whether the wrong number of elements
'''


def get_factor_from_table():
    # Manual list of units; to be updated when adding more units for functionality updates.
    units = ["erg/g/K", "Mbar-cc/g/K", "J/g/K", "J/mol/K", "kB/atom", "erg/g", "J/g", "Ry/atom", "eV/atom"]
    while True:
        try:
            choice = input("Please state the element, starting unit, and ending unit in this order:\n")
            choice_parameters = choice.split(" ")
            # Check if it is possible to fetch the element, and grab the element data from the mendeleev database.
            try:
                element = int(choice_parameters[0])
            except ValueError:
                with open("atomic_masses_list.txt") as in_file:
                    for line in in_file:
                        line_elements = line.split(" ")
                        if line_elements[1] == choice_parameters[0] or line_elements[2] == choice_parameters[0]:
                            element = int(line_elements[0])
                            break

            # Make sure there are exactly three elements in the parameters
            if len(choice_parameters) != 3:
                continue

            # Check if the units are valid and supported
            if choice_parameters[1] not in units:
                print("%s is not a supported unit / Please check your spelling.\n" % choice_parameters[1])
                continue
            if choice_parameters[2] not in units:
                print("%s is not a supported unit / Please check your spelling.\n" % choice_parameters[2])
                continue
        except (ValueError, IndexError):
            continue
        else:
            break

    # Entropy conditions:
    if choice_parameters[1] == "erg/g/K" or choice_parameters[1] == "Mbar-cc/g/K" or \
            choice_parameters[1] == "J/mol/K":
        access_factor_from_table("entropy_conversion_table", element, choice_parameters[1], choice_parameters[2])
    elif choice_parameters[1] == "J/g/K":
        if choice_parameters[2] == "kB/atom":
            access_factor_from_table("entropy_conversion_table", element, choice_parameters[1], choice_parameters[2])
        else:
            access_factor_from_table("entropy_conversion_table_reverse", element, choice_parameters[1],
                                     choice_parameters[2])
    elif choice_parameters[1] == "kB/atom":
        access_factor_from_table("entropy_conversion_table_reverse", element, choice_parameters[1],
                                 choice_parameters[2])

    # Energy conditions:
    elif choice_parameters[1] == "J/g" or choice_parameters == "Ry/atom":
        access_factor_from_table("energy_conversion_table", element, choice_parameters[1], choice_parameters[2])
    elif choice_parameters[1] == "erg/g":
        if choice_parameters[2] == "eV/atom":
            access_factor_from_table("energy_conversion_table", element, choice_parameters[1], choice_parameters[2])
        else:
            access_factor_from_table("energy_conversion_table_reverse", element, choice_parameters[1],
                                     choice_parameters[2])
    elif choice_parameters[1] == "eV/atom":
        access_factor_from_table("energy_conversion_table_reverse", element, choice_parameters[1], choice_parameters[2])

    # If it does match the correct conditions for conversion, restart the method and try again.
    else:
        print("\nInvalid input for element, starting unit, or ending unit!\n")
        get_factor_from_table()


# ==================================================================================================================== #


def main():
    """ This print statement prints out information about the parameters and conversions supported at the beginning of
            the program. It looks like this:

            ------------------------------
            Parameter Format:
            "Name/Atomic Number/Symbol" "Starting Unit" "Ending Unit"
            ------------------------------
            Current Conversions Supported:

                erg/g/K (cgs) <-> kB/atom
                J/g/K (SI units) <-> kB/atom
                Mbar-cc/g/K (bdivK) <-> kB/atom
                J/mol/K <-> J/g/K

                eV/atom <-> erg/g
                J/g <-> eV/atom
                Ry/atom <-> eV/atom
                Ry/atom <-> erg/g
            ------------------------------
                Examples:
                4 J/g/K kB/atom
                Carbon erg/g eV/atom
                Zr kB/atom Mbar-cc/g/K%s"
            ------------------------------

        """

    line_break = "------------------------------\n"
    print("%sParameter Format:\n\"Name/Atomic Number/Symbol\" \"Starting Unit\" \"Ending Unit\"\n%sCurrent Conversions "
          "Supported:\n\n\terg/g/K (cgs) <-> kB/atom\n\tJ/g/K (SI units) <-> kB/atom\n\tMbar-cc/g/K (bdivK) <-> "
          "kB/atom\n\tJ/mol/K <-> J/g/K\n\n\teV/atom <-> erg/g\n\tJ/g <-> eV/atom\n\tRy/atom <-> eV/atom\n\tRy/atom "
          "<-> erg/g\n%sExamples:\n4 J/g/K kB/atom\nCarbon erg/g eV/atom\nZr kB/atom Mbar-cc/g/K\n%s" % (line_break,
                                                                                                         line_break,
                                                                                                         line_break,
                                                                                                         line_break))

    # update_atomic_mass() # Only use this line to update the atomic mass (AM) list if there are changes to AM values
    create_conversion_table_entropy()
    create_conversion_table_entropy_reverse()
    create_conversion_table_energy()
    create_conversion_table_energy_reverse()
    get_factor_from_table()


if __name__ == "__main__":
    main()
