# This is a script designed to convert thermodynamic data of elements taken from nist.gov into different units.

import numpy
import scipy.constants as spc
import mendeleev as md
import requests as req
from bs4 import BeautifulSoup

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


def convert_table(txt):
    txt_data = txt.split("_")
    element = txt_data[0]
    state_of_matter = txt_data[1]

    _element = md.element(element)
    if "S" in state_of_matter:
        state_of_matter = "Solid"
    elif "L" in state_of_matter:
        state_of_matter = "Liquid"

    try:
        with open(txt) as f:
            next(f)
            with open(txt[0:len(txt) - 10] + ".dat", "w") as out_file:
                out_file.write("# %s at 1 bar, %s\n# Atomic Number: %s\n# Atomic Mass: %s\n# Source: nist.gov\n"
                               % (_element.symbol, state_of_matter, _element.atomic_number, _element.atomic_weight))
                if state_of_matter == "Solid":
                    out_file.write(next(f))
                out_file.write("# Unit Conversion Factors: 1 J/mol*K = 0.1203 kB/atom   |   1 kJ/mol = 1/10.3644 "
                               "meV/atom\n")
                out_file.write("# Temperature (K)\tEntropy (kB/atom)\tEnthalpy (meV/atom)\tEntropy (J/mol*K)"
                               "\tEnthalpy(kJ/mol)\n")
                for line in f:
                    numbers = line.split("     ")
                    if '#' not in numbers[0]:
                        temperature = float(numbers[0])
                        entropy = float(numbers[2])
                        enthalpy = float(numbers[4])
                        _entropy = Sconvert_JmolK_to_kBatom(float(numbers[2]))
                        _enthalpy = Econvert_kJmol_to_meVatom(float(numbers[4]))
                        if _enthalpy > 100:
                            out_file.write(
                                "%.1f\t\t\t%.4f\t\t\t%.4f\t\t%s\t\t\t%s\n" % (temperature, _entropy, _enthalpy,
                                                                              entropy, enthalpy))
                        else:
                            out_file.write(
                                "%.1f\t\t\t%.4f\t\t\t%.4f\t\t\t%s\t\t\t%s\n" % (temperature, _entropy, _enthalpy,
                                                                                entropy, enthalpy))
    except FileNotFoundError:
        print("\nThere is no such file called %s!" % txt)
        exit(-1)


def get_main_url(element, state_of_matter):
    base_url = "https://webbook.nist.gov/"
    element_url = base_url + "/cgi/cbook.cgi?Formula=%s&NoIon=on&Units=SI&cTC=on" % element
    element_page = req.get(element_url)

    soup = BeautifulSoup(element_page.content, "html.parser")
    links = soup.find_all("a")
    if state_of_matter == "L":
        for link in links:
            link_url = link["href"]
            if "&Table=on#JANAFL" in link_url:
                return base_url + link_url
    else:
        for link in links:
            link_url = link["href"]
            if "&Table=on#JANAFS" in link_url:
                return base_url + link_url


# liquid version
def create_table_liquid(element, state_of_matter, url):
    page = req.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table_contents = soup.find_all("tr", class_="exp")

    out_file_name = "%s_%s_table.txt" % (element, state_of_matter)

    try:
        with open(out_file_name, "w") as out_file:
            out_file.write("# Temperature C S G/T H-H298.15\n")
            for row in table_contents:
                temperature = row.find_all("td")[0].text
                heat_capacity = row.find_all("td")[1].text
                entropy = row.find_all("td")[2].text
                gibbs_energy_function = row.find_all("td")[3].text
                enthalpy = row.find_all("td")[4].text
                out_file.write("%s     %s     %s     %s     %s\n" % (temperature, heat_capacity, entropy,
                                                                     gibbs_energy_function, enthalpy))
    except FileNotFoundError:
        print("\nThere is no such file called %s!" % out_file_name)
        exit(-1)


# solid version
def create_table_solid(element, state_of_matter, url):
    page = req.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table_contents = soup.find_all("table", class_="data")
    info_table_contents = table_contents[0]
    phase_columns = info_table_contents.find_all("td", class_="exp left")
    phase_names = []
    unique_phases = []

    # Checks for which columns match with the correct phase of the element
    for count, column in enumerate(phase_columns):
        column = phase_columns[count].text
        phase_text = column.split(";")[0]
        phase_names.append(phase_text)
        unique_phases = numpy.unique(phase_names)

    for count, unique_phase in enumerate(unique_phases):
        out_file_name = "%s_%s%s_table.txt" % (element, state_of_matter, str(count + 1))
        try:
            with open(out_file_name, "w") as out_file:
                out_file.write("# Temperature C S G/T H-H298.15\n")
                for phase_count, phase_index in enumerate(phase_names):
                    if unique_phase == phase_names[phase_count]:
                        out_file.write("# %s\n" % phase_columns[phase_count].text)
                        contents = table_contents[phase_count + 1].find_all("tr", class_="exp")
                        for row in contents:
                            temperature = row.find_all("td")[0].text
                            heat_capacity = row.find_all("td")[1].text
                            entropy = row.find_all("td")[2].text
                            gibbs_energy_function = row.find_all("td")[3].text
                            enthalpy = row.find_all("td")[4].text
                            out_file.write("%s     %s     %s     %s     %s\n" % (temperature, heat_capacity, entropy,
                                                                                 gibbs_energy_function, enthalpy))
        except FileNotFoundError:
            print("\nThere is no such file called %s!" % out_file_name)
            exit(-1)


""" Helper method for the creation and conversion of the solid table.

Using web
"""


def get_number_of_phases(url):
    page = req.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table_contents = soup.find_all("table", class_="data")[0]
    phase_columns = table_contents.find_all("td", class_="exp left")
    num_phases = len(numpy.unique(phase_columns))

    return num_phases


def convert_periodic_table():
    # Convert every element in the periodic table supported by mendeleev's data
    for i in range(118):
        element = md.element(i + 1)
        _element = element.symbol
        url = get_main_url(_element, "S")  # Find url for table of thermodynamic data
        # If url is invalid or there is no table with valid data, report in the console.
        if url is None:
            print("There is no data available for %s." % _element)
        else:
            # Solid table creation and conversion:
            create_table_solid(_element, "S", url)
            phases = get_number_of_phases(url)
            for count in range(phases):
                table = "%s_%s%s_table.txt" % (_element, "S", count + 1)
                convert_table(table)
            # Liquid table creation and conversion:
            url = get_main_url(_element, "L")
            create_table_liquid(_element, "L", url)
            table = "%s_%s_table.txt" % (_element, "L")
            convert_table(table)


def convert_single_element(element, state_of_matter):
    url = get_main_url(element, state_of_matter)
    # If url is invalid or there is no table with valid data, report in the console and exit.
    if url is None:
        print("There is no data available for %s.\n" % element)
        exit(-1)
    table = "%s_%s_table.txt" % (element, state_of_matter)  # Default name/format for the table file
    # Solid table creation and conversion:
    if state_of_matter == "S":
        create_table_solid(element, state_of_matter, url)
        phases = get_number_of_phases(url)
        for count in range(phases):
            table = "%s_%s%s_table.txt" % (element, state_of_matter, count + 1)
            convert_table(table)
    # Liquid table creation and conversion:
    elif state_of_matter == "L":
        create_table_liquid(element, state_of_matter, url)
        convert_table(table)
    else:
        print(state_of_matter + " is not a valid input!")
        exit(-1)


def read_table(txt):
    try:
        with open(txt) as f:
            for line in f:
                print(line)
    except FileNotFoundError:
        print("\nThere is no such file called %s!" % txt)
        exit(-1)


def update_atomic_mass():
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
        print("\nThere is no such file called howerton_atomic_masses")
        exit(-1)

    try:
        with open("atomic_masses_list.txt", "w") as out_file:
            for i in range(118):
                out_file.write("{}: {}\n".format((i + 1), atomic_mass_list[i]))
    except FileNotFoundError:
        print("\nThere is no such file called atomic_masses_list")
        exit(-1)


def create_atomic_mass_list():
    atomic_masses = []
    try:
        with open("atomic_masses_list.txt") as in_file:
            for line in in_file:
                line_elements = line.split(" ")
                atomic_masses.append(float(line_elements[1]))
    except FileNotFoundError:
        print("\nThere is no such file called atomic_masses_list")
        exit(-1)

    return atomic_masses


# Creation of conversion tables:

def create_conversion_table_entropy():
    atomic_masses = create_atomic_mass_list()
    out_file_name = "entropy_conversion_table.txt"
    try:
        with open(out_file_name, "w") as out_file:
            out_file.write("Starting Unit\t\t\terg/g/K\t\tMbar-cc/g/K\tJ/g/K\t\tJ/mol/K\n")
            out_file.write("Ending Unit\t\t\tkB/atom\t\tkB/atom\t\tkB/atom\t\tJ/g/K\n")
            out_file.write("Element\t\tAMass\n")
            for i in range(118):
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


def access_factor_from_table(table, element, starting_unit, ending_unit):
    in_file_name = table + ".txt"
    starting_index = []
    ending_index = []
    
    try:
        with open(in_file_name) as in_file:
            for line in in_file:
                line_elements = line.split("\t")
                line_data = list(filter(None, line_elements))

                if line_data[0] == "Starting Unit":
                    for count, unit in enumerate(line_data):
                        if unit == starting_unit:
                            starting_index.append(count)
                if line_data[0] == "Ending Unit":
                    for count, unit in enumerate(line_data):
                        if unit == ending_unit:
                            ending_index.append(count)
                unit_index = common_member(starting_index, ending_index)
                for i in unit_index:
                    index = i

                if line_data[0] == str(element.atomic_number):
                    print("%s, %s -> %s: %s " % (element.name, starting_unit, ending_unit, line_data[index + 1]))
                    return line_data[index + 1]

    except FileNotFoundError:
        print("\nThere is no such file called %s!" % in_file_name)
        exit(-1)


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)

    return a_set & b_set


def get_factor_from_table():
    choice = input("Please state the element, starting unit, and ending unit in this order: \n(Examples: 4 J/g/K "
                   "kB/atom, Carbon erg/g eV/atom, or Zr kB/atom Mbar-cc/g/K) ")
    choice_parameters = choice.split(" ")
    try:
        element = md.element(int(choice_parameters[0]))
    except ValueError:
        element = md.element(choice_parameters[0])

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
    else:
        print("Invalid input for element, starting unit, or ending unit!")
