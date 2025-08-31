from generator import generate_password
import string

def is_password_safe(password: str, min_length: int = 12) -> bool:
    """Check if the password is safe based on length and character variety."""
    
    if len(password) < min_length:
        return False

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    return all([has_lower, has_upper, has_digit, has_special])

if __name__ == "__main__":
    
    pwd = generate_password(16)  
    print(f"Generated password: {pwd}")
    
    if is_password_safe(pwd):
        print("✅ The password is safe.")
    else:
        print("❌ The password is NOT safe.")
