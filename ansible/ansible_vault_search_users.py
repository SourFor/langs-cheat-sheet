import os
import argparse
import yaml
import csv
import sys
from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.constants import DEFAULT_VAULT_IDENTITY

def read_vault_password(password_file):
    """Читает пароль из файла"""
    with open(password_file, 'r') as f:
        return f.read().strip()

def decrypt_vault_file(file_path, vault_password):
    """Расшифровывает файл ansible-vault"""
    try:
        vault_secret = VaultSecret(vault_password.encode())
        vault = VaultLib([(DEFAULT_VAULT_IDENTITY, vault_secret)])
        
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = vault.decrypt(encrypted_data)
        return yaml.safe_load(decrypted_data)
    except Exception as e:
        raise Exception(f"Failed to decrypt {file_path}: {str(e)}")

def process_critical_files(directory, vault_password):
    """Обрабатывает все critical_ файлы в директории"""
    users_dict = {}
    
    for filename in os.listdir(directory):
        if filename.startswith('critical_'):
            file_path = os.path.join(directory, filename)
            try:
                data = decrypt_vault_file(file_path, vault_password)
                if data and 'postgresql_users' in data:
                    for user in data['postgresql_users']:
                        name = user['name']
                        if name not in users_dict:
                            users_dict[name] = []
                        users_dict[name].append(filename)
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}", file=sys.stderr)
    
    return users_dict

def save_to_file(data, filename, csv_format=False):
    """Сохраняет данные в файл"""
    if csv_format:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Key', 'Value'])
            for key, value in data.items():
                writer.writerow([key, ', '.join(value)])
    else:
        with open(filename, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)

def load_from_file(filename):
    """Загружает данные из файла"""
    with open(filename, 'r') as f:
        if filename.endswith('.csv'):
            reader = csv.reader(f)
            next(reader)  # Пропускаем заголовок
            return {row[0]: row[1].split(', ') for row in reader}
        else:
            return yaml.safe_load(f)

def display_data(data, keys=None, list_keys=False, csv_format=False):
    """Отображает данные согласно параметрам"""
    if csv_format:
        writer = csv.writer(sys.stdout)
        if list_keys:
            writer.writerow(['Available Keys'])
            for key in data.keys():
                writer.writerow([key])
        elif keys:
            requested_keys = [k.strip() for k in keys.split(',')]
            writer.writerow(['Key', 'Value'])
            for key in requested_keys:
                if key in data:
                    writer.writerow([key, ', '.join(data[key])])
                else:
                    writer.writerow([key, 'NOT FOUND'])
        else:
            writer.writerow(['Key', 'Value'])
            for key, value in data.items():
                writer.writerow([key, ', '.join(value)])
    else:
        if list_keys:
            print("Доступные ключи:")
            for key in data.keys():
                print(f"- {key}")
            return
        
        if keys:
            requested_keys = [k.strip() for k in keys.split(',')]
            for key in requested_keys:
                if key in data:
                    print(f"{key}: {data[key]}")
                else:
                    print(f"Ключ '{key}' не найден")
        else:
            print("Все данные:")
            for key, value in data.items():
                print(f"{key}: {value}")

def main():
    parser = argparse.ArgumentParser(description='Process ansible-vault encrypted files')
    
    # Группа параметров для обработки vault файлов
    vault_group = parser.add_argument_group('Vault processing')
    vault_group.add_argument('--dir', help='Path to group_vars directory')
    vault_group.add_argument('--vault-pass', help='Path to file with vault password')
    
    # Группа параметров для работы с сохраненным файлом
    file_group = parser.add_argument_group('File operations')
    file_group.add_argument('--file', '-f', help='Path to file with saved data (YAML or CSV)')
    file_group.add_argument('--output', '-o', help='Save results to file')
    
    # Параметры вывода
    output_group = parser.add_argument_group('Output control')
    output_group.add_argument('--ls', action='store_true', help='List all available keys')
    output_group.add_argument('--keys', help='Comma-separated list of keys to display')
    output_group.add_argument('--csv', action='store_true', help='Output in CSV format')
    
    args = parser.parse_args()
    
    try:
        # Определяем источник данных
        if args.file:
            data = load_from_file(args.file)
        elif args.dir and args.vault_pass:
            vault_password = read_vault_password(args.vault_pass)
            data = process_critical_files(args.dir, vault_password)
            
            if args.output:
                save_to_file(data, args.output, args.csv)
                print(f"Результат сохранен в {args.output}", file=sys.stderr)
        else:
            parser.error("Необходимо указать либо --file, либо --dir и --vault-pass")
            return
        
        # Обрабатываем параметры вывода
        display_data(data, args.keys, args.ls, args.csv)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()