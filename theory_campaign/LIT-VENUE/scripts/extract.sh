#!/bin/bash
# Convert local PDFs to text for grep-based reading (run via owls_run).
mkdir -p /tmp/litvenue_txt; cd Papers/Core_bibliography
for f in 01_* 02_* 06_* 08_* 09_* 10_* 11_* 12_* 14_* 18_* 22_* 23_* 24_* 25_* 29_* 31_*; do pdftotext -layout "$f" /tmp/litvenue_txt/${f:0:2}.txt; done
