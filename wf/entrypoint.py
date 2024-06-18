from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], genome: typing.Optional[str], fasta: LatchFile, gtf: LatchFile, skip_trimming: typing.Optional[bool], whitelist: typing.Optional[LatchFile], barcode_format: str, stranded: typing.Optional[str], save_secondary_alignment: typing.Optional[bool], analyze_uncorrected_bam: typing.Optional[bool], counts_level: str, skip_qc: typing.Optional[bool], skip_fastqc: typing.Optional[bool], skip_nanoplot: typing.Optional[bool], skip_toulligqc: typing.Optional[bool], skip_fastq_nanocomp: typing.Optional[bool], skip_bam_nanocomp: typing.Optional[bool], skip_rseqc: typing.Optional[bool], skip_seurat: typing.Optional[bool], skip_save_minimap2_index: typing.Optional[bool], skip_dedup: typing.Optional[bool], skip_multiqc: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], split_amount: typing.Optional[int], min_length: typing.Optional[int], min_q_score: typing.Optional[int], kmer_size: typing.Optional[int], retain_introns: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('gtf', gtf),
                *get_flag('split_amount', split_amount),
                *get_flag('min_length', min_length),
                *get_flag('min_q_score', min_q_score),
                *get_flag('skip_trimming', skip_trimming),
                *get_flag('whitelist', whitelist),
                *get_flag('barcode_format', barcode_format),
                *get_flag('stranded', stranded),
                *get_flag('kmer_size', kmer_size),
                *get_flag('save_secondary_alignment', save_secondary_alignment),
                *get_flag('analyze_uncorrected_bam', analyze_uncorrected_bam),
                *get_flag('counts_level', counts_level),
                *get_flag('retain_introns', retain_introns),
                *get_flag('skip_qc', skip_qc),
                *get_flag('skip_fastqc', skip_fastqc),
                *get_flag('skip_nanoplot', skip_nanoplot),
                *get_flag('skip_toulligqc', skip_toulligqc),
                *get_flag('skip_fastq_nanocomp', skip_fastq_nanocomp),
                *get_flag('skip_bam_nanocomp', skip_bam_nanocomp),
                *get_flag('skip_rseqc', skip_rseqc),
                *get_flag('skip_seurat', skip_seurat),
                *get_flag('skip_save_minimap2_index', skip_save_minimap2_index),
                *get_flag('skip_dedup', skip_dedup),
                *get_flag('skip_multiqc', skip_multiqc),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_scnanoseq", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_scnanoseq(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], genome: typing.Optional[str], fasta: LatchFile, gtf: LatchFile, skip_trimming: typing.Optional[bool], whitelist: typing.Optional[LatchFile], barcode_format: str, stranded: typing.Optional[str], save_secondary_alignment: typing.Optional[bool], analyze_uncorrected_bam: typing.Optional[bool], counts_level: str, skip_qc: typing.Optional[bool], skip_fastqc: typing.Optional[bool], skip_nanoplot: typing.Optional[bool], skip_toulligqc: typing.Optional[bool], skip_fastq_nanocomp: typing.Optional[bool], skip_bam_nanocomp: typing.Optional[bool], skip_rseqc: typing.Optional[bool], skip_seurat: typing.Optional[bool], skip_save_minimap2_index: typing.Optional[bool], skip_dedup: typing.Optional[bool], skip_multiqc: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], split_amount: typing.Optional[int] = 0, min_length: typing.Optional[int] = 500, min_q_score: typing.Optional[int] = 10, kmer_size: typing.Optional[int] = 14, retain_introns: typing.Optional[bool] = True) -> None:
    """
    nf-core/scnanoseq

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, genome=genome, fasta=fasta, gtf=gtf, split_amount=split_amount, min_length=min_length, min_q_score=min_q_score, skip_trimming=skip_trimming, whitelist=whitelist, barcode_format=barcode_format, stranded=stranded, kmer_size=kmer_size, save_secondary_alignment=save_secondary_alignment, analyze_uncorrected_bam=analyze_uncorrected_bam, counts_level=counts_level, retain_introns=retain_introns, skip_qc=skip_qc, skip_fastqc=skip_fastqc, skip_nanoplot=skip_nanoplot, skip_toulligqc=skip_toulligqc, skip_fastq_nanocomp=skip_fastq_nanocomp, skip_bam_nanocomp=skip_bam_nanocomp, skip_rseqc=skip_rseqc, skip_seurat=skip_seurat, skip_save_minimap2_index=skip_save_minimap2_index, skip_dedup=skip_dedup, skip_multiqc=skip_multiqc, multiqc_methods_description=multiqc_methods_description)

