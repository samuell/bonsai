"""Datamodels used for prediction results."""
from enum import Enum
from typing import Dict, List

from pydantic import BaseModel

from .base import RWModel


class VariantType(Enum):
    """Types of called variants."""

    SUBSTITUTION = "substitution"


class PredictionSoftware(Enum):
    """Container for software names."""

    # phenotype
    AMRFINDER = "amrfinder"
    RESFINDER = "resfinder"
    VIRFINDER = "virulencefinder"


class Strand(Enum):
    """Nomenclature of forward and reverse strand."""

    FORWARD = "+"
    REVERSE = "-"


class ElementType(Enum):
    """Prediction categories."""

    AMR = "AMR"
    ACID = "STRESS_ACID"
    BIOCIDE = "STRESS_BIOCIDE"
    METAL = "STRESS_METAL"
    HEAT = "STRESS_HEAT"
    VIR = "VIRULENCE"


class DatabaseReference(RWModel):  # pylint: disable=too-few-public-methods
    """Gene reference object."""

    ref_database: str | None
    ref_id: str | None


class GeneBase(BaseModel):  # pylint: disable=too-few-public-methods
    """Container for gene information"""

    gene_symbol: str | None
    sequence_name: str | None
    accession: str
    # prediction info
    depth: float | None
    identity: float
    coverage: float
    alignment_length: int
    ref_start_pos: int | None
    ref_end_pos: int | None
    ref_gene_length: int
    ass_start_pos: int | None
    ass_end_pos: int | None
    contig_id: str | None
    strand: Strand | None
    method: str | None  # prediction method
    # amrfinder plus exclusive amr classification
    element_type: str | None
    element_subtype: str | None


class ResistanceGene(
    GeneBase, DatabaseReference
):  # pylint: disable=too-few-public-methods
    """Container for resistance gene information"""

    phenotypes: List[str]
    res_class: str | None
    res_subclass: str | None


class VirulenceGene(
    GeneBase, DatabaseReference
):  # pylint: disable=too-few-public-methods
    """Container for virulence gene information"""

    virulence_category: str | None


class VariantBase(DatabaseReference):  # pylint: disable=too-few-public-methods
    """Container for mutation information"""

    variant_type: VariantType
    genes: List[str]
    position: int
    ref_codon: str
    alt_codon: str
    # prediction info
    depth: float


class ResistanceVariant(VariantBase):  # pylint: disable=too-few-public-methods
    """Container for resistance variant information"""

    phenotypes: List[str]


class ElementTypeResult(BaseModel):  # pylint: disable=too-few-public-methods
    """Phenotype result data model.

    A phenotype result is a generic data structure that stores predicted genes,
    mutations and phenotyp changes.
    """

    phenotypes: Dict[str, List[str]]
    genes: List[ResistanceGene | VirulenceGene]
    mutations: List[ResistanceVariant]
