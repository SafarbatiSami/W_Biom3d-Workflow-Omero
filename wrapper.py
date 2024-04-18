import sys
import os
import shutil
import subprocess
from subprocess import call
from cytomine.models import Job
from biaflows import CLASS_OBJSEG, CLASS_SPTCNT, CLASS_PIXCLA, CLASS_TRETRC, CLASS_LOOTRC, CLASS_OBJDET, CLASS_PRTTRK, CLASS_OBJTRK
from biaflows.helpers import BiaflowsJob, prepare_data, upload_data, upload_metrics, get_discipline
import time
import shutil
# Assuming biom3d has relevant classes/functions you need to import


def main(argv):
    
    with BiaflowsJob.from_cli(argv) as bj:
        # Change following to the actual problem class of the workflow
        problem_cls = get_discipline(bj, default=CLASS_OBJSEG)
        # 1. Prepare data for workflow
        in_imgs, gt_imgs, in_path, gt_path, out_path, tmp_path = prepare_data(problem_cls, bj, is_2d=False, **bj.flags)

        # 2. Run image analysis workflow
        bj.job.update(progress=25, statusComment="Launching workflow...")
        # Assuming these environment variables are set correctly
        num_classes = bj.parameters.num_classes
        description = bj.parameters.desc
        
 
        # Construct the command to run biom3d
        cmd = [
            "python", "-m", "biom3d.preprocess_train",
            "--img_dir", in_path,
            "--msk_dir", gt_path,
            "--num_classes", "{:d}".format(num_classes),
            "--desc", description
        ]


        status = subprocess.run(cmd)

        if status.returncode != 0:
            print("Running Biom3d failed, terminate")
            sys.exit(1)
                # 5. Pipeline finished

        bj.job.update(progress=100, status=Job.TERMINATED, status_comment="Finished.")

if __name__ == "__main__":
    main(sys.argv[1:])
