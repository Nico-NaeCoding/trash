import yaml
from pathlib import Path
from ultralytics import YOLO
import shutil

# ============================================
# 0. 기본 설정
# ============================================
class_list = ["can", "pet", "paper", "plastic", "glass", "vinyl"]
base_path = Path(r"D:\data")

# ============================================
# 1. 데이터 존재 확인
# ============================================
def check_data():
    """이미지/라벨 폴더 존재 여부 확인"""
    paths = [
        base_path / "images" / "train",
        base_path / "images" / "val",
        base_path / "labels" / "train",
        base_path / "labels" / "val",
    ]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        print("[에러] 다음 폴더가 없습니다:\n - " + "\n - ".join(missing))
        return False
    
    train_labels = list((base_path / "labels" / "train").glob("*.txt"))
    val_labels = list((base_path / "labels" / "val").glob("*.txt"))
    print(f"[확인] 데이터 폴더 OK: {base_path}")
    print(f"[확인] 학습 라벨: {len(train_labels)}개, 검증 라벨: {len(val_labels)}개")
    return True

# ============================================
# 2. YAML 설정 파일 생성
# ============================================
def create_yaml_config():
    """YOLOv8용 데이터셋 설정 파일 생성"""
    yaml_config = {
        "path": str(base_path),
        "train": "images/train",
        "val": "images/val",
        "names": class_list,
        "nc": len(class_list),
    }
    yaml_file_path = base_path / "data.yaml"
    with open(yaml_file_path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_config, f, allow_unicode=True, sort_keys=False)
    print(f"[생성] YAML 파일: {yaml_file_path.resolve()}")
    print(f"[정보] 클래스 개수: {len(class_list)}개")
    return yaml_file_path

# ============================================
# 3. 학습 함수
# ============================================
def train_best_model(config_path):
    """YOLOv8 모델 학습 실행"""
    print("\n[학습 시작] 6개 클래스 쓰레기 분류 모델 훈련")
    
    model = YOLO("yolov8n.pt")
    
    results = model.train(
        data=str(config_path),
        epochs=80,
        imgsz=640,
        batch=16,
        patience=30,
        device="cuda",
        workers=4,
        project="runs/detect",
        name="6class_waste_model",
    )
    
    # 결과 저장
    run_dir = Path(results.save_dir)
    best = run_dir / "weights" / "best.pt"
    
    if best.exists():
        backup_dir = Path("D:/models")  # ✅ D 드라이브로 수정!
        backup_dir.mkdir(exist_ok=True, parents=True)
        dst = backup_dir / "best_6class_model.pt"
        shutil.copy2(best, dst)
        print(f"\n[완료] 최적 가중치 저장: {dst}")
        print(f"[정보] 학습 결과 폴더: {run_dir}")
    else:
        print("\n[경고] best.pt가 생성되지 않았습니다.")
    
    return model, results, best

# ============================================
# 4. 메인 실행
# ============================================
if __name__ == "__main__":
    print("="*60)
    print("YOLOv8 6개 클래스 쓰레기 분류 모델 학습")
    print("="*60)
    
    if check_data():
        cfg = create_yaml_config()
        model, results, best = train_best_model(cfg)
        print("\n" + "="*60)
        print(f"[완료] 학습 종료")
        print(f"최적 모델: {best}")
        print("="*60)
    else:
        print("\n[실패] 데이터 폴더 구조를 확인해주세요.")