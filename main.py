import hashlib

text = b"hello"  # b"..." is bytes literal

print("md5:    ", hashlib.md5(text).hexdigest())      # 32 chars
print("sha1:   ", hashlib.sha1(text).hexdigest())     # 40 chars
print("sha256: ", hashlib.sha256(text).hexdigest())   # 64 chars
print("sha512: ", hashlib.sha512(text).hexdigest())   # 128 chars