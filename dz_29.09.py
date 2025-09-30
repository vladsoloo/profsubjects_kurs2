import heapq
import os
from collections import Counter
from typing import Dict, List, Tuple


class HuffmanNode:
    def __init__(self, char: int, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class SimpleArchiver:
    def __init__(self):
        self.codes = {}

    def build_huffman_tree(self, text: bytes) -> HuffmanNode:
        frequency = Counter(text)
        heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        return heap[0]

    def build_codes(self, node: HuffmanNode, current_code: str = ""):
        if node is None:
            return

        if node.char is not None:
            self.codes[node.char] = current_code or "0"
            return

        self.build_codes(node.left, current_code + "0")
        self.build_codes(node.right, current_code + "1")

    def rle_encode(self, data: bytes) -> bytes:
        if not data:
            return b""

        encoded = bytearray()
        i = 0

        while i < len(data):
            count = 1
            while i + count < len(data) and data[i + count] == data[i] and count < 255:
                count += 1

            encoded.append(count)
            encoded.append(data[i])
            i += count

        return bytes(encoded)

    def rle_decode(self, data: bytes) -> bytes:
        if not data:
            return b""

        decoded = bytearray()

        for i in range(0, len(data), 2):
            if i + 1 >= len(data):
                break
            count = data[i]
            byte_val = data[i + 1]
            decoded.extend([byte_val] * count)

        return bytes(decoded)

    def huffman_encode(self, data: bytes) -> Tuple[bytes, Dict[int, str]]:
        if not data:
            return b"", {}

        root = self.build_huffman_tree(data)
        self.codes = {}
        self.build_codes(root)

        encoded_bits = ''.join(self.codes[byte] for byte in data)

        padding = 8 - len(encoded_bits) % 8
        if padding == 8:
            padding = 0
        encoded_bits += '0' * padding

        encoded_bytes = bytearray()
        for i in range(0, len(encoded_bits), 8):
            byte = encoded_bits[i:i+8]
            encoded_bytes.append(int(byte, 2))

        return bytes(encoded_bytes), self.codes, padding

    def huffman_decode(self, encoded_data: bytes, huffman_codes: Dict[int, str], padding: int) -> bytes:
        if not encoded_data:
            return b""

        reverse_codes = {code: char for char, code in huffman_codes.items()}

        bits = ''.join(f'{byte:08b}' for byte in encoded_data)

        if padding > 0:
            bits = bits[:-padding]

        decoded = bytearray()
        current_code = ""

        for bit in bits:
            current_code += bit
            if current_code in reverse_codes:
                decoded.append(reverse_codes[current_code])
                current_code = ""

        return bytes(decoded)

    def serialize_codes(self, codes: Dict[int, str]) -> bytes:
        result = bytearray()
        result.append(len(codes))

        for char, code in codes.items():
            result.append(char)
            result.append(len(code))
            code_bytes = int(code, 2).to_bytes((len(code) + 7) // 8, byteorder='big')
            result.append(len(code_bytes))
            result.extend(code_bytes)

        return bytes(result)

    def deserialize_codes(self, data: bytes) -> Tuple[Dict[int, str], int]:
        if len(data) < 1:
            return {}, 0

        codes = {}
        pos = 0
        num_codes = data[pos]; pos += 1

        for _ in range(num_codes):
            if pos + 3 > len(data):
                break

            char = data[pos]; pos += 1
            code_len = data[pos]; pos += 1
            bytes_len = data[pos]; pos += 1

            if pos + bytes_len > len(data):
                break

            code_bytes = data[pos:pos + bytes_len]
            pos += bytes_len

            code_int = int.from_bytes(code_bytes, byteorder='big')
            code = bin(code_int)[2:].zfill(code_len)
            codes[char] = code

        return codes, pos

    def pack_files(self, file_paths: List[str], output_path: str):
        with open(output_path, 'wb') as out_file:
            out_file.write(b'SARCH')
            out_file.write(len(file_paths).to_bytes(4, byteorder='little'))

            for file_path in file_paths:
                if not os.path.exists(file_path):
                    print(f"Файл {file_path} не существует, пропускаем")
                    continue

                print(f"Обработка файла: {file_path}")

                with open(file_path, 'rb') as in_file:
                    file_data = in_file.read()

                rle_encoded = self.rle_encode(file_data)

                huffman_encoded, codes, padding = self.huffman_encode(rle_encoded)

                file_name = os.path.basename(file_path).encode('utf-8')
                out_file.write(len(file_name).to_bytes(2, byteorder='little'))
                out_file.write(file_name)

                codes_data = self.serialize_codes(codes)
                out_file.write(len(codes_data).to_bytes(4, byteorder='little'))
                out_file.write(codes_data)

                out_file.write(padding.to_bytes(1, byteorder='little'))
                out_file.write(len(huffman_encoded).to_bytes(4, byteorder='little'))
                out_file.write(huffman_encoded)

        print(f"Архив создан: {output_path}")

    def unpack_files(self, archive_path: str, output_dir: str):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(archive_path, 'rb') as in_file:
            signature = in_file.read(5)
            if signature != b'SARCH':
                raise ValueError("Неверный формат архива")

            num_files = int.from_bytes(in_file.read(4), byteorder='little')

            for i in range(num_files):
                name_len = int.from_bytes(in_file.read(2), byteorder='little')
                file_name = in_file.read(name_len).decode('utf-8')
                codes_len = int.from_bytes(in_file.read(4), byteorder='little')
                codes_data = in_file.read(codes_len)
                huffman_codes, _ = self.deserialize_codes(codes_data)

                padding = int.from_bytes(in_file.read(1), byteorder='little')
                data_len = int.from_bytes(in_file.read(4), byteorder='little')
                huffman_encoded = in_file.read(data_len)

                rle_encoded = self.huffman_decode(huffman_encoded, huffman_codes, padding)

                file_data = self.rle_decode(rle_encoded)

                output_path = os.path.join(output_dir, file_name)
                with open(output_path, 'wb') as out_file:
                    out_file.write(file_data)

                print(f"Распакован файл: {output_path}")


def main():
    archiver = SimpleArchiver()

    while True:
        print("\n=== Простой архиватор ===")
        print("1. Создать архив")
        print("2. Распаковать архив")
        print("3. Выйти")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            files_input = input("Введите пути к файлам (через пробел): ").strip()
            file_paths = files_input.split()
            output_path = input("Введите путь для архива: ").strip()

            if not output_path:
                output_path = "archive.sarch"

            try:
                archiver.pack_files(file_paths, output_path)
                print("Архивация завершена успешно!")
            except Exception as e:
                print(f"Ошибка при архивации: {e}")

        elif choice == '2':
            archive_path = input("Введите путь к архиву: ").strip()
            output_dir = input("Введите директорию для распаковки: ").strip()

            if not output_dir:
                output_dir = "extracted"

            try:
                archiver.unpack_files(archive_path, output_dir)
                print("Распаковка завершена успешно!")
            except Exception as e:
                print(f"Ошибка при распаковке: {e}")

        elif choice == '3':
            print("Выход...")
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()
