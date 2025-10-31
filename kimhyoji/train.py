from ultralytics import YOLO
import multiprocessing as mp

def run():
    model = YOLO("yolov8s.pt")  # COCO 사전학습 가중치

    model.train(
        data="data.yaml",
        epochs=50,
        imgsz=640,
        batch=-1,                # 자동 배치
        device=0,                # 단일 GPU
        workers=4,               # Windows면 0~4 사이 권장(에러시 0)
        project=r"E:\runs",
        name="can_bottle_paper_best",
        cache=False,             # RAM 넉넉하면 'ram'도 고려
        amp=True,                # 혼합정밀
        seed=42,
        deterministic=True,      # 재현성↑(약간 느려질 수 있음)
        cos_lr=True,             # cosine LR
        patience=20,             # 조기종료
        save_period=10,          # 10epoch마다 중간 저장
        plots=True,              # 학습 곡선/PR 등 저장
        verbose=True,

        # Augment & regularization (기본값 무난하지만 약간 보강)
        hsv_h=0.015, hsv_s=0.7, hsv_v=0.4,
        degrees=5.0, translate=0.1, scale=0.5, shear=2.0, perspective=0.000,
        flipud=0.0, fliplr=0.5, mosaic=1.0, mixup=0.1,
        close_mosaic=10,         # 마지막 10epoch 모자이크 off → 안정화
        copy_paste=0.0,          # 인물/중첩 많으면 0~0.2로 실험
        weight_decay=0.0005,     # 기본 0.0005 무난
        lr0=0.01, lrf=0.01,      # 기본값(필요시 조절)
    )

if __name__ == "__main__":
    mp.freeze_support()  # Windows 안전장치
    run()

