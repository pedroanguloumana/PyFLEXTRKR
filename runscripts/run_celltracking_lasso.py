import os
import sys
import logging
import dask
from dask.distributed import Client, LocalCluster
from pyflextrkr.ft_utilities import load_config
from pyflextrkr.regrid_lasso_reflectivity import regrid_lasso_reflectivity
from pyflextrkr.idfeature_driver import idfeature_driver
from pyflextrkr.advection_tiles import calc_mean_advection
from pyflextrkr.tracksingle_driver import tracksingle_driver
from pyflextrkr.gettracks import gettracknumbers
from pyflextrkr.trackstats_driver import trackstats_driver
from pyflextrkr.mapfeature_driver import mapfeature_driver
from pyflextrkr.regrid_celltracking_mask import regrid_celltracking_mask

if __name__ == '__main__':
    # Set the logging message level
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Load configuration file
    config_file = sys.argv[1]
    config = load_config(config_file)

    ################################################################################################
    # Parallel processing options
    if config['run_parallel'] == 1:
        # Set Dask temporary directory for workers
        dask_tmp_dir = config.get("dask_tmp_dir", "./")
        dask.config.set({'temporary-directory': dask_tmp_dir})
        # Local cluster
        cluster = LocalCluster(n_workers=config['nprocesses'], threads_per_worker=1, silence_logs=True)
        client = Client(cluster)

    # Step 0 - Regrid reflectivity
    if config['run_regridreflectivity']:
        regrid_lasso_reflectivity(config)

    # Step 1 - Identify features
    if config['run_idfeature']:
        idfeature_driver(config)

    # Step 2 - Run advection calculation
    if config['run_advection']:
        logger.info('Calculating domain mean advection.')
        driftfile = calc_mean_advection(config)
    else:
        driftfile = f'{config["stats_outpath"]}advection_' + \
                    f'{config["startdate"]}_{config["enddate"]}.nc'
    config.update({"driftfile": driftfile})

    # Step 3 - Link features in time adjacent files
    if config['run_tracksingle']:
        tracksingle_driver(config)

    # Step 4 - Track features through the entire dataset
    if config['run_gettracks']:
        tracknumbers_filename = gettracknumbers(config)

    # Step 5 - Calculate track statistics
    if config['run_trackstats']:
        trackstats_filename = trackstats_driver(config)

    # Step 6 - Map tracking to pixel files
    if config['run_mapfeature']:
        mapfeature_driver(config)

    # Step 7 - Regrid pixel masks to original grid
    if config['run_regridmask']:
        regrid_celltracking_mask(config)