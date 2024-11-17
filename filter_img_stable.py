import os
import shutil
import threading
from PIL import Image
import imagehash
from tqdm import tqdm

# Khởi tạo các thư mục gốc và đích
root_folder = "AIC/Keyframes"
target_folder = "AIC/si_img"

# Tạo thư mục đích nếu chưa tồn tại
os.makedirs(target_folder, exist_ok=True)

# Threshold để so sánh độ tương đồng của hash
HASH_THRESHOLD = 5

# Khóa để đồng bộ hóa truy cập vào processed_hashes
lock = threading.Lock()

# Hàm tính hash của hình ảnh
def calculate_hash(image_path):
    try:
        with Image.open(image_path) as img:
            return imagehash.phash(img)
    except Exception as e:
        print(f"Error calculating hash for {image_path}: {e}")
        return None

# Hàm xử lý một folder, tính hash và sao chép ảnh tương tự
def process_folder(folder_path, target_folder, progress_bar):
    processed_hashes = {}

    for root, _, files in os.walk(folder_path):
        # Sắp xếp danh sách file để đảm bảo thứ tự
        files = sorted(files)

        for file in files:
            file_path = os.path.join(root, file)

            # Bỏ qua nếu không phải file ảnh
            if not file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                progress_bar.update(1)
                continue

            # Tính hash của file ảnh
            img_hash = calculate_hash(file_path)
            if img_hash is None:
                progress_bar.update(1)
                continue

            is_similar = False

            # Sử dụng khóa khi truy cập tài nguyên chia sẻ
            with lock:
                for existing_hash in processed_hashes.values():
                    if abs(img_hash - existing_hash) <= HASH_THRESHOLD:
                        is_similar = True
                        break

            if is_similar:
                base_name, ext = os.path.splitext(file)
                target_path = os.path.join(target_folder, file)

                # Đổi tên nếu file đã tồn tại
                counter = 1
                while os.path.exists(target_path):
                    target_path = os.path.join(
                        target_folder, f"{base_name}_{counter}{ext}"
                    )
                    counter += 1

                shutil.copy(file_path, target_path)

            # Thêm hash mới vào danh sách
            with lock:
                processed_hashes[file_path] = img_hash
            progress_bar.update(1)

# Hàm quản lý đa luồng
def process_folders_multithreaded(root_folder, target_folder):
    # Lấy danh sách các folder con trong thư mục gốc
    subfolders = sorted([os.path.join(root_folder, d) for d in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, d))])

    # Tổng số file để theo dõi progress bar
    total_files = sum(
        len(files)
        for subfolder in subfolders
        for _, _, files in os.walk(subfolder)
    )

    # Khởi tạo progress bar
    with tqdm(total=total_files, desc="Processing images") as progress_bar:
        threads = []
        for subfolder in subfolders:
            thread = threading.Thread(target=process_folder, args=(subfolder, target_folder, progress_bar))
            threads.append(thread)
            thread.start()

        # Chờ tất cả các luồng hoàn thành
        for thread in threads:
            thread.join()

# Hàm xóa thư mục đích trước khi sao chép
def clear_target_folder(target_folder):
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)
    os.makedirs(target_folder, exist_ok=True)

# Chạy chương trình
if __name__ == "__main__":
    # Xóa thư mục đích trước khi bắt đầu
    clear_target_folder(target_folder)

    # Bắt đầu xử lý
    process_folders_multithreaded(root_folder, target_folder)
    print("Processing completed!")
