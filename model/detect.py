from ultralytics import YOLO
import cv2
import json
import time
import os

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

def detect_people(source=0):
    """
    source=0 means use webcam
    source="video.mp4" means use a video file
    """

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("❌ Error: Cannot open camera or video")
        return

    print("✅ Detection started. Press ESC to stop.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ Cannot read frame")
            break

        # Run YOLO detection on this frame
        results = model(frame, verbose=False)

        # Count only people (class 0 in YOLO = person)
        count = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                confidence = float(box.conf[0])

                if cls == 0 and confidence > 0.5:
                    count += 1

                    # Draw a green box around each person
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"Person {confidence:.0%}",
                                (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)

        # Determine crowd status
        if count <= 5:
            status = "Low"
            color = (0, 255, 0)
        elif count <= 15:
            status = "Medium"
            color = (0, 165, 255)
        else:
            status = "High"
            color = (0, 0, 255)

        # ============================================
        # ✅ NEW: Save data to JSON file for website
        # ============================================
        data = {
            "people_count": count,
            "status": status,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "time": time.strftime("%H:%M:%S")
        }

        # Save to a JSON file that your website can read
        json_path = os.path.join(os.path.dirname(__file__), "static", "detection_data.json")
        
        # Create 'static' folder if it doesn't exist
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        with open(json_path, "w") as f:
            json.dump(data, f)

        print(f"👥 People: {count} | Status: {status} | Time: {data['time']}")
        # ============================================

        # Show count and status on the frame
        cv2.putText(frame, f"People: {count}  Status: {status}",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, color, 2)

        resized = cv2.resize(frame, (960, 540))
        cv2.imshow("Smart Campus - Crowd Detection", resized)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Detection stopped.")

if __name__ == "__main__":
    detect_people(source="crowd.mp4")