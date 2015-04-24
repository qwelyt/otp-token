# otp-token
Generate OTP-tokens, like Google Authenticator


## .otpkeys
Put your key in .otpkeys
You can put as many spaces as you want to, it doesn't matter. For example, this

	myKey= J VQW  O2 LDKB X X IYLUN    5JW65L Q


will work. You can ofcourse choose not to have any spaces, which works just as well.

## otp
This is a basic shell script that will look for the .otpkeys file in $HOME/.otpkeys
If you wish to keep your keys somewhere else, just change line 3

	keyfile="path/to/keyfile"

and it will look for them there instead.

To run the script first do

	chmod +x otp

you can then run it with

    ./otp test

The argument `test` is the keyword for which key to use. To use the above key with all the spaces, the line would look like

	./otp myKey 

Another note: you could write

	./otp my

And get the same result. We could not write `Key` however, the matching is only done at the beginning of the word. Similarily, you can't write `yKe`.

## token.py
This is where the magic happens.
There are two methods: `get_totp_token(key)` and `get_hotp_token(key, interval)`.
`get_totp_token(key)` works just like Google Authenticator. Every 30 seconds, a new key will be generated.
`get_hotp_token(key, interval)` does all the heavylifting. It decodes the key (like what you put in `.otpkeys`) to get the real and actual key (the one used in this readme translate to `MagicPotatoSoup` btw).
Then it goes on to create a "message", really it just translates the interval to the correct format.
It goes on to greate a message digest of the decoded key and the formated interval. The digest is translated to its ASCII value and ANDs that to 15 (magic number).
The result is then used with the magic `(struct.unpack(">I", messageDigest[ASCIIvalue:ASCIIvalue+4])[0] & 0x7fffffff) % 1000000`, which, tbh, I found while researching the Authenticator. The result of that is then returned, and that is the code you are using!

So, like I said. This is where the magic happens!

### totp
totp == [Time-basde One-time Password Algorithm](http://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm)
Set an interval, and generate a password.

### hotp
hotp == [HMAC-based One-time Password Algorithm](http://en.wikipedia.org/wiki/HMAC-based_One-time_Password_Algorithm)

### OTP
This blog explains it neatly: http://blogs.forgerock.org/petermajor/2014/02/one-time-passwords-hotp-and-totp/


## Use it like you wish
The reason for bulding this as simple: I don't have a smartphone. I don't plan on getting one. But I need the autehnticator stuff for VPNs and whatnots.

There are several softwares to do this thing, like authy or winauth. However, I don't know what (and if) more they do than give me the number. This solution is open. You can see that there is no hidden code that gathers info or something.

Another nice feature: It works on Linux and Windows+Cygwin! And I'm pretty sure it works on OSX as well, but that's untested.

For whatever reason you have, use it as you wish.

## ToDo
* Encrypt .otpkeys so they're not in plaintext. Use `source .otpkeys` to get the keys perhaps?
* Look into putting it all in one language instead of bash+python.
