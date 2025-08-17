import os


def compare_category_folders(images_path, label_path):
    try:
        image_categories = {name for name in os.listdir(images_path)
                            if os.path.isdir(os.path.join(images_path, name))}
    except FileNotFoundError:
        print(f"❌ images 폴더를 찾을 수 없습니다: {images_path}")
        return

    try:
        label_categories = {name for name in os.listdir(label_path)
                            if os.path.isdir(os.path.join(label_path, name))}
    except FileNotFoundError:
        print(f"❌ label 폴더를 찾을 수 없습니다: {label_path}")
        return

    print(f"📊 카테고리 폴더 확인")
    print(f"   Images 카테고리: {sorted(image_categories)}")
    print(f"   Label 카테고리: {sorted(label_categories)}")
    print("=" * 80)

    # 카테고리 폴더 일치 확인
    common_categories = image_categories & label_categories
    only_in_images = image_categories - label_categories
    only_in_labels = label_categories - image_categories

    if only_in_images:
        print(f"⚠️ Images에만 있는 카테고리: {sorted(only_in_images)}")
    if only_in_labels:
        print(f"⚠️ Label에만 있는 카테고리: {sorted(only_in_labels)}")

    if not (only_in_images or only_in_labels):
        print("✅ 모든 카테고리 폴더가 일치합니다!")

    print("=" * 80)

    # 각 카테고리별로 이미지명 폴더 비교
    total_issues = 0
    category_results = {}

    for category in sorted(common_categories):
        print(f"📁 {category} 카테고리 분석중...")

        image_category_path = os.path.join(images_path, category)
        label_category_path = os.path.join(label_path, category)

        try:
            image_folders = {name for name in os.listdir(image_category_path)
                             if os.path.isdir(os.path.join(image_category_path, name))}
        except:
            image_folders = set()

        try:
            label_folders = {name for name in os.listdir(label_category_path)
                             if os.path.isdir(os.path.join(label_category_path, name))}
        except:
            label_folders = set()

        # 폴더 비교
        common_image_folders = image_folders & label_folders
        only_in_image = image_folders - label_folders
        only_in_label = label_folders - image_folders

        category_results[category] = {
            'image_count': len(image_folders),
            'label_count': len(label_folders),
            'common_count': len(common_image_folders),
            'only_image': only_in_image,
            'only_label': only_in_label
        }

        # 결과 출력
        print(f"   Images: {len(image_folders)}개 | Labels: {len(label_folders)}개 | 공통: {len(common_image_folders)}개")

        if only_in_image:
            print(f"   ⚠️ Images에만 있는 이미지폴더 ({len(only_in_image)}개):")
            for folder in sorted(list(only_in_image)[:10]):  # 최대 10개만 표시
                print(f"      - {folder}")
            if len(only_in_image) > 10:
                print(f"      ... 외 {len(only_in_image) - 10}개")
            total_issues += len(only_in_image)

        if only_in_label:
            print(f"   ⚠️ Label에만 있는 이미지폴더 ({len(only_in_label)}개):")
            for folder in sorted(list(only_in_label)[:10]):  # 최대 10개만 표시
                print(f"      - {folder}")
            if len(only_in_label) > 10:
                print(f"      ... 외 {len(only_in_label) - 10}개")
            total_issues += len(only_in_label)

        if not (only_in_image or only_in_label):
            print("   ✅ 완벽하게 일치!")

        print("-" * 60)

    # 최종 요약
    print("=" * 80)
    print("📋 최종 요약")
    print("=" * 80)

    for category in sorted(common_categories):
        result = category_results[category]
        status = "✅" if (len(result['only_image']) == 0 and len(result['only_label']) == 0) else "⚠️"
        mismatch_count = len(result['only_image']) + len(result['only_label'])

        print(
            f"{status} {category}: Images {result['image_count']}개 | Labels {result['label_count']}개 | 불일치 {mismatch_count}개")

    print("-" * 60)
    print(f"• 총 카테고리: {len(common_categories)}개")
    print(f"• 총 불일치 이미지폴더: {total_issues}개")

    if total_issues == 0 and not (only_in_images or only_in_labels):
        print("\n🎉 완벽! 모든 카테고리와 이미지폴더가 일치합니다!")
    else:
        print(f"\n❗ 문제 발견: 카테고리 불일치 {len(only_in_images) + len(only_in_labels)}개 + 이미지폴더 불일치 {total_issues}개")





# 실제 경로로 실행
if __name__ == "__main__":
    images_path = r"E:\images\train" #이미지폴더 경로로 바꿔주세용
    label_path = r"E:\label\train" #라벨링폴더 경로로 바꿔주세용

    print("🚀 폴더 비교 분석 시작")
    print("=" * 80)

    # 1단계: 카테고리별 이미지폴더 비교
    compare_category_folders(images_path, label_path)
