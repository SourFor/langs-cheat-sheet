from passlib.hash import bcrypt

def compare_bcrypt_hashes(hash1: bytes, hash2: bytes) -> bool:
    """
    Сравнивает два хеша bcrypt и возвращает True, если они равны, False - если различны
    
    :param hash1: Первый хеш bcrypt (в байтах)
    :param hash2: Второй хеш bcrypt (в байтах)
    :return: Результат сравнения
    """
    try:
        # Проверяем, что оба хеша валидны
        bcrypt.hashpw(b"", hash1)
        bcrypt.hashpw(b"", hash2)
    except ValueError:
        return False
        
    # Сравниваем хеши
    return bcrypt.hashpw(hash1, hash2) == hash2

def main():
    # Пример использования
    
    # Вводим два хеша от пользователя
    hash1 = input("Введите первый хеш bcrypt: ").encode()
    hash2 = input("Введите второй хеш bcrypt: ").encode()
    
    # Сравниваем хеши
    if compare_bcrypt_hashes(hash1, hash2):
        print("Хеш-суммы совпадают!")
    else:
        print("Хеш-суммы различаются!")

if __name__ == "__main__":
    main()
