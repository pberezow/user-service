def read_rsa_key(filename):
    try:
        with open(filename, 'r') as f:
            key = f.read()
            return key
    except:
        Exception('Error while reading rsa key file - ', filename)
