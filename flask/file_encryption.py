# 1
# Sets a default curve (secp256k1)
import time

import copy
import datetime
import random
import pickle
import ipfsapi
from umbral.signing import Signer
from umbral import pre, keys, config
from flask import Flask
from flask import request
from flask import jsonify
import flask_cors
import hashlib
import json

api = ipfsapi.connect('127.0.0.1', 5001)
config.set_default_curve()

app = Flask(__name__)
flask_cors.CORS(app)


class User:
    def __init__(self):
        # Generate keys for Alice
        self.priv_key = keys.UmbralPrivateKey.gen_key()
        self.pub_key = self.priv_key.get_pubkey()

        self.signing_priv_key = self.priv_key
        self.signer = Signer(self.signing_priv_key)
        self.signing_pub_key = self.signing_priv_key.get_pubkey()

        self.box_private = hashlib.sha256(('private' + str(time.time())).encode('utf-8')).hexdigest()
        self.box_public = hashlib.sha256(('public' + str(time.time())).encode('utf-8')).hexdigest()
        self.capsules = {"strange_hash": (None, None)}

    def encrypt_file(self, data_file):  # returns alice_ciphertext, umbral_capsule
        # Encrypt some data for Alice
        alice_ciphertext, umbral_capsule = pre.encrypt(self.pub_key, data_file)
        return alice_ciphertext, umbral_capsule

    def decrypt_file(self, alice_ciphertext, umbral_capsule, output_path):
        # Decrypt data for Alice
        with open(output_path, 'wb') as decoded_file:
            alice_decrypted_data = pre.decrypt(alice_ciphertext, umbral_capsule, self.priv_key, self.pub_key)
            decoded_file.write(alice_decrypted_data)

    def grant_access(self, accessor, umbral_capsule):
        bob_capsule = umbral_capsule
        kfrags = pre.split_rekey(self.priv_key, self.signer, accessor.pub_key, 10, 20)
        rand_min_shares = random.sample(kfrags, 10)
        bob_capsule.set_correctness_keys(delegating=self.pub_key,
                                         receiving=accessor.pub_key,
                                         verifying=self.signing_pub_key)
        for kfrag in rand_min_shares:
            cfrag = pre.reencrypt(kfrag, umbral_capsule)  # <- Ursula does that
            bob_capsule.attach_cfrag(cfrag)  # <- Bob does that

        return bob_capsule, self.pub_key

    def decrypt(self, cipher_file, bob_capsule, alice_pub_key):
        bob_plaintext = pre.decrypt(cipher_file, bob_capsule, self.priv_key, alice_pub_key)
        return bob_plaintext


# Global functions
Alices = []
# Alices[0].box_private = 'password'
# Alices[0].box_public = 'alice'
# Alices[1].box_private = 'password'
# Alices[1].box_public = 'bob'


def find_user(public, private=None):
    cool_Alice = None
    for Alice in Alices:
        if Alice.box_public == public:
            if private is not None:
                if Alice.box_private == private:
                    cool_Alice = Alice
            else:
                cool_Alice = Alice

    if cool_Alice is None:
        cool_Alice = User()
        cool_Alice.box_private = private
        cool_Alice.box_public = public
        Alices.append(cool_Alice)

    return cool_Alice

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')


@app.route('/upload', methods=['POST'])
@flask_cors.cross_origin()
def upload_file():
    # post_data_files = [b'123', b'345']
    # box_private = Alices[0].box_private
    # box_public = Alices[0].box_public
    data = request.get_json()
    box_public = data["alicePub"]
    box_private = data["alicePriv"]
    # Bob_box_public = Alices[1].box_public
    Bob_box_public = data["bobPub"]
    cool_Alice = find_user(box_public, box_private)
    Bob = find_user(Bob_box_public)


    hashes = []
    for file in data["files"]:
        alice_ciphertext, umb1 = cool_Alice.encrypt_file(file["bytes"].encode("utf-8"))
        alice_ciphertext, umb2 = cool_Alice.encrypt_file(file["bytes"].encode("utf-8"))
        res = api.add_bytes(alice_ciphertext)
        # umb1 = copy.copy(umbral_capsule)
        # umb2 = copy.copy(umbral_capsule)
        bob_capsule, alice_pub_key = cool_Alice.grant_access(Bob, umb1)
        Bob.capsules[res] = (bob_capsule, alice_pub_key)
        bob_capsule, alice_pub_key = cool_Alice.grant_access(cool_Alice, umb2)
        cool_Alice.capsules[res] = (bob_capsule, alice_pub_key)

        hashes.append(res)

    # answer = {'hashes': hashes}
    # print(answer)
    # return answer
    #
    # data = request.get_json()
    # hashes = []
    # for f in data["files"]:
    #     hashes.append(api.add_bytes(f["bytes"].encode("utf-8")))

    metadata = {
        "linkName": data["linkName"],
        "datetime": data["datetime"],
        "files": [{"name": data["files"][i]["name"], "hash": hashes[i]} for i in range(len(hashes))]
    }

    dir_to_encode = json.dumps(metadata).encode("utf-8")
    alice_ciphertext, umb1 = cool_Alice.encrypt_file(dir_to_encode)
    alice_ciphertext, umb2 = cool_Alice.encrypt_file(dir_to_encode)
    res = api.add_bytes(alice_ciphertext)
    # umb1 = copy.deepcopy(umbral_capsule)
    # umb2 = copy.deepcopy(umbral_capsule)
    bob_capsule, alice_pub_key = cool_Alice.grant_access(Bob, umb1)
    Bob.capsules[res] = (bob_capsule, alice_pub_key)
    bob_capsule, alice_pub_key = cool_Alice.grant_access(cool_Alice, umb2)
    cool_Alice.capsules[res] = (bob_capsule, alice_pub_key)

    # file = Bob.decrypt(alice_ciphertext, bob_capsule, alice_pub_key)

    return res


@app.route('/download', methods=['POST'])
@flask_cors.cross_origin()
def download_file():
    data = request.get_json()
    hashes = data["hashes"]
    # box_private = Alices[1].box_private
    # box_public = Alices[1].box_public
    box_public = data["pubKey"]
    box_private = data["privKey"]
    # Alice_box_public = Alices[0].box_public
    Bob = find_user(box_public, box_private)
    # alice_pub_key = find_user(Alice_box_public).pub_key
    return_data = {}
    for hash_i in hashes:
        bob_capsule, alice_pub_key = Bob.capsules[hash_i]
        cipher_file = api.cat(hash_i)
        file = Bob.decrypt(cipher_file, bob_capsule, alice_pub_key)
        return_data[hash_i] = file.decode("utf-8")

    # answer = {'files': post_data_files}
    # print(answer)
    #
    # data = request.get_json()
    # hashes = data["hashes"]
    # return_data = {}
    # for h in hashes:
    #     return_data[h] = api.cat(h).decode("utf-8")
    return jsonify(return_data)


# Alice.decrypt_file(alice_ciphertext, umbral_capsule, "decoded_file.jpg")

# Bob = Accessor()
# bob_capsule, alice_pub_key = Alice.grant_access(Bob, umbral_capsule)
# Bob.decrypt("decoded_by_Bob.jpg", alice_ciphertext, bob_capsule, alice_pub_key)
#
# bob_capsule_dump = pickle.dumps(bob_capsule)
# hashes = upload_file()['hashes']
# download_file(hashes)

app.run()
