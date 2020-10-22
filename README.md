# HLA graph

HLA Graph is a tool dedicated to biologist working on anti-HLA antibodies assay. 

Based on retrospective analysis of thousands of samples from Luminex™ LABScreen™ single-antigen assays, we designed networks, also named graphs, 
providing an updated overview of class I and II HLA antigens cross-reactivity. 

In these graphs, each node correspond to an allele and each link correspond to a strong MFI correlation between two alleles. 

As we showed that strong MFI correlation between different antigens reflect epitopic similarity, we have developed a tool 

<p align="center">
  <img width="300" height="200" src="https://raw.githubusercontent.com/cedricusureau/HLA_graph/master/figures/eplet_corr.png">
</p>

## Installation 

```shell script
git clone https://github.com/cedricusureau/HLA_graph.git
cd HLA_graph
conda env create -f environment.yml
```

## Usage 


### Activate environment:
```shell script
conda activate HLA_graph
```

### Run server:
```shell script
python server.py
```
Once running, open a web browser and go to `localhost:5000`

### Run in CLI:

Place any number of input file in `/data/sample_example/SA1` or `/data/sample_example/SA2`. Then run :

```shell script
python -m src.hla_main
```
Output files are generated in `result` folder.
You could change the MFI's treshold with `-c` argument (default: 1000).

```shell script
python -m src.hla_main.py -c 2000
```
