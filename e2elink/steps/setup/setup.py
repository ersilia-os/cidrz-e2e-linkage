import os
import json
import shutil
from ...vars import E2ELINK_DIR
from ... import logger
import time
SESSION_PARAMS = "session.json"


class Session(object):
    def __init__(self):
        self._params_json_file = self._session_params_file()

    def _session_params_file(self):
        return os.path.join(E2ELINK_DIR, SESSION_PARAMS)

    def get_output_path(self):
        with open(self._params_json_file, "r") as f:
            return json.load(f)["output_dir"]


class PipelineSetup(object):
    def __init__(self, src_file, trg_file, truth_file, output_dir, column_mapping_file):
        self.src_file = os.path.abspath(src_file)
        self.trg_file = os.path.abspath(trg_file)

        self.column_mapping = None
        if column_mapping_file is not None:
            column_mapping_file = os.path.abspath(column_mapping_file)
            with open(column_mapping_file) as f:
                self.column_mapping = json.load(f)

        if truth_file is not None:
            self.truth_file = os.path.abspath(truth_file)
        else:
            self.truth_file = None

        self.output_dir = os.path.abspath(output_dir)
        if os.path.exists(self.output_dir):
            logger.error("Output folder {0} exists!".format(self.output_dir))
            dir_suffix = time.strftime("%Y%m%d%H%M%S", time.localtime())
            self.output_dir = "{0}_{1}".format(self.output_dir, dir_suffix)
            #logger.info("creating new output director {0}{}".format())
            #raise FileExistsError("The specified output folder {0} already exists".format(self.output_dir))
        #else:
        logger.debug("Output folder {0} created".format(self.output_dir))
        os.makedirs(self.output_dir, exist_ok=True)

        self.session = Session()
        self.params = {"output_dir": self.output_dir}
        with open(self.session._params_json_file, "w") as f:
            json.dump(self.params, f, indent=4)
        logger.debug(
            "JSON parameters file {0} created".format(self.session._params_json_file)
        )

    def _make_subdir(self, name):
        os.makedirs(os.path.join(self.output_dir, name))

    def _create_output_structure(self):
        self._make_subdir("raw")
        self._make_subdir("schema")
        self._make_subdir("preprocess")
        self._make_subdir("block")
        self._make_subdir("compare")
        self._make_subdir("score")
        self._make_subdir("evaluate")
        self._make_subdir("finish")
        shutil.copyfile(self.src_file, os.path.join(self.output_dir, "raw", "src.csv"))
        shutil.copyfile(self.trg_file, os.path.join(self.output_dir, "raw", "trg.csv"))
        if self.truth_file is not None:
            shutil.copyfile(
                self.truth_file, os.path.join(self.output_dir, "raw", "truth.csv")
            )
        logger.info("Created output folder structure at {0}".format(self.output_dir))

    def setup(self):
        self._create_output_structure()
