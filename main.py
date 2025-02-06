from damgard_jurik import keygen

# Generate a key pair
public_key, private_key = keygen(s=1024)

# Print the public key
print(public_key)
print(private_key)