import qrcode
import argparse

# Функция для создания QR-кода из файла
def create_qr_from_file(input_file, output_file):
    # Чтение содержимого из входного файла
    with open(input_file, 'r') as file:
        file_content = file.read()

    # Создание QR-кода
    qr = qrcode.QRCode(
        version=1,  # Размер QR-кода: 1 — маленький, 40 — максимальный
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Уровень коррекции ошибок
        box_size=10,  # Размер каждого "пикселя" в QR-коде
        border=4,  # Размер границы (4 — дефолтное значение)
    )

    # Добавление данных в QR-код
    qr.add_data(file_content)
    qr.make(fit=True)

    # Генерация изображения с QR-кодом
    img = qr.make_image(fill='black', back_color='white')

    # Сохранение изображения в выходной файл
    img.save(output_file)
    print(f"QR-код сохранен в файл: {output_file}")

# Разбор аргументов командной строки
def main():
    parser = argparse.ArgumentParser(description="Создание QR-кода из файла.")
    
    # Аргументы для входного и выходного файлов
    parser.add_argument("input_file", help="Путь к входному файлу с данными для QR-кода")
    parser.add_argument("output_file", help="Путь к выходному файлу для сохранения QR-кода (например, qrcode.png)")
    
    # Получаем аргументы
    args = parser.parse_args()
    
    # Вызываем функцию создания QR-кода
    create_qr_from_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
