from passlib.hash import bcrypt

def generate_bcrypt_hashes(password, salt) -> str:

    try:
        pass_hash = bcrypt.using(ident='2y', salt=salt).hash(password)
    except ValueError:
        return False
        
    return pass_hash

def main():

    password = input("Введите пароль: ")
    salt = input("Введите соль(22 знака. При отсутствии генерируется): ")
    print(generate_bcrypt_hashes(password, salt))
    
if __name__ == "__main__":
    main()
