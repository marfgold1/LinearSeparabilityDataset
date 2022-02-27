# Linear Separability Dataset

Merupakan project menggunakan bahasa pemrograman Python untuk membuat algoritma _Convex Hull_ menggunakan strategi _divide and conquer_ dalam visualisasi _linear separability dataset_. Proyek ini dibuat untuk pemenuhan tugas kecil 2 IF2211 Strategi Algoritma.

## Daftar Isi

- [Deskripsi Singkat](#deskripsi-singkat)
- [Requirement](#requirement)
- [Setup](#setup)
- [Usage](#usage)
- [Author](#author)

## Deskripsi Singkat
_Linear Separability Dataset_ merupakan pengujian dataset yang memastikan antar kelas tidak saling overlap dengan analisis melalui _convex hull_ dari masing-masing target kelas terhadap setiap pasang fitur. Pustaka ini merupakan contoh implementasi sendiri dari convex hull menggunakan strategi _divide and conquer_, secara spesifik Quickhull. Pustaka ini juga dilengkapi kelas yang dapat memberikan visualisasi terhadap separabilitas linear pada suatu dataset.

## Requirement
1. Python >= 3.7

## Setup
> Instalasi package otomatis akan menginstall modul lain yang dibutuhkan, sehingga tidak perlu menginstall manual dependensi dari pustaka ini.
1. **[RECOMMENDED]** Gunakan virtual environment Python baru.
2. Change directory ke folder project ini.
3. Install package dengan command berikut:
    ```
    pip install .
    ```
    
    > Untuk pengembangan, jalankan `pip install -e .` sehingga package terinstall dalam edit mode.
4. **[OPTIONAL]** Untuk **load dataset** dari `sklearn.dataset`, **harus** menggunakan extras `datasets`.
    ```
    pip install .[datasets]
    ```
    Terdapat extras `tests` untuk melakukan unit testing yang membutuhkan `scipy` dan dataset sklearn.
    ```
    pip install .[tests]
    ```

## Usage
### A. Library
Package dapat digunakan sebagai module python yang bisa diimport oleh program lain.
Terdapat dua kelas utama, yakni `ConvexHull` dan `LinearSeparabilityDataset`.

1. `ConvexHull` dapat digunakan untuk mencari convex hull dari titik di 2 dimensi.

2. `LinearSeparabilityDataset` dapat digunakan untuk load data, mengumpulkan target, serta memvisualisasi convex hull setiap pasang fitur untuk setiap target.
Untuk dokumentasi lebih lanjut, lihat docstring dari masing-masing kelas/fungsi yang akan digunakan.

Dokumentasi secara spesifik dapat dilihat pada docstring yang tersedia di pustaka ini.

Beberapa sample program yang dapat digunakan sebagai referensi:
1. Mendapatkan convex hull dari sekumpulan titik.
    ```py
    from myConvexHull.lib import ConvexHull as MyConvexHull
    hull = MyConvexHull([
        (4.3, 3.0),
        (4.6, 3.6),
        (4.4, 3.2)
    ])
    print(hull.simplices) # [(0, 1)]
    print(hull.vertices) # [0, 1]
    ```
2. Visualisasi linear separability dataset dari dataset iris dengan pasangan fitur pertama dan kedua serta pasangan fitur ketiga dan keempat.
    ```py
    from myConvexHull.lib import LinearSeparabilityDataset
    from sklearn import datasets
    data = datasets.load_wine(as_frame=True)
    data = LinearSeparabilityDataset(
        frame=data.frame,
        target_names=data.target_names,
    )
    data.visualize(0, 1)
    data.visualize(2, 3)
    ```
3. Visualisasi convex hull untuk angka acak.
    ```py
    import numpy as np
    import pandas as pd
    from myConvexHull.lib import LinearSeparabilityDataset
    data=LinearSeparabilityDataset(
        frame=pd.DataFrame(
            {
                'X': np.random.rand(100) * 50,
                'Y': np.random.rand(100) * 25,
                'target': np.random.randint(0, 4, 100),
            },
        ),
        target_names=['A', 'B', 'C', 'D'],
    )
    data.visualize('X', 'Y')
    ```
### B. Driver / Main Program
Package ini juga dilengkapi dengan driver program utama yang dapat dijalankan pada command line. Untuk melihat argumen lebih lengkap, jalankan command berikut:
```sh
python -m myConvexHull -h
```
Berikut argumen lengkap untuk menjalankan `python -m myConvexHull`:
```
usage: __main__.py [-h] [-f FILE] [-tk TARGET_KEY] [-tn TARGET_NAMES [TARGET_NAMES ...]] [-n DATASET_NAME] -fp FEATURE_PAIR FEATURE_PAIR [-s SIZE SIZE] [-nc]

Main driver of linear separability dataset visualizer. It will generate a plot of convex hull given a dataset.

options:
  -h, --help            show this help message and exit

File Dataset Input:
  -f FILE, --file FILE  Input datasets file. Should have minimum 3 columns: 2 features and a target.
  -tk TARGET_KEY, --target_key TARGET_KEY
                        Target column name.
  -tn TARGET_NAMES [TARGET_NAMES ...], --target_names TARGET_NAMES [TARGET_NAMES ...]
                        Target name list, separated by space.

Sklearn Dataset Input:
  -n DATASET_NAME, --dataset_name DATASET_NAME
                        Name of the dataset.

Visualization Options:
  -fp FEATURE_PAIR FEATURE_PAIR, --feature_pair FEATURE_PAIR FEATURE_PAIR
                        Feature pair to plot. Should be separated by space. You can supply multiple pair of feature.
  -s SIZE SIZE, --size SIZE SIZE
                        Figure size (width, height) of the plot.
  -nc, --no_captions    Disable captions (title, x/y label).
```

Beberapa contoh command yang dapat dieksekusi:
1. Visualisasi linear separability dataset untuk pasangan fitur pertama dan kedua dari dataset `breast_cancer`
    ```sh
    python -m myConvexHull -n breast_cancer -fp 0 1
    ```
2. Visualisasi untuk lebih dari 1 pasang fitur pada dataset iris, misalnya menampilkan visualisasi fitur pertama dan kedua, fitur kedua dan ketiga, serta fitur "sepal length (cm)" dan "sepal width (cm)".
    ```sh
    python -m myConvexHull -n iris -fp 0 1 -fp 1 2 -fp "sepal length (cm)" "sepal width (cm)"
    ```
    > Selain dengan indeksnya, fitur juga dapat ditulis dengan nama kolom pada dataset. Pastikan nama yang ditulis ada pada kolom di dataset.
3. Visualisasi data dari file `datasets/wine_data.csv` (asumsi current working directory ada pada root package ini).
    ```sh
    python -m myConvexHull -f "datasets/wine_data.csv" -tn Class0 Class1 Class2 -fp 0 1
    ```
4. Visualisasi data dari dataset [_water potability_](https://www.kaggle.com/adityakadiwal/water-potability). Contoh command ini menampilkan convex hull dari pasangan fitur pH dan Hardness serta Sulfate dan Conductivity.
    ```sh
    python -m myConvexHull -f "datasets/water_potability.csv" -tn "Not Potable" "Potable" -tk "Potability" -fp 0 1 -fp Sulfate Conductivity
    ```

Dalam menggunakan mode input file, pastikan semua syarat berikut terpenuhi:
- File harus dalam format csv.
- File harus diawali dengan nama kolom/header, dilanjutkan dengan baris berisi data tiap kolom.
- Pastikan terdapat kolom target yang secara default dinamakan `target` (case-sensitive). Jika nama kolom target berbeda, tambahkan argumen `-tk TARGET_KEY` pada perintah dengan `TARGET_KEY` merupakan nama kolom target.
- Kolom target harus berisi data berupa bilangan cacah dan tidak lompat (misal ada 3 baris data, baris pertama targetnya 1, baris kedua targetnya 3, baris ketiga targetnya 0, maka data ini salah karena melompati angka 2).
- Label nilai (`-tn` atau `--target_names`) dari target harus disusun secara terurut mulai dari label untuk target = 0.

### C. Test
Untuk menjaga kualitas saat pengembangan, terdapat unit testing yang tersedia pada package ini. Unit testing terdiri dari library yang membandingkan hasil antara ConvexHull dari scipy dengan pustaka ini, dan utils yang memastikan beberapa contoh input menghasilkan nilai yang benar.
```sh
python -m unittest discover -s tests
```
Pastikan untuk menginstall package dengan extras `tests` sebelum menjalankan test.

## Author

**Amar Fadil** [13520103]

Halo, saya Amar Fadil, mahasiswa IF dengan NIM 13520103, adalah seorang software engineer yang suka ngoprek grafika komputer, computer security, dan competitive programming (maybe). Berkuliah dalam program studi/jurusan Teknik Informatika (IF) pada fakultas Sekolah Teknik Elektro dan Informatika (STEI) di Institut Teknologi Bandung (ITB), saya bercita-cita untuk mengembangkan industri digital kreatif di Indonesia :D
