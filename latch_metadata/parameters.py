
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'gtf': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title=None,
        description='Path to GTF file.',
    ),
    'split_amount': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title='Fastq options',
        description='The amount of lines to split  the fastq into (Default: 0)',
    ),
    'min_length': NextflowParameter(
        type=typing.Optional[int],
        default=500,
        section_title='Read trimming options',
        description='Choose minimum read length.',
    ),
    'min_q_score': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title=None,
        description='Choose minimum average read quality score.',
    ),
    'skip_trimming': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip quality trimming step.',
    ),
    'whitelist': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Cell barcode options',
        description='The file containing a list of barcodes.',
    ),
    'barcode_format': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Specify the format for the barcode+umi',
    ),
    'stranded': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Mapping',
        description='Library strandness option.',
    ),
    'kmer_size': NextflowParameter(
        type=typing.Optional[int],
        default=14,
        section_title=None,
        description='Minimizer k-mer length.',
    ),
    'save_secondary_alignment': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save secondary alignment outputs.',
    ),
    'analyze_uncorrected_bam': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Analysis options',
        description='Run downstream steps on the bam that contains reads that could not be corrected. Do not use this if no whitelist is provided.',
    ),
    'counts_level': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description="What level to generate the counts matrix at. Options: 'gene', 'transcript'.",
    ),
    'retain_introns': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Indicate whether to include introns in the count matrices',
    ),
    'skip_qc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Process skipping options',
        description='Skip all QC.',
    ),
    'skip_fastqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip FastQC.',
    ),
    'skip_nanoplot': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip Nanoplot.',
    ),
    'skip_toulligqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip ToulligQC.',
    ),
    'skip_fastq_nanocomp': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip NanoComp from FASTQ file(s).',
    ),
    'skip_bam_nanocomp': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip NanoComp from BAM file(s).',
    ),
    'skip_rseqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip RSeQC.',
    ),
    'skip_seurat': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip Seurat QC.',
    ),
    'skip_save_minimap2_index': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip saving minimap2 index.',
    ),
    'skip_dedup': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip umi dedup.',
    ),
    'skip_multiqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip MultiQC.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

