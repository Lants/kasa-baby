

hangman_0 = """```
   --------
   |      |
   |      0
   |     /|\\
   |      |
   |     / \\
___|_________

```"""

hangman_1 = """```
   --------
   |      |
   |      0
   |     /|\\
   |      |
   |     / 
___|_________

```"""

hangman_2 = """```
   --------
   |      |
   |      0
   |     /|\\
   |      |
   |     
___|_________

```"""

hangman_3 = """```
   --------
   |      |
   |      0
   |     /|\\
   |      
   |     
___|_________

```"""

hangman_4 = """```
   --------
   |      |
   |      0
   |     /|
   |      
   |    
___|_________

```"""

hangman_5 = """```
   --------
   |      |
   |      0
   |      |
   |      
   |     
___|_________

```"""

hangman_6 = """```
   --------
   |      |
   |      0
   |     
   |      
   |     
___|_________

```"""

hangman_7 = """```
   --------
   |      |
   |      
   |    
   |      
   |     
___|_________

```"""

def artChooser(n):
    if n == 0:
        return hangman_0
    elif n == 1:
        return hangman_1
    elif n == 2:
        return hangman_2
    elif n == 3:
        return hangman_3
    elif n == 4:
        return hangman_4
    elif n == 5:
        return hangman_5
    elif n == 6:
        return hangman_6
    elif n == 7:
        return hangman_7
    else:
        return "artChooser error, n is not 0-7"
