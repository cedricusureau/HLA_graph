# Input files format 

Every input files should have ".xls" or ".xlsx" extension. 

## Classe I format

 - __Two column__ (with or without column name) 
 - Contain HLA-A __and/or__ HLA-B __and/or__ HLA-C alleles in any orders.
 - __Empty MFI__ cells are considered to be __equal to 0__. 
 - __WARNING__: Alleles not present in the file will not be considered negative. Some eplets may therefore not be eliminated.
 
Compatible format:  
 
 |HLA-A Example|HLA-B & C example|
|--|--|
|<table> <tr><th>A*01:01</th><th>500</th></tr><tr><td>A\*02:01</td><td>1500</td></tr><tr><td>A\*02:03</td><td>2000</td></tr><tr><td>...</td><td>...</td></tr><tr><td>A\*33:03</td><td>0</td></tr> </table>| <table> <tr><th>Allele</th><th>MFI</th></tr><tr><td>B\*15:01</td><td>500</td></tr><tr><td>B\*15:02</td><td>1500</td></tr><tr><td>...</td><td>...</td></tr> <tr><td>C*04:01</td><td> </td></tr><tr><td>C\*17:01</td><td> </td></tr><tr><td>B\*46:01</td><td>500</td></tr></table>|

 