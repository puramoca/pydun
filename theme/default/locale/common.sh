# Primitive way of translating strings for background images

declare -A LANGCODE
declare -A CONTAINERCODE

LANGCODE[Arabic]=ARA
LANGCODE[Bosnian]=BOS
LANGCODE[Bulgarian]=BUL
LANGCODE[Chinese]=ZHO
LANGCODE[Croatian]=HRV
LANGCODE[Czech]=CES
LANGCODE[Danish]=DAN
LANGCODE[Dutch]=NLD
LANGCODE[English]=ENG
LANGCODE[Filipino]=FIL
LANGCODE[Finnish]=FIN
LANGCODE[French]=FRA
LANGCODE[German]=DEU
LANGCODE[Hebrew]=HEB
LANGCODE[Hungarian]=HUN
LANGCODE[Norvegian]=NOR
LANGCODE[Polish]=POL
LANGCODE[Portuguese]=POR
LANGCODE[Romanian]=RON
LANGCODE[Serbian]=SRB
LANGCODE[Slovak]=SLK
LANGCODE[Slovenian]=SLV
LANGCODE[Spanish]=SPA
LANGCODE[Swedish]=SWE
LANGCODE[Tagalog]=TGL
LANGCODE[Turkish]=TUR

CONTAINERCODE[matroska]=MKV

export LANGCODE
export CONTAINERCODE
