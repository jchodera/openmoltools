from unittest import skipIf
import tempfile
import os
from gaff2xml import utils
import numpy as np
import mdtraj as md
from distutils.spawn import find_executable
import tarfile
import pickle
import os
import numpy as np



@skipIf(find_executable('obabel') is None, 'You need obabel installed to run this test')
@skipIf(os.environ.get("TRAVIS", None) == 'true', "Skip testing of entire FreeSolv database on Travis.")
def test_load_freesolv_gaffmol2_vs_sybylmol2_vs_obabelpdb():
    with utils.enter_temp_directory():        
        
        tar_filename = utils.get_data_filename("chemicals/freesolv/freesolve_v0.3.tar.bz2")
        tar = tarfile.open(tar_filename, mode="r:bz2")
        tar.extractall()
        tar.close()

        database = pickle.load(open("./v0.3/database.pickle"))
        for key in database:
            gaff_filename = os.path.abspath("./v0.3/mol2files_gaff/%s.mol2" % key)            
            
            cmd = """sed -i "s/<0>/LIG/" %s""" % gaff_filename
            os.system(cmd)  # Have to remove the <0> because it leads to invalid XML in the forcefield files.
            
            t_gaff = md.load(gaff_filename)

            with utils.enter_temp_directory():        
                 yield utils.tag_description(lambda : utils.test_molecule("LIG", gaff_filename), "Testing freesolv %s" % key)
