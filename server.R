library(shiny)
library(data.table)

teldirati <- fread("teldirati.csv")
teldirati <- teldirati[,list(department, subdepartment, name, tel, fax, email, address, homepage)]
setnames(teldirati, c("Dept", "Subdept", "Name", "Telephone", "Fax", "Email", "Address", "Homepage"))

shinyServer(function(input, output) {
    output$teldir <- renderDataTable({
        teldirati
    })

    output$downloadData <- downloadHandler(
        filename = "teldirati.csv",
        content = function(file) {
            write.csv(teldirati, file)
        }
    )
})
