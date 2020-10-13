# hla_graph

Mon projet est cool pourquoi ? qu'est ce qu'on a fait

## Installation 

```shell script
git clone https://github.com/cedricusureau/HLA_graph.git
cd HLA_graph
conda env create -f environment.yml
```

## Usage 


###Activate environment:
```shell script
conda activate HLA_graph
```

###Run in CLI:

Place any number of input file in `/data/sample_example/SA1` or `/data/sample_example/SA2`. Then run :

```shell script
python -m src.hla_main.py
```
Output files are generated in `result` folder.
You could change the MFI's treshold with `-c` argument (default: 1000).

```shell script
python -m src.hla_main.py -c 2000
```

###Run server:
```shell script
python server.py
```

Once running, open a web browser and go to `localhost:5000`