import shutil
import os

# لیست فایل‌های مرتبط
files_to_move = [
    'move_chapter1_content.py',
    'move_chapter1_content_v2.py',
    'move_chapter1_content_final.py',
    'move_chapter1_simple.py',
    'move_chapter1_working.py',
    'refine_chapter1.py',
    'refine_chapter1_complete.py',
    'check_chapter1.py',
    'verify_transfers.py',
    'verify_final.py',
    'fix_chapter1_final.py',
    'final_fix_chapter1.py',
    'chapter1_text.txt'
]

target_folder = 'chapter1_refinement'

# ایجاد پوشه اگر وجود ندارد
os.makedirs(target_folder, exist_ok=True)

# انتقال فایل‌ها
moved_count = 0
for filename in files_to_move:
    source_path = filename
    target_path = os.path.join(target_folder, filename)
    
    if os.path.exists(source_path):
        try:
            shutil.move(source_path, target_path)
            print(f"✓ Moved: {filename}")
            moved_count += 1
        except Exception as e:
            print(f"✗ Error moving {filename}: {e}")
    else:
        print(f"- Not found: {filename}")

print(f"\n✓ Successfully moved {moved_count} files to {target_folder}/")
