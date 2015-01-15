![DOI](https://zenodo.org/badge/4998/sauloal/vcf_stats.svg "DOI")

# vcf_stats
## Stats for VCF files in standalone HTML5
http://sauloal.github.io/vcf_stats/

## Example
http://htmlpreview.github.io/?http://cdn.rawgit.com/sauloal/vcf_stats/master/vcf_stats_report.py_report.html

### Run
input file1.vcf file2.vcf filen.vcf
```
pyhton vcf_stats.py file1.vcf file2.vcf filen.vcf
```
output file1.vcf.json file2.vcf.json filen.vcf.json
```
python vcf_stats_report.py file1.vcf.json file2.vcf.json filen.vcf.json
```
output vcf_stats_report.py_report.html
```
open vcf_stats_report.py_report.html in your browser and select the desired file to see the report.
```
