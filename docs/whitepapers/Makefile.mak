all: basis5lm basis5hm bianchi

basis5lm:
	latexmk -pdf -jobname=Basis5LM/build/Basis5LM Basis5LM/main.tex

basis5hm:
	latexmk -pdf -jobname=Basis5HM/build/Basis5HM Basis5HM/main.tex

bianchi:
	latexmk -pdf -jobname=Bianchi_Residual/build/BianchiResidual Bianchi_Residual/main.tex

clean:
	latexmk -C Basis5LM/main.tex
	latexmk -C Basis5HM/main.tex
	latexmk -C Bianchi_Residual/main.tex
