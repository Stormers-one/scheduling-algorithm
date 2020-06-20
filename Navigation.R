if(getwd()!="~/GitLab/odu_komban_schd_algorithm"){
  setwd("~/GitLab/odu_komban_schd_algorithm")
}
rmarkdown::render("Rmd/algorithm_generation.Rmd",output_file = "../algorithm_generation.pdf")

