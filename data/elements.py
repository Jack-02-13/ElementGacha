from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Element:
    atomic_number: int
    symbol: str
    name_zh: str
    name_en: str
    rarity_level: int


ELEMENTS: list[Element] = [
    Element(1, "H", "氫", "Hydrogen", 2),
    Element(2, "He", "氦", "Helium", 5),
    Element(3, "Li", "鋰", "Lithium", 3),
    Element(4, "Be", "鈹", "Beryllium", 4),
    Element(5, "B", "硼", "Boron", 3),
    Element(6, "C", "碳", "Carbon", 3),
    Element(7, "N", "氮", "Nitrogen", 3),
    Element(8, "O", "氧", "Oxygen", 1),
    Element(9, "F", "氟", "Fluorine", 3),
    Element(10, "Ne", "氖", "Neon", 5),
    Element(11, "Na", "鈉", "Sodium", 1),
    Element(12, "Mg", "鎂", "Magnesium", 1),
    Element(13, "Al", "鋁", "Aluminum", 1),
    Element(14, "Si", "矽", "Silicon", 1),
    Element(15, "P", "磷", "Phosphorus", 2),
    Element(16, "S", "硫", "Sulfur", 3),
    Element(17, "Cl", "氯", "Chlorine", 3),
    Element(18, "Ar", "氬", "Argon", 5),
    Element(19, "K", "鉀", "Potassium", 1),
    Element(20, "Ca", "鈣", "Calcium", 1),
    Element(21, "Sc", "鈧", "Scandium", 3),
    Element(22, "Ti", "鈦", "Titanium", 2),
    Element(23, "V", "釩", "Vanadium", 3),
    Element(24, "Cr", "鉻", "Chromium", 3),
    Element(25, "Mn", "錳", "Manganese", 3),
    Element(26, "Fe", "鐵", "Iron", 1),
    Element(27, "Co", "鈷", "Cobalt", 3),
    Element(28, "Ni", "鎳", "Nickel", 3),
    Element(29, "Cu", "銅", "Copper", 3),
    Element(30, "Zn", "鋅", "Zinc", 3),
    Element(31, "Ga", "鎵", "Gallium", 3),
    Element(32, "Ge", "鍺", "Germanium", 4),
    Element(33, "As", "砷", "Arsenic", 4),
    Element(34, "Se", "硒", "Selenium", 5),
    Element(35, "Br", "溴", "Bromine", 4),
    Element(36, "Kr", "氪", "Krypton", 5),
    Element(37, "Rb", "銣", "Rubidium", 3),
    Element(38, "Sr", "鍶", "Strontium", 3),
    Element(39, "Y", "釔", "Yttrium", 3),
    Element(40, "Zr", "鋯", "Zirconium", 3),
    Element(41, "Nb", "鈮", "Niobium", 3),
    Element(42, "Mo", "鉬", "Molybdenum", 4),
    Element(43, "Tc", "鎝", "Technetium", 5),
    Element(44, "Ru", "釕", "Ruthenium", 5),
    Element(45, "Rh", "銠", "Rhodium", 5),
    Element(46, "Pd", "鈀", "Palladium", 5),
    Element(47, "Ag", "銀", "Silver", 5),
    Element(48, "Cd", "鎘", "Cadmium", 4),
    Element(49, "In", "銦", "Indium", 5),
    Element(50, "Sn", "錫", "Tin", 4),
    Element(51, "Sb", "銻", "Antimony", 4),
    Element(52, "Te", "碲", "Tellurium", 5),
    Element(53, "I", "碘", "Iodine", 4),
    Element(54, "Xe", "氙", "Xenon", 5),
    Element(55, "Cs", "銫", "Cesium", 4),
    Element(56, "Ba", "鋇", "Barium", 3),
    Element(57, "La", "鑭", "Lanthanum", 3),
    Element(58, "Ce", "鈰", "Cerium", 3),
    Element(59, "Pr", "鐠", "Praseodymium", 4),
    Element(60, "Nd", "釹", "Neodymium", 3),
    Element(61, "Pm", "鉕", "Promethium", 5),
    Element(62, "Sm", "釤", "Samarium", 4),
    Element(63, "Eu", "銪", "Europium", 4),
    Element(64, "Gd", "釓", "Gadolinium", 4),
    Element(65, "Tb", "鋱", "Terbium", 4),
    Element(66, "Dy", "鏑", "Dysprosium", 4),
    Element(67, "Ho", "鈥", "Holmium", 4),
    Element(68, "Er", "鉺", "Erbium", 4),
    Element(69, "Tm", "銩", "Thulium", 4),
    Element(70, "Yb", "鐿", "Ytterbium", 4),
    Element(71, "Lu", "鎦", "Lutetium", 4),
    Element(72, "Hf", "鉿", "Hafnium", 4),
    Element(73, "Ta", "鉭", "Tantalum", 4),
    Element(74, "W", "鎢", "Tungsten", 4),
    Element(75, "Re", "錸", "Rhenium", 5),
    Element(76, "Os", "鋨", "Osmium", 5),
    Element(77, "Ir", "銥", "Iridium", 5),
    Element(78, "Pt", "鉑", "Platinum", 5),
    Element(79, "Au", "金", "Gold", 5),
    Element(80, "Hg", "汞", "Mercury", 5),
    Element(81, "Tl", "鉈", "Thallium", 4),
    Element(82, "Pb", "鉛", "Lead", 3),
    Element(83, "Bi", "鉍", "Bismuth", 4),
    Element(84, "Po", "釙", "Polonium", 5),
    Element(85, "At", "砹", "Astatine", 5),
    Element(86, "Rn", "氡", "Radon", 5),
    Element(87, "Fr", "鍅", "Francium", 5),
    Element(88, "Ra", "鐳", "Radium", 5),
    Element(89, "Ac", "錒", "Actinium", 5),
    Element(90, "Th", "釷", "Thorium", 4),
    Element(91, "Pa", "鏷", "Protactinium", 5),
    Element(92, "U", "鈾", "Uranium", 4),
    Element(93, "Np", "鎿", "Neptunium", 5),
    Element(94, "Pu", "鈽", "Plutonium", 5),
    Element(95, "Am", "鋂", "Americium", 5),
    Element(96, "Cm", "鋦", "Curium", 5),
    Element(97, "Bk", "錇", "Berkelium", 5),
    Element(98, "Cf", "鉲", "Californium", 5),
    Element(99, "Es", "鑀", "Einsteinium", 5),
    Element(100, "Fm", "鐨", "Fermium", 5),
    Element(101, "Md", "鍆", "Mendelevium", 5),
    Element(102, "No", "鍩", "Nobelium", 5),
    Element(103, "Lr", "鐒", "Lawrencium", 5),
    Element(104, "Rf", "鑪", "Rutherfordium", 5),
    Element(105, "Db", "杜", "Dubnium", 5),
    Element(106, "Sg", "西", "Seaborgium", 5),
    Element(107, "Bh", "玻", "Bohrium", 5),
    Element(108, "Hs", "哈", "Hassium", 5),
    Element(109, "Mt", "邁", "Meitnerium", 5),
    Element(110, "Ds", "達", "Darmstadtium", 5),
    Element(111, "Rg", "倫", "Roentgenium", 5),
    Element(112, "Cn", "哥", "Copernicium", 5),
    Element(113, "Nh", "鉨", "Nihonium", 5),
    Element(114, "Fl", "鈇", "Flerovium", 5),
    Element(115, "Mc", "莫", "Moscovium", 5),
    Element(116, "Lv", "利", "Livermorium", 5),
    Element(117, "Ts", "田", "Tennessine", 5),
    Element(118, "Og", "奧", "Oganesson", 5),
]


def _validate_elements() -> None:
    if len(ELEMENTS) != 118:
        raise ValueError(f"Expected 118 elements, got {len(ELEMENTS)}")
    atomic_numbers = {element.atomic_number for element in ELEMENTS}
    if atomic_numbers != set(range(1, 119)):
        raise ValueError("Atomic numbers must be exactly 1..118")
    for element in ELEMENTS:
        if not 1 <= element.rarity_level <= 5:
            raise ValueError(f"Invalid rarity for {element.symbol}: {element.rarity_level}")


_validate_elements()

ELEMENT_BY_ATOMIC_NUMBER: dict[int, Element] = {
    element.atomic_number: element for element in ELEMENTS
}

