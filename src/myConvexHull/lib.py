"""
Main class definitions
"""

import numpy as np
import pandas as pd

from itertools import cycle
from matplotlib import pyplot as plt
from typing import Dict, Iterable, List, Tuple
from myConvexHull.types import Feature, Line, Point, PointIndex, LineIndex
from myConvexHull.utils import det, dist_to_line

class ConvexHull(object):
    def __init__(self, dt: Iterable):
        """Create new convex hull instance.

        It will auto process the data by generating
        the convex hull. Only works for static 2D points.

        Args:
            dt (Iterable): List of 2D points, where each element
                is an iterable that has two number, (x, y).
        """
        dt: List[Point] = [(p[0], p[1]) for p in dt]
        self.points = dt
        """All points inside and in the convex hull.
        """
        self.vertices: List[PointIndex] = []
        """List of the point/vertex in the convex hull. Each element
        is an index from self.points.
        """ 
        self.simplices: List[LineIndex] = []
        """List of the line/edge in the convex hull. Each element
        is a tuple, that is a pair of two index from self.points.
        """
        self.__convexHull()
    
    def __dnc_convexHull(self, dt: List[PointIndex], line: LineIndex):
        """Divide and Conquer algo of convex hull.

        It is based on quickhull algorithm.

        Args:
            dt (List[int]): Points to check outside the line.
                Each element is index to self.points.
            line (List[int, int]): Line to check the points.
                Each element is a pair of index to self.points.
        """
        # There are two base cases
        # 1. If there are no point left, then we are done.
        #    Add the line to the simplices list.
        if len(dt) == 0:
            self.simplices += [line]
        # 2. If there is only one point left, then the hull vertices
        #    must be the point. Add the point to vertices list.
        #    Make two lines that starts from point to each line point.
        #    Add both lines to the simplices list (edge of the hull).
        elif len(dt) == 1:
            self.simplices += [
                (dt[0], line[0]),
                (dt[0], line[1]),
            ]
            self.vertices.append(dt[0])
        # Recursive case
        else:
            # DIVIDE
            # 0. Get the line points in coord from self.points
            pline = (self.points[line[0]], self.points[line[1]])
            # 1. Get a point that has maximum distance to the line
            pmax = max(
                dt,
                key=lambda x: dist_to_line(pline, self.points[x])
            )
            # 1.1 The point above is the new vertices of the hull
            #     Add the point to the vertices list
            self.vertices.append(pmax)
            # 1.2 Remove that max point from the list
            dt.remove(pmax)
            # 2. Create two new lines that starts from each point
            #    in the line until the max point.
            newline: Tuple[LineIndex, LineIndex] = (
                (line[0], pmax),
                (pmax, line[1]),
            )
            # 2.1. Get the points of both line (remember that the
            #      new line from above is just the indexes).
            pnewline: Tuple[Line, Line] = tuple(
                (self.points[p[0]], self.points[p[1]])
                for p in newline
            )
            # 3. Get the points that are outside both the new line
            #    Also split the points into two groups, that is either
            #    outside the first line or the second line.
            dt_split: List[List[PointIndex], List[PointIndex]] = [[], []]
            for p in dt:
                # First line is vector (p1,pmax), so the point outside this
                # must be in the left side, which has determinant of > 0
                if det(pnewline[0], self.points[p]) > 0:
                    dt_split[0].append(p)
                # Second line is vector (pmax,p2), so the point outside this
                # must be in the left side (relative to vector direction) too,
                # which has determinant of > 0
                elif det(pnewline[1], self.points[p]) > 0:
                    dt_split[1].append(p)
            # COMBINE & CONQUER
            # 4. Recursive call
            # 4.1 Check for points outside the first line
            self.__dnc_convexHull(dt_split[0], newline[0])
            # 4.2 Check for points outside the second line.
            self.__dnc_convexHull(dt_split[1], newline[1])
    
    def __convexHull(self):
        """The first step before recursive DnC algo.
        """
        # Get index list of all points
        dt = [i for i in range(len(self.points))]
        # Base case:
        # 1. If there is less than 2 points,
        #    it doesn't have any convex hull, skip.
        # 2. If there is only 2 points, then the hull
        #    is just the line between them.
        if len(dt) == 2:
            self.vertices = dt
            self.simplices = [(dt[0], dt[1])]
        # If there are more than 2 points,
        # then we need to check for some things
        elif len(dt) > 2:
            # Sort the points ascending by their x and y coordinate
            dt.sort(key=lambda x: self.points[x])
            # Get the line that start from minimum point
            # to maximum point based on their x coordinate.
            line = (dt[0], dt[-1])
            # Both points are the vertex of the hull, so add them
            # to the vertices list.
            self.vertices.extend(line)
            # Also get the actual points instead of the indexes.
            pline = (self.points[line[0]], self.points[line[1]])
            # Remove min and max point from the list
            dt = dt[1:-1]
            # Divide the points into two groups, that is either
            # is in the left side or the right side of the line.
            dt_split = [[], []]
            for p in dt:
                d = det(pline, self.points[p])
                # If the determinant is > 0, then the point is
                # in the left side of the line.
                if d > 0:
                    dt_split[0].append(p)
                # If the determinant is < 0, then the point is
                # in the right side of the line.
                elif d < 0:
                    dt_split[1].append(p)

            # Base case 3
            if len(dt_split[0]) + len(dt_split[1]) == 0:
                # If points are in the same line, then the hull will
                # be the line that start from minimum point to
                # maximum point.
                self.simplices = [line]
                self.vertices = [*line]
            # Recursive case
            else:
                # COMBINE & CONQUER
                # Get convex hull from the left side of the line
                self.__dnc_convexHull(dt_split[0], line)
                # Get convex hull from the right side of the line
                #  Reverse the order of the line points because we have
                #  to keep side convention (if not reversed, left will
                #  be right and vice versa).
                self.__dnc_convexHull(dt_split[1], line[::-1])

# Color cycle constant
COLOR_CYCLE = cycle([
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
])

class LinearSeparabilityDataset(object):
    def __init__(self,
        frame: pd.DataFrame,
        target_names: Iterable,
        feature_names: Iterable=None,
        target_key: str='target',
        backend: ConvexHull=ConvexHull
    ) -> None:
        """Create new instance of Linearly Separable Data.
        Useful to easy visualize the data given their dataset.

        Target is the predicted column (y) of the rows given their
        features, while features is the column data other than
        target itself (x). You HAVE to always provide the target
        names. If `feature_names` is not provided, then it will
        automatically get the column names from the `frame` excluding
        the `target_key`.

        This class will lazy compute the convex hull, meaning that it
        will compute the convex hull of feature pair only once, that
        is when you first time call `getConvex` or `visualize` for
        that feature pair.
        
        Make sure:
        1. `target_names` has the same length as unique value
        counts on the `frame['target']`.
        2. `feature_names` has the same length as total column
        in the `frame` excluding `target_key`.
        3. `target_key` is in the frame.
        In any case those condition not met, the program will
        raise exception.

        Args:
            frame (pd.DataFrame): Dataframe of the dataset.
                It should include both target and its features.
            target_names (np.ndarray): Names of the target.
            feature_names (list): Names of the features.
            target_key (str, optional): Target column name.
                Defaults to 'target'.
            backend (ConvexHull, optional): Convex hull computation
                backend. Defaults to custom ConvexHull.
        
        Raises:
            ValueError: If the length of `target_names` or
            `feature_names` is not qualified.
            KeyError: If `target_key` not exists in the frame.
        """
        if len(target_names) != frame[target_key].nunique():
            raise ValueError(
                "The length of `target_names` should be equal to "
                "the unique value counts on `frame[target_key]` "
                "(Expected {} but got {}).".format(
                    frame[target_key].nunique(),
                    len(target_names),
                )
            )
        
        if feature_names is None:
            feature_names = list(frame.columns)
            feature_names.remove(target_key)
        elif len(feature_names) != len(frame.columns) - 1:
            raise ValueError(
                "The length of `feature_names` should be the same "
                "as the total column in the `frame` excluding "
                "`target_key` (Expected {} but got {}).".format(
                    len(frame.columns) - 1,
                    len(feature_names),
                )
            )

        if target_key not in frame.columns:
            raise KeyError(
                "The `target_key` should be in the frame."
            )

        self.__convex: Dict[str, List[ConvexHull]] = {}
        """List of convex hull for each target and for each
        pair of features. The key is joined index of both
        feature in the pair, separated by ';'.
        """
        self.target_key = target_key
        """Target column name in the dataframe.
        """
        self.frame = frame
        """Dataframe of the dataset, consist of both
        its features and target.
        """
        self.target_names = target_names
        """List of the target name/label.
        """
        self.feature_names = feature_names
        """List of the feature name/label.
        """
        self.backend = backend
        """Backend of the convex hull library.
        """

    def __getPair(self, pair1: Feature, pair2: Feature) -> Tuple[int, int]:
        """Get the feature pair index.
        It will get a pair of the feature index
        given both feature name.

        Args:
            pair1 (Feature): Feature pair 1.
            pair2 (Feature): Feature pair 2.

        Returns:
            Tuple[int, int]: Pair of the feature index.
        """
        return ((
            self.feature_names.index(pair1)
            if isinstance(pair1, str) else pair1,
            self.feature_names.index(pair2)
            if isinstance(pair2, str) else pair2,
        ))

    def __calculate(self, key:str, p1: int, p2: int) -> None:
        """Calculate the convex hull for each target.

        Args:
            key (str): Key in the dictionary of convex hull.
            p1 (int): First feature index.
            p2 (int): Second feature index.
        """
        self.__convex[key] = []
        for i in range(len(self.target_names)):
            # Get the dataframe with same target name.
            bucket = self.frame[self.frame[self.target_key] == i]
            # Get the pair of values from both features.
            # It will be our points.
            bucket = bucket.iloc[:, [p1, p2]].values
            # Create the convex hull and append it to the list.
            self.__convex[key].append(self.backend(bucket))

    def getConvex(self, pair1: Feature, pair2: Feature) -> List[ConvexHull]:
        """Get convex hull given pair of features.
        Pair of features can be given by their index or their name.

        Args:
            pair1 (int | str): First feature.
            pair2 (int | str): Second feature.

        Returns:
            List[ConvexHull]: List of convex hull for each target.
        """
        # Get the pair of feature index.
        pair1, pair2 = self.__getPair(pair1, pair2)
        # Get the key to use in the convex hull dictionary.
        key = ';'.join([str(pair1), str(pair2)])
        # If the convex hull is already calculated, just return it.
        if key in self.__convex:
            return self.__convex[key]
        # If the convex hull is not calculated, 
        # calculate and return it.
        self.__calculate(key, pair1, pair2)
        return self.__convex[key]

    def visualize(self,
        pair1: Feature,
        pair2: Feature,
        figsize: Tuple[int, int]=(10, 6),
        captions: bool=True,
        title: str=None,
        xlabel: str=None,
        ylabel: str=None,
    ) -> None:
        """Visualize the data given pair of features.
        Pair of features can be given by their index or their name.

        Args:
            pair1 (int | str): First feature.
            pair2 (int | str): Second feature.
            figsize (Tuple[int, int], optional): Figure size.
                Defaults to (10, 6).
            captions (bool, optional): Enable caption label.
                Consist of title, xlabel and ylabel. Defaults to True.
            title (str, optional): Title of the figure.
                Defaults to None.
            xlabel (str, optional): Label on the x side of the figure.
                Defaults to None.
            ylabel (str, optional): Label on the y side of the figure.
                Defaults to None.
        """
        # Get the convex of the pair of feature.
        data = self.getConvex(pair1, pair2)
        # Get the pair of feature index.
        pair1, pair2 = self.__getPair(pair1, pair2)
        # Create new figure.
        plt.figure(figsize=figsize)
        # Write captions if enabled.
        if captions:
            # Get the default x and y label
            if xlabel is None:
                xlabel = self.feature_names[pair1]
            if ylabel is None:
                ylabel = self.feature_names[pair2]
            # Write the title, x, and y label.
            plt.title(title if title else f'{xlabel} vs {ylabel}')
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
        # Plot the convex hull for each target.
        for i in range(len(self.target_names)):
            # Get current color
            col = next(COLOR_CYCLE)
            # Get the bucket points
            bucket = np.array(data[i].points)
            # Visualize the points with scatter plot.
            # Label them with its corresponding target name.
            plt.scatter(
                bucket[:, 0],
                bucket[:, 1],
                label=self.target_names[i],
                color=col,
            )
            # Visualize the convex hull.
            # Plot the simplices lines from the convex hull.
            for simplex in data[i].simplices:
                plt.plot(bucket[simplex, 0], bucket[simplex, 1], color=col)
        # Show legends and then show the figure.
        plt.legend()
        plt.show()
