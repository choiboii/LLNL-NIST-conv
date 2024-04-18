# This is a script designed to convert thermodynamic data of elements taken from nist.gov into different units.
import scipy.constants as spc

import scripts
import os


def main():
    choice = input("Type PT for entire periodic table, SE for just a single element, AM for Atomic Mass Testing, or "
                   "OTHER for different testing purposes: ")
    choice.upper()

    # Convert the entire periodic table:
    if choice == "PT":
        os.chdir(os.getcwd() + '\\Tables\\')
        scripts.convert_periodic_table()

    # Convert just a single element with a corresponding state of matter:
    elif choice == "SE":
        os.chdir(os.getcwd() + '\\Tables\\')
        element = input("What element would you like to convert the units of? (Use the symbol for input) ")
        state_of_matter = input("Solid or Liquid state of matter? (S for solid, L for liquid) ")
        scripts.convert_single_element(element, state_of_matter)

    elif choice == "AM":
        scripts.update_atomic_mass()
        scripts.create_conversion_table_entropy()
        scripts.create_conversion_table_entropy_reverse()
        scripts.create_conversion_table_energy()
        scripts.create_conversion_table_energy_reverse()
        # scripts.get_factor_from_table()

    elif choice == "Other":
        print(spc.erg)

    else:
        print("Invalid Output!")
        exit(-1)


if __name__ == '__main__':
    main()
