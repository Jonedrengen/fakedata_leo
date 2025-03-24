# fakedata_leo

This is a python program, that generates fake covid data based on real covid data sampled from the danish healthcare main laboratory and center for disease prevention and treatment - Statens Serum Institut (SSI)

## Installation

To install you need

1. a code editor like Visual Studio Code or PyCharm
2. a version of Homebrew: https://brew.sh/
3. python version 3.10 or later
4. the packages listed in "requirements.txt" installed (preferably in an isolated environment like Conda)

to install packages in requirements.txt
```bash
pip install -r requirements.txt
```

## Usage
When the packages from requirements.txt are installed, you can run the program from main.py
* you can change the batch amount and size as you please, but keep in mind that there are only 1.000.000 possible unique ids. If the program runs out of ids, it will crash

### in main.py:
these two variables can be changed

```python
batch_amount = 8500
batch_size = 96
```
## Output
6 csv formatted files will be generated in the output folder

## important_files folder
this folder contains files that originate from real covid data. The files are used to weigh the chance of which data should be generated. 
* If you wish to change the weighting of data, you can replace the csv files with other files of the same structure

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)