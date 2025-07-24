# --- Example of how to use both classes ---

# 1. Use case: Correcting specific names from a predefined list.
print("--- Using VocabularyCorrector ---")
nombres_propios = ["Javier", "Beatriz", "Alejandro", "Verónica"]
name_corrector = VocabularyCorrector(custom_vocabulary=nombres_propios)

palabras_a_corregir_nombres = ["Javierr", "Beatris", "Alexandro"]
for palabra in palabras_a_corregir_nombres:
    corregida = name_corrector.correct_word(palabra)
    print(f"Original: '{palabra}', Corregido: '{corregida}'")

print("\n" + "="*40 + "\n")

# 2. Use case: General spell checking for common Spanish words.
print("--- Using GeneralSpellChecker ---")
general_checker = GeneralSpellChecker(language='es')

# You can add words that are correct but might not be in the default dictionary
general_checker.add_custom_words(["pyspellchecker", "SymSpell"])

palabras_a_corregir_general = ["cosina", "vienbenido", "pyspellchecker", "diccionrio"]
for palabra in palabras_a_corregir_general:
    corregida = general_checker.correct_word(palabra)
    print(f"Original: '{palabra}', Corregido: '{corregida}'")

# --- Expected Output ---
# --- Using VocabularyCorrector ---
# Original: 'Javierr', Corregido: 'Javier'
# Original: 'Beatris', Corregido: 'Beatriz'
# Original: 'Alexandro', Corregido: 'Alejandro'
#
# ========================================
#
# --- Using GeneralSpellChecker ---
# Original: 'cosina', Corregido: 'cocina'
# Original: 'vienbenido', Corregido: 'bienvenido'
# Original: 'pyspellchecker', Corregido: 'pyspellchecker'
# Original: 'diccionrio', Corregido: 'diccionario'