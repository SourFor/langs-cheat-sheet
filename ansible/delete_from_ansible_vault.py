#!/usr/bin/env python3
import os
import argparse
import yaml
from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.constants import DEFAULT_VAULT_IDENTITY

def read_vault_password(password_file):
    """Читает пароль из файла"""
    with open(password_file, 'r') as f:
        return f.read().strip()

def read_substrings_from_file(file_path):
    """Читает подстроки для удаления из файла"""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def decrypt_vault_file(file_path, vault_password):
    """Расшифровывает файл ansible-vault"""
    try:
        vault_secret = VaultSecret(vault_password.encode())
        vault = VaultLib([(DEFAULT_VAULT_IDENTITY, vault_secret)])
        
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = vault.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        raise Exception(f"Failed to decrypt {file_path}: {str(e)}")

def encrypt_vault_file(file_path, content, vault_password):
    """Шифрует файл ansible-vault"""
    try:
        vault_secret = VaultSecret(vault_password.encode())
        vault = VaultLib([(DEFAULT_VAULT_IDENTITY, vault_secret)])
        
        encrypted_data = vault.encrypt(content.encode('utf-8'))
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
    except Exception as e:
        raise Exception(f"Failed to encrypt {file_path}: {str(e)}")

def process_file(file_path, vault_password, substrings, check_mode=False):
    """Обрабатывает файл: расшифровывает, удаляет строки, шифрует обратно"""
    try:
        decrypted_content = decrypt_vault_file(file_path, vault_password)
        lines = decrypted_content.split('\n')
        
        modified_lines = []
        affected = False
        
        for line in lines:
            if not any(sub in line for sub in substrings):
                modified_lines.append(line)
            else:
                affected = True
        
        if not affected:
            return False
        
        if check_mode:
            print(file_path)
            return True
        
        modified_content = '\n'.join(modified_lines)
        encrypt_vault_file(file_path, modified_content, vault_password)
        return True
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Remove lines containing substrings from ansible-vault encrypted files'
    )
    
    parser.add_argument('--dir', required=True, help='Directory with vault files')
    parser.add_argument('--vault-pass', required=True, help='Path to vault password file')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--remove', help='Substring to remove')
    group.add_argument('-f', '--file', help='File with substrings to remove')
    
    parser.add_argument('--check', action='store_true', 
                      help='Check mode (no changes, just print affected files)')
    
    args = parser.parse_args()
    
    try:
        # Получаем пароль
        vault_password = read_vault_password(args.vault_pass)
        
        # Получаем подстроки для удаления
        if args.file:
            substrings = read_substrings_from_file(args.file)
        else:
            substrings = [args.remove]
        
        # Обрабатываем файлы в директории
        affected_files = 0
        for filename in os.listdir(args.dir):
            if filename.endswith('.yml') or filename.startswith('critical_'):
                file_path = os.path.join(args.dir, filename)
                if process_file(file_path, vault_password, substrings, args.check):
                    affected_files += 1
        
        if not args.check:
            print(f"Processed {affected_files} files", file=sys.stderr)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    import sys
    main()