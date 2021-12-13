- [] local passwords:

```
- You need to save authorization keys on the disk.
- So you can take the local passcode, derive an encryption key from this passcode and use this key to encrypt the authorization keys before saving. So when you start the app you can't decrypt the keys (and start using the API) without providing a correct local passcode for that. You can also save some hash (like SHA256) of the original keys along so that you can check whether you've decrypted the correct keys or just garbage because of an incorrect passcode.
```

