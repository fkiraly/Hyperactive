import pytest
import numpy as np

from sklearn import svm, datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA


from sklearn.utils.validation import check_is_fitted

from hyperactive.integrations import HyperactiveSearchCV
from hyperactive.optimizers import RandomSearchOptimizer


iris = datasets.load_iris()
X, y = iris.data, iris.target

nb = GaussianNB()
svc = svm.SVC()
pca = PCA()


parameters_svc = {"kernel": ["linear", "rbf"], "C": [1, 10]}
parameters_nb = {"var_smoothing": [1e-7, 1e-8, 1e-9]}
parameters_pca = {"n_components": [2, 3, 4]}

opt = RandomSearchOptimizer()


def test_fit():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)

    check_is_fitted(search)


def test_score():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)
    score = search.score(X, y)

    assert isinstance(score, float)


def test_classes_():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)

    assert [0, 1, 2] == list(search.classes_)


def test_score_samples():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)

    with pytest.raises(AttributeError):
        search.score_samples(X)


def test_predict():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)
    result = search.predict(X)

    assert isinstance(result, np.ndarray)


def test_predict_proba():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)

    with pytest.raises(AttributeError):
        search.predict_proba(X)

    search = HyperactiveSearchCV(nb, opt, parameters_nb)
    search.fit(X, y)
    result = search.predict(X)

    assert isinstance(result, np.ndarray)


def test_predict_log_proba():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)

    with pytest.raises(AttributeError):
        search.predict_log_proba(X)

    search = HyperactiveSearchCV(nb, opt, parameters_nb)
    search.fit(X, y)
    result = search.predict_log_proba(X)

    assert isinstance(result, np.ndarray)


def test_decision_function():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)
    result = search.decision_function(X)

    assert isinstance(result, np.ndarray)


def test_transform():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)

    with pytest.raises(AttributeError):
        search.transform(X)

    search = HyperactiveSearchCV(pca, opt, parameters_pca)
    search.fit(X, y)
    result = search.transform(X)

    assert isinstance(result, np.ndarray)


def test_inverse_transform():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)

    with pytest.raises(AttributeError):
        search.inverse_transform(X)

    search = HyperactiveSearchCV(pca, opt, parameters_pca)
    search.fit(X, y)
    result = search.inverse_transform(search.transform(X))

    assert isinstance(result, np.ndarray)


def test_best_params_and_score():
    search = HyperactiveSearchCV(svc, opt, parameters_svc)
    search.fit(X, y)

    best_params = search.best_params_
    best_score = search.best_score_

    assert "kernel" in best_params and "C" in best_params
    assert isinstance(best_score, float)
