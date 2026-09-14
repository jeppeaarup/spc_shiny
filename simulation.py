def simulate_data(n):
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng()

    data = pd.DataFrame({
        'y': rng.normal(size=n),
        'x': np.arange(n) + 1
    })

    return data
    