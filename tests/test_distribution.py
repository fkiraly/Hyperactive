import numpy as np
from tqdm import tqdm
from hyperactive import Hyperactive


def objective_function(opt):
    score = -opt["x1"] * opt["x1"]
    return score


search_space = {
    "x1": np.arange(-100, 101, 1),
}


def test_n_jobs_0():
    hyper = Hyperactive(n_processes=2)
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)
    hyper.run()

    assert len(hyper.results_list) == 2


def test_n_jobs_1():
    hyper = Hyperactive(n_processes=4)
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=4)
    hyper.run()

    assert len(hyper.results_list) == 4


def test_n_jobs_2():
    hyper = Hyperactive(n_processes=8)
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=8)
    hyper.run()

    assert len(hyper.results_list) == 8


def test_n_jobs_3():
    hyper = Hyperactive(n_processes=-1)
    hyper.add_search(objective_function, search_space, n_iter=15)
    hyper.run()


def test_n_jobs_4():
    hyper = Hyperactive(n_processes=100)
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=100)
    hyper.run()

    assert len(hyper.results_list) == 100


def test_multiprocessing_0():
    hyper = Hyperactive(distribution="multiprocessing", n_processes=2)
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)
    hyper.run()


def test_multiprocessing_1():
    hyper = Hyperactive(
        distribution={
            "multiprocessing": {
                "initializer": tqdm.set_lock,
                "initargs": (tqdm.get_lock(),),
            }
        },
        n_processes=2,
    )
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)
    hyper.run()


def test_joblib_0():
    hyper = Hyperactive(distribution="joblib", n_processes=2)
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)
    hyper.run()


def test_joblib_1():
    from joblib import Parallel, delayed

    def joblib_wrapper(process_func, search_processes_paras, n_jobs, **kwargs):
        n_jobs = len(search_processes_paras)

        jobs = [
            delayed(process_func)(**info_dict) for info_dict in search_processes_paras
        ]
        results = Parallel(n_jobs=n_jobs, **kwargs)(jobs)

        return results

    hyper = Hyperactive(distribution=joblib_wrapper, n_processes=2)
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)

    hyper.run()
