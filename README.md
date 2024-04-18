NIST Conversion Scripts for LLNL:

A conversion script in which it can take user input for either single or multiple elements from the periodic table. The script requires minimal user setup; it only requires Scipy and Python, and the script can be run with NIST_conversion.py. The script utilizes a couple of .txt files scrapped from NIST.gov using BeautifulSoup.

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

Example of the program execution:

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

Please state the element, starting unit, and ending unit in this order:
>>> C erg/g eV/atom
Carbon, erg/g -> eV/atom: 1.244867E-11

Would you like to get another conversion factor? (Y/N) 
>>> N

Exiting...
