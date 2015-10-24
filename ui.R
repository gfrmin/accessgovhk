library(shiny)
library(data.table)

shinyUI(
    fluidPage(
        titlePanel("Access to Information Officer contact information"),
        downloadButton('downloadData', 'Download this data (.csv)'),
        fluidRow(column(12,
                        dataTableOutput('teldirati')
                        )
                 )
    )
)

        
