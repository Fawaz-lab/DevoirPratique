def get_most_common_product(product_names):
    """
    Détermine le produit le plus fréquent dans une liste de noms.
    
    Args:
        product_names (list): Une liste de chaînes de caractères (noms de produits).
        
    Returns:
        str: Le nom du produit le plus fréquent (format Title Case), ou None si la liste est vide.
    """
    if not product_names:
        return None
        
    product_counts = {}
    for name in product_names:
        # Normalisation pour éviter les doublons dus à la casse
        name_lower = name.lower()
        product_counts[name_lower] = product_counts.get(name_lower, 0) + 1
        
    most_common = max(product_counts, key=product_counts.get)
    return most_common.title()
