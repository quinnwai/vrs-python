"""Python support used across GA4GH projects

"""

from importlib.metadata import version, PackageNotFoundError

from .digests import sha512t24u
from .enderef import ga4gh_enref, ga4gh_deref
from .identifiers import (
    ga4gh_digest, ga4gh_identify, ga4gh_serialize, is_ga4gh_identifier,
    parse_ga4gh_identifier, VrsObjectIdentifierIs, use_ga4gh_compute_identifier_when,
    CURIE_NAMESPACE, CURIE_SEP, GA4GH_PREFIX_SEP, GA4GH_IR_REGEXP, GA4GH_DIGEST_REGEXP
)
from .pydantic import (
    is_pydantic_instance, is_curie_type, is_ga4gh_identifiable, is_literal, pydantic_copy
)
from . import entity_models, domain_models

__all__ = [
    "sha512t24u",
    "ga4gh_enref",
    "ga4gh_deref",
    "ga4gh_digest",
    "ga4gh_identify",
    "ga4gh_serialize",
    "is_ga4gh_identifier",
    "parse_ga4gh_identifier",
    "VrsObjectIdentifierIs",
    "use_ga4gh_compute_identifier_when",
    "CURIE_NAMESPACE",
    "CURIE_SEP",
    "GA4GH_PREFIX_SEP",
    "GA4GH_IR_REGEXP",
    "GA4GH_DIGEST_REGEXP",
    "is_pydantic_instance",
    "is_curie_type",
    "is_ga4gh_identifiable",
    "is_literal",
    "pydantic_copy",
    "entity_models",
    "domain_models"
]

try:
    __version__ = version(__name__)
except PackageNotFoundError:    # pragma: nocover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
