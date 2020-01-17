# Tsnewp
T-distributed stochastic neighbor embedding(t-SNE) rewrite with Python by ourselves, it's a good dimensionality reduction method.

# PyVersions
- Python 3.6

# Dependencies
- [numpy](https://github.com/numpy/numpy)

# Documentation
Install model
```python
pip install Tsnewp
```

Setup model
```python
from Tsnewp import Tsnewp
tsne = Tsnewp(is_reduce_dim=0, reduce_dim=None, out_dim=2, perplexity=30, max_iters=1000)
```

Transform data
```python
tsne.transform(data,initial_momentum=0.5, final_momentum=0.8, eta=500, min_gain=0.01)
```

