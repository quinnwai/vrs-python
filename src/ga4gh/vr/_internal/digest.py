import base64
import hashlib


def ga4gh_digest(blob, digest_size=24):
    """generate a GA4GH digest for the given binary object

    A GA4GH digest is a convention for constructing and formatting
    digests for use as object identifiers. Specifically::
    
        * generate a SHA512 digest on binary data
        * truncate at 24 bytes
        * encode using base64url encoding

    Examples:
    >>> ga4gh_digest(b'')
    'z4PhNX7vuL3xVChQ1m2AB9Yg5AULVxXc'

    >>> ga4gh_digest(b"ACGT")
    'aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2'

    """

    digest = hashlib.sha512(blob).digest()
    tdigest_b64us = base64.urlsafe_b64encode(digest[:digest_size])
    return tdigest_b64us.decode("ASCII")
