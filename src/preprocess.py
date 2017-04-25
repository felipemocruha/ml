import os
import pandas as pd
from parser import tokenize_url
from main import load_targets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


ROOT_DIR = os.path.dirname(os.path.abspath('.'))


def load_data():
    data_path = os.path.join(ROOT_DIR, 'data', 'meta_results.json')
    products = pd.read_json(data_path).products
    return products


if __name__ == '__main__':
    offers = load_targets()
    #tokenized = [tokenize_url(offer) for offer in offers]
    ###df = pd.DataFrame()
    vec = TfidfVectorizer()
    x = vec.fit_transform(offers)
    km = KMeans(n_clusters=10, init='k-means++', max_iter=100, n_init=1)
    km.fit(x)
    print(dir(km))
