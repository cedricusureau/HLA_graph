# Input files format 

 - Input files should have ".xls" or ".xlsx" extension. 
 - Empty MFI cells are considered to be equal to 0. 
 - Working template example could be download here
## Classe I format

 - __Two column__ : lists of alleles and corresponding MFI.
 - Contain __HLA-A__, __-B__ and/or __-C__ alleles in any order.
 
##### Compatible format example:  
 
 |Example 1|Example 2|
|--|--|
|<table> <tr><th>A\*01:01</th><th>500</th></tr><tr><td>A\*02:01</td><td>1500</td></tr><tr><td>A\*02:03</td><td>2000</td></tr><tr><td>...</td><td>...</td></tr><tr><td>A\*33:03</td><td>0</td></tr> </table>| <table> <tr><th>Allele</th><th>MFI</th></tr><tr><td>B\*15:01</td><td>500</td></tr><tr><td>...</td><td>...</td></tr> <tr><td>C*04:01</td><td> </td></tr><tr><td>C\*17:01</td><td> </td></tr><tr><td>B\*46:01</td><td>500</td></tr></table>|


 ## Classe II format
 
  - Two or three column file (see example below).
  - Contain __HLA-DR__, __-DQ__ and/or __-DP__ alleles in any orders.
  - __Empty MFI__ cells are considered to be __equal to 0__. 
 
 ##### Compatible format example:  
 
  |Example 1|Example 2|
|--|--|
|<table> <tr><th>DQA1\*02:01DQB1\*02:01</th><th>1000</th></tr><tr><td>DQA1\*03:01DQB1\*02:01</td><td>1500</td></tr><tr><td>DQA1\*01:02DQB1\*06:04</td><td>2000</td></tr><tr><td>...</td><td>...</td></tr><tr><td>DPA1\*02:01DPB1\*14:01</td><td>0</td></tr> </table>| <table> <tr><th>Allele 1</th><th>Allele 2</th><th>MFI</th></tr><tr><td>DRB3\*02:02</td><td></td><td>1500</td></tr><tr><td>...</td><td>...</td><td>...</td></tr> <tr><td></td><td></td><td> </td></tr><tr><td>DQA1\*02:01</td><td>DQB1*02:02</td><td>500</td></tr><tr><td>DPA1\*02:01</td><td>DPB1\*06:01</td><td>500</td></tr></table>|

__WARNING__: Alleles not present in the file will not be considered negative. Some eplets may therefore not be eliminated.