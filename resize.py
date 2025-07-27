from PIL import Image
import os


input_folder = '상대 경로 넣어주세요. 절대경로 넣으실때는 따옴표 앞에 r붙여야함 '  #데이터셋 폴더/ 절대경로 r'경로'!!!!
output_size = (1920, 1080)  #결과 이미지 해상도 FHD
bg_color = (0, 0, 0)  #패딩 배경색_검정
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp') #이미지 확장자
MAX_FILES = 0  #모든 이미지 처리

#하위 폴더 다 탐색해서 이미지 파일 불러오기
all_files = []
for root, _, files in os.walk(input_folder):
    for f in files:
        if f.lower().endswith(image_extensions):
            full_path = os.path.join(root, f)
            all_files.append(full_path)

#파일 개수 출력
print(f"\n 전체 이미지 수: {len(all_files)}장")

if MAX_FILES > 0:
    all_files = all_files[:MAX_FILES]

#변환 시작
total = len(all_files)
success = 0
fail = 0

for idx, path in enumerate(all_files):
    filename = os.path.basename(path)
    try:
        #1.이미지 열기
        img = Image.open(path).convert("RGB")
        orig_w, orig_h = img.size

        #2.비율 유지하면서 리사이즈
        ratio = min(output_size[0] / orig_w, output_size[1] / orig_h)
        new_size = (int(orig_w * ratio), int(orig_h * ratio))
        resized = img.resize(new_size, Image.LANCZOS)

        #3.패딩 포함 새 배경 생성
        new_img = Image.new("RGB", output_size, bg_color)
        offset = (
            (output_size[0] - new_size[0]) // 2,
            (output_size[1] - new_size[1]) // 2
        )
        new_img.paste(resized, offset)

        #4.덮어쓰기 저장
        new_img.save(path)

        success += 1
        print(f"[{idx+1}/{total}] ✅ {filename} 변환 완료")
    except Exception as e:
        fail += 1
        print(f"[{idx+1}/{total}] ❌ {filename} 실패: {e}")

#변환 완료 확인
print(f"\n 변환 완료: {success}장 성공, {fail}장 실패")
