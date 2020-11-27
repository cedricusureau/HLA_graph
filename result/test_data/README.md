# Input files format 

Every input files should have ".xls" or ".xlsx" extension. 

## Classe I format

 - __Two column__ (with or without column name) 
 - Contain HLA-A __and/or__ HLA-B __and/or__ HLA-C alleles in any orders.
 - __Empty MFI__ cells are considered to be __equal to 0__. 
 - __WARNING__: Alleles not present in the file will not be considered negative. Some eplets may therefore not be eliminated.
 
###Compatible format example:  
 
 |Example 1|Example 2|
|--|--|
|<table> <tr><th>A\*01:01</th><th>500</th></tr><tr><td>A\*02:01</td><td>1500</td></tr><tr><td>A\*02:03</td><td>2000</td></tr><tr><td>...</td><td>...</td></tr><tr><td>A\*33:03</td><td>0</td></tr> </table>| <table> <tr><th>Allele</th><th>MFI</th></tr><tr><td>B\*15:01</td><td>500</td></tr><tr><td>B\*15:02</td><td>1500</td></tr><tr><td>...</td><td>...</td></tr> <tr><td>C*04:01</td><td> </td></tr><tr><td>C\*17:01</td><td> </td></tr><tr><td>B\*46:01</td><td>500</td></tr></table>|

 ## Classe II format
 
  - __Two or three column__ (with or without column name)
  - __For two column file__, alpha and beta chain should follow this format :  DQA1\*02:01DQB1\*02:01
  - __For three column file__, DQ and QP alpha chain are in column 1 and beta chain is in column 2. DRB alleles are in column 1.
  - Contain HLA-DR __and/or__ HLA-DQ __and/or__ HLA-DP alleles in any orders.
  - __Empty MFI__ cells are considered to be __equal to 0__. 
  - __WARNING__: Alleles not present in the file will not be considered negative. Some eplets may therefore not be eliminated.
 
 ###Compatible format example:  
 
  |Example 1|Example 2|
|--|--|
|<table> <tr><th>DQA1\*02:01DQB1\*02:01</th><th>1000</th></tr><tr><td>DQA1\*03:01DQB1\*02:01</td><td>1500</td></tr><tr><td>DQA1\*01:02DQB1\*06:04</td><td>2000</td></tr><tr><td>...</td><td>...</td></tr><tr><td>DPA1\*02:01DPB1\*14:01</td><td>0</td></tr> </table>| <table> <tr><th>Allele 1</th><th>Allele 2</th><th>MFI</th></tr><tr><td>DRB1\*04:03</td><td> </td><td>1000</td></tr><tr><td>DRB3\*02:02</td><td></td><td>1500</td></tr><tr><td>...</td><td>...</td><td>...</td></tr> <tr><td></td><td></td><td> </td></tr><tr><td>DQA1\*02:01</td><td>DQB1*02:02</td><td>500</td></tr><tr><td>DPA1\*02:01</td><td>DPB1\*06:01</td><td>500</td></tr></table>|
