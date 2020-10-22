# HLA graph

__HLA Graph__ is a tool dedicated to biologist working on anti-HLA antibodies assay. 

Based on retrospective analysis of __thousands of samples__ from Luminex™ LABScreen™ single-antigen assays, we designed networks, also called __graphs__, 
providing an updated overview of class I and II HLA antigens cross-reactivity. 

[In these graphs](https://github.com/cedricusureau/HLA_graph/tree/master/data/graph_template), each node correspond to an allele and each link correspond to a strong MFI correlation between two alleles. 

We showed that strong MFI correlation between different antigens reflect epitopic similarity (see figure below), and we assumed that drawing graphs is a good way to display cross-reactivity interaction.

<p align="center">
  <img width="300" height="200" src="https://raw.githubusercontent.com/cedricusureau/HLA_graph/master/figures/eplet_corr.png">
</p>

Based on this model, we have implemented HLA Graph, a data visualization tool. Once user as uploaded datatable containing MFI values from SA1 or SA2 assay, HLA Graph workflow is following these steps :
   - Extract positive antigens toward given MFI Thresholds.
   - From empty graphs templates, highlight with shade of red the positive beads (proportional to MFI). Graphs templates for HLA-A, -B, -C, -DRB1, -DQB1, -DQA1, -DPB1 and -DPA1 are present in supplemental data.
   - Highlight in red the links between positive beads that are usually correlated.
   - From the eplets sequences provided by HLA Matchmaker, identify potentially immunoreactive eplet following specific rules. 

<p align="center">
  <img width="650" height="450" src="https://raw.githubusercontent.com/cedricusureau/HLA_graph/master/figures/HLA_graph_Flowcharts.png">
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
