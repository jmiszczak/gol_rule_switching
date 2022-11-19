NL_VERSION=6.3.0

GENEX_CLASS = GenerateExample
CALCMEAN_CLASS = CalculateMeanLiving

CLASS_PATH = ${HOME}/Local/NetLogo/${NL_VERSION}/lib/app/netlogo-${NL_VERSION}.jar

build:
	javac -cp ${CLASS_PATH} ${GENEX_CLASS}.java
	javac -cp ${CLASS_PATH} ${CALCMEAN_CLASS}.java


realizations:
	ln -sf run.sh deterministic_realizations.sh 
	ln -sf run.sh random_realizations.sh 
	./deterministic_realizations.sh
	./random_realizations.sh

genex:
	parallel java -cp .:${CLASS_PATH} ${GENEX_CLASS} 64 50 {1} {2} 2 {3} {4} ::: true false ::: true false ::: 0.0 0.25 0.5 0.75 1.0 ::: `seq 4 8`

calcmean:
	parallel java -cp .:${CLASS_PATH} ${CALCMEAN_CLASS} 64 50 {1} {2} 2 {3} {4} >> living_data_250steps_200runs.csv ::: true false ::: true false ::: `seq 0 0.05 1` ::: `seq 4 9` 

