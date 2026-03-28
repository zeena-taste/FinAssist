import requests

dummy_img = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfd\xfc\xff\xd9'

with open("dummy.jpg", "wb") as f:
    f.write(dummy_img)

url = "http://localhost:8000/vision/upload-receipt"

with open("dummy.jpg", "rb") as f:
    files = {"file": ("dummy.jpg", f, "image/jpeg")}
    try:
        print(f"Uploading dummy image to {url}...")
        res = requests.post(url, files=files)
        res.raise_for_status()
        
        with open("output.csv", "wb") as out_f:
            out_f.write(res.content)
            
        print("Success! CSV downloaded to output.csv:")
        print(res.text)
    except Exception as e:
        print(f"Test failed: {e}\n(Ensure 'uvicorn app.main:app' is actively running locally)")
