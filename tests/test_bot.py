from labelbot import bot
SECRET = "d653a60adc0a16a93e99f0620a67f4a67ef901df"
BODY = "Hello, World!"
SIGN = "sha1=8727505c9c036b2337a06d2e63f091a7aa41ae60"

def test_correct_hash():
    result = bot.authenticate_request(SECRET,BODY, SIGN)
    assert result

def test_incorrect_hash():
    result = bot.authenticate_request(SECRET,BODY.lower(), SIGN)
    assert not result

def test_no_signature():
    result = bot.authenticate_request(SECRET,BODY, None)
    assert not result
