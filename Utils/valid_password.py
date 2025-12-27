import re

def verificar_senha(senha):
    if not senha or not isinstance(senha, str):
        return False, "Senha é obrigatória"
    
    if len(senha) < 10:
        return False, "Senha deve conter pelo menos 10 caracteres"
    
    if not re.search(r'[A-Z]', senha):
        return False, "Senha deve conter pelo menos 1 letra Maiúscula"
    
    if not re.search(r'[a-z]', senha):
        return False, "Senha deve conter pelo menos 1 letra minúscula"
    
    if not re.search(r'\d', senha):
        return False, "Senha deve conter pelos menos 1 número"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False, "Senha deve conter pelo menos 1 caractere especial"
    
    return True, "Senha válida"