# Import of the necessary modules

#RSA is an encrytion algorithm that will create public and private keys for chat encryption
from cryptography.hazmat.primitives.asymmetric import rsa 
# serialization is used to store the RSA keys in byte-format
from cryptography.hazmat.primitives import serialization 

# Generating the private key
private_key = rsa.generate_private_key(
    public_exponent = 65537, #One mathematical property of the key generation
    key_size= 2048  # How many bits long the key should be, 2048 is secure, less than that has less security
)

# print(private_key) 

# Generating the public key from the private key
public_key = private_key.public_key()
print(public_key)

# Saving the private key in PEM format:

with open('private_keys.pem', 'wb') as f: 
    # 'With' is a context manager, handles opening and automatic closing of the file. 'wb' = writing binary which is required for cryptography
    f.write(private_key.generate_private(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))


