Set-Location $PSScriptRoot
latexmk -pdf -jobname=Basis5LM/build/Basis5LM Basis5LM/main.tex
latexmk -pdf -jobname=Basis5HM/build/Basis5HM Basis5HM/main.tex
latexmk -pdf -jobname=Bianchi_Residual/build/BianchiResidual Bianchi_Residual/main.tex
