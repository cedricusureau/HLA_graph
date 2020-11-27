# Input files format 

Every input files should have ".xls" or ".xlsx" extension. 

## Classe I format

 - __Two column__ (with or without column name) 
 - Contain HLA-A __and/or__ HLA-B __and/or__ HLA-C alleles in any orders.
 - __Empty MFI__ cells are considered to be __equal to 0__. 
 - __WARNING__: Alleles not present in the file will not be considered negative. Some eplets may therefore not be eliminated.
 
Compatible format: 

|HLA-A|HLA-B+C|
|--|--|
|<table> <tr><td>A\*02:01</th><th>2000</td></tr><tr><td>A\*02:03</td><td>2000</td></tr><tr><td>A*02:06</td><td>1500</td></tr><tr><td>...</td><td>...</td></tr><tr><td>A*80:01</td><td>0</td></tr><tr><td>A*33:03</td><td>500</td></tr></table>|<table> <tr><th>Allele</th><th>MFI</th></tr><tr><td>B*15:01</td><td>3000</td></tr>
 <tr><td>B*15:02</td><td>1500</td></tr>
  <tr><td>...</td><td>...</td></tr>
  <tr><td>C*04:01</td><td></td></tr>
  <tr><td>C*17:01</td><td></td></tr>
  <tr><td>B*40:06</td><td>500</td></tr>
 </table>|
 
 
 |Table 1|Table 2|
|--|--|
|<table> <tr><th>Table 1 Heading 1</th><th>Table 1 Heading 2</th></tr><tr><td>Row 1 Column 1</td><td>Row 1 Column 2</td></tr> </table>| <table> <tr><th>Table 2 Heading 1</th><th>Table 2 Heading 2</th></tr><tr><td>Row 1 Column 1</td><td>Row 1 Column 2</td></tr> </table>|

 