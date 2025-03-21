# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

# Paramètres de la grille
GRID_WIDTH = 25  # Largeur de la grille
GRID_HEIGHT = 15  # Hauteur de la grille

# Calcul des limites des zones (division par 3 de l'espace)
ZONE_WIDTH = GRID_WIDTH // 3  # Largeur de chaque zone
ZONE_GREEN = (0, ZONE_WIDTH - 1)  # Zone verte : colonnes 0 à 2 (si GRID_WIDTH = 9)
ZONE_YELLOW = (ZONE_WIDTH, 2 * ZONE_WIDTH - 1)  # Zone jaune : colonnes 3 à 5
ZONE_RED = (2 * ZONE_WIDTH, GRID_WIDTH - 1)  # Zone rouge : colonnes 6 à 8