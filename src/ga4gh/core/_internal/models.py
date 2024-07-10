"""GKS Common Library models

**This module should not be imported directly.**

Instead, users should use one of the following:

  * `from ga4gh.core import common_models`, and refer to models with the
    abbreviated name, e.g., `common_models.Gene` (recommended)

  * `import ga4gh.core`, and refer to models using the fully-qualified
    module name, e.g., `ga4gh.core.common_models.Gene`
"""
from __future__ import annotations
import datetime
from typing import Any, Dict, Literal, Annotated, Optional, Union, List
from enum import Enum

from pydantic import BaseModel, Field, RootModel, StringConstraints, constr, field_validator, model_serializer, model_validator

from ga4gh.core import GA4GH_IR_REGEXP

#########################################
# GKS Common Abstract Entity & Utility Class Definitions
#########################################

class AgentSubtype(str, Enum):
    """Define constraints for agent subtype"""

    PERSON = "person"
    ORGANIZATION = "organization"
    COMPUTER = "computer"

class Relation(str, Enum):
    """A mapping relation between concepts as defined by the Simple Knowledge
    Organization System (SKOS).
    """

    CLOSE_MATCH = 'closeMatch'
    EXACT_MATCH = 'exactMatch'
    BROAD_MATCH = 'broadMatch'
    NARROW_MATCH = 'narrowMatch'
    RELATED_MATCH = 'relatedMatch'


class Syntax(str, Enum):
    """The syntax used to describe the variation. The value should be one of the
    supported syntaxes.
    """

    HGVS_C = "hgvs.c"
    HGVS_P = "hgvs.p"
    HGVS_G = "hgvs.g"
    HGVS_M = "hgvs.m"
    HGVS_N = "hgvs.n"
    HGVS_R = "hgvs.r"
    HGVS_ISCN = "iscn"
    GNOMAD = "gnomad"
    SPDI = "spdi"

#########################################
# GKS Common Abstract Utility Classes
# These do not inherit from Entity and are not typed explicitly
#########################################

class Code(RootModel):
    """Indicates that the value is taken from a set of controlled strings defined
    elsewhere. Technically, a code is restricted to a string which has at least one
    character and no leading or  trailing whitespace, and where there is no whitespace
    other than single spaces in the contents."""

    root: Annotated[str, StringConstraints(pattern=r'\S+( \S+)*')] = Field(
        ...,
        json_schema_extra={
            'description': 'Indicates that the value is taken from a set of controlled strings defined elsewhere. Technically, a code is restricted to a string which has at least one character and no leading or  trailing whitespace, and where there is no whitespace other than single spaces in the contents.',
            'example': 'ENSG00000139618',
        }
    )


class IRI(RootModel):
    """An IRI Reference (either an IRI or a relative-reference), according to `RFC3986
    section 4.1 <https://datatracker.ietf.org/doc/html/rfc3986#section-4.1>` and
    `RFC3987 section 2.1 <https://datatracker.ietf.org/doc/html/rfc3987#section-2.1>`.
    MAY be a JSON Pointer as an IRI fragment, as described by `RFC6901 section 6
    <https://datatracker.ietf.org/doc/html/rfc6901#section-6>`.
    """

    def __hash__(self):
        return self.root.__hash__()

    @model_serializer(when_used='json')
    def ga4gh_serialize(self):
        m = GA4GH_IR_REGEXP.match(self.root)
        if m is not None:
            return m['digest']
        return self.root

    root: str = Field(
        ...,
        json_schema_extra={'description': 'An IRI Reference (either an IRI or a relative-reference), according to `RFC3986 section 4.1  <https://datatracker.ietf.org/doc/html/rfc3986#section-4.1>` and `RFC3987 section 2.1 <https://datatracker.ietf.org/doc/html/rfc3987#section-2.1>`. MAY be a JSON Pointer as an IRI fragment, as  described by `RFC6901 section 6 <https://datatracker.ietf.org/doc/html/rfc6901#section-6>`.',
        }
    )


class RecordMetadata(BaseModel):
    """A reusable structure that encapsulates provenance metadata about a serialized
    data record or object in a particular dataset (as opposed to provenance about the
    real world entity this record or object represents).
    """

    recordIdentifier: Optional[str] = Field(None, description="The identifier of the data record or object described in this RecordMetadata object.")
    recordVersion: Optional[str] = Field(None, description="The version number of the record-level artifact the object describes.")
    derivedFrom: Optional[str] = Field(None, description="Another data record from which the record described here was derived, through a data ingest and/or transformation process. Value should be a string representing the identifier of the source record.")
    dateRecordCreated: Optional[str] = Field(None, description="The date the record was initially created.")
    contributions: Optional[List[Contribution]] = Field(None, description="Describes specific contributions made by an human or software agent to the creation, modification, or administrative management of a data record or object.")


class Coding(BaseModel):
    """A structured representation of a code for a defined concept in a terminology or
    code system.
    """

    label: Optional[str] = Field(
        None,
        description='The human-readable name for the coded concept, as defined by the code system.'
    )
    system: str = Field(
        ...,
        description="The terminology/code system that defined the code. May be reported as a free-text name (e.g. 'Sequence Ontology'), but it is preferable to provide a uri/url for the system. When the 'code' is reported as a CURIE, the 'system' should be reported as the uri that the CURIE's prefix expands to (e.g. 'http://purl.obofoundry.org/so.owl/' for the Sequence Ontology)."
    )
    version: Optional[str] = Field(
        None,
        description='Version of the terminology or code system that provided the code.'
    )
    code: Code = Field(
        ...,
        description="A symbol uniquely identifying the concept, as in a syntax defined by the code system. CURIE format is preferred where possible (e.g. 'SO:0000704' is the CURIE form of the Sequence Ontology code for 'gene')."
    )


class ConceptMapping(BaseModel):
    """A mapping to a concept in a terminology or code system."""

    coding: Coding = Field(..., description="A structured representation of a code for a defined concept in a terminology or code system.")
    relation: Relation = Field(..., description="A mapping relation between concepts as defined by the Simple Knowledge Organization System (SKOS).")


class Extension(BaseModel):
    """The Extension class provides entities with a means to include additional
    attributes that are outside of the specified standard but needed by a given content
    provider or system implementer. These extensions are not expected to be natively
    understood, but may be used for pre-negotiated exchange of message attributes
    between systems.
    """

    name: str = Field(..., description='A name for the Extension. Should be indicative of its meaning and/or the type of information it value represents.')
    value: Optional[Union[float, str, bool, Dict[str, Any], List[Any]]] = Field(
        None, description='The value of the Extension - can be any primitive or structured object'
    )
    description: Optional[str] = Field(None, description="A description of the meaning or utility of the Extension, to explain the type of information it is meant to hold.")


class Expression(BaseModel):
    """Representation of a variation by a specified nomenclature or syntax for a
    Variation object. Common examples of expressions for the description of molecular
    variation include the HGVS and ISCN nomenclatures.
    """

    syntax: Syntax = Field(..., description="The syntax used to describe the variation. The value should be one of the supported syntaxes.")
    value: str = Field(..., description="The expression of the variation in the specified syntax. The value should be a valid expression in the specified syntax.")
    syntax_version: Optional[str] = Field(None, description="The version of the syntax used to describe the variation. This is particularly important for HGVS expressions, as the syntax has evolved over time.")


#########################################
# GKS Common Abstract Entity Class Definitions
#########################################


class CommonEntityType(str, Enum):
    """Define GKS Common Entity types"""

    AGENT = "Agent"
    CONTRIBUTION = "Contribution"
    DOCUMENT = "Document"
    METHOD = "Method"


class _Entity(BaseModel):
    """Entity is the root class of the 'gks-common' core information model classes -
    those that have identifiers and other general metadata like labels, xrefs, urls,
    descriptions, etc. All common classes descend from and inherit its attributes.
    """

    id: Optional[str] = Field(
        None,
        description="The 'logical' identifier of the entity in the system of record, e.g. a UUID. This 'id' is unique within a given system. The identified entity may have a different 'id' in a different system, or may refer to an 'id' for the shared concept in another system (e.g. a CURIE)."
    )
    type: str
    label: Optional[str] = Field(
        None,
        description='A primary label for the entity.'
    )
    description: Optional[str] = Field(
        None,
        description='A free-text description of the entity.'
    )
    alternativeLabels: Optional[List[str]] = Field(None, description="Alternative name(s) for the Entity.")
    extensions: Optional[List[Extension]] = Field(None, description="A list of extensions to the entity. Extensions are not expected to be natively understood, but may be used for pre-negotiated exchange of message attributes between systems.")


class _DomainEntity(_Entity):
    """An Entity that is specific to a particular biomedical domain such as disease,
    therapeutics, or genes. Domain Entities are considered as 'concept-level' entities,
    as opposed to particular instances. e.g. 'Lung Cancer', not 'patient123's lung
    cancer'. Or 'Erlotinib', not the particular doses given to a patient on a specific
    occasion.
    """

    mappings: Optional[List[ConceptMapping]] = Field(None, description="A list of mappings to concepts in terminologies or code systems. Each mapping should include a coding and a relation.")


class Agent(_Entity):
    """An autonomous actor (person, organization, or computational agent) that bears
    some form of responsibility for an activity taking place, for the existence of an
    entity, or for another agent's activity.
    """

    type: Literal[CommonEntityType.AGENT] = Field(CommonEntityType.AGENT, description=f"MUST be '{CommonEntityType.AGENT.value}'.")
    name: Optional[str] = Field(None, description="The descriptive name of the agent.")
    subtype: Optional[AgentSubtype] = Field(None, description="A more specific type of agent the agent represents.")


class Activity(_Entity):
    """An action or set of actions performed by an agent, that occurs over a period of
    time. Activities may use, generate, modify, move, or destroy one or more entities.
    """

    subtype: Optional[Coding] = Field(None, description="A more specific type of activity that an Activity object may represent.")
    date: Optional[str] = Field(None, description="The date that the Activity was completed. The date SHOULD be formatted as a date string in ISO format 'YYYY-MM-DD'.")
    performedBy: Optional[List[Agent]] = Field(None, description="An Agent who contributed to executing the Activity.")
    specifiedBy: Optional[List[Method]] = Field(None, description="A method that was followed in performing an Activity, that describes how it was executed.")

    @field_validator("date")
    @classmethod
    def date_format(cls, v: Optional[str]) -> Optional[str]:
        """Check that date is YYYY-MM-DD format"""
        if v:
            valid_format = "%Y-%m-%d"

            try:
                datetime.datetime.strptime(v, valid_format).replace(
                    tzinfo=datetime.timezone.utc
                ).strftime(valid_format)
            except ValueError as e:
                msg = "`date` must use YYYY-MM-DD format"
                raise ValueError(msg) from e
        return v


class Contribution(Activity):
    """An action taken by an agent in contributing to the creation, modification,
    assessment, or deprecation of a particular entity (e.g. a Statement, EvidenceLine,
    DataItem, Publication, etc.)
    """

    type: Literal[CommonEntityType.CONTRIBUTION] = CommonEntityType.CONTRIBUTION
    contributor: Optional[Agent] = Field(None, description="The agent that made the contribution.")
    contributionMadeTo: Optional[_InformationEntity] = Field(None, description="The artifact toward which the contribution was made.")  # noqa: N815
    activityType: Optional[Coding] = Field(None, description="SHOULD describe a concept descending from the Contributor Role Ontology.")

    @model_validator(mode="before")
    def handle_extends_prop(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Handle extends properties by renaming fields

        :param values: Input values to process
        :return: Processed values with extended properties renamed
        """
        if "performedBy" in values:
            values["contributor"] = values.pop("performedBy")
        return values


class _InformationEntity(_Entity):
    """Information Entities are abstract (non-physical) entities that are about
    something (i.e. they carry information about things in the real world).
    """

    id: str
    specifiedBy: Optional[Union[Method, IRI]] = Field(None, description="A `Method` that describes all or part of the process through which the information was generated.")
    contributions: Optional[List[Contribution]] = Field(None, description="A list of `Contribution` objects that describe the activities performed by agents upon this entity.")
    isReportedIn: Optional[List[Union[Document, IRI]]] = Field(None, description="A document in which the information content is expressed.")
    dateAuthored: Optional[str] = Field(None, description="Indicates when the information content expressed in the Information Entity was generated.")
    derivedFrom: Optional[List[_InformationEntity]] = Field(None, description="Another Information Entity from which this Information Entity is derived, in whole or in part.")
    recordMetadata: Optional[RecordMetadata] = Field(None, description="Metadata that applies to a specific concrete record of information as encoded in a particular system.")

class Document(_InformationEntity):
    """a representation of a physical or digital document"""

    type: Literal[CommonEntityType.DOCUMENT] = CommonEntityType.DOCUMENT
    subtype: Optional[Coding] = Field(
        None, description="A more specific type for the document (e.g. a publication, patent, pathology report)"
    )
    title: Optional[str] = Field(None, description="The title of the Document")
    url: Optional[constr(pattern="^(https?|s?ftp)://")] = Field(
        None, description="A URL at which the document may be retrieved."
    )
    doi: Optional[constr(pattern="^10.(\\d+)(\\.\\d+)*\\/[\\w\\-\\.]+")] = Field(
        None,
        description="A `Digital Object Identifier <https://www.doi.org/the-identifier/what-is-a-doi/>_` for the document.",
    )
    pmid: Optional[int] = Field(
        None,
        description="A `PubMed unique identifier <https://en.wikipedia.org/wiki/PubMed#PubMed_identifier>`_.",
    )


class Method(_InformationEntity):
    """A set of instructions that specify how to achieve some objective (e.g.
    experimental protocols, curation guidelines, rule sets, etc.)
    """

    type: Literal[CommonEntityType.METHOD] = Field(CommonEntityType.METHOD, description=f"MUST be '{CommonEntityType.METHOD.value}'.")
    isReportedIn: Optional[Union[Document, IRI]]  = None  # noqa: N815
    subtype: Optional[Coding] = Field(
        None,
        description="A more specific type of entity the method represents (e.g. Variant Interpretation Guideline, Experimental Protocol)",
    )
    license: Optional[str] = Field(None, description="A particular license that dictates legal permissions for how a published method (e.g. an experimental protocol, workflow specification, curation guideline) can be used.")


#########################################
# GKS Common Domain Entities
#########################################


class CommonDomainType(str, Enum):
    """Define GKS Common Domain Entity types"""

    PHENOTYPE = "Phenotype"
    DISEASE = "Disease"
    TRAIT_SET = "TraitSet"
    TR_ACTION = "TherapeuticAction"
    TR_AGENT = "TherapeuticAgent"
    TR_SUB = "TherapeuticSubstituteGroup"
    TR_COMB = "CombinationTherapy"
    GENE = "Gene"

class Phenotype(_DomainEntity):
    """An observable characteristic or trait of an organism."""

    type: Literal[CommonDomainType.PHENOTYPE] = Field(
        CommonDomainType.PHENOTYPE,
        description=f'MUST be "{CommonDomainType.PHENOTYPE.value}".'
    )


class Disease(_DomainEntity):
    """A particular abnormal condition that negatively affects the structure or function
    of all or part of an organism and is not immediately due to any external injury.
    """

    type: Literal[CommonDomainType.DISEASE] = Field(
        CommonDomainType.DISEASE,
        description=f'MUST be "{CommonDomainType.DISEASE.value}".'
    )


class TraitSet(_DomainEntity):
    """A set of phenotype and/or disease concepts that together constitute a condition."""

    type: Literal[CommonDomainType.TRAIT_SET] = Field(
        CommonDomainType.TRAIT_SET,
        description=f'MUST be "{CommonDomainType.TRAIT_SET.value}".'
    )
    traits: List[Union[Disease, Phenotype]] = Field(
        ...,
        min_length=2
    )


class Condition(RootModel):
    """A disease or other medical disorder."""

    root: Union[TraitSet, Disease, Phenotype] = Field(
        ...,
        json_schema_extra={'description': 'A disease or other medical disorder.'},
        discriminator='type',
    )


class TherapeuticAction(_DomainEntity):
    """A therapeutic action taken that is intended to alter or stop a pathologic process."""

    type: Literal[CommonDomainType.TR_ACTION] = Field(
        CommonDomainType.TR_ACTION,
        description=f'MUST be "{CommonDomainType.TR_ACTION.value}".'
    )


class TherapeuticAgent(_DomainEntity):
    """An administered therapeutic agent that is intended to alter or stop a pathologic process."""

    type: Literal[CommonDomainType.TR_AGENT] = Field(
        CommonDomainType.TR_AGENT,
        description=f'MUST be "{CommonDomainType.TR_AGENT.value}".'
    )


class TherapeuticSubstituteGroup(_DomainEntity):
    """A group of therapeutic procedures that may be treated as substitutes for one another."""

    type: Literal[CommonDomainType.TR_SUB] = Field(
        CommonDomainType.TR_SUB,
        description=f'MUST be "{CommonDomainType.TR_SUB.value}".'
    )
    substitutes: List[Union[TherapeuticAction, TherapeuticAgent]] = Field(
        ...,
        description='The individual therapeutic procedures that may be treated as substitutes.',
        min_length=2
    )


class CombinationTherapy(_DomainEntity):
    """A therapeutic procedure that involves multiple different therapeutic procedures
    performed in combination.
    """

    type: Literal[CommonDomainType.TR_COMB] = Field(
        CommonDomainType.TR_COMB,
        description=f'MUST be "{CommonDomainType.TR_COMB.value}".'
    )
    components: List[Union[TherapeuticSubstituteGroup, TherapeuticAction, TherapeuticAgent]] = Field(
        ...,
        description='The individual therapeutic procedure components that constitute the combination therapy.',
        min_length=2
    )


class TherapeuticProcedure(RootModel):
    """An action or administration of therapeutic agents to produce an effect  that is
    intended to alter or stop a pathologic process.
    """

    root: Union[CombinationTherapy, TherapeuticSubstituteGroup, TherapeuticAction, TherapeuticAgent] = Field(
        ...,
        json_schema_extra={'description': 'An action or administration of therapeutic agents to produce an effect that is intended to alter or stop a pathologic process.'},
        discriminator='type',
    )


class Gene(_DomainEntity):
    """A basic physical and functional unit of heredity."""

    type: Literal[CommonDomainType.GENE] = Field(
        CommonDomainType.GENE,
        description=f'MUST be "{CommonDomainType.GENE.value}".'
    )
