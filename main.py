from processor import Processor
from grabber import Grabber
import threading


grabber = Grabber(width=300, height=300, top=100, left=100)
processor = Processor()


if __name__ == "__main__":
    while True:
        image = grabber.capture_image(debug=True)
        t1 = threading.Thread(target=processor.find_text, args=(image,))
        t1.start()
