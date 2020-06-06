from numpy import genfromtxt
from .training import train
from .core import DMatrix, Booster
from . import rabit
import logging
import json

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Federated:
    def __init__(self, rabit_config, root_certificate, certificate_chain, private_key):
        """
        Parameters
        ----------
        rabit_config : list
            list of Rabit configuration variables for tracker
        root_certificate : str
            path to root certificate
        certificate_chain : str
            path to certificate chain
        private_key : str
            path to private key
        """
        rabit_config_lst = json.loads(rabit_config)
        rabit_config_lst.append("rabit_root_cert_path=" + root_certificate)
        rabit_config_lst.append("rabit_cert_chain_path=" + certificate_chain)
        rabit_config_lst.append("rabit_private_key_path=" + private_key)

        # Python strings are unicode, but C strings are bytes, so we must convert to bytes.
        rabit_config = [bytes(s, 'utf-8') for s in rabit_config_lst]

        rabit.init(rabit_config)

    def load_data(self, data, missing=None, weight=None, 
            silent=False, feature_names=None,
            feature_types=None, nthread=None):
        """
        Load data as DMatrix

        Parameters
        ----------
        data : string
            Path to data. Must be the same at each party.
        
        Returns
        -------
        dmat : DMatrix
        """
        logging.info("Loading test data")
        data = genfromtxt(data, delimiter=',')
        dmat = DMatrix(data[:, 1:], label=data[:, 0], missing=missing, weight=weight, silent=silent, feature_names=feature_names, feature_types=feature_types, nthread=nthread)
        return dmat
    
    def get_num_parties(self):
        """
        Get number of parties in the federation

        Returns
        -------
        n : int
            Total number of parties in the federation
        """
        return rabit.get_world_size()

    def shutdown(self):
        logging.info("Shutting down tracker")
        rabit.finalize()
