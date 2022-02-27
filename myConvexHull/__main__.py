import argparse
import pandas as pd

from myConvexHull.lib import LinearSeparabilityDataset

# Argument Parser
parser = argparse.ArgumentParser(
    description=' '.join([
        'Main driver of linear separability dataset visualizer.',
        'It will generate a plot of convex hull given a dataset.',
    ]),
    epilog=' '.join([
        'NOTE: You can specify the dataset by either',
        'file or dataset name, but NOT BOTH at the ',
        'same time. You always have to specify at least one',
        'of the feature pair you want to visualize.\n\n',
        'If you are using the file input mode, please make sure:\n',
        '(1) The file is in csv format.\n',
        '(2) The file started by a row for header/column name,',
        'continued by the row values.\n',
        '(3) There is a column named "target" for the target value.',
        'If the target column name is different, please specify',
        'the target column name with -tk/--target_key option.\n',
        '(4) Target column consist of whole number and cannot be skipped',
        '(e.g. you have 3 rows of values, first target is 1, second',
        'target is 3, and third target is 0, then this data is not valid',
        'because it skipped no. 2).\n',
        '(5) Specify the target names / label by -tn/--target_names option.',
        'Target names should be ordered starting from label for target = 0.',
    ])
)
# Group File Dataset
ginput = parser.add_argument_group('File Dataset Input')
ginput.add_argument('-f', '--file', help='Input datasets file. Should have minimum 3 columns: 2 features and a target.')
ginput.add_argument('-tk', '--target_key', help='Target column name.', default='target')
ginput.add_argument('-tn', '--target_names', nargs='+', help='Target name list, separated by space.')
# Group Sklearn Dataset
tinput = parser.add_argument_group('Sklearn Dataset Input')
tinput.add_argument('-n', '--dataset_name', help='Name of the dataset.')
# Group visualization options
vopt = parser.add_argument_group('Visualization Options')
vopt.add_argument('-fp', '--feature_pair', nargs=2, action='append', help='Feature pair to plot. Should be separated by space. You can supply multiple pair of feature.', required=True)
vopt.add_argument('-s', '--size', nargs=2, type=int, help='Figure size (width, height) of the plot.', default=(10, 6))
vopt.add_argument('-nc', '--no_captions', help='Disable captions (title, x/y label).', action='store_true')
args = parser.parse_args()

# Throw error if no dataset specified
if args.dataset_name is None and args.file is None:
    parser.error('Either dataset name or file should be supplied.')
# Throw error if both mode (file and dataset name) is specified
elif args.dataset_name is not None and args.file is not None:
    parser.error('Only one mode can be used, either dataset name or file should be supplied but not both.')

# Load and create visualizer object
vis: LinearSeparabilityDataset = None
if args.dataset_name:
    # Lazy load sklearn datasets
    from sklearn import datasets
    # Get the dataset in sklearn
    f = getattr(datasets, f'load_{args.dataset_name}')
    # If specified dataset name is not in sklearn, throw error.
    if f is None:
        parser.error(f'Dataset with name "{args.dataset_name}" is not exists.')
    # Create the dataset object
    data = f(as_frame=True)
    vis = LinearSeparabilityDataset(
        frame=data.frame,
        target_names=data.target_names,
    )
else:
    # Load the dataset from file
    data = pd.read_csv(args.file)
    data.dropna(inplace=True)
    vis = LinearSeparabilityDataset(
        frame=data,
        target_key=args.target_key,
        target_names=args.target_names,
    )

# Sanitize the feature pair
# (integer if number, else string)
args.feature_pair = [
    [
        int(fp[i])
        if fp[i].isnumeric()
        else fp[i]
        for i in range(2)
    ]
    for fp in args.feature_pair
]

# Visualize each feature pair
for fp in args.feature_pair:
    vis.visualize(
        fp[0], fp[1],
        figsize=args.size,
        captions=(not args.no_captions),
    )
