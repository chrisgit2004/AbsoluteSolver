import base64
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

# ==========================================
# APPROACH SELECTION
# ==========================================
# Set this to True to test raw hex bytes. 
# Set this to False to test pure plaintext strings.
USE_RAW_HEX_BYTES = False

if USE_RAW_HEX_BYTES:
    # Option A: Raw Hex String (Will be converted to cryptographic bytes)
    piece_1 = "4A434A454E534F4E"
    piece_2 = "534F4C564552"
    piece_3 = "636F707065722D39"
    piece_4 = "736F6C766572"
    piece_5 = "54455353415F434F4D50524F4D49534544"
    piece_6 = "32303236"
    
    hex_string = piece_1 + piece_2 + piece_3 + piece_4 + piece_5 + piece_6
    password = bytes.fromhex(hex_string)
    print(f"Current Mode: RAW HEX BYTES")
    print(f"Testing Hex Sequence: '{hex_string}'")
else:
    # Option B: Plaintext Strings
    piece_1 = "JCJenson"
    piece_2 = "NULLBYTE"
    piece_3 = "copper-9"
    piece_4 = "hunger"
    piece_5 = "TESSA_COMPROMISED"
    piece_6 = "2026"
    
    password = piece_1 + piece_2 + piece_3 + piece_4 + piece_5 + piece_6
    print(f"Current Mode: PLAINTEXT STRINGS")
    print(f"Testing Password String: '{password}'")

# ==========================================
# CRYPTOGRAPHIC PARAMETERS (FROM IMAGES)
# ==========================================
problems = {
    "Problem I": {
        "salt": "zjwPziNdCw/KeJllLzPmRljqfQxNWl8z",
        "iv": "U106CuxdAEp6AWTA",
        "ciphertext": "Ln+uvIwB+w+sVtlwLrwm6w==",
        "tag": "3Xyql/cHrxBVx0nCFrl7qA=="
    },
    "Problem II": {
        "salt": "6gV965IdM2b7zzmDy2gXcpp1DgawIXBq",
        "iv": "p7bkD7c2zDnQivbU",
        "ciphertext": "nSvFpXe1F6U7IwVJlEDR6A==",
        "tag": "0bHBGmjimZH2hm/OEjVnsQ=="
    },
    "Problem III": {
        "salt": "QkpTT/H3zL3SyLJUVlp07Pt70TJn8teS",
        "iv": "L1niTTFIU/gANvN3",
        "ciphertext": "MsDJIehDfbw8s2SQlARMKQ==",
        "tag": "ypc32PBsQyV06i59052+NQ=="
    }
}

iterations = 2100000

print("Crunching keys across all problems... (This will take a moment)")
print("-" * 60)

# Loop through each problem to find the real one
for name, data in problems.items():
    try:
        # Decode base64 components
        salt = base64.b64decode(data["salt"])
        iv = base64.b64decode(data["iv"])
        ciphertext = base64.b64decode(data["ciphertext"])
        auth_tag = base64.b64decode(data["tag"])
        
        # Derive the key using PBKDF2-HMAC-SHA256
        key = PBKDF2(password, salt, dkLen=32, count=iterations, hmac_hash_module=SHA256)
        
        # Attempt AES-256-GCM decryption
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        decrypted_bytes = cipher.decrypt_and_verify(ciphertext, auth_tag)
        
        print(f"\n[+++] SUCCESS AT {name}! [+++]")
        print("Decrypted Content:")
        print(decrypted_bytes.decode('utf-8'))
        print("-" * 60)
        
    except ValueError:
        # GCM authentication tag validation fails if the password is wrong
        print(f"[x] {name}: Verification failed.")
    except Exception as e:
        print(f"[!] {name}: Error occurred: {e}")

print("\nProcessing complete.")
