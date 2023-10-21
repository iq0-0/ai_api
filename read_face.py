import face_recognition
import cv2
from typing import List
import aiohttp
import numpy as np
import asyncio 

async def get_attendance(students: List[dict], lecture: str):


    face_encodings = await get_face_encoding(lecture)
    data = {}
    for student in students:
        student_id, student_url = student.popitem()
        student_encoding = await get_face_encoding(student_url)
        match = face_recognition.compare_faces(face_encodings, student_encoding, tolerance=0.6)
        if any(match):
            data[student_id] = True
        else:
            data[student_id] = False

    return data



async def get_face_encoding(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            bf = buffer_image(await resp.read())
            face_encodings = face_recognition.face_encodings(bf)
            return face_encodings[0] if len(face_encodings) == 1 else face_encodings


def buffer_image(content: bytes) -> np.ndarray:

    if not isinstance(content, bytes):
        raise TypeError(f"Expected 'content' to be bytes, received: {type(content)}")
    
    image = cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Expected 'content' to be image bytes")

    return image

if __name__ == "__main__":
    # Testing!
    data = {
        "Lecture":"https://mutabestudentpictures.s3.eu-north-1.amazonaws.com/Students/s441001222?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA4SLBX27DCTZ7LDPS%2F20231021%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20231021T134501Z&X-Amz-Expires=86400&X-Amz-Signature=98d81339bbd4ecd8c3fe607eb1a7ec07c4c9b8e825eb36e20c57182c97e3ec9e&X-Amz-SignedHeaders=host",
        "Students":
            [
                {
                    "s441000001": "https://mutabestudentpictures.s3.eu-north-1.amazonaws.com/Students/s441000001?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA4SLBX27DCTZ7LDPS%2F20231021%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20231021T133217Z&X-Amz-Expires=86400&X-Amz-Signature=13499a590539c6eec22041b35b2516b7efe316940d7a8f36776d89d92913fd44&X-Amz-SignedHeaders=host"
                },
                {
                    "s441000002":"https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F3.bp.blogspot.com%2F-awYYu6tAGtI%2FTuXy8CBjPTI%2FAAAAAAAAc-A%2F-JoR6P2Wc74%2Fs1600%2Fface29.jpg&f=1&nofb=1&ipt=afef2052e2ebdfd7547f4b4a562fac1260eaaa58074a8262f162d1d065322dab&ipo=images"
                }
            ]
    }
    lecture = data["Lecture"]
    students = data["Students"]
    asyncio.run(get_attendance(students=students, lecture=lecture))