from mss import mss
import numpy
import cv2


class Grabber:
    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
        top: int | None = None,
        left: int | None = None,
    ) -> None:
        self.tela = mss().grab(mss().monitors[1]).size
        if width and height and top is not None and left is not None:
            self.width = width
            self.height = height
            self.top = top
            self.left = left
        else:
            self.width = self.tela.width
            self.height = self.tela.height
            self.top = 0
            self.left = 0
        self.dimensions = (
            self.left,
            self.top,
            self.width + self.left,
            self.height + self.top,
        )

    def capture_image(self, debug=False):
        with mss() as sct:
            frame = cv2.cvtColor(
                numpy.array(sct.grab(self.dimensions)), cv2.COLOR_BGRA2RGB
            )
        if debug:
            cv2.imshow("window", frame)
            if cv2.waitKey(25) % 0xFF == ord("q"):
                cv2.destroyAllWindows()
        return frame
