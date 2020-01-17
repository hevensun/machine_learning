import pandas as pd
from collections import Counter
import pickle

train_data_path = '/Users/slade/Documents/Code/machine-learning/data/avazu_CTR/train_sample.csv'
train_data = pd.read_csv(train_data_path)
train_data['click'] = train_data['click'].map(lambda x: -1 if x == 0 else x)

click = set()
C1 = set()
C16 = set()
C18 = set()

# build category data
# for data in train_data:
data = train_data.copy()
click_v = set(data['click'].values)
click = click | click_v
C1_v = set(data['C1'].values)
C1 = C1 | C1_v
C16_v = set(data['C16'].values)
C16 = C16 | C16_v
C18_v = set(data['C18'].values)
C18 = C18 | C18_v

category_encoding_fields = ['C1', 'C18', 'C16']

feature2field = {}
field_index = 0
ind = 0
for field in category_encoding_fields:
    field_dict = {}
    field_sets = eval(field)
    for value in list(field_sets):
        field_dict[value] = ind
        feature2field[ind] = field_index
        ind += 1
    field_index += 1
    with open('/Users/slade/Documents/Code/machine-learning/data/avazu_CTR/sets/' + field + '.pkl', 'wb') as f:
        pickle.dump(field_dict, f)

click_dict = {}
click_sets = click
for value in list(click_sets):
    click_dict[value] = ind
    ind += 1

with open('/Users/slade/Documents/Code/machine-learning/data/avazu_CTR/sets/' + 'click' + '.pkl', 'wb') as f:
    pickle.dump(click_dict, f)

with open('/Users/slade/Documents/Code/machine-learning/data/avazu_CTR/sets/feature2field.pkl', 'wb') as f:
    pickle.dump(feature2field, f)
