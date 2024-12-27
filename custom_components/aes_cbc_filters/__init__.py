from base64 import b64encode, b64decode
from binascii import unhexlify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from homeassistant.helpers import template

_LOGGER = logging.getLogger(__name__)
_TemplateEnvironment = template.TemplateEnvironment

## -- encrypt
def encrypt(msg, key=, iv):
	iv = unhexlify(iv)
	key = unhexlify(key)
	msg = pad(msg.encode(), AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	cipher_text = cipher.encrypt(msg)
	out = b64encode(cipher_text).decode('utf-8')
	return out

## -- decrypt
def decrypt(msg, key=, iv=):
	decipher = AES.new(key, AES.MODE_CBC, iv)
	return unpad(decipher.decrypt(b64decode(out)), AES.block_size).decode('utf-8')

def init(*args):
    """Initialize filters"""
    env = _TemplateEnvironment(*args)
    env.filters["encrypt"] = encrypt
    env.globals["encrypt"] = encrypt
    env.filters["decrypt"] = decrypt
    env.globals["decrypt"] = decrypt
    return env

template.TemplateEnvironment = init
template._NO_HASS_ENV.filters["encrypt"] = encrypt
template._NO_HASS_ENV.globals["encrypt"] = encrypt
template._NO_HASS_ENV.filters["decrypt"] = decrypt
template._NO_HASS_ENV.globals["decrypt"] = decrypt

async def async_setup(hass, hass_config):
    tpl = template.Template("", template._NO_HASS_ENV.hass)
    tpl._env.globals = encrypt
    tpl._env.globals = decrypt
    return True
