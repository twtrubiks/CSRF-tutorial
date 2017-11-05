import string

# https://github.com/django/django/blob/master/django/middleware/csrf.py#L56

CSRF_SECRET_LENGTH = 32
CSRF_ALLOWED_CHARS = string.ascii_letters + string.digits

token = '< csrftoken of cookie or csrfmiddlewaretoken of form>'
salt = token[:CSRF_SECRET_LENGTH]
token = token[CSRF_SECRET_LENGTH:]
chars = CSRF_ALLOWED_CHARS
pairs = zip((chars.index(x) for x in token), (chars.index(x) for x in salt))
secret = ''.join(chars[x - y] for x, y in pairs)  # Note negative values are ok
print(secret)
