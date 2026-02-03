def get_most_common_product(product_names):
    
    if not product_names:
        return None
        
    product_counts = {}
    for name in product_names:
        if not name or not isinstance(name, str):
            continue
            
        # Normalisation : minuscule et suppression des espaces inutiles
        name_lower = name.strip().lower()
        
        if not name_lower: # Si vide après strip
            continue
            
        product_counts[name_lower] = product_counts.get(name_lower, 0) + 1
        
    if not product_counts:
        return None
        
    most_common = max(product_counts, key=product_counts.get)
    return most_common.title()
