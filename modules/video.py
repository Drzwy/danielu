import asyncio
import cv2
import base64


camera = cv2.VideoCapture(0)


async def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            continue
        else:
            # ret, buffer = cv2.imencode(".jpg", frame)
            # frame_data = base64.b64encode(buffer).decode("utf-8")
            # yield frame_data
            yield frame


async def main():
    async for frame in generate_frames():
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
