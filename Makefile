NL_VERSION=6.2.1

GENEX_CLASS = GenerateExample
CALC_CLASS = CalculateMeanLiving

CLASS_PATH = ${HOME}/Local/NetLogo/${NL_VERSION}/app/netlogo-${NL_VERSION}.jar

build:
	javac -cp ${CLASS_PATH} ${GENEX_CLASS}.java
	javac -cp ${CLASS_PATH} ${CALC_CLASS}.java

genex:
	parallel java -cp .:${CLASS_PATH} ${GENEX_CLASS} 64 50 {1} {2} 2 {3} {4} ::: true false ::: true false ::: 0.0 0.25 0.5 0.75 1.0 ::: `seq 4 8`

calc-mean:
	parallel java -cp .:${CLASS_PATH} ${CALC_CLASS} 64 50 {1} {2} 2 {3} {4} >>  living_data_250steps_500runs.csv  ::: true false ::: true false ::: `seq 0 0.01 1` ::: `seq 4 9` 

