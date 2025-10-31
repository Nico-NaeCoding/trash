# infer_easy.py
import os, glob, json, cv2
from ultralytics import YOLO

# (필요시 수정)
WEIGHTS = r"E:\runs\trash\weight\best.pt"
SAVE_DIR = r".\result"
CONF = 0.25
IOU = 0.7
DEVICE = "0"  # GPU: "0", CPU: "cpu"

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def is_image(p): return os.path.splitext(p.lower())[1] in IMG_EXTS

def pick_path():
    # Tk 없이도 동작하도록 환경에 따라 대체
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        root = tk.Tk(); root.withdraw()

        path = filedialog.askopenfilename(
            title="이미지 파일 선택 (취소하면 폴더선택)",
            filetypes=[("Images","*.jpg *.jpeg *.png *.bmp *.webp")]
        )
        if not path:
            path = filedialog.askdirectory(title="이미지 폴더 선택")
            if not path:
                messagebox.showinfo("알림", "선택이 취소되었습니다.")
                return None
        return path
    except Exception:
        # 콘솔 대체 입력
        print("이미지 파일 경로(또는 폴더 경로)를 입력하세요:")
        return input("> ").strip().strip('"')

def collect_inputs(path):
    if os.path.isdir(path):
        imgs = []
        for ext in IMG_EXTS:
            imgs += glob.glob(os.path.join(path, f"**/*{ext}"), recursive=True)
        return sorted(imgs)
    return [path] if is_image(path) else []

def save_json(res, dets, save_dir, img_path):
    h0, w0 = res.orig_shape[:2]
    records = []
    for name, cid, conf, (x1,y1,x2,y2) in dets:
        w, h = x2-x1, y2-y1
        cx, cy = x1 + w/2, y1 + h/2
        records.append({
            "class": name,
            "class_id": cid,
            "conf": round(conf, 4),
            "bbox_xyxy": [int(x1), int(y1), int(x2), int(y2)],
            "bbox_xywh_norm": [cx/w0, cy/h0, w/w0, h/h0]
        })
    base = os.path.splitext(os.path.basename(img_path))[0]
    json_path = os.path.join(save_dir, base + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"image": img_path, "width": w0, "height": h0, "detections": records}, f, ensure_ascii=False, indent=2)
    print(f"-> Saved boxes JSON: {json_path}")

def infer_one(model, img_path):
    results = model.predict(source=img_path, conf=CONF, iou=IOU, device=DEVICE, verbose=False)
    res = results[0]
    names = res.names
    boxes = res.boxes

    print(f"\n[Image] {img_path}")
    dets = []
    if boxes is None or len(boxes) == 0:
        print("- No objects detected.")
    else:
        for b in boxes:
            cid = int(b.cls)
            name = names.get(cid, str(cid))
            score = float(b.conf)
            x1, y1, x2, y2 = map(int, b.xyxy[0].cpu().numpy().tolist())
            dets.append((name, cid, score, (x1, y1, x2, y2)))
        for name, cid, score, (x1, y1, x2, y2) in sorted(dets, key=lambda x: x[2], reverse=True):
            print(f"- {name} (id={cid}) conf={score:.3f} box=[{x1},{y1},{x2},{y2}]")

    # 시각화 저장
    os.makedirs(SAVE_DIR, exist_ok=True)
    out_img = os.path.join(SAVE_DIR, os.path.basename(img_path))
    annotated = res.plot()  # BGR ndarray
    cv2.imwrite(out_img, annotated)
    print(f"-> Saved annotated image: {out_img}")

    # JSON 저장
    save_json(res, dets, SAVE_DIR, img_path)

def main():
    path = pick_path()
    if not path:
        return
    model = YOLO(WEIGHTS)
    print(f"Loaded model: {WEIGHTS}")
    print("Classes:", model.model.names)

    inputs = collect_inputs(path)
    if not inputs:
        print("이미지를 찾지 못했습니다.")
        return
    for p in inputs:
        infer_one(model, p)

if __name__ == "__main__":
    main()
